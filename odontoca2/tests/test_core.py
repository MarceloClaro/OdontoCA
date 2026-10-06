import numpy as np
import pytest
from pydantic import ValidationError

from odontoca2.schemas import (
    BoundingBox, ToothInstance, Finding, CaseResult,
    DetectionStatus, ExplainabilityRecord
)
from odontoca2.anatomy import anatomy_status
from odontoca2.consistency import validate_report_consistency, evaluate_tooth_conflict
from odontoca2.xai import validate_cam_provenance, validate_cam_array
from odontoca2.reporting import assert_no_autonomous_diagnosis

def test_invalid_bbox_is_rejected():
    with pytest.raises(ValidationError):
        BoundingBox(x1=10, y1=10, x2=5, y2=20)

def test_invalid_fdi_is_rejected():
    with pytest.raises(ValidationError):
        ToothInstance(
            instance_id="t1",
            bbox=BoundingBox(x1=0,y1=0,x2=10,y2=10),
            detection_score=0.9,
            fdi_candidate=99,
        )

def test_failed_anatomy_segmentation_is_not_absence():
    status = anatomy_status(0.12, 0.30)
    assert status == DetectionStatus.not_segmented
    assert status.value != "absent"

def test_finding_count_mismatch_is_blocking():
    tooth = ToothInstance(
        instance_id="tooth_26",
        bbox=BoundingBox(x1=1,y1=1,x2=10,y2=10),
        detection_score=0.91,
        fdi_candidate=26,
    )
    finding = Finding(
        finding_id="f1",
        finding_type="caries",
        tooth_instance_id="tooth_26",
        raw_score=0.47,
        location=tooth.bbox,
        model_version="caries-v2",
    )
    result = CaseResult(
        case_id="X",
        image_hash="abc",
        model_version="2.0",
        teeth=[tooth],
        findings=[finding],
        declared_findings_count=2,
    )
    flags = validate_report_consistency(result)
    assert any(f.code == "FINDING_COUNT_MISMATCH" for f in flags)

def test_caries_plus_restoration_requires_review():
    flags = evaluate_tooth_conflict(
        has_restoration=True,
        has_endodontics=False,
        caries_score=0.47,
        caries_threshold=0.30,
    )
    assert flags and flags[0].code == "CARIES_RESTORATIVE_CONFLICT"

def test_gradcam_requires_provenance_and_normalized_map():
    record = ExplainabilityRecord(
        method="GradCAM",
        model_version="caries-v2",
        target_layer="model.21",
        target_class="caries",
        detection_id="det-001",
        heatmap_path="heatmaps/det-001.npy",
    )
    validate_cam_provenance(record)
    validate_cam_array(np.array([[0.0,0.5],[0.2,1.0]], dtype=float))

def test_autonomous_diagnostic_wording_is_rejected():
    with pytest.raises(ValueError):
        assert_no_autonomous_diagnosis("Cárie confirmada no dente 26.")
