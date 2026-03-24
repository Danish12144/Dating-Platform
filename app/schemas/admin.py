# app/schemas/admin.py
from pydantic import BaseModel
from typing import Literal, Optional


class AdminActionSchema(BaseModel):
    action: Literal["APPROVE", "REJECT"]
    reason: Optional[str] = None
    remark: Optional[str] = None
