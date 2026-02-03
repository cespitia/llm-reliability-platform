from sqlmodel import Session, SQLModel, create_engine, select

from app.db.models import Prompt, PromptVersion


def test_db_models_create_and_insert():
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        prompt = Prompt(name="Incident summarizer", description="Summarize CI/CD failures.")
        session.add(prompt)
        session.commit()
        session.refresh(prompt)

        pv = PromptVersion(prompt_id=prompt.id, version=1, template="Summarize this log: {{log}}")
        session.add(pv)
        session.commit()

        prompts = session.exec(select(Prompt)).all()
        versions = session.exec(select(PromptVersion)).all()

        assert len(prompts) == 1
        assert len(versions) == 1
        assert versions[0].prompt_id == prompts[0].id
