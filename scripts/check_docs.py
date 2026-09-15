"""Check local Markdown/HTML link and asset paths without network requests."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt


EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "dist", "build", "coverage",
    "__pycache__", ".pytest_cache", ".next", ".cache", "out",
    "test-results", "playwright-report", ".local-data", ".local-assets",
    ".local-secrets",
}
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data"}


@dataclass
class Report:
    documents: int = 0
    local: int = 0
    external: int = 0
    errors: list[str] = field(default_factory=list)


class HTMLLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.links.extend(
            value for name, value in attrs
            if name in {"href", "src"} and value is not None
        )


def destinations(tokens, line=1):
    """The parser resolves reference links and excludes fenced/inline code."""
    for token in tokens:
        token_line = token.map[0] + 1 if token.map else line
        if token.type == "link_open":
            yield token.attrGet("href"), token_line
        elif token.type == "image":
            yield token.attrGet("src"), token_line
        elif token.type in {"html_inline", "html_block"}:
            parser = HTMLLinks()
            parser.feed(token.content)
            parser.close()
            for link in parser.links:
                yield link, token_line
        if token.children:
            yield from destinations(token.children, token_line)


def check_target(root: Path, source: Path, raw: str) -> tuple[str, str | None]:
    try:
        url = urlsplit(raw)
        if url.scheme.lower() in EXTERNAL_SCHEMES or raw.startswith("//"):
            return "external", None
        if url.scheme:
            return "local", "unsupported scheme or absolute file path"
        path = unquote(url.path)
        if not path:
            return "local", None  # Same-document fragment/query, not anchor validation.
        if path.startswith("/") or "\\" in path or re.match(r"^[A-Za-z]:", path):
            return "local", "use a document-relative path"
        target = (source.parent / path).resolve()
        if not target.is_relative_to(root):
            return "local", "target escapes repository root"
        if not target.exists():
            return "local", "target does not exist"
    except (ValueError, OSError, RuntimeError) as exc:
        return "local", f"invalid path: {exc}"
    return "local", None


def check_tree(root: Path) -> Report:
    root = root.resolve()
    report = Report()
    parser = MarkdownIt("commonmark", {"html": True})
    # Preserve unsafe/absolute destinations for validation instead of silently
    # treating those links as plain text. This script never renders their HTML.
    parser.validateLink = lambda _: True
    for source in sorted(root.rglob("*.md")):
        relative = source.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts[:-1]):
            continue
        report.documents += 1
        if not source.resolve().is_relative_to(root):
            report.errors.append(f"{relative}: document escapes repository root")
            continue
        try:
            tokens = parser.parse(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            report.errors.append(f"{relative}: cannot read Markdown: {exc}")
            continue
        for raw, line in destinations(tokens):
            kind, error = check_target(root, source, raw)
            if kind == "external":
                report.external += 1
            else:
                report.local += 1
            if error:
                report.errors.append(f"{relative}:{line}: {raw!r}: {error}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the directory containing scripts)",
    )
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("--root must be an existing directory")
    report = check_tree(args.root)
    for error in report.errors:
        print(error)
    print(
        f"{'FAIL' if report.errors else 'PASS'}: {report.documents} Markdown files, "
        f"{report.local} local references, {report.external} external references skipped, "
        f"{len(report.errors)} errors"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
