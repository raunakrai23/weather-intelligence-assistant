
import json

from app.services.query_router import route_query
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import get_current_user
from app.models.conversation import Conversation
from app.models.message import Message
from app.rag.answer import answer_weather_question
from app.weather.client import get_weather

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


class AskRequest(BaseModel):
    conversation_id: int
    question: str = Field(min_length=1)
    city: str | None = None


class AskResponse(BaseModel):
    question: str
    answer: str


@router.post("/ask", response_model=AskResponse)
async def ask_assistant(
    request: AskRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    try:
        # Step 1: Classify the question
        routing = route_query(request.question)

        requires_weather = routing["requires_weather"]
        requires_rag = routing["requires_rag"]

        # Step 2: Handle out-of-scope questions
        if routing["intent"] in ["out_of_scope", "general"]:
            answer = (
                "I can help with weather information and "
                "weather-safety questions. Please ask me "
                "something related to weather."
            )

        else:
            weather_context = None

            # Step 3: Fetch weather if required
            if requires_weather:

                if not request.city or not request.city.strip():
                    raise HTTPException(
                        status_code=422,
                        detail="Please provide a city for weather information."
                    )

                weather_data = await get_weather(request.city.strip())

                if "error" in weather_data:
                    raise HTTPException(
                        status_code=404,
                        detail=weather_data["error"]
                    )

                # Step 4: Extract only tomorrow's forecast
                daily = weather_data.get("daily_forecast") or {}

                tomorrow_forecast = {}

                for key, values in daily.items():
                    if isinstance(values, list) and len(values) > 1:
                        tomorrow_forecast[key] = values[1]

                # Step 5: Create compact weather context
                compact_weather_data = {
                    "location": weather_data.get("location"),
                    "current_weather": weather_data.get("current_weather"),
                    "tomorrow_forecast": tomorrow_forecast,
                    "units": weather_data.get("units")
                }

                weather_context = json.dumps(
                    compact_weather_data,
                    indent=2
                )

            # Step 6: Generate AI response
            answer = answer_weather_question(
                db=db,
                question=request.question,
                weather_context=weather_context,
                include_rag=requires_rag
            )

        # Step 7: Save conversation messages
        db.add(
            Message(
                conversation_id=conversation.id,
                role="user",
                content=request.question
            )
        )

        db.add(
            Message(
                conversation_id=conversation.id,
                role="assistant",
                content=answer
            )
        )

        db.commit()

        return AskResponse(
            question=request.question,
            answer=answer
        )

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Assistant error: {str(e)}"
        )
