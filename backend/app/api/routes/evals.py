from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import get_db
from app.api.schemas.evals import EvalCaseResultRead, EvalRunRead
from app.db.models import EvalCaseResult, EvalRun, PromptVersion
from app.eval.runner import run_offline_eval

router = APIRouter(tags=["evals"])


@router.post("/evals/run", response_model=EvalRunRead, status_code=201)
def run_eval(prompt_version_id: int | None = None, db: Session = Depends(get_db)):
    # Optional: tie the eval to a prompt version (for now, not used by FakeProvider)
    if prompt_version_id is not None:
        pv = db.get(PromptVersion, prompt_version_id)
        if not pv:
            raise HTTPException(status_code=404, detail="Prompt version not found")

    repo_root = Path(__file__).resolve().parents[4]
    dataset_dir = repo_root / "datasets" / "cicd" / "golden"

    report = run_offline_eval(dataset_dir=dataset_dir)

    eval_run = EvalRun(
        prompt_version_id=prompt_version_id,
        provider=report["provider"],
        dataset="datasets/cicd/golden",
        total_cases=report["total_cases"],
        passed_cases=report["passed_cases"],
        pass_rate=report["pass_rate"],
    )
    db.add(eval_run)
    db.commit()
    db.refresh(eval_run)

    # Persist per-case results
    for r in report["results"]:
        db.add(
            EvalCaseResult(
                eval_run_id=eval_run.id,
                case_id=r["case_id"],
                category=r["category"],
                passed=r["passed"],
                error_type=r.get("error_type"),
                confidence=r.get("confidence"),
                violations_json=json.dumps(r.get("violations", [])),
            )
        )
    db.commit()

    return EvalRunRead(
        id=eval_run.id,
        provider=eval_run.provider,
        dataset=eval_run.dataset,
        total_cases=eval_run.total_cases,
        passed_cases=eval_run.passed_cases,
        pass_rate=eval_run.pass_rate,
        prompt_version_id=eval_run.prompt_version_id,
    )


@router.get("/evals/runs", response_model=list[EvalRunRead])
def list_eval_runs(db: Session = Depends(get_db)):
    runs = db.exec(select(EvalRun).order_by(EvalRun.id.desc())).all()
    return [
        EvalRunRead(
            id=r.id,
            provider=r.provider,
            dataset=r.dataset,
            total_cases=r.total_cases,
            passed_cases=r.passed_cases,
            pass_rate=r.pass_rate,
            prompt_version_id=r.prompt_version_id,
        )
        for r in runs
    ]


@router.get("/evals/runs/{run_id}", response_model=list[EvalCaseResultRead])
def get_eval_run_details(run_id: int, db: Session = Depends(get_db)):
    run = db.get(EvalRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Eval run not found")

    rows = db.exec(select(EvalCaseResult).where(EvalCaseResult.eval_run_id == run_id)).all()

    return [
        EvalCaseResultRead(
            case_id=row.case_id,
            category=row.category,
            passed=row.passed,
            error_type=row.error_type,
            confidence=row.confidence,
            violations=json.loads(row.violations_json),
        )
        for row in rows
    ]
