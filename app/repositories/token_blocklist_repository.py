from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.token_blocklist import TokenBlocklist


def add_to_blocklist(db: Session, jti: str, expires_at: datetime) -> None:
    blocked_token = TokenBlocklist(jti=jti, expires_at=expires_at)
    db.add(blocked_token)
    db.commit()


def is_token_blocked(db: Session, jti: str) -> bool:
    statement = select(TokenBlocklist).where(TokenBlocklist.jti == jti)
    result = db.execute(statement).scalars().first()
    return result is not None
