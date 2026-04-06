from typing import Any, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.workspace import Workspace, WorkspaceMember
from app.schemas.workspace import WorkspaceCreate

class CRUDWorkspace:
    async def get(self, db: AsyncSession, id: Any) -> Optional[Workspace]:
        result = await db.execute(select(Workspace).filter(Workspace.id == id))
        return result.scalars().first()

    async def get_by_slug(self, db: AsyncSession, *, slug: str) -> Optional[Workspace]:
        result = await db.execute(select(Workspace).filter(Workspace.slug == slug))
        return result.scalars().first()

    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: Any, skip: int = 0, limit: int = 100
    ) -> List[Workspace]:
        result = await db.execute(
            select(Workspace)
            .filter(Workspace.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: WorkspaceCreate, owner_id: Any
    ) -> Workspace:
        db_obj = Workspace(
            name=obj_in.name,
            slug=obj_in.slug,
            description=obj_in.description,
            settings=obj_in.settings,
            owner_id=owner_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        # Add owner as admin member
        member = WorkspaceMember(
            workspace_id=db_obj.id,
            user_id=owner_id,
            role="admin"
        )
        db.add(member)
        await db.commit()
        
        return db_obj

    async def add_member(
        self, db: AsyncSession, *, workspace_id: Any, user_id: Any, role: str
    ) -> WorkspaceMember:
        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role
        )
        db.add(member)
        await db.commit()
        await db.refresh(member)
        return member

    async def get_members(
        self, db: AsyncSession, *, workspace_id: Any
    ) -> List[WorkspaceMember]:
        result = await db.execute(
            select(WorkspaceMember).filter(WorkspaceMember.workspace_id == workspace_id)
        )
        return list(result.scalars().all())

workspace = CRUDWorkspace()
