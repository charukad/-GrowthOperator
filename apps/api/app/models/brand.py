from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class Brand(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)
    name = Column(String, nullable=False)
    niche = Column(String)
    description = Column(Text)
    tone_profile = Column(Text)
    target_audience = Column(Text)
    content_pillars = Column(JSON, server_default='[]')
    banned_phrases = Column(JSON, server_default='[]')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
