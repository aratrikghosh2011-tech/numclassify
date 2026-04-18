"""
numclassify/_core/powers.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Power-based number classification functions.
"""
from __future__ import annotations

import math
from typing import Set

from numclassify._registry import register

# ---------------------------------------------------------------------------
# Helper (NOT registered)
# ---------------------------------------------------------------------------

def is_perfect_power_check(n: int, exp: int) -> bool:
    """Return True if n is a perfect exp-th power (n = k^exp for integer k > 0).

    Parameters
    ----------
    n : int
    exp : int

    Returns
    -------
    bool
    """
    if n < 0 or exp < 2:
        return False
    if n == 0 or n == 1:
        return True
    root = round(n ** (1.0 / exp))
    for r in range(max(1, root - 2), root + 3):
        if r ** exp == n:
            return True
    return False


# ---------------------------------------------------------------------------
# Registered classifiers
# ---------------------------------------------------------------------------

@register(name="Perfect Square", category="powers", oeis="A000290",
          description="n = k^2 for some non-negative integer k.")
def is_perfect_square(n: int) -> bool:
    """Return True if n is a perfect square.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_perfect_square(16)
    True
    >>> is_perfect_square(15)
    False
    """
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


@register(name="Perfect Cube", category="powers", oeis="A000578",
          description="n = k^3 for some positive integer k.")
def is_perfect_cube(n: int) -> bool:
    """Return True if n is a perfect cube.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_perfect_cube(27)
    True
    >>> is_perfect_cube(26)
    False
    """
    if n < 0:
        return False
    return is_perfect_power_check(n, 3)


@register(name="Perfect Fourth Power", category="powers", oeis="A000583",
          description="n = k^4 for some positive integer k.")
def is_perfect_fourth(n: int) -> bool:
    """Return True if n is a perfect fourth power.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 0:
        return False
    return is_perfect_power_check(n, 4)


@register(name="Perfect Fifth Power", category="powers", oeis="A000584",
          description="n = k^5 for some positive integer k.")
def is_perfect_fifth(n: int) -> bool:
    """Return True if n is a perfect fifth power.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 0:
        return False
    return is_perfect_power_check(n, 5)


@register(name="Perfect Power", category="powers", oeis="A001597",
          description="n = k^m for some integers k > 1, m > 1.")
def is_perfect_power(n: int) -> bool:
    """Return True if n is a perfect power (k^m, k>1, m>1).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n <= 1:
        return False
    for exp in range(2, n.bit_length() + 1):
        if is_perfect_power_check(n, exp):
            return True
    return False


@register(name="Sum of Two Squares", category="powers", oeis="A001481",
          description="n = a^2 + b^2 for non-negative integers a, b.")
def is_sum_of_two_squares(n: int) -> bool:
    """Return True if n can be expressed as the sum of two squares.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_sum_of_two_squares(5)
    True
    >>> is_sum_of_two_squares(3)
    False
    """
    if n < 0:
        return False
    a = 0
    while a * a <= n:
        remainder = n - a * a
        b = math.isqrt(remainder)
        if b * b == remainder:
            return True
        a += 1
    return False


@register(name="Sum of Two Cubes", category="powers", oeis="A003325",
          description="n = a^3 + b^3 for positive integers a, b.")
def is_sum_of_two_cubes(n: int) -> bool:
    """Return True if n can be expressed as the sum of two positive cubes.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 2:
        return False
    a = 1
    while a ** 3 < n:
        remainder = n - a ** 3
        b = round(remainder ** (1.0 / 3))
        for r in range(max(1, b - 1), b + 2):
            if r ** 3 == remainder:
                return True
        a += 1
    return False


@register(name="Sum of Three Squares", category="powers", oeis="A000443",
          description="n = a^2 + b^2 + c^2 (by Legendre's three-square theorem).")
def is_sum_of_three_squares(n: int) -> bool:
    """Return True if n can be expressed as the sum of three squares.

    Uses Legendre's three-square theorem: n is NOT expressible iff
    n = 4^a * (8b + 7) for non-negative integers a, b.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 0:
        return False
    # Remove factors of 4
    while n % 4 == 0:
        n //= 4
    return n % 8 != 7


@register(name="Taxicab", category="powers", oeis="A001235",
          description="Expressible as sum of two cubes in at least 2 different ways.")
def is_taxicab(n: int) -> bool:
    """Return True if n can be expressed as the sum of two positive cubes in ≥ 2 ways.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_taxicab(1729)
    True
    """
    if n < 2:
        return False
    ways = 0
    a = 1
    while a ** 3 < n:
        remainder = n - a ** 3
        b = round(remainder ** (1.0 / 3))
        for r in range(max(1, b - 1), b + 2):
            if r >= a and r ** 3 == remainder:
                ways += 1
                break
        a += 1
    return ways >= 2


@register(name="Power of 2", category="powers", oeis="A000079",
          description="n = 2^k for some non-negative integer k.")
def is_power_of_2(n: int) -> bool:
    """Return True if n is a power of 2.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n > 0 and (n & (n - 1)) == 0


@register(name="Power of 3", category="powers", oeis="A000244",
          description="n = 3^k for some non-negative integer k.")
def is_power_of_3(n: int) -> bool:
    """Return True if n is a power of 3.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1


@register(name="Power of 10", category="powers", oeis="A011557",
          description="n = 10^k for some non-negative integer k.")
def is_power_of_10(n: int) -> bool:
    """Return True if n is a power of 10.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    while n % 10 == 0:
        n //= 10
    return n == 1


@register(name="Sum of Squares of Primes", category="powers",
          description="n = p1^2 + p2^2 for primes p1, p2.")
def is_sum_of_squares_of_primes(n: int) -> bool:
    """Return True if n = p1^2 + p2^2 for primes p1, p2.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 4:
        return False
    from numclassify._core.primes import is_prime
    limit = math.isqrt(n)
    p1 = 2
    while p1 <= limit:
        if is_prime(p1):
            remainder = n - p1 * p1
            if remainder > 0:
                p2 = math.isqrt(remainder)
                if p2 * p2 == remainder and is_prime(p2):
                    return True
        p1 += 1 if p1 == 2 else 2
    return False
