# app/schemas/swipe.py
from pydantic import BaseModel, constr
from typing import Literal


class SwipeRequest(BaseModel):
    to_user_id: constr(min_length=1)   # Mongo ObjectId as string
    action: Literal["LIKE", "DISLIKE"]
