from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from app.eval.loader import load_golden_cases
from app.eval.types import CaseResult
from app.eval.validators import validate_summary
from app.llm.providers.fake import FakeProvider


def run_offline_eval(
    dataset_dir: Path,
    output_path: Optional[Path] = None,
) -> Dict:
    provider = FakeProvider()
    cases = load_golden_cases(dataset_dir)

    results: List[CaseResult] = []
    violation_counts: Dict[str, int] = {}

    for log_text, expected in cases:
        summary = provider.summarize_incident(log_text)
        violations = validate_summary(summary, expected)

        for v in violations:
            violation_counts[v.split(":")[0]] = violation_counts.get(v.split(":")[0], 0) + 1

        results.append(
            CaseResult(
                case_id=expected.case_id,
                category=expected.category,
                passed=len(violations) == 0,
                violations=violations,
                confidence=summary.confidence,
                error_type=summary.error_type,
            )
        )

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    pass_rate = (passed / total) if total else 0.0

    report = {
        "run_id": datetime.now(timezone.utc).isoformat(),
        "provider": "fake",
        "dataset": str(dataset_dir),
        "total_cases": total,
        "passed_cases": passed,
        "pass_rate": pass_rate,
        "violation_counts": violation_counts,
        "results": [asdict(r) for r in results],
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return report


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]  # backend/app/eval -> repo root
    dataset_dir = repo_root / "datasets" / "cicd" / "golden"
    report = run_offline_eval(dataset_dir=dataset_dir)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
