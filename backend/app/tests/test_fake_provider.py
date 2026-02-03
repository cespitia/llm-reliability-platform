from app.llm.providers.fake import FakeProvider


def test_fake_provider_returns_valid_schema_for_pytest_failure():
    log_text = """
Run pytest
FAILED tests/test_math.py::test_addition - AssertionError: expected 2, got 3
"""
    provider = FakeProvider()
    result = provider.summarize_incident(log_text)

    assert result.error_type == "test_failure"
    assert result.confidence in {"low", "medium", "high"}
    assert isinstance(result.next_steps, list)
    assert len(result.next_steps) >= 2
    assert "pytest" in result.citations or any("test_" in c for c in result.citations)


def test_fake_provider_dependency_failure():
    log_text = """
Run npm ci
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
"""
    provider = FakeProvider()
    result = provider.summarize_incident(log_text)

    assert result.error_type == "dependency_failure"
    assert len(result.next_steps) >= 2
