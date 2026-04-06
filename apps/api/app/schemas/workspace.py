from typing import Optional, Dict, Any
from pydantic import BaseModel
import uuid
from datetime import datetime

# Shared properties
class WorkspaceBase(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = {}

# Properties to receive via API on creation
class WorkspaceCreate(WorkspaceBase):
    name: str
    slug: str

# Properties to receive via API on update
class WorkspaceUpdate(WorkspaceBase):
    pass

class WorkspaceInDBBase(WorkspaceBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Workspace(WorkspaceInDBBase):
    pass

# Workspace member schemas
class WorkspaceMemberBase(BaseModel):
    user_id: uuid.UUID
    role: str

class WorkspaceMemberCreate(WorkspaceMemberBase):
    pass

class WorkspaceMember(WorkspaceMemberBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    joined_at: datetime

    class Config:
        from_attributes = True
