from sqlalchemy import Column, UUID, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.base_class import Base
import uuid

class TrendEmbedding(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trend_id = Column(UUID(as_uuid=True), ForeignKey("trend.id", ondelete="CASCADE"), nullable=False, unique=True)
    embedding = Column(Vector(1536)) # For OpenAI text-embedding-3-small or similar
    
    trend = relationship("Trend", backref="embedding_obj")
