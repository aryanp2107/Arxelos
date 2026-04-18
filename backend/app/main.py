"""
Arxelos — Synchronous Multi-Model Intelligence Platform
Main FastAPI application entrypoint.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.routers import health, tumor

logger = logging.getLogger("arxelos")

# Resolve paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML models on startup, clean up on shutdown."""
    # --- Startup ---
    from backend.app.services.tumor_service import classifier

    model_path = PROJECT_ROOT / settings.TUMOR_MODEL_PATH
    if model_path.exists():
        try:
            classifier.load(str(model_path))
            logger.info(f"Tumor classifier loaded from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load tumor classifier: {e}")
    else:
        logger.warning(
            f"Tumor model not found at {model_path}. "
            f"Place your .keras file there or update TUMOR_MODEL_PATH in .env"
        )

    yield

    # --- Shutdown ---
    logger.info("Arxelos shutting down.")


app = FastAPI(
    title="Arxelos API",
    description="AI at the Intersection of Intelligence & Biology",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static files ---
if (FRONTEND_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

# --- API Routers ---
app.include_router(health.router, tags=["Health"])
app.include_router(tumor.router, prefix="/api/v1/tumor", tags=["Brain Tumor Classifier"])

# Model routers — uncomment as each model is deployed:
# from backend.app.routers import lesions
# app.include_router(lesions.router, prefix="/api/v1/lesions", tags=["Virtual Lesions"])

# from backend.app.routers import rag
# app.include_router(rag.router, prefix="/api/v1/rag", tags=["Medical RAG Q&A"])


# --- API info endpoint ---
@app.get("/api")
async def api_info():
    """API metadata and model status."""
    from backend.app.services.tumor_service import classifier

    return {
        "platform": "Arxelos",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/docs",
        "models": {
            "tumor_classifier": "loaded" if classifier.is_loaded else "not_loaded",
            "virtual_lesions": "planned",
            "medical_rag": "planned",
        },
    }


# --- Landing page ---
@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """Serve the Arxelos landing page."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(
        content="<h1>Arxelos</h1><p>Frontend not found. Visit <a href='/docs'>/docs</a> for the API.</p>"
    )


@app.get("/tumor", response_class=HTMLResponse)
async def tumor_demo():
    """Serve the Brain Tumor Classifier demo page."""
    tumor_path = FRONTEND_DIR / "tumor.html"
    if tumor_path.exists():
        return HTMLResponse(content=tumor_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Demo not found</h1>")
