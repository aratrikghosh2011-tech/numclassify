#!/usr/bin/env python3
"""
Repo health checker for numclassify.
Catches encoding issues, version drift, stale counts, and other problems
that pytest alone cannot detect.

Usage:
    python tools/check_repo.py          # full check
    python tools/check_repo.py --fast   # skip slow checks

Exit code: 0 if all checks pass, 1 if any fail.
"""
import sys
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
ERRORS = []
WARNINGS = []
STRICT_MODE = False


def warn_or_err(msg):
    if STRICT_MODE:
        err(msg)
    else:
        warn(msg)


def err(msg):
    ERRORS.append(msg)
    print(f"  FAIL: {msg}")


def warn(msg):
    WARNINGS.append(msg)
    print(f"  WARN: {msg}")


def ok(msg):
    print(f"  OK:   {msg}")


def check_no_bom():
    print("\n[1] BOM check")
    extensions = ['.py', '.js', '.css', '.html', '.md', '.toml', '.yml', '.yaml']
    found = False
    for path in ROOT.rglob('*'):
        if any(part.startswith('.') or part == '__pycache__' for part in path.parts):
            continue
        if path.suffix not in extensions:
            continue
        try:
            raw = path.read_bytes()
            if raw[:3] == b'\xef\xbb\xbf':
                err(f"BOM found: {path.relative_to(ROOT)}")
                found = True
        except Exception:
            pass
    if not found:
        ok("No BOM in any source file")


def check_no_double_crlf():
    print("\n[2] Line ending check")
    found = False
    for path in ROOT.glob('docs/*.js'):
        raw = path.read_bytes()
        if b'\r\r\n' in raw:
            err(f"Double CRLF in: {path.relative_to(ROOT)}")
            found = True
    if not found:
        ok("No double CRLF in JS files")


def check_no_mojibake():
    print("\n[3] Mojibake check")
    BAD = ['\u00e2\u20ac', '\u00f0\u0178', '\u00e2\u0152', '\u00e2\u02dc']
    files = list(ROOT.glob('docs/*.js')) + list(ROOT.glob('docs/*.css')) + [ROOT / 'docs' / 'playground.html']
    found = False
    for path in files:
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
            hits = sum(text.count(b) for b in BAD)
            if hits:
                err(f"Mojibake ({hits} hits) in: {path.relative_to(ROOT)}")
                found = True
        except Exception as e:
            warn(f"Could not read {path.relative_to(ROOT)}: {e}")
    if not found:
        ok("No mojibake in playground files")


def check_version_consistency():
    print("\n[4] Version consistency")
    try:
        import tomllib as _toml
    except ModuleNotFoundError:
        try:
            import tomli as _toml
        except ModuleNotFoundError:
            _toml = None

    toml_path = ROOT / 'pyproject.toml'
    if _toml is not None:
        try:
            with open(toml_path, 'rb') as f:
                toml_version = _toml.load(f)['project']['version']
        except Exception as e:
            err(f"Cannot read version from pyproject.toml: {e}")
            return
    else:
        # Fallback: regex extract version = "X.Y.Z"
        text = toml_path.read_text(encoding='utf-8')
        m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        if m:
            toml_version = m.group(1)
        else:
            err("Cannot read version from pyproject.toml (no tomllib/tomli)")
            return
    ok(f"pyproject.toml version: {toml_version}")

    init = (ROOT / 'numclassify' / '__init__.py').read_text(encoding='utf-8')
    hardcoded = [h for h in re.findall(r'__version__\s*=\s*["\'][\d.]+["\']', init)
                 if '0.0.0' not in h]
    if hardcoded:
        err(f"Hardcoded __version__ in __init__.py: {hardcoded}")
    else:
        ok("__init__.py uses importlib.metadata for version (fallback 0.0.0 ignored)")

    html_path = ROOT / 'docs' / 'playground.html'
    if html_path.exists():
        html = html_path.read_text(encoding='utf-8')
        stale_counts = re.findall(r'(\d{4}\+)\s+named', html)
        for count in stale_counts:
            if count != '2140+':
                err(f"Stale count in playground.html subtitle: '{count}' (expected '2140+')")
        if '2140+' in html:
            ok("playground.html subtitle count: 2140+")

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    readme_versions = re.findall(r"What's new in v([\d.]+)", readme)
    if readme_versions:
        if readme_versions[0] != toml_version:
            warn_or_err(f"README 'What's new' says v{readme_versions[0]}, pyproject says v{toml_version}")
        else:
            ok(f"README 'What's new' matches version: v{toml_version}")

    changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    if f'[{toml_version}]' not in changelog:
        err(f"CHANGELOG.md missing entry for [{toml_version}]")
    else:
        ok(f"CHANGELOG.md has entry for [{toml_version}]")


def check_no_emoji_in_js():
    print("\n[5] Emoji check in JS files")
    EMOJI_RANGES = [(0x1F300, 0x1FFFF), (0x2600, 0x27BF), (0x1F000, 0x1F02F)]

    def has_emoji(text):
        return any(any(lo <= ord(c) <= hi for lo, hi in EMOJI_RANGES) for c in text)

    found = False
    for path in ROOT.glob('docs/*.js'):
        text = path.read_text(encoding='utf-8', errors='replace')
        if has_emoji(text):
            err(f"Emoji found in JS file: {path.relative_to(ROOT)}")
            found = True
    if not found:
        ok("No emoji in JS files")


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
            'why', 'why_hidden', 'practice_set', 'PRACTICE_TYPES', 'property_info', 'find', 'get_exam_types',
            'similar_numbers', 'specialness_percentile',
        }
        leaked = set(public) - ALLOWED
        if leaked:
            err(f"Leaked public names: {sorted(leaked)}")
        else:
            ok(f"Public API has {len(public)} names, no leaks")
    except Exception as e:
        warn(f"Could not check public API: {e}")


def check_practice_types():
    print("\n[9] PRACTICE_TYPES drift check")
    try:
        sys.path.insert(0, str(ROOT))
        from numclassify._registry import REGISTRY, _normalize
        from numclassify import PRACTICE_TYPES

        missing = [t for t in PRACTICE_TYPES if _normalize(t) not in REGISTRY]
        if missing:
            err(f"PRACTICE_TYPES references types not in REGISTRY: {missing}")
        else:
            ok(f"All {len(PRACTICE_TYPES)} PRACTICE_TYPES resolve correctly")

        import numclassify as nc
        import re
        leaked = []
        for t in PRACTICE_TYPES:
            type_word = t.split()[0].lower()
            pattern = re.compile(rf'\bis\s+(?:not\s+)?{re.escape(type_word)}\b', re.IGNORECASE)
            for n in [6, 7]:
                try:
                    hidden = nc.why_hidden(t, n)
                except RuntimeError:
                    continue
                if pattern.search(hidden):
                    leaked.append(f"{t}({n})")
        if leaked:
            err(f"why_hidden() leaks verdict for: {leaked}")
        else:
            ok("why_hidden() spot-check: no verdict leaks in PRACTICE_TYPES")
    except Exception as e:
        warn(f"Could not check PRACTICE_TYPES: {e}")


def check_no_em_dash_in_source():
    print("\n[10] Em dash check (comments, YAML, docs)")
    EXTENSIONS = ['.yml', '.yaml', '.md']
    found = False
    for path in ROOT.rglob('*'):
        if any(part.startswith('.') or part == '__pycache__' or part == 'node_modules' for part in path.parts):
            continue
        if path.suffix not in EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        in_code_block = False
        for i, line in enumerate(text.split('\n'), 1):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if '\u2014' in line or ' -- ' in line and path.suffix in ('.yml', '.yaml'):
                if '\u2014' in line:
                    warn(f"Em dash in {path.relative_to(ROOT)}:{i}")
                    found = True
    if not found:
        ok("No em dashes found in YAML/docs (outside code blocks)")


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
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode != 0:
                err(f"CLI failed: {' '.join(cmd)}\n    stderr: {result.stderr[:200]}")
            else:
                ok(f"CLI OK: {' '.join(cmd)}")
        except FileNotFoundError:
            err(f"CLI command not found: {' '.join(cmd)} (is the package installed?)")
        except subprocess.TimeoutExpired:
            err(f"CLI timed out: {' '.join(cmd)}")


def check_no_broken_imports():
    print("\n[12] Broken import check")
    import ast
    import importlib

    found = False
    for path in ROOT.rglob('numclassify/**/*.py'):
        if '__pycache__' in str(path):
            continue
        try:
            src = path.read_text(encoding='utf-8')
            tree = ast.parse(src, filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as e:
            warn(f"Could not parse {path.relative_to(ROOT)}: {e}")
            continue

        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or not node.module:
                continue
            if node.level > 0:
                module_name = f"numclassify.{node.module}" if not node.module.startswith('numclassify') else node.module
            else:
                module_name = node.module
            if not module_name.startswith('numclassify'):
                continue
            for alias in node.names:
                name = alias.name
                if name == '*':
                    continue
                try:
                    mod = importlib.import_module(module_name)
                    if not hasattr(mod, name):
                        err(
                            f"{path.relative_to(ROOT)}:{node.lineno}: "
                            f"imports '{name}' from '{module_name}' but it does not exist there"
                        )
                        found = True
                except ImportError as e:
                    warn(f"{path.relative_to(ROOT)}:{node.lineno}: could not import '{module_name}' to verify: {e}")
    if not found:
        ok("No broken internal imports found")


def check_coverage_badge_freshness():
    if not STRICT_MODE:
        return
    print("\n[11] Coverage badge freshness (strict mode only)")
    import json
    import re
    cov_path = ROOT / 'coverage.json'
    if not cov_path.exists():
        err("coverage.json not found. Run 'pytest --cov=numclassify --cov-report=json' before --strict check.")
        return
    try:
        data = json.loads(cov_path.read_text(encoding='utf-8'))
        actual_pct = int(data['totals']['percent_covered'])
    except (KeyError, json.JSONDecodeError) as e:
        err(f"Could not parse coverage.json: {e}")
        return

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    match = re.search(r'coverage-(\d+)%25-', readme)
    if not match:
        err("Could not find coverage badge pattern in README.md")
        return
    badge_pct = int(match.group(1))
    if abs(badge_pct - actual_pct) > 5:
        err(f"README coverage badge says {badge_pct}%, actual coverage is {actual_pct}%. Run tools/generate_docs.py before release.")
    else:
        ok(f"Coverage badge matches actual coverage: {actual_pct}%")


def main():
    global STRICT_MODE
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--fast', action='store_true', help='Skip slow checks')
    parser.add_argument('--strict', action='store_true', help='Treat drift warnings as hard failures (use before release)')
    args = parser.parse_args()
    STRICT_MODE = args.strict

    print("=" * 60)
    print(f"numclassify repo health check{' (STRICT)' if STRICT_MODE else ''}")
    print("=" * 60)

    check_no_bom()
    check_no_double_crlf()
    check_no_mojibake()
    check_version_consistency()
    check_no_emoji_in_js()
    check_registry_count()
    check_no_leaked_names()
    check_no_broken_imports()
    check_practice_types()
    check_no_em_dash_in_source()
    check_coverage_badge_freshness()
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
