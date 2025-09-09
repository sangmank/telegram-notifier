# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple CLI tool for sending Telegram notifications, designed for scripting and automation. The tool sends text messages to designated Telegram chats using the Telegram Bot API.

## Architecture

The project follows a modular design:
- **CLI layer**: Command-line argument parsing and user interface
- **Core notification module**: Telegram API integration and message sending logic
- **Configuration**: Environment variable and credential management

## Development Setup

This project uses Poetry for dependency management:

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run the CLI tool
poetry run telegram-notifier

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=telegram_notifier --cov-report=html

# Format code
poetry run black .

# Type checking
poetry run mypy telegram_notifier

# Lint code
poetry run flake8 telegram_notifier
```

## Key Implementation Requirements

- **Credentials**: Tool requires `bot_token` (from BotFather) and `chat_id` (target chat identifier)
- **Environment variables**: Support `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to avoid CLI exposure
- **CLI interface**: 
  - `send --token <token> --chat-id <id> --message <message>` for text messages
  - `send-file-cmd --file <path> --caption <text>` for file uploads (up to 50MB)
  - `send-photo-cmd --file <path> --caption <text>` for image uploads (up to 10MB)
- **File handling**: Proper file validation and error handling for non-existent files
- **Error handling**: Graceful handling of network issues, API errors, and file errors
- **Type hints**: All functions should include proper type annotations
- **Separation of concerns**: Keep CLI parsing separate from Telegram API logic

## Dependencies

- Use `python-telegram-bot` library for Telegram API integration
- Use `click` library for CLI interface and command parsing
- Follow PEP 8 style guidelines
- Include comprehensive docstrings for public APIs