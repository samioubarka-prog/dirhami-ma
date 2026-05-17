from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sys
import traceback

print("=== DIRHAMI STARTING ===", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)

try:
    from app.database import engine, Base
    print("Database imported OK", file=sys.stderr)

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Tables created OK", file=sys.stderr)

    from app.routers import auth, banks, blog, calculators, contacts
    print("Routers imported OK", file=sys.stderr)

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

    print("=== DIRHAMI READY ===", file=sys.stderr)

except Exception as e:
    print(f"FATAL ERROR: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    # Create minimal app to show error
    app = FastAPI(title="Dirhami API - ERROR", version="error")

    @app.get("/")
    async def error_root():
        return {"error": str(e), "trace": traceback.format_exc()}

    @app.get("/api/health")
    async def error_health():
        return {"status": "error", "message": str(e)}
