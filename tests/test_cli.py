import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from claude_summary_agent.cli import read_file, save_or_print, summarize_text


GOOD_SUMMARY = {
    "title": "Project Notes",
    "summary": "These notes describe a small Claude summary CLI.",
    "key_points": ["Read a file", "Return JSON"],
}


class FakeClaude:
    def __init__(self, text):
        self.text = text
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs
        return SimpleNamespace(
            content=[
                SimpleNamespace(type="text", text=self.text),
            ]
        )


class CliTests(unittest.TestCase):
    def test_read_file(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = Path(folder) / "notes.txt"
            file_path.write_text("hello", encoding="utf-8")

            self.assertEqual(read_file(file_path), "hello")

    def test_read_file_does_not_allow_empty_files(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = Path(folder) / "empty.txt"
            file_path.write_text("   ", encoding="utf-8")

            with self.assertRaises(ValueError):
                read_file(file_path)

    def test_summarize_text_uses_claude_and_returns_json(self):
        fake_claude = FakeClaude(json.dumps(GOOD_SUMMARY))

        summary = summarize_text("Some notes to summarize.", "claude-test", fake_claude)

        self.assertEqual(summary["title"], "Project Notes")
        self.assertEqual(fake_claude.last_request["model"], "claude-test")
        self.assertEqual(fake_claude.last_request["messages"][0]["content"], "Some notes to summarize.")

    def test_summarize_text_rejects_missing_key_points(self):
        fake_claude = FakeClaude(json.dumps({"title": "Oops", "summary": "Missing a field."}))

        with self.assertRaises(ValueError):
            summarize_text("Some notes.", "claude-test", fake_claude)

    def test_save_or_print_writes_output_file(self):
        with tempfile.TemporaryDirectory() as folder:
            output_file = Path(folder) / "summary.json"

            save_or_print(GOOD_SUMMARY, output_file)

            saved = json.loads(output_file.read_text(encoding="utf-8"))
            self.assertEqual(saved, GOOD_SUMMARY)


if __name__ == "__main__":
    unittest.main()
