# Morsecode-Übersetzer (AI Operations – Aufgabe DevOps)

Eine einfache REST-API (FastAPI) zur Übersetzung von **Text → Morsecode** und **Morsecode → Text**.

- **Input:** Text (Wort oder Satz) oder Morsecode
- **Output:** Übersetzung (Punkte/Striche bzw. Klartext) sowie eine Liste nicht übersetzbarer Zeichen
- **Format Morsecode:** Buchstaben mit Leerzeichen, Wörter mit ` / ` trennen, z. B. `... --- ... / .... .. .-.. ..-. .`

## Projektstruktur

```
morsecode-uebersetzer/
├── Code/
│   ├── __init__.py
│   ├── morse.py            # Business-Logik (Übersetzung)
│   ├── main.py             # FastAPI-App (API-Endpunkte)
│   └── test_morse.ipynb    # Notebook zum Testen von Logik und API
├── tests/
│   └── test_morse.py       # automatisierte Tests (pytest)
├── requirements.txt
├── .gitignore
└── README.md
```

## API-Endpunkte

| Methode | Pfad             | Request-Body                       | Beschreibung                          |
|---------|------------------|------------------------------------|---------------------------------------|
| GET     | `/`              | –                                  | Health-Check                          |
| POST    | `/text-zu-morse` | `{"text": "SOS Hilfe"}`            | Text → Morsecode                      |
| POST    | `/morse-zu-text` | `{"morse": "... --- ..."}`         | Morsecode → Text                      |
| POST    | `/uebersetzen`   | `{"eingabe": "..."}`               | Erkennt die Richtung automatisch      |

Beispiel-Response `/text-zu-morse`:
```json
{"eingabe": "SOS Hilfe", "ergebnis": "... --- ... / .... .. .-.. ..-. .", "unbekannte_zeichen": []}
```

---

## Teil 1: DevOps lokal (Windows, VS Code)

1. **Ordner öffnen:** VS Code → *File → Open Folder* → `morsecode-uebersetzer`
2. **Virtuelle Umgebung erstellen:** Terminal öffnen (*Terminal → New Terminal*)
   ```powershell
   python -m venv .venv
   ```
   (alternativ: `Ctrl+Shift+P` → *Python: Create Environment* → *Venv*)
3. **Umgebung aktivieren:**
   ```powershell
   .\.venv\Scripts\activate
   ```
   Falls PowerShell das Skript blockiert, einmalig:
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
   Danach steht `(.venv)` vor der Eingabezeile.
4. **Libraries installieren:**
   ```powershell
   pip install -r requirements.txt
   ```
5. **Logik testen (ohne API):**
   ```powershell
   python Code/morse.py
   ```
   Oder `Code/test_morse.ipynb` öffnen, oben rechts den Kernel `.venv` wählen
   (VS Code bietet ggf. an, `ipykernel` zu installieren → bestätigen) und die erste Zelle ausführen.
6. **API starten** (im Projektordner, nicht im Ordner `Code`):
   ```powershell
   uvicorn Code.main:app --reload
   ```
7. **API aufrufen:** Browser → <http://127.0.0.1:8000/docs>
   → Endpunkt aufklappen → *Try it out* → Eingabe → *Execute* → Response prüfen.
   Die Aufrufe erscheinen im Terminal (Uvicorn-Log). Alternativ die zweite Zelle im Notebook ausführen.
8. **Automatisierte Tests (optional):**
   ```powershell
   pip install pytest
   python -m pytest
   ```
9. Beenden mit `Ctrl+C`. 📹 Für die Abgabe Bildschirmvideo von Schritt 6–7 aufnehmen.

---

## Teil 2: DevOps Cloud (Git, GitHub, render.com)

Voraussetzungen: Git installiert, GitHub-Account, render.com-Account (mit GitHub einloggen).

1. **Repository auf GitHub erstellen:** <https://github.com/new>, Name `morsecode-uebersetzer`, **leer** (ohne README).
2. **Git lokal initialisieren** (Terminal im Projektordner):
   ```powershell
   git config --global user.name "Dein Name"        # nur beim ersten Mal
   git config --global user.email "deine@mail.ch"   # nur beim ersten Mal
   git init
   git add .
   git commit -m "Initial commit: Morsecode-Übersetzer"
   git branch -M main
   ```
   (`.gitignore` ist schon vorhanden, `.venv/` wird nicht hochgeladen.)
3. **Mit GitHub verbinden und pushen:**
   ```powershell
   git remote add origin https://github.com/<dein-user>/morsecode-uebersetzer.git
   git push -u origin main
   ```
4. **Deployment auf render.com:** <https://dashboard.render.com> → *New → Web Service* →
   *Configure in GitHub* → Zugriff auf das Repository erlauben → Repository wählen.
5. **Konfiguration:**
   - Language: Python 3
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn Code.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: Free
6. **Build überprüfen:** Im Tab *Logs* warten, bis „Your service is live“ erscheint.
7. **API abrufen:** `https://<dein-service>.onrender.com/docs`
   (oder im Notebook `BASIS_URL` anpassen). Die Aufrufe sind in den render-Logs sichtbar.
   Hinweis: Der Free-Plan schläft nach Inaktivität ein, der erste Aufruf dauert dann ca. 1 Minute.
8. **Code anpassen und neu deployen:** z. B. `version` in `Code/main.py` auf `1.1.0` erhöhen
   oder ein neues Zeichen ergänzen, dann:
   ```powershell
   git add .
   git commit -m "Version 1.1.0: ..."
   git push
   ```
   render deployt automatisch neu (Auto-Deploy). Falls nicht: *Manual Deploy → Deploy latest commit*.
   📹 Bildschirmvideo: Änderung → Push → neuer Build → geänderte Response.
