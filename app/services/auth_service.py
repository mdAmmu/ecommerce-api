from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from app.models.user import User
from app.schemas.user import UserRegister, UserLogin
from datetime import datetime, timezone
from app.repositories import user_repository, token_blocklist_repository
from app.core.security import verify_password, create_token, decode_token
from app.core.config import settings


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


def login_user(db: Session, data: UserLogin) -> dict:
    user = user_repository.get_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token_data = {"user_id": user.id, "email": user.email, "role": user.role}

    access_token = create_token(token_data, settings.ACCESS_TOKEN_EXPIRE_MINUTES, "access")
    refresh_token = create_token(token_data, settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60, "refresh")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_access_token(refresh_token: str) -> dict:
    try:
        payload = decode_token(refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    token_data = {"user_id": payload["user_id"], "email": payload["email"], "role": payload["role"]}
    new_access_token = create_token(token_data, settings.ACCESS_TOKEN_EXPIRE_MINUTES, "access")

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


def logout_user(db: Session, token: str) -> None:
    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    token_blocklist_repository.add_to_blocklist(db, payload["jti"], expires_at)