# Changelog

All notable changes to numclassify are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) — [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.6.0] - 2026-06-27

### Added
- `similar_numbers(n, top_k=5)` — returns integers most similar to n by Jaccard index on shared handcrafted properties
- `specialness_percentile(n, sample_size=1000)` — percentile rank of n's notable_score vs a random sample
- `property_info()` now returns `oeis_url` field (e.g. `"https://oeis.org/A000040"`)
- `_explain_templates.py` rewritten with 4 production-ready template factories: `digit_power_template`, `divisor_sum_template`, `sequence_membership_template`, `factorization_template`
- Explain coverage expanded: 33/139 → 116/139 handcrafted types (83.5%)
- `tools/audit_explain.py` — shows explain= coverage per category with `--missing-only` and `--covered-only` flags
- `tools/generate_docs.py` — reads REGISTRY, auto-writes category count table into docs and README between marker comments
- `tools/scaffold_type.py` — interactive stub generator for new number types; outputs ready-to-paste `@register` block
- `tools/release.py` — single-command release automation (version bump, changelog update, git tag)

### Changed
- Public API: 20 → 22 names (added `similar_numbers`, `specialness_percentile`)

---

## [0.5.0] - 2026-06-19

### Added
- `why(property, n)` — step-by-step explanation engine with dedicated explain functions for 33 high-value types
- `property_info(name)` — registry metadata lookup with auto-generated examples
- `find(start, end, has, not_has, any_of)` — multi-property range query wrapper
- `get_exam_types()` — returns all 8 exam-tagged NumberType entries
- `exam_tag` field on `NumberType` dataclass
- CLI `why <type> <n> [--json]` command
- CLI `query <start> <end> [--has ...] [--not-has ...] [--any-of ...] [--json]` command
- CLI no-args footer showing GitHub and docs links
- CLI `info` command now shows real computed examples via `property_info()`
- `PERFORMANCE.md` with before/after benchmark numbers for hang fixes
- `ARCHITECTURE.md` explaining the registry pattern
- README origin story section and `why()` above the fold
- 5-file playground split: `playground-base.css`, `playground-guide.css`, `playground-core.js`, `playground-tabs.js`, `playground-guide.js`
- Playground "Why" tab with step-by-step explanation UI
- Byte robot guide character with animations (walk-in, wave, idle, celebrate, loader)
- 69% line coverage, 251 tests

### Fixed
- Performance hangs in `is_untouchable` (500k sieve ceiling), `is_semiperfect`, `is_weird`, `is_zumkeller` (bitmask subset-sum DP)
- Exam types category tagging: `numclassify list --category exam_types` now returns all 8 types correctly

---

## [0.4.3] - 2026-06-16

### Fixed
- PyPI README now shows `Harshad` instead of `Zeisel` in the 1729 example

---

## [0.4.2] - 2026-06-15

### Fixed
- `is_kaprekar(99)`, `is_kaprekar(999)`, `is_kaprekar(9999)` now return `True`
  The right-part leading-zero string check was too strict — only the integer value
  needs to be nonzero, not the string representation. OEIS A006886 includes all three.
- Docs category counts corrected throughout to 2140+ (was incorrectly stated as 3000+)

---

## [0.4.1] - 2026-06-14

### Fixed
- `is_achilles(1)` now returns `False`. First Achilles number is 72 per OEIS A052486.
- `stream(min_score=N)` now filters on `notable_score` instead of raw score. Previously figurate inflation caused almost all numbers to pass any threshold.
- `is_spy(0)` now returns `False`. Spy numbers are defined for positive integers only.
- Playground version badge now reads live from installed package instead of hardcoded HTML.
- Fixed `find_any_in_range` and `find_all_in_range` documentation.

---

## [0.4.0] - 2026-06-13

### Added
- `SECURITY.md` with vulnerability reporting instructions.

### Changed
- Development status updated to `5 - Production/Stable`.

### Fixed
- `classify()` now returns `notable_score` field — score excluding figurate/centered-figurate hits.
- `is_unique(n)` now returns `False` for negative `n`.
- `is_practical(0)` now returns `False`.
- Removed leaked internal names (`Optional`, `_version`, `_PackageNotFoundError`) from `dir(numclassify)`.
- Playground now displays `notable_score` instead of raw score.

---

## [0.3.3] - 2026-06-13

### Added
- 8 new exam number types in `numclassify/_core/exam_types.py`: Strong, Sunny, Buzz, Magic, Fascinating, Trimorphic, Twisted Prime, Unique
- `classify()` now returns a `categories` dict grouping true properties by category
- `classify()` true_properties list now sorted by category then name
- `stream()` accepts `min_score` and `has_property` filter parameters
- `most_special_in_range()` accepts `verbose=True` for progress output
- `find_any_in_range()` exported to public API
- Auto-generated crash tests (every registered type tested on 0, 1, 2, −1)

### Fixed
- Infinite loop in `is_sum_of_three_squares(0)`
- Dead `else` branch removed from `classify()`
- Fixed wrong docstring example in `is_leyland_prime`

---

## [0.3.2.1] - 2026-06-12

### Fixed
- Batch classify rejected comma/space input — changed `type="number"` to `type="text"` with `inputmode="numeric"`
- Search autocomplete fallback if Pyodide load fails

### Changed
- MkDocs site theme updated to saffron (#FF9933)

---

## [0.3.2] - 2026-06-12

### Added
- Search autocomplete dropdown
- Confetti burst when score > 50 properties
- Keyboard shortcuts: `C`, `S`, `N`, `?`/`H`
- `prefers-reduced-motion` support

---

## [0.3.1] - 2026-06-12

### Added
- Version badge on playground (live from installed package)
- Category-colored property tags
- Batch classify mode
- Recent history panel (last 20 numbers, localStorage)
- Property tooltips, fuzzy search ("Did you mean X?"), search pagination
- Number of the Day date picker
- Light/dark theme toggle
- Download results as JSON
- Scroll-to-top button, keyboard shortcut hints

### Changed
- Playground split into 3 files: HTML, CSS (~1000 lines), JS (~660 lines)
- Tab switching, result reveal, score counter, number digits, tags, search results: all animated
- Click ripple effect on buttons
- Toast slides in from right

---

## [0.3.0] - 2026-06-12

### Added
- Pyodide playground (`docs/playground.html`) — real Python in the browser
- Classifier, property search, number comparison, random number, Number of the Day
- Shareable URLs via `?n=<number>`
- Copy results to clipboard
- Auto-deploy GitHub Pages on push to main and version tags
- Version read from `importlib.metadata` (single source of truth)
- PyPI version and downloads badges in README

---

## [0.2.1] - 2026-05-11

### Added
- `examples/` folder with 5 runnable scripts
- `CONTRIBUTING.md`
- Namespace cleanup — internal names removed from public `dir()`

---

## [0.2.0] - 2026-05-11

### Added
- `classify(n)` — returns `{number, score, true_properties, categories}`
- `classify_batch(numbers)` — classify a list in one call
- `random_number(max_n=10000)` — classify a random number
- `find_by_property(start, end, **filters)` — query numbers by property
- `stream(start, end)` — memory-safe generator
- CLI `compare <a> <b> [--json]` command
- Windows ANSI color fix via `SetConsoleMode` VT100 flag
- `py.typed` marker (PEP 561)
- Full type hints on all public API functions
- MkDocs Material documentation deployed to GitHub Pages
- OIDC trusted publishing via GitHub Actions (no stored API tokens)
- 60 hand-written tests

---

## [0.1.1] - 2026-05-06

### Fixed
- `cli.py`: fixed imports to use `numclassify._core` instead of `numclassify`
- `combinatorial.py`: moved `from math import comb` to module level
- `_registry.py`: fixed `find_any_in_range` docstring example

---

## [0.1.0] - 2026-04-18

### Added
- Complete package with `@register` decorator plugin architecture
- 2140+ number types across 10 categories, zero external dependencies, Python 3.8–3.13
- Figurate engine: auto-registers ~1003 polygonal + ~998 centered polygonal types (one parametric generator each)
- 41 prime family types with OEIS references
- 10 digital invariant types
- 27 divisor-based types
- 15 sequence types
- 13 power types
- 14 number theory types
- 10 combinatorial types
- 5 recreational types
- CLI: `check`, `find`, `range`, `list`, `info` commands (5 total)
- GitHub Actions CI across Python 3.8–3.13
- PyPI publish via OIDC trusted publishing
