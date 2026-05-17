from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import (
    auth, users, banks, investments, 
    loans, blog, calculators, contacts
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Dirhami API",
    description="Plateforme financière marocaine - Épargne, Investissement & Crédit",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(banks.router, prefix="/api/banks", tags=["Banques"])
app.include_router(investments.router, prefix="/api/investments", tags=["Investissements"])
app.include_router(loans.router, prefix="/api/loans", tags=["Crédits"])
app.include_router(blog.router, prefix="/api/blog", tags=["Blog"])
app.include_router(calculators.router, prefix="/api/calculators", tags=["Calculateurs"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["Contact"])

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "dirhami"}
