from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product

def create(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product