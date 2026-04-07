from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, JSON, Text, Numeric
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class ContentIdea(Base):
    __tablename__ = "content_idea"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brand.id"))
    trend_id = Column(UUID(as_uuid=True), ForeignKey("trend.id"))
    title = Column(String, nullable=False)
    brief = Column(Text)
    angle = Column(String)
    platform_goals = Column(JSON, server_default='{}')
    status = Column(String, default="draft") # draft, generated, approved, published
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class IdeaVariant(Base):
    __tablename__ = "idea_variant"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idea_id = Column(UUID(as_uuid=True), ForeignKey("content_idea.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String, nullable=False) # e.g., 'reels', 'tiktok', 'twitter'
    hook = Column(Text)
    caption = Column(Text)
    script_data = Column(JSON, server_default='{}')
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
