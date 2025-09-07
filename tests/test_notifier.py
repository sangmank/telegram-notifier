"""Tests for the core notifier module."""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from telegram.error import TelegramError

from telegram_notifier.notifier import TelegramNotifier, send_notification


class TestTelegramNotifier:
    """Tests for TelegramNotifier class."""
    
    def test_init(self) -> None:
        """Test TelegramNotifier initialization."""
        token = "test_token"
        notifier = TelegramNotifier(token)
        assert notifier.bot.token == token
    
    @pytest.mark.asyncio
    async def test_send_message_success(self) -> None:
        """Test successful message sending."""
        token = "test_token"
        chat_id = "123456789"
        message = "Test message"
        
        notifier = TelegramNotifier(token)
        
        # Mock the bot's send_message method
        notifier.bot.send_message = AsyncMock()
        
        result = await notifier.send_message(chat_id, message)
        
        assert result is True
        notifier.bot.send_message.assert_called_once_with(
            chat_id=chat_id, text=message
        )
    
    @pytest.mark.asyncio
    async def test_send_message_failure(self) -> None:
        """Test message sending failure."""
        token = "test_token"
        chat_id = "123456789"
        message = "Test message"
        
        notifier = TelegramNotifier(token)
        
        # Mock the bot's send_message method to raise an exception
        error_msg = "Invalid chat_id"
        notifier.bot.send_message = AsyncMock(side_effect=TelegramError(error_msg))
        
        with pytest.raises(TelegramError, match=f"Failed to send message: {error_msg}"):
            await notifier.send_message(chat_id, message)


class TestSendNotification:
    """Tests for send_notification function."""
    
    @patch('telegram_notifier.notifier.TelegramNotifier')
    def test_send_notification_success(self, mock_notifier_class: Mock) -> None:
        """Test successful notification sending."""
        token = "test_token"
        chat_id = "123456789"
        message = "Test message"
        
        # Mock the notifier instance and its send_message method
        mock_notifier = Mock()
        mock_notifier.send_message = AsyncMock(return_value=True)
        mock_notifier_class.return_value = mock_notifier
        
        with patch('asyncio.run') as mock_run:
            mock_run.return_value = True
            result = send_notification(token, chat_id, message)
        
        assert result is True
        mock_notifier_class.assert_called_once_with(token)
        mock_run.assert_called_once()
    
    @patch('telegram_notifier.notifier.TelegramNotifier')
    def test_send_notification_failure(self, mock_notifier_class: Mock) -> None:
        """Test notification sending failure."""
        token = "test_token"
        chat_id = "123456789"
        message = "Test message"
        
        # Mock the notifier instance to raise an exception
        mock_notifier = Mock()
        mock_notifier.send_message = AsyncMock(side_effect=TelegramError("API Error"))
        mock_notifier_class.return_value = mock_notifier
        
        with patch('asyncio.run') as mock_run:
            mock_run.side_effect = TelegramError("API Error")
            with pytest.raises(TelegramError):
                send_notification(token, chat_id, message)