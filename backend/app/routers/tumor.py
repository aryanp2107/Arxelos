"""
Model 1 — Brain Tumor MRI Classifier
API routes for image upload and prediction.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.app.services.tumor_service import classifier, CLASS_NAMES

router = APIRouter()

# Max file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


class PredictionResponse(BaseModel):
    predicted_class: str
    display_label: str
    confidence: float
    description: str
    probabilities: dict[str, float]
    disclaimer: str = (
        "This is an AI research demo for educational purposes only. "
        "It is NOT a medical diagnosis. Always consult a qualified healthcare professional."
    )


class ModelInfoResponse(BaseModel):
    model_name: str = "Brain Tumor MRI Classifier"
    architecture: str = "Custom 30-layer Sequential CNN"
    input_size: str = "224x224x3"
    classes: list[str] = CLASS_NAMES
    test_accuracy: str = "96.2%"
    dataset: str = "7,023 brain MRI scans (Kaggle)"
    status: str = "not_loaded"


@router.get("/info", response_model=ModelInfoResponse)
async def model_info():
    """Return model metadata and current status."""
    return ModelInfoResponse(
        status="loaded" if classifier.is_loaded else "not_loaded"
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_tumor(file: UploadFile = File(...)):
    """
    Upload a brain MRI scan and receive a classification prediction.

    Accepts JPEG, PNG, or WebP images up to 10MB.
    Returns predicted class, confidence, all class probabilities,
    and a clinical description.
    """
    # Validate model is loaded
    if not classifier.is_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded. The server is starting up or the model file is missing.",
        )

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Accepted: JPEG, PNG, WebP.",
        )

    # Read and validate file size
    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({len(image_bytes) / 1024 / 1024:.1f}MB). Max: 10MB.",
        )

    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    # Run inference
    try:
        result = classifier.predict(image_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )

    return PredictionResponse(**result)
