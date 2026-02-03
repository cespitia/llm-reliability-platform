from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (nothing needed yet)


app = FastAPI(
    title="LLM Reliability Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router, prefix="/api")
