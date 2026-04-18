"""
numclassify/_core/number_theory.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Number-theoretic classifiers plus math utility functions.

Registered classifiers appear in the global registry.
Math utilities (euler_totient, mobius, gcd, lcm, mod_pow, mod_inv) are
NOT registered but are importable by other modules.
"""
from __future__ import annotations

import math
from typing import List

from numclassify._registry import register

# ---------------------------------------------------------------------------
# Math utilities (NOT registered)
# ---------------------------------------------------------------------------

def euler_totient(n: int) -> int:
    """Return Euler's totient φ(n): count of integers 1..n coprime to n.

    Parameters
    ----------
    n : int

    Returns
    -------
    int
    """
    if n < 1:
        return 0
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def mobius(n: int) -> int:
    """Return the Möbius function μ(n).

    Returns 0 if n has a squared prime factor, otherwise (-1)^k
    where k is the number of distinct prime factors.

    Parameters
    ----------
    n : int

    Returns
    -------
    int
    """
    if n < 1:
        return 0
    if n == 1:
        return 1
    k = 0
    f = 2
    while f * f <= n:
        if n % f == 0:
            k += 1
            n //= f
            if n % f == 0:
                return 0  # squared factor
        f += 1
    if n > 1:
        k += 1
    return (-1) ** k


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of a and b.

    Parameters
    ----------
    a : int
    b : int

    Returns
    -------
    int
    """
    return math.gcd(a, b)


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of a and b.

    Parameters
    ----------
    a : int
    b : int

    Returns
    -------
    int
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def mod_pow(base: int, exp: int, mod: int) -> int:
    """Return base^exp % mod using fast modular exponentiation.

    Parameters
    ----------
    base : int
    exp : int
    mod : int

    Returns
    -------
    int
    """
    return pow(base, exp, mod)


def mod_inv(a: int, mod: int) -> int:
    """Return the modular inverse of a mod m (requires gcd(a,m)=1).

    Parameters
    ----------
    a : int
    mod : int

    Returns
    -------
    int
    """
    return pow(a, -1, mod)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _is_prime(n: int) -> bool:
    """Miller-Rabin primality (local to avoid circular import)."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))


# ---------------------------------------------------------------------------
# Registered classifiers
# ---------------------------------------------------------------------------

@register(name="Evil", category="number theory", oeis="A001969",
          description="Has an even number of 1s in its binary representation.")
def is_evil(n: int) -> bool:
    """Return True if n has an even number of 1-bits (evil number).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_evil(9)   # 1001 -> two 1s
    True
    >>> is_evil(7)   # 111  -> three 1s
    False
    """
    return n >= 0 and bin(n).count("1") % 2 == 0


@register(name="Odious", category="number theory", oeis="A000069",
          description="Has an odd number of 1s in its binary representation.")
def is_odious(n: int) -> bool:
    """Return True if n has an odd number of 1-bits (odious number).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and bin(n).count("1") % 2 == 1


@register(name="Pernicious", category="number theory", oeis="A052294",
          description="The number of 1s in binary representation is prime.")
def is_pernicious(n: int) -> bool:
    """Return True if the popcount of n is a prime number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and _is_prime(bin(n).count("1"))


@register(name="Blum Integer", category="number theory", oeis="A016105",
          description="Semiprime n=p*q where both p and q are ≡ 3 mod 4.")
def is_blum_integer(n: int) -> bool:
    """Return True if n is a Blum integer (semiprime p*q, p≡q≡3 mod 4, p≠q).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 15:
        return False
    # Find first prime factor
    f = 2
    while f * f <= n:
        if n % f == 0:
            p = f
            q = n // f
            # Must be semiprime: q must be prime and p != q
            if q != p and _is_prime(p) and _is_prime(q):
                return p % 4 == 3 and q % 4 == 3
            return False
        f += 1
    return False


@register(name="Carmichael", category="number theory", oeis="A002997",
          description="Composite n satisfying Fermat's little theorem for all coprime bases.")
def is_carmichael(n: int) -> bool:
    """Return True if n is a Carmichael number (Korselt's criterion).

    n is Carmichael iff: composite, squarefree, and for every prime p|n, (p-1)|(n-1).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_carmichael(561)
    True
    """
    if n < 2 or _is_prime(n):
        return False
    # Must be squarefree
    temp = n
    f = 2
    factors: List[int] = []
    while f * f <= temp:
        if temp % f == 0:
            factors.append(f)
            temp //= f
            if temp % f == 0:
                return False  # not squarefree
        f += 1
    if temp > 1:
        factors.append(temp)
    # Korselt: (p-1) | (n-1) for each prime factor p
    for p in factors:
        if (n - 1) % (p - 1) != 0:
            return False
    return len(factors) >= 2


@register(name="Primary Pseudoprime", category="number theory", oeis="A001567",
          description="Composite number that passes the Fermat test for base 2.")
def is_primary_pseudoprime(n: int) -> bool:
    """Return True if n is a base-2 Fermat pseudoprime (composite, 2^(n-1) ≡ 1 mod n).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 4 or _is_prime(n):
        return False
    return pow(2, n - 1, n) == 1


@register(name="Perfect Totient", category="number theory", oeis="A082897",
          description="n equals the sum of its iterated totients until reaching 1.")
def is_perfect_totient(n: int) -> bool:
    """Return True if n equals the sum of iterated Euler totients until reaching 1.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 3:
        return False
    total = 0
    k = euler_totient(n)
    while k >= 1:
        total += k
        if total > n:
            return False
        if k == 1:
            break
        k = euler_totient(k)
    return total == n


@register(name="Giuga", category="number theory", oeis="A007850",
          description="Composite n where for each prime p|n, p divides (n/p - 1).")
def is_giuga(n: int) -> bool:
    """Return True if n is a Giuga number.

    n is Giuga iff composite and for each prime p dividing n, p | (n/p - 1).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 2 or _is_prime(n):
        return False
    temp = n
    f = 2
    while f * f <= temp:
        if temp % f == 0:
            if (n // f - 1) % f != 0:
                return False
            while temp % f == 0:
                temp //= f
        f += 1
    if temp > 1:
        if (n // temp - 1) % temp != 0:
            return False
    return True


@register(name="Self Number", category="number theory", oeis="A003052",
          description="Cannot be expressed as k + digit_sum(k) for any k.")
def is_self_number(n: int) -> bool:
    """Return True if n is a self number (Colombian number).

    n is self iff no integer k satisfies k + digit_sum(k) = n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_self_number(20)
    True
    >>> is_self_number(21)
    False
    """
    if n < 1:
        return False
    # k + digit_sum(k) = n  =>  k is in range [n - 9*len(str(n)), n)
    digits_n = len(str(n))
    for k in range(max(1, n - 9 * digits_n), n):
        if k + _digit_sum(k) == n:
            return False
    return True


@register(name="Colombian", category="number theory", oeis="A003052",
          description="Alias for self number: cannot be expressed as k + digit_sum(k).")
def is_colombian(n: int) -> bool:
    """Return True if n is a Colombian (self) number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return is_self_number(n)


@register(name="Keith", category="number theory", oeis="A007629",
          description="Starts with its own digits; each subsequent term is sum of previous n terms.")
def is_keith(n: int) -> bool:
    """Return True if n is a Keith number.

    Example: 14 → sequence 1,4,5,9,14 (each term = sum of previous 2).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_keith(14)
    True
    >>> is_keith(15)
    False
    """
    if n < 10:
        return False
    digits = [int(d) for d in str(n)]
    seq = list(digits)
    while seq[-1] < n:
        seq.append(sum(seq[-len(digits):]))
    return seq[-1] == n


@register(name="Autobiographical", category="number theory", oeis="A046043",
          description="Digit i counts how many times i appears in n.")
def is_autobiographical(n: int) -> bool:
    """Return True if n is an autobiographical (self-describing) number.

    Digit at position i (0-indexed) equals the count of digit i in n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_autobiographical(1210)
    True
    >>> is_autobiographical(1211)
    False
    """
    s = str(n)
    k = len(s)
    for i, ch in enumerate(s):
        if s.count(str(i)) != int(ch):
            return False
    return True


@register(name="Narcissistic", category="number theory", oeis="A005188",
          description="Alias for Armstrong: sum of digits each raised to number of digits equals n.")
def is_narcissistic(n: int) -> bool:
    """Return True if n is a narcissistic (Armstrong) number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    digits = str(n)
    k = len(digits)
    return sum(int(d) ** k for d in digits) == n


@register(name="Perfect Digital Invariant", category="number theory", oeis="A023052",
          description="Sum of digits raised to some fixed power k equals n.")
def is_perfect_digital_invariant(n: int) -> bool:
    """Return True if sum(d^k for d in digits(n)) == n for some k >= 1.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    digits = [int(d) for d in str(n)]
    max_k = len(str(n)) + 3  # generous upper bound
    for k in range(1, max_k + 1):
        if sum(d ** k for d in digits) == n:
            return True
    return False
