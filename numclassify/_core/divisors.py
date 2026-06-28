"""
numclassify/_core/divisors.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Divisor-based number classification functions.

Complexity caveats
------------------
- is_semiperfect and is_zumkeller use bitmask DP (Python big-int bitset).
  This is efficient for numbers with many divisors but the bitmask grows
  with the target sum, so very large semiperfect/zumkeller candidates may
  still be slow.
- is_untouchable is fully precomputed for n <= 10_000.
  For n in (10_000, 500_000] it uses a sigma-based exhaustive sieve over
  [2, 2n].  n > 500_000 raises ValueError because [2, 2n] is
  computationally infeasible at that range.
"""
from __future__ import annotations

import math
from typing import List, Set

from numclassify._registry import register
from numclassify._explain_templates import factorization_template

# ---------------------------------------------------------------------------
# Helpers (NOT registered)
# ---------------------------------------------------------------------------

def proper_divisors(n: int) -> List[int]:
    """Return all divisors of n except n itself."""
    if n <= 1:
        return []
    divs = [1]
    i = 2
    while i * i <= n:
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
        i += 1
    return sorted(divs)


def sigma(n: int) -> int:
    """Return the sum of all divisors of n, including n itself."""
    if n <= 0:
        return 0
    total = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
        i += 1
    return total


def num_divisors(n: int) -> int:
    """Return the count of all divisors of n."""
    if n <= 0:
        return 0
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 2 if i != n // i else 1
        i += 1
    return count


def prime_factors_set(n: int) -> Set[int]:
    """Return the set of unique prime factors of n."""
    factors: Set[int] = set()
    if n <= 1:
        return factors
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    f = 3
    while f * f <= n:
        while n % f == 0:
            factors.add(f)
            n //= f
        f += 2
    if n > 1:
        factors.add(n)
    return factors


def _factorization(n: int) -> List[tuple]:
    """Return list of (prime, exponent) pairs for n."""
    result = []
    if n <= 1:
        return result
    f = 2
    while f * f <= n:
        if n % f == 0:
            exp = 0
            while n % f == 0:
                exp += 1
                n //= f
            result.append((f, exp))
        f += 1
    if n > 1:
        result.append((n, 1))
    return result


def _is_perfect_power(n: int) -> bool:
    """Return True if n = k^m for some k>1, m>1."""
    if n == 1:
        return True   # 1 = 1^k for any k >= 2
    if n <= 0:
        return False
    for exp in range(2, n.bit_length() + 1):
        root = round(n ** (1 / exp))
        for r in (root - 1, root, root + 1):
            if r > 1 and r ** exp == n:
                return True
    return False


# ---------------------------------------------------------------------------
# Precompute untouchable numbers up to 10000 via sieve
# ---------------------------------------------------------------------------

def _build_untouchable_set(limit: int = 10000) -> Set[int]:
    """Sieve: find all values that ARE proper-divisor-sums, complement is untouchable."""
    reachable: Set[int] = set()
    for k in range(2, limit + 1):
        s = sum(proper_divisors(k))
        if s <= limit:
            reachable.add(s)
    # 1 is never a proper divisor sum of anything >= 2 (pd(1)=[], pd(prime)=[1])
    # Actually pd(p)=[1] for prime p, so 1 is reachable. Untouchable = not reachable.
    return set(range(1, limit + 1)) - reachable


_UNTOUCHABLE: Set[int] = _build_untouchable_set(10000)

# ---------------------------------------------------------------------------
# Registered classifiers
# ---------------------------------------------------------------------------

def _explain_perfect(n: int) -> str:
    pd = proper_divisors(n)
    s = sum(pd)
    return f"proper divisors of {n} = {{{', '.join(map(str, pd))}}}, sum = {s}" + (" == " if s == n else " != ") + str(n)


@register(name="Perfect", category="divisors", oeis="A000396",
          description="Equal to the sum of its proper divisors.",
          explain=_explain_perfect)
def is_perfect(n: int) -> bool:
    """Return True if n equals the sum of its proper divisors.

    Parameters
    ----------
    n : int
        Positive integer.

    Returns
    -------
    bool

    Examples
    --------
    >>> is_perfect(6)
    True
    >>> is_perfect(28)
    True
    >>> is_perfect(12)
    False
    """
    if n < 2:
        return False
    return sigma(n) - n == n


def _explain_abundant(n: int) -> str:
    s = sigma(n) - n
    return f"sigma({n}) - {n} = {s} > {n}" if s > n else f"sigma({n}) - {n} = {s} <= {n}"


@register(name="Abundant", category="divisors", oeis="A005101",
          description="Proper divisor sum exceeds n.",
          explain=_explain_abundant)
def is_abundant(n: int) -> bool:
    """Return True if the sum of proper divisors of n exceeds n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_abundant(12)
    True
    >>> is_abundant(8)
    False
    """
    if n < 1:
        return False
    return sigma(n) - n > n


def _explain_deficient(n: int) -> str:
    s = sigma(n) - n
    return f"sigma({n}) - {n} = {s} < {n}" if s < n else f"sigma({n}) - {n} = {s} >= {n}"


@register(name="Deficient", category="divisors", oeis="A005100",
          description="Proper divisor sum is less than n.",
          explain=_explain_deficient)
def is_deficient(n: int) -> bool:
    """Return True if the sum of proper divisors of n is less than n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_deficient(8)
    True
    >>> is_deficient(6)
    False
    """
    if n < 1:
        return False
    return sigma(n) - n < n


@register(name="Semiperfect", category="divisors", oeis="A005835",
          description="Equal to the sum of some subset of its proper divisors.")
def is_semiperfect(n: int) -> bool:
    """Return True if n equals the sum of some subset of its proper divisors.

    Uses bitmask DP (Python big-int as bitset) for performance.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    divs = proper_divisors(n)
    if not divs:
        return False
    bitset = 1
    for d in divs:
        bitset |= bitset << d
        if (bitset >> n) & 1:
            return True
    return bool((bitset >> n) & 1)


def _explain_weird(n: int) -> str:
    s = sigma(n) - n
    sp = is_semiperfect(n)
    return f"sigma({n}) - {n} = {s} > {n} (abundant), semiperfect? {'yes' if sp else 'no'} -> {'weird' if (s > n and not sp) else 'not weird'}"


@register(name="Weird", category="divisors", oeis="A006037",
          description="Abundant but not semiperfect.",
          explain=_explain_weird)
def is_weird(n: int) -> bool:
    """Return True if n is abundant but not semiperfect.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_weird(70)
    True
    """
    return is_abundant(n) and not is_semiperfect(n)


def _explain_amicable(n: int) -> str:
    m = sigma(n) - n
    m_pair = sigma(m) - m if m > 1 else 0
    return f"sigma({n}) - {n} = {m}, sigma({m}) - {m} = {m_pair}" + ("  --  amicable pair!" if (m != n and m_pair == n) else "  --  not an amicable pair")


@register(name="Amicable", category="divisors", oeis="A063990",
          description="Pair where each number's proper divisor sum is the other.",
          explain=_explain_amicable)
def is_amicable(n: int) -> bool:
    """Return True if n is part of an amicable pair.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 2:
        return False
    m = sigma(n) - n
    return m != n and sigma(m) - m == n


def _explain_sociable(n: int) -> str:
    if n < 2:
        return f"{n} < 2 -- not applicable"
    cycle = [n]
    current = sigma(n) - n
    while len(cycle) < 7:
        if current <= 1:
            return f"{n}: chain terminates at {current} -> NO"
        if current == n:
            if len(cycle) > 2:
                return f"{n}: aliquot cycle of length {len(cycle)}: {cycle} -> YES"
            return f"{n}: amicable pair: {cycle[0]} <-> {cycle[1]} -> NOT sociable"
        if current in cycle:
            return f"{n}: chain enters a shorter cycle -> NO"
        cycle.append(current)
        current = sigma(current) - current
    return f"{n}: cycle exceeds length 6 or not detected -> NO"

@register(name="Sociable", category="divisors", oeis="A003416",
          description="Part of an aliquot cycle of length 3-6 (longer chains not detected).",
          explain=_explain_sociable)
def is_sociable(n: int) -> bool:
    """Return True if n is part of a sociable cycle of length 3–6.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 2:
        return False
    seen = [n]
    current = sigma(n) - n
    for _ in range(5):  # check up to length 6
        if current <= 1:
            return False
        if current == n and len(seen) > 2:
            return True
        if current in seen:
            return False
        seen.append(current)
        current = sigma(current) - current
    return current == n and len(seen) > 2


def _explain_untouchable(n: int) -> str:
    if n <= 0:
        return f"{n} <= 0 -- not applicable"
    if n <= 10000:
        result = n in _UNTOUCHABLE
        return f"{n}: precomputed untouchable set -> {'YES (untouchable)' if result else 'NO (reachable)'}"
    return f"{n}: use sigma sieve (10000 < n <= 500k) or raises ValueError -> see is_untouchable result"

@register(name="Untouchable", category="divisors", oeis="A005114",
          description="No integer has n as its proper divisor sum.",
          explain=_explain_untouchable)
def is_untouchable(n: int) -> bool:
    """Return True if no integer has n as its proper divisor sum.

    Uses a precomputed sieve for values up to 10000.
    For n in (10000, 500_000] uses an fast divisor-sum sieve over [2, 2n].
    n > 500_000 raises ValueError (computationally infeasible).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n <= 10000:
        return n in _UNTOUCHABLE
    if n > 500_000:
        raise ValueError(
            "is_untouchable(n) is not supported for n > 500,000 "
            "(checking requires an exhaustive sieve over [2, 2n] which is "
            "computationally infeasible at this range)"
        )
    limit = n * 2
    # Divisor-sum sieve: sigma_arr[k] = sum of divisors of k
    sigma_arr = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for j in range(i, limit + 1, i):
            sigma_arr[j] += i
    seen_sums = set()
    for k in range(2, limit + 1):
        seen_sums.add(sigma_arr[k] - k)
    return n not in seen_sums


def _explain_superperfect(n: int) -> str:
    if n < 1:
        return f"{n} < 1 -- not applicable"
    s1 = sigma(n)
    s2 = sigma(s1)
    return f"sigma({n}) = {s1}, sigma({s1}) = {s2}; 2n = {2*n} -> {'YES' if s2 == 2*n else 'NO'}"

@register(name="Superperfect", category="divisors", oeis="A019279",
          description="sigma(sigma(n)) == 2*n.",
          explain=_explain_superperfect)
def is_superperfect(n: int) -> bool:
    """Return True if sigma(sigma(n)) == 2*n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    return sigma(sigma(n)) == 2 * n


def _explain_harmonic_divisor(n: int) -> str:
    if n < 1:
        return f"{n} < 1 -- not applicable"
    nd = num_divisors(n)
    s = sigma(n)
    hm = n * nd / s
    is_int = (n * nd) % s == 0
    return f"n={n}, d(n)={nd}, sigma(n)={s}, HM = n*d/sigma = {n}*{nd}/{s} = {hm:.2f} -> {'integer -> YES' if is_int else 'not integer -> NO'}"

@register(name="Harmonic Divisor", category="divisors", oeis="A001599",
          description="Harmonic mean of divisors is an integer.",
          explain=_explain_harmonic_divisor)
def is_harmonic_divisor(n: int) -> bool:
    """Return True if the harmonic mean of n's divisors is an integer.

    The harmonic mean of divisors = n * num_divisors(n) / sigma(n).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    nd = num_divisors(n)
    s = sigma(n)
    # harmonic mean = n * nd / s must be integer
    return (n * nd) % s == 0


def _explain_practical(n: int) -> str:
    if n <= 0:
        return f"n = {n} <= 0"
    if n == 1:
        return f"n = 1 is trivially practical"
    if n % 2 != 0:
        return f"{n} is odd and > 1, cannot be practical"
    factors = _factorization(n)
    sp = 1
    for p, e in factors:
        if p > sp + 1:
            return f"prime factor {p} > 1 + sigma(previous prime powers) = {sp + 1}, fails practical criterion"
        sp *= (p ** (e + 1) - 1) // (p - 1)
    return f"all prime factors satisfy p <= 1 + sigma(previous): {n} is practical"


@register(name="Practical", category="divisors", oeis="A005153",
          description="Every integer 1..n can be expressed as a sum of distinct divisors of n.",
          explain=_explain_practical)
def is_practical(n: int) -> bool:
    """Return True if every integer 1..n is a sum of distinct divisors of n.

    Uses the standard criterion: n=1, or n=2, or for each prime p^a || n
    in sorted order, p <= 1 + sigma(product of earlier prime powers).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n <= 0:
        return False
    if n == 1:
        return True
    if n % 2 != 0 and n != 1:
        return False
    factors = _factorization(n)
    sigma_prefix = 1
    for p, e in factors:
        if p > sigma_prefix + 1:
            return False
        # sigma of p^e = (p^(e+1) - 1) / (p - 1)
        sigma_prefix *= (p ** (e + 1) - 1) // (p - 1)
    return True


def _explain_refactorable(n: int) -> str:
    if n <= 0:
        return f"{n} <= 0 -- not applicable"
    nd = num_divisors(n)
    return f"n={n}, d(n)={nd}; {n} % {nd} = {n % nd} -> {'YES' if n % nd == 0 else 'NO'}"

@register(name="Refactorable", category="divisors", oeis="A033950",
          description="Number of divisors divides n.",
          explain=_explain_refactorable)
def is_refactorable(n: int) -> bool:
    """Return True if the number of divisors of n divides n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    return n % num_divisors(n) == 0


def _explain_highly_composite(n: int) -> str:
    if n < 1:
        return f"{n} < 1 -- not applicable"
    nd = num_divisors(n)
    for k in range(1, n):
        if num_divisors(k) >= nd:
            return f"n={n}, d(n)={nd}, but d({k})={num_divisors(k)} >= d(n) -> NO"
    return f"n={n}, d(n)={nd}, no smaller number has >= d(n) divisors -> YES"

@register(name="Highly Composite", category="divisors", oeis="A002182",
          description="Has more divisors than any smaller positive integer.",
          explain=_explain_highly_composite)
def is_highly_composite(n: int) -> bool:
    """Return True if n has more divisors than any smaller positive integer.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    nd = num_divisors(n)
    for k in range(1, n):
        if num_divisors(k) >= nd:
            return False
    return True


_explain_squarefree = factorization_template(
    lambda f: len(f) == len(set(f)),
    "all prime factors appear exactly once",
    show_exponents=True,
)

@register(name="Squarefree", category="divisors", oeis="A005117",
          description="Not divisible by any perfect square greater than 1.",
          explain=_explain_squarefree)
def is_squarefree(n: int) -> bool:
    """Return True if n is not divisible by any perfect square > 1.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_squarefree(6)
    True
    >>> is_squarefree(4)
    False
    """
    if n <= 0:
        return False
    if n == 1:
        return True
    f = 2
    while f * f <= n:
        if n % (f * f) == 0:
            return False
        f += 1
    return True


_explain_powerful = factorization_template(
    lambda f: all(f.count(p) >= 2 for p in set(f)),
    "every prime factor appears at least twice",
    show_exponents=True,
)

@register(name="Powerful", category="divisors", oeis="A001694",
          description="For every prime p dividing n, p^2 also divides n.",
          explain=_explain_powerful)
def is_powerful(n: int) -> bool:
    """Return True if for every prime p dividing n, p^2 also divides n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_powerful(4)
    True
    >>> is_powerful(6)
    False
    """
    if n <= 0:
        return False
    if n == 1:
        return True
    for p, e in _factorization(n):
        if e < 2:
            return False
    return True


def _explain_achilles(n: int) -> str:
    if n <= 1:
        return f"{n} <= 1 -- not applicable"
    factors = _factorization(n)
    exp_dict = dict(factors)
    powerful = all(e >= 2 for _, e in factors)
    if not powerful:
        return f"{n}: exponents={exp_dict}, not all >= 2 -> not powerful -> NO"
    from math import gcd
    exponents = [e for _, e in factors]
    g = 0
    for e in exponents:
        g = gcd(g, e)
    fact_str = " x ".join(f"{p}^{e}" for p, e in factors)
    return (
        f"{n} = {fact_str}; all exponents >= 2 (powerful), "
        f"gcd(exponents)={g} {'= 1 -> Achilles: YES' if g == 1 else '> 1 -> perfect power -> NO'}"
    )

@register(name="Achilles", category="divisors", oeis="A052486",
          description="Powerful but not a perfect power. Smallest: 72.",
          explain=_explain_achilles)
def is_achilles(n: int) -> bool:
    """Return True if n is powerful but not a perfect power.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_achilles(72)
    True
    """
    return is_powerful(n) and not _is_perfect_power(n)


_explain_sphenic = factorization_template(
    lambda f: len(f) == 3 and len(set(f)) == 3,
    "product of exactly 3 distinct primes",
    show_exponents=True,
)

@register(name="Sphenic", category="divisors", oeis="A007304",
          description="Product of exactly 3 distinct primes.",
          explain=_explain_sphenic)
def is_sphenic(n: int) -> bool:
    """Return True if n is the product of exactly 3 distinct primes.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_sphenic(30)
    True
    >>> is_sphenic(12)
    False
    """
    factors = _factorization(n)
    return len(factors) == 3 and all(e == 1 for _, e in factors)


_explain_smooth_2 = factorization_template(
    lambda f: all(p <= 2 for p in set(f)),
    "all prime factors <= 2",
    show_exponents=True,
)

@register(name="2-smooth", category="divisors", oeis="A000079",
          description="Only prime factor is 2 (powers of 2).",
          explain=_explain_smooth_2)
def is_smooth_2(n: int) -> bool:
    """Return True if the only prime factor of n is 2.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    return n > 0 and (n & (n - 1)) == 0


_explain_smooth_3 = factorization_template(
    lambda f: all(p <= 3 for p in set(f)),
    "all prime factors <= 3",
    show_exponents=True,
)

@register(name="3-smooth", category="divisors", oeis="A003586",
          description="All prime factors are at most 3.",
          explain=_explain_smooth_3)
def is_smooth_3(n: int) -> bool:
    """Return True if all prime factors of n are <= 3.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    while n % 2 == 0:
        n //= 2
    while n % 3 == 0:
        n //= 3
    return n == 1


_explain_smooth_5 = factorization_template(
    lambda f: all(p <= 5 for p in set(f)),
    "all prime factors <= 5",
    show_exponents=True,
)

@register(name="5-smooth", category="divisors", oeis="A051037",
          description="All prime factors are at most 5 (regular numbers).",
          explain=_explain_smooth_5)
def is_smooth_5(n: int) -> bool:
    """Return True if all prime factors of n are <= 5.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
    return n == 1


_explain_smooth_7 = factorization_template(
    lambda f: all(p <= 7 for p in set(f)),
    "all prime factors <= 7",
    show_exponents=True,
)

@register(name="7-smooth", category="divisors", oeis="A002473",
          description="All prime factors are at most 7.",
          explain=_explain_smooth_7)
def is_smooth_7(n: int) -> bool:
    """Return True if all prime factors of n are <= 7.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    for p in (2, 3, 5, 7):
        while n % p == 0:
            n //= p
    return n == 1


_explain_rough_3 = factorization_template(
    lambda f: all(p >= 3 for p in set(f)),
    "all prime factors >= 3",
    show_exponents=True,
)

@register(name="3-rough", category="divisors",
          description="No prime factor less than 3 (i.e. odd numbers > 1).",
          explain=_explain_rough_3)
def is_rough_3(n: int) -> bool:
    """Return True if n has no prime factor less than 3 (i.e. n is odd).

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n > 1 and n % 2 != 0


_explain_rough_5 = factorization_template(
    lambda f: all(p >= 5 for p in set(f)),
    "all prime factors >= 5",
    show_exponents=True,
)

@register(name="5-rough", category="divisors",
          description="No prime factor less than 5.",
          explain=_explain_rough_5)
def is_rough_5(n: int) -> bool:
    """Return True if n has no prime factor less than 5.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n > 1 and n % 2 != 0 and n % 3 != 0


def _factorization_digit_count(n: int) -> int:
    """Count digits used to express the prime factorization of n.

    For each prime^exp: digits(prime) + (digits(exp) if exp>1 else 0).
    """
    if n == 1:
        return 1
    total = 0
    for p, e in _factorization(n):
        total += len(str(p))
        if e > 1:
            total += len(str(e))
    return total


def _explain_economical(n: int) -> str:
    if n <= 1:
        return f"{n} <= 1 -- not applicable"
    dig_n = len(str(n))
    dig_f = _factorization_digit_count(n)
    result = "economical" if dig_n > dig_f else "not economical"
    return f"{n} has {dig_n} digit(s); factorization uses {dig_f} digit(s) -> {result}"

@register(name="Economical", category="divisors", oeis="A046759",
          description="Prime factorization uses fewer digits than n.",
          explain=_explain_economical)
def is_economical(n: int) -> bool:
    """Return True if the prime factorization of n uses fewer digits than n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 2:
        return False
    return _factorization_digit_count(n) < len(str(n))


def _explain_equidigital(n: int) -> str:
    if n <= 1:
        return f"{n} <= 1 -- not applicable"
    dig_n = len(str(n))
    dig_f = _factorization_digit_count(n)
    result = "equidigital" if dig_n == dig_f else "not equidigital"
    return f"{n} has {dig_n} digit(s); factorization uses {dig_f} digit(s) -> {result}"

@register(name="Equidigital", category="divisors", oeis="A046758",
          description="Prime factorization uses the same number of digits as n.",
          explain=_explain_equidigital)
def is_equidigital(n: int) -> bool:
    """Return True if the prime factorization of n uses the same digits as n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 2:
        return False
    return _factorization_digit_count(n) == len(str(n))


def _explain_wasteful(n: int) -> str:
    if n <= 1:
        return f"{n} <= 1 -- not applicable"
    dig_n = len(str(n))
    dig_f = _factorization_digit_count(n)
    result = "wasteful" if dig_n < dig_f else "not wasteful"
    return f"{n} has {dig_n} digit(s); factorization uses {dig_f} digit(s) -> {result}"

@register(name="Wasteful", category="divisors", oeis="A046760",
          description="Prime factorization uses more digits than n.",
          explain=_explain_wasteful)
def is_wasteful(n: int) -> bool:
    """Return True if the prime factorization of n uses more digits than n.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 2:
        return False
    return _factorization_digit_count(n) > len(str(n))


@register(name="Zumkeller", category="divisors", oeis="A083207",
          description="Divisors can be partitioned into two sets with equal sum.")
def is_zumkeller(n: int) -> bool:
    """Return True if the divisors of n can be split into two sets with equal sum.

    Uses bitmask DP (Python big-int as bitset) for performance.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    if n < 1:
        return False
    divs_all = proper_divisors(n) + [n]
    total = sum(divs_all)
    if total % 2 != 0:
        return False
    target = total // 2
    bitset = 1
    for d in divs_all:
        bitset |= bitset << d
        if (bitset >> target) & 1:
            return True
    return bool((bitset >> target) & 1)
