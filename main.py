from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import os

app = FastAPI(title="Dirhami", description="Plateforme financiere Maroc")

# Determine le repertoire de base
BASE_DIR = Path(__file__).parent

# Mount static files
app.mount("/css", StaticFiles(directory=str(BASE_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(BASE_DIR / "js")), name="js")
app.mount("/images", StaticFiles(directory=str(BASE_DIR / "images")), name="images")

# Templates
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

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
