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
    # Create helpful indexes (btree + vector). Some may already exist via SQLAlchemy; IF NOT EXISTS avoids errors.
    with engine.begin() as conn:
        # Composite index for WHERE category IN (...) ORDER BY price
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_category_price_btree ON products (category, price)"))
        # Single-column price index for pure sorting
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_price_btree ON products (price)"))
        # Single-column category index for distinct/order
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_category_btree ON products (category)"))
        # Vector IVFFlat index for cosine similarity (requires pgvector). Choose a conservative lists value.
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_embedding_cos ON products USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"))


if __name__ == "__main__":
    init_db()


