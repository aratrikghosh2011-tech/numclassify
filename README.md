# numclassify

The most comprehensive Python library for number classification — 3000+ number types, zero dependencies.

[![PyPI version](https://img.shields.io/pypi/v/numclassify)](https://pypi.org/project/numclassify/)
[![Downloads](https://img.shields.io/pypi/dm/numclassify)](https://pypi.org/project/numclassify/)
[![Python versions](https://img.shields.io/pypi/pyversions/numclassify)](https://pypi.org/project/numclassify/)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/aratrikghosh2011-tech/numclassify/blob/main/LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/aratrikghosh2011-tech/numclassify/ci.yml?label=tests)](https://github.com/aratrikghosh2011-tech/numclassify/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/numclassify?label=version)](https://pypi.org/project/numclassify/)

> **Latest version: 0.2.1** — See [CHANGELOG](CHANGELOG.md) for what's new.

---

## Overview

Most number-theory libraries — `labmath`, `eulerlib`, `pyntlib` — are built around computation: factoring integers, finding GCDs, generating primes. `numclassify` solves a different problem: **given a number, what is it?**

```
153   →  Armstrong, Harshad, Triangular, Abundant ...
1729  →  Taxicab (Hardy-Ramanujan), Carmichael, Zeisel ...
28    →  Perfect, Triangular, Hexagonal, Semiprime ...
```

Over **3000 named number types** are supported, with instant lookup, no external dependencies, and a fully typed API.

---

## Installation

```bash
pip install numclassify
```

To install from source in editable mode:

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
nc.is_prime(17)            # True
nc.is_perfect(28)          # True

# Classify a single number
nc.classify(1729)
# {'number': 1729, 'true_properties': ['Taxicab', 'Carmichael', ...], 'score': 22}

# Classify multiple numbers at once
nc.classify_batch([6, 28, 496])

# Query by property
nc.find_by_property(start=1, end=1000, Perfect=True)
# [6, 28, 496]

# Memory-safe streaming over large ranges
for result in nc.stream(1, 1_000_000):
    if result['score'] > 30:
        print(result)

# Random number classification
nc.random_number()

# All true properties of a number
nc.get_true_properties(1729)

# Pretty-print everything
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

**Compare two numbers:**
```bash
$ numclassify compare 6 28
Comparing 6 and 28
──────────────────
Shared (13): Perfect, Triangular, Hexagonal, ...
Only in 6 (21): Armstrong, Factorial, Palindrome, ...
Only in 28 (8): Happy, Keith, Padovan, ...
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
| Polygonal (figurate) | 998 | Triangular, Square, Pentagonal, Chiliagonal |
| Centered Polygonal | 998 | Centered Triangular, Centered Hexagonal |
| Prime families | 41 | Twin, Mersenne, Sophie Germain, Wilson, Safe |
| Digital invariants | 10 | Armstrong, Spy, Harshad, Disarium, Happy, Neon |
| Divisor-based | 27 | Perfect, Abundant, Weird, Amicable, Practical |
| Sequences | 15 | Fibonacci, Lucas, Catalan, Bell, Padovan |
| Powers | 13 | Perfect Square, Taxicab, Sum of Two Squares |
| Number theory | 14 | Evil, Carmichael, Keith, Autobiographical |
| Combinatorial | 10 | Factorial, Primorial, Subfactorial, Catalan |
| Recreational | 5 | Kaprekar, Automorphic, Palindrome |
| **Total** | **3000+** | |

---

## Adding Custom Number Types

The `@register` decorator lets you define and integrate your own number types in a few lines. Once registered, the type is automatically available through the full API and CLI.

```python
from numclassify import register

@register(name="my_type", category="custom")
def is_my_type(n: int) -> bool:
    return n > 0 and n % 7 == 0 and str(n)[0] == "4"

import numclassify as nc
nc.is_my_type(49)              # False  (doesn't start with 4)
nc.is_my_type(42)              # True
nc.get_true_properties(42)     # [..., 'my_type', ...]
```

See the [`examples/`](examples/) folder for runnable scripts demonstrating all major features:
- [`basic_usage.py`](examples/basic_usage.py) — classify, batch, streaming
- [`custom_type.py`](examples/custom_type.py) — registering custom types
- [`find_perfect_numbers.py`](examples/find_perfect_numbers.py) — property-based search
- [`stream_large_range.py`](examples/stream_large_range.py) — memory-safe range streaming
- [`random_classify.py`](examples/random_classify.py) — random number classification

---

## API Reference

| Function | Description |
|---|---|
| `register(name, category, ...)` | Decorator to add custom number types to the full API |
| `classify(n)` | Returns a dict with the number, its true properties, and a score |
| `classify_batch(numbers)` | Classify a list of numbers; returns a list of dicts |
| `random_number(max_n)` | Classify a randomly selected number up to `max_n` |
| `find_by_property(start, end, **filters)` | Find numbers in a range matching given property filters |
| `stream(start, end)` | Generator yielding classify results one at a time; memory-safe |
| `is_prime(n)` | Returns `True` if `n` is prime |
| `is_armstrong(n)` | Returns `True` if `n` is an Armstrong (narcissistic) number |
| `get_all_properties(n)` | Dict mapping every registered type to `True` or `False` |
| `get_true_properties(n)` | List of only the properties that hold for `n` |
| `print_properties(n)` | Pretty-prints a formatted property table to stdout |
| `find_in_range(fn, lo, hi)` | All integers in `[lo, hi]` where `fn` returns `True` |
| `count_properties(n)` | Number of types that apply to `n` |
| `most_special_in_range(lo, hi)` | Number in `[lo, hi]` with the greatest count of true properties |

Full API documentation: [github.com/aratrikghosh2011-tech/numclassify](https://github.com/aratrikghosh2011-tech/numclassify)

---

## Requirements

- Python 3.8 or higher
- No external dependencies

---

## License

MIT © 2026 Aratrik Ghosh