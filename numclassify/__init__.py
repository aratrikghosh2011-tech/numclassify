"""
numclassify
~~~~~~~~~~~
The most comprehensive Python library for number classification.
Importing this package triggers registration of all built-in classification
functions via their ``@register`` decorators.

Public API
----------
.. autosummary::
   is_prime
   is_armstrong
   is_perfect
   get_all_properties
   get_true_properties
   print_properties
   find_in_range
   find_all_in_range
   count_properties
   most_special_in_range
   classify
   classify_batch
   random_number
   find_by_property
   stream
"""

from __future__ import annotations

from importlib.metadata import version as _version, PackageNotFoundError as _PackageNotFoundError
try:
    __version__ = _version("numclassify")
except _PackageNotFoundError:
    __version__ = "0.0.0"

# --- Import all _core submodules so @register decorators fire at import time ---
from numclassify._core import primes as _primes        # noqa: F401
from numclassify._core import figurate as _figurate      # noqa: F401
from numclassify._core import digital as _digital       # noqa: F401
from numclassify._core import recreational as _recreational  # noqa: F401
from numclassify._core import divisors as _divisors      # noqa: F401
from numclassify._core import sequences as _sequences     # noqa: F401
from numclassify._core import powers as _powers        # noqa: F401
from numclassify._core import number_theory as _number_theory # noqa: F401
from numclassify._core import combinatorial as _combinatorial # noqa: F401
from numclassify._core import exam_types as _exam_types      # noqa: F401

# --- Re-export key functions at top level ---
from numclassify._core.primes import is_prime         # noqa: F401
from numclassify._core.digital import is_armstrong    # noqa: F401
from numclassify._core.divisors import is_perfect     # noqa: F401
from numclassify._registry import register             # noqa: F401
from numclassify._registry import (                   # noqa: F401
    get_all_properties,
    get_true_properties,
    print_properties,
    find_in_range,
    find_all_in_range,
    find_any_in_range,
    count_properties,
    most_special_in_range,
)

# ---------------------------------------------------------------------------
# Dynamic attribute fallback — allows nc.<any_registered_type>() to work
# ---------------------------------------------------------------------------

def __getattr__(name: str):
    """Fallback: look up *name* in the global registry as a normalised key."""
    from numclassify._registry import REGISTRY, _normalize

    key = _normalize(name)
    if key in REGISTRY:
        return REGISTRY[key].func
    raise AttributeError(f"module 'numclassify' has no attribute {name!r}")


# ---------------------------------------------------------------------------
# New features
# ---------------------------------------------------------------------------

def classify(n: int) -> dict:
    """
    Returns a summary dict for a single integer.

    Returns
    -------
    {
        "number": n,
        "true_properties": [list of property names that are True, sorted by category],
        "score": int,
        "categories": {category_name: [list of property names]},
    }
    """
    from numclassify._registry import REGISTRY, _normalize

    all_props = get_all_properties(n)
    true_props_with_cat = []
    for name, val in all_props.items():
        if val:
            key = _normalize(name)
            cat = REGISTRY[key].category if key in REGISTRY else "other"
            true_props_with_cat.append((name, cat))

    # Sort by category then name
    true_props_with_cat.sort(key=lambda x: (x[1], x[0]))
    true_props = [name for name, _ in true_props_with_cat]

    # Build categories dict
    categories: dict = {}
    for name, cat in true_props_with_cat:
        categories.setdefault(cat, []).append(name)

    return {
        "number": n,
        "true_properties": true_props,
        "score": len(true_props),
        "notable_score": sum(
            len(v) for k, v in categories.items()
            if k not in ("figurate", "figurate_centered")
        ),
        "categories": categories,
    }


def classify_batch(numbers: list) -> list:
    """Returns a list of classify(n) dicts, one per number, same order."""
    return [classify(n) for n in numbers]


def random_number(max_n: int = 10000) -> dict:
    """Picks a random int between 1 and max_n inclusive, returns classify(n)."""
    import random as _random
    n = _random.randint(1, max_n)
    return classify(n)


def find_by_property(start: int = 1, end: int = 1000,
                     limit: int | None = None, **filters: bool) -> list:
    """
    Query numbers by property values within [start, end].

    Parameters
    ----------
    start, end : int
        Inclusive search range.
    limit : int, optional
        Stop after finding this many matches.
    **filters : bool
        Property name to required bool value mapping.

    Returns
    -------
    list of int

    Example
    -------
    find_by_property(start=1, end=1000, Perfect=True, Odious=True)
    """
    results = []
    for n in range(start, end + 1):
        if not filters:
            results.append(n)
        else:
            props = get_all_properties(n)
            if all(props.get(k) == v for k, v in filters.items()):
                results.append(n)
        if limit is not None and len(results) >= limit:
            break
    return results


from typing import Optional

def stream(start: int, end: int, min_score: int = 0, has_property: Optional[str] = None):
    """Generator. Yields classify(n) for each n in [start, end]. Memory-safe.

    Parameters
    ----------
    start, end : int
        Inclusive range.
    min_score : int, optional
        Only yield results with score >= min_score. Default 0 (yield all).
    has_property : str, optional
        Only yield results where this property is True.
        Accepts any registered property name (case-insensitive, spaces or underscores).

    Example
    -------
    # Only numbers with more than 20 true properties
    for result in nc.stream(1, 10000, min_score=20):
        print(result)

    # Only fibonacci numbers in a range
    for result in nc.stream(1, 1000, has_property='fibonacci'):
        print(result['number'])
    """
    from numclassify._registry import REGISTRY, _normalize, get_all_properties as _gap

    prop_key = _normalize(has_property) if has_property else None

    for n in range(start, end + 1):
        result = classify(n)
        if result["notable_score"] < min_score:
            continue
        if prop_key is not None:
            props = _gap(n)
            # find by normalized key
            matched = any(
                _normalize(k) == prop_key for k, v in props.items() if v
            )
            if not matched:
                continue
        yield result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "__version__",
    "register",
    "is_prime",
    "is_armstrong",
    "is_perfect",
    "get_all_properties",
    "get_true_properties",
    "print_properties",
    "find_in_range",
    "find_all_in_range",
    "find_any_in_range",
    "count_properties",
    "most_special_in_range",
    "classify",
    "classify_batch",
    "random_number",
    "find_by_property",
    "stream",
]

# Clean up internal names that leak into dir(nc)
del (_primes, _figurate, _digital, _recreational,
     _divisors, _sequences, _powers, _number_theory,
     _combinatorial, _exam_types, _core, _registry,
     Optional, _version, _PackageNotFoundError)
