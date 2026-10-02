#!/usr/bin/env python3
"""Kennzeichnet einen fiktiven oder gemischten Fall in jeder Notiz.

  python3 Werkzeuge/kennzeichnung.py            setzt oder erneuert den Hinweis in allen Notizen
  python3 Werkzeuge/kennzeichnung.py --pruefen  prüft nur, für den Git-Hook

Bei datenlage "gemischt" oder "fiktiv" (00 Steuerung/fall.md) steht unter der ersten
Überschrift jeder Notiz ein Hinweis, damit niemand die Angaben für echte oder
entwendete Daten hält, auch wer nur eine einzelne Datei sieht. Zusätzlich darf in
solchen Fällen kein Wert als `intern belegt` gekennzeichnet sein: Interne Belege
gibt es dort nicht.
"""
import re, sys
from vault import VAULT, MARKE_DATENLAGE, alle_md, datenlage, hinweis


def mit_hinweis(text, zeile):
    """Setzt die Hinweiszeile unter die erste Überschrift, ersetzt eine vorhandene."""
    zeilen = [z for z in text.split("\n") if MARKE_DATENLAGE not in z]
    kopf = 0
    if zeilen and zeilen[0].strip() == "---":
        kopf = next((i for i in range(1, len(zeilen)) if zeilen[i].strip() == "---"), 0) + 1
    ziel = next((i for i in range(kopf, len(zeilen)) if zeilen[i].startswith("# ")), None)
    if ziel is None:
        zeilen[kopf:kopf] = [zeile, ""]
    else:
        nach = ziel + 1
        while nach < len(zeilen) and not zeilen[nach].strip():
            nach += 1
        zeilen[ziel + 1:nach] = ["", zeile, ""]
    return "\n".join(zeilen)


def main():
    zeile = hinweis()
    if not zeile:
        # Wurde die Datenlage auf echt gestellt, verschwinden alte Hinweise.
        weg = 0
        if "--pruefen" not in sys.argv:
            for p in alle_md():
                t = p.read_text(encoding="utf-8")
                if any(z.startswith("> " + MARKE_DATENLAGE) for z in t.split("\n")):
                    neu = re.sub(r"\n> " + re.escape(MARKE_DATENLAGE) + r"[^\n]*\n\n?", "\n", t)
                    p.write_text(neu, encoding="utf-8"); weg += 1
        print("Datenlage echt oder leere Vorlage: kein Hinweis nötig."
              + (f" {weg} alte Hinweise entfernt." if weg else ""))
        return 0
    pruefen = "--pruefen" in sys.argv
    fehlt, intern, gesetzt = [], [], 0
    for p in alle_md():
        t = p.read_text(encoding="utf-8")
        rel = p.relative_to(VAULT)
        # Tabellenzeilen im Fall selbst: dort steht das Kennzeichen an einem Wert.
        if len(rel.parts) > 1 and rel.parts[0] != "Werkzeuge" and \
           any("`intern belegt`" in z for z in t.split("\n") if z.startswith("|")):
            intern.append(str(rel))
        if zeile in t:
            continue
        if pruefen:
            fehlt.append(str(rel))
        else:
            p.write_text(mit_hinweis(t, zeile), encoding="utf-8"); gesetzt += 1
    if pruefen:
        if fehlt:
            print(f"Datenlage {datenlage()}: In {len(fehlt)} Notizen fehlt der Hinweis, etwa: "
                  + ", ".join(fehlt[:6]) + ".\nBeheben mit: python3 Werkzeuge/kennzeichnung.py", file=sys.stderr)
        if intern:
            print(f"Datenlage {datenlage()}: Als `intern belegt` gekennzeichnete Werte in: "
                  + ", ".join(intern[:6]) + ".\nIn einem solchen Fall gibt es keine internen Belege. "
                  "Kennzeichen prüfen oder die Datenlage in fall.md bewusst auf echt ändern.", file=sys.stderr)
        return 1 if (fehlt or intern) else 0
    print(f"Hinweis gesetzt in {gesetzt} Notizen (Datenlage {datenlage()}).")
    if intern:
        print("ACHTUNG, `intern belegt` kommt vor in: " + ", ".join(intern[:6]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
