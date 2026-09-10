#!/usr/bin/env python3
"""Fail when any published Markdown source or internal link is absent from _site."""
from __future__ import annotations

import re
import yaml
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EXCLUDED = {".git", ".bundle", "vendor", "node_modules", "_site", "scripts", "validation", "artifacts", ".github"}
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)
PERMALINK_RE = re.compile(r'^permalink:\s*(\S+)', re.M)
errors: list[str] = []

config = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8")) or {}
CONFIG_EXCLUDED = {item.rstrip("/") for item in (config.get("exclude") or []) if isinstance(item, str)}


def is_config_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return rel in CONFIG_EXCLUDED or any(rel.startswith(item + "/") for item in CONFIG_EXCLUDED)


def sources() -> list[Path]:
    return [
        p for p in ROOT.rglob("*.md")
        if not any(part in EXCLUDED for part in p.parts) and not is_config_excluded(p)
    ]


def front_matter(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return text[4:end] if end >= 0 else ""


def expected_output(path: Path) -> Path:
    match = PERMALINK_RE.search(front_matter(path))
    if match:
        route = match.group(1).split("#", 1)[0].split("?", 1)[0].lstrip("/")
        return SITE / route / "index.html" if route.endswith("/") else SITE / route
    rel = path.relative_to(ROOT)
    return SITE / ("index.html" if rel.as_posix() == "index.md" else rel.with_suffix(".html"))


def source_candidates_for_href(path: str) -> list[Path]:
    """Map source-style links emitted by Jekyll back to published outputs."""
    clean = path.lstrip("./")
    candidates: list[Path] = []
    for source in (ROOT / clean, ROOT / "docs" / clean):
        if source.is_file() and not is_config_excluded(source):
            if source.suffix == ".md":
                candidates.append(expected_output(source))
            else:
                candidates.append(SITE / source.relative_to(ROOT))
        elif source.is_dir():
            index = source / "index.md"
            if index.is_file() and not is_config_excluded(index):
                candidates.append(expected_output(index))
    return candidates


if not (SITE / "index.html").is_file():
    errors.append("Missing _site/index.html")

source_files = sources()
for source in source_files:
    target = expected_output(source)
    if not target.is_file():
        errors.append(f"Missing rendered page for {source.relative_to(ROOT)} -> {target.relative_to(SITE)}")

for required in ("model/discovery-governance.html", "model/capability-negotiation.html"):
    if not (SITE / required).is_file():
        errors.append(f"Reported 404 route was not generated: {required}")

if not (SITE / "assets/js/mermaid-init.js").is_file():
    errors.append("Missing generated Mermaid bootstrap asset")

html_files = list(SITE.rglob("*.html"))
for page in html_files:
    text = page.read_text(encoding="utf-8", errors="replace")
    for href in HREF_RE.findall(text):
        parsed = urlsplit(href)
        if parsed.scheme or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        path = unquote(parsed.path)
        if not path:
            continue
        if path.startswith("/trust-systems-meta-model/"):
            target = SITE / path.removeprefix("/trust-systems-meta-model/")
        elif path == "/trust-systems-meta-model":
            target = SITE / "index.html"
        elif path.startswith("/"):
            continue
        else:
            target = page.parent / path
        candidates = [target]
        if target.suffix == "":
            candidates.extend([target.with_suffix(".html"), target / "index.html"])
        candidates.extend(source_candidates_for_href(path))
        if not any(candidate.resolve().exists() for candidate in candidates):
            errors.append(f"Broken generated link in {page.relative_to(SITE)} -> {href}")

if errors:
    for error in sorted(set(errors)):
        print(error)
    raise SystemExit(1)

print(f"Verified exact output routes for {len(source_files)} Markdown sources, {len(html_files)} HTML pages, internal links, and Mermaid assets.")
