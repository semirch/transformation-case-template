#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restliste.py: sammelt jeden offenen Punkt aus den Notizen des Falls in eine Liste.

Module, die in 00 Steuerung/fall.md als 'nicht benötigt' stehen, und Muster zählen nicht.

Die Kategorien werden anhand von Stichwörtern vorgeschlagen. Nicht erkannte Punkte bleiben unsortiert und müssen fachlich geprüft werden.

Aufruf:  python3 Werkzeuge/restliste.py
"""
import os, pathlib, re, datetime, collections, urllib.parse

HIER = pathlib.Path(__file__).parent
from vault import VAULT, LANDKARTE, fall_md

ZIEL = LANDKARTE / "restliste.md"

SORTEN = [
    # Reihenfolge ist Priorität: der erste Treffer gewinnt.
    ("Dauerhafter Vorbehalt",
                     r"ist nicht die arbeitsgrundlage|ist bewusst|bleibt bestehen|"
                     r"sind `?generiert`?|ist `?generiert`?|nicht \u00fcbertragbar|"
                     r"aus dem \u00fcbungsdatensatz|nicht unabh\u00e4ngig|"
                     r"wer sie weiterverwendet|muss gepflegt werden"),
    ("Noch nicht fällig",
                     r"kann vor|erste pr\u00fcfung liegt|entsteht mit|entsteht erst|"
                     r"ist je gepr\u00fcft|nie gelaufen|liegt sechs monate|"
                     r"wird erst|noch nie"),
    ("Freigabe",     r"nicht freigegeben|ist selbst nicht freigegeben|"
                     r"angenommen ist noch keines"),
    ("Auskunft",     r"auskunft|nachlesen|nachsehen|aktenzugang|ob \u00fcberhaupt|"
                     r"ist ein|gibt es|tr\u00e4gt das unternehmen|belegen|quelle pr\u00fcfen|"
                     r"nicht gepr\u00fcft|im original|belegbar"),
    ("Termin",       r"termin|frist|vor woche|bis woche|woche \d|monat \d|"
                     r"vorziehen|verschoben|nachzuziehen|nachziehen"),
    ("Stelle",       r"unbesetzt|vakant|besetzung|stelle|kapazit\u00e4t|niemand|"
                     r"ohne namen|wer tr\u00e4gt|rolle ohne|schafft keine stunden"),
    ("Entscheidung", r"entschieden|entscheidung|vorschlag|beschlossen|"
                     r"verhandeln|abzustimmen|abstimmen|zu kl\u00e4ren|kl\u00e4ren|"
                     r"mitbestimmung|abnahme|best\u00e4tigen"),
    ("Arbeit",       r"erheben|eintragen|rendern|durchf\u00fchren|erstellen|"
                     r"festlegen|aufnehmen|schlie\u00dfen|ausarbeiten|"
                     r"pr\u00e4zisieren|erg\u00e4nzen|schreiben|f\u00fchren"),
]

def sorte(text):
    t = text.lower()
    for name, muster in SORTEN:
        if re.search(muster, t):
            return name
    return "noch nicht sortiert"

def umlinken(text, quelle):
    """Links im Punkt gelten relativ zur Quelldatei; die Restliste liegt woanders."""
    ziel_ordner = ZIEL.parent
    def ersetze(m):
        h = m.group(2)
        if re.match(r"^[a-z]+:", h) or h.startswith("#"):
            return m.group(0)
        pfad, _, anker = h.partition("#")
        absolut = (quelle.parent / urllib.parse.unquote(pfad)).resolve()
        neu = urllib.parse.quote(os.path.relpath(absolut, ziel_ordner))
        return f"[{m.group(1)}]({neu}{'#' + anker if anker else ''})"
    return re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", ersetze, text)

def sammeln():
    treffer = collections.defaultdict(list)
    dateien = fall_md()
    for f in dateien:
        if f.name == "restliste.md":
            continue
        zeilen = f.read_text(encoding="utf-8").split("\n")
        i = 0
        while i < len(zeilen):
            if zeilen[i].startswith("- [ ] "):
                punkt = zeilen[i][6:]
                # Fortsetzungszeilen einsammeln
                j = i + 1
                while j < len(zeilen) and zeilen[j].startswith("      "):
                    punkt += " " + zeilen[j].strip(); j += 1
                punkt = re.sub(r"\s+", " ", punkt)
                pfad = f.relative_to(VAULT)
                treffer[sorte(punkt)].append((str(pfad), umlinken(punkt, f)))
                i = j
            else:
                i += 1
    return treffer

def schreiben(treffer):
    gesamt = sum(len(v) for v in treffer.values())
    z = [f"# Restliste: jeder offene Punkt an einem Ort\n",
         f"**Stand:** {datetime.date.today().strftime('%d.%m.%Y')}",
         "**Erzeugt von:** `Werkzeuge/restliste.py`. **Nicht von Hand pflegen:** Wer einen",
         "Punkt schließt, schließt ihn in der Datei, in der er steht, und erzeugt",
         "diese Liste neu.\n",
         f"**{gesamt} offene Punkte.** Das ist kein Mangel, sondern der Stand:",
         "Eine Ablage ohne offene Punkte hat aufgehört, sie aufzuschreiben.\n",
         "**Aufgabenarten:** Auskunft, Termin, Entscheidung und Stelle; zusätzlich:",
         "- **Arbeit**: jemand muss etwas tun, aber niemand etwas entscheiden.",
         "- **Freigabe**: dieselbe Sitzung schließt sie alle auf einmal.",
         "- **Noch nicht fällig**: kein Versäumnis, der Zeitpunkt ist nicht da.",
         "- **Dauerhafter Vorbehalt**: wird nie geschlossen und muss sichtbar bleiben.\n",
         "**Die letzten beiden sind gar nicht offen.** Sie standen unter `## Offen`,",
         "weil die Ablage keinen anderen Ort dafür hat, und blähen jede Zählung",
         "auf, die nach offenen Punkten fragt.\n",
         "## Verteilung\n",
         "| Sorte | Anzahl | Was sie kostet |", "|---|---:|---|"]
    kosten = {"Auskunft": "Stunden: jemand weiß es, er wurde nicht gefragt",
              "Termin": "eine Sitzung: die Zuständigkeit gibt es",
              "Stelle": "Monate: die Rolle gibt es nicht",
              "Entscheidung": "eine Entscheidung",
              "Arbeit": "Stunden bis Tage: niemand muss entscheiden",
              "Freigabe": "eine Sitzung, für alle zusammen",
              "Noch nicht fällig": "nichts: der Zeitpunkt ist nicht da",
              "Dauerhafter Vorbehalt": "nichts: wird nie geschlossen",
              "noch nicht sortiert": "unbekannt: erst ansehen"}
    REIHE = ["Auskunft", "Termin", "Entscheidung", "Arbeit", "Freigabe",
             "Stelle", "Noch nicht fällig", "Dauerhafter Vorbehalt",
             "noch nicht sortiert"]
    for name in REIHE:
        if treffer.get(name):
            z.append(f"| **{name}** | {len(treffer[name])} | {kosten[name]} |")
    REIHE = ["Auskunft", "Termin", "Entscheidung", "Arbeit", "Freigabe",
             "Stelle", "Noch nicht fällig", "Dauerhafter Vorbehalt",
             "noch nicht sortiert"]
    for name in REIHE:
        if not treffer.get(name):
            continue
        z.append(f"\n## {name}: {len(treffer[name])} Punkte\n")
        nach_datei = collections.defaultdict(list)
        for pfad, punkt in treffer[name]:
            nach_datei[pfad].append(punkt)
        for pfad in sorted(nach_datei):
            z.append(f"\n**[{pfad}]({urllib.parse.quote(os.path.relpath(VAULT / pfad, ZIEL.parent))})**\n")
            for p in nach_datei[pfad]:
                z.append(f"- {p}")
    ZIEL.write_text("\n".join(z) + "\n", encoding="utf-8")
    return gesamt

if __name__ == "__main__":
    t = sammeln()
    n = schreiben(t)
    print(f"restliste.md geschrieben: {n} offene Punkte")
    REIHE = ["Auskunft", "Termin", "Entscheidung", "Arbeit", "Freigabe",
             "Stelle", "Noch nicht fällig", "Dauerhafter Vorbehalt",
             "noch nicht sortiert"]
    for name in REIHE:
        if t.get(name):
            print(f"  {len(t[name]):3}  {name}")
