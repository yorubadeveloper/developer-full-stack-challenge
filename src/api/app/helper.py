from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import security
from src.api.app.db import get_db
from src.api.app.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = security.decode_access_token(token)
    if not token_data:
        raise credentials_exception
    user = get_user_by_username(token_data.username)
    if not user:
        raise credentials_exception
    return user


def get_user_by_username(username):
    db: Session = next(get_db())
    return db.query(User).filter(User.username == username).first()
