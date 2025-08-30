from __future__ import annotations

import os
from sqlalchemy import text
from .deps import engine
from .models import Base


def init_db() -> None:
    # Ensure pgvector extension in a committed transaction
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    # Create tables after extension is available
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()


