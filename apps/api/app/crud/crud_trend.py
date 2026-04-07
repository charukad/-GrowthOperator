from typing import Any, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trend import Trend

class CRUDTrend:
    async def get(self, db: AsyncSession, id: Any) -> Optional[Trend]:
        result = await db.execute(select(Trend).filter(Trend.id == id))
        return result.scalars().first()

    async def get_multi_by_workspace(
        self, db: AsyncSession, *, workspace_id: Any, skip: int = 0, limit: int = 100
    ) -> List[Trend]:
        result = await db.execute(
            select(Trend)
            .filter(Trend.workspace_id == workspace_id)
            .order_by(Trend.virality_score.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

trend = CRUDTrend()
