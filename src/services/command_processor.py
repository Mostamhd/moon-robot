from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.robot import Direction, Robot


class CommandProcessor:
    """Service for processing robot commands with obstacle detection"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_obstacles(self) -> set[tuple[int, int]]:
        """
        Get obstacles from database
        """
        from src.models.database import Obstacle

        result = await self.db_session.execute(select(Obstacle))
        obstacles = result.scalars().all()
        return {(obstacle.position_x, obstacle.position_y)
                for obstacle in obstacles}

    async def process_commands(
        self,
        command_string: str,
        start_position: tuple[int, int],
        start_direction: Direction,
    ) -> dict[str, Any]:
        """
        Process a command string and return the final robot state.
        Handles obstacle detection as specified in Part II.
        """
        robot = Robot(position=start_position, direction=start_direction)
        obstacles = await self.get_obstacles()
        return robot.execute_commands(command_string, obstacles=obstacles)
