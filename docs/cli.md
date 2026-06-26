# CLI Reference

Install the package and the `numclassify` command is available immediately.

Running `numclassify` with no arguments shows a short intro with links to the
GitHub repo and docs site, followed by the standard help output.

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

## why

Explain why a number does or does not have a given property, showing the
actual arithmetic.

```bash
numclassify why armstrong 153
numclassify why perfect 12
numclassify why armstrong 153 --json
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

## query

Find numbers in a range matching multiple property conditions (AND/OR/NOT).

```bash
numclassify query 1 1000 --has prime palindrome
numclassify query 1 500 --has prime --not-has emirp
numclassify query 1 10000 --any-of perfect amicable
numclassify query 1 1000 --has harshad --json
```

`--has` and `--any-of` cannot be combined in the same query.

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
