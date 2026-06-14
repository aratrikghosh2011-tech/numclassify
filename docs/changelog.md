# Changelog

All notable changes to numclassify are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) — [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.4.1] - 2026-06-14

### Fixed
- `is_achilles(1)` now returns `False`. Previously returned `True` because
  `_is_perfect_power(1)` incorrectly returned `False` (1 = 1² is a perfect power).
  First Achilles number is 72, per OEIS A052486.
- `stream(min_score=N)` now filters on `notable_score` instead of raw `score`.
  Previously, figurate inflation caused almost all numbers to pass any threshold.
- `is_spy(0)` now returns `False`. Spy numbers are defined for positive integers only.
- Playground version badge now always shows live installed version from PyPI
  instead of the hardcoded version in the HTML source.
- Fixed `find_any_in_range` and `find_all_in_range` documentation — both functions
  take a list of predicates as the first argument, not just `(lo, hi)`.

---

## [0.4.0] - 2026-06-13

### Fixed
- `classify()` now returns `notable_score` — score excluding figurate and centered-figurate hits. Prevents misleading inflation for n=1 (first member of every polygonal sequence).
- `is_unique(n)` now returns `False` for negative `n`.
- `is_practical(0)` now returns `False`.
- Removed leaked internal names (`Optional`, `_version`, `_PackageNotFoundError`) from `dir(numclassify)`.
- Playground now displays `notable_score` instead of raw score.

### Changed
- Development status updated to `5 - Production/Stable`.

### Added
- `SECURITY.md` with vulnerability reporting instructions.

---

## [0.3.3] - 2026-06-13

### Added
- 8 new exam number types: Strong, Sunny, Buzz, Magic, Fascinating, Trimorphic, Twisted Prime, Unique.
- `classify()` returns a `categories` dict grouping true properties by category.
- `stream()` accepts `min_score` and `has_property` filter parameters.
- `most_special_in_range()` accepts `verbose=True` for progress output.
- `find_any_in_range()` exported to public API.
- Auto-generated crash tests (every registered type tested on 0, 1, 2, −1).

### Fixed
- Infinite loop in `is_sum_of_three_squares(0)`: `while n%4==0` never exits for n=0.
- Dead `else` branch removed from `classify()`.
- Fixed wrong docstring example in `is_leyland_prime`.

---

## [0.3.2.1] - 2026-06-12

### Fixed
- Batch classify rejected comma/space input — changed `type="number"` to `type="text"` with `inputmode="numeric"`.
- Search autocomplete fallback if Pyodide load fails.

### Changed
- MkDocs site theme updated to saffron (#FF9933).

---

## [0.3.2] - 2026-06-12

### Added
- Search autocomplete dropdown.
- Confetti when score > 50.
- Keyboard shortcuts: `C`, `S`, `N`, `?`.
- `prefers-reduced-motion` support.

---

## [0.3.1] - 2026-06-12

### Added
- Version badge on playground (live from installed package).
- Category-colored property tags.
- Batch classify mode.
- Recent history panel (last 20 numbers).
- Property tooltips, fuzzy search, search pagination.
- Number of the Day date picker.
- Light/dark theme toggle.
- Download results as JSON.

---

## [0.3.0] - 2026-06-12

### Added
- Pyodide playground (`docs/playground.html`) — real Python in the browser.
- Auto GitHub Pages deployment on push to main.
- Version sync via `importlib.metadata`.
- PyPI badges in README.

---

## [0.2.1] - 2026-05-11

### Added
- `examples/` folder with 5 runnable scripts.
- `CONTRIBUTING.md`.
- Namespace cleanup.

---

## [0.2.0] - 2026-05

### Added
- OIDC trusted publishing via GitHub Actions.
- MkDocs Material documentation deployed to GitHub Pages.
- `py.typed` marker.
- 60 hand-written tests.

---

## [0.1.0] - 2026-05

Initial release.
