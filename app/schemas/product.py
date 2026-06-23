from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductCreate(BaseModel):
    name:str
    description:str
    price:float
    category_id:int
    initial_stock:int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    category_name: str
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedProductResponse(BaseModel):
    products: list[ProductResponse]
    total: int
    page: int
    total_pages: int

class GetProductByIdRequest(BaseModel):
    id: int

class GetProductByIdResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_name: str
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)

class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class ProductUpdateResponse(BaseModel):
    message: str