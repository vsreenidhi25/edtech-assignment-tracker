# backend/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import get_db
from .auth import decode_access_token
from . import crud, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # tokenUrl only used in docs


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_teacher(user: models.User = Depends(get_current_user)) -> models.User:
    if user.role != models.UserRole.teacher:
        raise HTTPException(status_code=403, detail="Teacher role required")
    return user


def require_student(user: models.User = Depends(get_current_user)) -> models.User:
    if user.role != models.UserRole.student:
        raise HTTPException(status_code=403, detail="Student role required")
    return user