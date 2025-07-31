from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.robot.core.config import settings
from src.robot.models.database import RobotState
from src.robot.services.database import get_db

router = APIRouter()

DBSession = Annotated[Session, Depends(get_db)]


@router.get("/reset")
def reset_robot(
    db: DBSession,
    position: str | None = Query(None, description="New position as (x,y)"),
    direction: str | None = Query(None, description="New direction"),
):
    """
    Reset the robot state for testing purposes.
    Accepts optional position and direction parameters.
    """
    # Parse position if provided
    if position:
        try:
            pos = eval(position)
            if not isinstance(pos, tuple) or len(pos) != 2:
                raise ValueError
        except Exception as e:
            return {"error": "Invalid position format. Use '(x,y)'", "details": e}
    else:
        pos = eval(settings.start_position)

    # Use provided direction or default
    dir = direction if direction else settings.start_direction

    # Validate direction
    if dir not in ["NORTH", "SOUTH", "EAST", "WEST"]:
        return {"error": "Invalid direction. Must be NORTH, SOUTH, EAST, or WEST"}

    # Clear existing state and create new one
    db.query(RobotState).delete()
    new_state = RobotState(position_x=pos[0], position_y=pos[1], direction=dir)
    db.add(new_state)
    db.commit()

    return {"position": {"x": pos[0], "y": pos[1]}, "direction": dir}
