"""Regression tests for the alt text linter."""

from alt_text_linter import AltTextLinter

HTML_IMAGES = """\
<img src="image.png">
<img src="decorative.png" alt="">
<img SRC="plot.png" ALT="A plot">
<img src="self-closing.png" />
"""


def test_flags_html_img_without_alt(tmp_path) -> None:
    """HTML img tags without alt attributes are reported."""
    path = tmp_path / "doc.qmd"
    path.write_text(HTML_IMAGES, encoding="utf-8")

    issues = AltTextLinter().check_file(path)

    assert issues == [
        (1, '<img src="image.png">'),
        (4, '<img src="self-closing.png" />'),
    ]
