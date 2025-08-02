from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.models.robot import Direction
from src.services.command_processor import CommandProcessor


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

    # Mock obstacles to return empty set using patch.object
    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        # Test simple forward command
        result = await processor.process_commands(
            command_string="F", start_position=(0, 0), start_direction=Direction.NORTH
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 1
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_process_rotation_commands():
    """Test processing rotation commands"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    # Mock obstacles to return empty set using patch.object
    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        # Test left rotation
        result = await processor.process_commands(
            command_string="L", start_position=(0, 0), start_direction=Direction.NORTH
        )
        assert result["direction"] == Direction.WEST

        # Test right rotation
        result = await processor.process_commands(
            command_string="R", start_position=(0, 0), start_direction=Direction.NORTH
        )
        assert result["direction"] == Direction.EAST


@pytest.mark.asyncio
async def test_process_obstacle_detection():
    """Test obstacle detection"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    # Mock obstacles to return set with obstacle at (0, 1)
    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = {(0, 1)}

        # Moving forward should detect obstacle
        result = await processor.process_commands(
            command_string="F", start_position=(0, 0), start_direction=Direction.NORTH
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 0  # Stopped at previous position
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is True


@pytest.mark.asyncio
async def test_process_complex_command_sequence():
    """Test processing a complex command sequence"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    # Mock obstacles to return empty set
    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        # Test complex sequence: FFRLB
        result = await processor.process_commands(
            command_string="FFRLB",
            start_position=(0, 0),
            start_direction=Direction.NORTH,
        )
        # Starting at (0,0) NORTH:
        # FF -> (0,2) NORTH
        # R -> (0,2) EAST
        # L -> (0,2) NORTH
        # B -> (0,1) NORTH
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 1
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_process_commands_with_multiple_obstacles():
    """Test processing commands with multiple obstacles"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    # Mock obstacles to return multiple obstacles
    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = {(0, 1), (1, 1), (1, 0)}

        # Test command that would hit an obstacle
        result = await processor.process_commands(
            command_string="FRF",  # Forward, Right, Forward
            start_position=(0, 0),
            start_direction=Direction.NORTH,
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 0
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is True


@pytest.mark.asyncio
async def test_process_empty_command_string():
    """Test processing an empty command string"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    # Mock obstacles to return empty set
    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        # Test empty command string
        result = await processor.process_commands(
            command_string="", start_position=(5, 3), start_direction=Direction.EAST
        )
        # Position and direction should remain unchanged
        assert result["position"]["x"] == 5
        assert result["position"]["y"] == 3
        assert result["direction"] == Direction.EAST
        assert result["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_process_commands_with_invalid_characters():
    """Test processing commands with invalid characters"""
    # Mock database session
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    # Mock obstacles to return empty set
    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        # Test command string with invalid characters
        result = await processor.process_commands(
            command_string="FXF",  # X is invalid
            start_position=(0, 0),
            start_direction=Direction.NORTH,
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 2
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_get_obstacles_from_database():
    """Test retrieving obstacles from database"""
    # Mock database session
    mock_db_session = AsyncMock()

    # Create mock obstacles
    mock_obstacles = [
        type("Obstacle", (), {"position_x": 1, "position_y": 4}),
        type("Obstacle", (), {"position_x": 3, "position_y": 5}),
        type("Obstacle", (), {"position_x": 7, "position_y": 4}),
    ]

    # Create mock result with proper scalars().all()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = mock_obstacles

    # Make execute return the mocked result
    mock_db_session.execute.return_value = mock_result

    processor = CommandProcessor(mock_db_session)
    obstacles = await processor.get_obstacles()

    # Check that we got the expected obstacles
    expected_obstacles = {(1, 4), (3, 5), (7, 4)}
    assert obstacles == expected_obstacles

    # Check that execute was called
    mock_db_session.execute.assert_awaited_once()
