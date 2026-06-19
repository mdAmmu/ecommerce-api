from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserRegister, UserResponse,TokenResponse,UserLogin
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)


@router.get("/get_user", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(email: str,  db: Session = Depends(get_db)):
    return auth_service.get_user(db, email)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(data: UserLogin,  db: Session = Depends(get_db)):
    return auth_service.login_user(db, data)


