# numclassify 

> A comprehensive, zero-dependency Python library for number classification — 653 functions, 155 boolean property checks, covering every major number type used in school, competitive programming, and number theory.

**Python 3.6+ · No dependencies · MIT License**

---

## Installation

No pip needed. Clone and drop the file into your project:

```bash
git clone https://github.com/aratrikghosh2011-tech/numclassify.git
```

```python
from numclassify import is_prime, is_armstrong, get_all_properties
```

---

## Quick start

```python
import numclassify as nc

nc.is_prime(17)            # True
nc.is_armstrong(153)       # True  (1³+5³+3³ = 153)
nc.is_perfect(28)          # True  (1+2+4+7+14 = 28)
nc.is_happy(7)             # True
nc.is_fibonacci(13)        # True
nc.is_harshad(18)          # True  (18 ÷ (1+8) = 2)
nc.is_taxicab(1729)        # True  (Hardy–Ramanujan number)
nc.is_carmichael(561)      # True
nc.is_strobogrammatic(69)  # True
nc.digital_root(9999)      # 9
nc.to_roman(2024)          # 'MMXXIV'
nc.int_to_words(1729)      # 'one thousand seven hundred twenty-nine'

# Scan every known property at once
nc.print_properties(1729)

# Get only the True properties
nc.get_true_properties(153)

# Find all Armstrong numbers from 1 to 9999
nc.find_in_range(nc.is_armstrong, 1, 9999)

# Find numbers satisfying multiple conditions at once
nc.find_all_in_range([nc.is_prime, nc.is_palindrome], 1, 1000)
```

### Sample output — `print_properties(1729)`

```
═════════════════════════════════════════════
  Properties of 1729
═════════════════════════════════════════════

  TRUE properties
  ────────────────────────────────────────
  ✓  is_composite
  ✓  is_carmichael
  ✓  is_sphenic           (7 × 13 × 19)
  ✓  is_taxicab           (1³+12³ = 9³+10³)
  ✓  is_harshad
  ✓  is_centered_cube
  ✓  is_squarefree
  ✓  is_known_constant    → Hardy-Ramanujan (taxicab)
  ... and 14 more

  Computed values
  ────────────────────────────────────────
  digit_sum                           19
  digital_root                        1
  prime_factors                       [7, 13, 19]
  collatz_steps                       104
  binary                              11011000001
  roman                               MDCCXXIX
  in_words            one thousand seven hundred twenty-nine
  mobius                              -1
═════════════════════════════════════════════
```

---

## Function categories

| Category | Count | Key functions |
|---|---|---|
| **Prime & composite** | 40+ | `is_prime`, `is_twin_prime`, `is_mersenne_prime`, `is_safe_prime`, `is_sophie_germain_prime`, `is_circular_prime`, `is_emirp`, `is_left_truncatable_prime`, `is_strong_prime`, `is_chen_prime`, `is_pythagorean_prime`, `is_carmichael`, `miller_rabin` |
| **Armstrong / narcissistic** | 10+ | `is_armstrong`, `is_disarium`, `is_munchausen`, `is_sum_of_digit_factorials`, `is_perfect_digital_invariant` |
| **Perfect / abundant** | 15+ | `is_perfect`, `is_abundant`, `is_deficient`, `is_weird`, `is_semiperfect`, `is_amicable`, `is_sociable`, `is_superperfect`, `is_harmonic_divisor`, `is_zumkeller` |
| **Palindrome** | 10+ | `is_palindrome`, `is_binary_palindrome`, `is_octal_palindrome`, `is_lychrel`, `is_strobogrammatic`, `reverse_add_steps` |
| **Fibonacci & sequences** | 20+ | `is_fibonacci`, `is_lucas`, `is_tribonacci`, `is_pell`, `is_padovan`, `is_perrin`, `is_jacobsthal`, `is_catalan`, `is_bell`, `is_motzkin`, `is_recaman`, `is_fibbinary` |
| **Figurate numbers** | 30+ | `is_triangular`, `is_pentagonal`, `is_hexagonal`–`is_dodecagonal`, `is_centered_square`, `is_centered_hexagonal`, `is_star`, `is_pronic`, `is_tetrahedral`, `is_pyramidal`, `is_icosahedral`, `is_centered_cube` |
| **Powers & squares** | 15+ | `is_perfect_square`, `is_perfect_cube`, `is_perfect_fourth_power`, `is_perfect_power`, `is_powerful`, `is_squarefree`, `is_achilles`, `is_sum_of_two_squares`, `is_loeschian` |
| **Digit properties** | 30+ | `digit_sum`, `digital_root`, `additive_persistence`, `multiplicative_persistence`, `is_smith`, `is_hoax`, `is_bouncy`, `is_metadrome`, `is_katadrome`, `is_undulating`, `is_cyclops`, `is_self_descriptive`, `is_nude`, `is_polydivisible` |
| **Binary / bits** | 15+ | `is_evil`, `is_odious`, `is_pernicious`, `is_fibbinary`, `count_set_bits`, `is_blum_integer`, `is_binary_palindrome`, `hamming_weight` |
| **Divisibility** | 30+ | `is_smooth` (2–23), `is_rough`, `is_practical`, `is_refactorable`, `is_economical`, `is_equidigital`, `is_wasteful`, `is_sphenic`, `is_brilliant`, `is_semi_prime` |
| **Factorial & related** | 10+ | `is_factorial`, `is_double_factorial`, `is_subfactorial`, `is_primorial`, `is_hyperfactorial`, `is_superfactorial`, `is_factorial_prime` |
| **Number theory** | 20+ | `euler_totient`, `mobius`, `sigma_0/1/2/k`, `is_primitive_root`, `legendre_symbol`, `jacobi_symbol`, `chinese_remainder`, `discrete_log`, `is_perfect_totient`, `is_giuga` |
| **Special & named** | 25+ | `is_taxicab`, `is_vampire`, `is_keith`, `is_parasitic`, `is_automorphic`, `is_trimorphic`, `is_kaprekar`, `is_happy`, `is_lucky`, `is_giuga`, `is_untouchable`, `is_zumkeller` |
| **Collatz** | 5 | `collatz_steps`, `collatz_sequence`, `collatz_max`, `is_collatz_record` |
| **Modular arithmetic** | 15+ | `is_quadratic_residue`, `is_primitive_root`, `chinese_remainder`, `mod_pow`, `mod_inv` |
| **Geometric** | 10+ | `is_tetrahedral`, `is_pyramidal`, `is_icosahedral`, `is_dodecahedral`, `is_pythagorean_hypotenuse`, `pythagorean_triples_with_hyp` |
| **Combinatorial** | 10+ | `is_catalan`, `is_bell`, `is_motzkin`, `is_central_binomial_coefficient`, `is_binomial_coefficient`, `is_partition_number`, `partition_count` |
| **Conversion** | 15+ | `to_roman`, `from_roman`, `int_to_words`, `to_binary`, `to_octal`, `to_hex`, `to_base`, `from_base`, `balanced_ternary` |
| **Generators** | 10+ | `primes_up_to`, `find_in_range`, `find_all_in_range`, `find_any_in_range`, `nth_prime`, `nth_fibonacci`, `nth_catalan`, `nth_bell`, `most_special_in_range` |
| **Master** | 5 | `get_all_properties`, `get_true_properties`, `print_properties`, `count_properties`, `most_special_in_range` |

---

## Advanced usage

```python
# Which number between 1–10000 has the most TRUE properties?
nc.most_special_in_range(1, 10000)

# Count properties a number satisfies
nc.count_properties(1729)   # → 22

# Batch check — scan a list against all known properties
numbers = [6, 28, 496, 8128, 33550336]
for n in numbers:
    true_props = nc.get_true_properties(n)
    print(f"{n}: {list(true_props.keys())}")

# Number theory tools
nc.euler_totient(100)               # 40
nc.mobius(30)                       # -1
nc.legendre_symbol(2, 7)            # 1
nc.chinese_remainder([2,3],[3,5])   # 8  (x≡2 mod 3, x≡3 mod 5)
nc.discrete_log(2, 3, 7)           # 1  (2^1 ≡ 3 mod 7? No, finds actual)
nc.miller_rabin(1000000007)         # True (deterministic)

# Collatz
nc.collatz_steps(27)       # 111
nc.collatz_sequence(6)     # [6, 3, 10, 5, 16, 8, 4, 2, 1]
nc.collatz_max(27)         # 9232

# Goldbach
nc.goldbach_pairs(28)      # [(5,23), (11,17)]
nc.goldbach_count(100)     # number of pairs

# Conversions
nc.to_base(255, 16)        # 'ff'
nc.balanced_ternary(10)    # '101'
nc.int_to_words(999999)    # 'nine hundred ninety-nine thousand...'

# Range finders
nc.find_in_range(nc.is_carmichael, 1, 10000)
nc.find_all_in_range([nc.is_prime, nc.is_fibonacci], 1, 1000)
nc.find_any_in_range([nc.is_perfect, nc.is_amicable], 1, 10000)
```

---

## Running tests

```bash
python3 tests.py -v
```

131 tests across 17 test classes covering every function category.

---

## Requirements

- Python 3.6+
- Standard library only (`math`, `itertools`, `functools`, `collections`)

---

## License

MIT © 2025 Aratrik Ghosh

---

## About

Built as an open-source portfolio project and reference library for number theory enthusiasts, competitive programmers, and students. Every function is documented with its mathematical definition.