# Claude Summary Agent

A simple Claude-powered CLI agent that reads a text file and outputs a structured JSON summary.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
export ANTHROPIC_API_KEY="your-api-key"
```

## Usage

Print a JSON summary to stdout:

```bash
claude-summary notes.txt
```

Write the summary to a file:

```bash
claude-summary notes.txt --output summary.json
```

Choose a model:

```bash
claude-summary notes.txt --model claude-haiku-4-5
```

## Output Shape

```json
{
  "title": "string",
  "summary": "string",
  "key_points": ["string"],
  "entities": ["string"],
  "sentiment": "positive | neutral | negative | mixed",
  "action_items": ["string"]
}
```

The command writes only JSON to stdout so it can be piped into other tools.

## Development

Run the offline tests:

```bash
python3 -m unittest discover -s tests
```
