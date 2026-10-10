"""Tests for reporting what the linter actually scanned."""

import pytest

from alt_text_linter import AltTextLinter, main


def test_no_qmd_files(tmp_path, capsys):
    """An empty scan does not claim to have checked images."""
    (tmp_path / "notes.md").write_text("![](image.png)", encoding="utf-8")

    assert AltTextLinter(root=tmp_path).run() == 0
    assert capsys.readouterr().out == (
        f"No .qmd files found under {tmp_path}.\n"
    )


@pytest.mark.parametrize(
    "content",
    [
        "",
        "A document without images.",
        "```markdown\n![](example.png)\n<img src='example.png'>\n```",
        "Inline code: `![](example.png)` and `<img src='example.png'>`.",
    ],
)
def test_no_images(tmp_path, capsys, content):
    """Code examples do not count as scanned images."""
    (tmp_path / "doc.qmd").write_text(content, encoding="utf-8")

    assert AltTextLinter(root=tmp_path).run() == 0
    assert capsys.readouterr().out == "No images found in .qmd files.\n"


@pytest.mark.parametrize(
    "content",
    [
        '![](image.png){fig-alt="A plot"}',
        '![](image.png){alt="A plot"}',
        "![A plot](image.png)\\",
        '<img src="image.png" alt="A plot">',
        '<img src="decorative.png" alt="" />',
        '<IMG SRC="image.png" ALT="A plot">',
    ],
)
def test_images_with_alt_text(tmp_path, capsys, content):
    """A real image with alt text retains the existing success message."""
    (tmp_path / "doc.qmd").write_text(content, encoding="utf-8")

    assert AltTextLinter(root=tmp_path).run() == 0
    assert capsys.readouterr().out == "\u2713 All images have alt text!\n"


@pytest.mark.parametrize(
    ("content", "kind"),
    [
        ("![](image.png)", "markdown"),
        ("![A caption](image.png)", "markdown"),
        ('<img src="image.png">', "html"),
    ],
)
def test_images_missing_alt_text(tmp_path, capsys, content, kind):
    """Findings keep their failure exit code and source details."""
    path = tmp_path / "doc.qmd"
    path.write_text(content, encoding="utf-8")

    assert AltTextLinter(root=tmp_path).run() == 1
    assert capsys.readouterr().out == (
        f"\n{path}:\n  Line 1 [{kind}]: {content}\n"
    )


@pytest.mark.parametrize("is_file", [False, True])
def test_invalid_root(tmp_path, capsys, is_file):
    """An invalid directory input fails clearly instead of claiming success."""
    root = tmp_path / "invalid"
    if is_file:
        root.write_text("A regular file.", encoding="utf-8")

    assert main([str(root)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"Not a directory: {root}\n"


def test_recursive_scan_with_image_free_files(tmp_path, capsys):
    """An image-free file does not hide images found in another directory."""
    (tmp_path / "empty.qmd").write_text("", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "doc.qmd").write_text(
        '![](image.png){fig-alt="A plot"}',
        encoding="utf-8",
    )

    assert AltTextLinter(root=tmp_path).run() == 0
    assert capsys.readouterr().out == "\u2713 All images have alt text!\n"
