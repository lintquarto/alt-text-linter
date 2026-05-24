"""Tests for AltTextLinter."""

import pytest

from alt_text_linter import AltTextLinter


@pytest.mark.parametrize(
    "content",
    [
        '![](image.png){fig-alt="This image has alt-text"}',
        '![](image.png){alt="This image also has alt-text"}',
        "![Due to backslash, image renders caption as alt text](image.png)\\",
        '<img src="image.png" alt="This HTML image has alt-text">',
    ],
)
def test_success(tmp_path, content):
    """Test it works on success cases."""
    qmd_path = tmp_path / "test.qmd"
    qmd_path.write_text(content, encoding="utf-8")
    linter = AltTextLinter()
    issues = linter.check_file(qmd_path)
    assert issues == []


@pytest.mark.parametrize(
    "content",
    [
        "![](image.png)",
        "![Only a caption, no alt text](image.png)",
        '<img src="image.png">',
    ],
)
def test_failure(tmp_path, content):
    """Test it raises issues on failure cases."""
    qmd_path = tmp_path / "test.qmd"
    qmd_path.write_text(content, encoding="utf-8")
    linter = AltTextLinter()
    issues = linter.check_file(qmd_path)
    assert issues == [(1, content)]
