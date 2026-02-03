from app.eval.types import ExpectedConstraints
from app.eval.validators import validate_summary
from app.llm.schemas import IncidentSummary


def test_validate_summary_must_contain_and_min_steps():
    expected = ExpectedConstraints(
        case_id="case_x",
        category="test_failure",
        must_contain=["pytest", "AssertionError"],
        forbidden_contain=["segmentation fault"],
        min_next_steps=2,
    )

    summary = IncidentSummary(
        summary="pytest failed",
        root_cause="AssertionError occurred",
        error_type="test_failure",
        next_steps=["step 1", "step 2"],
        citations=["pytest"],
        confidence="medium",
    )

    violations = validate_summary(summary, expected)
    assert violations == []


def test_validate_summary_detects_forbidden():
    expected = ExpectedConstraints(
        case_id="case_y",
        category="build_failure",
        must_contain=[],
        forbidden_contain=["OutOfMemory"],
        min_next_steps=0,
    )

    summary = IncidentSummary(
        summary="OutOfMemory happened",
        root_cause="OOM",
        error_type="build_failure",
        next_steps=[],
        citations=[],
        confidence="low",
    )

    violations = validate_summary(summary, expected)
    assert "forbidden_contain_present:OutOfMemory" in violations
