from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, JSON, Text, Numeric
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class Trend(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    source = Column(String)
    url = Column(String)
    external_id = Column(String)
    virality_score = Column(Numeric, default=0)
    raw_data = Column(JSON, server_default='{}')
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
