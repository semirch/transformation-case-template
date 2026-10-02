---
typ: sperre
status: offen                # offen, geklärt
geklaert_am:
bestaetigt_durch:
---

# Datenverarbeitung: was mit den Daten dieses Falls geschehen darf

**Solange hier `status: offen` steht, wird an keiner anderen Datei gearbeitet.**

Diese Notiz wird geklärt, bevor Falldaten in das Repo oder in ein Chatfenster gelangen. Die Fragen lassen sich ohne Falldaten beantworten: Gefragt ist die Regel, nicht das Dokument. Eine Antwort „weiß ich nicht" ist zulässig und führt zu einer Zeile unter Offen, nicht zu einer Annahme.

## 1. Grundlage

| Frage | Antwort |
|---|---|
| Auf welcher Grundlage liegen die Daten bei mir (Arbeitsvertrag, Beratungsvertrag, Vertraulichkeitsvereinbarung, Übungsfall)? | |
| Gibt es Regeln der Organisation zum Einsatz von KI-Werkzeugen? Was sagen sie? | |
| Wer in der Organisation kann eine offene Frage dazu entscheiden? | |

## 2. Werkzeuge

Je Werkzeug eine Zeile. Was hier nicht steht, sieht keine Falldaten.

| Werkzeug | Vertragsart und Anbieter | Darf sehen: Auszüge | Darf sehen: Rohmaterial | Darf sehen: Personenbezogenes | Wird mit den Eingaben trainiert? |
|---|---|---|---|---|---|

## 3. Ablage und Zugriff

| Frage | Antwort |
|---|---|
| Wo liegt dieses Repo (Dienst, privat oder Organisation)? | |
| Wer hat Zugriff? | |
| Bleibt Rohmaterial lokal (Voreinstellung über `.gitignore`), oder darf es ins Repo? | |
| Auf welchen Geräten liegt eine Kopie? | |

## 4. Personen

| Frage | Antwort |
|---|---|
| Dürfen Klarnamen von Beschäftigten geführt werden? | |
| Dürfen Gespräche aufgezeichnet oder transkribiert werden, und wissen die Befragten davon? | |
| Gibt es eine Arbeitnehmervertretung, die einzubinden ist? | |

## 5. Ende

| Frage | Antwort |
|---|---|
| Wann wird das Repo gelöscht oder übergeben? | |
| Was darf ich als Arbeitsprobe behalten, in welcher Form? | |
| Darf eine neutrale Fassung weitergegeben werden? | |

## Bestätigung

Den Status setzt nur die Person, die den Fall verantwortet, mit Datum und Namen im Frontmatter. Ändert sich eine Antwort, etwa ein neues Werkzeug, wird die Zeile ergänzt und die Änderung in [entscheidungen.md](entscheidungen.md) festgehalten.

## Offen

- [ ] Alle fünf Abschnitte klären und bestätigen.
