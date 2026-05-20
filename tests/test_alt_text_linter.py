"""Regression tests for alt-text-linter."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from alt_text_linter import AltTextLinter


class TestAltTextLinter(TestCase):
    """Exercise alt text linting behavior."""

    def test_code_masking_keeps_reported_line_numbers(self) -> None:
        """Report original line numbers after fenced and inline code."""
        text = "\n".join(
            [
                "Intro",
                "",
                "```yaml",
                "project:",
                "  type: website",
                "```",
                "",
                "Text with `![](ignored.png)` inline code.",
                "",
                "![](missing.png)",
                "",
            ],
        )
        expected_line = text.splitlines().index("![](missing.png)") + 1

        with TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "example.qmd"
            path.write_text(text, encoding="utf-8")

            issues = AltTextLinter().check_file(path)

        self.assertEqual([(expected_line, "![](missing.png)")], issues)
