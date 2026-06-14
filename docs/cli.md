# CLI Reference

Install the package and the `numclassify` command is available immediately.

## check

Classify a single number.

```bash
numclassify check 1729
numclassify check 1729 --json     # machine-readable JSON output
```

## compare

Show properties shared between two numbers and properties unique to each.

```bash
numclassify compare 6 28
numclassify compare 6 28 --json
```

## find

Find numbers of a given type, starting from 1.

```bash
numclassify find armstrong
numclassify find prime --limit 20
```

## range

Classify or filter all integers in a range.

```bash
numclassify range 1 100
numclassify range 1 100 --filter prime
```

## info

Show the definition, category, and OEIS reference for a number type.

```bash
numclassify info armstrong
numclassify info taxicab
```

## list

List all registered number types.

```bash
numclassify list
numclassify list --category primes
numclassify list --category divisors
```
