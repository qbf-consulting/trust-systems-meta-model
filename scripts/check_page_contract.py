#!/usr/bin/env python3
"""Validate the source-to-GitHub-Pages and Just The Docs publication contract."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '.bundle', 'vendor', 'node_modules', '_site', 'scripts', 'validation', 'artifacts', '.github'}
CONFIG_EXCLUDED = set()
errors = []
count = 0
pages = []

config = yaml.safe_load((ROOT / '_config.yml').read_text(encoding='utf-8')) or {}
for item in config.get('exclude') or []:
    if isinstance(item, str):
        CONFIG_EXCLUDED.add(item.rstrip('/'))
defaults = config.get('defaults') or []
has_page_layout_default = any(
    isinstance(item, dict)
    and (item.get('scope') or {}).get('path', '') == ''
    and (item.get('scope') or {}).get('type') == 'pages'
    and (item.get('values') or {}).get('layout') == 'default'
    for item in defaults
)
if not has_page_layout_default:
    errors.append('_config.yml: missing global layout: default for Jekyll pages')

for path in sorted(ROOT.rglob('*.md')):
    if any(part in EXCLUDED for part in path.parts):
        continue
    rel_path = path.relative_to(ROOT).as_posix()
    if rel_path in CONFIG_EXCLUDED or any(rel_path.startswith(item + '/') for item in CONFIG_EXCLUDED):
        continue
    text = path.read_text(encoding='utf-8', errors='replace')
    count += 1
    if not text.startswith('---\n'):
        errors.append(f'{path.relative_to(ROOT)}: missing front matter')
        continue
    end = text.find('\n---\n', 4)
    if end < 0:
        errors.append(f'{path.relative_to(ROOT)}: unterminated front matter')
        continue
    try:
        fm = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as exc:
        errors.append(f'{path.relative_to(ROOT)}: invalid YAML front matter: {exc}')
        continue
    title = fm.get('title')
    if not title:
        errors.append(f'{path.relative_to(ROOT)}: missing title')
    pages.append((path, fm))
    if path.is_relative_to(ROOT / 'docs'):
        rel = path.relative_to(ROOT / 'docs')
        expected = '/documentation/' if rel.as_posix() == 'index.md' else (
            f'/{rel.parts[0]}/' if rel.name == 'index.md' else f'/{rel.with_suffix(".html").as_posix()}'
        )
        actual = fm.get('permalink')
        if actual != expected:
            errors.append(f'{path.relative_to(ROOT)}: permalink {actual!r}, expected {expected!r}')

# Validate Just The Docs ancestry by title, not by filesystem location.
titles = {fm.get('title') for _, fm in pages if fm.get('title')}
for path, fm in pages:
    parent = fm.get('parent')
    grand_parent = fm.get('grand_parent')
    if parent and parent not in titles:
        errors.append(f'{path.relative_to(ROOT)}: parent title {parent!r} does not resolve')
    if grand_parent and grand_parent not in titles:
        errors.append(f'{path.relative_to(ROOT)}: grand_parent title {grand_parent!r} does not resolve')

# The documentation root must be the title referenced throughout the hierarchy.
docs_index = next((fm for path, fm in pages if path == ROOT / 'docs' / 'index.md'), {})
if docs_index.get('title') != 'Documentation':
    errors.append("docs/index.md: title must be 'Documentation' to match child parent references")

# Explicit regression checks for historically failing routes.
permalinks = {fm.get('permalink') for _, fm in pages}
for required in (
    '/documentation/',
    '/model/discovery-governance.html',
    '/model/capability-negotiation.html',
    '/model/runtime-governance-envelope.html',
):
    if required not in permalinks:
        errors.append(f'missing canonical route {required}')

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f'Validated Just The Docs layout, ancestry, and canonical routes for {count} Markdown sources.')
