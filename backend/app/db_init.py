from __future__ import annotations

import os
from sqlalchemy import text
from .deps import engine
from .models import Base


def init_db() -> None:
    # Ensure pgvector extension with an advisory lock to avoid race conditions
    # when multiple app instances initialize concurrently.
    with engine.begin() as conn:
        # Acquire a session-level advisory lock (arbitrary key)
        conn.execute(text("SELECT pg_advisory_lock(4815162342)"))
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        finally:
            # Always release the advisory lock
            conn.execute(text("SELECT pg_advisory_unlock(4815162342)"))
    # Create tables after extension is available
    Base.metadata.create_all(bind=engine)
    # Create helpful indexes (btree + vector). Some may already exist via SQLAlchemy; IF NOT EXISTS avoids errors.
    with engine.begin() as conn:
        # Composite index for WHERE category IN (...) ORDER BY price
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_category_price_btree ON products (category, price)"))
        # Single-column price index for pure sorting
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_price_btree ON products (price)"))
        # Single-column category index for distinct/order
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_category_btree ON products (category)"))


if __name__ == "__main__":
    init_db()


