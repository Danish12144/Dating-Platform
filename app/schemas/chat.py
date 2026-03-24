# app/schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageCreateSchema(BaseModel):
    to_user_id: str
    content: Optional[str] = None
    media_url: Optional[str] = None


class MessageResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")
    from_user_id: str
    to_user_id: str
    content: Optional[str] = None
    media_url: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
