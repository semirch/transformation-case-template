# Start

**Dieses Repo ist für echte Falldaten gebaut und muss privat bleiben.** Bevor das erste Dokument, der erste Name oder die erste Zahl hineinkommt, auch in ein Chatfenster, wird die [Datenverarbeitung](00%20Steuerung/datenverarbeitung.md) geklärt.

Zweck und Aufbau erklärt die [README](README.md). Hier stehen die Schritte.

## Einen Fall beginnen

1. Auf GitHub aus der Vorlage ein neues **privates** Repo erzeugen („Use this template") und lokal klonen.
2. Im Terminal im Repo-Ordner: `python3 Werkzeuge/neuer-fall.py`. Das Skript fragt Organisation, Fallart, Datenlage und Methoden-Repo ab, setzt den Fall auf `aktiv` und schaltet die Sperre scharf. Bei einem gemischten oder fiktiven Fall setzt es stattdessen in jede Notiz den Hinweis, dass die Angaben konstruiert sind; Schritt 3 entfällt dann.
3. Mit dem Assistenten die [Datenverarbeitung](00%20Steuerung/datenverarbeitung.md) klären und bestätigen. Bis dahin lassen die Hooks keine andere Änderung und keinen Commit zu. Die Änderungen des Startskripts werden deshalb zusammen mit der geklärten Datenverarbeitung committet.
4. In [fall.md](00%20Steuerung/fall.md) Auftrag und Umfang festhalten und entscheiden, welche Module dieser Fall braucht.
5. Im [Erhebungsplan](01%20Erhebung/erhebungsplan.md) festlegen, welche Angaben von wem kommen. Erst dann sammeln.

## Im laufenden Fall

| Wenn | Dann |
|---|---|
| ein Dokument oder Gespräch dazukommt | Kennung im [Quellenverzeichnis](01%20Erhebung/quellenverzeichnis.md), Auszug anlegen, Aussagen in die führende Notiz |
| eine Angabe fehlt | Zeile im [Erhebungsplan](01%20Erhebung/erhebungsplan.md) |
| etwas angenommen werden muss | Zeile in [annahmen.md](00%20Steuerung/annahmen.md), mit Bandbreite |
| ein neues Vorhaben auftaucht | [Muster](03%20Vorhaben/_muster-vorhaben.md) kopieren, im [Portfolio](03%20Vorhaben/portfolio.md) eintragen |
| etwas entschieden wurde | Zeile in [entscheidungen.md](00%20Steuerung/entscheidungen.md) |
| sich das Bild der Organisation ändert | Zeile in [ereignisse.md](00%20Steuerung/ereignisse.md) |
| eine Methode nicht passt | hier abweichen, in der [Methodenrückmeldung](00%20Steuerung/methodenrueckmeldung.md) festhalten |
| eine Analyse steht | die passende [Gegenprüfung](11%20Gegenpr%C3%BCfung/Challenge-Register.md) fahren |
| in einem gemischten oder fiktiven Fall eine Notiz neu entsteht | `python3 Werkzeuge/kennzeichnung.py` setzt den Hinweis |
| viel geändert wurde | `python3 Werkzeuge/landkarte-erzeugen.py` und `python3 Werkzeuge/restliste.py` |

Überblick: [Wie die Teile zusammenhängen](00%20Steuerung/Landkarte/Organisation%20vernetzt.md), [Restliste](00%20Steuerung/Landkarte/restliste.md), [Informationsbestand](00%20Steuerung/Landkarte/Informationsbestand.md).

## Die Vorlage selbst verbessern

Solange `fallstatus: vorlage` in `fall.md` steht, sind die Hooks ohne Wirkung und die Vorlage lässt sich normal bearbeiten. Verbesserungen gehören in das Vorlagen-Repo, nicht in einen laufenden Fall.
