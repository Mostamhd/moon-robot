import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_db_session():
    """Create a mock database session for testing."""
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session