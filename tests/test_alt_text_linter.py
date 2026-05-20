"""Regression tests for the alt text linter."""

import tempfile
import unittest
from pathlib import Path

from alt_text_linter import AltTextLinter


class AltTextLinterTests(unittest.TestCase):
    """Tests for image detection."""

    def test_flags_html_img_without_alt(self) -> None:
        """HTML img tags without alt attributes are reported."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "doc.qmd"
            path.write_text(
                "\n".join(
                    [
                        '<img src="image.png">',
                        '<img src="decorative.png" alt="">',
                        '<img SRC="plot.png" ALT="A plot">',
                        '<img src="self-closing.png" />',
                    ],
                ),
                encoding="utf-8",
            )

            issues = AltTextLinter().check_file(path)

        self.assertEqual(
            issues,
            [
                (1, '<img src="image.png">'),
                (4, '<img src="self-closing.png" />'),
            ],
        )


if __name__ == "__main__":
    unittest.main()
