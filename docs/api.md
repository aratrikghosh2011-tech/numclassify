# API Reference

## classify(n)
Returns dict with number, true_properties list, and score.

## classify_batch(numbers)
Classify a list of integers.

## random_number(max_n=10000)
Classify a random integer up to max_n.

## find_by_property(start, end, **filters)
Find numbers matching property filters.

## stream(start, end)
Memory-safe generator over large ranges.

## register(name, category, ...)
Decorator to register custom number types. See [examples/custom_type.py](https://github.com/aratrikghosh2011-tech/numclassify/blob/main/examples/custom_type.py).

## Utilities
- get_all_properties(n)
- get_true_properties(n)
- print_properties(n)
- count_properties(n)
- most_special_in_range(lo, hi)
- find_in_range(fn, lo, hi)
- is_prime(n), is_armstrong(n), is_perfect(n)
