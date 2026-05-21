from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database import engine, Base
from app.config import get_settings

# Import des routers
from app.routers import bank_cards, mortgage, opcvm, simulations, tax_regimes, auth

settings = get_settings()

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dirhami API",
    description="API de la plateforme financière Dirhami pour le Maroc",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS - Autoriser toutes les origines pour Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(auth.router)
app.include_router(bank_cards.router)
app.include_router(mortgage.router)
app.include_router(opcvm.router)
app.include_router(simulations.router)
app.include_router(tax_regimes.router)

# Servir le frontend statique (si présent)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Route racine API
@app.get("/api")
def root():
    return {
        "message": "Bienvenue sur l'API Dirhami",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "endpoints": {
            "auth": "/api/auth",
            "bank_cards": "/api/bank-cards",
            "mortgage": "/api/mortgage",
            "opcvm": "/api/opcvm",
            "simulations": "/api/simulations",
            "tax_regimes": "/api/tax-regimes"
        }
    }

# Health check
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
