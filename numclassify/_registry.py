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
    explain:
        Optional callable ``(n: int) -> str`` that returns a human-readable
        explanation of why *n* does or does not satisfy the classification.
    exam_tag:
        If True, this entry is grouped under the "exam_types" pseudo-category
        in CLI listings.  The real *category* field is unchanged.
    """

    name: str
    category: str
    func: Callable[[int], bool]
    oeis: str = ""
    description: str = ""
    aliases: List[str] = field(default_factory=list)
    explain: Optional[Callable[[int], str]] = None
    exam_tag: bool = False


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
    explain: Optional[Callable[[int], str]] = None,
    exam_tag: bool = False,
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
    explain:
        Optional callable ``(n: int) -> str`` returning a human-readable
        explanation for *n*.
    exam_tag:
        If True, this entry is grouped under the "exam_types" pseudo-category
        in CLI listings.

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
            explain=explain,
            exam_tag=exam_tag,
        )
        key = _normalize(name)
        with _REGISTRY_LOCK:
            REGISTRY[key] = entry
            # Also register under the function's __name__ so
            # nc.<func_name>() works via __getattr__ fallback
            REGISTRY[_normalize(func.__name__)] = entry
            for alias in _aliases:
                REGISTRY[_normalize(alias)] = entry
        return func

    return decorator


def get_exam_types() -> list:
    """Return all NumberType entries tagged exam_tag=True, deduplicated by name."""
    seen = set()
    result = []
    for entry in REGISTRY.values():
        if entry.exam_tag and entry.name not in seen:
            seen.add(entry.name)
            result.append(entry)
    return result


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
    [2, 3, 5, 7, 11, 13]
    """
    funcs = [_resolve(f) for f in funcs_or_names]
    return [n for n in range(start, end + 1) if any(f(n) for f in funcs)]


def most_special_in_range(start: int, end: int, verbose: bool = False) -> int:
    """Return the integer in ``[start, end]`` with the most ``True`` properties.

    Ties are broken by returning the smallest such integer.

    Parameters
    ----------
    start:
        Lower bound (inclusive).
    end:
        Upper bound (inclusive).
    verbose : bool, optional
        If True, prints progress every 1000 numbers. Default False.

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
    total = end - start + 1
    for i, n in enumerate(range(start, end + 1)):
        c = count_properties(n)
        if c > best_count:
            best_count = c
            best_n = n
        if verbose and (i + 1) % 1000 == 0:
            pct = (i + 1) / total * 100
            print(f"  most_special_in_range: {i+1}/{total} ({pct:.1f}%) — best so far: {best_n} ({best_count} props)")
    return best_n


# ---------------------------------------------------------------------------
# v0.6.0 — Discoverability API
# ---------------------------------------------------------------------------

def similar_numbers(
    n: int,
    top_k: int = 5,
    search_range: int = 500,
) -> list:
    """
    Return the top_k integers near n most similar to it by shared properties.

    Similarity = Jaccard index on the set of True handcrafted properties
    (excludes figurate types to avoid noise).

    Returns list of dicts: [{number, similarity, shared_properties}]

    May be slow for large search_range; default 500 is reasonable.
    """
    def handcrafted_props(x: int) -> frozenset:
        result = set()
        with _REGISTRY_LOCK:
            snapshot = dict(REGISTRY)
        for key, entry in snapshot.items():
            if key != _normalize(entry.name):
                continue
            cat = entry.category.lower().replace(' ', '_')
            if 'figurate' in cat or 'polygonal' in cat or 'centered' in cat:
                continue
            try:
                if entry.func(x):
                    result.add(entry.name)
            except Exception:
                pass
        return frozenset(result)

    n_props = handcrafted_props(n)
    if not n_props:
        return []

    candidates = []
    lo = max(1, n - search_range)
    hi = n + search_range

    for x in range(lo, hi + 1):
        if x == n:
            continue
        x_props = handcrafted_props(x)
        union = n_props | x_props
        if not union:
            continue
        jaccard = len(n_props & x_props) / len(union)
        if jaccard > 0:
            candidates.append({
                "number": x,
                "similarity": round(jaccard, 4),
                "shared_properties": sorted(n_props & x_props),
            })

    candidates.sort(key=lambda d: (-d["similarity"], abs(d["number"] - n)))
    return candidates[:top_k]


def specialness_percentile(n: int, sample_size: int = 1000) -> float:
    """
    Return the percentile rank of n's notable_score vs a random sample.

    Returns a float in [0, 100]: 95.0 means n scores higher than 95% of random integers.
    """
    import random
    from numclassify import classify

    n_score = classify(n)["notable_score"]
    sample = random.sample(range(1, 10001), min(sample_size, 10000))
    scores = [classify(x)["notable_score"] for x in sample]
    rank = sum(1 for s in scores if s < n_score)
    return round(100 * rank / len(scores), 1)


# ---------------------------------------------------------------------------
# v0.8.0 — Practice / Quiz mode
# ---------------------------------------------------------------------------

PRACTICE_TYPES = [
    "Armstrong", "Perfect", "Prime", "Composite", "Harshad", "Niven",
    "Palindromic Prime", "Circular Prime", "Emirp", "Fibonacci", "Buzz", "Spy",
    "Automorphic", "Neon", "Duck", "Disarium", "Kaprekar", "Happy", "Sunny",
    "Strong", "Twin Prime", "Abundant", "Deficient",
]
"""
Types included in practice/quiz mode. Restricted to the ICSE Class 10
Computer Applications syllabus so a beginner isn't quizzed on advanced
research-level types (Wolstenholme primes, Wall-Sun-Sun primes, etc).
Verified against REGISTRY before use -- all 23 names resolve correctly.
"""

PRACTICE_RANGE = (1, 200)
"""
Fixed range for all practice questions regardless of property. Every
question is answerable by hand (digit sums, small divisor lists, trial
division up to sqrt(200) ~ 14) without a calculator. Not scaled per
property: consistent difficulty framing matters more than exact
per-type difficulty matching at this level.
"""


def practice_set(
    property_name: str,
    count: int = 10,
    seed: int = None,
) -> list:
    """
    Generate a balanced random practice set for a given property.

    Returns count numbers from PRACTICE_RANGE, sampled to be roughly
    50/50 YES/NO for the property (within rounding for small counts or
    rare properties). Raises ValueError if property_name is not in
    PRACTICE_TYPES.

    Args:
        property_name: must be one of PRACTICE_TYPES (case-insensitive,
            resolved the same way as why()/property_info()).
        count: how many questions to generate. Default 10.
        seed: optional RNG seed for a reproducible worksheet (e.g. a
            teacher generating the same quiz for a whole class).

    Returns:
        List of dicts: [{"number": int, "answer": bool}, ...]
        The "answer" key lets CLI/playground score the student's guess
        but should NOT be shown before they answer.
    """
    import random as _random

    key = _normalize(property_name)
    allowed_keys = {_normalize(t) for t in PRACTICE_TYPES}
    if key not in allowed_keys:
        raise ValueError(
            f"'{property_name}' is not available in practice mode. "
            f"Available: {', '.join(PRACTICE_TYPES)}"
        )

    entry = REGISTRY[key]
    func = entry.func
    lo, hi = PRACTICE_RANGE

    rng = _random.Random(seed)

    yes_pool = [n for n in range(lo, hi + 1) if func(n)]
    no_pool = [n for n in range(lo, hi + 1) if not func(n)]

    half = count // 2
    remainder = count - half

    if len(yes_pool) < half:
        chosen_yes = yes_pool
        chosen_no = rng.sample(no_pool, min(count - len(chosen_yes), len(no_pool)))
    elif len(no_pool) < remainder:
        chosen_no = no_pool
        chosen_yes = rng.sample(yes_pool, min(count - len(chosen_no), len(yes_pool)))
    else:
        chosen_yes = rng.sample(yes_pool, half)
        chosen_no = rng.sample(no_pool, remainder)

    combined = [{"number": n, "answer": True} for n in chosen_yes] + \
               [{"number": n, "answer": False} for n in chosen_no]
    rng.shuffle(combined)

    return combined
