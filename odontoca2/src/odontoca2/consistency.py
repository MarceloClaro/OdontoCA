from dataclasses import dataclass
from odontoca2.schemas import CaseResult

DENTAL_FINDINGS = {
    "caries",
    "deep_caries",
    "restoration",
    "endodontic_treatment",
    "periapical_lesion",
}

@dataclass(frozen=True)
class ConsistencyFlag:
    code: str
    severity: str
    message: str

def validate_report_consistency(result: CaseResult) -> list[ConsistencyFlag]:
    flags: list[ConsistencyFlag] = []

    if result.declared_findings_count != len(result.findings):
        flags.append(ConsistencyFlag(
            "FINDING_COUNT_MISMATCH",
            "blocking",
            "Declared finding count does not match traceable records."
        ))

    tooth_ids = {t.instance_id for t in result.teeth}
    for finding in result.findings:
        if finding.finding_type in DENTAL_FINDINGS:
            if not finding.tooth_instance_id:
                flags.append(ConsistencyFlag(
                    "DENTAL_FINDING_WITHOUT_TOOTH",
                    "blocking",
                    f"{finding.finding_id} has no tooth reference."
                ))
            elif finding.tooth_instance_id not in tooth_ids:
                flags.append(ConsistencyFlag(
                    "DENTAL_FINDING_UNKNOWN_TOOTH",
                    "blocking",
                    f"{finding.finding_id} references an unknown tooth."
                ))

    fdis = [t.fdi_candidate for t in result.teeth if t.fdi_candidate is not None]
    if len(fdis) != len(set(fdis)):
        flags.append(ConsistencyFlag(
            "DUPLICATE_FDI",
            "blocking",
            "Duplicate FDI assignment detected."
        ))

    return flags

def evaluate_tooth_conflict(
    *,
    has_restoration: bool,
    has_endodontics: bool,
    caries_score: float | None,
    caries_threshold: float,
) -> list[ConsistencyFlag]:
    if (
        caries_score is not None
        and caries_score >= caries_threshold
        and (has_restoration or has_endodontics)
    ):
        return [ConsistencyFlag(
            "CARIES_RESTORATIVE_CONFLICT",
            "review_required",
            "Caries prediction overlaps restorative/endodontic material; human review required."
        )]
    return []
