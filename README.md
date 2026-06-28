# numclassify

[![PyPI version](https://img.shields.io/pypi/v/numclassify.svg?color=FF9933&style=flat-square)](https://pypi.org/project/numclassify/)
[![Downloads](https://img.shields.io/pypi/dm/numclassify.svg?color=FF9933&style=flat-square)](https://pypi.org/project/numclassify/)
[![Python](https://img.shields.io/pypi/pyversions/numclassify?style=flat-square&color=FF9933)](https://pypi.org/project/numclassify/)
[![Tests](https://img.shields.io/github/actions/workflow/status/aratrikghosh2011-tech/numclassify/ci.yml?label=tests&style=flat-square&color=FF9933)](https://github.com/aratrikghosh2011-tech/numclassify/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-FF9933?style=flat-square)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-69%25-e05d44?style=flat-square)](https://github.com/aratrikghosh2011-tech/numclassify/tree/main/tests)

## What's new in v0.6.0

- **`similar_numbers(n, top_k=5)`** — find integers mathematically closest to n by shared properties
- **`specialness_percentile(n)`** — how rare is your number? Returns its percentile rank
- **Explanation engine** — `why()` now covers 116/139 types (83.5%), up from 33
- **`property_info()`** — now includes `oeis_url` field
- **Developer tools** — `tools/audit_explain.py`, `tools/generate_docs.py`, `tools/scaffold_type.py`, `tools/release.py`

**Given a number, what is it?**

Most number-theory libraries — `labmath`, `eulerlib`, `pyntlib` — compute things: factor integers, find GCDs, generate primes. `numclassify` solves a different problem. Hand it a number and it tells you every named mathematical type that number belongs to, across 2140+ categories, with zero external dependencies.

## Why I built this

I was doing number programs in school (Armstrong numbers, perfect numbers,
that kind of thing) and went looking for a Python package I could just import
instead of rewriting the same checks every time. I couldn't find one. Every
library I found computed things, factors, GCDs, primes, but none of them
actually classified a number into the type it was.

Then I realized why: schools include these programs in the syllabus to teach
students Python and basic mathematical logic, not so students can look up
which number is which. The exercise is the point. So a library that just
answers "is this Armstrong" defeats the purpose schools have for assigning it
in the first place.

That's why `why()` and the explain functions exist. Instead of just returning
True or False, numclassify shows the actual math, the same steps you'd write
out by hand. The goal isn't to do the homework for you. It's to be the thing
you check your own work against, or use to explore beyond what one assignment
asks for.

```
153   →  Armstrong, Harshad, Triangular, Abundant, ...
1729  →  Taxicab (Hardy-Ramanujan), Carmichael, Harshad, ...
28    →  Perfect, Triangular, Hexagonal, Semiprime, ...
```

Try it in your browser: **[numclassify Playground](playground.html)**

---

## Installation

```bash
pip install numclassify
```

Python 3.8+ required. No external dependencies.

---

## Quick Start

The standout feature is `why()` — it explains the reasoning, not just the result:

```python
import numclassify as nc

# Not just True or False — shows you the actual math
nc.why("armstrong", 153)
# "153 is Armstrong because: 153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153"

nc.why("perfect", 28)
# "28 is Perfect because: proper divisors = {1, 2, 4, 7, 14}, sum = 28"
```

### Basic usage

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

# All true properties of a number (returns a dict of True properties)
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

# Explain why a number has a property
numclassify why armstrong 153

# Multi-property query with AND/OR/NOT logic
numclassify query 1 1000 --has prime palindrome
```

---

## Number Categories

<!-- category-table:start -->
| Category | Count |
|---|---|
| Polygonal figurate | ~1003 |
| Centered polygonal | ~998 |
| Prime families | 40 |
| Digital invariants | 13 |
| Divisor-based | 27 |
| Sequences | 16 |
| Powers | 13 |
| Combinatorial | 10 |
| Recreational | 6 |
| **Total** | **2140** |
<!-- category-table:end -->

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
| `get_true_properties(n)` | Dict mapping each True property name to `True` |
| `print_properties(n)` | Pretty-print property table to stdout |
| `count_properties(n)` | Count of True properties |
| `most_special_in_range(lo, hi, verbose)` | Number in range with the most True properties |
| `find_in_range(fn, lo, hi)` | Numbers where callable `fn` returns True |
| `find_any_in_range(predicates, lo, hi)` | Integers in range satisfying at least one predicate |
| `find_all_in_range(predicates, lo, hi)` | Integers in range satisfying all predicates |
| `why(property, n)` | Step-by-step explanation of why n does/doesn't satisfy a property |
| `property_info(name)` | Registry metadata for a type, with auto-generated examples |
| `find(start, end, has, not_has, any_of)` | Query a range with multi-property AND/OR/NOT logic |
| `register` | Decorator to add custom number types |
| `is_prime(n)` | Convenience boolean |
| `is_armstrong(n)` | Convenience boolean |
| `is_perfect(n)` | Convenience boolean |

Full docs: [aratrikghosh2011-tech.github.io/numclassify](https://aratrikghosh2011-tech.github.io/numclassify/)

---

## More

- [Contributing](CONTRIBUTING.md) — how to add new number types
- [Security](SECURITY.md) — reporting vulnerabilities
- [Performance](PERFORMANCE.md) — benchmarks and complexity notes
- [Architecture](ARCHITECTURE.md) — registry internals and module map
- [Changelog](CHANGELOG.md) — full version history

## License

MIT © 2026 Aratrik Ghosh