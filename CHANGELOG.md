# Changelog

All notable changes to numclassify will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.2] - 2026-06-12

### Added
- Search autocomplete dropdown — suggests property names as you type in the search field
- Confetti celebration burst when a number scores >50 properties
- Keyboard shortcuts: `C` (classify), `S` (search), `N` (Number of the Day), `?`/`H` (show shortcuts overlay)
- `prefers-reduced-motion` support — disables all animations for accessibility

### Fixed
- No bugs reported since v0.3.1

## [0.3.1] - 2026-06-12

### Added
- Version number displayed on playground page (fetched live from installed package)
- Category-colored tags on playground (distinct accent color per property category)
- Batch classify — enter comma/space-separated numbers for a mini-table of results
- Recent classification history panel (last 20 numbers, persisted in localStorage)
- Property tooltips on tag hover (shows category name)
- Fuzzy search suggestion ("Did you mean X?") on property misspellings
- Search pagination with "Load More" button (50 results per page)
- Number of the Day date picker — pick any past date for that day's number
- Scroll-to-top floating button (appears after 400px scroll)
- Light theme toggle (sun/moon button, saved to localStorage)
- Download classification results as JSON file
- Keyboard shortcut hints displayed on buttons

### Changed
- Split playground.html into 3 files: HTML skeleton, CSS (~1000 lines), JS (~660 lines)
- Tab switching now has slide-in animation (translateX + opacity)
- Result panels slide up on reveal (translateY + opacity)
- Score counter animates from 0 to final count (cubic ease-out, 400ms)
- Number digits fade in sequentially (40ms stagger per digit)
- Score badge pulses green on update
- Tags enter with random rotation (-3° to +3°) per tag
- Search results stagger in with 25ms delay per item
- Buttons have click ripple effect (radial gradient at cursor position)
- Toast slides in from the right instead of appearing in place
- All backgrounds and text colors transition smoothly on theme switch

## [0.3.0] - 2026-06-12

### Added
- Interactive Playground page (docs/playground.html) powered by Pyodide
- Classifier, property search, number comparison, random number, and Number of the Day features
- Shareable URLs via ?n=<number> query parameter
- Copy results to clipboard button
- Auto-deploy GitHub Pages workflow on every push to main and on version tags
- Version number now dynamically read from package metadata (single source of truth)
- PyPI version and downloads badges in README

## [0.2.0] - 2026-05-11

### Added
- `classify(n)` — returns `{"number": n, "true_properties": [...], "score": int}`
- `classify_batch(numbers)` — classify a list of numbers in one call
- `random_number(max_n=10000)` — classify a random number
- `find_by_property(start, end, **filters)` — query numbers by property name/value
- `stream(start, end)` — memory-safe generator yielding classify results
- `numclassify compare <a> <b> [--json]` — new CLI command showing shared/exclusive properties
- Windows ANSI color fix via `SetConsoleMode` VT100 flag
- `py.typed` marker added (PEP 561 compliant)
- Full type hints on all public API functions

## [0.1.1] - 2026-05-06
### Fixed
- cli.py: Fixed imports to use numclassify._core instead of numclassify
- combinatorial.py: Moved `from math import comb` to top-level (was inside loops)
- _registry.py: Fixed find_any_in_range docstring example (removed non-existent duplicate)

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