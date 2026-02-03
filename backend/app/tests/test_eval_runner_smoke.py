from pathlib import Path

from app.eval.runner import run_offline_eval


def test_offline_eval_runner_smoke():
    repo_root = Path(__file__).resolve().parents[3]
    dataset_dir = repo_root / "datasets" / "cicd" / "golden"

    report = run_offline_eval(dataset_dir=dataset_dir)

    assert report["provider"] == "fake"
    assert report["total_cases"] >= 1
    assert 0.0 <= report["pass_rate"] <= 1.0
    assert isinstance(report["results"], list)
