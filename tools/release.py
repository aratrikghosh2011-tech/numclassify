#!/usr/bin/env python3
"""
numclassify release automation.

Usage:
    cd C:\\Users\\Aratrik\\Desktop\\numclassify
    python tools/release.py 0.7.0

What it does:
    1. Validates the version string (semver format)
    2. Checks CHANGELOG.md has an entry for the new version
    3. Updates version in pyproject.toml
    4. Updates "What's new in vX.Y.Z" heading in README.md
    5. Removes stale hardcoded data-version from playground.html (if present)
    6. Runs `python tools/generate_docs.py` to refresh category counts
    7. Runs `pytest tests/ -x -q` — aborts if any test fails
    8. Prints the git commands to commit, tag, and push
       (does NOT run git automatically — you confirm and paste)
"""
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent


def err(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def validate_semver(v: str):
    if not re.fullmatch(r'\d+\.\d+\.\d+', v):
        err(f"'{v}' is not a valid semver version (expected X.Y.Z)")


def check_changelog(version: str):
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    pattern = f"## [{version}]"
    if pattern not in changelog:
        err(
            f"CHANGELOG.md has no entry for [{version}].\n"
            f"Add a '## [{version}] - YYYY-MM-DD' section before running this script."
        )
    print(f"  [OK] CHANGELOG.md has entry for [{version}]")


def update_pyproject(version: str):
    path = ROOT / "pyproject.toml"
    content = path.read_text(encoding="utf-8")
    old_version_match = re.search(r'^version = "([^"]+)"', content, re.MULTILINE)
    if not old_version_match:
        err("Could not find 'version = ...' in pyproject.toml")
    old_version = old_version_match.group(1)
    if old_version == version:
        print(f"  [OK] pyproject.toml already at {version}")
        return
    new_content = re.sub(
        r'^version = "[^"]+"',
        f'version = "{version}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    path.write_text(new_content, encoding="utf-8")
    print(f"  [OK] pyproject.toml: {old_version} -> {version}")


def update_readme(version: str):
    path = ROOT / "README.md"
    content = path.read_text(encoding="utf-8")
    new_content = re.sub(
        r"## What's new in v[\d.]+",
        f"## What's new in v{version}",
        content,
        count=1,
    )
    if new_content == content:
        print(f"  [SKIP] README.md: no 'What's new in v...' heading found")
    else:
        path.write_text(new_content, encoding="utf-8")
        print(f"  [OK] README.md: updated 'What's new' heading to v{version}")


def fix_playground_hardcode():
    path = ROOT / "docs" / "playground.html"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    # Remove data-version="..." attribute anywhere it appears
    new_content = re.sub(r' data-version="[^"]*"', '', content)
    if new_content != content:
        path.write_text(new_content, encoding="utf-8")
        print("  [OK] playground.html: removed stale data-version attribute")
    else:
        print("  [OK] playground.html: no data-version attribute found")


def run_generate_docs():
    gen = ROOT / "tools" / "generate_docs.py"
    if not gen.exists():
        print("  [SKIP] tools/generate_docs.py not found")
        return
    result = subprocess.run(
        [sys.executable, str(gen)],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    if result.returncode != 0:
        print(f"  [WARN] generate_docs.py failed:\n{result.stderr}")
    else:
        print("  [OK] generate_docs.py ran successfully")
        print(result.stdout)


def run_health_check():
    print("\nRunning repo health check (strict mode)...")
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q",
         "--cov=numclassify", "--cov-report=json"],
        cwd=str(ROOT)
    )
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check_repo.py"), "--strict"],
        cwd=str(ROOT)
    )
    if result.returncode != 0:
        err("Strict health check failed. Fix issues before releasing -- see errors above.")


def run_tests():
    print("\nRunning tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-x", "-q"],
        cwd=str(ROOT)
    )
    if result.returncode != 0:
        err("Tests failed. Fix before releasing.")
    print("  [OK] All tests pass")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    version = sys.argv[1].lstrip("v")
    validate_semver(version)

    print(f"\nPreparing release v{version}...\n")

    check_changelog(version)
    update_pyproject(version)
    update_readme(version)
    fix_playground_hardcode()
    run_generate_docs()
    run_health_check()
    run_tests()

    print(f"""
Release v{version} is ready. Run these commands:

    git add -A
    git commit -m "chore: release v{version}"
    git tag v{version}
    git push origin main --tags

The OIDC workflow will publish to PyPI automatically on the tag.
""")


if __name__ == "__main__":
    main()
