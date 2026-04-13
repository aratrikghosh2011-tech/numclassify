# numclassify 🔢

A pure-Python module with 138+ functions for number classification — covering every major number type used in school, competitive programming, and number theory.

No pip install needed. Zero dependencies. Python 3.6+.

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/numclassify.git
```

Then drop `numclassify.py` into your project.

## Quick start

```python
import numclassify as nc

nc.is_prime(17)          # True
nc.is_armstrong(153)     # True
nc.is_perfect(28)        # True
nc.is_happy(7)           # True
nc.is_fibonacci(13)      # True
nc.is_harshad(18)        # True

# Check every property at once
nc.print_properties(153)

# Find all Armstrong numbers 1–9999
nc.find_in_range(nc.is_armstrong, 1, 9999)
```

## Function categories

| Category | Key functions |
|---|---|
| Prime & composite | `is_prime`, `is_twin_prime`, `is_mersenne_prime`, `is_circular_prime`, `is_emirp` |
| Armstrong / narcissistic | `is_armstrong`, `is_disarium` |
| Perfect / abundant | `is_perfect`, `is_abundant`, `is_deficient`, `is_weird`, `is_semiperfect` |
| Palindrome | `is_palindrome`, `is_binary_palindrome`, `is_prime_palindrome` |
| Digit properties | `digit_sum`, `digital_root`, `additive_persistence`, `multiplicative_persistence` |
| Fibonacci / Lucas | `is_fibonacci`, `is_lucas`, `nth_fibonacci` |
| Figurate numbers | `is_triangular`, `is_pentagonal`, `is_hexagonal`, `is_pronic`, `is_star` |
| Power & square | `is_perfect_square`, `is_perfect_cube`, `is_powerful`, `is_squarefree` |
| Binary / bits | `to_binary`, `count_set_bits`, `is_power_of_two`, `is_pernicious` |
| Collatz | `collatz_steps`, `collatz_sequence` |
| Conversion | `to_roman`, `from_roman`, `int_to_words` |
| Generators | `primes_up_to`, `find_in_range`, `nth_prime` |
| Master | `get_all_properties`, `print_properties` |

## Requirements

- Python 3.6+
- Standard library only (`math`, `functools`, `itertools`)

## License

MIT — see [LICENSE](LICENSE)

## Author

Aratrik Ghosh
