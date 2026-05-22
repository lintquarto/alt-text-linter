import pytest
from pathlib import Path
from alt_text_linter import AltTextLinter


MISSING_BACKTICK = """\

Open `index.qmd in the editor.

![](image1.png)

In the terminal type `quarto preview.

![](image2.png)
"""


def test_missing_backtick(tmp_path):
    """Regression test for issue #14: inline code missing a backtick."""
    qmd = tmp_path / "test.qmd"
    qmd.write_text(MISSING_BACKTICK, encoding="utf-8")

    linter = AltTextLinter(root=tmp_path)
    issues = linter.check_file(qmd)
    images = [snippet for _, snippet in issues]

    # Raise a failure if the image (neither have alt-text) are not flagged
    failures = []
    for image in ["image1", "image2"]:
        if f"![]({image}.png)" not in images:
            failures.append(f"{image}.png")
    if failures:
        pytest.fail(f"Images not flagged: {failures}.")
