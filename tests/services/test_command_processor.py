import pytest
from unittest.mock import AsyncMock
from src.services.command_processor import CommandProcessor
from src.models.robot import Direction

@pytest.mark.asyncio
async def test_command_processor_initialization():
    """Test command processor initialization"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)
    assert processor.db_session == mock_db_session

@pytest.mark.asyncio
async def test_process_valid_commands():
    """Test processing valid command strings"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)
    
    # Mock obstacles to return empty set
    processor.get_obstacles = AsyncMock(return_value=set())
    
    # Test simple forward command
    result = await processor.process_commands(
        command_string="F",
        start_position=(0, 0),
        start_direction=Direction.NORTH
    )
    assert result["position"]["x"] == 0
    assert result["position"]["y"] == 1
    assert result["direction"] == Direction.NORTH
    assert result["obstacle_detected"] == False

@pytest.mark.asyncio
async def test_process_rotation_commands():
    """Test processing rotation commands"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)
    
    # Mock obstacles to return empty set
    processor.get_obstacles = AsyncMock(return_value=set())
    
    # Test left rotation
    result = await processor.process_commands(
        command_string="L",
        start_position=(0, 0),
        start_direction=Direction.NORTH
    )
    assert result["direction"] == Direction.WEST
    
    # Test right rotation
    result = await processor.process_commands(
        command_string="R",
        start_position=(0, 0),
        start_direction=Direction.NORTH
    )
    assert result["direction"] == Direction.EAST

@pytest.mark.asyncio
async def test_process_obstacle_detection():
    """Test obstacle detection"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)
    
    # Mock obstacles to return set with obstacle at (0, 1)
    processor.get_obstacles = AsyncMock(return_value={(0, 1)})
    
    # Moving forward should detect obstacle
    result = await processor.process_commands(
        command_string="F",
        start_position=(0, 0),
        start_direction=Direction.NORTH
    )
    assert result["position"]["x"] == 0
    assert result["position"]["y"] == 0  # Stopped at previous position
    assert result["direction"] == Direction.NORTH
    assert result["obstacle_detected"] == True