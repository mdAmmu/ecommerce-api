from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.inventory import Inventory
from app.repositories import product_repository, inventory_repository, category_repository
from app.schemas.product import ProductCreate


def create_product(db: Session, data: ProductCreate):
    category = category_repository.get_by_id(db, data.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    new_product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        category_id=data.category_id,
    )
    product_repository.create(db, new_product)

    inventory = Inventory(
        product_id=new_product.id,
        stock_quantity=data.initial_stock,
    )
    inventory_repository.create(db, inventory)

    return {
        "id": new_product.id,
        "name": new_product.name,
        "description": new_product.description,
        "price": new_product.price,
        "category_id": new_product.category_id,
        "category_name": category.name,
        "stock_quantity": inventory.stock_quantity,
        "is_active": new_product.is_active,
        "created_at": new_product.created_at,
        "updated_at": new_product.updated_at,
    }
