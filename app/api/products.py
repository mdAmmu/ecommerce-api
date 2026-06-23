from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, PaginatedProductResponse, GetProductByIdResponse, ProductUpdateRequest, ProductUpdateResponse,DeleteProductResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return product_service.create_product(db, data)

@router.get("/", response_model=PaginatedProductResponse)
def get_all_products(
    page: int = 1,
    limit: int = 20,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    sort_by: str | None = None,
    db: Session = Depends(get_db),
):
    return product_service.get_all_products(
        db,
        page=page,
        limit=limit,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        search=search,
        sort_by=sort_by,
    )


@router.get("/{id}", response_model=GetProductByIdResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, id)


@router.put("/{id}", response_model=ProductUpdateResponse)
def update_product_by_id(
    id: int,
    data: ProductUpdateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return product_service.update_product(db, id, data)

@router.delete("/{id}",response_model=DeleteProductResponse)
def delete_product_by_id(
    id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return product_service.delete_product(db,id)