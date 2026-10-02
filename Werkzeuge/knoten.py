"""Die Knoten der Landkarte für diesen Fall: Rollen, Gremien, Systeme.

landkarte-erzeugen.py legt je Knoten eine Notiz an und sucht mit dem Muster,
in welchen Dateien er vorkommt. Hier eintragen, sobald menschen.md und
systeme-daten.md stehen.

Je Knoten vier Angaben:
  1. Name der Notiz, zugleich Dateiname. Eine Rolle, nie ein Personenname.
  2. Suchmuster (regulärer Ausdruck). r"Leitung IT\b" findet "Leitung IT",
     aber nicht "Leitung ITSM". Mehrere Schreibweisen mit | trennen.
  3. Woher der Steckbrief kommt:
       "rolle"   Tabelle | Rolle | in 02 Organisation/menschen.md
       "gremium" Tabelle | Name | Mitglieder in menschen.md
       "system"  Tabelle | Name | Zweck in systeme-daten.md
       None      kein Eintrag im Profil, die Rolle entsteht erst in den Ausarbeitungen
  4. Womit die Zeile in dieser Tabelle beginnt (erste Zelle). Bei None ebenfalls None.

Neutrales Konfigurationsbeispiel:
  ("Leitung IT", r"Leitung IT\b", "rolle", "Leitung IT"),
  ("Champions", r"Champion", None, None),
"""

KNOTEN = {
    "Rollen": [
    ],
    "Gremien": [
    ],
    "Systeme": [
    ],
}
