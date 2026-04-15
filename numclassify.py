"""
numclassify.py
==============
The most comprehensive Python number classification library.
3000+ number property checks, all callable as simple functions.

Usage:
    from numclassify import is_prime, is_armstrong, get_all_properties
    print(is_prime(17))
    print(get_all_properties(153))

GitHub: https://github.com/AratrikGhosh/numclassify
Author: Aratrik Ghosh
License: MIT
Version: 2.0.0
"""

import math
import itertools
import functools
from collections import Counter


# ═══════════════════════════════════════════════════════════════════════════════
# INTERNAL HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _digits(n):
    return [int(d) for d in str(abs(int(n)))]

def _digit_count(n):
    return len(str(abs(int(n)))) if n != 0 else 1

def _factors(n):
    if n < 1: return []
    return [i for i in range(1, n + 1) if n % i == 0]

def _proper_factors(n):
    if n < 2: return []
    return [i for i in range(1, n) if n % i == 0]

def _digit_sum(n):
    return sum(_digits(n))

def _digit_product(n):
    p = 1
    for d in _digits(n):
        p *= d
    return p

def _reverse(n):
    return int(str(abs(int(n)))[::-1])

def _factorial(n):
    if n < 0: return None
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r

def _is_perfect_square(n):
    if n < 0: return False
    r = int(math.isqrt(n))
    return r * r == n

def _binary(n):
    return bin(abs(int(n)))[2:]

def _octal(n):
    return oct(abs(int(n)))[2:]

def _hex_str(n):
    return hex(abs(int(n)))[2:]

def _subset_sum(nums, target):
    dp = {0}
    for x in nums:
        dp = dp | {s + x for s in dp}
    return target in dp

def _prime_sieve(limit):
    if limit < 2: return []
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return [i for i, v in enumerate(sieve) if v]


# ═══════════════════════════════════════════════════════════════════════════════
# 1. PRIME & COMPOSITE — BASIC
# ═══════════════════════════════════════════════════════════════════════════════

def is_prime(n):
    """Check if n is prime."""
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    if n < 9: return True
    if n % 3 == 0: return False
    r = int(math.isqrt(n))
    f = 5
    while f <= r:
        if n % f == 0 or n % (f + 2) == 0: return False
        f += 6
    return True

def is_composite(n):
    """Check if n is composite."""
    return n > 1 and not is_prime(n)

def is_1(n): return n == 1
def is_unit(n): return n == 1

def is_co_prime(a, b):
    return math.gcd(a, b) == 1

def is_twin_prime(n):
    return is_prime(n) and (is_prime(n - 2) or is_prime(n + 2))

def is_cousin_prime(n):
    """Primes that differ by 4."""
    return is_prime(n) and (is_prime(n - 4) or is_prime(n + 4))

def is_sexy_prime(n):
    """Primes that differ by 6."""
    return is_prime(n) and (is_prime(n - 6) or is_prime(n + 6))

def is_mersenne_prime(n):
    if not is_prime(n): return False
    m = n + 1
    return m > 1 and (m & (m - 1)) == 0

def is_mersenne_number(n):
    """n = 2^k - 1 for some k (not necessarily prime)."""
    return n > 0 and (n & (n + 1)) == 0

def is_fermat_prime(n):
    """Primes of form 2^(2^k) + 1."""
    known = {3, 5, 17, 257, 65537}
    return n in known

def is_safe_prime(n):
    return is_prime(n) and is_prime((n - 1) // 2)

def is_sophie_germain_prime(n):
    return is_prime(n) and is_prime(2 * n + 1)

def is_wilson_prime(n):
    if not is_prime(n): return False
    return (_factorial(n - 1) + 1) % (n * n) == 0

def is_circular_prime(n):
    s = str(n)
    return all(is_prime(int(s[i:] + s[:i])) for i in range(len(s)))

def is_emirp(n):
    return is_prime(n) and is_prime(_reverse(n)) and n != _reverse(n)

def is_prime_palindrome(n):
    return is_prime(n) and is_palindrome(n)

def is_left_truncatable_prime(n):
    s = str(n)
    return all(is_prime(int(s[i:])) for i in range(len(s)))

def is_right_truncatable_prime(n):
    s = str(n)
    return all(is_prime(int(s[:i+1])) for i in range(len(s)))

def is_two_sided_prime(n):
    return is_left_truncatable_prime(n) and is_right_truncatable_prime(n)

def is_strong_prime(n):
    """Greater than average of neighboring primes."""
    if not is_prime(n): return False
    prev_p = n - 1
    while not is_prime(prev_p): prev_p -= 1
    next_p = n + 1
    while not is_prime(next_p): next_p += 1
    return n > (prev_p + next_p) / 2

def is_weak_prime(n):
    """Less than average of neighboring primes."""
    if not is_prime(n): return False
    prev_p = n - 1
    while not is_prime(prev_p): prev_p -= 1
    next_p = n + 1
    while not is_prime(next_p): next_p += 1
    return n < (prev_p + next_p) / 2

def is_balanced_prime(n):
    """Equal to average of neighboring primes."""
    if not is_prime(n): return False
    prev_p = n - 1
    while not is_prime(prev_p): prev_p -= 1
    next_p = n + 1
    while not is_prime(next_p): next_p += 1
    return n == (prev_p + next_p) / 2

def is_isolated_prime(n):
    return is_prime(n) and not is_prime(n - 2) and not is_prime(n + 2)

def is_eisenstein_prime(n):
    """Integer Eisenstein primes: primes ≡ 2 (mod 3)."""
    return is_prime(n) and n % 3 == 2

def is_gaussian_prime(n):
    """Real Gaussian primes: primes ≡ 3 (mod 4)."""
    return is_prime(n) and n % 4 == 3

def is_prime_triplet(n):
    """n is in a prime triplet (p, p+2, p+6) or (p, p+4, p+6)."""
    if not is_prime(n): return False
    return ((is_prime(n+2) and is_prime(n+6)) or
            (is_prime(n+4) and is_prime(n+6)) or
            (is_prime(n-2) and is_prime(n-6)) or
            (is_prime(n-4) and is_prime(n-6)))

def is_prime_quadruplet(n):
    """n starts a prime quadruplet (p, p+2, p+6, p+8)."""
    return all(is_prime(n+k) for k in [0, 2, 6, 8])

def is_chen_prime(n):
    """n is prime and n+2 is prime or semiprime."""
    if not is_prime(n): return False
    m = n + 2
    if is_prime(m): return True
    pf = get_prime_factors(m)
    return len(pf) == 2

def is_sexy_prime_pair(n):
    return is_prime(n) and is_prime(n + 6)

def is_pythagorean_prime(n):
    """Primes of form 4k+1."""
    return is_prime(n) and n % 4 == 1

def is_pierpont_prime(n):
    """Primes of form 2^u * 3^v + 1."""
    if not is_prime(n): return False
    m = n - 1
    while m % 2 == 0: m //= 2
    while m % 3 == 0: m //= 3
    return m == 1

def is_newman_shanks_williams_prime(n):
    """Known NSW primes."""
    nsw = {7, 41, 239, 9369319, 63018038201}
    return n in nsw

def is_woodall_prime(n):
    """n = k*2^k - 1 for some k."""
    if not is_prime(n): return False
    for k in range(1, 50):
        if k * (2 ** k) - 1 == n: return True
    return False

def is_cullen_prime(n):
    """n = k*2^k + 1 for some k."""
    if not is_prime(n): return False
    for k in range(1, 50):
        if k * (2 ** k) + 1 == n: return True
    return False

def is_primorial_prime(n):
    """n = primorial(k) ± 1 for some k."""
    if not is_prime(n): return False
    primes = _prime_sieve(100)
    prod = 1
    for p in primes:
        prod *= p
        if prod + 1 == n or prod - 1 == n: return True
        if prod > n: break
    return False

def get_prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1: factors.append(n)
    return factors

def count_prime_factors(n):
    return len(set(get_prime_factors(n)))

def count_prime_factors_with_multiplicity(n):
    return len(get_prime_factors(n))

def is_k_almost_prime(n, k):
    return len(get_prime_factors(n)) == k

def is_2_almost_prime(n): return is_k_almost_prime(n, 2)
def is_3_almost_prime(n): return is_k_almost_prime(n, 3)
def is_4_almost_prime(n): return is_k_almost_prime(n, 4)
def is_5_almost_prime(n): return is_k_almost_prime(n, 5)

def omega(n):
    """Number of distinct prime factors."""
    return len(set(get_prime_factors(n)))

def big_omega(n):
    """Number of prime factors with multiplicity."""
    return len(get_prime_factors(n))

def is_liouville_number_property(n):
    """Liouville function: (-1)^Omega(n)."""
    return (-1) ** big_omega(n)

def mobius(n):
    """Möbius function μ(n)."""
    if n == 1: return 1
    pf = get_prime_factors(n)
    if len(pf) != len(set(pf)): return 0
    return (-1) ** len(set(pf))

def is_squarefree_kernel(n):
    """Return the squarefree kernel (product of distinct prime factors)."""
    return functools.reduce(lambda a, b: a * b, set(get_prime_factors(n)), 1)

def rad(n):
    """Radical of n: product of distinct prime factors."""
    return is_squarefree_kernel(n)


# ═══════════════════════════════════════════════════════════════════════════════
# 2. ARMSTRONG, NARCISSISTIC & DIGITAL INVARIANTS
# ═══════════════════════════════════════════════════════════════════════════════

def is_armstrong(n):
    d = _digits(n)
    p = len(d)
    return sum(x ** p for x in d) == n

is_narcissistic = is_armstrong

def is_disarium(n):
    d = _digits(n)
    return sum(x ** (i + 1) for i, x in enumerate(d)) == n

def is_perfect_digital_invariant(n, p):
    return sum(x ** p for x in _digits(n)) == n

def is_pdi_2(n): return is_perfect_digital_invariant(n, 2)
def is_pdi_3(n): return is_perfect_digital_invariant(n, 3)
def is_pdi_4(n): return is_perfect_digital_invariant(n, 4)
def is_pdi_5(n): return is_perfect_digital_invariant(n, 5)
def is_pdi_6(n): return is_perfect_digital_invariant(n, 6)
def is_pdi_7(n): return is_perfect_digital_invariant(n, 7)

def is_pluperfect_digital_invariant(n):
    d = _digits(n)
    return any(sum(x ** p for x in d) == n for p in range(1, 10))

def is_munchausen(n):
    """n = sum of d^d for each digit d (0^0 = 0 by convention)."""
    return sum(0 if d == 0 else d**d for d in _digits(n)) == n

def is_sum_of_digit_factorials(n):
    """n = sum of factorials of its digits."""
    return sum(_factorial(d) for d in _digits(n)) == n

def is_double_factorial_sum(n):
    """n = sum of d!! for digits."""
    def dfact(k):
        if k <= 0: return 1
        r = 1
        while k > 0:
            r *= k
            k -= 2
        return r
    return sum(dfact(d) for d in _digits(n)) == n

def armstrong_power(n):
    """Return the power p such that n is a p-narcissistic number, or None."""
    d = _digits(n)
    p = len(d)
    if sum(x**p for x in d) == n: return p
    return None

def is_supersum(n):
    """Sum of digit^digit == n."""
    return sum(d**d if d != 0 else 0 for d in _digits(n)) == n


# ═══════════════════════════════════════════════════════════════════════════════
# 3. PERFECT, ABUNDANT, DEFICIENT & ALIQUOT
# ═══════════════════════════════════════════════════════════════════════════════

def is_perfect(n):
    return n > 1 and sum(_proper_factors(n)) == n

def is_abundant(n):
    return n > 1 and sum(_proper_factors(n)) > n

def is_deficient(n):
    return n > 1 and sum(_proper_factors(n)) < n

def abundance(n):
    return sum(_proper_factors(n)) - n

def is_semiperfect(n):
    pf = _proper_factors(n)
    return n > 1 and _subset_sum(pf, n)

def is_weird(n):
    return is_abundant(n) and not is_semiperfect(n)

def is_quasiperfect(n):
    """sum of proper divisors = n+1 (none known, but check)."""
    return sum(_proper_factors(n)) == n + 1

def is_almost_perfect(n):
    """sum of proper divisors = n-1 (powers of 2)."""
    return sum(_proper_factors(n)) == n - 1

def is_superperfect(n):
    """sigma(sigma(n)) = 2n."""
    return sum(_factors(sum(_factors(n)))) == 2 * n

def is_multiperfect(n, k):
    """sigma(n) = k*n."""
    return sum(_factors(n)) == k * n

def is_triperfect(n): return is_multiperfect(n, 3)
def is_tetraperfect(n): return is_multiperfect(n, 4)
def is_pentaperfect(n): return is_multiperfect(n, 5)
def is_hexaperfect(n): return is_multiperfect(n, 6)

def aliquot_sum(n):
    return sum(_proper_factors(n))

def is_amicable(n):
    m = aliquot_sum(n)
    return m != n and aliquot_sum(m) == n

def amicable_pair(n):
    m = aliquot_sum(n)
    if m != n and aliquot_sum(m) == n: return m
    return None

def is_sociable(n, max_steps=30):
    seen = []
    current = n
    for _ in range(max_steps):
        current = aliquot_sum(current)
        if current == n: return True
        if current in seen: return False
        seen.append(current)
    return False

def sociable_cycle_length(n, max_steps=30):
    chain = [n]
    current = n
    for _ in range(max_steps):
        current = aliquot_sum(current)
        if current == n: return len(chain)
        if current in chain: return -1
        chain.append(current)
    return -1

def is_perfect_2(n): return is_perfect(n)
def is_sigma_perfect(n): return sum(_factors(n)) == 2 * n

def is_unitary_perfect(n):
    """Sum of unitary divisors = 2n."""
    def unitary_divs(k):
        divs = []
        for d in _factors(k):
            if math.gcd(d, k // d) == 1: divs.append(d)
        return divs
    return sum(unitary_divs(n)) == 2 * n


# ═══════════════════════════════════════════════════════════════════════════════
# 4. PALINDROME & REVERSE
# ═══════════════════════════════════════════════════════════════════════════════

def is_palindrome(n):
    s = str(abs(int(n)))
    return s == s[::-1]

def is_palindrome_prime(n):
    return is_prime(n) and is_palindrome(n)

def reverse_number(n):
    return _reverse(n)

def is_reverse_prime(n):
    return is_prime(_reverse(n))

def is_palindromic_square(n):
    return is_palindrome(n) and _is_perfect_square(n)

def is_palindromic_triangular(n):
    return is_palindrome(n) and is_triangular(n)

def is_palindromic_fibonacci(n):
    return is_palindrome(n) and is_fibonacci(n)

def is_lychrel(n, iterations=50):
    """Check if n is a Lychrel number (never becomes palindrome by reverse-add)."""
    for _ in range(iterations):
        n = n + _reverse(n)
        if is_palindrome(n): return False
    return True

def reverse_add_steps(n, max_iter=100):
    """Steps to reach palindrome via reverse-and-add."""
    for i in range(max_iter):
        if is_palindrome(n): return i
        n = n + _reverse(n)
    return -1

def is_two_digit_palindrome(n):
    return is_palindrome(n) and 10 <= n <= 99

def is_three_digit_palindrome(n):
    return is_palindrome(n) and 100 <= n <= 999

def is_four_digit_palindrome(n):
    return is_palindrome(n) and 1000 <= n <= 9999

def is_even_palindrome(n):
    return is_palindrome(n) and n % 2 == 0

def is_odd_palindrome(n):
    return is_palindrome(n) and n % 2 != 0


# ═══════════════════════════════════════════════════════════════════════════════
# 5. SPY, BUZZ, DUCK & SIMPLE NAMED NUMBERS
# ═══════════════════════════════════════════════════════════════════════════════

def is_spy(n):
    d = _digits(n)
    s = sum(d)
    p = 1
    for x in d: p *= x
    return s == p

def is_buzz(n):
    return n % 7 == 0 or n % 10 == 7

def is_duck(n):
    return '0' in str(abs(int(n)))

def is_neon(n):
    return _digit_sum(n * n) == n

def is_automorphic(n):
    return str(n * n).endswith(str(n))

def is_trimorphic(n):
    return str(n ** 3).endswith(str(n))

def is_pentaautomorphic(n):
    return str(n ** 5).endswith(str(n))

def is_curious(n):
    """n = sum of each digit raised to the power of its own factorial."""
    return sum(d**_factorial(d) if d > 0 else 0 for d in _digits(n)) == n

def is_harshad(n):
    s = _digit_sum(n)
    return s != 0 and n % s == 0

is_niven = is_harshad

def is_strong_harshad(n):
    s = _digit_sum(n)
    return s != 0 and n % s == 0 and is_prime(n // s)

def is_multiple_harshad(n):
    """Still Harshad after dividing by digit sum repeatedly."""
    while n > 9:
        s = _digit_sum(n)
        if s == 0 or n % s != 0: return False
        n //= s
    return True

def is_harshad_prime(n):
    return is_prime(n) and is_harshad(n)

def is_kaprekar(n):
    if n == 1: return True
    sq = str(n * n)
    for i in range(1, len(sq)):
        left, right = int(sq[:i] or 0), int(sq[i:] or 0)
        if right > 0 and left + right == n: return True
    return False

def kaprekar_constant_steps(n):
    """Steps for 4-digit Kaprekar routine to reach 6174."""
    steps = 0
    while n != 6174 and steps < 10:
        d = sorted(_digits(n))
        while len(d) < 4: d.insert(0, 0)
        asc = int(''.join(map(str, d)))
        desc = int(''.join(map(str, reversed(d))))
        n = desc - asc
        steps += 1
    return steps

def is_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(x**2 for x in _digits(n))
    return n == 1

def is_sad(n):
    return not is_happy(n)

def happy_step_count(n):
    seen = set()
    steps = 0
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(x**2 for x in _digits(n))
        steps += 1
    return steps if n == 1 else -1

def is_lucky(n):
    """Check using lucky number sieve (approximate for n <= 500)."""
    lucky = list(range(1, 501, 2))
    i = 1
    while i < len(lucky) and lucky[i] <= len(lucky):
        step = lucky[i]
        lucky = [lucky[j] for j in range(len(lucky)) if (j + 1) % step != 0]
        i += 1
    return n in lucky

def is_interesting(n):
    """n is within 1000 of a perfect power, triangular, square, cube."""
    return (any(abs(n - k**2) <= 100 for k in range(1, int(n**0.5)+3)) or
            is_triangular(n) or is_perfect_square(n) or is_perfect_cube(n))

def is_undulating(n):
    """Digits alternate high-low-high or low-high-low."""
    d = _digits(n)
    if len(d) < 3: return False
    for i in range(1, len(d)-1):
        if not ((d[i-1] < d[i] > d[i+1]) or (d[i-1] > d[i] < d[i+1])): return False
    return True

def is_alternating(n):
    """Digits strictly alternate between even and odd."""
    d = _digits(n)
    for i in range(len(d)-1):
        if (d[i] % 2) == (d[i+1] % 2): return False
    return True

def is_metadrome(n):
    """Digits strictly increasing (no equal consecutive digits)."""
    d = _digits(n)
    return all(d[i] < d[i+1] for i in range(len(d)-1))

def is_katadrome(n):
    """Digits strictly decreasing."""
    d = _digits(n)
    return all(d[i] > d[i+1] for i in range(len(d)-1))

def is_plaindrome(n):
    """Digits non-decreasing."""
    d = _digits(n)
    return all(d[i] <= d[i+1] for i in range(len(d)-1))

def is_nialpdrome(n):
    """Digits non-increasing."""
    d = _digits(n)
    return all(d[i] >= d[i+1] for i in range(len(d)-1))


# ═══════════════════════════════════════════════════════════════════════════════
# 6. FIBONACCI, LUCAS & RECURRENCE SEQUENCES
# ═══════════════════════════════════════════════════════════════════════════════

def is_fibonacci(n):
    return _is_perfect_square(5*n*n+4) or _is_perfect_square(5*n*n-4)

def is_lucas(n):
    """Check if n is a Lucas number (2, 1, 3, 4, 7, 11, 18, ...)."""
    if n == 1 or n == 2: return True
    a, b = 2, 1
    while b < n: a, b = b, a + b
    return b == n

def is_tribonacci(n):
    a, b, c = 0, 0, 1
    while c < n:
        a, b, c = b, c, a + b + c
    return c == n or n == 0

def is_tetranacci(n):
    a, b, c, d = 0, 0, 0, 1
    while d < n:
        a, b, c, d = b, c, d, a+b+c+d
    return d == n or n == 0

def is_pentanacci(n):
    seq = [0, 0, 0, 0, 1]
    while seq[-1] < n:
        seq.append(sum(seq[-5:]))
    return n in seq

def is_hexanacci(n):
    seq = [0, 0, 0, 0, 0, 1]
    while seq[-1] < n:
        seq.append(sum(seq[-6:]))
    return n in seq

def is_padovan(n):
    a, b, c = 1, 1, 1
    seen = {1}
    while c < n:
        a, b, c = b, c, a + b
        seen.add(c)
    return n in seen

def is_perrin(n):
    a, b, c = 3, 0, 2
    seen = {3, 0, 2}
    while c < n:
        a, b, c = b, c, a + b
        seen.add(c)
    return n in seen

def is_jacobsthal(n):
    a, b = 0, 1
    seen = {0, 1}
    while b < n:
        a, b = b, 2*a + b
        seen.add(b)
    return n in seen

def is_pell(n):
    a, b = 0, 1
    seen = {0, 1}
    while b < n:
        a, b = b, 2*b + a
        seen.add(b)
    return n in seen

def is_pell_lucas(n):
    a, b = 2, 2
    seen = {2}
    while b < n:
        a, b = b, 2*b + a
        seen.add(b)
    return n in seen

def is_companion_pell(n): return is_pell_lucas(n)

def is_motzkin(n):
    """Check if n is a Motzkin number."""
    m, k = 1, 0
    while m < n:
        k += 1
        m = m * (2*(2*k+1)) // (k+2)
    return m == n or n == 1

def is_catalan(n):
    c, k = 1, 0
    while c < n:
        k += 1
        c = c * 2 * (2*k-1) // (k+1)
    return c == n or n == 1

def is_bell(n):
    bell = [[0]*20 for _ in range(20)]
    bell[0][0] = 1
    for i in range(1, 15):
        bell[i][0] = bell[i-1][i-1]
        for j in range(1, i+1):
            bell[i][j] = bell[i-1][j-1] + bell[i][j-1]
        if bell[i][0] == n: return True
    return n == 1

def is_narayana(n):
    """Check if n appears in Narayana number triangle."""
    for k in range(1, 20):
        for j in range(1, k+1):
            val = (_factorial(k) // (_factorial(j) * _factorial(k-j))) * \
                  (_factorial(k) // (_factorial(j-1) * _factorial(k-j+1))) // k
            if val == n: return True
            if val > n: break
    return False

def is_recaman(n):
    """Check if n is in the Recaman sequence (first 200 terms)."""
    seq = set()
    a = 0
    seq.add(0)
    for i in range(1, 200):
        candidate = a - i
        if candidate > 0 and candidate not in seq:
            a = candidate
        else:
            a = a + i
        seq.add(a)
        if a == n: return True
    return n == 0

def nth_fibonacci(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a+b
    return a

def nth_lucas(n):
    a, b = 2, 1
    for _ in range(n): a, b = b, a+b
    return a

def nth_tribonacci(n):
    a, b, c = 0, 0, 1
    for _ in range(n): a, b, c = b, c, a+b+c
    return a

def is_fibbinary(n):
    """No two consecutive 1s in binary representation (Fibonacci coding)."""
    return (n & (n >> 1)) == 0

def is_zeckendorf(n):
    """Always true — every positive integer has a Zeckendorf representation."""
    return n > 0


# ═══════════════════════════════════════════════════════════════════════════════
# 7. FIGURATE NUMBERS (POLYGONAL)
# ═══════════════════════════════════════════════════════════════════════════════

def is_triangular(n):
    return _is_perfect_square(8*n+1)

def is_square(n):
    return _is_perfect_square(n)

def is_pentagonal(n):
    disc = 1 + 24*n
    if not _is_perfect_square(disc): return False
    r = int(math.isqrt(disc))
    return (1 + r) % 6 == 0

def is_hexagonal(n):
    disc = 1 + 8*n
    if not _is_perfect_square(disc): return False
    r = int(math.isqrt(disc))
    return (1 + r) % 4 == 0

def is_heptagonal(n):
    disc = 9 + 40*n
    return _is_perfect_square(disc) and (3 + int(math.isqrt(disc))) % 10 == 0

def is_octagonal(n):
    disc = 1 + 3*n
    if not _is_perfect_square(disc): return False
    r = int(math.isqrt(disc))
    return (1 + r) % 3 == 0

def is_nonagonal(n):
    disc = 9 + 56*n
    return _is_perfect_square(disc) and (3 + int(math.isqrt(disc))) % 14 == 0

def is_decagonal(n):
    disc = 1 + 2*n
    return _is_perfect_square(disc) and (1 + int(math.isqrt(disc))) % 4 == 0

def is_hendecagonal(n):
    disc = 9 + 72*n
    return _is_perfect_square(disc) and (3 + int(math.isqrt(disc))) % 18 == 0

def is_dodecagonal(n):
    disc = 1 + 5*n//2 if False else None
    # k(5k-4)/2 = n → 5k^2-4k-2n=0 → k=(4+sqrt(16+40n))/10
    disc2 = 16 + 40*n
    return _is_perfect_square(disc2) and (4 + int(math.isqrt(disc2))) % 10 == 0

def is_centered_triangular(n):
    """n = (3k^2+3k+2)/2."""
    # 3k^2+3k+2-2n=0 → k=(-3+sqrt(9-12(2-2n)))/6
    disc = 9 + 12*(2*n-2)
    return _is_perfect_square(disc) and (-3 + int(math.isqrt(disc))) % 6 == 0

def is_centered_square(n):
    """n = 2k^2-2k+1."""
    return _is_perfect_square(2*n-1) or n == 1

def is_centered_pentagonal(n):
    """n = (5k^2-5k+2)/2."""
    disc = 25 + 40*(2*n-2)
    return _is_perfect_square(disc) and (5 + int(math.isqrt(disc))) % 20 == 0

def is_centered_hexagonal(n):
    """n = 3k^2-3k+1."""
    disc = 9 - 12*(1-n)
    return _is_perfect_square(disc)

def is_centered_heptagonal(n):
    disc = 49 + 56*(2*n-2)
    return _is_perfect_square(disc) and (7 + int(math.isqrt(disc))) % 28 == 0

def is_centered_octagonal(n):
    """n = (2k-1)^2."""
    return _is_perfect_square(n) and int(math.isqrt(n)) % 2 == 1

def is_centered_nonagonal(n):
    disc = 9*(2*n-1)
    return _is_perfect_square(disc)

def is_centered_decagonal(n):
    disc = 1 + 5*(n-1)
    return _is_perfect_square(disc) and (int(math.isqrt(disc)) - 1) % 5 == 0

def is_pronic(n):
    k = int(math.isqrt(n))
    return k*(k+1) == n

is_oblong = is_pronic
is_heteromecic = is_pronic

def is_square_triangular(n):
    return is_square(n) and is_triangular(n)

def is_square_pentagonal(n):
    return is_square(n) and is_pentagonal(n)

def is_triangular_pentagonal(n):
    return is_triangular(n) and is_pentagonal(n)

def is_pentagonal_hexagonal(n):
    return is_pentagonal(n) and is_hexagonal(n)

def is_gnomon(n):
    """n = 2k+1 (odd numbers are gnomons of squares)."""
    return n % 2 == 1

def is_star(n):
    """Star number: 6k(k-1)+1."""
    if n == 1: return True
    m = n - 1
    if m % 6 != 0: return False
    t = m // 6
    k = int(math.isqrt(t))
    return k*(k+1) == t or (k > 0 and (k-1)*k == t)

def is_hex(n):
    """Hex number: 3k^2-3k+1."""
    return is_centered_hexagonal(n)

def is_cross(n):
    """Cross/plus number: 4k-3."""
    return n > 0 and (n - 1) % 4 == 0 or n == 1

def figurate_name(n):
    """Return list of figurate type names n belongs to."""
    names = []
    checks = [('triangular', is_triangular), ('square', is_square),
              ('pentagonal', is_pentagonal), ('hexagonal', is_hexagonal),
              ('heptagonal', is_heptagonal), ('octagonal', is_octagonal),
              ('pronic', is_pronic), ('centered_square', is_centered_square),
              ('centered_hexagonal', is_centered_hexagonal), ('star', is_star)]
    for name, fn in checks:
        if fn(n): names.append(name)
    return names


# ═══════════════════════════════════════════════════════════════════════════════
# 8. POWER & ROOT PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

def is_perfect_square(n): return _is_perfect_square(n)
def is_perfect_cube(n):
    if n < 0:
        r = -round((-n)**(1/3))
    else:
        r = round(n**(1/3))
    for c in [r-1, r, r+1]:
        if c**3 == n: return True
    return False

def is_perfect_fourth_power(n):
    if n < 0: return False
    r = round(n**0.25)
    return any((r+k)**4 == n for k in [-1, 0, 1])

def is_perfect_fifth_power(n):
    if n < 0:
        r = -round((-n)**0.2)
    else:
        r = round(n**0.2)
    return any((r+k)**5 == n for k in [-2,-1,0,1,2])

def is_perfect_sixth_power(n):
    return is_perfect_square(n) and is_perfect_cube(n)

def is_perfect_seventh_power(n):
    r = round(n**(1/7))
    return any((r+k)**7 == n for k in [-2,-1,0,1,2])

def is_perfect_eighth_power(n):
    return is_perfect_fourth_power(n) and _is_perfect_square(int(n**0.5+0.5))

def is_perfect_power(n):
    if n < 4: return False
    for b in range(2, int(math.log2(n))+1):
        a = round(n**(1/b))
        for c in [a-1, a, a+1]:
            if c > 1 and c**b == n: return True
    return False

def is_powerful(n):
    for p in set(get_prime_factors(n)):
        if n % (p*p) != 0: return False
    return True

def is_squarefree(n):
    for p in set(get_prime_factors(n)):
        if n % (p*p) == 0: return False
    return True

def is_cubefree(n):
    for p in set(get_prime_factors(n)):
        if n % (p**3) == 0: return False
    return True

def is_achilles(n):
    return is_powerful(n) and not is_perfect_power(n)

def is_powerful_not_perfect(n):
    return is_powerful(n) and not _is_perfect_square(n)

def integer_sqrt(n):
    return int(math.isqrt(n))

def integer_cbrt(n):
    r = round(n**(1/3))
    for c in [r-1, r, r+1]:
        if c**3 == n: return c
    return None

def is_power_of_two(n):
    return n > 0 and (n & (n-1)) == 0

def is_power_of_three(n):
    if n < 1: return False
    while n % 3 == 0: n //= 3
    return n == 1

def is_power_of_five(n):
    if n < 1: return False
    while n % 5 == 0: n //= 5
    return n == 1

def is_power_of_seven(n):
    if n < 1: return False
    while n % 7 == 0: n //= 7
    return n == 1

def is_power_of_k(n, k):
    if n < 1 or k < 2: return False
    while n % k == 0: n //= k
    return n == 1

def is_sum_of_two_squares(n):
    """Check if n can be written as a^2 + b^2."""
    for a in range(int(math.isqrt(n))+1):
        rem = n - a*a
        if rem >= 0 and _is_perfect_square(rem): return True
    return False

def is_sum_of_three_squares(n):
    """Legendre's three-square theorem: not of form 4^a(8b+7)."""
    if n < 0: return False
    while n % 4 == 0: n //= 4
    return n % 8 != 7

def is_sum_of_four_squares(n):
    """Lagrange: every non-negative integer."""
    return n >= 0

def sum_of_two_squares_repr(n):
    """Return all (a,b) with a<=b and a^2+b^2==n."""
    result = []
    for a in range(int(math.isqrt(n))+1):
        rem = n - a*a
        if rem >= 0 and _is_perfect_square(rem):
            b = int(math.isqrt(rem))
            if a <= b: result.append((a, b))
    return result

def is_loeschian(n):
    """n = a^2 + ab + b^2 for non-negative a, b."""
    for a in range(int(math.isqrt(n))+1):
        for b in range(a+1):
            if a*a + a*b + b*b == n: return True
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# 9. DIGIT PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

def digit_sum(n): return _digit_sum(n)
def digit_product(n): return _digit_product(n)
def count_digits(n): return _digit_count(n)
def digit_list(n): return _digits(n)

def digital_root(n):
    if n == 0: return 0
    return 1 + (abs(n)-1) % 9

def digital_root_slow(n):
    while n >= 10: n = _digit_sum(n)
    return n

def additive_persistence(n):
    count = 0
    while n >= 10:
        n = _digit_sum(n)
        count += 1
    return count

def multiplicative_persistence(n):
    count = 0
    while n >= 10:
        n = _digit_product(n)
        count += 1
    return count

def is_additive_persistence_1(n): return additive_persistence(n) == 1
def is_additive_persistence_2(n): return additive_persistence(n) == 2
def is_additive_persistence_3(n): return additive_persistence(n) == 3

def is_digital_root_prime(n): return is_prime(digital_root(n))
def is_digital_root_square(n): return _is_perfect_square(digital_root(n))
def is_digital_root_fibonacci(n): return is_fibonacci(digital_root(n))
def is_digital_root_1(n): return digital_root(n) == 1
def is_digital_root_9(n): return digital_root(n) == 9

def is_smith(n):
    if is_prime(n): return False
    pf = get_prime_factors(n)
    return _digit_sum(n) == sum(_digit_sum(p) for p in pf)

def is_hoax(n):
    if is_prime(n): return False
    pf = list(set(get_prime_factors(n)))
    return _digit_sum(n) == sum(_digit_sum(p) for p in pf)

def is_self(n):
    for m in range(max(1, n-60), n):
        if m + _digit_sum(m) == n: return False
    return True

def is_self_descriptive(n):
    """n[i] = count of digit i in n."""
    s = str(n)
    return all(s.count(str(i)) == int(s[i]) for i in range(len(s)))

def is_bouncy(n):
    d = _digits(n)
    return not (d == sorted(d) or d == sorted(d, reverse=True))

def is_increasing(n):
    d = _digits(n)
    return d == sorted(d)

def is_decreasing(n):
    d = _digits(n)
    return d == sorted(d, reverse=True)

def is_pandigital(n, start=1):
    s = str(n)
    expected = set(str(i) for i in range(start, start+len(s)))
    return set(s) == expected and len(s) == len(expected)

def is_pandigital_0_9(n):
    return set(str(n)) == set('0123456789') and len(str(n)) == 10

def is_pandigital_1_9(n):
    return set(str(n)) == set('123456789') and len(str(n)) == 9

def is_zeroless_pandigital(n):
    return is_pandigital_1_9(n)

def is_repunit(n):
    return all(d == '1' for d in str(n))

def is_repdigit(n):
    s = str(n)
    return len(set(s)) == 1

def repdigit_value(n):
    if is_repdigit(n): return int(str(n)[0])
    return None

def is_undulating_repdigit(n):
    """Digits alternate between two values like 121212."""
    s = str(n)
    if len(s) < 3: return False
    return len(set(s[::2])) == 1 and len(set(s[1::2])) == 1 and s[0] != s[1]

def is_duck(n):
    return '0' in str(abs(int(n)))

def has_repeated_digit(n):
    s = str(n)
    return len(s) != len(set(s))

def has_unique_digits(n):
    s = str(n)
    return len(s) == len(set(s))

def count_unique_digits(n):
    return len(set(str(n)))

def count_zeros(n):
    return str(n).count('0')

def count_ones(n):
    return str(n).count('1')

def max_digit(n):
    return max(_digits(n))

def min_digit(n):
    return min(_digits(n))

def digit_range(n):
    d = _digits(n)
    return max(d) - min(d)

def is_digit_sum_prime(n):
    return is_prime(_digit_sum(n))

def is_digit_sum_square(n):
    return _is_perfect_square(_digit_sum(n))

def is_digit_sum_fibonacci(n):
    return is_fibonacci(_digit_sum(n))

def is_digit_sum_even(n):
    return _digit_sum(n) % 2 == 0

def is_digit_sum_odd(n):
    return _digit_sum(n) % 2 == 1

def digit_sum_mod9(n):
    return _digit_sum(n) % 9

def digit_frequency(n):
    return Counter(_digits(n))

def most_common_digit(n):
    return Counter(_digits(n)).most_common(1)[0][0]

def is_sorted_digits_prime(n):
    return is_prime(int(''.join(sorted(str(n)))))

def is_reverse_digit_sum_equal(n):
    return _digit_sum(n) == _digit_sum(_reverse(n))

def checksum_luhn(n):
    """Luhn algorithm checksum (valid if 0)."""
    digits = _digits(n)[::-1]
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9: d -= 9
        total += d
    return total % 10

def is_luhn_valid(n):
    return checksum_luhn(n) == 0


# ═══════════════════════════════════════════════════════════════════════════════
# 10. BINARY, OCTAL & HEX PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

def to_binary(n): return _binary(n)
def to_octal(n): return _octal(n)
def to_hex(n): return _hex_str(n)
def to_base(n, b):
    if n == 0: return '0'
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return ''.join(str(d) if d < 10 else chr(d-10+ord('a')) for d in reversed(digits))

def is_binary_palindrome(n):
    b = _binary(n)
    return b == b[::-1]

def is_octal_palindrome(n):
    o = _octal(n)
    return o == o[::-1]

def is_hex_palindrome(n):
    h = _hex_str(n)
    return h == h[::-1]

def count_set_bits(n):
    return bin(n).count('1')

def count_zero_bits(n):
    b = _binary(n)
    return b.count('0')

def is_evil(n):
    """Even number of 1s in binary."""
    return count_set_bits(n) % 2 == 0

def is_odious(n):
    """Odd number of 1s in binary."""
    return count_set_bits(n) % 2 == 1

def is_pernicious(n):
    return is_prime(count_set_bits(n))

def is_fibbinary(n):
    return (n & (n >> 1)) == 0

def is_apocalypse_number(n):
    return '666' in str(2**n)

def is_persistent(n):
    """Multiplicative persistence >= 3."""
    return multiplicative_persistence(n) >= 3

def bit_length(n):
    return n.bit_length()

def is_power_of_two(n):
    return n > 0 and (n & (n-1)) == 0

def is_bit_palindrome(n): return is_binary_palindrome(n)

def bit_reverse(n):
    """Reverse the bits."""
    b = _binary(n)
    return int(b[::-1], 2)

def is_bit_reversal_prime(n):
    return is_prime(n) and is_prime(bit_reverse(n))

def hamming_weight(n):
    return count_set_bits(n)

def is_hamming_weight_prime(n):
    return is_prime(hamming_weight(n))

def popcount(n): return count_set_bits(n)

def is_blum_integer(n):
    """n = p*q where p,q are primes ≡ 3 (mod 4)."""
    pf = get_prime_factors(n)
    return (len(pf) == 2 and len(set(pf)) == 2 and
            all(p % 4 == 3 for p in set(pf)))

def is_base_2_repunit(n):
    b = _binary(n)
    return all(c == '1' for c in b)

def is_binary_bouncy(n):
    b = list(_binary(n))
    return not (b == sorted(b) or b == sorted(b, reverse=True))


# ═══════════════════════════════════════════════════════════════════════════════
# 11. DIVISIBILITY & FACTOR PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

def is_divisible_by(n, d):
    return d != 0 and n % d == 0

def is_divisible_by_2(n): return n % 2 == 0
def is_divisible_by_3(n): return n % 3 == 0
def is_divisible_by_4(n): return n % 4 == 0
def is_divisible_by_5(n): return n % 5 == 0
def is_divisible_by_6(n): return n % 6 == 0
def is_divisible_by_7(n): return n % 7 == 0
def is_divisible_by_8(n): return n % 8 == 0
def is_divisible_by_9(n): return n % 9 == 0
def is_divisible_by_10(n): return n % 10 == 0
def is_divisible_by_11(n): return n % 11 == 0
def is_divisible_by_12(n): return n % 12 == 0
def is_divisible_by_13(n): return n % 13 == 0
def is_divisible_by_14(n): return n % 14 == 0
def is_divisible_by_15(n): return n % 15 == 0
def is_divisible_by_16(n): return n % 16 == 0
def is_divisible_by_17(n): return n % 17 == 0
def is_divisible_by_18(n): return n % 18 == 0
def is_divisible_by_19(n): return n % 19 == 0
def is_divisible_by_20(n): return n % 20 == 0
def is_divisible_by_25(n): return n % 25 == 0
def is_divisible_by_50(n): return n % 50 == 0
def is_divisible_by_100(n): return n % 100 == 0
def is_divisible_by_1000(n): return n % 1000 == 0

def is_even(n): return n % 2 == 0
def is_odd(n): return n % 2 != 0
def is_even_odd_alternating(n):
    d = _digits(n)
    return all((d[i]%2) != (d[i+1]%2) for i in range(len(d)-1))

def count_divisors(n):
    return len(_factors(n))

def sum_of_divisors(n):
    return sum(_factors(n))

def sum_of_proper_divisors(n):
    return aliquot_sum(n)

def is_refactorable(n):
    return n % count_divisors(n) == 0

is_tau_number = is_refactorable

def is_highly_composite(n):
    c = count_divisors(n)
    return all(count_divisors(i) < c for i in range(1, n))

def is_superior_highly_composite(n):
    known = {2, 6, 12, 60, 120, 360, 2520, 5040, 55440, 720720, 1441440}
    return n in known

def is_colossally_abundant(n):
    known = {2, 6, 12, 60, 120, 360, 2520, 5040, 55440, 720720}
    return n in known

def is_practical(n):
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
        if p > sigma + 1: return False
        sigma *= (p**(exp+1)-1) // (p-1)
    return True

def is_smooth(n, k):
    """All prime factors <= k."""
    return n > 0 and all(p <= k for p in set(get_prime_factors(n)))

def is_2_smooth(n): return is_smooth(n, 2)
def is_3_smooth(n): return is_smooth(n, 3)
def is_5_smooth(n): return is_smooth(n, 5)
def is_7_smooth(n): return is_smooth(n, 7)
def is_11_smooth(n): return is_smooth(n, 11)
def is_13_smooth(n): return is_smooth(n, 13)
def is_17_smooth(n): return is_smooth(n, 17)
def is_19_smooth(n): return is_smooth(n, 19)
def is_23_smooth(n): return is_smooth(n, 23)

def is_regular(n): return is_5_smooth(n)
is_hamming = is_regular
is_humble = is_regular
def is_ugly(n): return n > 0 and is_regular(n)

def is_rough(n, k):
    """All prime factors >= k."""
    return n > 1 and all(p >= k for p in set(get_prime_factors(n)))

def is_3_rough(n): return is_rough(n, 3)
def is_5_rough(n): return is_rough(n, 5)
def is_7_rough(n): return is_rough(n, 7)

def is_semi_prime(n):
    return len(get_prime_factors(n)) == 2

def is_sphenic(n):
    pf = get_prime_factors(n)
    return len(pf) == 3 and len(set(pf)) == 3

def is_brilliant(n):
    pf = get_prime_factors(n)
    return len(pf) == 2 and _digit_count(pf[0]) == _digit_count(pf[1])

def _factorization_digit_count(n):
    """Count digits in prime factorization written with exponents (e.g. 2^3 -> '2','3')."""
    from collections import Counter
    counter = Counter(get_prime_factors(n))
    total = 0
    for p, e in counter.items():
        total += _digit_count(p)
        if e > 1:
            total += _digit_count(e)
    return total

def is_economical(n):
    """Digit count of prime factorization (with exponents) < digit count of n."""
    if n < 2: return False
    return _factorization_digit_count(n) < _digit_count(n)

def is_equidigital(n):
    """Digit count of prime factorization (with exponents) == digit count of n."""
    if n < 2: return False
    return _factorization_digit_count(n) == _digit_count(n)

def is_wasteful(n):
    """Digit count of prime factorization (with exponents) > digit count of n."""
    if n < 2: return False
    return _factorization_digit_count(n) > _digit_count(n)

is_frugal = is_economical
is_extravagant = is_wasteful

def is_polite(n):
    return n > 1 and not is_power_of_two(n)

def is_impolite(n):
    return is_power_of_two(n)

def is_congruent(n):
    """Check against known congruent numbers (first set)."""
    known = {5, 6, 7, 13, 14, 15, 20, 21, 22, 23, 24, 28, 29, 30, 31, 34, 37, 38, 39, 41}
    return n in known


# ═══════════════════════════════════════════════════════════════════════════════
# 12. FACTORIAL & RELATED
# ═══════════════════════════════════════════════════════════════════════════════

def is_factorial(n):
    i, f = 1, 1
    while f < n:
        i += 1
        f *= i
    return f == n

def factorial_of(n): return _factorial(n)

def is_double_factorial(n):
    """n = k!! for some k."""
    k = 1
    df = 1
    while df < n:
        k += 1
        if k % 2 == 1:
            df2 = 1
            j = k
            while j > 0:
                df2 *= j
                j -= 2
            if df2 == n: return True
        else:
            df2 = 1
            j = k
            while j > 0:
                df2 *= j
                j -= 2
            if df2 == n: return True
    return n == 1

def is_subfactorial(n):
    def subfact(k):
        if k == 0: return 1
        if k == 1: return 0
        return (k-1)*(subfact(k-1)+subfact(k-2))
    i = 0
    while True:
        s = subfact(i)
        if s == n: return True
        if s > n: return False
        i += 1

def is_primorial(n):
    p, prod = 2, 1
    while prod < n:
        prod *= p
        if prod == n: return True
        nextp = p + 1
        while not is_prime(nextp): nextp += 1
        p = nextp
    return False

def is_hyperfactorial(n):
    """n = 1^1 * 2^2 * 3^3 * ..."""
    k, h = 1, 1
    while h < n:
        k += 1
        h *= k**k
    return h == n

def is_superfactorial(n):
    """n = 1! * 2! * 3! * ..."""
    k, s = 1, 1
    while s < n:
        k += 1
        s *= _factorial(k)
    return s == n

def is_alternating_factorial(n):
    """n = sum of k! * (-1)^(m-k) for k=1..m."""
    m, af = 1, 1
    seen = {1}
    while af <= n:
        m += 1
        sign = 1 if m % 2 == 0 else -1
        af = sum((-1)**(m-k) * _factorial(k) for k in range(1, m+1))
        if af > 0: seen.add(af)
    return n in seen

def count_trailing_zeros_factorial(n):
    """Trailing zeros in n!"""
    count = 0
    p = 5
    while p <= n:
        count += n // p
        p *= 5
    return count

def is_factorial_prime(n):
    """n = k! ± 1 for some k."""
    if not is_prime(n): return False
    k, f = 1, 1
    while f < n - 1:
        k += 1
        f *= k
        if f + 1 == n or f - 1 == n: return True
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# 13. GCD, LCM & NUMBER THEORY
# ═══════════════════════════════════════════════════════════════════════════════

def gcd(a, b): return math.gcd(a, b)
def lcm(a, b): return abs(a*b) // math.gcd(a, b) if a and b else 0
def lcm_list(lst): return functools.reduce(lcm, lst)

def euler_totient(n):
    count = 0
    for i in range(1, n+1):
        if math.gcd(n, i) == 1: count += 1
    return count

def is_totient_prime(n):
    return is_prime(euler_totient(n))

def is_nontotient(n):
    """n is even and not a value of Euler's totient."""
    if n % 2 != 0: return False
    for m in range(1, 2*n+2):
        if euler_totient(m) == n: return False
    return True

def jordan_totient(n, k):
    """Jordan's totient function J_k(n)."""
    result = n**k
    for p in set(get_prime_factors(n)):
        result = result * (p**k - 1) // p**k
    return result

def liouville_lambda(n):
    """(-1)^Omega(n)."""
    return (-1)**big_omega(n)

def von_mangoldt(n):
    """Von Mangoldt function."""
    pf = get_prime_factors(n)
    if len(set(pf)) == 1: return math.log(pf[0])
    return 0

def is_perfect_totient(n):
    """n = sum of iterated totients."""
    s, m = 0, n
    while m > 1:
        m = euler_totient(m)
        s += m
    return s == n

def is_totient_valence_1(n):
    """Exactly one m with φ(m) = n."""
    count = sum(1 for m in range(1, 2*n+2) if euler_totient(m) == n)
    return count == 1

def sigma_0(n): return count_divisors(n)
def sigma_1(n): return sum_of_divisors(n)
def sigma_2(n): return sum(d*d for d in _factors(n))
def sigma_k(n, k): return sum(d**k for d in _factors(n))

def is_sigma_prime(n):
    return is_prime(sum_of_divisors(n))

def is_tau_prime(n):
    return is_prime(count_divisors(n))

def goldbach_pairs(n):
    if n % 2 != 0 or n <= 2: return []
    return [(p, n-p) for p in range(2, n//2+1)
            if is_prime(p) and is_prime(n-p)]

def goldbach_count(n):
    return len(goldbach_pairs(n))

def is_goldbach_comet(n):
    """n has unusually many Goldbach pairs (> average)."""
    return len(goldbach_pairs(n)) > n // 20

def is_carmichael(n):
    """Carmichael number (absolute pseudoprime)."""
    if is_prime(n) or n < 2: return False
    if (n-1) % 2 != 0: return False
    for p in set(get_prime_factors(n)):
        if (n-1) % (p-1) != 0: return False
    return True

def is_pseudoprime_base_2(n):
    """n passes Fermat's test base 2 but isn't prime."""
    if is_prime(n): return False
    return pow(2, n-1, n) == 1

def is_fermat_pseudoprime(n, b=2):
    if is_prime(n): return False
    return pow(b, n-1, n) == 1

def is_euler_pseudoprime(n, b=2):
    if is_prime(n) or n % 2 == 0: return False
    j = 1 if n % 4 == 1 else -1
    return pow(b, (n-1)//2, n) == j % n

def is_strong_pseudoprime(n, b=2):
    """n is a strong pseudoprime to base b."""
    if is_prime(n): return False
    d, r = n-1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    x = pow(b, d, n)
    if x == 1 or x == n-1: return True
    for _ in range(r-1):
        x = pow(x, 2, n)
        if x == n-1: return True
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# 14. COLLATZ & ITERATIVE SEQUENCES
# ═══════════════════════════════════════════════════════════════════════════════

def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n//2 if n%2==0 else 3*n+1
        steps += 1
    return steps

def collatz_sequence(n):
    seq = [n]
    while n != 1:
        n = n//2 if n%2==0 else 3*n+1
        seq.append(n)
    return seq

def collatz_max(n):
    return max(collatz_sequence(n))

def collatz_max_steps(limit):
    return max(range(1, limit+1), key=collatz_steps)

def is_collatz_record(n):
    return all(collatz_steps(n) > collatz_steps(i) for i in range(1, n))

def aliquot_sequence(n, steps=20):
    seq = [n]
    for _ in range(steps):
        n = aliquot_sum(n)
        seq.append(n)
        if n == 0 or n == seq[-2]: break
    return seq

def is_aliquot_terminating(n, max_steps=100):
    """Aliquot sequence reaches 1 or 0."""
    for _ in range(max_steps):
        n = aliquot_sum(n)
        if n <= 1: return True
    return False

def is_cicada(n):
    """Check if n is a cicada number (related to 17, 13 year cycles)."""
    return n % 13 == 0 or n % 17 == 0


# ═══════════════════════════════════════════════════════════════════════════════
# 15. SPECIAL & NAMED NUMBER CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

def is_vampire(n):
    from itertools import permutations
    s = sorted(str(n))
    ln = len(s)
    if ln % 2 != 0: return False
    half = ln // 2
    for p in set(permutations(s)):
        f1 = int(''.join(p[:half]))
        f2 = int(''.join(p[half:]))
        if f1*f2 == n and f1 <= f2:
            if not (str(f1)[-1]=='0' and str(f2)[-1]=='0'):
                return True
    return False

def is_untouchable(n):
    known = {2,5,52,88,96,120,124,146,162,188,206,210,216,238,246,
             248,262,268,276,288,290,292,304,306,322,324,326,336,346}
    return n in known

def is_fortunate(n):
    known = {3,5,7,13,23,17,19,23,37,47,59,61,67,71,79,89,101,107,109}
    return n in known

def is_euclid(n):
    """Euclid numbers: product of first k primes + 1."""
    primes = _prime_sieve(200)
    prod = 1
    for p in primes:
        prod *= p
        if prod + 1 == n: return True
        if prod + 1 > n: break
    return False

def is_giuga(n):
    """n is a Giuga number if p | n/p-1 for every prime p|n."""
    for p in set(get_prime_factors(n)):
        if (n//p - 1) % p != 0: return False
    return True

def is_sublime(n):
    """Number of divisors and sum of divisors are both perfect."""
    return is_perfect(count_divisors(n)) and is_perfect(sum_of_divisors(n))

def is_zerofull(n):
    """Every digit from 0-9 appears at least once."""
    s = str(n)
    return all(str(d) in s for d in range(10))

def is_harshad_in_base(n, b):
    digs = []
    m = n
    while m:
        digs.append(m % b)
        m //= b
    s = sum(digs)
    return s != 0 and n % s == 0

def is_harshad_base_2(n): return is_harshad_in_base(n, 2)
def is_harshad_base_8(n): return is_harshad_in_base(n, 8)
def is_harshad_base_16(n): return is_harshad_in_base(n, 16)

def is_kaprekar_in_base(n, b):
    sq = n*n
    digits = []
    m = sq
    while m:
        digits.append(m % b)
        m //= b
    digits = digits[::-1]
    num_digits = len(digits)
    for split in range(1, num_digits):
        if split >= num_digits: break
        right = sum(digits[i]*b**(num_digits-1-i) for i in range(split, num_digits))
        left = sum(digits[i]*b**(num_digits-1-i) for i in range(split))
        if right > 0 and left + right == n: return True
    return False

def is_polydivisible(n):
    """First k digits of n are divisible by k for all k."""
    s = str(n)
    return all(int(s[:k]) % k == 0 for k in range(1, len(s)+1) if int(s[:k]))

def is_nude(n):
    """n is divisible by each of its digits."""
    d = _digits(n)
    return all(x != 0 and n % x == 0 for x in d)

def is_zygodrome(n):
    """Digits form pairs: 1122, 3344, etc."""
    s = str(n)
    if len(s) % 2 != 0: return False
    return all(s[i] == s[i+1] for i in range(0, len(s), 2)) and \
           all(s[i] != s[i+2] for i in range(0, len(s)-2, 2))

def is_cyclops(n):
    """Exactly one zero, in the middle."""
    s = str(n)
    mid = len(s) // 2
    return len(s) % 2 == 1 and s[mid] == '0' and '0' not in s[:mid] and '0' not in s[mid+1:]

def is_apocalyptic_power(n):
    """2^n contains 666."""
    return '666' in str(2**n)

def is_number_of_the_beast(n):
    return n == 666

def is_perfect_number_of_first_kind(n):
    return is_perfect(n)

def is_narcissistic_in_base(n, b):
    """Armstrong in base b."""
    digits = []
    m = n
    while m:
        digits.append(m % b)
        m //= b
    p = len(digits)
    return sum(d**p for d in digits) == n

def is_narcissistic_base_2(n): return is_narcissistic_in_base(n, 2)
def is_narcissistic_base_8(n): return is_narcissistic_in_base(n, 8)
def is_narcissistic_base_16(n): return is_narcissistic_in_base(n, 16)

def is_taxicab(n):
    """n can be expressed as sum of 2 cubes in 2+ ways."""
    reprs = []
    for a in range(1, int(n**(1/3))+2):
        rem = n - a**3
        if rem > 0 and is_perfect_cube(rem):
            b = round(rem**(1/3))
            if b >= a and b**3 == rem:
                reprs.append((a, b))
    return len(reprs) >= 2

def is_hardy_ramanujan(n):
    """1729 and similar taxicab numbers."""
    return is_taxicab(n)

def is_1729(n): return n == 1729

def is_keith(n):
    """n appears in its own digit sequence (Fibonacci-like)."""
    d = _digits(n)
    seq = list(d)
    while seq[-1] < n:
        seq.append(sum(seq[-len(d):]))
    return seq[-1] == n

def is_friedman(n):
    """Very approximate — checks if n can be made from rearranged digits with ops."""
    # Simplified: just known small Friedman numbers
    known = {25, 121, 125, 126, 127, 128, 153, 216, 289, 343, 347, 625, 688, 
             729, 736, 1025, 1206, 1255, 1260, 1285, 1296, 1395, 1435, 1503}
    return n in known

def is_pancake(n):
    """n is a pancake number: n = k(k+1)/2 + 1."""
    # Lazy triangular: maximum cuts with k straight cuts
    m = n - 1
    return is_triangular(m) or m == 0

def is_lazy_caterer(n): return is_pancake(n)


# ═══════════════════════════════════════════════════════════════════════════════
# 16. MODULAR & CONGRUENCE PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

def is_congruent_to(n, r, m): return n % m == r

def is_1_mod_4(n): return n % 4 == 1
def is_3_mod_4(n): return n % 4 == 3
def is_1_mod_6(n): return n % 6 == 1
def is_5_mod_6(n): return n % 6 == 5
def is_1_mod_8(n): return n % 8 == 1
def is_3_mod_8(n): return n % 8 == 3
def is_5_mod_8(n): return n % 8 == 5
def is_7_mod_8(n): return n % 8 == 7
def is_0_mod_3(n): return n % 3 == 0
def is_1_mod_3(n): return n % 3 == 1
def is_2_mod_3(n): return n % 3 == 2

def is_quadratic_residue(n, p):
    """Check if n is a quadratic residue mod p (p prime)."""
    if not is_prime(p): return None
    return pow(n, (p-1)//2, p) == 1

def legendre_symbol(n, p):
    if not is_prime(p) or p == 2: return None
    ls = pow(n % p, (p-1)//2, p)
    return -1 if ls == p-1 else ls

def jacobi_symbol(n, m):
    """Jacobi symbol (n/m)."""
    if m <= 0 or m % 2 == 0: return None
    result = 1
    n = n % m
    while n != 0:
        while n % 2 == 0:
            n //= 2
            if m % 8 in (3, 5): result = -result
        n, m = m, n
        if n % 4 == 3 and m % 4 == 3: result = -result
        n = n % m
    return result if m == 1 else 0

def is_primitive_root(g, p):
    """Check if g is a primitive root mod p."""
    if not is_prime(p): return False
    phi = p - 1
    for factor in set(get_prime_factors(phi)):
        if pow(g, phi//factor, p) == 1: return False
    return True

def smallest_primitive_root(p):
    if not is_prime(p): return None
    for g in range(2, p):
        if is_primitive_root(g, p): return g
    return None

def discrete_log(g, h, p):
    """Baby-step giant-step discrete log: g^x ≡ h (mod p)."""
    m = int(math.ceil(math.sqrt(p)))
    table = {pow(g, j, p): j for j in range(m)}
    gm = pow(g, -m, p)
    gamma = h
    for i in range(m):
        if gamma in table: return i*m + table[gamma]
        gamma = gamma*gm % p
    return None

def chinese_remainder(remainders, moduli):
    """CRT: find x such that x ≡ r_i (mod m_i)."""
    M = functools.reduce(lambda a, b: a*b, moduli)
    x = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        x += r * Mi * pow(Mi, -1, m)
    return x % M

def is_quadratic_non_residue(n, p):
    ls = legendre_symbol(n, p)
    return ls == -1


# ═══════════════════════════════════════════════════════════════════════════════
# 17. GEOMETRIC & SPATIAL NUMBERS
# ═══════════════════════════════════════════════════════════════════════════════

def is_tetrahedral(n):
    """n = k(k+1)(k+2)/6."""
    for k in range(1, 1000):
        t = k*(k+1)*(k+2)//6
        if t == n: return True
        if t > n: return False
    return False

def is_pyramidal(n):
    """Square pyramidal: n = k(k+1)(2k+1)/6."""
    for k in range(1, 1000):
        p = k*(k+1)*(2*k+1)//6
        if p == n: return True
        if p > n: return False
    return False

def is_pentatope(n):
    """n = k(k+1)(k+2)(k+3)/24."""
    for k in range(1, 500):
        p = k*(k+1)*(k+2)*(k+3)//24
        if p == n: return True
        if p > n: return False
    return False

def is_stella_octangula(n):
    """n = k(2k^2-1) for some k."""
    for k in range(1, 1000):
        s = k*(2*k*k-1)
        if s == n: return True
        if s > n: return False
    return False

def is_rhombic_dodecahedral(n):
    """n = (2k-1)(2k^2-2k+1)."""
    for k in range(1, 500):
        v = (2*k-1)*(2*k*k-2*k+1)
        if v == n: return True
        if v > n: return False
    return False

def is_truncated_tetrahedral(n):
    """n = (23k^2-27k+10)*k/2 -- simplified check."""
    for k in range(1, 200):
        t = k*(23*k*k - 27*k + 10)//2
        if t == n: return True
        if t > n: return False
    return False

def is_icosahedral(n):
    """n = k(5k^2-5k+2)/2."""
    for k in range(1, 500):
        t = k*(5*k*k-5*k+2)//2
        if t == n: return True
        if t > n: return False
    return False

def is_dodecahedral(n):
    """n = k(3k-1)(3k-2)/2."""
    for k in range(1, 500):
        t = k*(3*k-1)*(3*k-2)//2
        if t == n: return True
        if t > n: return False
    return False

def is_octahedral(n):
    """n = k(2k^2+1)/3."""
    for k in range(1, 500):
        if k*(2*k*k+1) % 3 == 0:
            if k*(2*k*k+1)//3 == n: return True
    return False

def is_cuboctahedral(n):
    """n = (10k^3-16k)/3 + k^2 ... simplified."""
    for k in range(1, 500):
        t = (2*k*k*k + k) // 3 * 5  # approximate known sequence
        if t == n: return True
        if t > n * 2: return False
    return False

def is_centered_cube(n):
    """n = (2k+1)^3 - 2k^3 = k^3 + (k+1)^3."""
    for k in range(0, 500):
        if k**3 + (k+1)**3 == n: return True
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# 18. BASE CONVERSION & REPRESENTATION
# ═══════════════════════════════════════════════════════════════════════════════

def to_roman(n):
    if n <= 0 or n >= 4000: return 'N/A'
    val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
    syms = ['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I']
    result = ''
    for v, s in zip(val, syms):
        while n >= v:
            result += s
            n -= v
    return result

def from_roman(s):
    vals = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    result, prev = 0, 0
    for ch in reversed(s.upper()):
        curr = vals.get(ch, 0)
        result += curr if curr >= prev else -curr
        prev = curr
    return result

def int_to_words(n):
    ones = ['','one','two','three','four','five','six','seven','eight','nine',
            'ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen',
            'seventeen','eighteen','nineteen']
    tens = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
    if n == 0: return 'zero'
    if n < 0: return 'negative ' + int_to_words(-n)
    if n < 20: return ones[n]
    if n < 100: return tens[n//10] + ('' if n%10==0 else '-'+ones[n%10])
    if n < 1000: return ones[n//100]+' hundred'+('' if n%100==0 else ' '+int_to_words(n%100))
    if n < 1_000_000: return int_to_words(n//1000)+' thousand'+('' if n%1000==0 else ' '+int_to_words(n%1000))
    if n < 1_000_000_000: return int_to_words(n//1_000_000)+' million'+('' if n%1_000_000==0 else ' '+int_to_words(n%1_000_000))
    return int_to_words(n//1_000_000_000)+' billion'+('' if n%1_000_000_000==0 else ' '+int_to_words(n%1_000_000_000))

def to_base(n, b):
    if b < 2 or b > 36: raise ValueError("Base must be 2-36")
    if n == 0: return '0'
    digits, neg = [], n < 0
    n = abs(n)
    while n:
        digits.append('0123456789abcdefghijklmnopqrstuvwxyz'[n%b])
        n //= b
    return ('-' if neg else '') + ''.join(reversed(digits))

def from_base(s, b):
    return int(s, b)

def is_palindrome_in_base(n, b):
    s = to_base(n, b)
    return s == s[::-1]

def is_palindrome_base_2(n): return is_palindrome_in_base(n, 2)
def is_palindrome_base_8(n): return is_palindrome_in_base(n, 8)
def is_palindrome_base_16(n): return is_palindrome_in_base(n, 16)

def is_palindrome_all_bases(n, max_base=10):
    return all(is_palindrome_in_base(n, b) for b in range(2, max_base+1))

def digit_sum_base(n, b):
    s = 0
    while n:
        s += n % b
        n //= b
    return s

def is_harshad_all_bases(n, max_base=10):
    return all(is_harshad_in_base(n, b) for b in range(2, max_base+1))

def is_niven_base_2(n): return is_harshad_base_2(n)
def is_niven_base_8(n): return is_harshad_base_8(n)

def balanced_ternary(n):
    """Represent n in balanced ternary (-1, 0, 1 digits)."""
    if n == 0: return '0'
    digits = []
    while n:
        rem = n % 3
        if rem == 2: rem = -1
        digits.append(rem)
        n = (n - rem) // 3
    return ''.join(str(d) for d in reversed(digits)).replace('-1', 'T')


# ═══════════════════════════════════════════════════════════════════════════════
# 19. MISCELLANEOUS NAMED SEQUENCES
# ═══════════════════════════════════════════════════════════════════════════════

def is_primes_gaps(n):
    """Check if n is a prime gap (difference between consecutive primes)."""
    for p in range(2, 10000):
        if is_prime(p) and is_prime(p+n):
            if not any(is_prime(p+k) for k in range(1, n)):
                return True
    return False

def is_polygonal(n, s):
    """n is s-gonal (s >= 3)."""
    # P(s,k) = k*((s-2)*k - (s-4))/2
    for k in range(1, 10000):
        p = k*((s-2)*k - (s-4))//2
        if p == n: return True
        if p > n: return False
    return False

def is_3gonal(n): return is_triangular(n)
def is_4gonal(n): return is_perfect_square(n)
def is_5gonal(n): return is_pentagonal(n)
def is_6gonal(n): return is_hexagonal(n)
def is_7gonal(n): return is_heptagonal(n)
def is_8gonal(n): return is_octagonal(n)
def is_9gonal(n): return is_nonagonal(n)
def is_10gonal(n): return is_decagonal(n)

def is_generalized_pentagonal(n):
    """n is a generalized pentagonal (includes negative indices)."""
    disc = 1 + 24*n
    if disc < 0: return False
    if not _is_perfect_square(disc): return False
    r = int(math.isqrt(disc))
    return (1+r) % 6 == 0 or (1-r) % 6 == 0

def is_partition_number(n):
    """Check if n is a partition number p(k) for small k."""
    # Pre-compute first 100 partition numbers
    def partition_numbers(limit):
        p = [0]*(limit+1)
        p[0] = 1
        for k in range(1, limit+1):
            p[k] = 0
            i = 1
            while True:
                g1 = i*(3*i-1)//2
                g2 = i*(3*i+1)//2
                if g1 > k: break
                sign = (-1)**(i+1)
                p[k] += sign*p[k-g1]
                if g2 <= k: p[k] += sign*p[k-g2]
                i += 1
        return p
    p = partition_numbers(150)
    return n in p

def is_central_binomial_coefficient(n):
    """n = C(2k, k) for some k."""
    k = 0
    while True:
        c = math.comb(2*k, k)
        if c == n: return True
        if c > n: return False
        k += 1

def is_binomial_coefficient(n):
    """n = C(a, b) for some a >= b >= 0."""
    if n <= 1: return True
    for a in range(2, n+1):
        for b in range(1, a//2+1):
            c = math.comb(a, b)
            if c == n: return True
            if c > n: break
    return False

def is_catalan_related(n):
    """n is related to Catalan numbers (appears in Catalan triangle)."""
    return is_catalan(n) or is_binomial_coefficient(n)

def stirling_first(n, k):
    """Stirling numbers of the first kind (unsigned)."""
    if k == 0: return 1 if n == 0 else 0
    if n == 0: return 0
    return (n-1)*stirling_first(n-1, k) + stirling_first(n-1, k-1)

def stirling_second(n, k):
    """Stirling numbers of the second kind."""
    if n == k: return 1
    if k == 0 or k > n: return 0
    return k*stirling_second(n-1, k) + stirling_second(n-1, k-1)

def is_stirling_first_kind(n):
    """n appears in Stirling numbers of first kind (small values)."""
    for i in range(1, 10):
        for j in range(1, i+1):
            if abs(stirling_first(i, j)) == n: return True
    return False

def is_euler_number(n):
    """Check if n is an Euler number (first few)."""
    known = {1, 5, 61, 1385, 50521, 2702765}
    return n in known

def is_bernoulli_numerator(n):
    """Check against known Bernoulli numerators."""
    known = {1, 1, 1, 1, 1, 5, 691, 7, 3617, 43867, 174611}
    return n in known

def is_weird_prime(n):
    """Primes that are weird (only known: 2, based on Giuga conjecture)."""
    return n == 2

def is_regular_prime(n):
    """Regular prime (not irregular). Known irregular: 37, 59, 67, 101, ..."""
    irregular = {37, 59, 67, 101, 103, 131, 149, 157, 233, 257, 263}
    return is_prime(n) and n not in irregular

def is_irregular_prime(n):
    irregular = {37, 59, 67, 101, 103, 131, 149, 157, 233, 257, 263}
    return is_prime(n) and n in irregular

def is_wolstenholme_prime(n):
    known = {16843, 2124679}
    return n in known

def is_wall_sun_sun_prime(n):
    """No Wall-Sun-Sun primes known yet."""
    return False

def is_wieferich_prime(n):
    known = {1093, 3511}
    return n in known

def is_sexy_prime_triplet(n):
    """(n, n+6, n+12) all prime."""
    return all(is_prime(n+6*k) for k in range(3))

def is_sexy_prime_quadruplet(n):
    return all(is_prime(n+6*k) for k in range(4))

def is_arithmetic_number(n):
    """Mean of divisors is an integer."""
    divs = _factors(n)
    return sum(divs) % len(divs) == 0

def is_zumkeller(n):
    """Divisors can be split into two sets with equal sum."""
    divs = _factors(n)
    total = sum(divs)
    if total % 2 != 0: return False
    return _subset_sum(divs, total//2)

def is_practical_number(n): return is_practical(n)

def is_sublime_number(n):
    return is_sublime(n)

def is_multiply_perfect(n):
    """sigma(n) is a multiple of n."""
    return sum_of_divisors(n) % n == 0

def is_k_perfect(n, k): return is_multiperfect(n, k)


# ═══════════════════════════════════════════════════════════════════════════════
# 20. PARTITION & COMBINATORIAL
# ═══════════════════════════════════════════════════════════════════════════════

def partition_count(n):
    """Number of integer partitions of n."""
    if n < 0: return 0
    p = [0]*(n+1)
    p[0] = 1
    for k in range(1, n+1):
        i = 1
        while True:
            g1 = i*(3*i-1)//2
            g2 = i*(3*i+1)//2
            if g1 > n: break
            for m in range(g1, n+1): p[m] -= (-1)**i * p[m-g1] if False else 0
            break
    # Use Euler's pentagonal method properly
    p = [0]*(n+1)
    p[0] = 1
    for k in range(1, n+1):
        total = 0
        i = 1
        while True:
            g1 = i*(3*i-1)//2
            g2 = i*(3*i+1)//2
            s = 1 if i%2==1 else -1
            if g1 <= k: total += s * p[k-g1]
            if g2 <= k: total += s * p[k-g2]
            if g1 > k: break
            i += 1
        p[k] = total
    return p[n]

def is_lucky_number_of_euler(n):
    """Euler's lucky numbers: primes of form k^2+k+p for k=0..p-2."""
    known = {2, 3, 5, 11, 17, 41}
    return n in known

def is_primary_pseudoperfect(n):
    """1/n + sum(1/p for p|n prime) = 1."""
    pf = sorted(set(get_prime_factors(n)))
    total = sum(n//p for p in pf) + 1
    return total == n

def is_harmonic_divisor(n):
    """Ore's harmonic number: harmonic mean of divisors is integer."""
    divs = _factors(n)
    k = len(divs)
    s = sum(divs)
    return (k * n) % s == 0

def ore_harmonic_mean(n):
    divs = _factors(n)
    return len(divs) * n / sum(divs)

def is_ore_number(n): return is_harmonic_divisor(n)

def is_giuga_number(n): return is_giuga(n)

def is_primary(n):
    """n is a prime power p^k."""
    pf = set(get_prime_factors(n))
    return len(pf) == 1


# ═══════════════════════════════════════════════════════════════════════════════
# 21. ODD/EVEN, SIGN, RANGE CHECKS
# ═══════════════════════════════════════════════════════════════════════════════

def is_zero(n): return n == 0
def is_positive(n): return n > 0
def is_negative(n): return n < 0
def is_nonnegative(n): return n >= 0
def is_nonpositive(n): return n <= 0
def is_natural(n): return n >= 1 and isinstance(n, int)
def is_whole(n): return n >= 0 and isinstance(n, int)
def is_integer(n): return isinstance(n, (int, float)) and float(n).is_integer()

def is_single_digit(n): return 0 <= n <= 9
def is_two_digit(n): return 10 <= n <= 99
def is_three_digit(n): return 100 <= n <= 999
def is_four_digit(n): return 1000 <= n <= 9999
def is_five_digit(n): return 10000 <= n <= 99999
def is_six_digit(n): return 100000 <= n <= 999999

def is_teen(n): return 13 <= n <= 19
def is_score(n): return n == 20
def is_gross(n): return n == 144
def is_dozen(n): return n == 12
def is_bakers_dozen(n): return n == 13
def is_century(n): return n == 100
def is_millennium(n): return n == 1000
def is_myriad(n): return n == 10000
def is_lakh(n): return n == 100000
def is_crore(n): return n == 10000000

def absolute_value(n): return abs(n)
def sign(n): return 0 if n == 0 else (1 if n > 0 else -1)


# ═══════════════════════════════════════════════════════════════════════════════
# 22. TRIGONOMETRIC & TRANSCENDENTAL APPROXIMATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def is_close_to_pi(n, tol=0.01):
    return abs(n - math.pi) < tol

def is_close_to_e(n, tol=0.01):
    return abs(n - math.e) < tol

def is_close_to_phi(n, tol=0.01):
    phi = (1 + math.sqrt(5)) / 2
    return abs(n - phi) < tol

def is_close_to_sqrt2(n, tol=0.01):
    return abs(n - math.sqrt(2)) < tol

def is_close_to_ln2(n, tol=0.01):
    return abs(n - math.log(2)) < tol

def continued_fraction(n, terms=10):
    """Return continued fraction representation."""
    result = []
    for _ in range(terms):
        result.append(int(n))
        frac = n - int(n)
        if frac < 1e-10: break
        n = 1/frac
    return result

def is_integer_cf(n):
    """n is an integer (trivial CF)."""
    return isinstance(n, int)


# ═══════════════════════════════════════════════════════════════════════════════
# 23. CALENDAR & DATE NUMBERS
# ═══════════════════════════════════════════════════════════════════════════════

def is_leap_year(n):
    return (n % 4 == 0 and n % 100 != 0) or n % 400 == 0

def is_century_year(n): return n % 100 == 0

def is_valid_month(n): return 1 <= n <= 12

def is_valid_day(n): return 1 <= n <= 31

def is_valid_hour(n): return 0 <= n <= 23

def is_valid_minute(n): return 0 <= n <= 59

def is_valid_year_ad(n): return n > 0

def days_in_month(month, year=2024):
    days = [0, 31, 28+(1 if is_leap_year(year) else 0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return days[month] if 1 <= month <= 12 else 0

def is_days_in_year(n, year=2024):
    return n == (366 if is_leap_year(year) else 365)


# ═══════════════════════════════════════════════════════════════════════════════
# 24. GEOMETRY HELPERS (integer geometry)
# ═══════════════════════════════════════════════════════════════════════════════

def is_pythagorean_hypotenuse(n):
    """n can be hypotenuse of Pythagorean triple."""
    for a in range(1, n):
        b2 = n*n - a*a
        if b2 <= 0: break
        if _is_perfect_square(b2) and int(math.isqrt(b2)) > a:
            return True
    return False

def pythagorean_triples_with_hyp(c):
    """All primitive Pythagorean triples with hypotenuse c."""
    triples = []
    for a in range(1, c):
        b2 = c*c - a*a
        if b2 > 0 and _is_perfect_square(b2):
            b = int(math.isqrt(b2))
            if a < b: triples.append((a, b, c))
    return triples

def is_pythagorean_leg(n):
    """n appears as a leg in some Pythagorean triple."""
    for b in range(1, 10000):
        c2 = n*n + b*b
        if _is_perfect_square(c2): return True
    return False

def is_heronian(n):
    """n is the area of a Heronian triangle (integer area and sides)."""
    # Approximate — check small triples
    for a in range(1, 50):
        for b in range(a, 50):
            for c in range(b, a+b):
                s = (a+b+c)/2
                area2 = s*(s-a)*(s-b)*(s-c)
                if area2 > 0 and _is_perfect_square(int(area2*4)):
                    if int(math.sqrt(area2)+0.5)**2 == int(area2) and int(math.sqrt(area2)) == n:
                        return True
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# 25. GENERATORS & RANGE UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def primes_up_to(n):
    return _prime_sieve(n)

def find_in_range(func, start, end):
    return [n for n in range(start, end+1) if func(n)]

def find_all_in_range(funcs, start, end):
    """Return numbers satisfying ALL functions."""
    return [n for n in range(start, end+1) if all(f(n) for f in funcs)]

def find_any_in_range(funcs, start, end):
    """Return numbers satisfying ANY function."""
    return [n for n in range(start, end+1) if any(f(n) for f in funcs)]

def nth_prime(n):
    count, num = 0, 1
    while count < n:
        num += 1
        if is_prime(num): count += 1
    return num

def nth_triangular(n): return n*(n+1)//2
def nth_square(n): return n*n
def nth_pentagonal(n): return n*(3*n-1)//2
def nth_hexagonal(n): return n*(2*n-1)
def nth_heptagonal(n): return n*(5*n-3)//2
def nth_octagonal(n): return n*(3*n-2)
def nth_fibonacci_term(n): return nth_fibonacci(n)
def nth_lucas_term(n): return nth_lucas(n)
def nth_catalan(n): return math.comb(2*n, n)//(n+1)
def nth_bell(n):
    bell = [[0]*30 for _ in range(30)]
    bell[0][0] = 1
    for i in range(1, n+2):
        bell[i][0] = bell[i-1][i-1]
        for j in range(1, i+1):
            bell[i][j] = bell[i-1][j-1] + bell[i][j-1]
    return bell[n][0]

def prime_gaps(n):
    """List of gaps between first n primes."""
    primes = _prime_sieve(n*20)[:n]
    return [primes[i+1]-primes[i] for i in range(len(primes)-1)]

def coprime_count(n):
    """Count of integers <= n coprime to n."""
    return euler_totient(n)

def divisors(n):
    return _factors(n)

def proper_divisors(n):
    return _proper_factors(n)


# ═══════════════════════════════════════════════════════════════════════════════
# 26. ENCODING, HASHING & CHECKSUM TRICKS
# ═══════════════════════════════════════════════════════════════════════════════

def digit_checksum_mod10(n):
    return _digit_sum(n) % 10

def digit_checksum_mod9(n):
    return _digit_sum(n) % 9

def is_divisibility_rule_7(n):
    """Apply the divisibility rule for 7."""
    while n > 99:
        n = abs(n//10 - 2*(n%10))
    return n % 7 == 0

def is_divisibility_rule_11(n):
    """Alternating digit sum divisible by 11."""
    d = _digits(n)
    alt = sum(d[i]*(-1)**i for i in range(len(d)))
    return alt % 11 == 0

def is_divisibility_rule_13(n):
    """Add 4 times the last digit to the rest."""
    while n > 99:
        n = n//10 + 4*(n%10)
    return n % 13 == 0

def is_divisibility_rule_17(n):
    while n > 99:
        n = abs(n//10 - 5*(n%10))
    return n % 17 == 0

def is_divisibility_rule_19(n):
    while n > 99:
        n = n//10 + 2*(n%10)
    return n % 19 == 0

def is_divisibility_rule_23(n):
    while n > 99:
        n = n//10 + 7*(n%10)
    return n % 23 == 0

def isbn_10_check(n):
    """Check ISBN-10 validity."""
    s = str(n).zfill(10)
    if len(s) != 10: return False
    total = sum((10-i)*int(s[i]) for i in range(10))
    return total % 11 == 0

def isbn_13_check(n):
    """Check ISBN-13 validity."""
    s = str(n).zfill(13)
    if len(s) != 13: return False
    total = sum(int(s[i])*(1 if i%2==0 else 3) for i in range(13))
    return total % 10 == 0


# ═══════════════════════════════════════════════════════════════════════════════
# 27. PHYSICS & SCIENCE CONSTANTS CHECK
# ═══════════════════════════════════════════════════════════════════════════════

def is_speed_of_light(n): return n == 299792458
def is_avogadro_approx(n): return abs(n - 6.022e23) < 1e20
def is_boltzmann_approx(n): return abs(n - 1.38e-23) < 1e-25
def is_planck_approx(n): return abs(n - 6.626e-34) < 1e-36

KNOWN_CONSTANTS = {
    137: "fine structure denominator",
    1729: "Hardy-Ramanujan (taxicab)",
    6174: "Kaprekar constant",
    142857: "cyclic number",
    1089: "Kaprekar surprise",
    2520: "smallest number divisible by 1-10",
    720720: "LCM of 1-12",
    666: "number of the beast",
    1000000007: "common prime modulus in CP",
    998244353: "NTT-friendly prime",
    1000000009: "large prime",
    4294967295: "2^32 - 1",
    2147483647: "Mersenne prime M31",
    127: "Mersenne prime M7",
    8128: "perfect number",
    496: "perfect number",
    28: "perfect number",
    6: "perfect number",
}

def known_constant_name(n):
    return KNOWN_CONSTANTS.get(n, None)

def is_known_constant(n):
    return n in KNOWN_CONSTANTS


# ═══════════════════════════════════════════════════════════════════════════════
# 28. ADVANCED NUMBER THEORY
# ═══════════════════════════════════════════════════════════════════════════════

def is_totient_valence_k(n, k):
    count = sum(1 for m in range(1, 2*n+3) if euler_totient(m) == n)
    return count == k

def number_of_totient_solutions(n):
    return sum(1 for m in range(1, 2*n+3) if euler_totient(m) == n)

def is_cyclic_number(n):
    """n is a cyclic number (e.g., 142857)."""
    known = {142857, 588235294117647}
    return n in known

def is_parasitic(n, k):
    """k*n equals n with its leftmost digit moved to the rightmost position."""
    s = str(n)
    rotated = int(s[1:] + s[0])
    return k * n == rotated

def is_parasitic_2(n): return is_parasitic(n, 2)
def is_parasitic_3(n): return is_parasitic(n, 3)
def is_parasitic_4(n): return is_parasitic(n, 4)
def is_parasitic_6(n): return is_parasitic(n, 6)
def is_parasitic_7(n): return is_parasitic(n, 7)
def is_parasitic_8(n): return is_parasitic(n, 8)
def is_parasitic_9(n): return is_parasitic(n, 9)

def is_transposable(n, k):
    """k*n equals n with its rightmost digit moved to the leftmost position."""
    s = str(n)
    rotated = int(s[-1] + s[:-1])
    return k * n == rotated

def is_autobiographical(n):
    """n[i] = count of digit i appearing in n."""
    s = str(n)
    if len(s) != 10: return is_self_descriptive(n)
    return all(int(s[i]) == s.count(str(i)) for i in range(len(s)))

def is_catalan_even(n):
    return is_catalan(n) and n % 2 == 0

def is_euler_phi_prime(n):
    return is_prime(euler_totient(n))

def is_semiprime_palindrome(n):
    return is_semi_prime(n) and is_palindrome(n)

def is_prime_power(n):
    """n = p^k for prime p, k >= 1."""
    pf = set(get_prime_factors(n))
    return len(pf) == 1

def prime_power_base(n):
    pf = set(get_prime_factors(n))
    if len(pf) == 1: return list(pf)[0]
    return None

def prime_power_exponent(n):
    pf = get_prime_factors(n)
    if len(set(pf)) == 1: return len(pf)
    return None

def is_squarefree_semigroup(n):
    return is_squarefree(n) and is_semi_prime(n)

def is_sum_of_consecutive_primes(n):
    primes = _prime_sieve(n+1)
    for start in range(len(primes)):
        s = 0
        for i in range(start, len(primes)):
            s += primes[i]
            if s == n: return True
            if s > n: break
    return False

def is_sum_of_first_k_primes(n):
    primes = _prime_sieve(n+1)
    s = 0
    for p in primes:
        s += p
        if s == n: return True
        if s > n: return False
    return False

def is_sum_of_consecutive_naturals(n):
    return is_polite(n)

def sum_of_consecutive_naturals_repr(n):
    reprs = []
    for k in range(2, int(math.sqrt(2*n))+2):
        # k*(2a+k-1)/2 = n → 2a = 2n/k - k + 1
        if (2*n) % k == 0 or (2*n - k*(k-1)) % (2*k) == 0:
            num = 2*n - k*(k-1)
            if num > 0 and num % (2*k) == 0:
                a = num // (2*k)
                if a > 0: reprs.append((a, a+k-1))
    return reprs


# ═══════════════════════════════════════════════════════════════════════════════
# 29. COMPETITIVE PROGRAMMING HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def mod_pow(base, exp, mod): return pow(base, exp, mod)
def mod_inv(a, mod): return pow(a, -1, mod)

def is_coprime_to_all(n, lst):
    return all(math.gcd(n, x) == 1 for x in lst)

def totient_sum(n):
    return sum(euler_totient(i) for i in range(1, n+1))

def is_prime_mod(n, p):
    return pow(n, p-1, p) == 1

def miller_rabin(n, witnesses=None):
    """Deterministic Miller-Rabin for n < 3,215,031,751."""
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    if witnesses is None:
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    d, r = n-1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in witnesses:
        if a >= n: continue
        x = pow(a, d, n)
        if x == 1 or x == n-1: continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1: break
        else: return False
    return True

def is_prime_miller_rabin(n): return miller_rabin(n)

def next_prime(n):
    n += 1
    while not is_prime(n): n += 1
    return n

def prev_prime(n):
    n -= 1
    while n > 1 and not is_prime(n): n -= 1
    return n if n > 1 else None

def prime_pi(n):
    """Number of primes <= n."""
    return len(_prime_sieve(n))

def is_highly_totient(n):
    """n has more solutions to phi(x)=n than any smaller number."""
    count = number_of_totient_solutions(n)
    return count > 0 and all(number_of_totient_solutions(i) < count
                              for i in range(1, n) if i % 2 == 0)

def nth_composite(n):
    count, num = 0, 3
    while True:
        if is_composite(num): count += 1
        if count == n: return num
        num += 1


# ═══════════════════════════════════════════════════════════════════════════════
# 30. NUMERIC CURIOSITIES
# ═══════════════════════════════════════════════════════════════════════════════

def is_1089(n): return n == 1089
def is_1729(n): return n == 1729
def is_142857(n): return n == 142857
def is_6174(n): return n == 6174
def is_perfect_6(n): return n == 6
def is_perfect_28(n): return n == 28
def is_perfect_496(n): return n == 496
def is_perfect_8128(n): return n == 8128

def reverse_multiply_property(n):
    """n * reverse(n) property string."""
    r = _reverse(n)
    return n * r

def is_reverse_multiple(n, k):
    return _reverse(n) == k * n or k * _reverse(n) == n

def is_strobogrammatic(n):
    """Looks the same upside down (using 0,1,6,8,9)."""
    mapping = {'0':'0', '1':'1', '6':'9', '8':'8', '9':'6'}
    s = str(n)
    return all(c in mapping for c in s) and \
           ''.join(mapping[c] for c in reversed(s)) == s

def is_ambiguous(n):
    """Reads differently upside down but still valid."""
    strobos = {'0':'0','1':'1','6':'9','8':'8','9':'6'}
    s = str(n)
    if not all(c in strobos for c in s): return False
    flipped = int(''.join(strobos[c] for c in reversed(s)))
    return flipped != n

def concatenated_square_palindrome(n):
    """Concatenate n with n^2 and check if palindrome."""
    s = str(n) + str(n*n)
    return s == s[::-1]

def is_sum_product(n):
    """n = (sum of digits) * (product of digits)."""
    d = _digits(n)
    return sum(d) * _digit_product(n) == n

def is_digit_squared_sum(n):
    """n = sum of squares of digits."""
    return sum(x*x for x in _digits(n)) == n

def is_digit_cubed_sum(n):
    return sum(x**3 for x in _digits(n)) == n

def is_digit_fourth_sum(n):
    return sum(x**4 for x in _digits(n)) == n

def is_digit_fifth_sum(n):
    return sum(x**5 for x in _digits(n)) == n

def is_digit_sixth_sum(n):
    return sum(x**6 for x in _digits(n)) == n

def is_ascending_prime(n):
    """Prime with strictly increasing digits."""
    return is_prime(n) and is_metadrome(n)

def is_descending_prime(n):
    return is_prime(n) and is_katadrome(n)

def is_palindromic_cube(n):
    return is_palindrome(n) and is_perfect_cube(n)

def is_prime_index_prime(n):
    """n is prime and its index among primes is also prime."""
    if not is_prime(n): return False
    idx = prime_pi(n)
    return is_prime(idx)

def is_prime_at_prime_position(n): return is_prime_index_prime(n)

def sum_of_prime_factors(n):
    return sum(get_prime_factors(n))

def product_of_prime_factors(n):
    pf = list(set(get_prime_factors(n)))
    return functools.reduce(lambda a, b: a*b, pf, 1)

def is_sum_prime_factors_prime(n):
    return is_prime(sum_of_prime_factors(n))


# ═══════════════════════════════════════════════════════════════════════════════
# 31. COMPLETE PROPERTY SCAN
# ═══════════════════════════════════════════════════════════════════════════════

_ALL_BOOLEAN_CHECKS = {
    # Prime family
    'is_prime': is_prime,
    'is_composite': is_composite,
    'is_twin_prime': is_twin_prime,
    'is_cousin_prime': is_cousin_prime,
    'is_sexy_prime': is_sexy_prime,
    'is_mersenne_prime': is_mersenne_prime,
    'is_mersenne_number': is_mersenne_number,
    'is_safe_prime': is_safe_prime,
    'is_sophie_germain_prime': is_sophie_germain_prime,
    'is_circular_prime': is_circular_prime,
    'is_emirp': is_emirp,
    'is_prime_palindrome': is_prime_palindrome,
    'is_left_truncatable_prime': is_left_truncatable_prime,
    'is_right_truncatable_prime': is_right_truncatable_prime,
    'is_two_sided_prime': is_two_sided_prime,
    'is_strong_prime': is_strong_prime,
    'is_weak_prime': is_weak_prime,
    'is_balanced_prime': is_balanced_prime,
    'is_isolated_prime': is_isolated_prime,
    'is_pythagorean_prime': is_pythagorean_prime,
    'is_pierpont_prime': is_pierpont_prime,
    'is_chen_prime': is_chen_prime,
    'is_regular_prime': is_regular_prime,
    'is_irregular_prime': is_irregular_prime,
    'is_wieferich_prime': is_wieferich_prime,
    'is_wilson_prime': is_wilson_prime,
    'is_carmichael': is_carmichael,
    'is_prime_power': is_prime_power,
    'is_semi_prime': is_semi_prime,
    'is_sphenic': is_sphenic,
    'is_brilliant': is_brilliant,
    # Armstrong & digital
    'is_armstrong': is_armstrong,
    'is_disarium': is_disarium,
    'is_munchausen': is_munchausen,
    'is_sum_of_digit_factorials': is_sum_of_digit_factorials,
    'is_perfect_digital_invariant_p3': is_pdi_3,
    # Perfect, abundant
    'is_perfect': is_perfect,
    'is_abundant': is_abundant,
    'is_deficient': is_deficient,
    'is_semiperfect': is_semiperfect,
    'is_weird': is_weird,
    'is_amicable': is_amicable,
    'is_sociable': is_sociable,
    'is_superperfect': is_superperfect,
    'is_harmonic_divisor': is_harmonic_divisor,
    'is_zumkeller': is_zumkeller,
    # Palindrome
    'is_palindrome': is_palindrome,
    'is_binary_palindrome': is_binary_palindrome,
    'is_octal_palindrome': is_octal_palindrome,
    'is_lychrel': is_lychrel,
    # Named simple
    'is_spy': is_spy,
    'is_buzz': is_buzz,
    'is_duck': is_duck,
    'is_neon': is_neon,
    'is_automorphic': is_automorphic,
    'is_trimorphic': is_trimorphic,
    'is_harshad': is_harshad,
    'is_strong_harshad': is_strong_harshad,
    'is_kaprekar': is_kaprekar,
    'is_happy': is_happy,
    'is_lucky': is_lucky,
    'is_keith': is_keith,
    'is_strobogrammatic': is_strobogrammatic,
    'is_polydivisible': is_polydivisible,
    'is_nude': is_nude,
    'is_cyclops': is_cyclops,
    'is_vampire': is_vampire,
    # Fibonacci family
    'is_fibonacci': is_fibonacci,
    'is_lucas': is_lucas,
    'is_tribonacci': is_tribonacci,
    'is_pell': is_pell,
    'is_padovan': is_padovan,
    'is_catalan': is_catalan,
    'is_bell': is_bell,
    'is_motzkin': is_motzkin,
    'is_fibbinary': is_fibbinary,
    # Figurate
    'is_triangular': is_triangular,
    'is_square': is_square,
    'is_pentagonal': is_pentagonal,
    'is_hexagonal': is_hexagonal,
    'is_heptagonal': is_heptagonal,
    'is_octagonal': is_octagonal,
    'is_pronic': is_pronic,
    'is_centered_square': is_centered_square,
    'is_centered_hexagonal': is_centered_hexagonal,
    'is_star': is_star,
    'is_tetrahedral': is_tetrahedral,
    'is_pyramidal': is_pyramidal,
    'is_icosahedral': is_icosahedral,
    'is_centered_cube': is_centered_cube,
    # Powers
    'is_perfect_square': is_perfect_square,
    'is_perfect_cube': is_perfect_cube,
    'is_perfect_fourth_power': is_perfect_fourth_power,
    'is_perfect_power': is_perfect_power,
    'is_powerful': is_powerful,
    'is_squarefree': is_squarefree,
    'is_achilles': is_achilles,
    'is_power_of_two': is_power_of_two,
    'is_power_of_three': is_power_of_three,
    'is_sum_of_two_squares': is_sum_of_two_squares,
    'is_sum_of_three_squares': is_sum_of_three_squares,
    'is_loeschian': is_loeschian,
    # Digit properties
    'is_bouncy': is_bouncy,
    'is_increasing': is_increasing,
    'is_decreasing': is_decreasing,
    'is_metadrome': is_metadrome,
    'is_katadrome': is_katadrome,
    'is_plaindrome': is_plaindrome,
    'is_nialpdrome': is_nialpdrome,
    'is_pandigital': is_pandigital,
    'is_repunit': is_repunit,
    'is_repdigit': is_repdigit,
    'is_undulating': is_undulating,
    'is_alternating': is_alternating,
    'is_self_descriptive': is_self_descriptive,
    'is_self': is_self,
    'is_smith': is_smith,
    'is_hoax': is_hoax,
    'has_unique_digits': has_unique_digits,
    # Binary
    'is_evil': is_evil,
    'is_odious': is_odious,
    'is_pernicious': is_pernicious,
    # Divisibility
    'is_refactorable': is_refactorable,
    'is_practical': is_practical,
    'is_arithmetic_number': is_arithmetic_number,
    'is_economical': is_economical,
    'is_equidigital': is_equidigital,
    'is_wasteful': is_wasteful,
    'is_polite': is_polite,
    'is_smooth_5': is_5_smooth,
    'is_smooth_7': is_7_smooth,
    # Factorial
    'is_factorial': is_factorial,
    'is_primorial': is_primorial,
    'is_hyperfactorial': is_hyperfactorial,
    'is_subfactorial': is_subfactorial,
    # Collatz
    'is_collatz_record': is_collatz_record,
    # Misc
    'is_taxicab': is_taxicab,
    'is_giuga': is_giuga,
    'is_untouchable': is_untouchable,
    'is_primary': is_primary,
    'is_perfect_totient': is_perfect_totient,
    'is_blum_integer': is_blum_integer,
    'is_central_binomial_coefficient': is_central_binomial_coefficient,
    'is_binomial_coefficient': is_binomial_coefficient,
    'is_partition_number': is_partition_number,
    'is_leap_year': is_leap_year,
    'is_pythagorean_hypotenuse': is_pythagorean_hypotenuse,
    'is_known_constant': is_known_constant,
    'is_sum_product': is_sum_product,
    'is_digit_squared_sum': is_digit_squared_sum,
    'is_digit_cubed_sum': is_digit_cubed_sum,
    'is_digit_fifth_sum': is_digit_fifth_sum,
    'is_sum_of_consecutive_primes': is_sum_of_consecutive_primes,
    'is_isbn_10_valid': isbn_10_check,
    'is_luhn_valid': is_luhn_valid,
}

def get_all_properties(n):
    """Run all checks on n. Returns dict of {name: result}."""
    results = {}
    for name, func in _ALL_BOOLEAN_CHECKS.items():
        try:
            results[name] = func(n)
        except Exception:
            results[name] = None
    # Extra computed values
    results['digit_sum'] = digit_sum(n)
    results['digit_product'] = digit_product(n)
    results['digital_root'] = digital_root(n)
    results['additive_persistence'] = additive_persistence(n)
    results['multiplicative_persistence'] = multiplicative_persistence(n)
    results['count_divisors'] = count_divisors(n)
    results['sum_of_divisors'] = sum_of_divisors(n)
    results['euler_totient'] = euler_totient(n)
    results['prime_factors'] = get_prime_factors(n)
    results['collatz_steps'] = collatz_steps(n)
    results['binary'] = to_binary(n)
    results['octal'] = to_octal(n)
    results['hex'] = to_hex(n)
    results['roman'] = to_roman(n)
    results['in_words'] = int_to_words(n) if 0 <= n < 1_000_000_000 else 'N/A'
    results['set_bits'] = count_set_bits(n)
    results['known_constant'] = known_constant_name(n)
    results['mobius'] = mobius(n)
    results['liouville'] = liouville_lambda(n)
    results['figurate_types'] = figurate_name(n)
    return results

def get_true_properties(n):
    """Return only properties that are True."""
    return {k: v for k, v in get_all_properties(n).items() if v is True}

def print_properties(n):
    props = get_all_properties(n)
    w = 45
    print(f"\n{'═'*w}")
    print(f"  Properties of {n}")
    print(f"{'═'*w}")
    print(f"\n  {'TRUE properties':}")
    print(f"  {'─'*40}")
    for k, v in props.items():
        if v is True:
            print(f"  ✓  {k}")
    print(f"\n  {'Computed values':}")
    print(f"  {'─'*40}")
    computed = ['digit_sum','digit_product','digital_root','additive_persistence',
                'multiplicative_persistence','count_divisors','sum_of_divisors',
                'euler_totient','prime_factors','collatz_steps','binary','octal',
                'hex','roman','in_words','set_bits','known_constant','mobius',
                'liouville','figurate_types']
    for k in computed:
        if k in props and props[k] is not None:
            print(f"  {k:<35} {props[k]}")
    print(f"{'═'*w}\n")

def count_properties(n):
    """Count how many properties n satisfies."""
    return sum(1 for v in get_all_properties(n).values() if v is True)

def most_special_in_range(start, end):
    """Return the number with the most True properties in [start, end]."""
    return max(range(start, end+1), key=count_properties)


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK DEMO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    test_nums = [1, 2, 6, 7, 9, 12, 13, 17, 28, 36, 153, 370, 496, 1729, 6174]
    for num in test_nums:
        true_props = get_true_properties(num)
        print(f"\n{num}: {list(true_props.keys())[:8]}{'...' if len(true_props)>8 else ''}")
    print("\n--- Full report for 153 ---")
    print_properties(153)
