# Changelog

All notable changes to numclassify will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-04-18

### Added

- Complete package with `@register` decorator plugin architecture — any function
  decorated with `@register` is automatically available via `get_all_properties`,
  `get_true_properties`, the CLI, and all search utilities
- **3000+ number types** across 10 categories, all zero-dependency pure Python

#### Figurate engine
- Auto-registers 998 polygonal types (triangular through chiliagonal)
- Auto-registers 998 centered polygonal types (centered triangular through centered chiliagonal)
- Single parametric generator — adding a new figurate family is one line

#### Prime families (41 types)
- Standard prime, twin prime, cousin prime, sexy prime
- Mersenne prime, Mersenne number, double Mersenne prime
- Sophie Germain prime, safe prime, Cunningham chain member
- Wilson prime, Fermat prime, Wieferich prime, Wall-Sun-Sun prime
- Lucky prime, Fortunate prime, Primorial prime
- Emirp, palindromic prime, permutable prime, circular prime
- Chen prime, Eisenstein prime, Gaussian prime
- Titanic prime, gigantic prime, megaprime (digit-count based)
- OEIS references included in metadata for all 41 types

#### Digital invariants (10 types)
- Armstrong (narcissistic), Spy number, Harshad (Niven), Disarium
- Happy number (cycle detection), Neon number, Duck number
- Nude number (divisible by all its digits), Automorphic, Cyclic

#### Divisor-based (27 types)
- Perfect, abundant, deficient, weird, pseudoperfect
- Amicable, sociable (order 4, 6, 8), quasiperfect candidate
- Practical, semiperfect, primitive abundant
- Hyperperfect, superperfect, multiply perfect
- Unitary perfect, bi-unitary perfect, hemiperfect
- Sublime, sublime-adjacent, colossally abundant, highly abundant

#### Sequences (15 types)
- Fibonacci, Lucas, Tribonacci, Tetranacci
- Catalan, Bell, Motzkin, Padovan, Perrin
- Pell, Jacobsthal, Stern, Recaman
- Lazy caterer, cake number

#### Powers (13 types)
- Perfect square, perfect cube, perfect power (any exponent)
- Taxicab (Hardy-Ramanujan number), generalized taxicab
- Sum of two squares, sum of three squares, sum of four squares (Lagrange)
- Powerful number, squarefree, cubefree, k-free
- Achilles number

#### Number theory (14 types)
- Evil number, odious number (Thue-Morse based)
- Carmichael number, Zeisel number, Keith number
- Autobiographical number, self-describing number
- Kaprekar number, Kaprekar constant check
- Economical, equidigital, extravagant (prime factorization digit count)
- Polydivisible number, pandigital

#### Combinatorial (10 types)
- Factorial, primorial, subfactorial (derangements)
- Catalan number (also in sequences), Bell number (also in sequences)
- Binomial coefficient (any row), central binomial coefficient
- Catalan's triangle member, Narayana number, Motzkin number

#### Recreational (5 types)
- Palindrome, near-palindrome
- Bouncy number (neither increasing nor decreasing digits)
- Increasing digits, decreasing digits

#### CLI — 5 commands
- `numclassify check <n>` — all true properties of a number, with `--json` flag
- `numclassify find <type> --limit <k>` — first k numbers of a given type
- `numclassify range <lo> <hi> --filter <type>` — filter a range by type
- `numclassify list --category <cat>` — list all registered types in a category
- `numclassify info <type>` — name, description, OEIS ref, examples

#### Infrastructure
- Zero external dependencies; stdlib only
- Python 3.8–3.13 compatible (tested in CI matrix)
- 60 pytest tests, all passing
- GitHub Actions CI across Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- PyPI publish via OIDC trusted publishing (no API token)
- `pyproject.toml` with Hatchling build backend