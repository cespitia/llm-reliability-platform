from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

from app.eval.types import ExpectedConstraints


def load_golden_cases(dataset_dir: Path) -> List[Tuple[str, ExpectedConstraints]]:
    """
    Returns a list of (log_text, constraints) loaded from dataset_dir.

    Expects files:
      case_XXX_input.log
      case_XXX_expected.json
    """
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    expected_files = sorted(dataset_dir.glob("*_expected.json"))
    cases: List[Tuple[str, ExpectedConstraints]] = []

    for expected_path in expected_files:
        stem = expected_path.name.replace("_expected.json", "")
        input_path = dataset_dir / f"{stem}_input.log"
        if not input_path.exists():
            raise FileNotFoundError(f"Missing input log for {expected_path.name}: {input_path}")

        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        constraints = ExpectedConstraints(
            case_id=expected["case_id"],
            category=expected["category"],
            must_contain=expected.get("must_contain", []),
            forbidden_contain=expected.get("forbidden_contain", []),
            min_next_steps=int(expected.get("min_next_steps", 0)),
        )

        log_text = input_path.read_text(encoding="utf-8")
        cases.append((log_text, constraints))

    return cases
