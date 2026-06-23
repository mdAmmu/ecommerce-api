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

def get_all_products(
    db: Session,
    page: int,
    limit: int,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    sort_by: str | None = None,
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Page must be at least 1"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be between 1 and 100"
        )

    products, total = product_repository.get_all_filtered(
        db,
        page=page,
        limit=limit,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        search=search,
        sort_by=sort_by,
    )

    import math
    total_pages = math.ceil(total / limit) if total > 0 else 0

    product_list = []
    for product in products:
        category = category_repository.get_by_id(db, product.category_id)
        inventory = inventory_repository.get_by_product_id(db, product.id)

        product_list.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
            "category_name": category.name if category else "Unknown",
            "stock_quantity": inventory.stock_quantity if inventory else 0,
            "is_active": product.is_active,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
        })

    return {
        "products": product_list,
        "total": total,
        "page": page,
        "total_pages": total_pages,
    }