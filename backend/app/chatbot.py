from __future__ import annotations

from typing import Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .models import ProductORM
from fastembed import TextEmbedding


def search_similar_products(db: Session, embedding: List[float], top_k: int = 8) -> list[ProductORM]:
    # cosine_distance lower is more similar; order ascending
    q = (
        select(ProductORM)
        .order_by(func.cosine_distance(ProductORM.embedding, embedding))
        .limit(top_k)
    )
    return db.execute(q).scalars().all()


_text_model: TextEmbedding | None = None


def get_text_model() -> TextEmbedding:
    global _text_model
    if _text_model is None:
        _text_model = TextEmbedding()
    return _text_model


