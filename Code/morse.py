"""Business-Logik: Übersetzung Text <-> Morsecode (internationales Morsealphabet, ITU)."""

# Zeichen -> Morsecode
MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    "Ä": ".-.-", "Ö": "---.", "Ü": "..--",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--", "'": ".----.",
    "/": "-..-.", "(": "-.--.", ")": "-.--.-", "&": ".-...", ":": "---...",
    ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-", "_": "..--.-",
    '"': ".-..-.", "$": "...-..-", "@": ".--.-.",
}

# Morsecode -> Zeichen (Umkehrung)
REVERSE_CODE = {code: char for char, code in MORSE_CODE.items()}

BUCHSTABEN_TRENNER = " "   # zwischen Buchstaben
WORT_TRENNER = " / "       # zwischen Wörtern


def text_zu_morse(text: str) -> dict:
    """Übersetzt Text in Morsecode. Unbekannte Zeichen werden ausgelassen und gemeldet."""
    text = text.strip().upper().replace("ß", "SS")
    unbekannt = []
    woerter = []
    for wort in text.split():
        codes = []
        for zeichen in wort:
            if zeichen in MORSE_CODE:
                codes.append(MORSE_CODE[zeichen])
            elif zeichen not in unbekannt:
                unbekannt.append(zeichen)
        if codes:
            woerter.append(BUCHSTABEN_TRENNER.join(codes))
    return {"ergebnis": WORT_TRENNER.join(woerter), "unbekannte_zeichen": unbekannt}


def morse_zu_text(morse: str) -> dict:
    """Übersetzt Morsecode in Text. Buchstaben durch Leerzeichen, Wörter durch ' / ' getrennt."""
    # Auch Unicode-Varianten (•, –, —) und '_' als Strich akzeptieren
    morse = (morse.strip().replace("•", ".").replace("·", ".")
             .replace("–", "-").replace("—", "-").replace("_", "-"))
    unbekannt = []
    woerter = []
    for wort in morse.split("/"):
        buchstaben = []
        for code in wort.split():
            if code in REVERSE_CODE:
                buchstaben.append(REVERSE_CODE[code])
            else:
                buchstaben.append("?")
                if code not in unbekannt:
                    unbekannt.append(code)
        if buchstaben:
            woerter.append("".join(buchstaben))
    return {"ergebnis": " ".join(woerter), "unbekannte_zeichen": unbekannt}


def ist_morsecode(eingabe: str) -> bool:
    """Erkennt, ob die Eingabe Morsecode ist (nur Punkte, Striche, Leerzeichen, '/')."""
    erlaubt = set(".-/ •·–—_")
    eingabe = eingabe.strip()
    return bool(eingabe) and all(z in erlaubt for z in eingabe) and any(z in ".-•·–—" for z in eingabe)


def uebersetzen(eingabe: str) -> dict:
    """Erkennt automatisch die Richtung und übersetzt."""
    if ist_morsecode(eingabe):
        return {"richtung": "morse_zu_text", **morse_zu_text(eingabe)}
    return {"richtung": "text_zu_morse", **text_zu_morse(eingabe)}


if __name__ == "__main__":
    # Schneller lokaler Test ohne API
    print(uebersetzen("SOS Hilfe"))
    print(uebersetzen("... --- ... / .... .. .-.. ..-. ."))
