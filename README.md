# Telegram Notifier

A simple CLI tool for sending Telegram notifications, designed for scripting and automation.

## Installation

```bash
# Install with Poetry
poetry install

# Or install from source
pip install .
```

## Usage

### Basic usage with command-line arguments:

```bash
telegram-notifier send --token "YOUR_BOT_TOKEN" --chat-id "YOUR_CHAT_ID" --message "Hello, world!"
```

### Using environment variables (recommended for scripts):

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
telegram-notifier send --message "Hello from script!"
```

## Setup

1. Create a Telegram bot by messaging [@BotFather](https://t.me/BotFather)
2. Get your bot token from BotFather
3. Find your chat ID (message your bot and check updates via API)

## Development

```bash
# Install dependencies
poetry install

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