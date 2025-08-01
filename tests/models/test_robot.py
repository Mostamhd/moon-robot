import pytest
from src.models.robot import Robot, Direction

def test_robot_initialization():
    """Test robot initialization with default values"""
    robot = Robot((0, 0), Direction.NORTH)
    assert robot.position.x == 0
    assert robot.position.y == 0
    assert robot.direction == Direction.NORTH

def test_robot_move_forward():
    """Test robot moving forward in different directions"""
    # Test moving north
    robot = Robot((0, 0), Direction.NORTH)
    robot.move_forward()
    assert robot.position.x == 0
    assert robot.position.y == 1

def test_robot_move_backward():
    """Test robot moving backward in different directions"""
    # Test moving south (backward from north)
    robot = Robot((0, 0), Direction.NORTH)
    robot.move_backward()
    assert robot.position.x == 0
    assert robot.position.y == -1

def test_robot_rotate_left():
    """Test robot rotating left"""
    robot = Robot((0, 0), Direction.NORTH)
    robot.rotate_left()
    assert robot.direction == Direction.WEST

def test_robot_rotate_right():
    """Test robot rotating right"""
    robot = Robot((0, 0), Direction.NORTH)
    robot.rotate_right()
    assert robot.direction == Direction.EAST