#!/usr/bin/env python3
"""Die Sperre: Solange ein aktiver Fall seine Datenverarbeitung nicht geklärt hat,
darf nur 00 Steuerung/datenverarbeitung.md geändert werden.

  python3 Werkzeuge/sperre.py            zeigt den Zustand
  python3 Werkzeuge/sperre.py --hook     für den Assistenten: liest den geplanten
                                         Schreibzugriff als JSON von der Standardeingabe
  python3 Werkzeuge/sperre.py --commit   für Git: prüft die vorgemerkten Dateien

Im Zustand "vorlage" ist die Sperre ohne Wirkung, damit sich die Vorlage selbst
bearbeiten lässt. Ein Schreibzugriff über die Shell umgeht den Hook des Assistenten.
Dafür gibt es die Regel in AGENTS.md und den Git-Hook.
"""
import json, pathlib, subprocess, sys
from vault import VAULT, SPERRE, fallstatus, sperre_offen

HINWEIS = ("Gesperrt: Die Datenverarbeitung dieses Falls ist noch nicht geklärt. "
           "Zuerst die Fragen in '00 Steuerung/datenverarbeitung.md' mit der verantwortlichen "
           "Person klären und dort eintragen. Erst ihre ausdrückliche Bestätigung setzt "
           "'status: geklärt'. Bis dahin keine andere Datei ändern.")


def erlaubt(pfad):
    """Die Sperrnotiz selbst darf immer geändert werden, ebenso alles außerhalb des Repos."""
    p = pathlib.Path(pfad)
    if not p.is_absolute():
        p = VAULT / p
    p = p.resolve()
    return p == SPERRE.resolve() or VAULT.resolve() not in p.parents


def main():
    modus = sys.argv[1] if len(sys.argv) > 1 else ""
    if not sperre_offen():
        if not modus:
            print(f"Fallstatus: {fallstatus()}. Die Sperre ist nicht aktiv.")
        return 0
    if modus == "--hook":
        try:
            eingabe = json.load(sys.stdin)
        except ValueError:
            eingabe = {}
        ziel = (eingabe.get("tool_input") or {}).get("file_path") or \
               (eingabe.get("tool_input") or {}).get("notebook_path")
        if ziel and erlaubt(ziel):
            return 0
        print(HINWEIS, file=sys.stderr)
        return 2
    if modus == "--commit":
        aus = subprocess.run(["git", "diff", "--cached", "--name-only", "-z"],
                             capture_output=True, text=True, cwd=VAULT).stdout
        fremd = [f for f in aus.split("\0") if f and not erlaubt(f)]
        if not fremd:
            return 0
        print(HINWEIS, file=sys.stderr)
        print("Vorgemerkt sind: " + ", ".join(fremd[:8]), file=sys.stderr)
        return 1
    print("Fallstatus: aktiv. Die Sperre ist AKTIV: Datenverarbeitung noch offen.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
