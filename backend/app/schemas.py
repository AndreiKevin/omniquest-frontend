from __future__ import annotations

from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    product_name: str
    brand: str
    category: str
    price: float
    quantity: int
    product_id: str
    product_image: str


class ProductsResponse(BaseModel):
    items: List[Product]
    page: int
    page_size: int
    total: int
    has_next: bool


