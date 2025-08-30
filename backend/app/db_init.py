from __future__ import annotations

import os
from sqlalchemy import text
from .deps import engine
from .models import Base


def init_db() -> None:
    with engine.connect() as conn:
        # Ensure pgvector extension
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        except Exception:
            pass
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()


