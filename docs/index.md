# numclassify

**Given a number, what is it?**

Most number-theory libraries — `labmath`, `eulerlib`, `pyntlib` — compute things: factor integers, find GCDs, generate primes. `numclassify` solves a different problem. Hand it an integer and it tells you every named mathematical type that number belongs to, across 2140+ categories, with zero external dependencies.

```
153   →  Armstrong, Harshad, Triangular, Abundant, ...
1729  →  Taxicab (Hardy–Ramanujan), Carmichael, Zeisel, ...
28    →  Perfect, Triangular, Hexagonal, Semiprime, ...
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
#   'score': 22,
#   'notable_score': 18,
#   'true_properties': ['Taxicab', 'Carmichael', ...],
#   'categories': {'primes': [...], 'sequences': [...], ...}
# }

nc.is_prime(17)           # True
nc.is_perfect(28)         # True
nc.get_true_properties(6) # ['Perfect', 'Triangular', 'Pronic', ...]
```

---

## Categories

| Category | Count | Examples |
|---|---|---|
| Polygonal figurate | ~1003 | Triangular, Square, Pentagonal |
| Centered polygonal | ~998 | Centered Triangular, Centered Hexagonal |
| Prime families | 40 | Twin, Mersenne, Sophie Germain, Safe |
| Digital invariants | 13 | Armstrong, Harshad, Disarium, Happy |
| Divisor-based | 27 | Perfect, Abundant, Weird, Practical |
| Sequences | 16 | Fibonacci, Lucas, Catalan, Bell |
| Powers | 13 | Perfect Square, Taxicab, Powerful |
| Number theory | 14 | Evil, Carmichael, Autobiographical |
| Combinatorial | 10 | Factorial, Primorial, Subfactorial |
| Recreational | 6 | Kaprekar, Automorphic, Palindrome |
| Exam types | 8 | Strong, Sunny, Buzz, Magic, Unique |

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
