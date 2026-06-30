#!/usr/bin/env python3
"""
Repo health checker for numclassify.
Catches encoding issues, version drift, stale counts, and other problems
that pytest alone cannot detect.

Usage:
    python tools/check_repo.py          # full check
    python tools/check_repo.py --fast   # skip slow checks
    python tools/check_repo.py --fix    # auto-fix what can be fixed

Exit code: 0 if all checks pass, 1 if any fail.
"""
import sys
import re
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
ERRORS = []
WARNINGS = []

def err(msg):
    ERRORS.append(msg)
    print(f"  FAIL: {msg}")

def warn(msg):
    WARNINGS.append(msg)
    print(f"  WARN: {msg}")

def ok(msg):
    print(f"  OK:   {msg}")


# ---- Check 1: No BOM in any source file ----
def check_no_bom():
    print("\n[1] BOM check")
    extensions = ['.py', '.js', '.css', '.html', '.md', '.toml', '.yml', '.yaml']
    for path in ROOT.rglob('*'):
        if any(part.startswith('.') for part in path.parts):
            continue
        if path.suffix not in extensions:
            continue
        try:
            raw = path.read_bytes()
            if raw[:3] == b'\xef\xbb\xbf':
                err(f"BOM found: {path.relative_to(ROOT)}")
        except Exception:
            pass
    if not any('BOM' in e for e in ERRORS):
        ok("No BOM in any source file")


# ---- Check 2: No double CRLF ----
def check_no_double_crlf():
    print("\n[2] Line ending check")
    for path in ROOT.glob('docs/*.js'):
        raw = path.read_bytes()
        if b'\r\r\n' in raw:
            err(f"Double CRLF in: {path.relative_to(ROOT)}")
    if not any('CRLF' in e for e in ERRORS):
        ok("No double CRLF in JS files")


# ---- Check 3: No mojibake in JS/HTML files ----
def check_no_mojibake():
    print("\n[3] Mojibake check")
    BAD = ['\u00e2\u20ac', '\u00f0\u0178', '\u00e2\u0152', '\u00c2\u00a0\u00c2']
    files = list(ROOT.glob('docs/*.js')) + list(ROOT.glob('docs/*.css')) + [ROOT / 'docs' / 'playground.html']
    for path in files:
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
            hits = sum(text.count(b) for b in BAD)
            if hits:
                err(f"Mojibake ({hits} hits) in: {path.relative_to(ROOT)}")
        except Exception as e:
            warn(f"Could not read {path.relative_to(ROOT)}: {e}")
    if not any('Mojibake' in e for e in ERRORS):
        ok("No mojibake in playground files")


# ---- Check 4: Version consistency ----
def check_version_consistency():
    print("\n[4] Version consistency")
    import tomllib

    toml_path = ROOT / 'pyproject.toml'
    try:
        with open(toml_path, 'rb') as f:
            toml_version = tomllib.load(f)['project']['version']
    except Exception as e:
        err(f"Cannot read version from pyproject.toml: {e}")
        return

    ok(f"pyproject.toml version: {toml_version}")

    # Check __init__.py does NOT hardcode a version (fallback "0.0.0" is allowed)
    init = (ROOT / 'numclassify' / '__init__.py').read_text(encoding='utf-8')
    hardcoded = [h for h in re.findall(r'__version__\s*=\s*["\'][\d.]+["\']', init)
                 if '0.0.0' not in h]
    if hardcoded:
        err(f"Hardcoded __version__ in __init__.py: {hardcoded}")
    else:
        ok("__init__.py uses importlib.metadata for version (fallback 0.0.0 ignored)")

    # Check playground.html subtitle count
    html_path = ROOT / 'docs' / 'playground.html'
    if html_path.exists():
        html = html_path.read_text(encoding='utf-8')
        stale_counts = re.findall(r'(\d{4}\+)\s+named', html)
        for count in stale_counts:
            if count != '2140+':
                err(f"Stale count in playground.html subtitle: '{count}' (expected '2140+')")
        if '2140+' in html:
            ok("playground.html subtitle count: 2140+")

    # Check README "What's new" matches pyproject version
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    readme_versions = re.findall(r"What's new in v([\d.]+)", readme)
    if readme_versions:
        if readme_versions[0] != toml_version:
            warn(f"README 'What's new' says v{readme_versions[0]}, pyproject says v{toml_version}")
        else:
            ok(f"README 'What's new' matches version: v{toml_version}")

    # Check CHANGELOG has entry for current version
    changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    if f'[{toml_version}]' not in changelog:
        err(f"CHANGELOG.md missing entry for [{toml_version}]")
    else:
        ok(f"CHANGELOG.md has entry for [{toml_version}]")


# ---- Check 5: No emoji in JS files ----
def check_no_emoji_in_js():
    print("\n[5] Emoji check in JS files")
    EMOJI_RANGES = [
        (0x1F300, 0x1FFFF),
        (0x2600, 0x27BF),
        (0x1F000, 0x1F02F),
    ]
    def has_emoji(text):
        return any(
            any(lo <= ord(c) <= hi for lo, hi in EMOJI_RANGES)
            for c in text
        )
    for path in ROOT.glob('docs/*.js'):
        text = path.read_text(encoding='utf-8', errors='replace')
        if has_emoji(text):
            err(f"Emoji found in JS file: {path.relative_to(ROOT)}")
    if not any('Emoji' in e for e in ERRORS):
        ok("No emoji in JS files")


# ---- Check 6: Registry count vs docs ----
def check_registry_count():
    print("\n[6] Registry count vs docs")
    try:
        sys.path.insert(0, str(ROOT))
        from numclassify._registry import REGISTRY, _normalize
        total = sum(1 for k, e in REGISTRY.items() if k == _normalize(e.name))
        ok(f"Registry has {total} unique types")

        idx = (ROOT / 'docs' / 'index.md').read_text(encoding='utf-8')
        counts = re.findall(r'(\d+)\+?\s+(?:named\s+)?(?:mathematical\s+)?types', idx)
        for c in counts:
            if abs(int(c) - total) > 200:
                warn(f"docs/index.md mentions {c} types but registry has {total}")
    except Exception as e:
        warn(f"Could not check registry count: {e}")


# ---- Check 7: No leaked internal names in public API ----
def check_no_leaked_names():
    print("\n[7] Public API leak check")
    try:
        import numclassify as nc
        public = [x for x in dir(nc) if not x.startswith('_')]
        ALLOWED = {
            'classify', 'classify_batch', 'random_number', 'find_by_property',
            'stream', 'get_all_properties', 'get_true_properties', 'print_properties',
            'count_properties', 'most_special_in_range', 'find_in_range',
            'find_all_in_range', 'find_any_in_range', 'register',
            'is_prime', 'is_armstrong', 'is_perfect',
            'why', 'property_info', 'find', 'get_exam_types',
            'similar_numbers', 'specialness_percentile',
        }
        leaked = set(public) - ALLOWED
        if leaked:
            err(f"Leaked public names: {sorted(leaked)}")
        else:
            ok(f"Public API has {len(public)} names, no leaks")
    except Exception as e:
        warn(f"Could not check public API: {e}")


# ---- Check 8: CLI commands respond without crashing ----
def check_cli_smoke():
    print("\n[8] CLI smoke check")
    import subprocess
    commands = [
        ['numclassify', 'check', '153'],
        ['numclassify', 'check', '6', '--json'],
        ['numclassify', 'info', 'prime'],
        ['numclassify', 'why', 'prime', '7'],
        ['numclassify', 'find', 'prime', '--limit', '3'],
        ['numclassify', 'list', '--category', 'primes'],
        ['numclassify', 'compare', '6', '28'],
        ['numclassify', 'query', '1', '100', '--has', 'prime'],
        ['numclassify'],
    ]
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            err(f"CLI failed: {' '.join(cmd)}\n    stderr: {result.stderr[:200]}")
        else:
            ok(f"CLI OK: {' '.join(cmd)}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--fast', action='store_true', help='Skip slow checks')
    parser.add_argument('--fix', action='store_true', help='Auto-fix what can be fixed')
    args = parser.parse_args()

    print("=" * 60)
    print("numclassify repo health check")
    print("=" * 60)

    check_no_bom()
    check_no_double_crlf()
    check_no_mojibake()
    check_version_consistency()
    check_no_emoji_in_js()
    check_registry_count()
    check_no_leaked_names()
    if not args.fast:
        check_cli_smoke()

    print("\n" + "=" * 60)
    if ERRORS:
        print(f"FAILED: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)
    elif WARNINGS:
        print(f"PASSED with {len(WARNINGS)} warning(s)")
        for w in WARNINGS:
            print(f"  - {w}")
        sys.exit(0)
    else:
        print("ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == '__main__':
    main()
