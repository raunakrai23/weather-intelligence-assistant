
from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class MessageCreate(BaseModel):
    role: Literal["user"] = "user"
    content: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
