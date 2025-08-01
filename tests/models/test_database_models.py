import pytest
from src.models.database import RobotState, CommandHistory, Obstacle

def test_database_models():
    """Test database model creation"""
    # Test RobotState model
    robot_state = RobotState(position_x=1, position_y=2, direction="NORTH")
    assert robot_state.position_x == 1
    assert robot_state.position_y == 2
    assert robot_state.direction == "NORTH"
    
    # Test CommandHistory model
    command = CommandHistory(
        command="F",
        position_x=0,
        position_y=0,
        direction="NORTH",
        obstacle_detected=False
    )
    assert command.command == "F"
    assert command.position_x == 0
    assert command.position_y == 0
    assert command.direction == "NORTH"
    assert command.obstacle_detected == False
    
    # Test Obstacle model
    obstacle = Obstacle(position_x=3, position_y=5)
    assert obstacle.position_x == 3
    assert obstacle.position_y == 5
    