
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate, MessageResponse
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["Messages"]
)


@router.post("/", response_model=MessageResponse, status_code=201)
def create_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    new_message = Message(
        conversation_id=conversation_id,
        role=message_data.role,
        content=message_data.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@router.get("/", response_model=list[MessageResponse])
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    return messages
