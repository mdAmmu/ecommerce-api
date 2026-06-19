from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserRegister, UserResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)


@router.get("/get_user", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(email: str,  db: Session = Depends(get_db)):
    return auth_service.get_user(db, email)

