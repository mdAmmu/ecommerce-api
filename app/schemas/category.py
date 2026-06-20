from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UpdateCategoryRequest(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

class UpdateCategoryResponse(BaseModel):
    message: str

class GetCategoryRequest(BaseModel):
    pass 

class GetCategoryResponse(BaseModel):
    categories: list