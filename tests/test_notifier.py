"""Tests for the core notifier module."""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from telegram.error import TelegramError

from telegram_notifier.notifier import TelegramNotifier, send_notification, send_file, send_photo


class TestTelegramNotifier:
    """Tests for TelegramNotifier class."""
    
    def test_init(self) -> None:
        """Test TelegramNotifier initialization."""
        token = "test_token"
        notifier = TelegramNotifier(token)
        assert notifier.bot.token == token
    
    @pytest.mark.asyncio
    @patch('telegram.Bot.send_message', new_callable=AsyncMock)
    async def test_send_message_success(self, mock_send_message: AsyncMock) -> None:
        """Test successful message sending."""
        token = "test_token"
        chat_id = "123456789"
        message = "Test message"
        
        notifier = TelegramNotifier(token)
        
        result = await notifier.send_message(chat_id, message)
        
        assert result is True
        mock_send_message.assert_called_once_with(
            chat_id=chat_id, text=message
        )
    
    @pytest.mark.asyncio
    @patch('telegram.Bot.send_message', new_callable=AsyncMock)
    async def test_send_message_failure(self, mock_send_message: AsyncMock) -> None:
        """Test message sending failure."""
        token = "test_token"
        chat_id = "123456789"
        message = "Test message"
        
        notifier = TelegramNotifier(token)
        
        # Mock the bot's send_message method to raise an exception
        error_msg = "Invalid chat_id"
        mock_send_message.side_effect = TelegramError(error_msg)
        
        with pytest.raises(TelegramError, match=f"Failed to send message: {error_msg}"):
            await notifier.send_message(chat_id, message)
    
    @pytest.mark.asyncio
    @patch('telegram.Bot.send_document', new_callable=AsyncMock)
    async def test_send_document_success(self, mock_send_document: AsyncMock, tmp_path) -> None:
        """Test successful document sending."""
        token = "test_token"
        chat_id = "123456789"
        
        # Create a temporary test file
        test_file = tmp_path / "test_document.pdf"
        test_file.write_text("Test document content")
        
        notifier = TelegramNotifier(token)
        
        result = await notifier.send_document(chat_id, str(test_file), "Test caption")
        
        assert result is True
        mock_send_document.assert_called_once()
        args, kwargs = mock_send_document.call_args
        assert kwargs['chat_id'] == chat_id
        assert kwargs['caption'] == "Test caption"
        assert kwargs['filename'] == "test_document.pdf"
    
    @pytest.mark.asyncio
    async def test_send_document_file_not_found(self) -> None:
        """Test document sending with non-existent file."""
        token = "test_token"
        chat_id = "123456789"
        file_path = "/nonexistent/file.pdf"
        
        notifier = TelegramNotifier(token)
        
        with pytest.raises(FileNotFoundError, match=f"File not found: {file_path}"):
            await notifier.send_document(chat_id, file_path)
    
    @pytest.mark.asyncio
    @patch('telegram.Bot.send_document', new_callable=AsyncMock)
    async def test_send_document_telegram_error(self, mock_send_document: AsyncMock, tmp_path) -> None:
        """Test document sending with Telegram API error."""
        token = "test_token"
        chat_id = "123456789"
        
        test_file = tmp_path / "test_document.pdf"
        test_file.write_text("Test document content")
        
        notifier = TelegramNotifier(token)
        error_msg = "File too large"
        mock_send_document.side_effect = TelegramError(error_msg)
        
        with pytest.raises(TelegramError, match=f"Failed to send document: {error_msg}"):
            await notifier.send_document(chat_id, str(test_file))
    
    @pytest.mark.asyncio
    @patch('telegram.Bot.send_photo', new_callable=AsyncMock)
    async def test_send_photo_success(self, mock_send_photo: AsyncMock, tmp_path) -> None:
        """Test successful photo sending."""
        token = "test_token"
        chat_id = "123456789"
        
        # Create a temporary test image file
        test_file = tmp_path / "test_image.jpg"
        test_file.write_bytes(b"fake image data")
        
        notifier = TelegramNotifier(token)
        
        result = await notifier.send_photo(chat_id, str(test_file), "Test photo")
        
        assert result is True
        mock_send_photo.assert_called_once()
        args, kwargs = mock_send_photo.call_args
        assert kwargs['chat_id'] == chat_id
        assert kwargs['caption'] == "Test photo"
    
    @pytest.mark.asyncio
    async def test_send_photo_file_not_found(self) -> None:
        """Test photo sending with non-existent file."""
        token = "test_token"
        chat_id = "123456789"
        file_path = "/nonexistent/image.jpg"
        
        notifier = TelegramNotifier(token)
        
        with pytest.raises(FileNotFoundError, match=f"File not found: {file_path}"):
            await notifier.send_photo(chat_id, file_path)
    
    @pytest.mark.asyncio
    @patch('telegram.Bot.send_photo', new_callable=AsyncMock)
    async def test_send_photo_telegram_error(self, mock_send_photo: AsyncMock, tmp_path) -> None:
        """Test photo sending with Telegram API error."""
        token = "test_token"
        chat_id = "123456789"
        
        test_file = tmp_path / "test_image.jpg"
        test_file.write_bytes(b"fake image data")
        
        notifier = TelegramNotifier(token)
        error_msg = "Invalid image format"
        mock_send_photo.side_effect = TelegramError(error_msg)
        
        with pytest.raises(TelegramError, match=f"Failed to send photo: {error_msg}"):
            await notifier.send_photo(chat_id, str(test_file))


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


class TestSendFile:
    """Tests for send_file function."""
    
    @patch('telegram_notifier.notifier.TelegramNotifier')
    def test_send_file_success(self, mock_notifier_class: Mock, tmp_path) -> None:
        """Test successful file sending."""
        token = "test_token"
        chat_id = "123456789"
        
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")
        
        mock_notifier = Mock()
        mock_notifier.send_document = AsyncMock(return_value=True)
        mock_notifier_class.return_value = mock_notifier
        
        with patch('asyncio.run') as mock_run:
            mock_run.return_value = True
            result = send_file(token, chat_id, str(test_file), "Test caption")
        
        assert result is True
        mock_notifier_class.assert_called_once_with(token)
        mock_run.assert_called_once()
    
    @patch('telegram_notifier.notifier.TelegramNotifier')
    def test_send_file_failure(self, mock_notifier_class: Mock) -> None:
        """Test file sending failure."""
        token = "test_token"
        chat_id = "123456789"
        file_path = "/nonexistent/file.pdf"
        
        mock_notifier = Mock()
        mock_notifier.send_document = AsyncMock(side_effect=FileNotFoundError("File not found"))
        mock_notifier_class.return_value = mock_notifier
        
        with patch('asyncio.run') as mock_run:
            mock_run.side_effect = FileNotFoundError("File not found")
            with pytest.raises(FileNotFoundError):
                send_file(token, chat_id, file_path)


class TestSendPhoto:
    """Tests for send_photo function."""
    
    @patch('telegram_notifier.notifier.TelegramNotifier')
    def test_send_photo_success(self, mock_notifier_class: Mock, tmp_path) -> None:
        """Test successful photo sending."""
        token = "test_token"
        chat_id = "123456789"
        
        test_file = tmp_path / "test.jpg"
        test_file.write_bytes(b"fake image data")
        
        mock_notifier = Mock()
        mock_notifier.send_photo = AsyncMock(return_value=True)
        mock_notifier_class.return_value = mock_notifier
        
        with patch('asyncio.run') as mock_run:
            mock_run.return_value = True
            result = send_photo(token, chat_id, str(test_file), "Test photo")
        
        assert result is True
        mock_notifier_class.assert_called_once_with(token)
        mock_run.assert_called_once()
    
    @patch('telegram_notifier.notifier.TelegramNotifier')
    def test_send_photo_failure(self, mock_notifier_class: Mock) -> None:
        """Test photo sending failure."""
        token = "test_token"
        chat_id = "123456789"
        file_path = "/nonexistent/image.jpg"
        
        mock_notifier = Mock()
        mock_notifier.send_photo = AsyncMock(side_effect=FileNotFoundError("File not found"))
        mock_notifier_class.return_value = mock_notifier
        
        with patch('asyncio.run') as mock_run:
            mock_run.side_effect = FileNotFoundError("File not found")
            with pytest.raises(FileNotFoundError):
                send_photo(token, chat_id, file_path)