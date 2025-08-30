from __future__ import annotations

from typing import Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func, cast, literal
from .models import ProductORM
from pgvector.sqlalchemy import Vector
from fastembed import TextEmbedding


def search_similar_products(db: Session, embedding: List[float], top_k: int = 8) -> list[ProductORM]:
    # Cast the Python list to a Postgres vector so the function signature matches
    vec_param = cast(literal(embedding), Vector(384))
    distance = ProductORM.embedding.op('<=>')(vec_param)
    q = select(ProductORM).order_by(distance.asc()).limit(top_k)
    return db.execute(q).scalars().all()


_text_model: TextEmbedding | None = None


def get_text_model() -> TextEmbedding:
    global _text_model
    if _text_model is None:
        _text_model = TextEmbedding()
    return _text_model


