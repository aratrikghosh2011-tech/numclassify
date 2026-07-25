#!/usr/bin/env python3
"""
Pre-push CI gate for numclassify.

Runs exactly what CI checks, catches failures before push.
Usage: python tools/pre_push.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
STEPS = []


def step(num: int, total: int, label: str, cmd: list, cwd: str = None) -> None:
    header = f"[{num}/{total}] {label}"
    print()
    print("=" * 60)
    print(f"  {header}")
    print("=" * 60)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=360, cwd=cwd or ROOT)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            print(f"  FAIL: {header}")
            print(f"  Exit code: {result.returncode}")
            sys.exit(1)
        print(f"  PASS: {header}")
    except subprocess.TimeoutExpired:
        print(f"  FAIL: {header} (timed out)")
        sys.exit(1)
    except FileNotFoundError:
        print(f"  FAIL: {header} (command not found: {cmd[0]})")
        sys.exit(1)


def step_cli(num: int, total: int) -> None:
    header = f"[{num}/{total}] CLI smoke check"
    print()
    print("=" * 60)
    print(f"  {header}")
    print("=" * 60)
    python = "numclassify"
    try:
        subprocess.run([python, "--version"], capture_output=True, timeout=5)
    except FileNotFoundError:
        python = f"{sys.executable} -m numclassify"
    # If python is a string with args, we need a list
    if " " in python:
        base = python.split()
    else:
        base = [python]
    commands = [
        base + ["check", "153"],
        base + ["check", "6", "--json"],
        base + ["find", "prime", "--limit", "5"],
        base + ["info", "armstrong"],
        base + ["why", "prime", "7"],
        base + ["compare", "6", "28"],
        base + ["query", "1", "100", "--has", "prime", "--json"],
        base,
    ]
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, cwd=ROOT)
            if result.returncode != 0:
                print(f"  FAIL: {' '.join(cmd)}")
                print(f"  stdout: {result.stdout}")
                print(f"  stderr: {result.stderr}")
                sys.exit(1)
            print(f"  OK: {' '.join(cmd)}")
        except FileNotFoundError:
            print(f"  FAIL: command not found: {' '.join(cmd)} (is the package installed?)")
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print(f"  FAIL: timed out: {' '.join(cmd)}")
            sys.exit(1)
    print(f"  PASS: {header}")


def main() -> None:
    total = 4

    step(1, total, "Running tests with coverage...",
         [sys.executable, "-m", "pytest", "tests/", "-q",
          "--cov=numclassify", "--cov-report=term-missing",
          "--cov-report=json", "--cov-fail-under=75"])

    step(2, total, "Running check_repo.py --strict --fast...",
         [sys.executable, "tools/check_repo.py", "--strict", "--fast"])

    step(3, total, "Running check_repo.py --fast...",
         [sys.executable, "tools/check_repo.py", "--fast"])

    step_cli(4, total)

    print()
    print("=" * 60)
    print("  ALL CHECKS PASSED - safe to push")
    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
