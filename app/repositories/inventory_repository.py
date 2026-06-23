from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import Inventory

def create(db: Session, inventory: Inventory) -> Inventory:
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


def get_by_product_id(db: Session, product_id: int) -> Inventory | None:
    statement = select(Inventory).where(Inventory.product_id == product_id)
    return db.execute(statement).scalars().first()