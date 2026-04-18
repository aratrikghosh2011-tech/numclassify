"""
numclassify/_core/combinatorial.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Combinatorial number classification functions.

All membership sets are precomputed at module load time up to 10^9
(or 50 terms, whichever comes first) for O(1) lookup.
"""
from __future__ import annotations

from typing import Set

from numclassify._registry import register

_LIMIT = 10 ** 9
_MAX_TERMS = 50

# ---------------------------------------------------------------------------
# Precomputed sets
# ---------------------------------------------------------------------------

def _gen_factorials() -> Set[int]:
    s: Set[int] = set()
    k, val = 0, 1
    while val <= _LIMIT and k <= _MAX_TERMS:
        s.add(val)
        k += 1
        val *= k
    return s


def _gen_double_factorials() -> Set[int]:
    s: Set[int] = set()
    # k!! = k*(k-2)*...
    for k in range(0, 200):
        val = 1
        i = k
        while i > 0:
            val *= i
            i -= 2
        if val > _LIMIT:
            break
        s.add(val)
    return s


def _gen_subfactorials() -> Set[int]:
    s: Set[int] = set()
    # !0=1, !1=0, !n=(n-1)*(!{n-1}+!{n-2})
    a, b = 1, 0  # !0, !1
    s.add(a)
    s.add(b)
    for n in range(2, _MAX_TERMS + 1):
        c = (n - 1) * (a + b)
        if c > _LIMIT:
            break
        s.add(c)
        a, b = b, c
    return s


def _is_prime_simple(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    f = 5
    while f * f <= n:
        if n % f == 0 or n % (f + 2) == 0:
            return False
        f += 6
    return True


def _gen_primorials() -> Set[int]:
    s: Set[int] = set()
    val = 1
    n = 2
    while True:
        if _is_prime_simple(n):
            val *= n
            if val > _LIMIT:
                break
            s.add(val)
        n += 1
    return s


def _gen_central_binomials() -> Set[int]:
    s: Set[int] = set()
    # C(2k, k) for k = 0, 1, 2, ...
    val = 1
    k = 0
    while val <= _LIMIT and k <= _MAX_TERMS:
        s.add(val)
        k += 1
        # C(2k,k) = C(2(k-1),k-1) * 2*(2k-1)/k
        val = val * 2 * (2 * k - 1) // k
    return s


def _gen_binomial_coefficients() -> Set[int]:
    s: Set[int] = set()
    # Generate Pascal's triangle rows until values exceed _LIMIT
    row = [1]
    while True:
        for v in row:
            if v <= _LIMIT:
                s.add(v)
        next_row = [1]
        overflow = True
        for i in range(len(row) - 1):
            nv = row[i] + row[i + 1]
            next_row.append(nv)
            if nv <= _LIMIT:
                overflow = False
        next_row.append(1)
        if overflow and len(row) > 5:
            break
        row = next_row
        if len(row) > 1000:
            break
    return s


def _gen_partition_numbers() -> Set[int]:
    s: Set[int] = set()
    # Use Euler's pentagonal number theorem
    # p(n) = sum over k != 0 of (-1)^(k+1) * p(n - k*(3k-1)/2)
    # Build iteratively
    partitions = [1]  # p(0) = 1
    s.add(1)
    n = 1
    while True:
        total = 0
        k = 1
        while True:
            pent1 = k * (3 * k - 1) // 2
            pent2 = k * (3 * k + 1) // 2
            if pent1 > n:
                break
            sign = (-1) ** (k + 1)
            total += sign * partitions[n - pent1]
            if pent2 <= n:
                total += sign * partitions[n - pent2]
            k += 1
        partitions.append(total)
        if total > _LIMIT:
            break
        s.add(total)
        n += 1
        if n > 10000:
            break
    return s


def _gen_euler_numbers() -> Set[int]:
    # Euler numbers E_0=1, E_2=-1, E_4=5, E_6=-61, ... (all odd-indexed = 0)
    # We store absolute values of non-zero ones: 1, 1, 5, 61, 1385, ...
    s: Set[int] = set()
    # Use the recurrence via the Euler number triangle
    # E_n = 0 for odd n; for even n use: sum formula
    # Simple approach: build the alternating permutation triangle
    T = [[0] * 100 for _ in range(100)]
    T[1][1] = 1
    s.add(1)
    for i in range(2, 30):
        if i % 2 == 0:
            T[i][1] = T[i - 1][1]
            for j in range(2, i + 1):
                T[i][j] = T[i][j - 1] + T[i - 1][i - j + 1]
        else:
            T[i][i] = T[i - 1][i - 1]
            for j in range(i - 1, 0, -1):
                T[i][j] = T[i][j + 1] + T[i - 1][j]
        val = T[i][1] if i % 2 == 0 else T[i][i]
        if val > _LIMIT:
            break
        if val > 0:
            s.add(val)
    return s


# Known Bernoulli numerators (absolute values) — partial list
_BERNOULLI_NUMERATORS: Set[int] = {
    1, 1, 1, 1, 1, 5, 691, 7, 3617, 43867, 174611, 854513,
    236364091, 8553103, 23749461029, 8615841276005, 7709321041217,
    2577687858367
}


def _gen_catalan_triangle() -> Set[int]:
    s: Set[int] = set()
    # T(n,k) = C(n+k, k) - C(n+k, k-1) for 0 <= k <= n
    # T(n,0)=1 for all n; T(n,n) = Catalan(n)
    for n in range(0, 60):
        for k in range(0, n + 1):
            from math import comb
            val = comb(n + k, k) - (comb(n + k, k - 1) if k > 0 else 0)
            if val > _LIMIT:
                break
            s.add(val)
        if n > 0:
            from math import comb
            check = comb(2 * n, n) - comb(2 * n, n - 1) if n > 0 else 1
            if check > _LIMIT:
                break
    return s


# Build at module load time
_FACTORIALS: Set[int] = _gen_factorials()
_DOUBLE_FACTORIALS: Set[int] = _gen_double_factorials()
_SUBFACTORIALS: Set[int] = _gen_subfactorials()
_PRIMORIALS: Set[int] = _gen_primorials()
_CENTRAL_BINOMIALS: Set[int] = _gen_central_binomials()
_BINOMIAL_COEFFICIENTS: Set[int] = _gen_binomial_coefficients()
_PARTITION_NUMBERS: Set[int] = _gen_partition_numbers()
_EULER_NUMBERS: Set[int] = _gen_euler_numbers()
_CATALAN_TRIANGLE: Set[int] = _gen_catalan_triangle()

# ---------------------------------------------------------------------------
# Registered classifiers
# ---------------------------------------------------------------------------

@register(name="Factorial", category="combinatorial", oeis="A000142",
          description="n = k! for some non-negative integer k.")
def is_factorial(n: int) -> bool:
    """Return True if n is a factorial number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_factorial(24)
    True
    >>> is_factorial(25)
    False
    """
    return n >= 0 and n in _FACTORIALS


@register(name="Double Factorial", category="combinatorial", oeis="A006882",
          description="n = k!! for some non-negative integer k.")
def is_double_factorial(n: int) -> bool:
    """Return True if n is a double factorial number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _DOUBLE_FACTORIALS


@register(name="Subfactorial", category="combinatorial", oeis="A000166",
          description="n = !k (number of derangements of k elements).")
def is_subfactorial(n: int) -> bool:
    """Return True if n is a subfactorial (derangement number).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _SUBFACTORIALS


@register(name="Primorial", category="combinatorial", oeis="A002110",
          description="n = p# (product of all primes up to prime p).")
def is_primorial(n: int) -> bool:
    """Return True if n is a primorial.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 1 and n in _PRIMORIALS


@register(name="Central Binomial Coefficient", category="combinatorial", oeis="A000984",
          description="n = C(2k, k) for some non-negative integer k.")
def is_central_binomial(n: int) -> bool:
    """Return True if n is a central binomial coefficient C(2k, k).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _CENTRAL_BINOMIALS


@register(name="Binomial Coefficient", category="combinatorial", oeis="A007318",
          description="n = C(a, b) for some integers a >= b >= 0.")
def is_binomial_coefficient(n: int) -> bool:
    """Return True if n appears in Pascal's triangle.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _BINOMIAL_COEFFICIENTS


@register(name="Partition Number", category="combinatorial", oeis="A000041",
          description="n = p(k), the number of integer partitions of k.")
def is_partition_number(n: int) -> bool:
    """Return True if n is an integer partition number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _PARTITION_NUMBERS


@register(name="Euler Number", category="combinatorial", oeis="A122045",
          description="n is an absolute value of an Euler number.")
def is_euler_number(n: int) -> bool:
    """Return True if n is (the absolute value of) an Euler number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _EULER_NUMBERS


@register(name="Bernoulli Numerator", category="combinatorial",
          description="n appears as the numerator of a Bernoulli number (partial list).")
def is_bernoulli_numerator(n: int) -> bool:
    """Return True if n appears as a Bernoulli number numerator (partial known list).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _BERNOULLI_NUMERATORS


@register(name="Catalan Triangle", category="combinatorial", oeis="A009766",
          description="n appears in Catalan's triangle T(n,k) = C(n+k,k) - C(n+k,k-1).")
def is_catalan_triangle(n: int) -> bool:
    """Return True if n appears in Catalan's triangle.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _CATALAN_TRIANGLE
