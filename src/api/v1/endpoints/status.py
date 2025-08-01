from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config import settings
from src.models.database import RobotState
from src.services.database import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter()


@router.get("/status")
async def get_status(db: DBSession):
    """
    Returns the current position and direction of the robot.
    """
    # Get the latest robot state from database
    result = await db.execute(
        select(RobotState).order_by(RobotState.updated_at.desc()).limit(1)
    )
    robot_state = result.scalars().first()

    if not robot_state:
        # Return initial state from environment variable
        return {
            "position": {
                "x": settings.start_position[0],
                "y": settings.start_position[1],
            },
            "direction": settings.start_direction,
        }

    return {
        "position": {"x": robot_state.position_x, "y": robot_state.position_y},
        "direction": robot_state.direction,
    }
