"""Command-line interface for Telegram Notifier."""

import os
import sys
from typing import Optional

import click
from telegram.error import TelegramError

from .notifier import send_notification


@click.group()
@click.version_option()
def cli() -> None:
    """Telegram Notifier - Send messages to Telegram chats from the command line."""
    pass


@cli.command()
@click.option(
    "--token",
    help="Telegram bot token (or set TELEGRAM_BOT_TOKEN env var)",
    type=str,
)
@click.option(
    "--chat-id",
    help="Target chat ID (or set TELEGRAM_CHAT_ID env var)",
    type=str,
)
@click.option(
    "--message",
    required=True,
    help="Message text to send",
    type=str,
)
def send(token: Optional[str], chat_id: Optional[str], message: str) -> None:
    """Send a message to a Telegram chat."""
    # Get credentials from environment if not provided
    bot_token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    target_chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
    
    # Validate required parameters
    if not bot_token:
        click.echo("Error: Bot token is required. Use --token or set TELEGRAM_BOT_TOKEN", err=True)
        sys.exit(1)
    
    if not target_chat_id:
        click.echo("Error: Chat ID is required. Use --chat-id or set TELEGRAM_CHAT_ID", err=True)
        sys.exit(1)
    
    try:
        success = send_notification(bot_token, target_chat_id, message)
        if success:
            click.echo("Message sent successfully!")
        else:
            click.echo("Failed to send message", err=True)
            sys.exit(1)
    except TelegramError as e:
        click.echo(f"Telegram API error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


def main() -> None:
    """Entry point for the CLI application."""
    cli()