from typing import Any, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.idea import ContentIdea, IdeaVariant
from app.schemas.idea import ContentIdeaCreate, IdeaVariantCreate

class CRUDIdea:
    async def get(self, db: AsyncSession, id: Any) -> Optional[ContentIdea]:
        result = await db.execute(select(ContentIdea).filter(ContentIdea.id == id))
        return result.scalars().first()

    async def get_multi_by_workspace(
        self, db: AsyncSession, *, workspace_id: Any, skip: int = 0, limit: int = 100
    ) -> List[ContentIdea]:
        result = await db.execute(
            select(ContentIdea)
            .filter(ContentIdea.workspace_id == workspace_id)
            .order_by(ContentIdea.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_with_workspace(
        self, db: AsyncSession, *, obj_in: ContentIdeaCreate, workspace_id: Any
    ) -> ContentIdea:
        db_obj = ContentIdea(
            workspace_id=workspace_id,
            trend_id=obj_in.trend_id,
            brand_id=obj_in.brand_id,
            title=obj_in.title,
            brief=obj_in.brief,
            angle=obj_in.angle,
            platform_goals=obj_in.platform_goals,
            status=obj_in.status
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_variants_by_idea(
        self, db: AsyncSession, *, idea_id: Any
    ) -> List[IdeaVariant]:
        result = await db.execute(
            select(IdeaVariant).filter(IdeaVariant.idea_id == idea_id)
        )
        return list(result.scalars().all())

    async def create_variant(
        self, db: AsyncSession, *, obj_in: IdeaVariantCreate
    ) -> IdeaVariant:
        db_obj = IdeaVariant(
            idea_id=obj_in.idea_id,
            platform=obj_in.platform,
            hook=obj_in.hook,
            caption=obj_in.caption,
            script_data=obj_in.script_data,
            status=obj_in.status
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

idea = CRUDIdea()
