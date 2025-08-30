from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Literal, Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json


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


def _load_products_from_repo() -> list[dict[str, Any]]:
    # repo_root = omniquest-frontend/ (two levels up from this file)
    repo_root = Path(__file__).resolve().parents[2]
    data_path = repo_root / "data.json"
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


ALL_PRODUCTS: list[dict[str, Any]] = _load_products_from_repo()


app = FastAPI(title="OmniQuest Grocery API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/categories")
def list_categories() -> list[str]:
    seen: set[str] = set()
    for p in ALL_PRODUCTS:
        c = p.get("category")
        if isinstance(c, str):
            seen.add(c)
    return sorted(seen)


@app.get("/products", response_model=ProductsResponse)
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100),
    category: Optional[str] = Query(None),
    sort: Optional[Literal["price_asc", "price_desc"]] = Query(None),
):
    items = ALL_PRODUCTS

    if category:
        items = [p for p in items if p.get("category") == category]

    if sort == "price_asc":
        items = sorted(items, key=lambda p: float(p.get("price", 0)))
    elif sort == "price_desc":
        items = sorted(items, key=lambda p: float(p.get("price", 0)), reverse=True)

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = items[start:end]
    has_next = end < total

    return ProductsResponse(
        items=[Product(**p) for p in page_items],
        page=page,
        page_size=page_size,
        total=total,
        has_next=has_next,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


