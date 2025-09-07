"""Core Telegram notification functionality."""

import asyncio
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