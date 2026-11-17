from pydantic import BaseModel
from datetime import datetime


class ConversationCreate(BaseModel):
    title: str = "New Conversation"


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}