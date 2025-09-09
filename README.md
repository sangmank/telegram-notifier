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

### Send text messages:

```bash
# With command-line arguments
telegram-notifier send --token "YOUR_BOT_TOKEN" --chat-id "YOUR_CHAT_ID" --message "Hello, world!"

# Using environment variables (recommended for scripts)
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
telegram-notifier send --message "Hello from script!"
```

### Send files:

```bash
# Send any file (up to 50MB)
telegram-notifier send-file-cmd --file "/path/to/document.pdf" --caption "Monthly report"

# Send with environment variables
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
telegram-notifier send-file-cmd --file "report.xlsx" --caption "Q3 Sales Data"
```

### Send photos:

```bash
# Send image files (up to 10MB)
telegram-notifier send-photo-cmd --file "/path/to/image.jpg" --caption "Screenshot"

# Send without caption
telegram-notifier send-photo-cmd --file "graph.png"
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