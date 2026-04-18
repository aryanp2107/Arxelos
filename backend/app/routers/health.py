"""
Health check endpoints — confirms the API is alive and reports model status.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic liveness probe."""
    return {"status": "healthy", "platform": "Arxelos"}


@router.get("/health/models")
async def model_status():
    """Reports readiness of each deployed model."""
    return {
        "tumor_classifier": {
            "status": "not_loaded",
            "version": None,
        },
        "virtual_lesions": {
            "status": "not_loaded",
            "version": None,
        },
        "medical_rag": {
            "status": "not_loaded",
            "version": None,
        },
    }
