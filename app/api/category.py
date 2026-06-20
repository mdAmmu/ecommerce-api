from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    UpdateCategoryRequest,
    UpdateCategoryResponse,
    DeleteCategoryResponse,
)
from app.services import category_service

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return category_service.create_category(db, data)

@router.put("/", response_model=UpdateCategoryResponse)
def update_category(
    data: UpdateCategoryRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return category_service.update_category(db, data)


@router.get("/", response_model=list[CategoryResponse])
def get_all_category(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return category_service.get_all_categories(db)



@router.delete("/{id}", response_model=DeleteCategoryResponse)
def delete_category(
    id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return category_service.delete_category(db, id)




