from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.robot.core.config import settings
from src.robot.models.database import CommandHistory, RobotState
from src.robot.models.robot import Direction, Robot
from src.robot.services.command_processor import CommandProcessor
from src.robot.services.database import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter()


class CommandRequest(BaseModel):
    command: str


class CommandResponse(BaseModel):
    position: dict[str, int]
    direction: str
    obstacle_detected: bool = False
    stopped_at: int | None = None


@router.post("/commands", response_model=CommandResponse)
async def execute_commands(request: CommandRequest, db: DBSession):
    """
    Execute a string of commands and return the final position.
    """
    # Get the latest robot state from database
    result = await db.execute(
        select(RobotState).order_by(RobotState.updated_at.desc()).limit(1)
    )
    robot_state = result.scalars().first()

    # If no state exists, initialize with starting position
    if not robot_state:
        # No eval needed - start_position is already a tuple
        start_position = settings.start_position
        start_direction = Direction[settings.start_direction]
        robot = Robot(position=start_position, direction=start_direction)
    else:
        robot = Robot(
            position=(robot_state.position_x, robot_state.position_y),
            direction=Direction[robot_state.direction],
        )

    # Execute commands with obstacle detection
    command_processor = CommandProcessor(db)
    result = await command_processor.process_commands(
        request.command, (robot.position.x, robot.position.y), robot.direction
    )

    x_position = result["position"]["x"]
    y_position = result["position"]["y"]
    direction = result["direction"]
    obstacle_detected = result["obstacle_detected"]
    stopped_at = result.get("stopped_at")

    # Save command to history
    command_history = CommandHistory(
        command=request.command,
        position_x=x_position,
        position_y=y_position,
        direction=direction,
        obstacle_detected=obstacle_detected,
        stopped_at=stopped_at,
    )
    db.add(command_history)

    # Update robot state
    if not robot_state:
        robot_state = RobotState(
            position_x=x_position, position_y=y_position, direction=direction
        )
        db.add(robot_state)
    else:
        robot_state.position_x = x_position
        robot_state.position_y = y_position
        robot_state.direction = direction

    await db.commit()

    # Format response
    return {
        "position": {"x": x_position, "y": y_position},
        "direction": direction,
        "obstacle_detected": obstacle_detected,
        "stopped_at": stopped_at,
    }
