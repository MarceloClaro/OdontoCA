from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, model_validator

VALID_FDI = {
    11,12,13,14,15,16,17,18,
    21,22,23,24,25,26,27,28,
    31,32,33,34,35,36,37,38,
    41,42,43,44,45,46,47,48,
}

class ReviewStatus(str, Enum):
    accepted = "accepted"
    review_required = "review_required"
    indeterminate = "indeterminate"
    rejected = "rejected"

class DetectionStatus(str, Enum):
    detected = "detected"
    not_detected = "not_detected"
    not_segmented = "not_segmented"
    not_evaluable = "not_evaluable"

class FDIStatus(str, Enum):
    probable = "probable"
    ambiguous = "ambiguous"
    undetermined = "undetermined"

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

    @model_validator(mode="after")
    def validate_geometry(self):
        if self.x2 <= self.x1 or self.y2 <= self.y1:
            raise ValueError("invalid bounding box geometry")
        return self

class ToothInstance(BaseModel):
    instance_id: str
    bbox: BoundingBox
    detection_score: float = Field(ge=0.0, le=1.0)
    arch: Optional[str] = None
    side: Optional[str] = None
    fdi_candidate: Optional[int] = None
    fdi_status: FDIStatus = FDIStatus.undetermined

    @model_validator(mode="after")
    def validate_fdi(self):
        if self.fdi_candidate is not None and self.fdi_candidate not in VALID_FDI:
            raise ValueError(f"invalid FDI: {self.fdi_candidate}")
        return self

class Finding(BaseModel):
    finding_id: str
    finding_type: str
    tooth_instance_id: Optional[str] = None
    raw_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    location: BoundingBox
    model_version: str
    review_status: ReviewStatus = ReviewStatus.review_required

class AnatomyFinding(BaseModel):
    structure: str
    status: DetectionStatus
    model_version: str
    score: Optional[float] = Field(default=None, ge=0.0, le=1.0)

class ExplainabilityRecord(BaseModel):
    method: str
    model_version: str
    target_layer: str
    target_class: str
    detection_id: str
    heatmap_path: str

class CaseResult(BaseModel):
    case_id: str
    image_hash: str
    model_version: str
    teeth: list[ToothInstance] = []
    findings: list[Finding] = []
    anatomy: list[AnatomyFinding] = []
    declared_findings_count: int = 0
    human_review_required: bool = True
