#!/usr/bin/env python3
"""Macht aus der leeren Vorlage einen Fall.

  python3 Werkzeuge/neuer-fall.py
  python3 Werkzeuge/neuer-fall.py --organisation "Name" --fallart beratung \
          --methoden-repo <Adresse oder Pfad> --methoden-stand <Version>

Setzt den Namen der Organisation in allen Notizen, trägt Beginn und Methodenstand
in 00 Steuerung/fall.md ein, stellt den Fall auf "aktiv" und schaltet damit die
Sperre scharf. Aktiviert den Git-Hook, wenn dieser Ordner ein eigenes Repo ist.
"""
import argparse, datetime, os, re, subprocess, sys
from vault import VAULT, FALL, alle_md, fallstatus

PLATZ = "‹Organisation›"
ARTEN = ("anstellung", "beratung", "übung")


def fragen(text, vorgabe=""):
    antwort = input(f"{text}{' [' + vorgabe + ']' if vorgabe else ''}: ").strip()
    return antwort or vorgabe


def setze(text, feld, wert):
    return re.sub(rf"^{feld}:.*$", lambda m: f'{feld}: {wert}', text, count=1, flags=re.M)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--organisation"); ap.add_argument("--fallart", choices=ARTEN)
    ap.add_argument("--methoden-repo"); ap.add_argument("--methoden-stand")
    a = ap.parse_args()

    if fallstatus() != "vorlage":
        sys.exit("Dieser Ordner ist bereits ein Fall. Für einen neuen Fall die Vorlage neu erzeugen.")

    oben = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                          text=True, cwd=VAULT).stdout.strip()
    eigenes_repo = oben and os.path.realpath(oben) == os.path.realpath(VAULT)

    org = a.organisation or fragen("Name der Organisation")
    if not org:
        sys.exit("Ohne Namen kein Fall.")
    art = a.fallart or fragen("Fallart (anstellung, beratung, übung)", "beratung")
    if art not in ARTEN:
        sys.exit(f"Fallart muss eine von {', '.join(ARTEN)} sein.")
    repo = a.methoden_repo if a.methoden_repo is not None else fragen("Methoden-Repo (Adresse oder Pfad, leer lassen wenn noch offen)")
    stand = a.methoden_stand if a.methoden_stand is not None else fragen("Stand des Methoden-Repos (Version oder Commit, leer wenn offen)")

    n = 0
    for p in alle_md():
        t = p.read_text(encoding="utf-8")
        if PLATZ in t:
            p.write_text(t.replace(PLATZ, org), encoding="utf-8"); n += 1

    t = FALL.read_text(encoding="utf-8")
    t = setze(t, "fallstatus", "aktiv")
    t = setze(t, "fallart", art)
    t = setze(t, "beginn", datetime.date.today().isoformat())
    t = setze(t, "methoden_repo", repo)
    t = setze(t, "methoden_stand", stand)
    FALL.write_text(t, encoding="utf-8")

    print(f"Fall angelegt: {org} ({art}). Name in {n} Notizen gesetzt.")
    if eigenes_repo:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=VAULT)
        subprocess.run(["chmod", "+x", str(VAULT / ".githooks/pre-commit")])
        print("Git-Hook aktiviert.")
    else:
        print("ACHTUNG: Dieser Ordner ist kein eigenes Git-Repo. Der Git-Hook wurde nicht aktiviert.\n"
              "Nach 'git init' nachholen:  git config core.hooksPath .githooks")
    print("Die Sperre ist jetzt aktiv. Nächster Schritt: 00 Steuerung/datenverarbeitung.md klären.\n"
          "Prüfen, dass das Repo auf GitHub privat ist.")


if __name__ == "__main__":
    main()
