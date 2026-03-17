from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
    get_password_hash,
)
from app.models.user import User
from app.models.refresh_token import RefreshToken


def create_token_pair(user: User, db: Session) -> dict:
    jti = str(uuid.uuid4())
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "jti": jti}
    )

    db_token = RefreshToken(
        token=jti,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user.to_dict(),
    }


def refresh_access_token(refresh_token_str: str, db: Session) -> Optional[dict]:
    payload = decode_token(refresh_token_str)
    if payload is None or payload.get("type") != "refresh":
        return None

    jti = payload.get("jti")
    username = payload.get("sub")
    if not jti or not username:
        return None

    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == jti, RefreshToken.revoked == False)
        .first()
    )
    if db_token is None:
        return None

    if db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return None

    user = db.query(User).filter(User.username == username).first()
    if user is None or not user.is_active:
        return None

    # Revoke old token (rotation)
    db_token.revoked = True
    db.commit()

    return create_token_pair(user, db)


def revoke_token(jti_or_token: str, db: Session) -> bool:
    # Try to decode if it's a full JWT
    payload = decode_token(jti_or_token)
    if payload and payload.get("jti"):
        jti = payload["jti"]
    else:
        jti = jti_or_token

    db_token = db.query(RefreshToken).filter(RefreshToken.token == jti).first()
    if db_token:
        db_token.revoked = True
        db.commit()
        return True
    return False


def revoke_all_user_tokens(user_id: int, db: Session) -> int:
    count = (
        db.query(RefreshToken)
        .filter(RefreshToken.user_id == user_id, RefreshToken.revoked == False)
        .update({"revoked": True})
    )
    db.commit()
    return count


def cleanup_expired_tokens(db: Session) -> int:
    count = (
        db.query(RefreshToken)
        .filter(RefreshToken.expires_at < datetime.now(timezone.utc))
        .delete()
    )
    db.commit()
    return count


def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_default_admin(db: Session) -> Optional[User]:
    existing = db.query(User).filter(User.role == "superuser").first()
    if existing:
        return None

    admin = User(
        username=settings.DEFAULT_ADMIN_USERNAME,
        email=settings.DEFAULT_ADMIN_EMAIL,
        full_name="System Administrator",
        hashed_password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
        role="superuser",
        is_active=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
