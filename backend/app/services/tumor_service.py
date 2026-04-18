"""
Model 1 — Brain Tumor MRI Classifier
Inference service: loads the Keras model, preprocesses images, returns predictions.

Model details (from training notebook):
  - Architecture: Custom 30-layer Sequential CNN (5 conv blocks)
  - Input: 224x224x3, rescaled to [0, 1]
  - Classes: ['glioma', 'meningioma', 'notumor', 'pituitary']
  - Format: .keras
  - Test accuracy: 96.2%
"""

import io
import numpy as np
from pathlib import Path
from PIL import Image

# Class labels — alphabetical order, matching flow_from_directory output
CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]

# Human-readable display labels
CLASS_DISPLAY = {
    "glioma": "Glioma Tumor",
    "meningioma": "Meningioma Tumor",
    "notumor": "No Tumor",
    "pituitary": "Pituitary Tumor",
}

# Clinical context for each class (for the UI)
CLASS_INFO = {
    "glioma": "Gliomas originate from glial cells in the brain or spine. They are the most common type of primary brain tumor.",
    "meningioma": "Meningiomas arise from the meninges, the membranes surrounding the brain and spinal cord. Most are benign.",
    "notumor": "No tumor was detected in this MRI scan.",
    "pituitary": "Pituitary tumors develop in the pituitary gland at the base of the brain. Most are benign adenomas.",
}

IMG_SIZE = 224


class TumorClassifier:
    """Wraps the trained Keras model for inference."""

    def __init__(self, model_path: str = None):
        self.model = None
        self.model_path = model_path
        self._loaded = False

    def load(self, model_path: str = None):
        """Load the Keras model from disk."""
        import tensorflow as tf

        path = model_path or self.model_path
        if path is None:
            raise ValueError("No model path provided.")

        resolved = Path(path)
        if not resolved.exists():
            raise FileNotFoundError(f"Model not found at {resolved}")

        self.model = tf.keras.models.load_model(str(resolved))
        self.model_path = str(resolved)
        self._loaded = True
        print(f"[TumorClassifier] Model loaded from {resolved}")

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess raw image bytes into model-ready tensor.

        Steps (matching training notebook):
          1. Open image, convert to RGB
          2. Resize to 224x224
          3. Convert to float32 array
          4. Rescale to [0, 1] by dividing by 255.0
          5. Add batch dimension
        """
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)
        arr = np.array(img, dtype=np.float32) / 255.0
        return np.expand_dims(arr, axis=0)  # (1, 224, 224, 3)

    def predict(self, image_bytes: bytes) -> dict:
        """
        Run inference on raw image bytes.

        Returns:
            {
                "predicted_class": str,
                "display_label": str,
                "confidence": float,
                "description": str,
                "probabilities": {class_name: float, ...}
            }
        """
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call .load() first.")

        # Preprocess
        img_tensor = self.preprocess(image_bytes)

        # Inference
        predictions = self.model.predict(img_tensor, verbose=0)[0]

        # Parse results
        pred_idx = int(np.argmax(predictions))
        pred_class = CLASS_NAMES[pred_idx]

        return {
            "predicted_class": pred_class,
            "display_label": CLASS_DISPLAY[pred_class],
            "confidence": float(predictions[pred_idx]),
            "description": CLASS_INFO[pred_class],
            "probabilities": {
                name: float(prob) for name, prob in zip(CLASS_NAMES, predictions)
            },
        }


# Singleton instance — loaded once at startup
classifier = TumorClassifier()
