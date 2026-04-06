from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class Workspace(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    description = Column(String)
    settings = Column(JSON, server_default='{}')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class WorkspaceMember(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    role = Column(String, nullable=False) # e.g., 'admin', 'member', 'editor'
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
