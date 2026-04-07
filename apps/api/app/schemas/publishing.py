from typing import Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

# Social Account Schemas
class SocialAccountBase(BaseModel):
    platform: str
    username: Optional[str] = None
    is_active: bool = True

class SocialAccountCreate(SocialAccountBase):
    platform_user_id: Optional[str] = None
    access_token: str
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None

class SocialAccount(SocialAccountBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Publish Job Schemas
class PublishJobBase(BaseModel):
    scheduled_for: Optional[datetime] = None
    status: str = "scheduled"

class PublishJobCreate(PublishJobBase):
    variant_id: uuid.UUID
    social_account_id: uuid.UUID

class PublishJob(PublishJobBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    variant_id: uuid.UUID
    social_account_id: uuid.UUID
    published_at: Optional[datetime] = None
    error_message: Optional[str] = None
    platform_post_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
