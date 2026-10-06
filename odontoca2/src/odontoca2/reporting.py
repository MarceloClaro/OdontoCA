from odontoca2.schemas import CaseResult
from odontoca2.consistency import validate_report_consistency

FORBIDDEN_AUTONOMOUS_PHRASES = {
    "cárie confirmada",
    "diagnóstico definitivo",
    "paciente possui cárie com certeza",
}

def build_safe_summary(result: CaseResult) -> dict:
    flags = validate_report_consistency(result)
    blocking = [f for f in flags if f.severity == "blocking"]
    return {
        "case_id": result.case_id,
        "model_version": result.model_version,
        "total_teeth_segmented": len(result.teeth),
        "total_findings": len(result.findings),
        "declared_findings_count": result.declared_findings_count,
        "human_review_required": True,
        "status": "blocked" if blocking else "review_required",
        "consistency_flags": [f.__dict__ for f in flags],
        "disclaimer": (
            "Saída automatizada para apoio à revisão profissional. "
            "Scores do modelo não são probabilidades clínicas."
        ),
    }

def assert_no_autonomous_diagnosis(text: str) -> None:
    lower = text.lower()
    for phrase in FORBIDDEN_AUTONOMOUS_PHRASES:
        if phrase in lower:
            raise ValueError(f"Forbidden autonomous diagnostic wording: {phrase}")
