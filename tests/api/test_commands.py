import pytest
from httpx import AsyncClient

from src.robot.main import app


@pytest.mark.asyncio
async def test_execute_commands_basic():
    """Test executing basic movement commands"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/commands", json={"command": "F"})
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 1}
    assert data["direction"] == "NORTH"
    assert data["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_execute_commands_rotation():
    """Test executing rotation commands"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Start with clean state
        await client.get("/api/v1/reset")

        response = await client.post("/api/v1/commands", json={"command": "R"})
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 0}
    assert data["direction"] == "EAST"
    assert data["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_obstacle_detection():
    """Test that the robot stops when encountering an obstacle"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Start with clean state at position (0,3) facing north
        await client.get("/api/v1/reset?position=(0,3)&direction=NORTH")

        # Move forward into obstacle at (0,4)
        response = await client.post("/api/v1/commands", json={"command": "F"})
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 3}  # Should not have moved
    assert data["obstacle_detected"] is True
    assert data["stopped_at"] == 0  # Stopped at first command
