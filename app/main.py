
from fastapi import FastAPI, HTTPException
from app.weather.client import get_weather
from app.routers.auth import router as auth_router
from app.routers.conversation import router as conversation_router
from app.routers.message import router as message_router
from app.routers.assistant import router as assistant_router


app = FastAPI(
    title="Weather Intelligence & Advisory Assistant",
    description="An AI-powered assistant for weather information and safety advice.",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(assistant_router)


@app.get("/")
def home():
    return {
        "message": "Weather Intelligence Assistant is running!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Weather Intelligence Assistant"
    }


@app.get("/weather/{city}")
async def weather(city: str):
    try:
        result = await get_weather(city)

        if "error" in result:
            raise HTTPException(
                status_code=404,
                detail=result["error"]
            )

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Weather service error: {str(e)}"
        )
