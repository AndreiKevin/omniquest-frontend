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

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


