from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.post("/", response_model=ConversationResponse, status_code=201)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_conversation = Conversation(
        title=conversation_data.title,
        user_id=current_user.id
    )

    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation


@router.get("/", response_model=list[ConversationResponse])
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
        .all()
    )

    return conversations


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return conversation