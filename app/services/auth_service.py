from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from app.models.user import User
from app.schemas.user import UserRegister
from app.repositories import user_repository


def register_user(db: Session, data: UserRegister) -> User:
    existing_user = user_repository.get_by_email(db, data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    new_user = User(
        email=data.email,
        hashed_password=hashed_password,
        full_name=data.full_name,
    )

    return user_repository.create_user(db, new_user)


def get_user(db: Session, email: str) -> User:
    user_detail = user_repository.get_by_email(db, email)
    if not user_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_detail