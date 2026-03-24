# app/schemas/auth.py
from pydantic import BaseModel, Field
from typing import Literal, Optional


class GoogleLoginRequest(BaseModel):
    idToken: str = Field(..., description="Firebase ID token")


class PhoneLoginRequest(BaseModel):
    phone: str = Field(..., description="E.164 format, e.g. +919999999999")
    otp: str = Field(..., description="One‑time password sent to phone")


class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: Literal["bearer"] = "bearer"


class AuthSuccessResponse(BaseModel):
    success: bool = True
    data: TokenResponse
    message: Optional[str] = None
