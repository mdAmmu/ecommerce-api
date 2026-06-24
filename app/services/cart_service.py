from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cartItem import CartItem
from app.repositories import cart_repository, product_repository, inventory_repository
from app.schemas.cart import AddCartItem


def add_item_to_cart(db: Session, user_id: int, data: AddCartItem):
    product = product_repository.get_by_id(db, data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    inventory = inventory_repository.get_by_product_id(db, data.product_id)
    available_stock = inventory.stock_quantity if inventory else 0

    cart = cart_repository.get_cart_by_user_id(db, user_id)
    if not cart:
        cart = cart_repository.create_cart(db, user_id)

    existing_item = cart_repository.get_cart_item(db, cart.id, data.product_id)

    if existing_item:
        new_quantity = existing_item.quantity + data.quantity
        if new_quantity > available_stock:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Insufficient stock"
            )
        return cart_repository.update_cart_item_quantity(db, existing_item, new_quantity)
    else:
        if data.quantity > available_stock:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Insufficient stock"
            )
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity,
        )
        return cart_repository.add_cart_item(db, cart_item)


def cart_items(db: Session, user_id: int):
    cart = cart_repository.get_cart_by_user_id(db, user_id)
    if not cart:
        return {"items": [], "item_count": 0, "cart_total": 0.0}

    cart_item_list = cart_repository.get_all_cart_items(db, cart.id)
    if not cart_item_list:
        return {"items": [], "item_count": 0, "cart_total": 0.0}

    items = []
    cart_total = 0.0

    for item in cart_item_list:
        product = product_repository.get_by_id(db, item.product_id)
        line_total = product.price * item.quantity
        cart_total += line_total

        items.append({
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "line_total": line_total,
        })

    return {
        "items": items,
        "item_count": len(items),
        "cart_total": cart_total,
    }
    