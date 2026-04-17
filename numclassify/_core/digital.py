"""
numclassify._core.digital
~~~~~~~~~~~~~~~~~~~~~~~~~
Digital (digit-based) number classification functions.

Helper functions ``digit_sum`` and ``digital_root`` are provided as plain
module-level utilities and are **not** registered (they return integers, not
booleans).  All boolean predicates are registered via ``@register``.
"""

from __future__ import annotations

from functools import reduce
from typing import List

from numclassify._registry import register


# ---------------------------------------------------------------------------
# Helpers (not registered — return int, not bool)
# ---------------------------------------------------------------------------

def digit_sum(n: int) -> int:
    """Return the sum of the decimal digits of *n*.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    int

    Example
    -------
    >>> digit_sum(493)
    16
    >>> digit_sum(0)
    0
    """
    return sum(int(d) for d in str(abs(n)))


def digital_root(n: int) -> int:
    """Return the digital root of *n* (repeated digit sum until single digit).

    For *n* = 0 the digital root is 0.  For *n* > 0, ``digital_root(n)`` is
    equivalent to ``1 + (n - 1) % 9``.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    int in [0, 9]

    Example
    -------
    >>> digital_root(493)
    7
    >>> digital_root(0)
    0
    """
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


# ---------------------------------------------------------------------------
# Boolean predicates — all registered
# ---------------------------------------------------------------------------

@register(
    name="Armstrong",
    category="digital",
    oeis="A005188",
    description=(
        "A number equal to the sum of its own digits each raised to the power "
        "of the number of digits (narcissistic number)."
    ),
    aliases=["narcissistic", "pluperfect digital invariant"],
)
def is_armstrong(n: int) -> bool:
    """Return ``True`` if *n* is an Armstrong (narcissistic) number.

    For a *d*-digit number, ``is_armstrong(n)`` iff
    ``n == sum(digit^d for digit in digits(n))``.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_armstrong(153)   # 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153
    True
    >>> is_armstrong(370)
    True
    >>> is_armstrong(100)
    False
    """
    if n < 0:
        return False
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n


@register(
    name="Spy",
    category="digital",
    oeis="A059716",
    description=(
        "A number whose digit sum equals its digit product. "
        "All single-digit numbers are spy numbers (sum = digit = product)."
    ),
    aliases=["spy number"],
)
def is_spy(n: int) -> bool:
    """Return ``True`` if *n* is a spy number.

    A spy number satisfies ``digit_sum(n) == digit_product(n)``.
    Single-digit numbers (0–9) trivially qualify because their digit sum and
    digit product are both equal to the digit itself.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_spy(1124)   # 1+1+2+4=8  and  1*1*2*4=8
    True
    >>> is_spy(5)      # single digit: sum=5=product
    True
    >>> is_spy(123)    # sum=6, product=6  →  True
    True
    >>> is_spy(124)    # sum=7, product=8  →  False
    False
    """
    if n < 0:
        return False
    digits = [int(d) for d in str(n)]
    s = sum(digits)
    p = 1
    for d in digits:
        p *= d
    return s == p


@register(
    name="Harshad",
    category="digital",
    oeis="A005349",
    description=(
        "A number divisible by its own digit sum (also called a Niven number)."
    ),
    aliases=["niven", "harshad number", "niven number"],
)
def is_harshad(n: int) -> bool:
    """Return ``True`` if *n* is a Harshad (Niven) number.

    A Harshad number is divisible by its digit sum: ``n % digit_sum(n) == 0``.

    Parameters
    ----------
    n:
        Positive integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_harshad(18)   # digit_sum=9, 18 % 9 == 0
    True
    >>> is_harshad(19)   # digit_sum=10, 19 % 10 != 0
    False
    """
    if n <= 0:
        return False
    ds = digit_sum(n)
    if ds == 0:
        return False
    return n % ds == 0


@register(
    name="Disarium",
    category="digital",
    oeis="A032799",
    description=(
        "A number equal to the sum of its digits each raised to the power of "
        "their 1-based position from the left."
    ),
    aliases=["disarium number"],
)
def is_disarium(n: int) -> bool:
    """Return ``True`` if *n* is a Disarium number.

    For digits ``d₁ d₂ … dₖ`` (1-indexed from the left),
    ``is_disarium(n)`` iff ``n == d₁¹ + d₂² + … + dₖᵏ``.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_disarium(135)   # 1^1 + 3^2 + 5^3 = 1 + 9 + 125 = 135
    True
    >>> is_disarium(89)    # 8^1 + 9^2 = 8 + 81 = 89
    True
    >>> is_disarium(136)
    False
    """
    if n < 0:
        return False
    digits = [int(d) for d in str(n)]
    return sum(d ** (i + 1) for i, d in enumerate(digits)) == n


@register(
    name="Happy",
    category="digital",
    oeis="A007770",
    description=(
        "A number that eventually reaches 1 under iteration of the sum-of-"
        "squared-digits map."
    ),
    aliases=["happy number"],
)
def is_happy(n: int) -> bool:
    """Return ``True`` if *n* is a happy number.

    Starting from *n*, repeatedly replace the number by the sum of the squares
    of its digits.  If the process reaches 1, *n* is happy.  Otherwise it
    enters a cycle not including 1 (the cycle always contains 4 for unhappy
    numbers).

    Cycle detection uses a *seen* set.

    Parameters
    ----------
    n:
        Positive integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_happy(19)   # 1²+9²=82 → 8²+2²=68 → … → 1
    True
    >>> is_happy(4)    # enters cycle: 4→16→37→58→89→145→42→20→4
    False
    """
    if n <= 0:
        return False
    seen = set()
    current = n
    while current != 1:
        if current in seen:
            return False
        seen.add(current)
        current = sum(int(d) ** 2 for d in str(current))
    return True


@register(
    name="Neon",
    category="digital",
    oeis="A208854",
    description=(
        "A number whose digit sum equals the number itself when applied to n²."
    ),
    aliases=["neon number"],
)
def is_neon(n: int) -> bool:
    """Return ``True`` if *n* is a neon number.

    A neon number satisfies ``digit_sum(n²) == n``.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_neon(9)    # 9² = 81, digit_sum(81) = 9
    True
    >>> is_neon(1)    # 1² = 1, digit_sum(1) = 1
    True
    >>> is_neon(2)    # 2² = 4, digit_sum(4) = 4 ≠ 2
    False
    """
    if n < 0:
        return False
    return digit_sum(n * n) == n


@register(
    name="Duck",
    category="digital",
    oeis="",
    description=(
        "A positive number that contains the digit 0 but does not start with 0."
    ),
    aliases=["duck number"],
)
def is_duck(n: int) -> bool:
    """Return ``True`` if *n* is a duck number.

    A duck number is a positive integer that contains at least one digit ``0``
    and does not have a leading zero (i.e. it is not zero itself).

    Parameters
    ----------
    n:
        Integer to test.

    Returns
    -------
    bool

    Example
    -------
    >>> is_duck(1230)
    True
    >>> is_duck(1234)
    False
    >>> is_duck(100)
    True
    """
    if n <= 0:
        return False
    s = str(n)
    return "0" in s  # leading zero is impossible for n > 0 as int


@register(
    name="Nude",
    category="digital",
    oeis="",
    description=(
        "A number divisible by each of its non-zero digits."
    ),
    aliases=["nude number"],
)
def is_nude(n: int) -> bool:
    """Return ``True`` if *n* is a nude number.

    A nude number is divisible by every one of its non-zero digits.

    Parameters
    ----------
    n:
        Positive integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_nude(12)   # 12 % 1 == 0 and 12 % 2 == 0
    True
    >>> is_nude(13)   # 13 % 3 != 0
    False
    >>> is_nude(36)   # 36 % 3 == 0 and 36 % 6 == 0
    True
    """
    if n <= 0:
        return False
    digits = [int(d) for d in str(n) if d != "0"]
    if not digits:
        return False
    return all(n % d == 0 for d in digits)
