from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.services.content_engine import content_engine

router = APIRouter()

@router.get("/", response_model=List[schemas.ContentIdeaWithVariants])
async def read_ideas(
    db: AsyncSession = Depends(deps.get_db),
    workspace_id: str = None,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve ideas for a workspace.
    """
    if not workspace_id:
        raise HTTPException(status_code=400, detail="workspace_id is required")
        
    ideas = await crud.idea.get_multi_by_workspace(db, workspace_id=workspace_id, skip=skip, limit=limit)
    
    # Simple way to append variants for the response
    results = []
    for i in ideas:
        variants = await crud.idea.get_variants_by_idea(db, idea_id=i.id)
        # Using dict and Pydantic validation via response_model
        idea_dict = {
            "id": i.id,
            "workspace_id": i.workspace_id,
            "trend_id": i.trend_id,
            "brand_id": i.brand_id,
            "title": i.title,
            "brief": i.brief,
            "angle": i.angle,
            "platform_goals": i.platform_goals,
            "status": i.status,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
            "variants": variants
        }
        results.append(idea_dict)
        
    return results

@router.post("/generate")
async def generate_ideas(
    *,
    db: AsyncSession = Depends(deps.get_db),
    workspace_id: str = Body(...),
    trend_id: str = Body(...),
    count: int = Body(3),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate ideas from a specific trend.
    """
    # Check workspace
    workspace = await crud.workspace.get(db, id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
        
    # Get trend
    trend = await crud.trend.get(db, id=trend_id)
    if not trend or str(trend.workspace_id) != workspace_id:
        raise HTTPException(status_code=404, detail="Trend not found or access denied")
        
    # Generate ideas via LLM Service
    try:
        generated_ideas = await content_engine.generate_ideas_from_trend(trend=trend, count=count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate ideas: {str(e)}")
        
    # Save ideas to DB
    saved_ideas = []
    for raw_idea in generated_ideas:
        idea_in = schemas.ContentIdeaCreate(
            title=raw_idea.get("title", "Untitled Idea"),
            brief=raw_idea.get("brief", ""),
            angle=raw_idea.get("angle", ""),
            trend_id=trend.id,
            status="generated"
        )
        db_idea = await crud.idea.create_with_workspace(db, obj_in=idea_in, workspace_id=workspace_id)
        
        # If the LLM suggested a platform, create a variant draft
        if raw_idea.get("platform"):
            variant_in = schemas.IdeaVariantCreate(
                idea_id=db_idea.id,
                platform=raw_idea["platform"]
            )
            await crud.idea.create_variant(db, obj_in=variant_in)
            
        saved_ideas.append(db_idea)
        
    return {"message": f"Successfully generated {len(saved_ideas)} ideas", "status": "success"}

@router.post("/{idea_id}/hooks/generate")
async def generate_hooks(
    *,
    db: AsyncSession = Depends(deps.get_db),
    idea_id: str,
    platform: str = Body(...),
    count: int = Body(3),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate hooks for a specific idea and platform.
    """
    idea = await crud.idea.get(db, id=idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
        
    # Generate hooks via LLM Service
    try:
        hooks = await content_engine.generate_hooks_for_idea(
            idea_brief=idea.brief or idea.title, 
            platform=platform, 
            count=count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate hooks: {str(e)}")
        
    return {"hooks": hooks}

@router.post("/variants/{variant_id}/generate-caption")
async def generate_caption(
    *,
    db: AsyncSession = Depends(deps.get_db),
    variant_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate a full caption for a variant based on its idea and hook.
    """
    # 1. Get Variant and Idea
    from sqlalchemy import select
    result = await db.execute(
        select(models.IdeaVariant, models.ContentIdea)
        .join(models.ContentIdea, models.IdeaVariant.idea_id == models.ContentIdea.id)
        .filter(models.IdeaVariant.id == variant_id)
    )
    data = result.first()
    if not data:
        raise HTTPException(status_code=404, detail="Variant not found")
    
    variant, idea = data
    
    if not variant.hook:
        raise HTTPException(status_code=400, detail="A hook is required to generate a caption")

    # 2. Get Brand context if available
    brand = None
    if idea.brand_id:
        brand = await crud.brand.get(db, id=idea.brand_id)

    # 3. Generate via LLM
    try:
        caption = await content_engine.generate_caption(
            idea_brief=idea.brief or idea.title,
            hook=variant.hook,
            platform=variant.platform,
            brand=brand
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    # 4. Save to DB
    variant.caption = caption
    variant.status = "generated"
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    
    return variant

@router.post("/variants/{variant_id}/generate-script")
async def generate_script(
    *,
    db: AsyncSession = Depends(deps.get_db),
    variant_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate a scene-by-scene script for a variant.
    """
    # 1. Get Variant and Idea
    from sqlalchemy import select
    result = await db.execute(
        select(models.IdeaVariant, models.ContentIdea)
        .join(models.ContentIdea, models.IdeaVariant.idea_id == models.ContentIdea.id)
        .filter(models.IdeaVariant.id == variant_id)
    )
    data = result.first()
    if not data:
        raise HTTPException(status_code=404, detail="Variant not found")
    
    variant, idea = data
    
    if not variant.hook:
        raise HTTPException(status_code=400, detail="A hook is required to generate a script")

    # 2. Get Brand context if available
    brand = None
    if idea.brand_id:
        brand = await crud.brand.get(db, id=idea.brand_id)

    # 3. Generate via LLM
    try:
        script_data = await content_engine.generate_script(
            idea_brief=idea.brief or idea.title,
            hook=variant.hook,
            platform=variant.platform,
            brand=brand
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    # 4. Save to DB
    variant.script_data = script_data
    variant.status = "generated"
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    
    return variant
