from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import os
import json
from datetime import datetime

app = FastAPI(title="Dirhami", description="Plateforme financiere Maroc")

# Determine le repertoire de base
BASE_DIR = Path(__file__).parent

# Creer les dossiers s'ils n'existent pas
(BASE_DIR / "images").mkdir(exist_ok=True)
(BASE_DIR / "data").mkdir(exist_ok=True)

# Fichier pour stocker les messages
MESSAGES_FILE = BASE_DIR / "data" / "messages.json"

# Mount static files
app.mount("/css", StaticFiles(directory=str(BASE_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(BASE_DIR / "js")), name="js")
app.mount("/images", StaticFiles(directory=str(BASE_DIR / "images")), name="images")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR))

# === ROUTES PRINCIPALES ===

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cartes-bancaires", response_class=HTMLResponse)
async def cartes(request: Request):
    return templates.TemplateResponse("cartes-bancaires.html", {"request": request})

@app.get("/credit-immobilier", response_class=HTMLResponse)
async def credit(request: Request):
    return templates.TemplateResponse("credit-immobilier.html", {"request": request})

@app.get("/opcvm", response_class=HTMLResponse)
async def opcvm(request: Request):
    return templates.TemplateResponse("opcvm.html", {"request": request})

@app.get("/retraite", response_class=HTMLResponse)
async def retraite(request: Request):
    return templates.TemplateResponse("retraite.html", {"request": request})

@app.get("/budget", response_class=HTMLResponse)
async def budget(request: Request):
    return templates.TemplateResponse("budget.html", {"request": request})

@app.get("/regimes-epargne", response_class=HTMLResponse)
async def regimes(request: Request):
    return templates.TemplateResponse("regimes-epargne.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

# === API CONTACT ===

@app.post("/api/contact")
async def submit_contact(
    nom: str = Form(...),
    email: str = Form(...),
    sujet: str = Form(...),
    message: str = Form(...)
):
    """Recevoir un message de contact et le stocker"""

    # Charger les messages existants
    messages = []
    if MESSAGES_FILE.exists():
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            try:
                messages = json.load(f)
            except:
                messages = []

    # Ajouter le nouveau message
    new_message = {
        "id": len(messages) + 1,
        "nom": nom,
        "email": email,
        "sujet": sujet,
        "message": message,
        "date": datetime.now().isoformat(),
        "lu": False
    }
    messages.append(new_message)

    # Sauvegarder
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    return JSONResponse({
        "success": True,
        "message": "Message envoyé avec succes ! Nous vous repondrons sous 48h.",
        "id": new_message["id"]
    })

@app.get("/api/messages")
async def get_messages():
    """Recuperer tous les messages (pour toi, admin)"""
    if not MESSAGES_FILE.exists():
        return JSONResponse({"messages": []})

    with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
        try:
            messages = json.load(f)
        except:
            messages = []

    return JSONResponse({"messages": messages})

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}
