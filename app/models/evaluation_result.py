
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=True)
    actual_answer = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    evaluation_status = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
