from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, cartes, opcvm, simulations, blog, calculators

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dirhami API",
    description="API backend pour la plateforme financière Dirhami - Maroc",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(cartes.router, prefix="/api/v1/cartes", tags=["cartes"])
app.include_router(opcvm.router, prefix="/api/v1/opcvm", tags=["opcvm"])
app.include_router(simulations.router, prefix="/api/v1/simulations", tags=["simulations"])
app.include_router(blog.router, prefix="/api/v1/blog", tags=["blog"])
app.include_router(calculators.router, prefix="/api/v1/calculators", tags=["calculators"])

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Dirhami", "version": "2.0.0", "status": "online"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
