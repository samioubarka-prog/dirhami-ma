from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import os
import json
from datetime import datetime

app = FastAPI(title="Dirhami", description="Plateforme financiere Maroc")

BASE_DIR = Path(__file__).parent

(BASE_DIR / "images").mkdir(exist_ok=True)
(BASE_DIR / "data").mkdir(exist_ok=True)

MESSAGES_FILE = BASE_DIR / "data" / "messages.json"

app.mount("/css", StaticFiles(directory=str(BASE_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(BASE_DIR / "js")), name="js")
app.mount("/images", StaticFiles(directory=str(BASE_DIR / "images")), name="images")

templates = Jinja2Templates(directory=str(BASE_DIR))

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

@app.post("/api/contact")
async def submit_contact(
    nom: str = Form(...),
    email: str = Form(...),
    sujet: str = Form(...),
    message: str = Form(...)
):
    messages = []
    if MESSAGES_FILE.exists():
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            try:
                messages = json.load(f)
            except:
                messages = []

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

    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    return JSONResponse({
        "success": True,
        "message": "Message envoyé avec succes ! Nous vous repondrons sous 48h.",
        "id": new_message["id"]
    })

@app.get("/api/messages")
async def get_messages():
    if not MESSAGES_FILE.exists():
        return JSONResponse({"messages": []})

    with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
        try:
            messages = json.load(f)
        except:
            messages = []

    return JSONResponse({"messages": messages})

@app.get("/health")
async def health():
    return {"status": "ok"}
