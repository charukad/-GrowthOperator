from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app import crud, models, schemas
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()

@router.post("/scrape")
async def trigger_scrape(
    *,
    db: AsyncSession = Depends(deps.get_db),
    workspace_id: str = Body(...),
    niche: str = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Trigger a background scraping task for a specific niche.
    """
    # Check if user has access to workspace
    workspace = await crud.workspace.get(db, id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Send task to Celery
    task = celery_app.send_task(
        "scrape_reddit_trends", 
        args=[workspace_id, niche],
        queue="trend-queue"
    )
    
    return {"task_id": task.id, "status": "pending"}

@router.get("/", response_model=List[schemas.Trend])
async def read_trends(
    db: AsyncSession = Depends(deps.get_db),
    workspace_id: str = None,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve trends for a workspace.
    """
    if not workspace_id:
        raise HTTPException(status_code=400, detail="workspace_id is required")
        
    result = await db.execute(
        select(models.Trend)
        .filter(models.Trend.workspace_id == workspace_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
