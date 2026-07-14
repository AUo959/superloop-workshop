#!/usr/bin/env python3
"""Dependency-free structural checks for Superloop Workshop."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "PROJECT_CHARTER.md",
    "README.md",
    "ROADMAP.md",
    "docs/bridges",
    "docs/decisions",
    "docs/whitepapers",
    "experiments",
    "registry/CONCEPT_REGISTRY.md",
    "specs",
    "src",
    "tests",
)
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
IGNORED_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:")


def check_required_paths() -> list[str]:
    return [f"missing required path: {path}" for path in REQUIRED_PATHS if not (ROOT / path).exists()]


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    for document in sorted(ROOT.rglob("*.md")):
        if ".git" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith("#") or target.startswith(IGNORED_SCHEMES):
                continue
            path_text = unquote(target.split("#", 1)[0].split("?", 1)[0])
            resolved = (document.parent / path_text).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{document.relative_to(ROOT)}: link escapes repository: {raw_target}")
                continue
            if not resolved.exists():
                errors.append(f"{document.relative_to(ROOT)}: missing link target: {raw_target}")
    return errors


def main() -> int:
    errors = check_required_paths() + check_markdown_links()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    markdown_count = sum(1 for _ in ROOT.rglob("*.md"))
    print(f"Repository integrity passed: {markdown_count} Markdown files checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

