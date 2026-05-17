from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dirhami", version="1.0")

@app.on_event("startup")
async def startup():
    import sys
    print(f"STARTUP: Python {sys.version}", flush=True)

    try:
        from app.database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("STARTUP: DB OK", flush=True)
    except Exception as e:
        print(f"STARTUP DB ERROR: {e}", flush=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers inside try to catch errors
try:
    from app.routers import auth, banks, blog, calculators, contacts
    app.include_router(auth.router, prefix="/api/auth")
    app.include_router(banks.router, prefix="/api/banks")
    app.include_router(blog.router, prefix="/api/blog")
    app.include_router(calculators.router, prefix="/api/calculators")
    app.include_router(contacts.router, prefix="/api/contacts")
    print("ROUTERS: OK", flush=True)
except Exception as e:
    print(f"ROUTERS ERROR: {e}", flush=True)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/health")
async def health():
    return {"status": "ok"}
