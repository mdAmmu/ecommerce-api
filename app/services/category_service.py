from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories import category_repository
from app.schemas.category import CategoryCreate, UpdateCategoryRequest


def create_category(db: Session, data: CategoryCreate) -> Category:
    existing = category_repository.get_by_name(db, data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists"
        )

    new_category = Category(
        name=data.name,
        description=data.description,
    )

    return category_repository.create(db, new_category)

def update_category(db: Session, data: UpdateCategoryRequest):
    category = category_repository.get_by_id(db, data.id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    updates = {}
    if data.name is not None:
        updates["name"] = data.name
    if data.description is not None:
        updates["description"] = data.description

    if not updates:
        return {"message": "Nothing to update"}

    category_repository.update(db, category, updates)
    return {"message": "Category Update Successful"}


def get_all_categories(db: Session):
    return category_repository.get_all(db)


def delete_category(db: Session, id: int):
    category = category_repository.get_by_id(db, id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    if category_repository.has_active_products(db, id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete category with active products"
        )

    category_repository.soft_delete(db, category)
    return {"message": "Category deleted successfully"}

    