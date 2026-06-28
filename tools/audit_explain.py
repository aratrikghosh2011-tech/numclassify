#!/usr/bin/env python3
"""Audit explain= coverage across all handcrafted numclassify types."""
import argparse
import sys
from itertools import groupby
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from numclassify._registry import REGISTRY, _normalize

FIGURATE_CATS = {
    'figurate', 'centered_figurate', 'polygonal figurate',
    'centered polygonal', 'polygonal_figurate', 'centered_polygonal',
}

def is_figurate(entry) -> bool:
    cat = entry.category.lower().replace(' ', '_')
    return (
        'figurate' in cat or
        ('centered' in cat and 'polygonal' in cat) or
        cat in FIGURATE_CATS
    )


def main():
    parser = argparse.ArgumentParser(description="Audit explain= coverage")
    parser.add_argument('--category', help="Filter by category")
    parser.add_argument('--missing-only', action='store_true', help="Show only types without explain")
    parser.add_argument('--covered-only', action='store_true', help="Show only types with explain")
    args = parser.parse_args()

    has_explain = []
    no_explain = []

    for key, entry in REGISTRY.items():
        if key != _normalize(entry.name):
            continue
        if is_figurate(entry):
            continue
        if args.category and entry.category.lower() != args.category.lower():
            continue
        if entry.explain is not None:
            has_explain.append(entry)
        else:
            no_explain.append(entry)

    total = len(has_explain) + len(no_explain)
    pct = 100 * len(has_explain) / total if total > 0 else 0

    print(f"\nExplain coverage: {len(has_explain)}/{total} ({pct:.1f}%)\n")

    if not args.missing_only:
        print(f"WITH explain ({len(has_explain)}):")
        has_explain.sort(key=lambda e: e.category)
        for cat, items in groupby(has_explain, key=lambda e: e.category):
            names = [e.name for e in items]
            print(f"  [{cat}] {names}")

    if not args.covered_only:
        print(f"\nMISSING explain ({len(no_explain)}):")
        no_explain.sort(key=lambda e: e.category)
        for cat, items_iter in groupby(no_explain, key=lambda e: e.category):
            names = [e.name for e in items_iter]
            print(f"  [{cat}] ({len(names)}): {names}")


if __name__ == "__main__":
    main()
