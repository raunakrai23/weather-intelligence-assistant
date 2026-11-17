
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    source_url = Column(Text, nullable=True)
    file_path = Column(Text, nullable=True)
    document_type = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
