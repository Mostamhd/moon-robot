import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_get_status_initial():
    """Test getting the robot status with initial position"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 0}
    assert data["direction"] == "NORTH"


@pytest.mark.asyncio
async def test_get_status_after_movement():
    """Test getting the robot status after movement commands"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First send some movement commands
        await client.post("/api/v1/commands", json={"command": "F"})

        # Then check status
        response = await client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 1}
    assert data["direction"] == "NORTH"
