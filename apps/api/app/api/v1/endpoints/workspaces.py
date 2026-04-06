from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Workspace])
async def read_workspaces(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve workspaces.
    """
    if crud.user.is_super_admin(current_user):
        # Super admin can see all (simplified for now, usually would have a different method)
        workspaces = await crud.workspace.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    else:
        workspaces = await crud.workspace.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return workspaces

@router.post("/", response_model=schemas.Workspace)
async def create_workspace(
    *,
    db: AsyncSession = Depends(deps.get_db),
    workspace_in: schemas.WorkspaceCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new workspace.
    """
    workspace = await crud.workspace.get_by_slug(db, slug=workspace_in.slug)
    if workspace:
        raise HTTPException(
            status_code=400,
            detail="The workspace with this slug already exists in the system.",
        )
    workspace = await crud.workspace.create_with_owner(
        db, obj_in=workspace_in, owner_id=current_user.id
    )
    return workspace

@router.get("/{id}", response_model=schemas.Workspace)
async def read_workspace(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get workspace by ID.
    """
    workspace = await crud.workspace.get(db, id=id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    if not crud.user.is_super_admin(current_user) and (workspace.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough privileges")
    return workspace
