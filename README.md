# Mini AI Assistant

A fully local, open-source text-based AI assistant for reminders, note-taking, calculations, and simple Q&A. Core features work offline using only Python's standard library. Optional integration with OpenAI/Gemini APIs for advanced responses.

## Features

- **Reminders**: Schedule reminders with time (e.g., `remind "Meeting" --time 14:00`).
- **Notes**: Add and list notes locally.
- **Calculations**: Safe evaluation of math expressions (e.g., `calc "2+3*4"`).
- **Q&A**: Basic offline AI responses; optional online queries.
- **Offline-First**: No internet required for core functionality.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Eternal0404/mini-ai-assistant.git
   cd mini-ai-assistant
   ```

2. (Optional) Install dependencies for online features:
   ```
   pip install -r requirements.txt
   ```

Python 3.10+ is required.

## Usage

Run commands using the CLI:

```bash
python -m assistant.cli <command> [options]
```

### Commands

- **Remind**: `python -m assistant.cli remind "Message" --time HH:MM`
  - Schedules a reminder that alerts at the specified time.

- **Note Add**: `python -m assistant.cli note add "Your note"`
  - Saves a note locally.

- **Note List**: `python -m assistant.cli note list`
  - Lists all saved notes.

- **Calc**: `python -m assistant.cli calc "expression"`
  - Evaluates a safe math expression (e.g., "2 + 3").

- **Ask**: `python -m assistant.cli ask "Question" [--online]`
  - Gets an answer. Use `--online` for API queries (requires keys).

- **Check Reminders**: `python -m assistant.cli check`
  - Manually checks for due reminders.

### Offline Mode

All commands work offline. Data is stored in `data/` as JSON files.

### Optional Online Features

Set environment variables for API access:
- `OPENAI_API_KEY`: For OpenAI GPT-4.
- `GEMINI_API_KEY`: For Google Gemini 1.5-flash.

If keys are set and `--online` is used, queries APIs; otherwise, falls back to offline.

## Examples

```bash
# Schedule a reminder
python -m assistant.cli remind "Doctor appointment" --time 15:30

# Add a note
python -m assistant.cli note add "Buy groceries"

# List notes
python -m assistant.cli note list

# Calculate
python -m assistant.cli calc "10 / 2 + 3"

# Ask offline
python -m assistant.cli ask "What is your name?"

# Ask online (if configured)
python -m assistant.cli ask "Explain quantum physics" --online
```

## Testing

Run tests:
```
python -m unittest discover tests/
```

## Contributing

Contributions welcome! Please submit issues/PRs on GitHub.

## License

MIT License. See LICENSE file.
