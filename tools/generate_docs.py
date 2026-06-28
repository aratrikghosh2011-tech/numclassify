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

if __name__ == "__main__":
    main()
