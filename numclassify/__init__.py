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
"""

from __future__ import annotations

__version__ = "0.1.0"

# --- Import all _core submodules so @register decorators fire at import time ---
from numclassify._core import primes       # noqa: F401
from numclassify._core import figurate     # noqa: F401
from numclassify._core import digital      # noqa: F401
from numclassify._core import recreational  # noqa: F401

# --- Re-export key functions at top level ---
from numclassify._core.primes import is_prime        # noqa: F401
from numclassify._core.digital import is_armstrong   # noqa: F401
from numclassify._registry import (                  # noqa: F401
    get_all_properties,
    get_true_properties,
    print_properties,
    find_in_range,
    find_all_in_range,
    count_properties,
    most_special_in_range,
)


def is_perfect(n: int) -> bool:
    """Return ``True`` if *n* is a perfect number.

    A perfect number equals the sum of its proper divisors (divisors excluding
    itself).  Examples: 6 = 1+2+3, 28 = 1+2+4+7+14.

    Parameters
    ----------
    n:
        Positive integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_perfect(6)
    True
    >>> is_perfect(28)
    True
    >>> is_perfect(12)
    False
    """
    if n < 2:
        return False
    total = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
        i += 1
    return total == n


# Register is_perfect so it appears in the registry
from numclassify._registry import register as _register  # noqa: E402

_register(
    name="Perfect",
    category="number theory",
    oeis="A000396",
    description="A number equal to the sum of its proper divisors.",
    aliases=["perfect number"],
)(is_perfect)


__all__ = [
    "__version__",
    "is_prime",
    "is_armstrong",
    "is_perfect",
    "get_all_properties",
    "get_true_properties",
    "print_properties",
    "find_in_range",
    "find_all_in_range",
    "count_properties",
    "most_special_in_range",
]
