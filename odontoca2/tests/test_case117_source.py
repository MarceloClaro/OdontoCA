from pathlib import Path
import pytest

from odontoca2.case117 import CASE117_SHA256, verify_case117_source


def test_case117_hash_constant_matches_registered_fixture():
    assert CASE117_SHA256 == "871bb224a0d93e394704dc9756cd60185b54b65103128d442f5ab404ab179bfb"


def test_case117_rejects_modified_bytes(tmp_path: Path):
    p = tmp_path / "117.jpg"
    p.write_bytes(b"not-the-original-radiograph")
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_case117_source(p)
