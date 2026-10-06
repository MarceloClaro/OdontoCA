from odontoca2.schemas import DetectionStatus

def anatomy_status(score: float | None, threshold: float) -> DetectionStatus:
    if score is None:
        return DetectionStatus.not_evaluable
    if score < threshold:
        return DetectionStatus.not_segmented
    return DetectionStatus.detected
