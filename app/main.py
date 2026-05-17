from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, banks, blog, calculators, contacts

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dirhami API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(banks.router, prefix="/api/banks", tags=["Banques"])
app.include_router(blog.router, prefix="/api/blog", tags=["Blog"])
app.include_router(calculators.router, prefix="/api/calculators", tags=["Calculateurs"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["Contact"])

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "dirhami"}
