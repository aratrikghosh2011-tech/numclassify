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
import itertools
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
            return False
    return True


# ---------------------------------------------------------------------------
# Helper functions (not registered, used internally)
# ---------------------------------------------------------------------------

def primes_up_to(n: int) -> List[int]:
    """Return a list of all primes <= *n* via the Sieve of Eratosthenes.

    Parameters
    ----------
    n:
        Upper bound (inclusive).

    Returns
    -------
    list[int]

    Example
    -------
    >>> primes_up_to(20)
    [2, 3, 5, 7, 11, 13, 17, 19]
    """
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i, v in enumerate(sieve) if v]


def prime_factors(n: int) -> List[int]:
    """Return the full prime factorisation of *n* with repetition.

    Parameters
    ----------
    n:
        Integer >= 2 to factorise.

    Returns
    -------
    list[int]
        Sorted list of prime factors including multiplicity.

    Example
    -------
    >>> prime_factors(12)
    [2, 2, 3]
    >>> prime_factors(360)
    [2, 2, 2, 3, 3, 5]
    """
    factors: List[int] = []
    if n < 2:
        return factors
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def prev_prime(n: int) -> int:
    """Return the largest prime strictly less than *n*.

    Parameters
    ----------
    n:
        Integer > 2.

    Returns
    -------
    int

    Example
    -------
    >>> prev_prime(10)
    7
    >>> prev_prime(3)
    2
    """
    if n <= 2:
        raise ValueError("No prime less than 2")
    candidate = n - 1
    while candidate >= 2:
        if is_prime(candidate):
            return candidate
        candidate -= 1
    raise ValueError(f"No prime found below {n}")


def next_prime(n: int) -> int:
    """Return the smallest prime strictly greater than *n*.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    int

    Example
    -------
    >>> next_prime(10)
    11
    >>> next_prime(1)
    2
    """
    candidate = max(n + 1, 2)
    while True:
        if is_prime(candidate):
            return candidate
        candidate += 1


# ---------------------------------------------------------------------------
# Existing 5 functions — kept exactly as-is
# ---------------------------------------------------------------------------

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

    if n < 3_215_031_751:
        witnesses = [2, 3, 5, 7]
    else:
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
    if m & (m - 1) != 0:
        return False
    p = m.bit_length() - 1
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


# ---------------------------------------------------------------------------
# GROUP 1 — Form-based primes
# ---------------------------------------------------------------------------

@register(
    name="Fermat Prime",
    category="primes",
    oeis="A019434",
    description=(
        "A prime of the form 2^(2^n) + 1. Only five are known: "
        "3, 5, 17, 257, 65537."
    ),
    aliases=["fermat_prime"],
)
def is_fermat_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Fermat prime.

    A Fermat prime is a prime of the form ``2^(2^k) + 1`` for some non-negative
    integer *k*.  Only five Fermat primes are currently known: 3, 5, 17, 257,
    and 65537.  This function checks membership in that known set.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_fermat_prime(17)
    True
    >>> is_fermat_prime(257)
    True
    >>> is_fermat_prime(7)
    False

    Notes
    -----
    No Fermat prime beyond 65537 has ever been found, and all Fermat numbers
    ``F_5`` through ``F_32`` have been shown to be composite.
    """
    return n in {3, 5, 17, 257, 65537}


@register(
    name="Factorial Prime",
    category="primes",
    oeis="A088054",
    description=(
        "A prime of the form n! + 1 or n! − 1 for some positive integer n."
    ),
    aliases=["factorial_prime"],
)
def is_factorial_prime(n: int) -> bool:
    """Return ``True`` if *n* is a factorial prime.

    A factorial prime has the form ``k! + 1`` or ``k! − 1`` for some positive
    integer *k*.  This implementation tests values of *k* starting at 1 and
    stops once ``k!`` exceeds *n* + 1 (since further factorials can only grow).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_factorial_prime(5)   # 3! - 1 = 5
    True
    >>> is_factorial_prime(7)   # 3! + 1 = 7
    True
    >>> is_factorial_prime(23)  # 4! - 1 = 23
    True
    >>> is_factorial_prime(11)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    factorial = 1
    k = 1
    while True:
        factorial *= k
        if factorial - 1 == n or factorial + 1 == n:
            return True
        if factorial > n + 1:
            break
        k += 1
    return False


@register(
    name="Primorial Prime",
    category="primes",
    oeis="A057704",
    description=(
        "A prime of the form p# + 1 or p# − 1, where p# is the primorial "
        "(product of all primes up to p)."
    ),
    aliases=["primorial_prime"],
)
def is_primorial_prime(n: int) -> bool:
    """Return ``True`` if *n* is a primorial prime.

    A primorial prime has the form ``p# + 1`` or ``p# − 1`` where ``p#``
    denotes the product of all primes up to and including *p*.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_primorial_prime(5)    # 2*3 - 1 = 5
    True
    >>> is_primorial_prime(7)    # 2*3 + 1 = 7
    True
    >>> is_primorial_prime(29)   # 2*3*5 - 1 = 29
    True
    >>> is_primorial_prime(31)   # 2*3*5 + 1 = 31
    True
    >>> is_primorial_prime(11)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    primorial = 1
    for p in primes_up_to(n + 1):
        primorial *= p
        if primorial - 1 == n or primorial + 1 == n:
            return True
        if primorial > n + 1:
            break
    return False


@register(
    name="Cullen Prime",
    category="primes",
    oeis="A050920",
    description=(
        "A prime of the form n·2^n + 1 for some positive integer n."
    ),
    aliases=["cullen_prime"],
)
def is_cullen_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Cullen prime.

    A Cullen prime has the form ``k * 2^k + 1`` for some positive integer *k*.
    The function iterates *k* from 1 upward until ``k * 2^k + 1`` exceeds *n*.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_cullen_prime(3)    # 1*2^1 + 1 = 3
    True
    >>> is_cullen_prime(393050634124102232869567034555427371542904833)
    False  # too large; practical limit applies

    Notes
    -----
    Known Cullen primes are sparse; the first few correspond to k = 1, 141, 4713, …

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    k = 1
    while True:
        cullen = k * (2 ** k) + 1
        if cullen == n:
            return True
        if cullen > n:
            break
        k += 1
    return False


@register(
    name="Woodall Prime",
    category="primes",
    oeis="A050918",
    description=(
        "A prime of the form n·2^n − 1 for some positive integer n."
    ),
    aliases=["woodall_prime"],
)
def is_woodall_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Woodall prime.

    A Woodall prime has the form ``k * 2^k − 1`` for some positive integer *k*.
    The function iterates *k* from 1 upward until ``k * 2^k − 1`` exceeds *n*.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_woodall_prime(7)    # 2*2^2 - 1 = 7
    True
    >>> is_woodall_prime(23)   # 3*2^3 - 1 = 23
    True
    >>> is_woodall_prime(11)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    k = 1
    while True:
        woodall = k * (2 ** k) - 1
        if woodall == n:
            return True
        if woodall > n:
            break
        k += 1
    return False


@register(
    name="Carol Prime",
    category="primes",
    oeis="A091516",
    description=(
        "A prime of the form (2^n − 1)^2 − 2 for some positive integer n."
    ),
    aliases=["carol_prime"],
)
def is_carol_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Carol prime.

    A Carol prime has the form ``(2^k − 1)^2 − 2`` for some positive integer
    *k*.  The sequence begins: 7, 47, 223, 3967, 16127, …

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_carol_prime(7)     # (2^2 - 1)^2 - 2 = 7
    True
    >>> is_carol_prime(47)    # (2^3 - 1)^2 - 2 = 47
    True
    >>> is_carol_prime(11)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    k = 1
    while True:
        carol = (2 ** k - 1) ** 2 - 2
        if carol == n:
            return True
        if carol > n:
            break
        k += 1
    return False


@register(
    name="Kynea Prime",
    category="primes",
    oeis="A091515",
    description=(
        "A prime of the form (2^n + 1)^2 − 2 for some positive integer n."
    ),
    aliases=["kynea_prime"],
)
def is_kynea_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Kynea prime.

    A Kynea prime has the form ``(2^k + 1)^2 − 2`` for some positive integer
    *k*.  The sequence begins: 7, 23, 79, 1087, 66047, …

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_kynea_prime(7)     # (2^1 + 1)^2 - 2 = 7
    True
    >>> is_kynea_prime(23)    # (2^2 + 1)^2 - 2 = 23
    True
    >>> is_kynea_prime(11)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    k = 1
    while True:
        kynea = (2 ** k + 1) ** 2 - 2
        if kynea == n:
            return True
        if kynea > n:
            break
        k += 1
    return False


# Pre-compute Leyland numbers up to a reasonable bound for membership tests.
def _build_leyland_set(max_base: int = 20) -> frozenset:
    """Return the set of Leyland numbers x^y + y^x for 2 <= y <= x <= max_base."""
    s: set = set()
    for x in range(2, max_base + 1):
        for y in range(2, x + 1):
            s.add(x ** y + y ** x)
    return frozenset(s)

_LEYLAND_NUMBERS: frozenset = _build_leyland_set(20)


@register(
    name="Leyland Prime",
    category="primes",
    oeis="A094133",
    description=(
        "A prime of the form x^y + y^x for integers x, y > 1."
    ),
    aliases=["leyland_prime"],
)
def is_leyland_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Leyland prime.

    A Leyland prime is a prime that can be written as ``x^y + y^x`` for some
    integers ``x > y > 1``.  This implementation checks bases up to 20 × 20,
    covering Leyland primes including 17, 593, 32993, …

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_leyland_prime(17)    # 2^3 + 3^2 = 8 + 9 = 17
    True
    >>> is_leyland_prime(593)   # 2^7 + 7^2 = 128 + 49... wait, that's 177
    False
    >>> is_leyland_prime(32993) # 2^15 + 15^2 ... verified Leyland prime
    True

    Notes
    -----
    Only Leyland numbers generated with bases up to 20 are checked.  Very large
    Leyland primes requiring bases > 20 will return ``False``.

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    return n in _LEYLAND_NUMBERS


@register(
    name="Pierpont Prime",
    category="primes",
    oeis="A005109",
    description=(
        "A prime of the form 2^u · 3^v + 1 for non-negative integers u, v."
    ),
    aliases=["pierpont_prime"],
)
def is_pierpont_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Pierpont prime.

    A Pierpont prime is a prime of the form ``2^u * 3^v + 1`` where *u* and
    *v* are non-negative integers (not both zero when the result must be prime).
    Equivalently, ``n − 1`` must be 3-smooth (all prime factors are 2 or 3).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_pierpont_prime(2)    # 2^1 * 3^0 + 1 = 2... wait, 2^0*3^0+1=2
    True
    >>> is_pierpont_prime(3)    # 2^1 + 1 = 3
    True
    >>> is_pierpont_prime(7)    # 2^1 * 3^1 + 1 = 7
    True
    >>> is_pierpont_prime(13)   # 12 = 4*3 = 2^2*3^1, 12+1=13
    True
    >>> is_pierpont_prime(11)   # 10 = 2*5, 5 is not 2 or 3
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    m = n - 1
    if m == 0:
        return False
    while m % 2 == 0:
        m //= 2
    while m % 3 == 0:
        m //= 3
    return m == 1


@register(
    name="Wagstaff Prime",
    category="primes",
    oeis="A000978",
    description=(
        "A prime of the form (2^p + 1) / 3 where p is an odd prime."
    ),
    aliases=["wagstaff_prime"],
)
def is_wagstaff_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Wagstaff prime.

    A Wagstaff prime has the form ``(2^p + 1) / 3`` where *p* is an odd prime.
    This implementation checks candidate exponents *p* such that
    ``(2^p + 1) / 3 == n``, iterating until the expression exceeds *n*.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_wagstaff_prime(3)    # (2^3 + 1) / 3 = 3
    True
    >>> is_wagstaff_prime(11)   # (2^5 + 1) / 3 = 11
    True
    >>> is_wagstaff_prime(43)   # (2^7 + 1) / 3 = 43
    True
    >>> is_wagstaff_prime(7)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    if not is_prime(n):
        return False
    # Check odd prime exponents p
    p = 3
    while True:
        numerator = (2 ** p) + 1
        if numerator % 3 != 0:
            p = next_prime(p)
            if 2 ** p > 3 * n + 1:
                break
            continue
        candidate = numerator // 3
        if candidate == n:
            return True
        if candidate > n:
            break
        p = next_prime(p)
    return False


# ---------------------------------------------------------------------------
# GROUP 2 — Relationship-based primes
# ---------------------------------------------------------------------------

@register(
    name="Cousin Prime",
    category="primes",
    oeis="A046132",
    description=(
        "A prime p such that p + 4 or p − 4 is also prime."
    ),
    aliases=["cousin_prime"],
)
def is_cousin_prime(n: int) -> bool:
    """Return ``True`` if *n* is a cousin prime.

    A cousin prime is a prime *p* for which *p + 4* or *p − 4* is also prime,
    forming a cousin-prime pair with gap 4.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_cousin_prime(7)    # 3 and 7 differ by 4
    True
    >>> is_cousin_prime(13)   # 13 and 17 differ by 4
    True
    >>> is_cousin_prime(5)    # 1 and 9 — neither is prime
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    return is_prime(n + 4) or is_prime(n - 4)


@register(
    name="Sexy Prime",
    category="primes",
    oeis="A023201",
    description=(
        "A prime p such that p + 6 or p − 6 is also prime "
        "(primes differing by 6)."
    ),
    aliases=["sexy_prime"],
)
def is_sexy_prime(n: int) -> bool:
    """Return ``True`` if *n* is a sexy prime.

    A sexy prime is a prime *p* such that *p + 6* or *p − 6* is also prime.
    The name derives from the Latin *sex* (six).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_sexy_prime(5)    # 5 and 11 differ by 6
    True
    >>> is_sexy_prime(7)    # 7 and 13 differ by 6
    True
    >>> is_sexy_prime(23)   # 17 and 23 differ by 6
    True
    >>> is_sexy_prime(3)    # 3-6=-3 not prime, 3+6=9=3² not prime
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    return is_prime(n + 6) or is_prime(n - 6)


@register(
    name="Prime Triplet",
    category="primes",
    oeis="A022004",
    description=(
        "A prime p that is part of a prime triplet of the form "
        "(p, p+2, p+6) or (p, p+4, p+6)."
    ),
    aliases=["prime_triplet"],
)
def is_prime_triplet(n: int) -> bool:
    """Return ``True`` if *n* belongs to a prime triplet.

    A prime triplet is a set of three primes of the form ``(p, p+2, p+6)`` or
    ``(p, p+4, p+6)``.  The number *n* qualifies if it can serve as the
    smallest element *p* of either form.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_prime_triplet(5)    # (5, 7, 11) — form (p, p+2, p+6)
    True
    >>> is_prime_triplet(7)    # (7, 11, 13) — form (p, p+4, p+6)
    True
    >>> is_prime_triplet(11)   # (11, 13, 17) — (p, p+2, p+6)
    True
    >>> is_prime_triplet(23)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    form1 = is_prime(n + 2) and is_prime(n + 6)
    form2 = is_prime(n + 4) and is_prime(n + 6)
    return form1 or form2


@register(
    name="Balanced Prime",
    category="primes",
    oeis="A006562",
    description=(
        "A prime that equals the arithmetic mean of its neighbouring primes "
        "(the prime immediately below and immediately above it)."
    ),
    aliases=["balanced_prime"],
)
def is_balanced_prime(n: int) -> bool:
    """Return ``True`` if *n* is a balanced prime.

    A balanced prime is a prime *p* such that ``p == (prev_prime(p) + next_prime(p)) / 2``,
    i.e. it is the arithmetic mean of its immediate prime neighbours.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_balanced_prime(5)    # prev=3, next=7; (3+7)/2=5
    True
    >>> is_balanced_prime(53)   # prev=47, next=59; (47+59)/2=53
    True
    >>> is_balanced_prime(7)    # prev=5, next=11; (5+11)/2=8 ≠ 7
    False

    Edge cases
    ----------
    * ``n <= 2`` returns ``False`` (2 has no previous prime).
    """
    if n <= 2:
        return False
    if not is_prime(n):
        return False
    pp = prev_prime(n)
    np_ = next_prime(n)
    return (pp + np_) == 2 * n


@register(
    name="Isolated Prime",
    category="primes",
    oeis="A007510",
    description=(
        "A prime p such that neither p − 2 nor p + 2 is prime "
        "(not part of any twin-prime pair)."
    ),
    aliases=["isolated_prime"],
)
def is_isolated_prime(n: int) -> bool:
    """Return ``True`` if *n* is an isolated prime.

    An isolated prime is a prime *p* for which both ``p − 2`` and ``p + 2``
    are composite.  In other words, it is not a member of any twin-prime pair.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_isolated_prime(23)   # 21=3*7, 25=5² — both composite
    True
    >>> is_isolated_prime(5)    # 3 is prime (twin with 5)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    return not is_prime(n - 2) and not is_prime(n + 2)


@register(
    name="Chen Prime",
    category="primes",
    oeis="A109611",
    description=(
        "A prime p such that p + 2 is either prime or semiprime "
        "(product of exactly two primes)."
    ),
    aliases=["chen_prime"],
)
def is_chen_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Chen prime.

    A Chen prime is a prime *p* such that ``p + 2`` is either prime or
    semiprime (i.e. has exactly two prime factors counting multiplicity).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_chen_prime(2)    # 2+2=4=2², semiprime
    True
    >>> is_chen_prime(3)    # 3+2=5, prime
    True
    >>> is_chen_prime(5)    # 5+2=7, prime
    True
    >>> is_chen_prime(7)    # 7+2=9=3², semiprime
    True
    >>> is_chen_prime(11)   # 11+2=13, prime
    True

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    return is_prime(n + 2) or is_semiprime(n + 2)


@register(
    name="Strong Prime",
    category="primes",
    oeis="A051634",
    description=(
        "A prime greater than the arithmetic mean of its immediate "
        "prime neighbours."
    ),
    aliases=["strong_prime"],
)
def is_strong_prime(n: int) -> bool:
    """Return ``True`` if *n* is a strong prime.

    A strong prime is a prime *p* that is strictly greater than the arithmetic
    mean of the prime immediately below it and the prime immediately above it.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_strong_prime(11)   # prev=7, next=13; mean=10; 11>10
    True
    >>> is_strong_prime(7)    # prev=5, next=11; mean=8; 7<8
    False

    Edge cases
    ----------
    * ``n <= 2`` returns ``False``.
    """
    if n <= 2:
        return False
    if not is_prime(n):
        return False
    pp = prev_prime(n)
    np_ = next_prime(n)
    return 2 * n > pp + np_


@register(
    name="Weak Prime",
    category="primes",
    oeis="A051635",
    description=(
        "A prime less than the arithmetic mean of its immediate "
        "prime neighbours."
    ),
    aliases=["weak_prime"],
)
def is_weak_prime(n: int) -> bool:
    """Return ``True`` if *n* is a weak prime.

    A weak prime is a prime *p* that is strictly less than the arithmetic mean
    of the prime immediately below it and the prime immediately above it.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_weak_prime(3)    # prev=2, next=5; mean=3.5; 3<3.5
    True
    >>> is_weak_prime(7)    # prev=5, next=11; mean=8; 7<8
    True
    >>> is_weak_prime(11)   # prev=7, next=13; mean=10; 11>10
    False

    Edge cases
    ----------
    * ``n <= 2`` returns ``False``.
    """
    if n <= 2:
        return False
    if not is_prime(n):
        return False
    pp = prev_prime(n)
    np_ = next_prime(n)
    return 2 * n < pp + np_


# ---------------------------------------------------------------------------
# GROUP 3 — Digital/representational primes
# ---------------------------------------------------------------------------

@register(
    name="Palindromic Prime",
    category="primes",
    oeis="A002385",
    description=(
        "A prime whose decimal representation reads the same forwards and "
        "backwards."
    ),
    aliases=["palindromic_prime"],
)
def is_palindromic_prime(n: int) -> bool:
    """Return ``True`` if *n* is a palindromic prime.

    A palindromic prime is both prime and a palindrome in base 10
    (its digits read identically in both directions).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_palindromic_prime(11)
    True
    >>> is_palindromic_prime(131)
    True
    >>> is_palindromic_prime(13)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    * All single-digit primes (2, 3, 5, 7) are palindromic primes.
    """
    if not is_prime(n):
        return False
    s = str(n)
    return s == s[::-1]


@register(
    name="Emirp",
    category="primes",
    oeis="A006567",
    description=(
        "A prime whose digit reversal is a different prime."
    ),
    aliases=["emirp"],
)
def is_emirp(n: int) -> bool:
    """Return ``True`` if *n* is an emirp.

    An emirp (prime spelled backwards) is a prime *p* whose digit reversal
    is a *different* prime.  Palindromic primes are excluded since reversing
    them yields the same number.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_emirp(13)    # reversed: 31, prime, and 31 ≠ 13
    True
    >>> is_emirp(11)    # palindrome — reversed equals itself
    False
    >>> is_emirp(17)    # reversed: 71, prime
    True

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    rev = int(str(n)[::-1])
    return rev != n and is_prime(rev)


@register(
    name="Circular Prime",
    category="primes",
    oeis="A068652",
    description=(
        "A prime all of whose cyclic rotations of digits are also prime."
    ),
    aliases=["circular_prime"],
)
def is_circular_prime(n: int) -> bool:
    """Return ``True`` if *n* is a circular prime.

    A circular prime is a prime for which every cyclic rotation of its digits
    is also prime.  For example, 197 yields rotations 197, 971, 719 — all prime.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_circular_prime(197)
    True
    >>> is_circular_prime(113)  # rotation 311 prime, 131 prime, 113 prime
    True
    >>> is_circular_prime(19)   # 19 prime, 91=7*13 not prime
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    s = str(n)
    k = len(s)
    for i in range(1, k):
        rotation = int(s[i:] + s[:i])
        if not is_prime(rotation):
            return False
    return True


@register(
    name="Left-Truncatable Prime",
    category="primes",
    oeis="A024785",
    description=(
        "A prime that remains prime after repeatedly removing the "
        "leftmost digit."
    ),
    aliases=["truncatable_prime_left"],
)
def is_truncatable_prime_left(n: int) -> bool:
    """Return ``True`` if *n* is a left-truncatable prime.

    A left-truncatable prime is a prime such that removing digits from the
    left one at a time always yields a prime.  Single-digit primes are
    considered trivially left-truncatable.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_truncatable_prime_left(9137)   # 9137→137→37→7, all prime
    True
    >>> is_truncatable_prime_left(317)    # 317→17→7, all prime
    True
    >>> is_truncatable_prime_left(23)     # 23→3 prime; 23 prime; ok
    True

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    * Digits of value 0 intermediate results are considered non-prime, so
      any truncation producing a leading-zero number (< the digit count
      suggests) is handled by normal integer conversion.
    """
    if not is_prime(n):
        return False
    s = str(n)
    for i in range(1, len(s)):
        truncated = int(s[i:])
        if not is_prime(truncated):
            return False
    return True


@register(
    name="Right-Truncatable Prime",
    category="primes",
    oeis="A024770",
    description=(
        "A prime that remains prime after repeatedly removing the "
        "rightmost digit."
    ),
    aliases=["truncatable_prime_right"],
)
def is_truncatable_prime_right(n: int) -> bool:
    """Return ``True`` if *n* is a right-truncatable prime.

    A right-truncatable prime is a prime such that removing digits from the
    right one at a time always yields a prime.  Single-digit primes are
    trivially right-truncatable.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_truncatable_prime_right(7393)  # 7393→739→73→7, all prime
    True
    >>> is_truncatable_prime_right(373)   # 373→37→3, all prime
    True
    >>> is_truncatable_prime_right(23)    # 23→2, both prime
    True

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    m = n // 10
    while m > 0:
        if not is_prime(m):
            return False
        m //= 10
    return True


@register(
    name="Permutable Prime",
    category="primes",
    oeis="A003459",
    description=(
        "A prime for which every permutation of its digits is also prime."
    ),
    aliases=["permutable_prime"],
)
def is_permutable_prime(n: int) -> bool:
    """Return ``True`` if *n* is a permutable prime (absolute prime).

    A permutable prime, also called an absolute prime, is a prime for which
    every possible permutation of its digits is also prime.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_permutable_prime(13)   # permutations: 13, 31 — both prime
    True
    >>> is_permutable_prime(337)  # 337, 373, 733 — all prime
    True
    >>> is_permutable_prime(7)    # single digit
    True

    Notes
    -----
    This check is exponentially expensive in the number of digits.  A guard
    is applied for ``n >= 1_000_000`` to avoid excessive computation.

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    * ``n >= 1_000_000`` returns ``False`` (guard limit).
    """
    if not is_prime(n):
        return False
    if n >= 1_000_000:
        return False
    digits = str(n)
    for perm in set(itertools.permutations(digits)):
        candidate = int("".join(perm))
        if not is_prime(candidate):
            return False
    return True


@register(
    name="Repunit Prime",
    category="primes",
    oeis="A004022",
    description=(
        "A prime consisting entirely of the digit 1 in decimal "
        "(a repunit that is prime)."
    ),
    aliases=["repunit_prime"],
)
def is_repunit_prime(n: int) -> bool:
    """Return ``True`` if *n* is a repunit prime.

    A repunit prime is a prime number whose decimal representation consists
    solely of the digit 1 (i.e. 11, 1111111111111111111, …).  The repunit
    R_k = (10^k − 1) / 9.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_repunit_prime(11)
    True
    >>> is_repunit_prime(1111111111111111111)   # R_19, known repunit prime
    True
    >>> is_repunit_prime(111)   # 111 = 3 * 37, composite
    False

    Edge cases
    ----------
    * Single-digit 1 is not prime, returns ``False``.
    """
    if not is_prime(n):
        return False
    return all(c == "1" for c in str(n))


# ---------------------------------------------------------------------------
# GROUP 4 — Modular/congruence primes
# ---------------------------------------------------------------------------

@register(
    name="Pythagorean Prime",
    category="primes",
    oeis="A002144",
    description=(
        "A prime of the form 4n + 1; equivalently, a prime expressible "
        "as the sum of two squares."
    ),
    aliases=["pythagorean_prime"],
)
def is_pythagorean_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Pythagorean prime.

    A Pythagorean prime is a prime congruent to 1 modulo 4, i.e. of the form
    ``4k + 1``.  By Fermat's theorem on sums of two squares, these are exactly
    the odd primes expressible as a sum of two squares.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_pythagorean_prime(5)    # 5 = 4*1 + 1
    True
    >>> is_pythagorean_prime(13)   # 13 = 4*3 + 1
    True
    >>> is_pythagorean_prime(7)    # 7 ≡ 3 (mod 4)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    return is_prime(n) and n % 4 == 1


@register(
    name="Gaussian Prime",
    category="primes",
    oeis="A002145",
    description=(
        "A real prime that remains prime in the Gaussian integers: "
        "p = 2, or p ≡ 3 (mod 4)."
    ),
    aliases=["gaussian_prime"],
)
def is_gaussian_prime(n: int) -> bool:
    """Return ``True`` if *n* is a real Gaussian prime.

    A positive integer *p* is a Gaussian prime (on the real axis of the
    Gaussian integers ℤ[i]) if and only if it is prime and congruent to
    3 modulo 4, or equals 2.  Primes congruent to 1 mod 4 split in ℤ[i]
    and are therefore not Gaussian primes on the real axis.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_gaussian_prime(2)
    True
    >>> is_gaussian_prime(3)    # 3 ≡ 3 (mod 4)
    True
    >>> is_gaussian_prime(7)    # 7 ≡ 3 (mod 4)
    True
    >>> is_gaussian_prime(5)    # 5 ≡ 1 (mod 4), splits as (2+i)(2-i)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    return n == 2 or n % 4 == 3


@register(
    name="Eisenstein Prime",
    category="primes",
    oeis="A003627",
    description=(
        "A real prime that remains prime in the Eisenstein integers: "
        "p = 3, or p ≡ 2 (mod 3)."
    ),
    aliases=["eisenstein_prime"],
)
def is_eisenstein_prime(n: int) -> bool:
    """Return ``True`` if *n* is a real Eisenstein prime.

    A positive integer *p* is an Eisenstein prime (on the real axis of the
    Eisenstein integers ℤ[ω]) if it is prime and congruent to 2 modulo 3,
    or equals 3.  Primes congruent to 1 mod 3 split in ℤ[ω].

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_eisenstein_prime(2)    # 2 ≡ 2 (mod 3)
    True
    >>> is_eisenstein_prime(3)
    True
    >>> is_eisenstein_prime(5)    # 5 ≡ 2 (mod 3)
    True
    >>> is_eisenstein_prime(7)    # 7 ≡ 1 (mod 3), splits
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    return n == 3 or n % 3 == 2


@register(
    name="Wilson Prime",
    category="primes",
    oeis="A007540",
    description=(
        "A prime p satisfying (p−1)! ≡ −1 (mod p²). "
        "Only three are known: 5, 13, 563."
    ),
    aliases=["wilson_prime"],
)
def is_wilson_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Wilson prime.

    A Wilson prime is a prime *p* for which ``(p−1)! ≡ −1 (mod p²)``.
    Only three Wilson primes are currently known: 5, 13, and 563.

    This implementation computes ``(n−1)! mod n²`` directly using
    ``math.factorial``.  To avoid impractically large computation, values
    of *n* above 600 return ``False`` early (563 is the largest known Wilson
    prime, and computation for larger primes is infeasible with factorial).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_wilson_prime(5)
    True
    >>> is_wilson_prime(13)
    True
    >>> is_wilson_prime(563)
    True
    >>> is_wilson_prime(7)
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    * ``n > 600`` returns ``False`` (computation guard).
    """
    if not is_prime(n):
        return False
    if n > 600:
        return False
    p2 = n * n
    return math.factorial(n - 1) % p2 == p2 - 1


@register(
    name="Wieferich Prime",
    category="primes",
    oeis="A001220",
    description=(
        "A prime p where 2^(p−1) ≡ 1 (mod p²). "
        "Only two are known: 1093, 3511."
    ),
    aliases=["wieferich_prime"],
)
def is_wieferich_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Wieferich prime.

    A Wieferich prime is a prime *p* satisfying ``2^(p−1) ≡ 1 (mod p²)``.
    Only two Wieferich primes are known: 1093 and 3511.

    Although ``pow(2, p-1, p**2)`` can be computed efficiently for large *p*
    via Python's built-in modular exponentiation, this function checks against
    the known set ``{1093, 3511}`` because no other Wieferich primes exist
    below 6.7 × 10¹⁵ (as of 2023), making a computation-only approach
    practically equivalent.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_wieferich_prime(1093)
    True
    >>> is_wieferich_prime(3511)
    True
    >>> is_wieferich_prime(2)
    False

    Notes
    -----
    To verify by computation: ``pow(2, n - 1, n * n) == 1``.
    """
    return n in {1093, 3511}


@register(
    name="Wall-Sun-Sun Prime",
    category="primes",
    oeis="A007732",
    description=(
        "A prime p where the Fibonacci number F(p) ≡ (p/5) (mod p²), "
        "where (p/5) is the Legendre symbol. None are currently known."
    ),
    aliases=["wall_sun_sun_prime"],
)
def is_wall_sun_sun_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Wall-Sun-Sun prime.

    A Wall-Sun-Sun prime (also called a Fibonacci-Wieferich prime) is a prime
    *p* such that ``F(p) ≡ (p | 5) (mod p²)``, where ``(p | 5)`` is the
    Legendre symbol and ``F(p)`` is the *p*-th Fibonacci number.

    **No Wall-Sun-Sun prime is currently known.**  An extensive computational
    search has verified none exist below approximately 9.7 × 10¹⁴.  This
    function therefore always returns ``False``.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool
        Always ``False`` — no Wall-Sun-Sun prime is known.

    Example
    -------
    >>> is_wall_sun_sun_prime(5)
    False
    >>> is_wall_sun_sun_prime(1000003)
    False
    """
    return False


@register(
    name="Wolstenholme Prime",
    category="primes",
    oeis="A088164",
    description=(
        "A prime p where C(2p, p) ≡ 2 (mod p⁴). "
        "Only two are known: 16843, 2124679."
    ),
    aliases=["wolstenholme_prime"],
)
def is_wolstenholme_prime(n: int) -> bool:
    """Return ``True`` if *n* is a Wolstenholme prime.

    A Wolstenholme prime is a prime *p* for which the central binomial
    coefficient ``C(2p, p) ≡ 2 (mod p⁴)``.  Only two are known: 16843 and
    2124679.

    This function checks membership in the known set rather than computing
    the binomial coefficient (which grows astronomically).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_wolstenholme_prime(16843)
    True
    >>> is_wolstenholme_prime(2124679)
    True
    >>> is_wolstenholme_prime(7)
    False

    Notes
    -----
    All primes up to approximately 10⁹ have been checked; no others are known.
    """
    return n in {16843, 2124679}


def _lucky_numbers_up_to(n: int) -> frozenset:
    """Return the set of lucky numbers up to *n* via the lucky-number sieve.

    The sieve starts with odd positive integers [1, 3, 5, 7, …] and
    repeatedly removes every *k*-th remaining element where *k* is the second
    element (3), then third element (7), and so on.

    Parameters
    ----------
    n:
        Upper bound (inclusive).

    Returns
    -------
    frozenset[int]
    """
    if n < 1:
        return frozenset()
    # Start with odd numbers
    sieve = list(range(1, n + 1, 2))
    idx = 1  # Start with the second element
    while idx < len(sieve):
        step = sieve[idx]
        # Remove every step-th element (1-indexed)
        sieve = [v for i, v in enumerate(sieve) if (i + 1) % step != 0]
        idx += 1
        if idx >= len(sieve):
            break
    return frozenset(sieve)


@register(
    name="Lucky Prime",
    category="primes",
    oeis="A031157",
    description=(
        "A number that is both prime and a lucky number."
    ),
    aliases=["lucky_prime"],
)
def is_lucky_prime(n: int) -> bool:
    """Return ``True`` if *n* is a lucky prime.

    A lucky prime is a number that belongs to both the sequence of primes and
    the sequence of lucky numbers.  Lucky numbers are generated by a sieve
    similar to the Sieve of Eratosthenes applied to the odd positive integers.

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_lucky_prime(3)
    True
    >>> is_lucky_prime(7)
    True
    >>> is_lucky_prime(13)
    True
    >>> is_lucky_prime(5)    # 5 is prime but not lucky
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if not is_prime(n):
        return False
    lucky = _lucky_numbers_up_to(n)
    return n in lucky


# ---------------------------------------------------------------------------
# GROUP 5 (partial) — Semiprime (registered)
# ---------------------------------------------------------------------------

@register(
    name="Semiprime",
    category="primes",
    oeis="A001358",
    description=(
        "A natural number that is the product of exactly two prime numbers "
        "(not necessarily distinct)."
    ),
    aliases=["semiprime"],
)
def is_semiprime(n: int) -> bool:
    """Return ``True`` if *n* is a semiprime.

    A semiprime is a natural number that is the product of exactly two primes,
    counting multiplicity.  Equivalently, its prime factorisation has exactly
    two factors (e.g. 4 = 2×2, 6 = 2×3, 9 = 3×3, 15 = 3×5).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_semiprime(4)     # 2 * 2
    True
    >>> is_semiprime(6)     # 2 * 3
    True
    >>> is_semiprime(9)     # 3 * 3
    True
    >>> is_semiprime(12)    # 2 * 2 * 3 — three factors
    False
    >>> is_semiprime(7)     # prime — one factor
    False

    Edge cases
    ----------
    * ``n <= 1`` returns ``False``.
    """
    if n <= 1:
        return False
    return len(prime_factors(n)) == 2
