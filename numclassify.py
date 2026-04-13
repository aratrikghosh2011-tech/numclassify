"""
numclassify.py
==============
A comprehensive Python module for number classification.
150+ number property checks, all callable as simple functions.

Usage:
    from numclassify import is_prime, is_armstrong, get_all_properties
    print(is_prime(17))
    print(get_all_properties(153))

GitHub: https://github.com/YOUR_USERNAME/numclassify
Author: Aratrik Ghosh
License: MIT
"""

import math
from functools import lru_cache


# ─────────────────────────────────────────────
# HELPERS (internal)
# ─────────────────────────────────────────────

def _digits(n):
    return [int(d) for d in str(abs(n))]

def _digit_count(n):
    return len(str(abs(n)))

def _factors(n):
    if n < 1:
        return []
    return [i for i in range(1, n + 1) if n % i == 0]

def _proper_factors(n):
    if n < 2:
        return []
    return [i for i in range(1, n) if n % i == 0]

def _digit_sum(n):
    return sum(_digits(n))

def _digit_product(n):
    p = 1
    for d in _digits(n):
        p *= d
    return p

def _reverse(n):
    return int(str(abs(n))[::-1])

def _factorial(n):
    if n < 0:
        return None
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r

def _is_perfect_square(n):
    if n < 0:
        return False
    r = int(math.isqrt(n))
    return r * r == n

def _binary(n):
    return bin(abs(n))[2:]

def _octal(n):
    return oct(abs(n))[2:]

def _hex_str(n):
    return hex(abs(n))[2:]

def _fibonacci_set(limit=10**7):
    s = set()
    a, b = 0, 1
    while a <= limit:
        s.add(a)
        a, b = b, a + b
    return s


# ─────────────────────────────────────────────
# 1. PRIME & COMPOSITE
# ─────────────────────────────────────────────

def is_prime(n):
    """Check if n is a prime number."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_composite(n):
    """Check if n is composite (not prime, > 1)."""
    return n > 1 and not is_prime(n)

def is_co_prime(a, b):
    """Check if a and b are co-prime (GCD == 1)."""
    return math.gcd(a, b) == 1

def is_twin_prime(n):
    """Check if n is part of a twin prime pair."""
    return is_prime(n) and (is_prime(n - 2) or is_prime(n + 2))

def is_mersenne_prime(n):
    """Check if n is a Mersenne prime (2^p - 1 for prime p)."""
    if not is_prime(n):
        return False
    m = n + 1
    return m > 1 and (m & (m - 1)) == 0

def is_safe_prime(n):
    """Check if n is a safe prime ((n-1)/2 is also prime)."""
    return is_prime(n) and is_prime((n - 1) // 2)

def is_sophie_germain_prime(n):
    """Check if n is a Sophie Germain prime (2n+1 is also prime)."""
    return is_prime(n) and is_prime(2 * n + 1)

def is_wilson_prime(n):
    """Check if n is a Wilson prime (p^2 divides (p-1)!+1)."""
    if not is_prime(n):
        return False
    return (_factorial(n - 1) + 1) % (n * n) == 0

def is_circular_prime(n):
    """Check if all rotations of n's digits are prime."""
    s = str(n)
    return all(is_prime(int(s[i:] + s[:i])) for i in range(len(s)))

def is_emirp(n):
    """Check if n is an emirp (prime whose reverse is a different prime)."""
    return is_prime(n) and is_prime(_reverse(n)) and n != _reverse(n)

def is_prime_palindrome(n):
    """Check if n is both prime and a palindrome."""
    return is_prime(n) and is_palindrome(n)

def get_prime_factors(n):
    """Return list of prime factors of n."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def count_prime_factors(n):
    """Count distinct prime factors."""
    return len(set(get_prime_factors(n)))


# ─────────────────────────────────────────────
# 2. ARMSTRONG & NARCISSISTIC
# ─────────────────────────────────────────────

def is_armstrong(n):
    """Check if n is an Armstrong (narcissistic) number."""
    d = _digits(n)
    p = len(d)
    return sum(x ** p for x in d) == n

def is_perfect_digital_invariant(n, p):
    """Check if n equals sum of its digits each raised to power p."""
    return sum(x ** p for x in _digits(n)) == n

def is_pluperfect_digital_invariant(n):
    """Check if n is a PPDI for any power."""
    d = _digits(n)
    return any(sum(x ** p for x in d) == n for p in range(1, 10))


# ─────────────────────────────────────────────
# 3. PERFECT, ABUNDANT, DEFICIENT
# ─────────────────────────────────────────────

def is_perfect(n):
    """Check if n equals the sum of its proper divisors."""
    return n > 1 and sum(_proper_factors(n)) == n

def is_abundant(n):
    """Check if sum of proper divisors > n."""
    return n > 1 and sum(_proper_factors(n)) > n

def is_deficient(n):
    """Check if sum of proper divisors < n."""
    return n > 1 and sum(_proper_factors(n)) < n

def abundance(n):
    """Return abundance of n (sum of proper divisors - n)."""
    return sum(_proper_factors(n)) - n

def is_semiperfect(n):
    """Check if n equals sum of some subset of its proper divisors."""
    pf = _proper_factors(n)
    total = sum(pf)
    if total < n:
        return False
    # subset sum check
    dp = {0}
    for f in pf:
        dp = dp | {x + f for x in dp}
    return n in dp

def is_weird(n):
    """Check if n is abundant but not semiperfect."""
    return is_abundant(n) and not is_semiperfect(n)


# ─────────────────────────────────────────────
# 4. PALINDROME & REVERSE
# ─────────────────────────────────────────────

def is_palindrome(n):
    """Check if n reads the same forwards and backwards."""
    s = str(abs(n))
    return s == s[::-1]

def is_palindrome_prime(n):
    """Alias for prime palindrome."""
    return is_prime(n) and is_palindrome(n)

def reverse_number(n):
    """Return the reverse of n."""
    return _reverse(n)

def is_reverse_prime(n):
    """Check if reverse of n is prime (n need not be prime)."""
    return is_prime(_reverse(n))


# ─────────────────────────────────────────────
# 5. SPY NUMBER
# ─────────────────────────────────────────────

def is_spy(n):
    """Check if sum of digits equals product of digits."""
    d = _digits(n)
    return _digit_sum(n) == _digit_product(n)


# ─────────────────────────────────────────────
# 6. AUTOMORPHIC & CYCLIC
# ─────────────────────────────────────────────

def is_automorphic(n):
    """Check if n^2 ends with n."""
    return str(n * n).endswith(str(n))

def is_trimorphic(n):
    """Check if n^3 ends with n."""
    return str(n ** 3).endswith(str(n))


# ─────────────────────────────────────────────
# 7. NEON
# ─────────────────────────────────────────────

def is_neon(n):
    """Check if sum of digits of n^2 equals n."""
    return _digit_sum(n * n) == n


# ─────────────────────────────────────────────
# 8. HAPPY & SAD
# ─────────────────────────────────────────────

def is_happy(n):
    """Check if n is a happy number."""
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(x ** 2 for x in _digits(n))
    return n == 1

def is_sad(n):
    """Check if n is not a happy number."""
    return not is_happy(n)


# ─────────────────────────────────────────────
# 9. FIBONACCI & LUCAS
# ─────────────────────────────────────────────

def is_fibonacci(n):
    """Check if n is a Fibonacci number."""
    return _is_perfect_square(5 * n * n + 4) or _is_perfect_square(5 * n * n - 4)

def is_lucas(n):
    """Check if n is a Lucas number."""
    lucas = set()
    a, b = 2, 1
    while a <= max(n, 10):
        lucas.add(a)
        a, b = b, a + b
    return n in lucas

def nth_fibonacci(n):
    """Return nth Fibonacci number (0-indexed)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ─────────────────────────────────────────────
# 10. HARSHAD / NIVEN
# ─────────────────────────────────────────────

def is_harshad(n):
    """Check if n is divisible by its digit sum."""
    s = _digit_sum(n)
    return s != 0 and n % s == 0

is_niven = is_harshad  # alias

def is_strong_harshad(n):
    """Check if n is a strong Harshad number (n/digitsum is prime)."""
    s = _digit_sum(n)
    return s != 0 and n % s == 0 and is_prime(n // s)


# ─────────────────────────────────────────────
# 11. DISARIUM
# ─────────────────────────────────────────────

def is_disarium(n):
    """Check if sum of digits^position equals n."""
    d = _digits(n)
    return sum(x ** (i + 1) for i, x in enumerate(d)) == n


# ─────────────────────────────────────────────
# 12. KAPREKAR
# ─────────────────────────────────────────────

def is_kaprekar(n):
    """Check if n is a Kaprekar number."""
    if n == 1:
        return True
    sq = str(n * n)
    for i in range(1, len(sq)):
        left, right = int(sq[:i] or 0), int(sq[i:] or 0)
        if right > 0 and left + right == n:
            return True
    return False

def kaprekar_constant(n):
    """Apply Kaprekar routine and return steps to reach 6174 (4-digit)."""
    steps = 0
    while n != 6174 and steps < 10:
        d = sorted(_digits(n))
        while len(d) < 4:
            d.insert(0, 0)
        asc = int(''.join(map(str, d)))
        desc = int(''.join(map(str, reversed(d))))
        n = desc - asc
        steps += 1
    return steps, n


# ─────────────────────────────────────────────
# 13. AMICABLE & SOCIABLE
# ─────────────────────────────────────────────

def is_amicable(n):
    """Check if n and sum of its proper divisors form an amicable pair."""
    m = sum(_proper_factors(n))
    return m != n and sum(_proper_factors(m)) == n

def amicable_pair(n):
    """Return the amicable partner of n, or None."""
    m = sum(_proper_factors(n))
    if m != n and sum(_proper_factors(m)) == n:
        return m
    return None


# ─────────────────────────────────────────────
# 14. DIGIT PROPERTIES
# ─────────────────────────────────────────────

def digit_sum(n):
    return _digit_sum(n)

def digit_product(n):
    return _digit_product(n)

def digital_root(n):
    """Repeatedly sum digits until single digit."""
    while n >= 10:
        n = _digit_sum(n)
    return n

def is_digital_root_prime(n):
    return is_prime(digital_root(n))

def additive_persistence(n):
    """Count steps to reduce n to single digit by summing digits."""
    count = 0
    while n >= 10:
        n = _digit_sum(n)
        count += 1
    return count

def multiplicative_persistence(n):
    """Count steps to reduce n to single digit by multiplying digits."""
    count = 0
    while n >= 10:
        n = _digit_product(n)
        count += 1
    return count

def is_smith(n):
    """Check if n is a Smith number (digit sum == sum of digits of prime factors)."""
    if is_prime(n):
        return False
    pf = get_prime_factors(n)
    return _digit_sum(n) == sum(_digit_sum(p) for p in pf)

def is_hoax(n):
    """Check if n is a Hoax number (composite, digit sum == sum of digits of distinct prime factors)."""
    if is_prime(n):
        return False
    pf = list(set(get_prime_factors(n)))
    return _digit_sum(n) == sum(_digit_sum(p) for p in pf)

def is_self(n):
    """Check if n is a self number (cannot be expressed as m + digit_sum(m))."""
    for m in range(max(1, n - 50), n):
        if m + _digit_sum(m) == n:
            return False
    return True

def is_bouncy(n):
    """Check if n is bouncy (neither increasing nor decreasing digits)."""
    d = _digits(n)
    return not (d == sorted(d) or d == sorted(d, reverse=True))

def is_increasing(n):
    """Check if digits are non-decreasing."""
    d = _digits(n)
    return d == sorted(d)

def is_decreasing(n):
    """Check if digits are non-increasing."""
    d = _digits(n)
    return d == sorted(d, reverse=True)

def is_pandigital(n, start=1):
    """Check if n contains each digit from start to 9 exactly once."""
    s = str(n)
    expected = set(str(i) for i in range(start, start + len(s)))
    return set(s) == expected and len(s) == len(expected)

def is_repunit(n):
    """Check if n consists of all 1s."""
    return all(d == '1' for d in str(n))

def is_repdigit(n):
    """Check if all digits of n are the same."""
    s = str(n)
    return len(set(s)) == 1

def count_digits(n):
    """Return count of digits in n."""
    return _digit_count(n)

def sum_of_digits(n):
    return _digit_sum(n)

def is_duck(n):
    """Check if n has a zero digit (but not leading zero)."""
    return '0' in str(n)

def is_buzz(n):
    """Check if n is divisible by 7 or ends with 7."""
    return n % 7 == 0 or n % 10 == 7

def is_spy(n):
    """Check if sum of digits == product of digits."""
    d = _digits(n)
    s = sum(d)
    p = 1
    for x in d:
        p *= x
    return s == p


# ─────────────────────────────────────────────
# 15. POWER & SQUARE PROPERTIES
# ─────────────────────────────────────────────

def is_perfect_square(n):
    return _is_perfect_square(n)

def is_perfect_cube(n):
    if n < 0:
        r = -round((-n) ** (1/3))
    else:
        r = round(n ** (1/3))
    return r ** 3 == n

def is_perfect_power(n):
    """Check if n = a^b for some a,b > 1."""
    if n < 4:
        return False
    for b in range(2, int(math.log2(n)) + 1):
        a = round(n ** (1 / b))
        for candidate in [a - 1, a, a + 1]:
            if candidate > 1 and candidate ** b == n:
                return True
    return False

def is_powerful(n):
    """Check if for every prime p dividing n, p^2 also divides n."""
    for p in set(get_prime_factors(n)):
        if n % (p * p) != 0:
            return False
    return True

def is_squarefree(n):
    """Check if n is not divisible by any perfect square > 1."""
    for p in set(get_prime_factors(n)):
        if n % (p * p) == 0:
            return False
    return True

def is_achilles(n):
    """Check if n is powerful but not a perfect power."""
    return is_powerful(n) and not is_perfect_power(n)


# ─────────────────────────────────────────────
# 16. FACTORIAL & RELATED
# ─────────────────────────────────────────────

def is_factorial(n):
    """Check if n is a factorial number."""
    i, f = 1, 1
    while f < n:
        i += 1
        f *= i
    return f == n

def is_subfactorial(n):
    """Check if n is a subfactorial (!n)."""
    def subfact(k):
        if k == 0: return 1
        if k == 1: return 0
        return (k - 1) * (subfact(k - 1) + subfact(k - 2))
    i = 0
    while True:
        s = subfact(i)
        if s == n: return True
        if s > n: return False
        i += 1

def factorial_of(n):
    return _factorial(n)

def is_primorial(n):
    """Check if n is a product of first k primes."""
    p, prod = 2, 1
    while prod < n:
        prod *= p
        if prod == n:
            return True
        p = next(x for x in range(p + 1, p + 100) if is_prime(x))
    return prod == n


# ─────────────────────────────────────────────
# 17. BINARY / BIT PROPERTIES
# ─────────────────────────────────────────────

def to_binary(n):
    return _binary(n)

def to_octal(n):
    return _octal(n)

def to_hex(n):
    return _hex_str(n)

def is_binary_palindrome(n):
    b = _binary(n)
    return b == b[::-1]

def count_set_bits(n):
    return bin(n).count('1')

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

def is_power_of_three(n):
    if n < 1: return False
    while n % 3 == 0:
        n //= 3
    return n == 1

def is_power_of_k(n, k):
    if n < 1 or k < 2: return False
    while n % k == 0:
        n //= k
    return n == 1

def is_apocalypse_number(n):
    """Check if 2^n contains '666'."""
    return '666' in str(2 ** n)


# ─────────────────────────────────────────────
# 18. DIVISIBILITY
# ─────────────────────────────────────────────

def is_divisible_by(n, d):
    return d != 0 and n % d == 0

def count_divisors(n):
    return len(_factors(n))

def sum_of_divisors(n):
    return sum(_factors(n))

def is_refactorable(n):
    """Check if n is divisible by its count of divisors."""
    return n % count_divisors(n) == 0

def is_pronic(n):
    """Check if n = k*(k+1) for some k (oblong number)."""
    k = int(math.isqrt(n))
    return k * (k + 1) == n

is_oblong = is_pronic  # alias

def is_triangular(n):
    """Check if n is a triangular number."""
    return _is_perfect_square(8 * n + 1)

def is_square_triangular(n):
    return is_perfect_square(n) and is_triangular(n)

def is_pentagonal(n):
    """Check if n is a pentagonal number."""
    # n = k(3k-1)/2 → 24n+1 must be a perfect square ≡ 5 mod 6... simpler:
    disc = 1 + 24 * n
    if not _is_perfect_square(disc):
        return False
    k = (1 + int(math.isqrt(disc))) // 6
    return k * (3 * k - 1) // 2 == n

def is_hexagonal(n):
    """Check if n is a hexagonal number."""
    disc = 1 + 8 * n
    if not _is_perfect_square(disc):
        return False
    k = (1 + int(math.isqrt(disc))) // 4
    return k * (2 * k - 1) == n

def is_heptagonal(n):
    disc = 1 + 40 * n
    if not _is_perfect_square(disc):
        return False
    k = (3 + int(math.isqrt(disc * 4 - 12))) // 10
    return k * (5 * k - 3) // 2 == n

def is_octagonal(n):
    disc = 1 + 3 * n
    if not _is_perfect_square(disc):
        return False
    k = (1 + int(math.isqrt(disc * 3))) // 6 + 1
    return k * (3 * k - 2) == n

def is_centered_square(n):
    return _is_perfect_square(2 * (n - 1) + 1) and (n - 1) % 2 == 0 or _is_perfect_square(4 * n - 3)

def is_star(n):
    """Check if n is a star number (6k(k-1)+1)."""
    if (n - 1) % 6 != 0:
        return _is_perfect_square(n) and False
    t = (n - 1) // 6
    k = int(math.isqrt(t))
    return k * (k + 1) == t or k > 0 and (k - 1) * k == t


# ─────────────────────────────────────────────
# 19. SPECIAL SEQUENCES
# ─────────────────────────────────────────────

def is_catalan(n):
    """Check if n is a Catalan number."""
    c, k = 1, 0
    while c < n:
        k += 1
        c = c * 2 * (2 * k - 1) // (k + 1)
    return c == n

def is_bell(n):
    """Check if n is a Bell number."""
    # Generate Bell numbers until >= n
    bell = [[0] * 20 for _ in range(20)]
    bell[0][0] = 1
    for i in range(1, 15):
        bell[i][0] = bell[i-1][i-1]
        for j in range(1, i + 1):
            bell[i][j] = bell[i-1][j-1] + bell[i][j-1]
        if bell[i][0] == n:
            return True
    return n == 1

def is_colossally_abundant(n):
    """Approximate check for first few colossally abundant numbers."""
    ca = {1, 2, 6, 12, 60, 120, 360, 2520, 5040, 55440, 720720}
    return n in ca

def is_highly_composite(n):
    """Check if n has more divisors than any smaller positive integer."""
    count = count_divisors(n)
    return all(count_divisors(i) < count for i in range(1, n))

def is_superior_highly_composite(n):
    """Check against known list."""
    shc = {2, 6, 12, 60, 120, 360, 2520, 5040, 55440, 720720, 1441440}
    return n in shc

def is_regular(n):
    """Check if n is 5-smooth (regular/Hamming number)."""
    for p in [2, 3, 5]:
        while n % p == 0:
            n //= p
    return n == 1

is_hamming = is_regular  # alias
is_humble = is_regular   # alias

def is_ugly(n):
    """Check if n is an ugly number (factors only 2,3,5)."""
    return n > 0 and is_regular(n)

def is_semi_prime(n):
    """Check if n is a product of exactly two primes (not necessarily distinct)."""
    pf = get_prime_factors(n)
    return len(pf) == 2

def is_almost_prime(n, k=2):
    """Check if n has exactly k prime factors (with multiplicity)."""
    return len(get_prime_factors(n)) == k

def is_economical(n):
    """Check if digits in prime factorization < digits in n."""
    pf = get_prime_factors(n)
    factor_digits = sum(_digit_count(p) for p in pf)
    return factor_digits < _digit_count(n)

def is_equidigital(n):
    pf = get_prime_factors(n)
    factor_digits = sum(_digit_count(p) for p in pf)
    return factor_digits == _digit_count(n)

def is_wasteful(n):
    pf = get_prime_factors(n)
    factor_digits = sum(_digit_count(p) for p in pf)
    return factor_digits > _digit_count(n)


# ─────────────────────────────────────────────
# 20. COLLATZ
# ─────────────────────────────────────────────

def collatz_steps(n):
    """Return number of steps to reach 1 via Collatz sequence."""
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

def collatz_sequence(n):
    """Return full Collatz sequence starting from n."""
    seq = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq


# ─────────────────────────────────────────────
# 21. GOLDBACH & CONJECTURE TOOLS
# ─────────────────────────────────────────────

def goldbach_pairs(n):
    """Return list of prime pairs that sum to n (even n > 2)."""
    if n % 2 != 0 or n <= 2:
        return []
    return [(p, n - p) for p in range(2, n // 2 + 1)
            if is_prime(p) and is_prime(n - p)]


# ─────────────────────────────────────────────
# 22. GCD / LCM
# ─────────────────────────────────────────────

def gcd(a, b):
    return math.gcd(a, b)

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def lcm_list(lst):
    result = lst[0]
    for x in lst[1:]:
        result = lcm(result, x)
    return result

def euler_totient(n):
    """Return Euler's totient φ(n)."""
    count = 0
    for i in range(1, n + 1):
        if math.gcd(n, i) == 1:
            count += 1
    return count


# ─────────────────────────────────────────────
# 23. MISC NAMED NUMBERS
# ─────────────────────────────────────────────

def is_vampire(n):
    """Check if n is a vampire number."""
    s = sorted(str(n))
    ln = len(s)
    if ln % 2 != 0:
        return False
    half = ln // 2
    from itertools import permutations
    for p in set(permutations(s)):
        f1 = int(''.join(p[:half]))
        f2 = int(''.join(p[half:]))
        if f1 * f2 == n and not (str(f1)[-1] == '0' and str(f2)[-1] == '0'):
            if f1 <= f2:
                return True
    return False

def is_narcissistic(n):
    """Alias for Armstrong."""
    return is_armstrong(n)

def is_sociable(n, k=None):
    """Check if n is part of a sociable chain (aliquot cycle)."""
    seen = []
    current = n
    for _ in range(30):
        current = sum(_proper_factors(current))
        if current == n:
            return True
        if current in seen:
            return False
        seen.append(current)
    return False

def is_untouchable(n):
    """Check against known untouchable numbers (first 20)."""
    untouchable = {2, 5, 52, 88, 96, 120, 124, 146, 162, 188,
                   206, 210, 216, 238, 246, 248, 262, 268, 276, 288}
    return n in untouchable

def is_frugal(n):
    return is_economical(n)

def is_pernicious(n):
    """Check if n has a prime number of set bits."""
    return is_prime(count_set_bits(n))

def is_polite(n):
    """Check if n can be expressed as sum of consecutive naturals (n is not power of 2)."""
    return n > 1 and not is_power_of_two(n)

def is_impolite(n):
    return is_power_of_two(n)

def is_practical(n):
    """Check if every integer <= n can be represented as sum of distinct divisors of n."""
    if n == 1: return True
    if n % 2 != 0: return False
    factors = sorted(set(get_prime_factors(n)))
    sigma = 1
    for p in factors:
        exp = 0
        temp = n
        while temp % p == 0:
            temp //= p
            exp += 1
        if p > sigma + 1:
            return False
        sigma *= (p ** (exp + 1) - 1) // (p - 1)
    return True

def is_fortunate(n):
    """Check if n is a Fortunate number (known list)."""
    fortunate = {3, 5, 7, 13, 23, 17, 19, 23, 37, 61, 67, 61, 71, 47, 107, 59, 61}
    return n in fortunate

def is_sphenic(n):
    """Check if n is a product of exactly 3 distinct primes."""
    pf = get_prime_factors(n)
    return len(pf) == 3 and len(set(pf)) == 3

def is_brilliant(n):
    """Check if n is a product of two primes with same digit count."""
    pf = get_prime_factors(n)
    return len(pf) == 2 and _digit_count(pf[0]) == _digit_count(pf[1])


# ─────────────────────────────────────────────
# 24. NUMBER CONVERSIONS & REPRESENTATIONS
# ─────────────────────────────────────────────

def to_roman(n):
    """Convert integer to Roman numeral."""
    val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
    syms = ['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I']
    result = ''
    for i, v in enumerate(val):
        while n >= v:
            result += syms[i]
            n -= v
    return result

def from_roman(s):
    """Convert Roman numeral to integer."""
    vals = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    result = 0
    prev = 0
    for ch in reversed(s):
        curr = vals[ch]
        result += curr if curr >= prev else -curr
        prev = curr
    return result

def int_to_words(n):
    """Convert integer to English words (up to millions)."""
    ones = ['','one','two','three','four','five','six','seven','eight','nine',
            'ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen',
            'seventeen','eighteen','nineteen']
    tens = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
    if n == 0: return 'zero'
    if n < 0: return 'negative ' + int_to_words(-n)
    if n < 20: return ones[n]
    if n < 100: return tens[n//10] + ('' if n%10==0 else '-'+ones[n%10])
    if n < 1000: return ones[n//100]+' hundred'+('' if n%100==0 else ' '+int_to_words(n%100))
    if n < 1000000: return int_to_words(n//1000)+' thousand'+('' if n%1000==0 else ' '+int_to_words(n%1000))
    return int_to_words(n//1000000)+' million'+('' if n%1000000==0 else ' '+int_to_words(n%1000000))


# ─────────────────────────────────────────────
# 25. GENERATORS / RANGE FINDERS
# ─────────────────────────────────────────────

def primes_up_to(n):
    """Sieve of Eratosthenes."""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]

def find_in_range(func, start, end):
    """Return all numbers in [start,end] satisfying func(n)==True."""
    return [n for n in range(start, end + 1) if func(n)]

def nth_prime(n):
    """Return nth prime (1-indexed)."""
    count, num = 0, 1
    while count < n:
        num += 1
        if is_prime(num):
            count += 1
    return num


# ─────────────────────────────────────────────
# 26. GET ALL PROPERTIES (master function)
# ─────────────────────────────────────────────

def get_all_properties(n):
    """
    Run all applicable checks on n.
    Returns a dict of {property_name: True/False or value}.
    """
    checks = {
        'is_prime': is_prime,
        'is_composite': is_composite,
        'is_twin_prime': is_twin_prime,
        'is_mersenne_prime': is_mersenne_prime,
        'is_circular_prime': is_circular_prime,
        'is_emirp': is_emirp,
        'is_armstrong': is_armstrong,
        'is_perfect': is_perfect,
        'is_abundant': is_abundant,
        'is_deficient': is_deficient,
        'is_palindrome': is_palindrome,
        'is_spy': is_spy,
        'is_automorphic': is_automorphic,
        'is_trimorphic': is_trimorphic,
        'is_neon': is_neon,
        'is_happy': is_happy,
        'is_fibonacci': is_fibonacci,
        'is_lucas': is_lucas,
        'is_harshad': is_harshad,
        'is_disarium': is_disarium,
        'is_kaprekar': is_kaprekar,
        'is_amicable': is_amicable,
        'is_perfect_square': is_perfect_square,
        'is_perfect_cube': is_perfect_cube,
        'is_perfect_power': is_perfect_power,
        'is_powerful': is_powerful,
        'is_squarefree': is_squarefree,
        'is_smith': is_smith,
        'is_hoax': is_hoax,
        'is_self': is_self,
        'is_bouncy': is_bouncy,
        'is_duck': is_duck,
        'is_buzz': is_buzz,
        'is_repdigit': is_repdigit,
        'is_repunit': is_repunit,
        'is_pandigital': is_pandigital,
        'is_triangular': is_triangular,
        'is_pentagonal': is_pentagonal,
        'is_hexagonal': is_hexagonal,
        'is_pronic': is_pronic,
        'is_factorial': is_factorial,
        'is_catalan': is_catalan,
        'is_ugly': is_ugly,
        'is_semi_prime': is_semi_prime,
        'is_sphenic': is_sphenic,
        'is_binary_palindrome': is_binary_palindrome,
        'is_power_of_two': is_power_of_two,
        'is_pernicious': is_pernicious,
        'is_polite': is_polite,
        'is_economical': is_economical,
        'is_equidigital': is_equidigital,
        'is_wasteful': is_wasteful,
        'is_practical': is_practical,
        'is_refactorable': is_refactorable,
        'is_harshad': is_harshad,
    }
    results = {}
    for name, func in checks.items():
        try:
            results[name] = func(n)
        except Exception:
            results[name] = None

    # Extra info
    results['digit_sum'] = digit_sum(n)
    results['digit_product'] = digit_product(n)
    results['digital_root'] = digital_root(n)
    results['additive_persistence'] = additive_persistence(n)
    results['multiplicative_persistence'] = multiplicative_persistence(n)
    results['count_divisors'] = count_divisors(n)
    results['prime_factors'] = get_prime_factors(n)
    results['collatz_steps'] = collatz_steps(n)
    results['binary'] = to_binary(n)
    results['roman'] = to_roman(n) if 0 < n < 4000 else 'N/A'

    return results

def print_properties(n):
    """Pretty-print all properties of n."""
    props = get_all_properties(n)
    print(f"\n{'='*45}")
    print(f"  Properties of {n}")
    print(f"{'='*45}")
    for k, v in props.items():
        print(f"  {k:<35} {v}")
    print(f"{'='*45}\n")


# ─────────────────────────────────────────────
# QUICK DEMO
# ─────────────────────────────────────────────

if __name__ == '__main__':
    test_nums = [153, 6, 28, 12, 17, 1]
    for num in test_nums:
        print_properties(num)
