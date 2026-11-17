
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database.connection import Base


class WeatherAPILog(Base):
    __tablename__ = "weather_api_logs"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
