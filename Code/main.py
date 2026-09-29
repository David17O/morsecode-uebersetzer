"""FastAPI-App: stellt den Morsecode-Übersetzer als REST-API bereit.

Start lokal:  uvicorn Code.main:app --reload
Doku:         http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from Code.morse import morse_zu_text, text_zu_morse, uebersetzen

app = FastAPI(
    title="Morsecode-Übersetzer",
    description="Übersetzt Text → Morsecode und Morsecode → Text. "
                "Morsecode: Buchstaben mit Leerzeichen, Wörter mit ' / ' trennen.",
    version="1.0.0",
)


class TextEingabe(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, examples=["SOS Hilfe"])


class MorseEingabe(BaseModel):
    morse: str = Field(..., min_length=1, max_length=5000,
                       examples=["... --- ... / .... .. .-.. ..-. ."])


class FreieEingabe(BaseModel):
    eingabe: str = Field(..., min_length=1, max_length=5000, examples=["Hallo Welt"])


@app.get("/")
def status():
    """Einfacher Health-Check."""
    return {"status": "ok", "app": "Morsecode-Übersetzer", "doku": "/docs"}


@app.post("/text-zu-morse")
def api_text_zu_morse(daten: TextEingabe):
    resultat = text_zu_morse(daten.text)
    if not resultat["ergebnis"]:
        raise HTTPException(status_code=422, detail="Keine übersetzbaren Zeichen gefunden.")
    return {"eingabe": daten.text, **resultat}


@app.post("/morse-zu-text")
def api_morse_zu_text(daten: MorseEingabe):
    return {"eingabe": daten.morse, **morse_zu_text(daten.morse)}


@app.post("/uebersetzen")
def api_uebersetzen(daten: FreieEingabe):
    """Erkennt automatisch, ob Text oder Morsecode eingegeben wurde."""
    return {"eingabe": daten.eingabe, **uebersetzen(daten.eingabe)}
