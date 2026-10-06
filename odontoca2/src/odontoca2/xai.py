import numpy as np
from odontoca2.schemas import ExplainabilityRecord

ALLOWED_METHODS = {"GradCAM", "HiResCAM", "EigenCAM"}

def validate_cam_provenance(record: ExplainabilityRecord) -> None:
    if record.method not in ALLOWED_METHODS:
        raise ValueError("Unsupported explainability method")
    for name in ("model_version", "target_layer", "target_class", "detection_id", "heatmap_path"):
        if not getattr(record, name):
            raise ValueError(f"Missing CAM provenance field: {name}")

def validate_cam_array(cam: np.ndarray) -> None:
    if cam.ndim != 2 or cam.size == 0:
        raise ValueError("CAM must be a non-empty 2D array")
    if float(cam.min()) < 0.0 or float(cam.max()) > 1.0:
        raise ValueError("CAM must be normalized to [0, 1]")
