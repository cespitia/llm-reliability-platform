from __future__ import annotations

from sqlmodel import Session, create_engine

from app.core.config import get_database_url

engine = create_engine(get_database_url(), echo=False)


def get_session() -> Session:
    return Session(engine)
