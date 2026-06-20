from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import Inventory

def create(db: Session, inventory: Inventory) -> Inventory:
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory