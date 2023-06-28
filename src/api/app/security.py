from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from .config import jwt_secret_key
from src.api.app.schemas import TokenPayload

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except JWTError:
        return None
    return token_data
