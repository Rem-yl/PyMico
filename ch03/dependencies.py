from typing import Annotated

from database import UserDatabase, get_user_db
from fastapi import Depends, HTTPException
from model import User


def get_current_user(
    username: str, password: str, user_db: Annotated[UserDatabase, Depends(get_user_db)]
) -> User:
    user = user_db.get_user(username)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


def admin_required(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    return user
