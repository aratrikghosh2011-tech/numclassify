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
from numclassify._core import primes        # noqa: F401
from numclassify._core import figurate      # noqa: F401
from numclassify._core import digital       # noqa: F401
from numclassify._core import recreational  # noqa: F401
from numclassify._core import divisors      # noqa: F401
from numclassify._core import sequences     # noqa: F401
from numclassify._core import powers        # noqa: F401
from numclassify._core import number_theory # noqa: F401
from numclassify._core import combinatorial # noqa: F401

# --- Re-export key functions at top level ---
from numclassify._core.primes import is_prime         # noqa: F401
from numclassify._core.digital import is_armstrong    # noqa: F401
from numclassify._core.divisors import is_perfect     # noqa: F401
from numclassify._registry import (                   # noqa: F401
    get_all_properties,
    get_true_properties,
    print_properties,
    find_in_range,
    find_all_in_range,
    count_properties,
    most_special_in_range,
)

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
