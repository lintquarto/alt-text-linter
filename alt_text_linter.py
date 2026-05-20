"""
Check QMD files for images missing alt text .

Intended for use in CI/CD pipelines, returning a non-zero exit code
when issues are found.
"""

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class _HTMLImageParser(HTMLParser):
    """
    Collect HTML image tags that do not define alt text.

    HTMLParser gives us line numbers and normalized attributes without adding a
    heavier dependency for this small action.

    """

    def __init__(self) -> None:
        """Initialise the parser."""
        super().__init__()
        self.issues: list[tuple[int, str]] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Check non-empty HTML start tags."""
        self._check_image(tag, attrs)

    def handle_startendtag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Check self-closing HTML start tags."""
        self._check_image(tag, attrs)

    def _check_image(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        """Record an issue for img tags without an alt attribute."""
        if tag.lower() != "img":
            return

        if any(name.lower() == "alt" for name, _value in attrs):
            return

        line, _offset = self.getpos()
        self.issues.append((line, self.get_starttag_text() or "<img>"))


class AltTextLinter:
    """
    Scan QMD files for images missing alt text.

    Searches for markdown image syntax `![](...)` that is not followed
    by a Quarto attribute block containing `alt` or `fig-alt`, and HTML
    `<img>` tags without an `alt` attribute. Code blocks (fenced and inline)
    are stripped before scanning to avoid false positives.

    Attributes
    ----------
    root : Path
        Root directory for the file search.

    """

    # Regex to match fenced code blocks (i.e., ``` ... ```)
    _CODE_FENCE_RE = re.compile(r"```[\s\S]*?```")

    # Regex to match inline code (i.e., ` ... `)
    _INLINE_CODE_RE = re.compile(r"`[^`]*`")

    # Regex to match markdown images
    _IMAGE_RE = re.compile(r"(?<!\[)!\[(?:\s*)\]\([^)]+\)")

    # Regex to match a Quarto attribute block containing alt or fig-alt
    _ALT_RE = re.compile(r"\s*\{[^}]*(?:\balt=|\bfig-alt=)[^}]*\}")

    def __init__(self, root: Path = Path()) -> None:
        """
        Initialise the linter.

        Parameters
        ----------
        root : Path
            Directory to recursively search for `.qmd` files. Defaults to the
            current working directory.

        """
        self.root = root

    def _strip_code(self, text: str) -> str:
        """
        Remove fenced and inline code blocks from text.

        Prevents code examples containing image syntax from being
        flagged as missing alt text.

        Parameters
        ----------
        text : str
            Raw file content.

        Returns
        -------
        str
            Content with all code blocks replaced by empty strings.

        """
        result = self._CODE_FENCE_RE.sub("", text)
        return self._INLINE_CODE_RE.sub("", result)

    def check_file(self, path: Path) -> list[tuple[int, str]]:
        """
        Find markdown images missing alt or fig-alt in a single file.

        Parameters
        ----------
        path : Path
            Path to a `.qmd` file.

        Returns
        -------
        list[tuple[int, str]]
            Pairs of (line_number, image_snippet) for each image that is not
            followed by an attribute block containing `alt` or `fig-alt`.

        """
        text = path.read_text(encoding="utf-8")
        stripped = self._strip_code(text)

        issues: list[tuple[int, str]] = []

        for match in self._IMAGE_RE.finditer(stripped):
            # Check the text after the image for a {fig-alt=...} block
            following = stripped[match.end() : match.end() + 200]
            if self._ALT_RE.match(following):
                continue

            line = text.count("\n", 0, match.start()) + 1
            issues.append((line, match.group(0)))

        html_parser = _HTMLImageParser()
        html_parser.feed(stripped)
        issues.extend(html_parser.issues)

        return sorted(issues, key=lambda issue: issue[0])

    def run(self) -> int:
        """
        Lint all QMD files under root and print results.

        Returns
        -------
        int
            Exit code: 0 if all images have alt text, 1 otherwise.

        """
        found_any = False

        for path in self.root.rglob("*.qmd"):
            issues = self.check_file(path)
            if not issues:
                continue

            found_any = True
            print(f"\n{path}:")
            for line, snippet in issues:
                kind = (
                    "html"
                    if snippet.lstrip().lower().startswith("<img")
                    else "markdown"
                )
                print(f"  Line {line} [{kind}]: {snippet}")

        if not found_any:
            print("\u2713 All images have alt text!")

        return 1 if found_any else 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Parameters
    ----------
    argv : list of str, optional
        Arguments to parse (defaults to `sys.argv[1:]`).

    Returns
    -------
    argparse.Namespace
        Parsed arguments.

    """
    parser = argparse.ArgumentParser(
        description="Check QMD files for images missing alt text (fig-alt).",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to search (default: current directory).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point for command-line execution."""
    args = parse_args(argv)
    root = Path(args.path)
    linter = AltTextLinter(root=root)
    return linter.run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
