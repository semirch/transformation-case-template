"""Erzeugt die Landkarte des Falls: wer und was in der Organisation mit wem
zusammenhängt, welche Informationen gesammelt sind und welche Bezüge sie haben.

Schreibt nach 00 Steuerung/Landkarte/:
  Rollen/, Gremien/, Systeme/   je Knoten eine Notiz — Steckbrief aus dem
                                Unternehmensprofil, wo er vorkommt, womit er
                                zusammen vorkommt
  Informationsbestand.md        je Datei Stand, Herkunftskennzeichen, Offenes
  Bezüge.md                     je Datei die lokalen Links hinein und hinaus

Nicht von Hand pflegen: alles hier wird bei jedem Lauf neu gezählt. Ausnahme ist
'Organisation vernetzt.md'. Nach jeder größeren Änderung neu laufen lassen:
  python3 Werkzeuge/landkarte-erzeugen.py
"""
import collections, datetime, os, re, sys, unicodedata, urllib.parse
from vault import VAULT, LANDKARTE, HERKUNFT, alle_md

MARKE = "<!-- erzeugt von landkarte-erzeugen.py -->"
HEUTE = datetime.date.today().strftime("%d.%m.%Y")

# Knoten: Name, Suchmuster, Steckbrief-Quelle (Datei, Tabellenkopf, erste Zelle beginnt mit, Spalten)
ROLLE = ("menschen.md", "| Rolle |", ["Person", "Formaler Einfluss", "Informeller Einfluss", "Haltung zum Vorhaben (Quelle)", "Was diese Rolle beschäftigt"])
GREMIUM = ("menschen.md", "| Name | Mitglieder", ["Mitglieder (Rollen)", "Rhythmus", "Was dort entschieden wird", "Herkunft"])
SYSTEM = ("systeme-daten.md", "| Name | Zweck", ["Zweck", "Betrieb (intern, Anbieter)", "Schnittstellen", "Verantwortliche Rolle", "Herkunft"])

# Die Knoten des Falls stehen in knoten.py, nicht hier — so bleibt dieses
# Skript für jeden Fall dasselbe.
from knoten import KNOTEN as _KNOTEN
_QUELLE = {"rolle": ROLLE, "gremium": GREMIUM, "system": SYSTEM, None: None}
KNOTEN = {art: [(n, m, _QUELLE[q], a) for n, m, q, a in liste] for art, liste in _KNOTEN.items()}


def nfc(t):
    return unicodedata.normalize("NFC", t)


def rel(von, nach):
    """Relativer, für Obsidian kodierter Link von Datei 'von' zu Datei 'nach'."""
    return urllib.parse.quote(os.path.relpath(nach, von.parent))


def titel(p):
    for z in p.read_text(encoding="utf-8").split("\n"):
        if z.startswith("# "):
            return z[2:].strip()
    return p.stem


def stand_von(t):
    """Stand aus dem Dateikopf: **Stand:** TT.MM.JJJJ, Stand: JJJJ-MM-TT oder stand: im Frontmatter."""
    m = re.search(r"(?:\*\*Stand:\*\*|^Stand:?|^stand:)\s*(\d{2}\.\d{2}\.\d{4}|\d{4}-\d{2}-\d{2})", t, re.M)
    if not m:
        return "—"
    d = m.group(1)
    return f"{d[8:10]}.{d[5:7]}.{d[:4]}" if "-" in d else d


def steckbrief(quelle):
    datei, kopf, anfang, spalten = quelle[0], quelle[1], quelle[3], quelle[2]
    pfad = next(VAULT.glob(f"02 Organisation/{datei}"))
    zeilen, koepfe, drin = [], None, False
    for l in pfad.read_text(encoding="utf-8").split("\n"):
        if l.startswith(kopf):
            koepfe = [z.strip() for z in l.strip("|").split("|")]; drin = True; continue
        if drin:
            if l.startswith("|---"):
                continue
            if not l.startswith("|"):
                break
            zeilen.append([z.strip() for z in l.strip("|").split("|")])
    for z in zeilen:
        if z[0].startswith(anfang):
            werte = dict(zip(koepfe, z))
            return pfad, [(s, werte[s]) for s in spalten if werte.get(s)]
    return pfad, []


def main():
    dateien = [p for p in alle_md() if LANDKARTE not in p.parents]
    texte = {p: p.read_text(encoding="utf-8") for p in dateien}

    # ── Knoten: wo kommt wer vor ──────────────────────────────────────────
    # Erzeugte Sammeldateien wiederholen andere Dateien und würden doppelt zählen.
    abgeleitet = {"restliste.md"}
    quellen = {p: t for p, t in texte.items() if p.name not in abgeleitet}
    vorkommen = {}
    for art, liste in KNOTEN.items():
        for name, muster, quelle, anfang in liste:
            rx = re.compile(muster)
            vorkommen[name] = {p: len(rx.findall(t)) for p, t in quellen.items() if rx.search(t)}

    # Zusammen vorkommen: gemeinsame Dateien je Knotenpaar
    namen = list(vorkommen)
    gemeinsam = collections.defaultdict(dict)
    for a in namen:
        for b in namen:
            if a != b:
                n = len(set(vorkommen[a]) & set(vorkommen[b]))
                if n:
                    gemeinsam[a][b] = n
    art_von = {name: art for art, liste in KNOTEN.items() for name, *_ in liste}

    for art in KNOTEN:
        ziel = LANDKARTE / art
        ziel.mkdir(parents=True, exist_ok=True)
        for alt in ziel.glob("*.md"):
            if MARKE in alt.read_text(encoding="utf-8"):
                alt.unlink()

    for art, liste in KNOTEN.items():
        for name, muster, quelle, anfang in liste:
            p = LANDKARTE / art / f"{name}.md"
            z = [f"# {name}", "", MARKE,
                 f"**Stand:** {HEUTE} · erzeugt von `Werkzeuge/landkarte-erzeugen.py`, nicht von Hand pflegen.",
                 f"**Art:** {art[:-1] if art != 'Gremien' else 'Gremium'} · zurück zur [Organisationskarte]({rel(p, LANDKARTE / 'Organisation vernetzt.md')})",
                 ""]
            if quelle:
                qpfad, felder = steckbrief((quelle[0], quelle[1], quelle[2], anfang))
                z.append(f"## Steckbrief")
                z.append("")
                z.append(f"Aus [{qpfad.name}]({rel(p, qpfad)}). Maßgeblich bleibt das Herkunftskennzeichen dort.")
                z.append("")
                if not felder:
                    sys.exit(f"Steckbrief für {name} nicht gefunden ({quelle[0]}, beginnt mit {anfang!r}).")
                for s, w in felder:
                    z.append(f"- **{s}:** {w}")
                z.append("")
            else:
                z += ["## Steckbrief", "",
                      "Kein eigener Eintrag in 02 Organisation: der Knoten entsteht erst in den Analysen. "
                      "Was sie ist, steht in den Dateien unten, die meisten Nennungen zuerst.", ""]
            nach = gemeinsam.get(name, {})
            if nach:
                z += ["## Kommt oft zusammen vor mit", "",
                      "Gezählt: in wie vielen Dateien beide genannt sind. Das ist Nähe im Material, "
                      "keine belegte Beziehung in der Organisation.", ""]
                for b, n in sorted(nach.items(), key=lambda x: -x[1])[:8]:
                    z.append(f"- [{b}]({rel(p, LANDKARTE / art_von[b] / (b + '.md'))}) — {n} Dateien")
                z.append("")
            z += ["## Kommt vor in", "", "| Datei | Bereich | Nennungen |", "|---|---|---|"]
            for d, n in sorted(vorkommen[name].items(), key=lambda x: (-x[1], x[0].name)):
                bereich = d.relative_to(VAULT).parts[0]
                z.append(f"| [{titel(d)}]({rel(p, d)}) | {bereich} | {n} |")
            if not vorkommen[name]:
                z.append("| — | — | 0 |")
            z.append("")
            p.write_text("\n".join(z), encoding="utf-8")

    # ── Informationsbestand ───────────────────────────────────────────────
    # Gezählt werden nur Kennzeichen in Backticks. So zählt der erklärende Text nicht mit.
    p = LANDKARTE / "Informationsbestand.md"
    z = ["# Informationsbestand", "", MARKE,
         f"**Stand:** {HEUTE} · erzeugt von `Werkzeuge/landkarte-erzeugen.py`, nicht von Hand pflegen.",
         "",
         "Was gesammelt ist, je Notiz: Stand, wie oft jedes der fünf Herkunftskennzeichen vorkommt, "
         "und was offen ist. **Die Zählung sagt, wie viel von welcher Sorte in einer Notiz steckt, "
         "nicht, welcher einzelne Wert belegt ist.** Maßgeblich bleibt das Kennzeichen am Wert. "
         "Ein Strich beim Stand heißt: Die Notiz hat noch kein Datum im Kopf.",
         ""]
    kopf = "| Notiz | Stand | " + " | ".join(HERKUNFT) + " | Offen |"
    summe = collections.Counter()
    for bereich in sorted({d.relative_to(VAULT).parts[0] for d in dateien}):
        teil = [d for d in dateien if d.relative_to(VAULT).parts[0] == bereich
                and len(d.relative_to(VAULT).parts) > 1 and d.name != "README.md"
                and not d.name.startswith("_muster")]
        if bereich == "Werkzeuge" or not teil:
            continue
        z += [f"## {bereich}", "", kopf, "|---" * (len(HERKUNFT) + 3) + "|"]
        for d in teil:
            t = texte[d]
            c = {k: len(re.findall("`" + re.escape(k) + "`", t)) for k in HERKUNFT}
            offen = len(re.findall(r"^\s*- \[ \] ", t, re.M))
            summe.update(c); summe["offen"] += offen
            z.append(f"| [{titel(d)}]({rel(p, d)}) | {stand_von(t)} | "
                     + " | ".join(str(c[k]) for k in HERKUNFT) + f" | {offen} |")
        z.append("")
    z += ["## Summe", "",
          ", ".join(f"{summe[k]} × `{k}`" for k in HERKUNFT)
          + f", {summe['offen']} offene Punkte. Die sortierte Liste steht in "
          f"[restliste.md]({rel(p, LANDKARTE / 'restliste.md')}).",
          ""]
    p.write_text("\n".join(z), encoding="utf-8")

    # Lokale Verbindungen zwischen den Notizen.
    links = re.compile(r"\]\(([^)\s]+)\)")
    rein = collections.Counter()
    raus = {}
    for d, text in texte.items():
        targets = set()
        for h in links.findall(text):
            if ":" in h or h.startswith("#"):
                continue
            target = (d.parent / urllib.parse.unquote(h.split("#")[0])).resolve()
            if target in texte and target != d:
                targets.add(target)
        raus[d] = targets
        rein.update(targets)
    p = LANDKARTE / "Bezüge.md"
    z = ["# Lokale Bezüge", "", MARKE,
         f"**Stand:** {HEUTE} · automatisch erzeugt.", "",
         "Verbindungen zwischen Notizen sind Prüfbeziehungen, keine Nachweise einer Ursache.", "",
         "| Notiz | Eingehende Verweise | Ausgehende Verweise |", "|---|---|---|"]
    for d in dateien:
        z.append(f"| [{titel(d)}]({rel(p, d)}) | {rein[d]} | {len(raus[d])} |")
    p.write_text("\n".join(z) + "\n", encoding="utf-8")

    n = sum(len(l) for l in KNOTEN.values())
    print(f"Landkarte geschrieben: {n} Knoten, {len(dateien)} Dateien im Informationsbestand und in den Bezügen.")
    leer = [k for k, v in vorkommen.items() if not v]
    if leer:
        print("  ohne Vorkommen:", ", ".join(leer))


if __name__ == "__main__":
    main()
