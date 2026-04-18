"""
numclassify.cli
~~~~~~~~~~~~~~~
Command-line interface for numclassify.

Entry point: ``numclassify`` (configured in pyproject.toml).

Commands
--------
check <number> [--full] [--json]
    Classify a single number.

range <start> <end> [--filter <name>] [--json]
    Inspect a range of integers.

find <type_name> [--limit N] [--json]
    Find the first N integers satisfying a named type.

info <type_name>
    Show registry metadata for a type.

list [--category <cat>]
    List all registered types, optionally filtered by category.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, NoReturn, Optional, Tuple


# ---------------------------------------------------------------------------
# Terminal colour / Unicode helpers
# ---------------------------------------------------------------------------
# _USE_COLOR and _USE_UNICODE are set to False at import time; main() may
# flip them to True after reconfiguring stdout.

_USE_COLOR:   bool = False
_USE_UNICODE: bool = False


def _c(text: str, *codes: int) -> str:
    """Wrap *text* in ANSI escape codes when stdout is a colour TTY."""
    if not _USE_COLOR:
        return text
    seq = ";".join(str(c) for c in codes)
    return f"\033[{seq}m{text}\033[0m"


def _bold(text: str) -> str:
    return _c(text, 1)


def _green(text: str) -> str:
    return _c(text, 32)


def _red(text: str) -> str:
    return _c(text, 31)


def _yellow(text: str) -> str:
    return _c(text, 33)


def _cyan(text: str) -> str:
    return _c(text, 36)


def _check_mark() -> str:
    """Return ✓ on Unicode-capable TTYs, plain [YES] otherwise."""
    return "✓" if _USE_UNICODE else "[YES]"


def _rule(width: int) -> str:
    """Return a horizontal rule of *width* chars."""
    return ("─" if _USE_UNICODE else "-") * width


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def _die(msg: str, code: int = 1) -> NoReturn:
    """Print *msg* to stderr and exit with *code*."""
    print(_red(f"Error: {msg}"), file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# Lazy imports
# ---------------------------------------------------------------------------

def _lazy_import() -> Tuple[Any, Dict[str, Any], Any]:
    """Import numclassify lazily so CLI starts quickly and errors are clean."""
    try:
        import numclassify as nc
        from numclassify._registry import REGISTRY, find_in_range
        return nc, REGISTRY, find_in_range
    except Exception as exc:
        _die(f"Failed to import numclassify: {exc}")


def _normalize(name: str) -> str:
    """Normalise a type name: lower-case, spaces → underscores."""
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def _resolve_type(name: str, registry: Dict[str, Any]) -> str:
    """Return the registry key for *name* or call _die."""
    key = _normalize(name)
    if key not in registry:
        _die(
            f"Unknown type: '{name}'. "
            f"Use 'numclassify list' to see all types."
        )
    return key


# ---------------------------------------------------------------------------
# Computed extras for `check`
# ---------------------------------------------------------------------------

def _computed_extras(n: int) -> Dict[str, int]:
    """Return a small dict of directly computed values for display."""
    try:
        from numclassify.digital import digit_sum, digital_root
        ds = digit_sum(n)
        dr = digital_root(n)
    except Exception:
        ds = sum(int(d) for d in str(abs(n))) if n != 0 else 0
        dr = ds  # fallback
    try:
        from numclassify.divisors import count_divisors
        nd = count_divisors(n)
    except Exception:
        nd = sum(1 for i in range(1, abs(n) + 1) if n % i == 0) if n != 0 else 0
    return {"digit_sum": ds, "digital_root": dr, "num_divisors": nd}


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------

def cmd_check(args: argparse.Namespace) -> None:
    """Handle: numclassify check <number> [--full] [--json]."""
    nc, registry, _ = _lazy_import()

    try:
        n = int(args.number)
    except ValueError:
        _die(f"'{args.number}' is not a valid integer.")

    if args.json:
        true_props = nc.get_true_properties(n)
        false_props = [
            k for k in registry
            if k not in set(_normalize(p) for p in true_props)
        ]
        payload = {
            "number": n,
            "true_properties": sorted(true_props),
            "false_properties": sorted(false_props),
        }
        print(json.dumps(payload, indent=2))
        return

    if args.full:
        nc.print_properties(n)
        return

    # Default: clean summary
    true_props = nc.get_true_properties(n)
    header = f"Properties of {n}"
    print(_bold(header))
    print(_bold(_rule(len(header))))

    if not true_props:
        print("  (no registered properties satisfied)")
    else:
        for name in sorted(true_props):
            print(f"  {_green(_check_mark())} {name}")

    # Computed extras
    extras = _computed_extras(n)
    extra_str = "  ".join(f"{k}={v}" for k, v in extras.items())
    print()
    print(_cyan(f"Computed:  {extra_str}"))


def cmd_range(args: argparse.Namespace) -> None:
    """Handle: numclassify range <start> <end> [--filter <name>] [--json]."""
    nc, registry, find_in_range = _lazy_import()

    try:
        start = int(args.start)
        end = int(args.end)
    except ValueError:
        _die("start and end must be integers.")

    if start > end:
        _die("start must be ≤ end.")

    span = end - start + 1
    if span > 100_000:
        print(
            _yellow(f"Warning: range has {span} numbers — this may be slow."),
            file=sys.stderr,
        )

    if args.filter:
        key = _resolve_type(args.filter, registry)
        func = registry[key].func
        results = find_in_range(func, start, end)

        if args.json:
            print(json.dumps(results))
            return

        label = registry[key].name if hasattr(registry[key], "name") else args.filter
        if results:
            print(
                _bold(f"{label} in range {start}..{end}:")
                + f" {results}"
            )
        else:
            print(f"No numbers in [{start}, {end}] satisfy '{args.filter}'.")
    else:
        rows: List[Dict[str, Any]] = []
        for n in range(start, end + 1):
            c = nc.count_properties(n)
            rows.append({"number": n, "property_count": c})

        if args.json:
            print(json.dumps(rows, indent=2))
            return

        for row in rows:
            n = row["number"]
            c = row["property_count"]
            noun = "property" if c == 1 else "properties"
            print(f"  {n}: {c} {noun}")


def cmd_find(args: argparse.Namespace) -> None:
    """Handle: numclassify find <type_name> [--limit N] [--json]."""
    nc, registry, find_in_range = _lazy_import()

    key = _resolve_type(args.type_name, registry)
    limit = args.limit
    if limit < 1:
        _die("--limit must be a positive integer.")

    func = registry[key].func
    upper = 100_000
    results = find_in_range(func, 0, upper)[:limit]

    label = registry[key].name if hasattr(registry[key], "name") else args.type_name

    if args.json:
        print(json.dumps(results))
        return

    if results:
        print(_bold(f"First {len(results)} {label} numbers:") + f" {results}")
    else:
        print(f"No '{label}' numbers found up to {upper:,}.")


def cmd_info(args: argparse.Namespace) -> None:
    """Handle: numclassify info <type_name>."""
    _, registry, _ = _lazy_import()

    key = _resolve_type(args.type_name, registry)
    entry = registry[key]

    # Gracefully handle registries that use different attribute names
    name        = getattr(entry, "name",        key)
    category    = getattr(entry, "category",    "—")
    oeis        = getattr(entry, "oeis",        None)
    description = getattr(entry, "description", None)
    example     = getattr(entry, "example",     None)

    col_w = 14
    def row(label: str, value: Optional[str]) -> None:
        if value:
            print(f"  {_bold(label + ':'): <{col_w + 8}}  {value}")

    print()
    row("Name",        name)
    row("Category",    str(category).capitalize() if category else None)
    row("OEIS",        oeis)
    row("Description", description)
    row("Example",     str(example) if example else None)
    print()


def cmd_list(args: argparse.Namespace) -> None:
    """Handle: numclassify list [--category <cat>]."""
    _, registry, _ = _lazy_import()

    # Group entries by category
    from collections import defaultdict
    groups: Dict[str, List[str]] = defaultdict(list)

    for key, entry in registry.items():
        cat  = str(getattr(entry, "category", "other")).upper()
        name = getattr(entry, "name", key)
        groups[cat].append(name)

    target_cat: Optional[str] = None
    if args.category:
        # Accept any capitalisation; also try appending S so "prime" → "PRIMES"
        needle = args.category.upper().rstrip("S")
        target_cat = next(
            (k for k in groups if k.upper().rstrip("S") == needle),
            None,
        )
        if target_cat is None:
            available = ", ".join(sorted(groups.keys()))
            _die(
                f"Unknown category '{args.category}'. "
                f"Available: {available}"
            )

    for cat in sorted(groups.keys()):
        if target_cat and cat != target_cat:
            continue
        names = sorted(groups[cat])
        print(_bold(f"\n{cat} ({len(names)} types)"))
        # Print names in a wrapped paragraph style
        line = "  "
        for i, n in enumerate(names):
            chunk = n + (", " if i < len(names) - 1 else "")
            if len(line) + len(chunk) > 78:
                print(line.rstrip(", "))
                line = "  " + chunk
            else:
                line += chunk
        if line.strip():
            print(line)

    print()


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="numclassify",
        description="Number classification toolkit — 3000+ number types.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # -- check ---------------------------------------------------------------
    p_check = sub.add_parser(
        "check",
        help="Classify a single number.",
        description=(
            "Classify a single integer and print all satisfied properties.\n\n"
            "Examples:\n"
            "  numclassify check 153\n"
            "  numclassify check 153 --full\n"
            "  numclassify check 153 --json"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_check.add_argument("number", help="Integer to classify.")
    p_check.add_argument(
        "--full",
        action="store_true",
        help="Print full formatted report (calls print_properties).",
    )
    p_check.add_argument(
        "--json",
        action="store_true",
        help="Output true and false properties as JSON.",
    )
    p_check.set_defaults(func=cmd_check)

    # -- range ---------------------------------------------------------------
    p_range = sub.add_parser(
        "range",
        help="Inspect a range of integers.",
        description=(
            "Show property counts or filtered matches for a range.\n\n"
            "Examples:\n"
            "  numclassify range 1 20\n"
            "  numclassify range 1 100 --filter prime\n"
            "  numclassify range 1 50  --filter prime --json"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_range.add_argument("start", help="Start of range (inclusive).")
    p_range.add_argument("end",   help="End of range (inclusive).")
    p_range.add_argument(
        "--filter",
        metavar="TYPE",
        default=None,
        help="Show only numbers satisfying this type name.",
    )
    p_range.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON.",
    )
    p_range.set_defaults(func=cmd_range)

    # -- find ----------------------------------------------------------------
    p_find = sub.add_parser(
        "find",
        help="Find the first N numbers of a given type.",
        description=(
            "Search up to 100 000 for numbers satisfying a named type.\n\n"
            "Examples:\n"
            "  numclassify find armstrong\n"
            "  numclassify find 'twin prime' --limit 10\n"
            "  numclassify find mersenne_prime --json"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_find.add_argument("type_name", help="Registered type name.")
    p_find.add_argument(
        "--limit",
        type=int,
        default=20,
        metavar="N",
        help="How many numbers to find (default: 20).",
    )
    p_find.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON array.",
    )
    p_find.set_defaults(func=cmd_find)

    # -- info ----------------------------------------------------------------
    p_info = sub.add_parser(
        "info",
        help="Show metadata for a registered type.",
        description=(
            "Display name, category, OEIS reference, and description.\n\n"
            "Examples:\n"
            "  numclassify info armstrong\n"
            "  numclassify info 'twin prime'"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_info.add_argument("type_name", help="Registered type name.")
    p_info.set_defaults(func=cmd_info)

    # -- list ----------------------------------------------------------------
    p_list = sub.add_parser(
        "list",
        help="List all registered types, grouped by category.",
        description=(
            "Print every registered type name, grouped by category.\n\n"
            "Examples:\n"
            "  numclassify list\n"
            "  numclassify list --category prime"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_list.add_argument(
        "--category",
        metavar="CAT",
        default=None,
        help="Show only this category.",
    )
    p_list.set_defaults(func=cmd_list)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the ``numclassify`` CLI command."""
    import io

    global _USE_COLOR, _USE_UNICODE  # noqa: PLW0603

    # ------------------------------------------------------------------
    # 1. Reconfigure stdout to UTF-8 so Unicode chars never crash on
    #    Windows cp1252 / latin-1 terminals or when output is piped.
    # ------------------------------------------------------------------
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    elif hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )

    # ------------------------------------------------------------------
    # 2. Enable colour + Unicode only when writing to a real terminal.
    #    Subprocesses/pipes get plain ASCII — no ✓, no ─, no ANSI codes.
    # ------------------------------------------------------------------
    if sys.stdout.isatty():
        _USE_COLOR   = True
        _USE_UNICODE = True

    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        print()          # clean newline
        sys.exit(0)
    except Exception as exc:
        _die(str(exc))


if __name__ == "__main__":
    main()
