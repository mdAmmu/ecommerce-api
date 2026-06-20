from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


def get_by_name(db: Session, name: str) -> Category | None:
    statement = select(Category).where(Category.name == name)
    return db.execute(statement).scalars().first()

def get_by_id(db: Session, id: int) -> Category | None:
    statement = select(Category).where(Category.id == id, Category.is_active == True)
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

def soft_delete(db: Session, category: Category) -> None:
    category.is_active = False
    db.commit()


def has_active_products(db: Session, category_id: int) -> bool:
    return False


def get_all(db: Session):
    statement = select(Category).where(Category.is_active == True)
    return db.execute(statement).scalars().all()

