from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.product import Product

def create(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_all_filtered(
    db: Session,
    page: int,
    limit: int,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    sort_by: str | None = None,
):
    query = select(Product).where(Product.is_active == True)

    if category_id is not None:
        query = query.where(Product.category_id == category_id)

    if min_price is not None:
        query = query.where(Product.price >= min_price)

    if max_price is not None:
        query = query.where(Product.price <= max_price)

    if search is not None:
        query = query.where(Product.name.ilike(f"%{search}%"))

    count_query = select(func.count()).select_from(query.subquery())
    total = db.execute(count_query).scalar()

    if sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "newest":
        query = query.order_by(Product.created_at.desc())

    query = query.offset((page - 1) * limit).limit(limit)

    products = db.execute(query).scalars().all()

    return products, total

def get_by_id(db: Session, id: int) -> Product | None:
    statement = select(Product).where(Product.id == id, Product.is_active == True)
    return db.execute(statement).scalars().first()

def update_by_id(db: Session, product: Product, updates: dict) -> Product:
    for key, value in updates.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product
