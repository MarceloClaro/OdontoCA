from __future__ import annotations

import hashlib
from pathlib import Path

CASE117_SHA256 = "871bb224a0d93e394704dc9756cd60185b54b65103128d442f5ab404ab179bfb"


def sha256_file(path: str | Path) -> str:
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_case117_source(path: str | Path) -> None:
    digest = sha256_file(path)
    if digest != CASE117_SHA256:
        raise ValueError(
            "CASE_117 source hash mismatch; refusing to run the sentinel case "
            "against a modified image."
        )


def run_case117(path: str | Path, pipeline) -> object:
    verify_case117_source(path)
    return pipeline.run(str(path))
