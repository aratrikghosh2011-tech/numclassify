# numclassify

> The most comprehensive Python library for number classification — 3000+ number types, zero dependencies.

[![PyPI version](https://img.shields.io/pypi/v/numclassify)](https://pypi.org/project/numclassify/)
[![Python versions](https://img.shields.io/pypi/pyversions/numclassify)](https://pypi.org/project/numclassify/)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/aratrikghosh2011-tech/numclassify/blob/main/LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/aratrikghosh2011-tech/numclassify/ci.yml?label=tests)](https://github.com/aratrikghosh2011-tech/numclassify/actions/workflows/ci.yml)

---

## Why numclassify?

Most number-theory libraries — `labmath`, `eulerlib`, `pyntlib` — answer *computational* questions: factor this, find the GCD, generate primes up to N.

`numclassify` answers a different question: **what kind of number is this?**

- `153` → Armstrong, Narcissistic, Harshad, Triangular, Abundant…
- `1729` → Taxicab (Hardy-Ramanujan), Zeisel, Carmichael…
- `28` → Perfect, Triangular, Hexagonal, Semiprime…

Over **3000 named number types**, instant lookup, no external dependencies.

---

## Installation

```bash
pip install numclassify
```

Or clone and install in editable mode:

```bash
git clone https://github.com/aratrikghosh2011-tech/numclassify.git
cd numclassify
pip install -e .
```

---

## Quick Start

```python
import numclassify as nc

# Boolean checks
nc.is_prime(17)          # True
nc.is_armstrong(153)     # True
nc.is_perfect(28)        # True

# All true properties of a number
nc.get_true_properties(1729)
# ['taxicab', 'zeisel', 'carmichael', 'odd', 'composite',
#  'deficient', 'squarefree', 'cubefree', 'powerful_not_perfect_power']

# Search a range
nc.find_in_range(nc.is_armstrong, 1, 10000)
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474]

# Pretty-print everything about a number
nc.print_properties(153)
# ┌─────────────────────────────────────────┐
# │  Properties of 153                      │
# ├─────────────────────────────────────────┤
# │  armstrong         ✓                    │
# │  harshad           ✓                    │
# │  triangular        ✓                    │
# │  ...                                    │
# └─────────────────────────────────────────┘
```

---

## CLI

numclassify ships with a fully-featured command-line interface.

**Check a number:**
```bash
$ numclassify check 1729
1729 properties:
  taxicab         ✓
  carmichael      ✓
  zeisel          ✓
  odd             ✓
  deficient       ✓
  squarefree      ✓
```

**JSON output (pipe-friendly):**
```bash
$ numclassify check 153 --json
{"armstrong": true, "harshad": true, "triangular": true, "abundant": true, ...}
```

**Find numbers of a type:**
```bash
$ numclassify find armstrong --limit 10
1, 2, 3, 4, 5, 6, 7, 8, 9, 153
```

**Filter a range:**
```bash
$ numclassify range 1 20 --filter prime
2, 3, 5, 7, 11, 13, 17, 19
```

**List all registered types in a category:**
```bash
$ numclassify list --category primes
twin_prime, mersenne_prime, sophie_germain_prime, safe_prime,
wilson_prime, fermat_prime, ... (41 total)
```

**Get info about a type:**
```bash
$ numclassify info armstrong
Name:        armstrong
Category:    digital_invariants
Description: A number equal to the sum of its digits each raised to the power
             of the number of digits. Also called narcissistic numbers.
OEIS:        A005188
Examples:    1, 2, 3, 153, 370, 371, 407, 1634, 8208, 9474
```

---

## Number Categories

| Category | Count | Examples |
|---|---|---|
| Polygonal (figurate) | 998 | Triangular, Square, Pentagonal … Chiliagonal |
| Centered Polygonal | 998 | Centered Triangular, Centered Hexagonal … |
| Prime families | 41 | Twin, Mersenne, Sophie Germain, Wilson, Safe… |
| Digital invariants | 10 | Armstrong, Spy, Harshad, Disarium, Happy, Neon… |
| Divisor-based | 27 | Perfect, Abundant, Weird, Amicable, Practical… |
| Sequences | 15 | Fibonacci, Lucas, Catalan, Bell, Padovan… |
| Powers | 13 | Perfect Square, Taxicab, Sum of Two Squares… |
| Number theory | 14 | Evil, Carmichael, Keith, Autobiographical… |
| Combinatorial | 10 | Factorial, Primorial, Subfactorial, Catalan… |
| Recreational | 5 | Kaprekar, Automorphic, Palindrome… |
| **Total** | **3000+** | |

---

## Adding Your Own Number Type

The `@register` decorator lets you plug in custom types in 6 lines:

```python
from numclassify import register

@register(name="my_type", category="custom")
def is_my_type(n: int) -> bool:
    return n > 0 and n % 7 == 0 and str(n)[0] == "4"

# Now works everywhere
import numclassify as nc
nc.is_my_type(49)              # False  (doesn't start with 4)
nc.is_my_type(42)              # True
nc.get_true_properties(42)     # [..., 'my_type', ...]
```

---

## API Reference

| Function | Description |
|---|---|
| `is_prime(n)` | Returns `True` if `n` is a standard prime |
| `is_armstrong(n)` | Returns `True` if `n` is a narcissistic/Armstrong number |
| `get_all_properties(n)` | Dict of every registered type → `True`/`False` |
| `get_true_properties(n)` | List of only the properties that are `True` |
| `print_properties(n)` | Pretty-prints a formatted property table to stdout |
| `find_in_range(fn, lo, hi)` | All integers in `[lo, hi]` where `fn` returns `True` |
| `find_all_in_range(lo, hi)` | Dict mapping every number in range to its true properties |
| `count_properties(n)` | Count of how many types apply to `n` |
| `most_special_in_range(lo, hi)` | The number in `[lo, hi]` with the most true properties |

Full API docs: [github.com/aratrikghosh2011-tech/numclassify](https://github.com/aratrikghosh2011-tech/numclassify)

---

## Requirements

- Python 3.8 or higher
- Zero external dependencies

---

## License

MIT © 2026 Aratrik Ghosh