import bcrypt
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repository
from app.schemas.user import UserUpdate


def update_user(db: Session, current_user: User, data: UserUpdate) -> User:
    updates = {}

    if data.full_name is not None:
        updates["full_name"] = data.full_name

    if data.password is not None:
        updates["hashed_password"] = bcrypt.hashpw(
            data.password.encode(), bcrypt.gensalt()
        ).decode()

    if not updates:
        return current_user

    return user_repository.update_user(db, current_user, updates)
