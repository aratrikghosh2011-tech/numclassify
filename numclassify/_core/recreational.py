"""
numclassify._core.recreational
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Recreational / curiosity number classifications.

All functions are registered via ``@register`` and exposed as plain
module-level callables.
"""

from __future__ import annotations

from numclassify._registry import register


@register(
    name="Kaprekar",
    category="recreational",
    oeis="A006886",
    description=(
        "A number n such that n² can be split into two parts (no leading zero "
        "on the right part) that sum to n.  n=1 is included by convention."
    ),
    aliases=["kaprekar number"],
)
def is_kaprekar(n: int) -> bool:
    """Return ``True`` if *n* is a Kaprekar number.

    A positive integer *n* is Kaprekar if its square ``n²`` can be partitioned
    at some point into a left part *A* and a right part *B* (where *B* > 0 and
    has no leading zero) such that ``A + B == n``.

    Special case: *n* = 1 is Kaprekar by convention (1² = 1, split as 0 + 1).

    Parameters
    ----------
    n:
        Positive integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_kaprekar(45)   # 45²=2025; split (20, 25) → 20+25=45
    True
    >>> is_kaprekar(9)    # 9²=81; split (8, 1) → 8+1=9
    True
    >>> is_kaprekar(1)
    True
    >>> is_kaprekar(100)
    False
    """
    if n <= 0:
        return False
    if n == 1:
        return True
    sq = n * n
    sq_str = str(sq)
    length = len(sq_str)
    for split in range(1, length):
        left_str = sq_str[:length - split]
        right_str = sq_str[length - split:]
        # Right part must not start with '0' (leading zero check)
        if right_str[0] == "0":
            continue
        left = int(left_str) if left_str else 0
        right = int(right_str)
        if right > 0 and left + right == n:
            return True
    return False


@register(
    name="Automorphic",
    category="recreational",
    oeis="A003226",
    description="A number whose square ends in the number itself.",
    aliases=["automorphic number"],
)
def is_automorphic(n: int) -> bool:
    """Return ``True`` if *n* is an automorphic number.

    An automorphic number satisfies: the last *k* digits of *n²* equal *n*,
    where *k* is the number of digits in *n*.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_automorphic(5)    # 5²=25, ends in 5
    True
    >>> is_automorphic(6)    # 6²=36, ends in 6
    True
    >>> is_automorphic(76)   # 76²=5776, ends in 76
    True
    >>> is_automorphic(7)    # 7²=49, does not end in 7
    False
    """
    if n < 0:
        return False
    sq = n * n
    n_str = str(n)
    sq_str = str(sq)
    return sq_str.endswith(n_str)


@register(
    name="Palindrome",
    category="recreational",
    oeis="A002113",
    description=(
        "A number whose decimal representation reads the same forwards and "
        "backwards."
    ),
    aliases=["palindromic", "palindromic number"],
)
def is_palindrome(n: int) -> bool:
    """Return ``True`` if *n* is a palindromic number.

    A palindromic number reads the same in both directions in base-10.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_palindrome(121)
    True
    >>> is_palindrome(1221)
    True
    >>> is_palindrome(123)
    False
    """
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]


@register(
    name="Strobogrammatic",
    category="recreational",
    oeis="",
    description=(
        "A number that looks the same when rotated 180°. "
        "Valid digits are 0, 1, 6, 8, 9 with map 0→0, 1→1, 6→9, 8→8, 9→6."
    ),
    aliases=["strobogrammatic number"],
)
def is_strobogrammatic(n: int) -> bool:
    """Return ``True`` if *n* is a strobogrammatic number.

    A strobogrammatic number appears the same when rotated 180°.  Only the
    digits 0, 1, 6, 8, 9 are valid; their rotated equivalents are
    0→0, 1→1, 6→9, 8→8, 9→6.  The rotated string is the reverse of the
    mapped digits.

    Parameters
    ----------
    n:
        Non-negative integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_strobogrammatic(69)   # 69 rotated → 96... wait: 6→9, 9→6; reversed: '96' → same as '96' ✓
    True
    >>> is_strobogrammatic(88)
    True
    >>> is_strobogrammatic(1)
    True
    >>> is_strobogrammatic(6)    # 6 alone rotated → '9' ≠ '6'
    False
    """
    if n < 0:
        return False
    rotate_map = {"0": "0", "1": "1", "6": "9", "8": "8", "9": "6"}
    s = str(n)
    for ch in s:
        if ch not in rotate_map:
            return False
    rotated = "".join(rotate_map[ch] for ch in reversed(s))
    return rotated == s


@register(
    name="Bouncy",
    category="recreational",
    oeis="A152054",
    description=(
        "A positive integer whose digits are neither all non-decreasing nor "
        "all non-increasing."
    ),
    aliases=["bouncy number"],
)
def is_bouncy(n: int) -> bool:
    """Return ``True`` if *n* is a bouncy number.

    A bouncy number has digits that are neither monotonically non-decreasing
    nor monotonically non-increasing.  Numbers with fewer than three digits
    can never be bouncy.

    Parameters
    ----------
    n:
        Positive integer.

    Returns
    -------
    bool

    Example
    -------
    >>> is_bouncy(155349)
    True
    >>> is_bouncy(134468)   # non-decreasing → not bouncy
    False
    >>> is_bouncy(66420)    # non-increasing → not bouncy
    False
    """
    if n <= 0:
        return False
    digits = [int(d) for d in str(n)]
    if len(digits) < 3:
        return False
    increasing = any(digits[i] < digits[i + 1] for i in range(len(digits) - 1))
    decreasing = any(digits[i] > digits[i + 1] for i in range(len(digits) - 1))
    return increasing and decreasing
