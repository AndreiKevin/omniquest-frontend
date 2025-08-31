from __future__ import annotations

import os
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


# Load variables from a local .env if present
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Default local dev url; docker-compose will override
    "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/omniquest",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=80,
    pool_timeout=30,
    pool_recycle=300,
)
# pool_size=20 → Keep 20 reusable connections open.
# max_overflow=80 → Allow up to 80 extra temporary connections if needed.
# pool_timeout=30 → Wait at most 30s for a connection if pool is full.
# pool_recycle=300 → Refresh connections every 5 minutes.
# pool_pre_ping=True → Ensure connections are valid before use.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


