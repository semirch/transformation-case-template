# Werkzeuge

Python 3.9 oder neuer, ohne zusätzliche Pakete. Alle Skripte arbeiten ausschließlich innerhalb dieses Repos. Im Terminal im Repo-Ordner ausführen, unter Windows je nach Installation mit `py -3` statt `python3`.

| Skript | Wozu | Wann |
|---|---|---|
| `neuer-fall.py` | Macht aus der Vorlage einen Fall: setzt Organisation, Beginn und Methodenstand, schaltet die Sperre scharf | einmal, am Anfang |
| `sperre.py` | Zeigt, ob die Sperre aktiv ist. Wird außerdem von den beiden Hooks aufgerufen | bei Bedarf |
| `landkarte-erzeugen.py` | Schreibt Informationsbestand, Bezüge und je Rolle, Gremium und System eine Knotennotiz nach `00 Steuerung/Landkarte/` | nach größeren Änderungen |
| `restliste.py` | Sammelt alle offenen Punkte in eine sortierte Liste | nach größeren Änderungen |

`vault.py` und `knoten.py` sind Hilfsdateien. In `knoten.py` stehen die Rollen, Gremien und Systeme, die die Landkarte als Knoten führen soll. Dort eintragen, sobald `02 Organisation/menschen.md` und `systeme-daten.md` gefüllt sind.

## Die Sperre

Solange `fallstatus: aktiv` in `00 Steuerung/fall.md` steht und `00 Steuerung/datenverarbeitung.md` nicht `status: geklärt` trägt, darf nur die Datenverarbeitungsnotiz geändert werden. Zwei Hooks setzen das durch:

- **Im Assistenten:** `.claude/settings.json` ruft vor jedem Schreibzugriff `sperre.py --hook` auf. Gilt für Claude Code. Andere Assistenten brauchen einen eigenen Eintrag oder halten sich an die Regel in `AGENTS.md`.
- **In Git:** `.githooks/pre-commit` ruft `sperre.py --commit` auf. Muss je Klon einmal aktiviert werden: `git config core.hooksPath .githooks`. Das Startskript erledigt das.

Was die Hooks nicht verhindern: Schreibzugriffe über die Shell, und Falldaten, die in ein Chatfenster eingefügt werden.
