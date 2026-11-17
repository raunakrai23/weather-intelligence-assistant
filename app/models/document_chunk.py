
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import DateTime
from pgvector.sqlalchemy import Vector
from app.database.connection import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding = Column(Vector(384), nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
