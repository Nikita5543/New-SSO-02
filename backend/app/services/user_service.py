from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_password_hash


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
    full_name: Optional[str] = None,
    role: str = "user",
) -> User:
    user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=get_password_hash(password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, **kwargs) -> User:
    if "password" in kwargs and kwargs["password"]:
        user.hashed_password = get_password_hash(kwargs.pop("password"))
    else:
        kwargs.pop("password", None)

    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)  # Allow None to clear fields

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> bool:
    db.delete(user)
    db.commit()
    return True


def get_user_count(db: Session) -> int:
    return db.query(User).count()
