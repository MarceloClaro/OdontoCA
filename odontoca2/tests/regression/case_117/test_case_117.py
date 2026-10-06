import json
from pathlib import Path

HERE = Path(__file__).parent

def load_meta():
    return json.loads((HERE / "case.json").read_text(encoding="utf-8"))

def test_case117_is_never_training_data():
    assert load_meta()["must_not_be_used_for_training"] is True

def test_case117_ground_truth_is_not_fabricated():
    assert load_meta()["clinical_ground_truth_status"] == "pending_expert_consensus"

def test_case117_has_immutable_source_hash():
    meta = load_meta()
    assert meta["sha256"] == "871bb224a0d93e394704dc9756cd60185b54b65103128d442f5ab404ab179bfb"
