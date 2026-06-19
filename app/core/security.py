from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def create_token(data: dict, expires_in_minutes: int, token_type: str = "access") -> str:
    to_encode = data.copy()
    to_encode["type"] = token_type
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
