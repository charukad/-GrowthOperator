from fastapi import APIRouter
from app.api.v1.endpoints import login, users, workspaces, trends

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(trends.router, prefix="/trends", tags=["trends"])
