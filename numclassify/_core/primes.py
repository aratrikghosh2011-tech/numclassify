"""
numclassify._core.primes
~~~~~~~~~~~~~~~~~~~~~~~~
Prime-number classification functions.

All functions are registered in the global registry via ``@register`` and are
also available as plain module-level callables so other modules can import them
directly (e.g. ``from numclassify._core.primes import is_prime``).
"""

from __future__ import annotations

import math
from typing import List

from numclassify._registry import register


# ---------------------------------------------------------------------------
# Miller-Rabin primality test (deterministic for n < 3_215_031_751,
# probabilistic with 20 rounds for larger values)
# ---------------------------------------------------------------------------

def _miller_rabin_test(n: int, witnesses: List[int]) -> bool:
    """Return ``True`` if *n* passes Miller-Rabin for all *witnesses*.

    Writes *n-1* as ``2^r * d`` then checks each witness *a*.

    Parameters
    ----------
    n:
        Odd integer > 2 to test.
    witnesses:
        List of bases to use.
    """
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # definitely composite
    return True  # probably prime (or prime)


@register(
    name="Prime",
    category="primes",
    oeis="A000040",
    description=(
        "A natural number greater than 1 with no positive divisors other than "
        "1 and itself."
    ),
)
def is_prime(n: int) -> bool:
    """Return ``True`` if *n* is a prime number.

    Uses a deterministic Miller-Rabin test with witnesses ``[2, 3, 5, 7]``
    for *n* < 3,215,031,751.  For larger values, 20 additional random-free
    witnesses ``[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
    59, 61, 67, 71]`` are used, which is deterministic up to at least 3.3 × 10²⁴.

    Correctly rejects Carmichael numbers such as 561.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_prime(2)
    True
    >>> is_prime(561)   # Carmichael number — composite
    False
    >>> is_prime(1_000_000_007)
    True
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False

    # Small composites covered; use Miller-Rabin
    if n < 3_215_031_751:
        witnesses = [2, 3, 5, 7]
    else:
        # Deterministic up to 3,317,044,064,679,887,385,961,981 per BPSW
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                     41, 43, 47, 53, 59, 61, 67, 71]

    return _miller_rabin_test(n, witnesses)


@register(
    name="Twin Prime",
    category="primes",
    oeis="A001097",
    description=(
        "A prime p such that p − 2 or p + 2 is also prime "
        "(i.e. p is part of a twin-prime pair)."
    ),
    aliases=["twin_prime"],
)
def is_twin_prime(n: int) -> bool:
    """Return ``True`` if *n* is a twin prime.

    A twin prime is a prime *p* for which *p − 2* or *p + 2* is also prime.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_twin_prime(5)   # 3 and 7 are both prime
    True
    >>> is_twin_prime(23)  # 21=3*7 composite, 25=5² composite
    False
    """
    if not is_prime(n):
        return False
    return is_prime(n - 2) or is_prime(n + 2)


@register(
    name="Mersenne Prime",
    category="primes",
    oeis="A000668",
    description=(
        "A prime of the form 2^p − 1 where p itself is prime."
    ),
    aliases=["mersenne_prime"],
)
def is_mersenne_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Mersenne prime.

    A Mersenne prime has the form 2^p − 1 where *p* is prime.  This
    implementation checks that *n* + 1 is a power of 2 and that the
    corresponding exponent is prime, then verifies *n* itself is prime.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_mersenne_prime(7)   # 2^3 - 1 = 7, 3 is prime
    True
    >>> is_mersenne_prime(15)  # 2^4 - 1 = 15, 4 is not prime
    False
    """
    if n < 2:
        return False
    m = n + 1
    # m must be a power of 2
    if m & (m - 1) != 0:
        return False
    p = m.bit_length() - 1  # 2^p = m  =>  p = log2(m)
    return is_prime(p) and is_prime(n)


@register(
    name="Sophie Germain Prime",
    category="primes",
    oeis="A005384",
    description=(
        "A prime p such that 2p + 1 is also prime."
    ),
    aliases=["sophie_germain_prime", "sophie germain prime"],
)
def is_sophie_germain_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Sophie Germain prime.

    A Sophie Germain prime is a prime *p* for which ``2p + 1`` is also prime.
    The prime ``2p + 1`` is called a *safe prime*.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_sophie_germain_prime(11)  # 2*11+1=23, prime
    True
    >>> is_sophie_germain_prime(13)  # 2*13+1=27=3^3, composite
    False
    """
    return is_prime(n) and is_prime(2 * n + 1)


@register(
    name="Safe Prime",
    category="primes",
    oeis="A005385",
    description=(
        "A prime p such that (p − 1) / 2 is also prime."
    ),
    aliases=["safe_prime"],
)
def is_safe_prime(n: int) -> bool:
    """Return ``True`` if *n* is a safe prime.

    A safe prime is a prime *p* for which ``(p − 1) / 2`` is also prime.
    Safe primes are related to Sophie Germain primes: *p* is safe iff
    ``(p − 1) / 2`` is a Sophie Germain prime.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_safe_prime(23)   # (23-1)/2 = 11, prime
    True
    >>> is_safe_prime(7)    # (7-1)/2 = 3, prime
    True
    >>> is_safe_prime(11)   # (11-1)/2 = 5, prime
    True
    >>> is_safe_prime(13)   # (13-1)/2 = 6, composite
    False
    """
    if not is_prime(n):
        return False
    if (n - 1) % 2 != 0:
        return False
    return is_prime((n - 1) // 2)
