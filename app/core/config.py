# app/core/config.py
from pydantic import BaseSettings, Field, SecretStr
from typing import List

class Settings(BaseSettings):
    # ---- General ----
    APP_NAME: str = "Social Dating Platform"
    API_V1_STR: str = "/api/v1"

    # ---- MongoDB ----
    MONGO_URI: str = Field(..., env="MONGO_URI")
    MONGO_DB_NAME: str = Field(default="dating", env="MONGO_DB_NAME")

    # ---- JWT ----
    JWT_SECRET_KEY: SecretStr = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ---- Firebase ----
    FIREBASE_PROJECT_ID: str = Field(..., env="FIREBASE_PROJECT_ID")
    FIREBASE_CLIENT_EMAIL: str = Field(..., env="FIREBASE_CLIENT_EMAIL")
    FIREBASE_PRIVATE_KEY: str = Field(..., env="FIREBASE_PRIVATE_KEY")

    # ---- Cloudflare R2 ----
    R2_ACCOUNT_ID: str = Field(..., env="R2_ACCOUNT_ID")
    R2_ACCESS_KEY_ID: str = Field(..., env="R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY: str = Field(..., env="R2_SECRET_ACCESS_KEY")
    R2_BUCKET_NAME: str = Field(..., env="R2_BUCKET_NAME")
    R2_REGION: str = Field(default="auto", env="R2_REGION")

    # ---- CORS (dev) ----
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
