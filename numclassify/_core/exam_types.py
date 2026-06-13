"""
numclassify._core.exam_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Number types frequently asked in school/college Python exams (ICSE, CBSE,
competitive programming, interview prep). All functions registered via @register.

Types added:
- Strong Number
- Sunny Number
- Buzz Number
- Magic Number
- Fascinating Number
- Trimorphic Number
- Twisted Prime
- Unique Number (no repeated digits)
"""
from __future__ import annotations

import math
from typing import List

from numclassify._registry import register
from numclassify._core.primes import is_prime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))


def _is_perfect_square_exact(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


# ---------------------------------------------------------------------------
# Strong Number
# ---------------------------------------------------------------------------

@register(
    name="Strong",
    category="digital",
    oeis="A014080",
    description=(
        "A number equal to the sum of the factorials of its digits. "
        "Also called a factorion. Examples: 1, 2, 145, 40585."
    ),
    aliases=["strong_number", "factorion"],
)
def is_strong(n: int) -> bool:
    """Return True if n equals the sum of the factorials of its digits.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_strong(145)   # 1! + 4! + 5! = 1 + 24 + 120 = 145
    True
    >>> is_strong(2)     # 2! = 2
    True
    >>> is_strong(40585)
    True
    >>> is_strong(100)
    False
    """
    if n <= 0:
        return False
    return sum(math.factorial(int(d)) for d in str(n)) == n


# ---------------------------------------------------------------------------
# Sunny Number
# ---------------------------------------------------------------------------

@register(
    name="Sunny",
    category="sequences",
    oeis="A005563",
    description=(
        "A number n where n+1 is a perfect square. "
        "Examples: 3, 8, 15, 24, 35, 48."
    ),
    aliases=["sunny_number"],
)
def is_sunny(n: int) -> bool:
    """Return True if n+1 is a perfect square.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_sunny(3)    # 3+1 = 4 = 2^2
    True
    >>> is_sunny(8)    # 8+1 = 9 = 3^2
    True
    >>> is_sunny(24)   # 24+1 = 25 = 5^2
    True
    >>> is_sunny(5)    # 5+1 = 6, not a perfect square
    False
    """
    if n <= 0:
        return False
    return _is_perfect_square_exact(n + 1)


# ---------------------------------------------------------------------------
# Buzz Number
# ---------------------------------------------------------------------------

@register(
    name="Buzz",
    category="recreational",
    description=(
        "A number divisible by 7 or ending in 7 (or both). "
        "Named after the Buzz game where players say 'buzz' for such numbers."
    ),
    aliases=["buzz_number"],
)
def is_buzz(n: int) -> bool:
    """Return True if n is divisible by 7 or ends in the digit 7.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_buzz(7)    # divisible by 7 and ends in 7
    True
    >>> is_buzz(14)   # divisible by 7
    True
    >>> is_buzz(17)   # ends in 7
    True
    >>> is_buzz(10)
    False
    """
    if n <= 0:
        return False
    return n % 7 == 0 or n % 10 == 7


# ---------------------------------------------------------------------------
# Magic Number
# ---------------------------------------------------------------------------

@register(
    name="Magic",
    category="digital",
    description=(
        "A number whose repeated digit sum (digital root) equals 1. "
        "Examples: 1, 10, 19, 28, 100."
    ),
    aliases=["magic_number"],
)
def is_magic(n: int) -> bool:
    """Return True if the digital root of n equals 1.

    Repeatedly sum the digits until a single digit remains.
    If that digit is 1, the number is magic.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_magic(1)
    True
    >>> is_magic(10)   # 1+0 = 1
    True
    >>> is_magic(19)   # 1+9=10, 1+0=1
    True
    >>> is_magic(28)   # 2+8=10, 1+0=1
    True
    >>> is_magic(12)   # 1+2=3 ≠ 1
    False
    """
    if n <= 0:
        return False
    while n >= 10:
        n = _digit_sum(n)
    return n == 1


# ---------------------------------------------------------------------------
# Fascinating Number
# ---------------------------------------------------------------------------

@register(
    name="Fascinating",
    category="digital",
    description=(
        "A 3-digit number n where the concatenation of n, 2n, and 3n "
        "contains all digits 1-9 exactly once (no zeros, no repeats). "
        "Examples: 192, 219, 273, 327, 192."
    ),
    aliases=["fascinating_number"],
)
def is_fascinating(n: int) -> bool:
    """Return True if n is a fascinating number.

    For a 3-digit n, concatenate str(n) + str(2*n) + str(3*n).
    The result must use each digit 1-9 exactly once and contain no 0.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_fascinating(192)   # '192' + '384' + '576' = '192384576'
    True
    >>> is_fascinating(273)   # '273' + '546' + '819' = '273546819'
    True
    >>> is_fascinating(100)
    False
    >>> is_fascinating(123)
    False

    Notes
    -----
    Only 3-digit numbers qualify by definition. Numbers outside [100, 999]
    always return False.
    """
    if n < 100 or n > 999:
        return False
    s = str(n) + str(2 * n) + str(3 * n)
    return len(s) == 9 and set(s) == set('123456789')


# ---------------------------------------------------------------------------
# Trimorphic Number
# ---------------------------------------------------------------------------

@register(
    name="Trimorphic",
    category="digital",
    description=(
        "A number whose cube ends with the number itself. "
        "Examples: 1, 5, 6, 25, 76, 376."
    ),
    aliases=["trimorphic_number", "automorphic_cube"],
)
def is_trimorphic(n: int) -> bool:
    """Return True if n^3 ends with n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_trimorphic(5)    # 5^3 = 125, ends in 5
    True
    >>> is_trimorphic(25)   # 25^3 = 15625, ends in 25
    True
    >>> is_trimorphic(376)  # 376^3 = 53157376, ends in 376
    True
    >>> is_trimorphic(4)    # 4^3 = 64, does not end in 4
    False

    Notes
    -----
    n <= 0 always returns False.
    """
    if n <= 0:
        return False
    return str(n ** 3).endswith(str(n))


# ---------------------------------------------------------------------------
# Twisted Prime
# ---------------------------------------------------------------------------

@register(
    name="Twisted Prime",
    category="primes",
    description=(
        "A prime number whose digit sum is also prime. "
        "Examples: 2, 3, 5, 7, 11, 23, 29, 41."
    ),
    aliases=["twisted_prime"],
)
def is_twisted_prime(n: int) -> bool:
    """Return True if n is prime and the sum of its digits is also prime.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_twisted_prime(2)    # prime, digit sum 2 (prime)
    True
    >>> is_twisted_prime(23)   # prime, digit sum 5 (prime)
    True
    >>> is_twisted_prime(13)   # prime, digit sum 4 (not prime)
    False
    >>> is_twisted_prime(29)   # prime, digit sum 11 (prime)
    True
    """
    if not is_prime(n):
        return False
    return is_prime(_digit_sum(n))


# ---------------------------------------------------------------------------
# Unique Number
# ---------------------------------------------------------------------------

@register(
    name="Unique",
    category="digital",
    description=(
        "A number with no repeated digits. "
        "Examples: 1, 12, 123, 1234, 9876543210."
    ),
    aliases=["unique_number", "unique_digit"],
)
def is_unique(n: int) -> bool:
    """Return True if n has no repeated digits.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_unique(1234)    # all digits distinct
    True
    >>> is_unique(1123)    # digit 1 repeated
    False
    >>> is_unique(9876)
    True
    >>> is_unique(0)
    True
    >>> is_unique(-5)      # negative numbers are not unique
    False

    Notes
    -----
    Single-digit numbers and 0 are always unique.
    """
    if n < 0:
        return False
    s = str(abs(n))
    return len(s) == len(set(s))
