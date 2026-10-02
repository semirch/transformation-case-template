# Fall-Vorlage für KI-Transformationsvorhaben

Ein leeres Repo für einen Transformationsfall: eine Organisation, ihre KI-Vorhaben, die Belege dazu und die Analysen darüber. Je Arbeitgeber oder Kunde entsteht daraus ein eigenes, **privates** Repo, das mit Hilfe eines KI-Assistenten gefüllt wird.

## Wozu

Wer bei einer neuen Organisation anfängt, sammelt in den ersten Wochen viel und findet später wenig wieder: Was war belegt, was nur behauptet, was angenommen? Diese Vorlage gibt jeder Angabe einen Ort, eine Herkunft und eine Quelle, bevor sie in eine Rechnung oder eine Empfehlung eingeht.

## Wie es zusammenspielt

Diese Vorlage ist das leere Gefäß. Für jeden neuen Fall entsteht daraus eine eigene Kopie, die gefüllt wird. Die Vorlage selbst bleibt leer und sieht nie Falldaten.

| | Enthält | Lebt |
|---|---|---|
| **Diese Vorlage** | Die leere Struktur und die Regeln eines Falls | dauerhaft, ändert sich selten |
| **Fall-Repo** (Kopie je Fall) | Daten und Befunde einer Organisation | so lange der Fall läuft |

Die Methoden, mit denen ein Fall gefüllt wird, liegen getrennt in einem Methoden-Repo. Das schützt den Methodenkoffer: Besonderheiten eines Kunden oder einer Branche bleiben im Fall. Zurück in die Methoden geht nur, was eine Person verallgemeinert hat, über die Notiz `00 Steuerung/methodenrueckmeldung.md`.

## Aufbau

| Ordner | Art | Inhalt |
|---|---|---|
| `00 Steuerung` | Kern | Auftrag, Sperre, Entscheidungen, Annahmen, Risiken, Ereignisse |
| `01 Erhebung` | Kern | Was gesammelt werden soll, was gesammelt ist, woher es stammt |
| `02 Organisation` | Kern | Profil, Menschen, Systeme und Daten, Zahlen, Umfeld |
| `03 Vorhaben` | Kern | Portfolio und je Vorhaben ein Steckbrief |
| `04` bis `10` | Modul | Diagnose, Ziele und Programm, Menschen und Kommunikation, Governance und Recht, Plattform und Kosten, Daten, Synthese |
| `11 Gegenprüfung` | Kern | Zwölf Hypothesen über Zusammenhänge, die scheitern können |
| `Werkzeuge` | | Skripte für Start, Sperre, Landkarte und Restliste |

Der **Kern** ist in jedem Fall gleich und methodenunabhängig. Die **Module** sind leer, bis eine Methode sie füllt. Welche ein Fall braucht, wird in `00 Steuerung/fall.md` entschieden.

## Vier Grundsätze

1. **Erst klären, dann sammeln.** Solange nicht feststeht, was mit den Daten geschehen darf, lassen zwei Hooks keine Änderung außer an `00 Steuerung/datenverarbeitung.md` zu.
2. **Jede Aussage hat Herkunft und Quelle.** Fünf Kennzeichen (`öffentlich`, `intern belegt`, `angenommen`, `generiert`, `ungeprüft`) und eine Quellenkennung (`Q-001`, `G-001`).
3. **Jede Tatsache hat genau eine führende Notiz.** Alles andere verweist dorthin.
4. **Eine Lücke ist eine Zeile im Erhebungsplan,** keine Annahme.

Die vollständigen Regeln stehen in [AGENTS.md](AGENTS.md). Diese Datei ist zugleich der Vertrag, an den sich das Methoden-Repo hält.

## Loslegen

```sh
# 1. Auf GitHub: "Use this template", neues PRIVATES Repo, lokal klonen
# 2. Im Repo-Ordner:
python3 Werkzeuge/neuer-fall.py
```

Danach mit dem Assistenten die Datenverarbeitung klären. Die weiteren Schritte stehen in [Start.md](Start.md). Der Ordner lässt sich in Obsidian als Vault öffnen, zusätzliche Plugins sind nicht nötig. Die Skripte brauchen Python 3.9 oder neuer, ohne weitere Pakete.

## Was die Vorlage nicht leistet

- Sie enthält keine Methoden. Ohne Methoden-Repo bleiben die Module leer.
- Die Hooks schützen das Repo, nicht das Gespräch: Was in ein Chatfenster eingefügt wird, hält kein Hook auf.
- Der Werkzeug-Hook gilt für Claude Code. Für andere Assistenten bleiben die Regel in `AGENTS.md` und der Git-Hook.
- Sie ersetzt keine Rechtsberatung.
- Weitergegeben wird nie das Repo selbst, sondern eine geprüfte Kopie, siehe [Weitergabe.md](Weitergabe.md).
