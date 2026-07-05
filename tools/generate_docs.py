#!/usr/bin/env python3
"""Auto-generate category count tables in docs/index.md and README.md."""
import sys
from pathlib import Path
from collections import Counter
from itertools import groupby

sys.path.insert(0, str(Path(__file__).parent.parent))
from numclassify._registry import REGISTRY, _normalize

CATEGORY_DISPLAY = {
    'primes': 'Prime families',
    'digital': 'Digital invariants',
    'divisors': 'Divisor-based',
    'sequences': 'Sequences',
    'powers': 'Powers',
    'number_theory': 'Number theory',
    'combinatorial': 'Combinatorial',
    'recreational': 'Recreational',
    'exam_types': 'Exam types',
}


def count_by_category():
    counts = Counter()
    figurate_total = 0
    centered_total = 0
    for key, entry in REGISTRY.items():
        if key != _normalize(entry.name):
            continue
        cat = entry.category.lower().replace(' ', '_')
        if 'centered' in cat and ('polygonal' in cat or 'figurate' in cat):
            centered_total += 1
        elif 'figurate' in cat or 'polygonal' in cat:
            figurate_total += 1
        else:
            counts[entry.category] += 1
    return counts, figurate_total, centered_total

def build_table(counts, figurate_total, centered_total):
    total = sum(counts.values()) + figurate_total + centered_total
    lines = ["| Category | Count |", "|---|---|"]
    lines.append(f"| Polygonal figurate | ~{figurate_total} |")
    lines.append(f"| Centered polygonal | ~{centered_total} |")
    for cat, display in CATEGORY_DISPLAY.items():
        c = counts.get(cat, 0)
        if c:
            lines.append(f"| {display} | {c} |")
    lines.append(f"| **Total** | **{total}** |")
    return "\n".join(lines)

def replace_between_markers(content: str, marker: str, new_content: str) -> str:
    start_marker = f"<!-- {marker}:start -->"
    end_marker = f"<!-- {marker}:end -->"
    start = content.find(start_marker)
    end = content.find(end_marker)
    if start == -1 or end == -1:
        print(f"  WARNING: markers '{marker}' not found -- skipping")
        return content
    return content[:start + len(start_marker)] + "\n" + new_content + "\n" + content[end:]

def update_file(path: Path, table: str, marker: str):
    if not path.exists():
        print(f"  SKIP: {path} not found")
        return
    content = path.read_text(encoding='utf-8')
    new_content = replace_between_markers(content, marker, table)
    if new_content == content:
        print(f"  UNCHANGED: {path}")
    else:
        path.write_text(new_content, encoding='utf-8')
        print(f"  UPDATED: {path}")

def get_public_api_count():
    import numclassify as nc
    return len([x for x in dir(nc) if not x.startswith('_')])


def get_pyproject_version():
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib
    with open('pyproject.toml', 'rb') as f:
        return tomllib.load(f)['project']['version']


def build_version_heading(version: str) -> str:
    return f"## What's new in v{version}"


def coverage_color(pct: float) -> str:
    if pct >= 90:
        return 'brightgreen'
    elif pct >= 75:
        return 'green'
    elif pct >= 60:
        return 'yellow'
    elif pct >= 40:
        return 'orange'
    else:
        return 'red'


def build_coverage_badge(pct: float) -> str:
    color = coverage_color(pct)
    pct_int = int(pct)
    return (
        f"[![Coverage](https://img.shields.io/badge/coverage-{pct_int}%25-{color}"
        f"?style=flat-square)](https://github.com/aratrikghosh2011-tech/numclassify/tree/main/tests)"
    )


def read_coverage_from_json(path='coverage.json'):
    import json
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        return data['totals']['percent_covered']
    except (KeyError, json.JSONDecodeError):
        return None


def main():
    root = Path(__file__).parent.parent
    counts, fig, cen = count_by_category()
    table = build_table(counts, fig, cen)

    print(f"\nGenerated table:\n{table}\n")

    update_file(root / "docs" / "index.md", table, "category-table")
    update_file(root / "README.md", table, "category-table")

    handcrafted_with = sum(
        1 for k, e in REGISTRY.items()
        if k == _normalize(e.name)
        and 'figurate' not in e.category.lower()
        and 'polygonal' not in e.category.lower()
        and e.explain is not None
    )
    handcrafted_total = sum(
        1 for k, e in REGISTRY.items()
        if k == _normalize(e.name)
        and 'figurate' not in e.category.lower()
        and 'polygonal' not in e.category.lower()
    )
    print(f"Explain coverage: {handcrafted_with}/{handcrafted_total} ({100*handcrafted_with/handcrafted_total:.1f}%)")

    version = get_pyproject_version()
    version_heading = build_version_heading(version)
    readme_path = root / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding='utf-8')
        new_content = replace_between_markers(content, "version-heading", version_heading)
        if new_content != content:
            readme_path.write_text(new_content, encoding='utf-8')
            print(f"  UPDATED: README.md version heading -> v{version}")
        else:
            print(f"  UNCHANGED: README.md version heading")

    api_count = get_public_api_count()
    print(f"\nPublic API count: {api_count} names")

    coverage_pct = read_coverage_from_json()
    if coverage_pct is not None:
        badge = build_coverage_badge(coverage_pct)
        if readme_path.exists():
            content = readme_path.read_text(encoding='utf-8')
            new_content = replace_between_markers(content, "coverage-badge", badge)
            if new_content != content:
                readme_path.write_text(new_content, encoding='utf-8')
                print(f"  UPDATED: README.md coverage badge -> {int(coverage_pct)}%")
            else:
                print(f"  UNCHANGED: README.md coverage badge")
    else:
        print(f"  SKIPPED: coverage badge (no coverage.json -- run pytest --cov-report=json first)")

if __name__ == "__main__":
    main()
