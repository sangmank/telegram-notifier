"""Tests for the CLI interface."""

import os
from unittest.mock import Mock, patch
import pytest
from click.testing import CliRunner
from telegram.error import TelegramError

from telegram_notifier.cli import cli


class TestCLI:
    """Tests for the CLI interface."""
    
    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    @patch('telegram_notifier.cli.send_notification')
    def test_send_command_with_args_success(self, mock_send: Mock) -> None:
        """Test send command with command-line arguments."""
        mock_send.return_value = True
        
        result = self.runner.invoke(cli, [
            'send',
            '--token', 'test_token',
            '--chat-id', '123456789',
            '--message', 'Test message'
        ])
        
        assert result.exit_code == 0
        assert 'Message sent successfully!' in result.output
        mock_send.assert_called_once_with('test_token', '123456789', 'Test message')
    
    @patch('telegram_notifier.cli.send_notification')
    @patch.dict(os.environ, {
        'TELEGRAM_BOT_TOKEN': 'env_token',
        'TELEGRAM_CHAT_ID': '987654321'
    })
    def test_send_command_with_env_vars(self, mock_send: Mock) -> None:
        """Test send command using environment variables."""
        mock_send.return_value = True
        
        result = self.runner.invoke(cli, [
            'send',
            '--message', 'Test message from env'
        ])
        
        assert result.exit_code == 0
        assert 'Message sent successfully!' in result.output
        mock_send.assert_called_once_with('env_token', '987654321', 'Test message from env')
    
    def test_send_command_missing_token(self) -> None:
        """Test send command with missing token."""
        result = self.runner.invoke(cli, [
            'send',
            '--chat-id', '123456789',
            '--message', 'Test message'
        ])
        
        assert result.exit_code == 1
        assert 'Bot token is required' in result.output
    
    def test_send_command_missing_chat_id(self) -> None:
        """Test send command with missing chat ID."""
        result = self.runner.invoke(cli, [
            'send',
            '--token', 'test_token',
            '--message', 'Test message'
        ])
        
        assert result.exit_code == 1
        assert 'Chat ID is required' in result.output
    
    def test_send_command_missing_message(self) -> None:
        """Test send command with missing message."""
        result = self.runner.invoke(cli, [
            'send',
            '--token', 'test_token',
            '--chat-id', '123456789'
        ])
        
        assert result.exit_code == 2  # Click error for missing required option
    
    @patch('telegram_notifier.cli.send_notification')
    def test_send_command_telegram_error(self, mock_send: Mock) -> None:
        """Test send command with Telegram API error."""
        mock_send.side_effect = TelegramError("Invalid token")
        
        result = self.runner.invoke(cli, [
            'send',
            '--token', 'invalid_token',
            '--chat-id', '123456789',
            '--message', 'Test message'
        ])
        
        assert result.exit_code == 1
        assert 'Telegram API error: Invalid token' in result.output
    
    @patch('telegram_notifier.cli.send_notification')
    def test_send_command_unexpected_error(self, mock_send: Mock) -> None:
        """Test send command with unexpected error."""
        mock_send.side_effect = Exception("Unexpected error")
        
        result = self.runner.invoke(cli, [
            'send',
            '--token', 'test_token',
            '--chat-id', '123456789',
            '--message', 'Test message'
        ])
        
        assert result.exit_code == 1
        assert 'Unexpected error: Unexpected error' in result.output
    
    @patch('telegram_notifier.cli.send_notification')
    def test_send_command_false_return(self, mock_send: Mock) -> None:
        """Test send command when send_notification returns False."""
        mock_send.return_value = False
        
        result = self.runner.invoke(cli, [
            'send',
            '--token', 'test_token',
            '--chat-id', '123456789',
            '--message', 'Test message'
        ])
        
        assert result.exit_code == 1
        assert 'Failed to send message' in result.output
    
    def test_version_option(self) -> None:
        """Test --version option."""
        result = self.runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0
        # Version should be displayed (from package metadata)
    
    def test_help_output(self) -> None:
        """Test help output."""
        result = self.runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'Telegram Notifier' in result.output
        assert 'Send messages to Telegram chats' in result.output