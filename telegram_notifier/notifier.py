"""Core Telegram notification functionality."""

import asyncio
import os
from pathlib import Path
from typing import Optional

from telegram import Bot
from telegram.error import TelegramError


class TelegramNotifier:
    """Handles sending messages via Telegram Bot API."""
    
    def __init__(self, bot_token: str) -> None:
        """Initialize the notifier with a bot token.
        
        Args:
            bot_token: The Telegram bot token from BotFather
        """
        self.bot = Bot(token=bot_token)
    
    async def send_message(self, chat_id: str, message: str) -> bool:
        """Send a message to a Telegram chat.
        
        Args:
            chat_id: The target chat ID
            message: The message text to send
            
        Returns:
            True if message was sent successfully, False otherwise
            
        Raises:
            TelegramError: If there's an issue with the Telegram API
        """
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
            return True
        except TelegramError as e:
            raise TelegramError(f"Failed to send message: {e}")
    
    async def send_document(self, chat_id: str, file_path: str, caption: Optional[str] = None) -> bool:
        """Send a document file to a Telegram chat.
        
        Args:
            chat_id: The target chat ID
            file_path: Path to the file to send
            caption: Optional caption for the file
            
        Returns:
            True if file was sent successfully, False otherwise
            
        Raises:
            TelegramError: If there's an issue with the Telegram API
            FileNotFoundError: If the file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                await self.bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=caption,
                    filename=Path(file_path).name
                )
            return True
        except TelegramError as e:
            raise TelegramError(f"Failed to send document: {e}")
    
    async def send_photo(self, chat_id: str, file_path: str, caption: Optional[str] = None) -> bool:
        """Send a photo to a Telegram chat.
        
        Args:
            chat_id: The target chat ID
            file_path: Path to the image file to send
            caption: Optional caption for the photo
            
        Returns:
            True if photo was sent successfully, False otherwise
            
        Raises:
            TelegramError: If there's an issue with the Telegram API
            FileNotFoundError: If the file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=file,
                    caption=caption
                )
            return True
        except TelegramError as e:
            raise TelegramError(f"Failed to send photo: {e}")


def send_notification(bot_token: str, chat_id: str, message: str) -> bool:
    """Send a Telegram notification (synchronous wrapper).
    
    Args:
        bot_token: The Telegram bot token
        chat_id: The target chat ID
        message: The message text to send
        
    Returns:
        True if message was sent successfully, False otherwise
        
    Raises:
        TelegramError: If there's an issue with the Telegram API
    """
    notifier = TelegramNotifier(bot_token)
    return asyncio.run(notifier.send_message(chat_id, message))


def send_file(bot_token: str, chat_id: str, file_path: str, caption: Optional[str] = None) -> bool:
    """Send a file to a Telegram chat (synchronous wrapper).
    
    Args:
        bot_token: The Telegram bot token
        chat_id: The target chat ID
        file_path: Path to the file to send
        caption: Optional caption for the file
        
    Returns:
        True if file was sent successfully, False otherwise
        
    Raises:
        TelegramError: If there's an issue with the Telegram API
        FileNotFoundError: If the file doesn't exist
    """
    notifier = TelegramNotifier(bot_token)
    return asyncio.run(notifier.send_document(chat_id, file_path, caption))


def send_photo(bot_token: str, chat_id: str, file_path: str, caption: Optional[str] = None) -> bool:
    """Send a photo to a Telegram chat (synchronous wrapper).
    
    Args:
        bot_token: The Telegram bot token
        chat_id: The target chat ID
        file_path: Path to the image file to send
        caption: Optional caption for the photo
        
    Returns:
        True if photo was sent successfully, False otherwise
        
    Raises:
        TelegramError: If there's an issue with the Telegram API
        FileNotFoundError: If the file doesn't exist
    """
    notifier = TelegramNotifier(bot_token)
    return asyncio.run(notifier.send_photo(chat_id, file_path, caption))