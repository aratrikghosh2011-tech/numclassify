"""
numclassify._core.figurate
~~~~~~~~~~~~~~~~~~~~~~~~~~
Figurate (polygonal) number classifications — stub for Prompt 2.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MATHEMATICAL BACKGROUND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

k-GONAL (POLYGONAL) NUMBERS
The n-th k-gonal number is:

    P(k, n) = n * ((k - 2) * n  -  (k - 4)) / 2

  k=3  → triangular   1, 3, 6, 10, 15, …   (OEIS A000217)
  k=4  → square       1, 4, 9, 16, 25, …   (OEIS A000290)
  k=5  → pentagonal   1, 5, 12, 22, 35, …  (OEIS A000326)
  k=6  → hexagonal    1, 6, 15, 28, 45, …  (OEIS A000384)
  …and so on up to at least k=100 in the full implementation.

CENTERED k-GONAL NUMBERS
The n-th centered k-gonal number is:

    C(k, n) = k * n * (n - 1) // 2 + 1

  k=3  → centered triangular  1, 4, 10, 19, …  (OEIS A005448)
  k=4  → centered square      1, 5, 13, 25, …  (OEIS A001844)
  k=6  → centered hexagonal   1, 7, 19, 37, …  (OEIS A003215)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTO-REGISTRATION ENGINE (Prompt 2 plan)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In Prompt 2 we will auto-generate and register one checker per value of k
(triangular through 100-gonal, plus centered variants) using a loop:

    POLYGON_NAMES = {3: "Triangular", 4: "Square", 5: "Pentagonal", ...}
    OEIS_MAP      = {3: "A000217", 4: "A000290", ...}

    for k, poly_name in POLYGON_NAMES.items():

        def _make_checker(k_: int) -> Callable[[int], bool]:
            def _is_k_gonal(n: int) -> bool:
                # invert P(k, n) = n*((k-2)*n - (k-4))/2
                # discriminant = (k-4)^2 + 8*(k-2)*n
                disc = (k_ - 4) ** 2 + 8 * (k_ - 2) * n
                if disc < 0:
                    return False
                sqrt_disc = math.isqrt(disc)
                if sqrt_disc * sqrt_disc != disc:
                    return False
                num = (k_ - 4) + sqrt_disc
                den = 2 * (k_ - 2)
                return num > 0 and num % den == 0
            return _is_k_gonal

        func = _make_checker(k)          # <-- closure captures k_ not k
        register(
            name=f"{poly_name} Number",
            category="figurate",
            oeis=OEIS_MAP.get(k, ""),
            description=f"k-gonal number with k={k}: P({k}, n) = n*({k-2}*n - {k-4})/2",
        )(func)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LATE-BINDING CLOSURE BUG — MUST AVOID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Python closures capture variables by reference, not by value.  In a loop:

    BAD:
        for k in range(3, 101):
            func = lambda n: is_k_gonal_impl(n, k)   # ALL lambdas share k=100!
            register(...)(func)

    GOOD — use a factory function or a default-argument trick:
        for k in range(3, 101):
            func = lambda n, _k=k: is_k_gonal_impl(n, _k)   # each lambda owns its _k
            register(...)(func)

    BETTER — explicit factory (used in the plan above):
        def _make_checker(k_):
            def checker(n): ...
            return checker

This is the canonical Python pattern for avoiding the loop variable capture bug.
"""

from __future__ import annotations

import math


def is_k_gonal(n: int, k: int) -> bool:
    """Return ``True`` if *n* is a k-gonal (polygonal) number.

    Uses the closed-form discriminant test to avoid enumerating the sequence.
    The n-th k-gonal number is ``P(k, n) = n * ((k-2)*n - (k-4)) / 2``.

    Parameters
    ----------
    n:
        Integer to test.
    k:
        Number of sides of the polygon (k ≥ 3).

    Returns
    -------
    bool

    Raises
    ------
    NotImplementedError
        This function is a stub pending the Prompt-2 full implementation.

    Example
    -------
    >>> is_k_gonal(10, 3)   # 10 is the 4th triangular number
    Traceback (most recent call last):
        ...
    NotImplementedError
    """
    raise NotImplementedError(
        "is_k_gonal is a stub — full implementation arrives in Prompt 2."
    )
