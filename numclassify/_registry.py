"""
numclassify._registry
~~~~~~~~~~~~~~~~~~~~~
Central registry for all number-classification functions.

Every classification function is stored as a :class:`NumberType` entry keyed by
a normalised name (lowercase, spaces replaced with underscores).  The
:func:`register` decorator factory is the sole public mechanism for adding
entries; it is used by every ``_core`` submodule.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Union


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class NumberType:
    """Metadata and implementation for a single number classification.

    Parameters
    ----------
    name:
        Human-readable name, e.g. ``"Prime"``.
    category:
        Broad category, e.g. ``"primes"`` or ``"digital"``.
    func:
        A callable ``(n: int) -> bool`` that returns ``True`` when *n*
        satisfies the classification.
    oeis:
        Optional OEIS sequence identifier, e.g. ``"A000040"``.
    description:
        One-line mathematical description.
    aliases:
        Alternative names under which this entry is also registered.
    """

    name: str
    category: str
    func: Callable[[int], bool]
    oeis: str = ""
    description: str = ""
    aliases: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Global registry
# ---------------------------------------------------------------------------

REGISTRY: Dict[str, NumberType] = {}
_REGISTRY_LOCK = threading.Lock()


def _normalize(name: str) -> str:
    """Return *name* normalised to a registry key.

    >>> _normalize("Twin Prime")
    'twin_prime'
    """
    return name.strip().lower().replace(" ", "_").replace("-", "_")


# ---------------------------------------------------------------------------
# @register decorator factory
# ---------------------------------------------------------------------------

def register(
    name: str,
    category: str,
    oeis: str = "",
    description: str = "",
    aliases: Optional[List[str]] = None,
) -> Callable[[Callable[[int], bool]], Callable[[int], bool]]:
    """Decorator factory that registers a classification function.

    The function is stored under the normalised *name* **and** under every
    entry in *aliases*.  Registration is thread-safe.

    Parameters
    ----------
    name:
        Canonical name for the number type.
    category:
        Broad category grouping (used in the printed report).
    oeis:
        OEIS sequence identifier (optional).
    description:
        Short mathematical description (optional).
    aliases:
        List of alternative lookup names (optional).

    Returns
    -------
    decorator:
        A transparent decorator — the original function is returned unchanged
        so it can still be called directly.

    Example
    -------
    >>> @register(name="Even", category="basic", description="Divisible by 2")
    ... def is_even(n: int) -> bool:
    ...     return n % 2 == 0
    >>> "even" in REGISTRY
    True
    """
    _aliases: List[str] = aliases if aliases is not None else []

    def decorator(func: Callable[[int], bool]) -> Callable[[int], bool]:
        entry = NumberType(
            name=name,
            category=category,
            func=func,
            oeis=oeis,
            description=description,
            aliases=_aliases,
        )
        key = _normalize(name)
        with _REGISTRY_LOCK:
            REGISTRY[key] = entry
            for alias in _aliases:
                REGISTRY[_normalize(alias)] = entry
        return func

    return decorator


# ---------------------------------------------------------------------------
# Public query helpers
# ---------------------------------------------------------------------------

def _resolve(func_or_name: Union[Callable[[int], bool], str]) -> Callable[[int], bool]:
    """Return the callable for *func_or_name*.

    Accepts either a raw callable or a string name (normalised before lookup).

    Raises
    ------
    KeyError
        If the string name is not found in :data:`REGISTRY`.
    TypeError
        If *func_or_name* is neither a string nor a callable.
    """
    if callable(func_or_name):
        return func_or_name  # type: ignore[return-value]
    if isinstance(func_or_name, str):
        key = _normalize(func_or_name)
        if key not in REGISTRY:
            raise KeyError(
                f"No number type named {func_or_name!r} is registered. "
                f"Available: {sorted(REGISTRY)}"
            )
        return REGISTRY[key].func
    raise TypeError(
        f"Expected a callable or a type name string, got {type(func_or_name)!r}"
    )


def get_all_properties(n: int) -> Dict[str, bool]:
    """Run every registered classification function against *n*.

    Parameters
    ----------
    n:
        The integer to classify.

    Returns
    -------
    dict
        Mapping of canonical name → bool for **every** registered type.

    Example
    -------
    >>> result = get_all_properties(6)
    >>> isinstance(result, dict)
    True
    """
    with _REGISTRY_LOCK:
        snapshot = dict(REGISTRY)
    result: Dict[str, bool] = {}
    for key, entry in snapshot.items():
        if key == _normalize(entry.name):          # skip alias duplicates
            try:
                result[entry.name] = bool(entry.func(n))
            except Exception:
                result[entry.name] = False
    return result


def get_true_properties(n: int) -> Dict[str, bool]:
    """Return only the properties of *n* that are ``True``.

    Parameters
    ----------
    n:
        The integer to classify.

    Returns
    -------
    dict
        Subset of :func:`get_all_properties` where value is ``True``.

    Example
    -------
    >>> all(get_true_properties(28).values())
    True
    """
    return {k: v for k, v in get_all_properties(n).items() if v}


def count_properties(n: int) -> int:
    """Return the number of registered types satisfied by *n*.

    Parameters
    ----------
    n:
        The integer to classify.

    Returns
    -------
    int
        Count of ``True`` entries in :func:`get_all_properties`.

    Example
    -------
    >>> count_properties(2) >= 1
    True
    """
    return sum(1 for v in get_all_properties(n).values() if v)


def print_properties(n: int) -> None:
    """Print a formatted classification report for *n*.

    The report uses box-drawing characters and is divided into three
    sections: TRUE (properties satisfied), FALSE (properties not
    satisfied), and a summary line.

    Parameters
    ----------
    n:
        The integer to classify.

    Example
    -------
    >>> print_properties(153)  # doctest: +SKIP
    ┌─────────────────────────────────────────┐
    │  Classification report for n = 153      │
    ...
    """
    props = get_all_properties(n)
    true_props = {k: v for k, v in props.items() if v}
    false_props = {k: v for k, v in props.items() if not v}

    width = 50
    border = "─" * (width - 2)

    print(f"┌{border}┐")
    title = f"  Classification report for n = {n}"
    print(f"│{title:<{width - 2}}│")
    print(f"├{border}┤")

    if true_props:
        header = "  ✓ TRUE"
        print(f"│{header:<{width - 2}}│")
        for name in sorted(true_props):
            line = f"    • {name}"
            print(f"│{line:<{width - 2}}│")
    else:
        line = "  (no properties satisfied)"
        print(f"│{line:<{width - 2}}│")

    print(f"├{border}┤")

    if false_props:
        header = "  ✗ FALSE"
        print(f"│{header:<{width - 2}}│")
        for name in sorted(false_props):
            line = f"    • {name}"
            print(f"│{line:<{width - 2}}│")

    print(f"├{border}┤")
    summary = f"  Total TRUE: {len(true_props)} / {len(props)}"
    print(f"│{summary:<{width - 2}}│")
    print(f"└{border}┘")


# ---------------------------------------------------------------------------
# Range search helpers
# ---------------------------------------------------------------------------

def find_in_range(
    func_or_name: Union[Callable[[int], bool], str],
    start: int,
    end: int,
) -> List[int]:
    """Return all integers in ``[start, end]`` satisfying *func_or_name*.

    Parameters
    ----------
    func_or_name:
        Either a callable ``(int) -> bool`` or a registered type name string.
    start:
        Lower bound (inclusive).
    end:
        Upper bound (inclusive).

    Returns
    -------
    list[int]
        Sorted list of matching integers.

    Example
    -------
    >>> from numclassify._core.primes import is_prime
    >>> find_in_range(is_prime, 1, 10)
    [2, 3, 5, 7]
    """
    func = _resolve(func_or_name)
    return [n for n in range(start, end + 1) if func(n)]


def find_all_in_range(
    funcs_or_names: List[Union[Callable[[int], bool], str]],
    start: int,
    end: int,
) -> List[int]:
    """Return integers in ``[start, end]`` satisfying **all** given types.

    Parameters
    ----------
    funcs_or_names:
        List of callables or registered name strings.
    start:
        Lower bound (inclusive).
    end:
        Upper bound (inclusive).

    Returns
    -------
    list[int]
        Sorted list of integers satisfying every predicate.

    Example
    -------
    >>> find_all_in_range(["prime", "palindrome"], 1, 200)
    [2, 3, 5, 7, 11]
    """
    funcs = [_resolve(f) for f in funcs_or_names]
    return [n for n in range(start, end + 1) if all(f(n) for f in funcs)]


def find_any_in_range(
    funcs_or_names: List[Union[Callable[[int], bool], str]],
    start: int,
    end: int,
) -> List[int]:
    """Return integers in ``[start, end]`` satisfying **at least one** type.

    Parameters
    ----------
    funcs_or_names:
        List of callables or registered name strings.
    start:
        Lower bound (inclusive).
    end:
        Upper bound (inclusive).

    Returns
    -------
    list[int]
        Sorted list of integers satisfying at least one predicate.

    Example
    -------
    >>> find_any_in_range(["prime", "palindrome"], 1, 15)
    [2, 3, 5, 7, 11, 11, 13]
    """
    funcs = [_resolve(f) for f in funcs_or_names]
    return [n for n in range(start, end + 1) if any(f(n) for f in funcs)]


def most_special_in_range(start: int, end: int) -> int:
    """Return the integer in ``[start, end]`` with the most ``True`` properties.

    Ties are broken by returning the smallest such integer.

    Parameters
    ----------
    start:
        Lower bound (inclusive).
    end:
        Upper bound (inclusive).

    Returns
    -------
    int
        The most-classified integer in the range.

    Example
    -------
    >>> most_special_in_range(1, 10) >= 1
    True
    """
    best_n = start
    best_count = -1
    for n in range(start, end + 1):
        c = count_properties(n)
        if c > best_count:
            best_count = c
            best_n = n
    return best_n
