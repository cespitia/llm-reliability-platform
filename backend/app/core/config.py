from __future__ import annotations

import os


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        # Safe local default for running outside Docker. You can override via env.
        url = "sqlite:///./local.db"
    return url
