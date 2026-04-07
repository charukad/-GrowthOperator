from sqlalchemy import Column, String, DateTime, UUID, JSON, Text, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector
import uuid

Base = declarative_base()

class Trend(Base):
    __tablename__ = "trend"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    source = Column(String)
    url = Column(String)
    external_id = Column(String)
    virality_score = Column(Numeric, default=0)
    raw_data = Column(JSON, server_default='{}')
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TrendEmbedding(Base):
    __tablename__ = "trendembedding"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trend_id = Column(UUID(as_uuid=True), ForeignKey("trend.id", ondelete="CASCADE"), nullable=False, unique=True)
    embedding = Column(Vector(1536))
