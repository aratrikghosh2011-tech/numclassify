# API Reference

## classify(n)

Classifies a single integer. Returns a dict:

```python
{
    "number": 1729,
    "score": 22,             # total true properties (includes all figurate types)
    "notable_score": 18,     # score excluding polygonal figurate noise — better for display
    "true_properties": ["Taxicab", "Carmichael", ...],   # sorted by category then name
    "categories": {
        "primes": ["Carmichael"],
        "sequences": ["..."],
        ...
    }
}
```

`notable_score` excludes `figurate` and `figurate_centered` hits. Use it when displaying
a score to humans  --  otherwise n=1 (which is the first k-gonal number for every k) shows
a score of 2000+.

## classify_batch(numbers)

Classify a list of integers. Returns a list of dicts in the same format as `classify()`.

```python
nc.classify_batch([6, 28, 496])
```

## random_number(max_n=10000)

Classify a random integer from 1 to `max_n`.

## find_by_property(start, end, **filters)

Find integers in `[start, end]` matching keyword property filters.

```python
nc.find_by_property(start=1, end=1000, Perfect=True)
# [6, 28, 496]
```

## stream(start, end, min_score=None, has_property=None)

Memory-safe generator over a range. Yields one result dict per integer.

- `min_score`  --  skip numbers with `notable_score` below this threshold
- `has_property`  --  skip numbers that don't have this property as True

```python
for result in nc.stream(1, 1_000_000, min_score=20):
    print(result)

for result in nc.stream(1, 10_000, has_property="prime"):
    print(result)
```

## get_all_properties(n)

Returns a dict of every registered type mapped to `True` or `False`.

## get_true_properties(n)

Returns a dict mapping each True property name to `True`.

Note: `classify(n)["true_properties"]` gives the same names as a sorted list.

## print_properties(n)

Pretty-prints a formatted table of all True properties to stdout.

## count_properties(n)

Returns the count of True properties (equivalent to `score` in `classify()`).

## most_special_in_range(lo, hi, verbose=False)

Returns the integer in `[lo, hi]` with the highest `score`. Pass `verbose=True`
for progress output on large ranges.

## find_in_range(fn, lo, hi)

Returns all integers in `[lo, hi]` where callable `fn(n)` returns `True`.

```python
nc.find_in_range(nc.is_prime, 1, 100)
```

## find_any_in_range(funcs_or_names, start, end)

Returns all integers in `[start, end]` that satisfy **at least one** of the given predicates.

```python
# Numbers that are prime OR palindrome in 1..100
nc.find_any_in_range(["prime", "palindrome"], 1, 100)

# Using callables
nc.find_any_in_range([nc.is_prime, nc.is_armstrong], 1, 500)
```

## find_all_in_range(funcs_or_names, start, end)

Returns all integers in `[start, end]` that satisfy **every** predicate given.

```python
# Numbers that are BOTH prime AND palindrome in 1..1000
nc.find_all_in_range(["prime", "palindrome"], 1, 1000)
# => [2, 3, 5, 7, 11, 101, 131, 151, ...]
```

## why(property_name, n)

Explain why `n` does or does not have a given property, showing the actual arithmetic.

```python
nc.why("armstrong", 153)
# '153 is Armstrong because: 153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153'

nc.why("perfect", 12)
# '12 is NOT Perfect: proper divisors of 12 = {1, 2, 3, 4, 6}, sum = 16 != 12'
```

Raises `ValueError` for unknown property names.

## property_info(name)

Returns registry metadata for a property, including auto-generated examples.

```python
nc.property_info("armstrong")
# {
#   "name": "Armstrong",
#   "description": "An Armstrong number (also known as a narcissistic or pluperfect number) is an integer that is equal to the sum of its own digits each raised to the power of the number of digits.",
#   "category": "digital",
#   "oeis": "A005188",
#   "examples": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407]
# }
```

Raises `ValueError` for unknown property names.

## find(start, end, has=None, not_has=None, any_of=None)

Query numbers in a range by property combinations.

```python
nc.find(1, 10000, has=["harshad", "palindrome"])
nc.find(1, 500, has=["prime"], not_has=["emirp"])
nc.find(1, 10000, any_of=["perfect", "amicable"])
```

`has` and `any_of` cannot be combined in the same call.

## register

Decorator to add a custom number type. Registered types appear everywhere  --  `classify()`,
`find_by_property()`, the CLI, all of it.

```python
from numclassify import register

@register(name="My Type", category="recreational", oeis="A000000",
          description="Numbers divisible by 7 starting with 4")
def is_my_type(n: int) -> bool:
    return n > 0 and n % 7 == 0 and str(n)[0] == "4"
```

Parameters:

- `name`  --  display name (required)
- `category`  --  category string (required)
- `oeis`  --  OEIS sequence ID, e.g. `"A000040"` (optional)
- `description`  --  one-line description (optional)

## Convenience booleans

```python
nc.is_prime(17)       # True
nc.is_armstrong(153)  # True
nc.is_perfect(28)     # True
```

These are thin wrappers around the registered functions, exported for direct use.
