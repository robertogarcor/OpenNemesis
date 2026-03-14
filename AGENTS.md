# OpenNemesis - Agent Guidelines

## Project Overview

OpenNemesis is a modular AI Telegram bot powered by Google Gemini. It processes text and voice messages, uses tools (weather, time, web search, command execution), and supports skills for extended functionality.

### Core Tools

- **get_weather(city)**: Get current weather for a city
- **get_time()**: Get current time and date
- **search_web(query)**: Search the web for information
- **execute_command(command)**: Execute any shell command

### GOG CLI

The project uses GOG CLI (`/opt/gogcli`) for Google Workspace operations (Gmail, Calendar, Drive, Contacts). Commands are executed via the `execute_command` tool.

---

## Running the Project

### Requirements

- Python 3.10+
- Telegram Bot Token
- Google Gemini API Key
- GOG CLI (Google Workspace CLI) for Gmail/Calendar/Drive operations
- Default model: `gemini-3.1-flash-lite-preview`

### Installation

```bash
# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# The virtual environment .venv is already initialized in this project
```

### Git

The project uses Git for version control:
- Branch: `main`
- Commits follow conventional commits format

### Environment Setup

```bash
# Copy template and configure
cp .env.local .env
# Edit .env with your credentials
```

### Running the Bot

```bash
# Validate connections only
python main.py

# Start the bot
python main.py run
```

### Running a Single Test

No formal test suite exists yet. To run tests manually:

```bash
# Run pytest if tests are added
pytest

# Run a specific test file
pytest tests/test_file.py

# Run a specific test function
pytest tests/test_file.py::test_function_name
```

### Linting and Formatting

No formal linting/formatting is configured. Follow these guidelines:

- Use `black` for formatting (if added later): `black .`
- Use `ruff` for linting (if added later): `ruff check .`
- Use `mypy` for type checking (if added later): `mypy .`

---

## Code Style Guidelines

### General Principles

- **Language**: Python 3.x with type hints
- **Encoding**: UTF-8
- **Line length**: 100 characters max (soft guideline)
- **Indentation**: 4 spaces

### Imports

Standard order (separate with blank lines between groups):

1. Standard library (`os`, `sys`, `logging`, `asyncio`, etc.)
2. Third-party packages (`telegram`, `google.genai`, `requests`, etc.)
3. Local application modules (`from ... import`)

```python
# Correct
import os
import sys
import logging
import asyncio
from datetime import datetime
from pathlib import Path

import requests
from telegram import Update
from telegram.ext import Application

from telegram_bot import TelegramBot
from gemini_client import GeminiClient
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Files | snake_case | `telegram_bot.py`, `gemini_client.py` |
| Classes | PascalCase | `TelegramBot`, `GeminiClient` |
| Functions | snake_case | `get_weather()`, `handle_text()` |
| Variables | snake_case | `user_message`, `api_key` |
| Constants | UPPER_SNAKE_CASE | `MAX_ITERATIONS`, `DEFAULT_MODEL` |
| Private functions | _snake_case | `_init_client()` |

### Type Hints

Use type hints for all function signatures:

```python
# Good
def get_weather(city: str) -> str:
    ...

def chat(self, message: str) -> str:
    ...

async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ...

# Good - using Union for optional types
from typing import Union, Optional

def process_message(message: Optional[str] = None) -> Union[str, None]:
    ...
```

### Docstrings

Use Google-style docstrings for public functions:

```python
def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: Name of the city to get weather for.

    Returns:
        Weather information as a string.
    """
```

### Error Handling

- Use try/except blocks with specific exception types
- Log errors with appropriate level
- Return user-friendly error messages (with ⚠️ prefix for bot responses)

```python
# Good
try:
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        logging.error(f"Failed request: {response.status_code}")
        return "Could not retrieve data."
except requests.RequestException as e:
    logging.error(f"Request error: {e}")
    return "An error occurred while retrieving data."
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    return "⚠️ An unexpected error occurred."
```

### Logging

Use the project logger pattern:

```python
import logging

logger = logging.getLogger("OpenNemesis.SubModule")

logger.info("Operation successful")
logger.warning("Something might be wrong")
logger.error("Operation failed")
```

### Async/Await

- Use `async def` for asynchronous functions
- Use `await` for async calls
- Apply `nest_asyncio` for Jupyter/interactive environments

```python
import asyncio
import nest_asyncio

nest_asyncio.apply()

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

result = asyncio.run(fetch_data())
```

### Configuration

- Store secrets in `.env.local` (never commit)
- Use `python-dotenv` for loading
- Validate required environment variables at startup

```python
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".env.local")
if env_path.exists():
    load_dotenv(env_path)
```

---

## Project Structure

```
OpenNemesis/
├── main.py              # Entry point, validation logic
├── telegram_bot.py      # Telegram bot handlers
├── gemini_client.py     # Gemini AI client with tools
├── prompt.py            # System prompts
├── tts_client.py        # Text-to-speech client
├── requirements.txt     # Dependencies
├── .env.local          # Environment variables (secrets)
├── .agent/             # Developer documentation (for agents)
│   ├── CHANGELOG.md   # Project changelog (update on commits)
│   └── MEMORIA.md     # Project milestones and roadmap
├── skills/             # Skill loaders and definitions
│   ├── loader.py
│   └── gog/
├── tools/              # Tool implementations
│   ├── tools.py        # Core tools
│   └── gog_tools.py    # GOG CLI tools
└── credentials/        # API credentials (never commit)
```

---

## Key Conventions

1. **Bot responses**: Start error messages with `⚠️` for user-friendly output
2. **Shell commands**: Always use full paths and pass environment variables
3. **API keys**: Load from environment, never hardcode
4. **Timezone**: Europe/Madrid (UTC+1/UTC+2)
5. **Date format**: `YYYY-MM-DDTHH:MM:SS+01:00` for calendar events

---

## Git Conventions

### Commit Format

Follow Conventional Commits with emojis:

```
:emoji: tipo(ámbito): descripción
```

| Type | Emoji | Description |
|------|-------|-------------|
| feat | ✨ | New feature |
| fix | 🐛 | Bug fix |
| docs | 📝 | Documentation |
| style | 🎨 | Formatting (no code change) |
| refactor | ♻️ | Code refactoring |
| test | ✅ | Add/update tests |
| chore | 🔧 | Build tools, utilities |

**Rules:**
- Max 50 characters in description
- Use imperative mood ("add button" not "added button")
- Emoji first

**Example:**
`✨ feat(ui): add save button`

### Changelog

Update CHANGELOG.md after commits:

```bash
powershell -ExecutionPolicy Bypass -File .agent/skills/changelog-generator/scripts/update_changelog.ps1
```

The changelog extracts commit messages from Git history.

### Project Documentation

After commits, consider updating:
- **CHANGELOG.md** - Recent changes (auto-generated or manual)
- **MEMORIA.md** - Milestones and roadmap updates
- **README.md** - User-facing documentation

---

## Creating New Skills

Skills are stored in `.agent/skills/<skill_name>/`:

```
.agent/skills/
├── SKILL.md           # Required: name + description in YAML frontmatter
├── scripts/           # Optional: automation scripts
├── examples/          # Optional: usage examples
└── resources/         # Optional: templates, assets
```

### SKILL.md Frontmatter
```yaml
---
name: skill-name
description: Brief description in third person
---
```

Use `skills/skill-creator/SKILL.md` as reference.

### Adding a New Tool

1. Implement function in `tools/tools.py`
2. Add function declaration to `TOOLS_SCHEMA` in `gemini_client.py`
3. Register in `_init_tools()` method

### Adding a New Skill

1. Create directory in `skills/<skill_name>/`
2. Add `SKILL.md` with skill definition (auto-loaded by `skills/loader.py`)
3. The skill context is automatically included in Gemini's system prompt

### Skills System

- Skills are defined in `skills/<name>/SKILL.md` files
- `skills/loader.py` automatically loads all SKILL.md files and combines them into the system prompt
- Currently available: `gog` skill for Google Workspace (Gmail, Calendar, Drive, Contacts)
- New skills = just add a folder with SKILL.md, no code changes needed

### Adding Dependencies

Add to `requirements.txt` and document purpose with comment:

```python
# OpenNemesis Dependencies

# Core
python-dotenv>=0
nest-asyncio>=1.5.0

# Telegram Bot
python-telegram-bot>=20.0
```
