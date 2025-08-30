from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class ProductORM(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=False), primary_key=True)
    product_name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    product_image = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=True)  # OpenAI text-embedding-3-large dims

    __table_args__ = (
        Index("ix_products_category_price", "category", "price"),
    )


