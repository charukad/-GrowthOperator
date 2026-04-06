from typing import Optional, Dict, Any
from pydantic import BaseModel
import uuid
from datetime import datetime

# Shared properties
class TrendBase(BaseModel):
    title: str
    summary: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    external_id: Optional[str] = None
    virality_score: Optional[float] = 0.0
    raw_data: Optional[Dict[str, Any]] = {}

# Properties to return via API
class Trend(TrendBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    detected_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
