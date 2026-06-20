from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


def get_by_name(db: Session, name: str) -> Category | None:
    statement = select(Category).where(Category.name == name)
    return db.execute(statement).scalars().first()

def get_by_id(db: Session, id: int) -> Category | None:
    statement = select(Category).where(Category.id == id)
    return db.execute(statement).scalars().first()

def create(db: Session, category: Category) -> Category:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update(db: Session, category: Category, updates: dict) -> Category:
    for key, value in updates.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete(db: Session, id: int) -> None:
    category = get_by_id(db, id)
    if category:
        db.delete(category)
        db.commit()

def get_all(db: Session):
    statement = select(Category)
    return db.execute(statement).scalars().all()

