"""Test configuration and fixtures."""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_bot() -> Mock:
    """Create a mock Telegram bot."""
    bot = Mock()
    bot.token = "test_token"
    return bot


@pytest.fixture
def sample_chat_id() -> str:
    """Sample chat ID for testing."""
    return "123456789"


@pytest.fixture
def sample_message() -> str:
    """Sample message text for testing."""
    return "Test message for unit testing"


@pytest.fixture
def sample_token() -> str:
    """Sample bot token for testing."""
    return "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"