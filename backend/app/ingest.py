from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import select
from .deps import SessionLocal
from .models import ProductORM
from .db_init import init_db


def load_repo_data() -> list[dict[str, Any]]:
    repo_root = Path(__file__).resolve().parents[2]
    data_path = repo_root / "data.json"
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def upsert_products(db: Session, data: list[dict[str, Any]]) -> None:
    existing_ids = {row[0] for row in db.execute(select(ProductORM.id)).all()}
    for p in data:
        pid = p.get("product_id")
        if not pid or pid in existing_ids:
            continue
        db.add(
            ProductORM(
                id=pid,
                product_name=p.get("product_name"),
                brand=p.get("brand"),
                category=p.get("category"),
                price=float(p.get("price", 0)),
                quantity=int(p.get("quantity", 0)),
                product_image=p.get("product_image"),
                embedding=None,
            )
        )
    db.commit()


def main() -> None:
    init_db()
    data = load_repo_data()
    with SessionLocal() as db:
        upsert_products(db, data)
    print(f"Ingested {len(data)} products.")


if __name__ == "__main__":
    main()


