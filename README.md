# numclassify

[![PyPI version](https://img.shields.io/pypi/v/numclassify.svg?color=FF9933&style=flat-square)](https://pypi.org/project/numclassify/)
[![Downloads](https://img.shields.io/pypi/dm/numclassify.svg?color=FF9933&style=flat-square)](https://pypi.org/project/numclassify/)
[![Python](https://img.shields.io/pypi/pyversions/numclassify?style=flat-square&color=FF9933)](https://pypi.org/project/numclassify/)
[![Tests](https://img.shields.io/github/actions/workflow/status/aratrikghosh2011-tech/numclassify/ci.yml?label=tests&style=flat-square&color=FF9933)](https://github.com/aratrikghosh2011-tech/numclassify/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-FF9933?style=flat-square)](LICENSE)

**Given a number, what is it?**

Most number-theory libraries — `labmath`, `eulerlib`, `pyntlib` — compute things: factor integers, find GCDs, generate primes. `numclassify` solves a different problem. Hand it a number and it tells you every named mathematical type that number belongs to, across 3000+ categories, with zero external dependencies.

```
153   →  Armstrong, Harshad, Triangular, Abundant, ...
1729  →  Taxicab (Hardy-Ramanujan), Carmichael, Zeisel, ...
28    →  Perfect, Triangular, Hexagonal, Semiprime, ...
```

Try it in your browser: **[numclassify Playground](https://aratrikghosh2011-tech.github.io/numclassify/playground.html)**

---

## Installation

```bash
pip install numclassify
```

Python 3.8+ required. No external dependencies.

---

## Quick Start

```python
import numclassify as nc

# Boolean checks
nc.is_prime(17)       # True
nc.is_perfect(28)     # True

# Classify a single number
nc.classify(1729)
# {
#   'number': 1729,
#   'score': 22,            # total true properties (incl. figurate)
#   'notable_score': 18,    # score excluding polygonal figurate noise
#   'true_properties': ['Taxicab', 'Carmichael', ...],
#   'categories': {'primes': [...], 'sequences': [...], ...}
# }

# Batch classify
nc.classify_batch([6, 28, 496])

# Find numbers in a range with a given property
nc.find_by_property(start=1, end=1000, Perfect=True)
# [6, 28, 496]

# Stream over large ranges without loading everything into memory
for result in nc.stream(1, 1_000_000, min_score=20):
    print(result)

# Stream only numbers with a specific property
for result in nc.stream(1, 10_000, has_property="prime"):
    print(result)

# All true properties of a number
nc.get_true_properties(1729)

# Pretty-print a formatted table
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

```bash
# Classify a number
numclassify check 1729

# JSON output for piping
numclassify check 153 --json

# Find numbers of a type
numclassify find armstrong --limit 10

# Filter a range
numclassify range 1 20 --filter prime

# Compare two numbers
numclassify compare 6 28

# List all types in a category
numclassify list --category primes

# Get info and OEIS reference for a type
numclassify info armstrong
```

---

## Number Categories

| Category | Count | Examples |
|---|---|---|
| Polygonal figurate | ~1003 | Triangular, Square, Pentagonal, Chiliagonal |
| Centered polygonal | ~998 | Centered Triangular, Centered Hexagonal |
| Prime families | 40 | Twin, Mersenne, Sophie Germain, Wilson, Safe |
| Digital invariants | 13 | Armstrong, Spy, Harshad, Disarium, Happy, Neon |
| Divisor-based | 27 | Perfect, Abundant, Weird, Amicable, Practical |
| Sequences | 16 | Fibonacci, Lucas, Catalan, Bell, Padovan |
| Powers | 13 | Perfect Square, Taxicab, Sum of Two Squares |
| Number theory | 14 | Evil, Carmichael, Keith, Autobiographical |
| Combinatorial | 10 | Factorial, Primorial, Subfactorial |
| Recreational | 6 | Kaprekar, Automorphic, Palindrome |
| Exam types | 8 | Armstrong, Strong, Sunny, Buzz, Magic, Unique |
| **Total** | **2140+** | |

---

## Custom Types

The `@register` decorator lets you add your own number types. Once registered, the type appears everywhere — `classify()`, `find_by_property()`, the CLI, all of it.

```python
from numclassify import register

@register(name="my_type", category="custom")
def is_my_type(n: int) -> bool:
    return n > 0 and n % 7 == 0 and str(n)[0] == "4"

import numclassify as nc
nc.is_my_type(42)           # True
nc.get_true_properties(42)  # [..., 'my_type', ...]
```

See [`examples/`](examples/) for runnable scripts covering all major features.

---

## API Reference

| Function | Description |
|---|---|
| `classify(n)` | Returns `{number, score, notable_score, true_properties, categories}` |
| `classify_batch(numbers)` | Classify a list; returns list of dicts |
| `random_number(max_n)` | Classify a randomly selected number |
| `find_by_property(start, end, **filters)` | Numbers in range matching property filters |
| `stream(start, end, min_score, has_property)` | Generator — memory-safe range classification |
| `get_all_properties(n)` | Dict of every type mapped to True/False |
| `get_true_properties(n)` | List of True property names only |
| `print_properties(n)` | Pretty-print property table to stdout |
| `count_properties(n)` | Count of True properties |
| `most_special_in_range(lo, hi, verbose)` | Number in range with the most True properties |
| `find_in_range(fn, lo, hi)` | Numbers where callable `fn` returns True |
| `find_any_in_range(predicates, lo, hi)` | Integers in range satisfying at least one predicate |
| `find_all_in_range(predicates, lo, hi)` | Integers in range satisfying all predicates |
| `register` | Decorator to add custom number types |
| `is_prime(n)` | Convenience boolean |
| `is_armstrong(n)` | Convenience boolean |
| `is_perfect(n)` | Convenience boolean |

Full docs: [aratrikghosh2011-tech.github.io/numclassify](https://aratrikghosh2011-tech.github.io/numclassify/)

---

## License

MIT © 2026 Aratrik Ghosh