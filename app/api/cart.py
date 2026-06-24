from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.schemas.cart import AddCartItem, CartItemResponse,CartResponse
from app.services import cart_service
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_item(
    data: AddCartItem,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return cart_service.add_item_to_cart(db, current_user.id, data)


@router.get("/items", response_model=CartResponse)
def view_cart_item(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return cart_service.cart_items(db, current_user.id)