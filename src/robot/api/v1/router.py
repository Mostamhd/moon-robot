from fastapi import APIRouter

from src.robot.api.v1.endpoints import commands, status, test

API_V1_STR = "/api/v1"

api_router = APIRouter()
api_router.include_router(status.router, tags=["status"])
api_router.include_router(commands.router, tags=["commands"])
api_router.include_router(test.router, tags=["test"], include_in_schema=False)
