# numclassify

**Given a number, what is it?**

Most number-theory libraries — `labmath`, `eulerlib`, `pyntlib` — compute things: factor integers, find GCDs, generate primes. `numclassify` solves a different problem. Hand it an integer and it tells you every named mathematical type that number belongs to, across 2140+ categories, with zero external dependencies.

```
153   →  Armstrong, Harshad, Triangular, Deficient, ...
1729  →  Taxicab (Hardy–Ramanujan), Carmichael, Harshad, ...
28    →  Perfect, Triangular, Hexagonal, Harmonic Divisor, ...
```

Try it live: **[numclassify Playground](playground.html)**

---

## Installation

```bash
pip install numclassify
```

Python 3.8–3.13. No external dependencies.

---

## Quick example

```python
import numclassify as nc

nc.classify(1729)
# {
#   'number': 1729,
#   'score': 25,
#   'notable_score': 19,
#   'true_properties': ['Taxicab', 'Carmichael', ...],
#   'categories': {'primes': [...], 'sequences': [...], ...}
# }

nc.is_prime(17)           # True
nc.is_perfect(28)         # True
nc.get_true_properties(6) # {'Perfect': True, 'Triangular': True, 'Pronic': True, ...}

nc.why("armstrong", 153)
# "153 is Armstrong because: 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153"

nc.property_info("armstrong")
# {'name': 'Armstrong', 'category': 'digital', 'oeis': 'A005188', 'examples': [...]}

nc.find(1, 1000, has=["harshad", "palindrome"])
```

---

## Categories

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

## Add your own types

```python
from numclassify import register

@register(name="My Type", category="recreational")
def is_my_type(n: int) -> bool:
    return n > 0 and n % 7 == 0

import numclassify as nc
nc.is_my_type(42)  # True — available everywhere immediately
```

See [API Reference](api.md) for the full function list, or the [CLI Reference](cli.md) for command-line usage.
