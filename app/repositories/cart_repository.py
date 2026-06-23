from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cartItem import CartItem


def get_cart_by_user_id(db: Session, user_id: int) -> Cart | None:
    statement = select(Cart).where(Cart.user_id == user_id)
    return db.execute(statement).scalars().first()


def create_cart(db: Session, user_id: int) -> Cart:
    cart = Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def get_cart_item(db: Session, cart_id: int, product_id: int) -> CartItem | None:
    statement = select(CartItem).where(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id,
    )
    return db.execute(statement).scalars().first()


def add_cart_item(db: Session, cart_item: CartItem) -> CartItem:
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def update_cart_item_quantity(db: Session, cart_item: CartItem, quantity: int) -> CartItem:
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item
