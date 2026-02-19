"""Tests for file sending CLI commands."""

import os
from unittest.mock import Mock, patch
import pytest
from click.testing import CliRunner
from telegram.error import TelegramError

from telegram_notifier.cli import cli


class TestSendFileCommand:
    """Tests for the send-file-cmd CLI command."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("telegram_notifier.cli.send_file")
    def test_send_file_success(self, mock_send: Mock, tmp_path) -> None:
        """Test send-file-cmd command success."""
        mock_send.return_value = True

        test_file = tmp_path / "test_document.pdf"
        test_file.write_text("test content")

        result = self.runner.invoke(
            cli,
            [
                "send-file-cmd",
                "--token",
                "test_token",
                "--chat-id",
                "123456789",
                "--file",
                str(test_file),
                "--caption",
                "Test file",
            ],
        )

        assert result.exit_code == 0
        assert f"File '{test_file}' sent successfully!" in result.output
        mock_send.assert_called_once_with(
            "test_token", "123456789", str(test_file), "Test file"
        )

    @patch("telegram_notifier.cli.send_file")
    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "env_token", "TELEGRAM_CHAT_ID": "987654321"}
    )
    def test_send_file_with_env_vars(self, mock_send: Mock, tmp_path) -> None:
        """Test send-file-cmd command using environment variables."""
        mock_send.return_value = True

        test_file = tmp_path / "test_document.pdf"
        test_file.write_text("test content")

        result = self.runner.invoke(cli, ["send-file-cmd", "--file", str(test_file)])

        assert result.exit_code == 0
        assert f"File '{test_file}' sent successfully!" in result.output
        mock_send.assert_called_once_with(
            "env_token", "987654321", str(test_file), None
        )

    def test_send_file_missing_token(self, tmp_path) -> None:
        """Test send-file-cmd command with missing token."""
        test_file = tmp_path / "test_document.pdf"
        test_file.write_text("test content")

        result = self.runner.invoke(
            cli, ["send-file-cmd", "--chat-id", "123456789", "--file", str(test_file)]
        )

        assert result.exit_code == 1
        assert "Bot token is required" in result.output

    def test_send_file_missing_chat_id(self, tmp_path) -> None:
        """Test send-file-cmd command with missing chat ID."""
        test_file = tmp_path / "test_document.pdf"
        test_file.write_text("test content")

        result = self.runner.invoke(
            cli, ["send-file-cmd", "--token", "test_token", "--file", str(test_file)]
        )

        assert result.exit_code == 1
        assert "Chat ID is required" in result.output

    def test_send_file_nonexistent_file(self) -> None:
        """Test send-file-cmd command with non-existent file."""
        result = self.runner.invoke(
            cli,
            [
                "send-file-cmd",
                "--token",
                "test_token",
                "--chat-id",
                "123456789",
                "--file",
                "/nonexistent/file.pdf",
            ],
        )

        assert result.exit_code == 2  # Click error for non-existent file

    @patch("telegram_notifier.cli.send_file")
    def test_send_file_telegram_error(self, mock_send: Mock, tmp_path) -> None:
        """Test send-file-cmd command with Telegram API error."""
        mock_send.side_effect = TelegramError("File too large")

        test_file = tmp_path / "test_document.pdf"
        test_file.write_text("test content")

        result = self.runner.invoke(
            cli,
            [
                "send-file-cmd",
                "--token",
                "test_token",
                "--chat-id",
                "123456789",
                "--file",
                str(test_file),
            ],
        )

        assert result.exit_code == 1
        assert "Telegram API error: File too large" in result.output


class TestSendPhotoCommand:
    """Tests for the send-photo-cmd CLI command."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("telegram_notifier.cli.send_photo")
    def test_send_photo_success(self, mock_send: Mock, tmp_path) -> None:
        """Test send-photo-cmd command success."""
        mock_send.return_value = True

        test_file = tmp_path / "test_image.jpg"
        test_file.write_bytes(b"fake image data")

        result = self.runner.invoke(
            cli,
            [
                "send-photo-cmd",
                "--token",
                "test_token",
                "--chat-id",
                "123456789",
                "--file",
                str(test_file),
                "--caption",
                "Test photo",
            ],
        )

        assert result.exit_code == 0
        assert f"Photo '{test_file}' sent successfully!" in result.output
        mock_send.assert_called_once_with(
            "test_token", "123456789", str(test_file), "Test photo"
        )

    @patch("telegram_notifier.cli.send_photo")
    @patch.dict(
        os.environ, {"TELEGRAM_BOT_TOKEN": "env_token", "TELEGRAM_CHAT_ID": "987654321"}
    )
    def test_send_photo_with_env_vars(self, mock_send: Mock, tmp_path) -> None:
        """Test send-photo-cmd command using environment variables."""
        mock_send.return_value = True

        test_file = tmp_path / "test_image.jpg"
        test_file.write_bytes(b"fake image data")

        result = self.runner.invoke(cli, ["send-photo-cmd", "--file", str(test_file)])

        assert result.exit_code == 0
        assert f"Photo '{test_file}' sent successfully!" in result.output
        mock_send.assert_called_once_with(
            "env_token", "987654321", str(test_file), None
        )

    def test_send_photo_missing_token(self, tmp_path) -> None:
        """Test send-photo-cmd command with missing token."""
        test_file = tmp_path / "test_image.jpg"
        test_file.write_bytes(b"fake image data")

        result = self.runner.invoke(
            cli, ["send-photo-cmd", "--chat-id", "123456789", "--file", str(test_file)]
        )

        assert result.exit_code == 1
        assert "Bot token is required" in result.output

    @patch("telegram_notifier.cli.send_photo")
    def test_send_photo_telegram_error(self, mock_send: Mock, tmp_path) -> None:
        """Test send-photo-cmd command with Telegram API error."""
        mock_send.side_effect = TelegramError("Invalid image format")

        test_file = tmp_path / "test_image.jpg"
        test_file.write_bytes(b"fake image data")

        result = self.runner.invoke(
            cli,
            [
                "send-photo-cmd",
                "--token",
                "test_token",
                "--chat-id",
                "123456789",
                "--file",
                str(test_file),
            ],
        )

        assert result.exit_code == 1
        assert "Telegram API error: Invalid image format" in result.output
