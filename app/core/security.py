# app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Mapping

from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: Mapping[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = dict(data)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY.get_secret_value(), algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: Mapping[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = dict(data)
    expire = datetime.utcnow() + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY.get_secret_value(), algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY.get_secret_value(), algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None