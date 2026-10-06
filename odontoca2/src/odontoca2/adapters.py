from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from odontoca2.schemas import BoundingBox


@dataclass(frozen=True)
class ModelDetection:
    class_id: int
    class_name: str
    score: float
    bbox: BoundingBox


class UltralyticsDetectorAdapter:
    """
    Adaptador fino para resultados Ultralytics/YOLO.

    Não interpreta score como probabilidade clínica e não atribui FDI.
    A função desta camada é apenas normalizar as detecções brutas.
    """

    def __init__(self, model: Any, *, class_map: Mapping[int, str] | None = None):
        self.model = model
        self.class_map = dict(class_map or {})

    def predict(self, image: Any, **kwargs: Any) -> list[ModelDetection]:
        results = self.model.predict(source=image, verbose=False, **kwargs)
        if not results:
            return []

        result = results[0]
        boxes = getattr(result, "boxes", None)
        if boxes is None:
            return []

        names = self.class_map or getattr(result, "names", None) or getattr(self.model, "names", {})
        detections: list[ModelDetection] = []

        xyxy = getattr(boxes, "xyxy", [])
        conf = getattr(boxes, "conf", [])
        cls = getattr(boxes, "cls", [])

        for coords, score, class_id in zip(xyxy, conf, cls):
            vals = coords.tolist() if hasattr(coords, "tolist") else list(coords)
            cid = int(class_id.item() if hasattr(class_id, "item") else class_id)
            s = float(score.item() if hasattr(score, "item") else score)
            name = names[cid] if isinstance(names, (dict, list, tuple)) else str(cid)

            detections.append(
                ModelDetection(
                    class_id=cid,
                    class_name=str(name),
                    score=s,
                    bbox=BoundingBox(
                        x1=float(vals[0]),
                        y1=float(vals[1]),
                        x2=float(vals[2]),
                        y2=float(vals[3]),
                    ),
                )
            )

        return detections
