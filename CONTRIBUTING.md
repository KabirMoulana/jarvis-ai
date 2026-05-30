
# Contributing to Jarvis AI

Thanks for your interest! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/KabirMoulana/jarvis-ai.git
cd jarvis-ai
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Running Tests

```bash
pytest tests/ -v
```

## Adding a New Command

1. Create `commands/your_command.py`
2. Implement a `handle(command: str) -> str | None` function
3. Import and register it in `commands/router.py`
4. Add tests in `tests/test_your_command.py`

## Code Style

- Follow PEP 8
- Add type hints to all function signatures
- Write docstrings for all public functions and classes
