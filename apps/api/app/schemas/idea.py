from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import uuid
from datetime import datetime

# Idea Variant Schemas
class IdeaVariantBase(BaseModel):
    platform: str
    hook: Optional[str] = None
    caption: Optional[str] = None
    script_data: Optional[Dict[str, Any]] = {}
    status: str = "draft"

class IdeaVariantCreate(IdeaVariantBase):
    idea_id: uuid.UUID

class IdeaVariantUpdate(IdeaVariantBase):
    pass

class IdeaVariant(IdeaVariantBase):
    id: uuid.UUID
    idea_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Content Idea Schemas
class ContentIdeaBase(BaseModel):
    title: str
    brief: Optional[str] = None
    angle: Optional[str] = None
    platform_goals: Optional[Dict[str, Any]] = {}
    status: str = "draft"

class ContentIdeaCreate(ContentIdeaBase):
    trend_id: Optional[uuid.UUID] = None
    brand_id: Optional[uuid.UUID] = None

class ContentIdeaUpdate(ContentIdeaBase):
    pass

class ContentIdea(ContentIdeaBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    trend_id: Optional[uuid.UUID] = None
    brand_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ContentIdeaWithVariants(ContentIdea):
    variants: List[IdeaVariant] = []
