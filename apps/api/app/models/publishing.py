from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, JSON, Text, Boolean
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class SocialAccount(Base):
    __tablename__ = "social_account"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)
    platform = Column(String, nullable=False) # facebook, instagram, twitter, tiktok
    platform_user_id = Column(String)
    username = Column(String)
    access_token = Column(String) # Encrypted at rest in production
    refresh_token = Column(String)
    token_expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PublishJob(Base):
    __tablename__ = "publish_job"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("idea_variant.id"), nullable=False)
    social_account_id = Column(UUID(as_uuid=True), ForeignKey("social_account.id"), nullable=False)
    scheduled_for = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    status = Column(String, default="scheduled") # scheduled, publishing, published, failed
    error_message = Column(Text)
    platform_post_id = Column(String) # ID of the post on the social platform
    created_at = Column(DateTime(timezone=True), server_default=func.now())
