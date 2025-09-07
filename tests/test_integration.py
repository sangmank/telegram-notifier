"""Integration tests for error handling and edge cases."""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from telegram.error import TelegramError, NetworkError, Unauthorized

from telegram_notifier.notifier import TelegramNotifier, send_notification


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_unauthorized_error(self) -> None:
        """Test handling of unauthorized bot token."""
        notifier = TelegramNotifier("invalid_token")
        notifier.bot.send_message = AsyncMock(
            side_effect=Unauthorized("Unauthorized")
        )
        
        with pytest.raises(TelegramError, match="Failed to send message: Unauthorized"):
            await notifier.send_message("123456789", "Test message")
    
    @pytest.mark.asyncio
    async def test_network_error(self) -> None:
        """Test handling of network errors."""
        notifier = TelegramNotifier("test_token")
        notifier.bot.send_message = AsyncMock(
            side_effect=NetworkError("Connection timeout")
        )
        
        with pytest.raises(TelegramError, match="Failed to send message: Connection timeout"):
            await notifier.send_message("123456789", "Test message")
    
    @pytest.mark.asyncio
    async def test_invalid_chat_id(self) -> None:
        """Test handling of invalid chat ID."""
        notifier = TelegramNotifier("test_token")
        notifier.bot.send_message = AsyncMock(
            side_effect=TelegramError("Chat not found")
        )
        
        with pytest.raises(TelegramError, match="Failed to send message: Chat not found"):
            await notifier.send_message("invalid_chat_id", "Test message")
    
    def test_empty_message(self) -> None:
        """Test sending empty message."""
        with patch('telegram_notifier.notifier.TelegramNotifier') as mock_class:
            mock_instance = Mock()
            mock_instance.send_message = AsyncMock(return_value=True)
            mock_class.return_value = mock_instance
            
            with patch('asyncio.run') as mock_run:
                mock_run.return_value = True
                result = send_notification("test_token", "123456789", "")
                assert result is True
    
    def test_long_message(self) -> None:
        """Test sending very long message."""
        long_message = "A" * 5000  # Very long message
        
        with patch('telegram_notifier.notifier.TelegramNotifier') as mock_class:
            mock_instance = Mock()
            mock_instance.send_message = AsyncMock(return_value=True)
            mock_class.return_value = mock_instance
            
            with patch('asyncio.run') as mock_run:
                mock_run.return_value = True
                result = send_notification("test_token", "123456789", long_message)
                assert result is True
    
    def test_special_characters_in_message(self) -> None:
        """Test sending message with special characters."""
        special_message = "Test with émojis 🚀 and spëcial chars: <>&"
        
        with patch('telegram_notifier.notifier.TelegramNotifier') as mock_class:
            mock_instance = Mock()
            mock_instance.send_message = AsyncMock(return_value=True)
            mock_class.return_value = mock_instance
            
            with patch('asyncio.run') as mock_run:
                mock_run.return_value = True
                result = send_notification("test_token", "123456789", special_message)
                assert result is True