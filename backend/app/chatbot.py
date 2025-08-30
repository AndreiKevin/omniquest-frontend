from __future__ import annotations

from typing import Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .models import ProductORM


def search_similar_products(db: Session, embedding: List[float], top_k: int = 8) -> list[ProductORM]:
    # cosine_distance lower is more similar; order ascending
    q = (
        select(ProductORM)
        .order_by(func.cosine_distance(ProductORM.embedding, embedding))
        .limit(top_k)
    )
    return db.execute(q).scalars().all()


