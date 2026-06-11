# Contributing to numclassify

## Adding a New Number Type

The fastest way to contribute is adding a new number type using the `@register` decorator.

### Step 1 \u2014 Write your function

```python
from numclassify import register

@register(name="My Type", category="recreational")
def is_my_type(n: int) -> bool:
    return n > 0 and n % 7 == 0
```

That's it. Your type is now available via:
- `nc.get_all_properties(n)`
- `nc.get_true_properties(n)`
- `nc.find_in_range(nc.is_my_type, 1, 1000)`
- `numclassify find my_type` in the CLI

### Step 2 \u2014 Add it to the right module

Place your function in the appropriate file under `numclassify/_core/`:

| Module | Types |
|---|---|
| `primes.py` | Prime families |
| `figurate.py` | Polygonal/figurate numbers |
| `divisors.py` | Divisor-based (perfect, abundant...) |
| `digital.py` | Digit-based (Armstrong, Harshad...) |
| `sequences.py` | Number sequences (Fibonacci, Lucas...) |
| `powers.py` | Powers and sums |
| `number_theory.py` | Number theory properties |
| `combinatorial.py` | Combinatorial numbers |
| `recreational.py` | Recreational/fun types |

### Step 3 \u2014 Add a test

Add a test in `tests/` following the existing pattern:

```python
def test_is_my_type():
    assert nc.is_my_type(7) == True
    assert nc.is_my_type(1) == False
```

### Step 4 \u2014 Submit a PR

```bash
git checkout -b add-my-type
git add .
git commit -m "Add My Type number classification"
git push origin add-my-type
```

Then open a pull request on GitHub.

## Running Tests

```bash
cd numclassify
python -m pytest tests/ -v
```

## Code Style

- Pure Python, no external dependencies
- Type hints required on all functions
- Function name must start with `is_` for boolean classifiers
