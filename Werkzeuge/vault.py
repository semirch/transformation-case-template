"""Portable Dateisuche ausschließlich innerhalb dieses Repos, dazu der Fallstatus."""
import pathlib, re, sys

VAULT = pathlib.Path(__file__).resolve().parent.parent
STEUERUNG = VAULT / "00 Steuerung"
LANDKARTE = STEUERUNG / "Landkarte"
FALL = STEUERUNG / "fall.md"
SPERRE = STEUERUNG / "datenverarbeitung.md"

# Nie durchsuchen: abgelegte Altstände haben dieselben Namen wie die gültigen,
# Rohmaterial ist kein Arbeitsstand.
NIE = {"Archiv", ".obsidian", ".trash", ".git", ".claude", ".githooks", "Rohmaterial"}

HERKUNFT = ["öffentlich", "intern belegt", "angenommen", "generiert", "ungeprüft"]

# Sichtbarer Hinweis in jeder Notiz eines Falls, der nicht auf echten internen Daten beruht.
MARKE_DATENLAGE = "<!-- datenlage -->"
_HINWEIS = {
    "fiktiv": ("**Fiktiver Fall.** {org} ist eine erfundene Organisation. Alle Angaben in diesem "
               "Repo sind konstruiert und beschreiben kein reales Unternehmen und keine reale Person."),
    "gemischt": ("**Konstruierter Fall zu einem realen Unternehmen.** Dieses Repo enthält ausschließlich "
                 "öffentlich zugängliche Angaben über {org}, eigene Annahmen und erfundene Ergänzungen. "
                 "Es enthält keine internen Daten, nichts stammt aus dem Unternehmen, und es besteht "
                 "keine Verbindung zu {org}. Was nicht als `öffentlich` gekennzeichnet ist, ist nicht belegt."),
}


def _sichtbar(p):
    return not (NIE & set(p.relative_to(VAULT).parts))


def frontmatter(pfad):
    """Liest das Frontmatter als flaches Wörterbuch. Kommentare hinter # fallen weg.
    Eingerückte Zeilen unter 'module:' landen unter dem Schlüssel 'module'."""
    werte, module = {}, {}
    try:
        text = pfad.read_text(encoding="utf-8")
    except FileNotFoundError:
        return werte
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return werte
    for zeile in m.group(1).split("\n"):
        ohne = re.sub(r"\s+#.*$", "", zeile).rstrip()
        if ":" not in ohne:
            continue
        k, _, v = ohne.partition(":")
        v = v.strip().strip('"')
        if zeile.startswith((" ", "\t")):
            module[k.strip()] = v
        else:
            werte[k.strip()] = v
    werte["module"] = module
    return werte


def fallstatus():
    return frontmatter(FALL).get("fallstatus", "vorlage")


def sperre_offen():
    """Wahr, wenn ein aktiver Fall seine Datenverarbeitung noch nicht geklärt hat."""
    return fallstatus() == "aktiv" and frontmatter(SPERRE).get("status") != "geklärt"


def datenlage():
    return frontmatter(FALL).get("datenlage", "echt") or "echt"


def hinweis():
    """Die Hinweiszeile für diesen Fall, oder '' bei echter Datenlage und in der leeren Vorlage."""
    art = datenlage()
    if fallstatus() == "vorlage" or art not in _HINWEIS:
        return ""
    org = frontmatter(FALL).get("organisation", "Die Organisation")
    return f"> {MARKE_DATENLAGE} " + _HINWEIS[art].format(org=org)


def modul_status(name):
    return frontmatter(FALL).get("module", {}).get(name, "offen")


def alle_md():
    """Alle Markdown-Dateien im Repo außer Archiv, Rohmaterial und Verwaltung."""
    return sorted(p for p in VAULT.rglob("*.md") if _sichtbar(p))


def fall_md():
    """Die Notizen, deren offene Punkte zählen: ohne Werkzeuge, ohne erzeugte
    Landkarte, ohne Muster, ohne Module, die der Fall nicht braucht."""
    aus = []
    for p in alle_md():
        teile = p.relative_to(VAULT).parts
        if len(teile) == 1 or teile[0] == "Werkzeuge" or LANDKARTE in p.parents:
            continue
        if p.name.startswith("_muster"):
            continue
        if modul_status(teile[0]) == "nicht benötigt":
            continue
        aus.append(p)
    return aus
