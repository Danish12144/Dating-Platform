# app/schemas/swipe.py
from pydantic import BaseModel, Field
from typing import Literal


class SwipeRequest(BaseModel):
    to_user_id: str = Field(..., min_length=1)  # ✅ constr ki jagah Field
    action: Literal["LIKE", "DISLIKE"]
