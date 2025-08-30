from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Literal, Any
import os

from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .deps import get_db
from .models import ProductORM
from .chatbot import search_similar_products, get_text_model
from .llm import async_generate_reasoning


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


class ChatRequest(BaseModel):
    query: str
    top_k: int = 8


class ChatResponse(BaseModel):
    message: str
    products: List[Product]


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
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "https://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/categories")
def list_categories(db: Session = Depends(get_db)) -> list[str]:
    if os.getenv("DATABASE_URL"):
        rows = db.execute(select(ProductORM.category).distinct().order_by(ProductORM.category.asc())).all()
        return [row[0] for row in rows]
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
    category: Optional[str] = Query(None, description="Single category (deprecated)"),
    categories: Optional[str] = Query(None, description="Comma-separated categories"),
    sort: Optional[Literal["price_asc", "price_desc"]] = Query(None),
    db: Session = Depends(get_db),
):
    if os.getenv("DATABASE_URL"):
        query = select(ProductORM)
        count_query = select(func.count()).select_from(ProductORM)
        cats = None
        if categories:
            cats = [c for c in categories.split(',') if c]
        elif category:
            cats = [category]
        if cats:
            query = query.where(ProductORM.category.in_(cats))
            count_query = select(func.count()).select_from(ProductORM).where(ProductORM.category.in_(cats))
        if sort == "price_asc":
            query = query.order_by(ProductORM.price.asc())
        elif sort == "price_desc":
            query = query.order_by(ProductORM.price.desc())
        total = db.execute(count_query).scalar_one()
        rows = db.execute(query.offset((page - 1) * page_size).limit(page_size)).scalars().all()
        items = [
            {
                "product_name": r.product_name,
                "brand": r.brand,
                "category": r.category,
                "price": r.price,
                "quantity": r.quantity,
                "product_id": str(r.id),
                "product_image": r.product_image,
            }
            for r in rows
        ]
        has_next = page * page_size < total
        return ProductsResponse(items=[Product(**p) for p in items], page=page, page_size=page_size, total=total, has_next=has_next)

    items = ALL_PRODUCTS

    cats = None
    if categories:
        cats = [c for c in categories.split(',') if c]
    elif category:
        cats = [category]
    if cats:
        items = [p for p in items if p.get("category") in cats]

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


@app.post("/chatbot", response_model=ChatResponse)
async def chatbot(body: ChatRequest, db: Session = Depends(get_db)):
    # FastEmbed query embedding (384 dims by default)
    emb_arr = list(get_text_model().embed([body.query]))[0]
    emb = emb_arr.tolist()
    products = []
    if os.getenv("DATABASE_URL"):
        rows = search_similar_products(db, emb, top_k=body.top_k)
        products = [
            Product(
                product_name=r.product_name,
                brand=r.brand,
                category=r.category,
                price=r.price,
                quantity=r.quantity,
                product_id=str(r.id),
                product_image=r.product_image,
            )
            for r in rows
        ]
    else:
        # fallback: return first K items
        for p in ALL_PRODUCTS[: body.top_k]:
            products.append(Product(**p))

    # Build concise prompt with past conversation context (approx <= 200 words)
    # For simplicity, we include only the current query here; extend as needed with history.
    import json as _json
    products_json = _json.dumps([p.model_dump() for p in products])
    prompt = (
        "You are a shopping assistant. Given the user's query and retrieved products, "
        "explain briefly (<= 150 words) why these products are good recommendations. "
        "Focus on matching category, price suitability, and brand.\n\n"
        f"User query: {body.query}\n\n"
        f"Retrieved products (JSON): {products_json}"
    )
    message = await async_generate_reasoning(prompt)
    return ChatResponse(message=message, products=products)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


