# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, conint
from typing import List, Literal, Optional
from datetime import date


class LocationSchema(BaseModel):
    latitude: float
    longitude: float


class PreferenceSchema(BaseModel):
    interested_in: List[Literal["MEN", "WOMEN", "BINARY", "EVERYONE"]]
    age_min: conint(ge=18, le=100) = 18
    age_max: conint(ge=18, le=100) = 100
    distance_km: conint(ge=1, le=5000) = 50


class UserCreateSchema(BaseModel):
    first_name: str
    phone: str
    email: EmailStr | None = None
    dob: date
    gender: Literal["MALE", "FEMALE", "NON_BINARY", "OTHER"]
    city: str
    bio: Optional[str] = None
    height_cm: Optional[int] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    living_in: Optional[str] = None
    relationship_goal: Literal["LONG_TERM", "SHORT_TERM", "FRIENDS", "OPEN", "UNSURE"]


class UserResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")
    first_name: str
    email: Optional[EmailStr] = None
    phone: str
    age: int
    city: str
    distance_km: Optional[int] = None
    photos: List[str] = []
    bio: Optional[str] = None
    relationship_goal: str
    gender: str
    status: Literal["UNDER_REVIEW", "APPROVED", "REJECTED"]
    discover_enabled: bool = True

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
