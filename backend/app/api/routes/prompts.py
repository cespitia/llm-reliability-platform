from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import get_db
from app.api.schemas.prompts import PromptCreate, PromptRead, PromptVersionCreate, PromptVersionRead
from app.db.models import Prompt, PromptVersion

router = APIRouter(tags=["prompts"])


@router.post("/prompts", response_model=PromptRead, status_code=201)
def create_prompt(payload: PromptCreate, db: Session = Depends(get_db)):
    prompt = Prompt(name=payload.name, description=payload.description)
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return PromptRead(id=prompt.id, name=prompt.name, description=prompt.description)


@router.get("/prompts", response_model=list[PromptRead])
def list_prompts(db: Session = Depends(get_db)):
    prompts = db.exec(select(Prompt).order_by(Prompt.id.desc())).all()
    return [PromptRead(id=p.id, name=p.name, description=p.description) for p in prompts]


@router.post("/prompts/{prompt_id}/versions", response_model=PromptVersionRead, status_code=201)
def create_prompt_version(prompt_id: int, payload: PromptVersionCreate, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Determine next version number
    existing_versions = db.exec(
        select(PromptVersion).where(PromptVersion.prompt_id == prompt_id).order_by(PromptVersion.version.desc())
    ).all()
    next_version = (existing_versions[0].version + 1) if existing_versions else 1

    pv = PromptVersion(
        prompt_id=prompt_id,
        version=next_version,
        template=payload.template,
        model=payload.model,
        temperature=payload.temperature,
    )
    db.add(pv)
    db.commit()
    db.refresh(pv)

    return PromptVersionRead(
        id=pv.id,
        prompt_id=pv.prompt_id,
        version=pv.version,
        template=pv.template,
        model=pv.model,
        temperature=pv.temperature,
    )


@router.get("/prompts/{prompt_id}/versions", response_model=list[PromptVersionRead])
def list_prompt_versions(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    versions = db.exec(
        select(PromptVersion).where(PromptVersion.prompt_id == prompt_id).order_by(PromptVersion.version.desc())
    ).all()

    return [
        PromptVersionRead(
            id=v.id,
            prompt_id=v.prompt_id,
            version=v.version,
            template=v.template,
            model=v.model,
            temperature=v.temperature,
        )
        for v in versions
    ]
