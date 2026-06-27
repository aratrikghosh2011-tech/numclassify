# Architecture

numclassify is built around a central registry of mathematical predicates,
each registered with metadata via a decorator.

## Registry

`numclassify/_registry.py` is the backbone. It defines:

- `NumberType` — a dataclass holding each registered type's metadata:
  name, category, predicate function, OEIS ID, description, aliases,
  an optional `explain` function, and an `exam_tag` boolean.
- `REGISTRY` — a flat dict mapping every normalized name and alias to its
  `NumberType`. A type with 3 aliases appears 3 times in `REGISTRY` but
  is counted once toward the 2140 unique types.
- `@register(name, category, oeis, description, aliases, explain, exam_tag)`
  — the decorator that registers a predicate function. Every `is_*`
  function in the `_core/` modules uses this.

## Adding a new type

1. Pick the right `_core/` module (primes, digital, divisors, sequences,
   powers, figurate, number_theory, combinatorial, recreational, exam_types).
2. Write an `is_yourtype(n: int) -> bool` function.
3. Decorate it with `@register(name=..., category=..., oeis=..., description=...)`.
4. Add OEIS examples to `tests/test_registry.py`.
5. Optionally add `explain=` using a template from `_explain_templates.py`
   or a custom lambda.

The function is automatically discoverable via `classify()`, `why()`,
`find()`, `property_info()`, and the CLI with no further changes.

## Module map

```
numclassify/
├── __init__.py          — public API (17 exported names)
├── _registry.py         — NumberType, REGISTRY, @register, Step, render_steps
├── cli.py               — argparse CLI, 8 commands
└── _core/
    ├── primes.py        — 40 types (prime, twin prime, mersenne, ...)
    ├── figurate.py      — 1003 polygonal types (auto-generated)
    ├── digital.py       — 13 types (armstrong, harshad, neon, ...)
    ├── divisors.py      — 27 types (perfect, abundant, weird, ...)
    ├── sequences.py     — 16 types (fibonacci, catalan, bell, ...)
    ├── powers.py        — 13 types (perfect square, taxicab, ...)
    ├── number_theory.py — 14 types (keith, carmichael, evil, ...)
    ├── combinatorial.py — 10 types (factorial, catalan, ...)
    ├── recreational.py  — 6 types (kaprekar, palindrome, ...)
    └── exam_types.py    — 8 types tagged exam_tag=True for school use
```

## Figurate auto-generation

`figurate.py` doesn't hand-code 1003 types. It loops k from 3 to 1005
and calls a factory that generates both the predicate (closed-form
formula check) and the @register call for "k-gonal" and "centered k-gonal"
types. This is why the registry has 2140 types but only ~10 lines per
category in the source.

## Explanation engine

`_explain_templates.py` provides two reusable template factories:
- `digit_power_template(power_fn)` — for digit-transform properties
- `divisor_sum_template(target_fn, compare)` — for divisor-comparison properties

Templates return `Callable[[int], str]` so they're drop-in replacements
for hand-written `explain=` lambdas. 33 of 139 handcrafted types currently
have explain coverage.
