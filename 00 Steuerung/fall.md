---
typ: fall
fallstatus: vorlage          # vorlage, aktiv, abgeschlossen
organisation: "‹Organisation›"
fallart:                     # anstellung, beratung, übung
datenlage: echt              # echt, gemischt, fiktiv
beginn:
methoden_repo:
methoden_stand:
module:
  04 Diagnose: offen                    # offen, aktiv, nicht benötigt
  05 Ziele und Programm: offen
  06 Menschen und Kommunikation: offen
  07 Governance und Recht: offen
  08 Plattform und Kosten: offen
  09 Daten: offen
  10 Synthese: offen
---

# Der Fall: ‹Organisation›

**Stand:** TT.MM.JJJJ

Diese Notiz sagt, worum es geht, wie weit der Auftrag reicht und welche Teile der Ablage dieser Fall braucht. Sie ist die erste, die ein Assistent liest.

## Auftrag

| Frage | Antwort | Herkunft |
|---|---|---|
| Wer hat beauftragt, in welcher Rolle? | | |
| Welche Entscheidung soll am Ende möglich sein? | | |
| Bis wann? | | |
| Wer nimmt das Ergebnis ab? | | |
| Was ist ausdrücklich nicht Teil des Auftrags? | | |

## Datenlage

Das Feld `datenlage` im Frontmatter sagt, woraus dieser Fall besteht. Es wird beim Anlegen gesetzt und danach nicht still geändert.

| Wert | Bedeutung |
|---|---|
| `echt` | Reale Organisation, mit internen Dokumenten und Gesprächen |
| `gemischt` | Reale, benannte Organisation, aber nur öffentliche Angaben, Annahmen und erfundene Ergänzungen. Keine internen Daten |
| `fiktiv` | Erfundene Organisation. Alles ist konstruiert |

Bei `gemischt` und `fiktiv` trägt jede Notiz einen Hinweis unter der Überschrift, siehe [AGENTS.md](../AGENTS.md), Abschnitt 11.

## Umfang

Welche Bereiche, Standorte und Gruppen der Organisation untersucht werden, und welche nicht. Eine Grenze, die hier nicht steht, wird später überschritten.

## Module

Im Frontmatter je Modul einen der drei Werte setzen. `nicht benötigt` braucht unten eine Zeile Begründung: Ein Modul, das stillschweigend fehlt, ist von einem vergessenen nicht zu unterscheiden.

| Modul | Warum nicht benötigt |
|---|---|

## Methodenstand

Das Methoden-Repo und der Stand, mit dem dieser Fall begonnen wurde, stehen im Frontmatter. Jede Analyse trägt zusätzlich den Stand, mit dem sie tatsächlich erzeugt wurde.

## Offen

- [ ] Auftrag und Umfang festhalten.
- [ ] Je Modul entscheiden: aktiv oder nicht benötigt.
