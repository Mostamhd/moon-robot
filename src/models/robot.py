from enum import Enum
from typing import NamedTuple


class Direction(str, Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class Position(NamedTuple):
    x: int
    y: int


class Robot:
    def __init__(self, position: tuple[int, int], direction: Direction) -> None:
        self.position = Position(*position)
        self.direction = direction
        self.obstacle_detected = False

    def move_forward(self) -> None:
        """Move the robot forward one unit in the current direction"""
        x, y = self.position

        if self.direction == Direction.NORTH:
            y += 1
        elif self.direction == Direction.SOUTH:
            y -= 1
        elif self.direction == Direction.EAST:
            x += 1
        elif self.direction == Direction.WEST:
            x -= 1

        self.position = Position(x, y)

    def move_backward(self) -> None:
        """Move the robot backward one unit in the current direction"""
        x, y = self.position

        if self.direction == Direction.NORTH:
            y -= 1
        elif self.direction == Direction.SOUTH:
            y += 1
        elif self.direction == Direction.EAST:
            x -= 1
        elif self.direction == Direction.WEST:
            x += 1

        self.position = Position(x, y)

    def rotate_left(self) -> None:
        """Rotate the robot 90 degrees to the left (counter-clockwise)"""
        if self.direction == Direction.NORTH:
            self.direction = Direction.WEST
        elif self.direction == Direction.WEST:
            self.direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.EAST
        elif self.direction == Direction.EAST:
            self.direction = Direction.NORTH

    def rotate_right(self) -> None:
        """Rotate the robot 90 degrees to the right (clockwise)"""
        if self.direction == Direction.NORTH:
            self.direction = Direction.EAST
        elif self.direction == Direction.EAST:
            self.direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.WEST
        elif self.direction == Direction.WEST:
            self.direction = Direction.NORTH

    def process_command(self, command: str) -> bool:
        """
        Process a single command character.
        Returns True if movement occurred, False for rotation commands.
        """
        if command == "F":
            self.move_forward()
            return True
        if command == "B":
            self.move_backward()
            return True
        if command == "L":
            self.rotate_left()
            return False
        if command == "R":
            self.rotate_right()
            return False
        return False
