#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
EXCLUDED_DIRS = {".git", ".bundle", "vendor", "node_modules", "_site"}
MARKDOWN_FILES = [
    p for p in ROOT.rglob("*.md")
    if not any(part in EXCLUDED_DIRS for part in p.parts)
]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
APP_VERSION_RE = re.compile(r"^applicable_version:\s*(.+)$", re.MULTILINE)

IGNORE_PREFIXES = ("http://", "https://", "mailto:", "#")
IGNORE_FILES_FOR_VERSION = {p for p in (ROOT / "releases").glob("v*.md")}


def semver(value: str) -> tuple[int, int, int] | None:
    value = value.strip().strip('"').strip("'").removeprefix("v")
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def check_frontmatter_version(path: Path) -> list[str]:
    errors: list[str] = []
    if path in IGNORE_FILES_FOR_VERSION:
        return errors
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return errors
    fm = match.group(1)
    version_match = APP_VERSION_RE.search(fm)
    if not version_match:
        return errors

    value = version_match.group(1).strip()
    declared = semver(value)
    current = semver(VERSION)
    if declared is None:
        errors.append(f"{path.relative_to(ROOT)} has invalid applicable_version {value}")
    elif current is None:
        errors.append(f"VERSION {VERSION} is not valid semantic version metadata")
    elif declared > current:
        errors.append(
            f"{path.relative_to(ROOT)} has future applicable_version {value}, current release is {VERSION}"
        )
    return errors


def resolve_link(path: Path, link: str) -> Path | None:
    target = link.split("#", 1)[0].strip()
    if not target or target.startswith(IGNORE_PREFIXES):
        return None
    return (path.parent / target).resolve()


def check_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for link in LINK_RE.findall(text):
        resolved = resolve_link(path, link)
        if resolved is None:
            continue
        if not resolved.exists():
            errors.append(f"Broken link in {path.relative_to(ROOT)} -> {link}")
    return errors


def main() -> None:
    errors: list[str] = []
    for md in MARKDOWN_FILES:
        errors.extend(check_links(md))
        errors.extend(check_frontmatter_version(md))
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(
        f"Checked {len(MARKDOWN_FILES)} markdown files: links and non-future applicable_version metadata passed."
    )


if __name__ == "__main__":
    main()
