"""
numclassify.cli
~~~~~~~~~~~~~~~
Command-line interface for numclassify.

Entry point: ``numclassify`` (configured in pyproject.toml).

Commands
--------
check <number> [--full] [--json]
    Classify a single number.

range <start> <end> [--filter <name>]
    Inspect a range of integers.

find <type_name> [--limit N]
    Find the first N integers satisfying a named type.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import NoReturn


def _die(msg: str, code: int = 1) -> NoReturn:
    """Print *msg* to stderr and exit with *code*."""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def _lazy_import():
    """Import numclassify lazily so CLI starts quickly and errors are clean."""
    try:
        import numclassify as nc
        from numclassify._registry import REGISTRY, find_in_range
        return nc, REGISTRY, find_in_range
    except Exception as exc:  # pragma: no cover
        _die(f"Failed to import numclassify: {exc}")


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------

def cmd_check(args: argparse.Namespace) -> None:
    """Handle: numclassify check <number> [--full] [--json]."""
    nc, _registry, _fir = _lazy_import()

    try:
        n = int(args.number)
    except ValueError:
        _die(f"{args.number!r} is not a valid integer.")

    if args.json:
        props = nc.get_all_properties(n)
        print(json.dumps(props, indent=2))
    elif args.full:
        nc.print_properties(n)
    else:
        props = nc.get_true_properties(n)
        if not props:
            print(f"  n = {n}: (no registered properties satisfied)")
        else:
            print(f"  n = {n} is:")
            for name in sorted(props):
                print(f"    • {name}")


def cmd_range(args: argparse.Namespace) -> None:
    """Handle: numclassify range <start> <end> [--filter <name>]."""
    nc, registry, find_in_range = _lazy_import()

    try:
        start = int(args.start)
        end = int(args.end)
    except ValueError:
        _die("start and end must be integers.")

    if start > end:
        _die("start must be ≤ end.")

    if args.filter:
        from numclassify._registry import _normalize
        key = _normalize(args.filter)
        if key not in registry:
            _die(
                f"Unknown type name {args.filter!r}. "
                f"Use 'numclassify check 1 --full' to see available types."
            )
        func = registry[key].func
        results = find_in_range(func, start, end)
        if results:
            print(f"  Numbers in [{start}, {end}] satisfying '{args.filter}':")
            print("  " + ", ".join(str(x) for x in results))
        else:
            print(f"  No numbers in [{start}, {end}] satisfy '{args.filter}'.")
    else:
        print(f"  Property counts for n in [{start}, {end}]:")
        for n in range(start, end + 1):
            c = nc.count_properties(n)
            print(f"    n={n:>6}  →  {c} propert{'y' if c == 1 else 'ies'}")


def cmd_find(args: argparse.Namespace) -> None:
    """Handle: numclassify find <type_name> [--limit N]."""
    nc, registry, find_in_range = _lazy_import()

    from numclassify._registry import _normalize
    key = _normalize(args.type_name)
    if key not in registry:
        _die(
            f"Unknown type name {args.type_name!r}. "
            f"Available types can be seen with: numclassify check 1 --full"
        )

    limit = args.limit
    func = registry[key].func
    upper = max(limit * limit * 10, 10_000)
    results = find_in_range(func, 0, upper)[:limit]

    if results:
        print(f"  First {len(results)} numbers satisfying '{args.type_name}':")
        print("  " + ", ".join(str(x) for x in results))
    else:
        print(f"  No numbers satisfying '{args.type_name}' found up to {upper}.")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="numclassify",
        description="Number classification toolkit — 3000+ number types.",
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # -- check --
    p_check = sub.add_parser("check", help="Classify a single number.")
    p_check.add_argument("number", help="Integer to classify.")
    p_check.add_argument(
        "--full", action="store_true", help="Print full formatted report."
    )
    p_check.add_argument(
        "--json", action="store_true", help="Output all properties as JSON."
    )
    p_check.set_defaults(func=cmd_check)

    # -- range --
    p_range = sub.add_parser("range", help="Inspect a range of integers.")
    p_range.add_argument("start", help="Start of range (inclusive).")
    p_range.add_argument("end", help="End of range (inclusive).")
    p_range.add_argument(
        "--filter",
        metavar="NAME",
        default=None,
        help="Show only numbers satisfying this type name.",
    )
    p_range.set_defaults(func=cmd_range)

    # -- find --
    p_find = sub.add_parser(
        "find", help="Find the first N numbers of a given type."
    )
    p_find.add_argument("type_name", help="Registered type name.")
    p_find.add_argument(
        "--limit",
        type=int,
        default=20,
        metavar="N",
        help="How many numbers to find (default: 20).",
    )
    p_find.set_defaults(func=cmd_find)

    return parser


def main() -> None:
    """Entry point for the ``numclassify`` CLI command."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:  # pragma: no cover
        _die(str(exc))


if __name__ == "__main__":
    main()
