import argparse
import json
import os
import sys
from pathlib import Path


DEFAULT_MODEL = "claude-haiku-4-5"


PROMPT = """Summarize this text file as JSON.

Return only JSON in this shape:
{
  "title": "short title",
  "summary": "short summary",
  "key_points": ["point one", "point two"]
}
"""


def read_file(file_path):
    path = Path(file_path)

    if not path.exists():
        raise ValueError(f"File not found: {file_path}")

    text = path.read_text(encoding="utf-8")

    if text.strip() == "":
        raise ValueError("File is empty.")

    return text


def get_response_text(response):
    text_parts = []

    for item in response.content:
        if item.type == "text":
            text_parts.append(item.text)

    return "".join(text_parts).strip()


def check_summary(summary):
    needed_keys = ["title", "summary", "key_points"]

    for key in needed_keys:
        if key not in summary:
            raise ValueError(f"Claude forgot this JSON field: {key}")

    if not isinstance(summary["key_points"], list):
        raise ValueError("key_points must be a list.")


def summarize_text(text, model=DEFAULT_MODEL, client=None):
    if client is None:
        if "ANTHROPIC_API_KEY" not in os.environ:
            raise ValueError("ANTHROPIC_API_KEY is not set.")

        from anthropic import Anthropic

        client = Anthropic().messages

    response = client.create(
        model=model,
        max_tokens=1000,
        temperature=0,
        system=PROMPT,
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
    )

    response_text = get_response_text(response)
    summary = json.loads(response_text)
    check_summary(summary)
    return summary


def save_or_print(summary, output_file=None):
    pretty_json = json.dumps(summary, indent=2) + "\n"

    if output_file:
        Path(output_file).write_text(pretty_json, encoding="utf-8")
    else:
        print(pretty_json, end="")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-o", "--output")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    try:
        text = read_file(args.file)
        summary = summarize_text(text, args.model)
        save_or_print(summary, args.output)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
