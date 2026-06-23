from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class AddCartItem(BaseModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v


class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)
