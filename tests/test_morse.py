"""Automatisierte Tests (Start: python -m pytest)."""
from Code.morse import morse_zu_text, text_zu_morse, uebersetzen


def test_text_zu_morse():
    assert text_zu_morse("SOS")["ergebnis"] == "... --- ..."


def test_morse_zu_text():
    assert morse_zu_text("... --- ... / .... .. .-.. ..-. .")["ergebnis"] == "SOS HILFE"


def test_hin_und_zurueck():
    satz = "HALLO WELT 2026"
    assert morse_zu_text(text_zu_morse(satz)["ergebnis"])["ergebnis"] == satz


def test_unbekannte_zeichen():
    assert text_zu_morse("A€")["unbekannte_zeichen"] == ["€"]


def test_automatische_erkennung():
    assert uebersetzen(".-")["richtung"] == "morse_zu_text"
    assert uebersetzen("A")["richtung"] == "text_zu_morse"
