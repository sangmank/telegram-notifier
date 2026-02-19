"""Command-line interface for Telegram Notifier."""

import os
import sys
from typing import Optional

import click
from telegram.error import TelegramError

from .notifier import send_notification, send_file, send_photo


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
        click.echo(
            "Error: Bot token is required. Use --token or set TELEGRAM_BOT_TOKEN",
            err=True,
        )
        sys.exit(1)

    if not target_chat_id:
        click.echo(
            "Error: Chat ID is required. Use --chat-id or set TELEGRAM_CHAT_ID",
            err=True,
        )
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
    "--file",
    required=True,
    help="Path to the file to send",
    type=click.Path(exists=True),
)
@click.option(
    "--caption",
    help="Optional caption for the file",
    type=str,
)
def send_file_cmd(
    token: Optional[str], chat_id: Optional[str], file: str, caption: Optional[str]
) -> None:
    """Send a file to a Telegram chat."""
    # Get credentials from environment if not provided
    bot_token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    target_chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    # Validate required parameters
    if not bot_token:
        click.echo(
            "Error: Bot token is required. Use --token or set TELEGRAM_BOT_TOKEN",
            err=True,
        )
        sys.exit(1)

    if not target_chat_id:
        click.echo(
            "Error: Chat ID is required. Use --chat-id or set TELEGRAM_CHAT_ID",
            err=True,
        )
        sys.exit(1)

    try:
        success = send_file(bot_token, target_chat_id, file, caption)
        if success:
            click.echo(f"File '{file}' sent successfully!")
        else:
            click.echo("Failed to send file", err=True)
            sys.exit(1)
    except FileNotFoundError as e:
        click.echo(f"File error: {e}", err=True)
        sys.exit(1)
    except TelegramError as e:
        click.echo(f"Telegram API error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


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
    "--file",
    required=True,
    help="Path to the image file to send",
    type=click.Path(exists=True),
)
@click.option(
    "--caption",
    help="Optional caption for the photo",
    type=str,
)
def send_photo_cmd(
    token: Optional[str], chat_id: Optional[str], file: str, caption: Optional[str]
) -> None:
    """Send a photo to a Telegram chat."""
    # Get credentials from environment if not provided
    bot_token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    target_chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    # Validate required parameters
    if not bot_token:
        click.echo(
            "Error: Bot token is required. Use --token or set TELEGRAM_BOT_TOKEN",
            err=True,
        )
        sys.exit(1)

    if not target_chat_id:
        click.echo(
            "Error: Chat ID is required. Use --chat-id or set TELEGRAM_CHAT_ID",
            err=True,
        )
        sys.exit(1)

    try:
        success = send_photo(bot_token, target_chat_id, file, caption)
        if success:
            click.echo(f"Photo '{file}' sent successfully!")
        else:
            click.echo("Failed to send photo", err=True)
            sys.exit(1)
    except FileNotFoundError as e:
        click.echo(f"File error: {e}", err=True)
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
