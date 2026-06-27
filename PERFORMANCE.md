# Performance

## Hang Fixes (v0.5.0)

Four functions that previously caused indefinite hangs on large inputs were
fixed in v0.5.0 using bitmask subset-sum DP and a bounded sieve approach.

### Before / After

| Function | Input | Before | After |
|---|---|---|---|
| `is_semiperfect` | 999,999,999 | hangs indefinitely | 0.134s |
| `is_weird` | 999,999,999 | hangs indefinitely | 0.000s (early-exit: number is deficient, subset-sum not needed) |
| `is_zumkeller` | 999,999,999 | hangs indefinitely | 0.448s |
| `is_untouchable` | 500,000 | hangs indefinitely | 4.132s (near ceiling; values above 500,000 raise ValueError) |

### Algorithm Details

**`is_semiperfect` / `is_zumkeller` / `is_weird`**
Previously used a Python set-based subset-sum DP that rebuilt the entire
set for each divisor, causing exponential blowup for numbers with many
divisors. Replaced with Python big-integer bitmask DP:

```python
bitset = 1
for d in divisors:
    bitset |= bitset << d
```

Python's arbitrary-precision integers implement this in C, making it fast
even for numbers with hundreds of divisors.

**`is_untouchable`**
Previously attempted a raw Python loop over [2, 2n] for n > 10,000.
Now raises `ValueError` for n > 500,000 (measured ceiling where the
sieve completes in under 5 seconds) with a clear error message.

## Algorithmic Complexity

| Category | Typical complexity | Notes |
|---|---|---|
| Primality checks | O(√n) | Trial division |
| Digital properties | O(d) | d = number of digits |
| Divisor-based | O(√n) for divisor list | O(n·d) for subset-sum types |
| Figurate | O(1) | Closed-form formula |
| Sequence membership | O(log n) to O(n) | Varies by sequence |
