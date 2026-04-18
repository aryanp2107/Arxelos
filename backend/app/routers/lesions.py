"""
Model 2 — Virtual Lesions CNN Visualizer
Routes for image upload, layer selection, ablation, and Grad-CAM visualization.
Activate in main.py when the model is ready (target: Week 3-4).
"""

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

router = APIRouter()


class LesionRequest(BaseModel):
    layer_name: str = "layer4"  # Target layer to ablate
    channel_indices: list[int] = []  # Specific channels (empty = full layer)
    visualization: str = "gradcam"  # gradcam | saliency | both


@router.post("/ablate")
async def ablate_and_visualize(
    file: UploadFile = File(...),
    # params: LesionRequest  # Uncomment when implementing
):
    """
    Upload an image, select a layer to ablate, and visualize the
    prediction change with Grad-CAM or saliency maps.
    """
    return {
        "status": "stub",
        "message": "Model 2 endpoint scaffolded — ablation pipeline not yet connected.",
        "filename": file.filename,
    }
