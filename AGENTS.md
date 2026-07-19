# numclassify — agent guidance

Read this before touching code. Every section below exists because
something broke this exact way at least once.

## Build & install

```bash
pip install -e .                        # editable install (hatchling backend)
pip install hatchling && pip install -e .
```

## Test

```bash
python -m pytest tests/ -v --cov=numclassify --cov-report=term-missing --cov-fail-under=75
```

Coverage gate is **75%** (enforced in CI), current actual is **80%**.
10 test files under `tests/`. `cli.py` is the weakest-covered file at
**58%** — the interactive quiz loop and several argparse branches are
undertested. If you're looking for where to add tests next, start there.

Run tests before claiming anything is fixed. See "Verification discipline"
below — this is not optional advice, it's the single most violated rule
in this project's history.

## Repo health

```bash
python tools/check_repo.py          # full (includes CLI smoke tests)
python tools/check_repo.py --fast   # skip slow smoke tests
python tools/check_repo.py --strict # drift warnings -> hard errors (pre-release)
```

`--strict` exists because `warn()` alone never blocked anything, ever,
even right before a tag. A stale README coverage badge (58% vs actual
80%) sat committed on `main` through three version tags before anyone
caught it, specifically because nothing enforced the warning. Normal
mode stays lenient for day-to-day commits; `--strict` (called by
`release.py` before tagging) escalates the same checks to hard failures.

`check_repo.py` includes a static AST scan (`check_no_broken_imports`)
that verifies every `from numclassify.X import Y` resolves to a real
attribute on X. This exists because `cli.py` imported a function called
`count_divisors` that never existed — masked by a broad `except Exception:`
that silently fell back to an O(n) brute-force loop instead of raising.
Nobody noticed for multiple versions because the fallback "worked," just
slowly. **If you add a broad `except Exception:` around an import, you are
disabling this class of protection for that one call site — make sure the
fallback path is actually correct, not just non-crashing.**

## CLI entry points

- `numclassify` -> `numclassify.cli:main` (pyproject.toml `[project.scripts]`)
- `python -m numclassify` -> `numclassify/__main__.py` -> same

CLI uses **lazy imports** of `numclassify` (inside each `cmd_*` function),
not at module top level. Preserve this pattern in new commands — it keeps
CLI startup fast since the full registry (2140+ types) doesn't need to
import until a command actually runs.

## Architecture

- **`@register(name, category, ...)`** decorator in `_core/*.py` adds to
  `REGISTRY` (flat dict keyed by normalized name).
- Importing `numclassify` imports all `_core/*` submodules, triggering
  `@register` at import time.
- Adding a new `_core/*.py` module? Add its import to `numclassify/__init__.py`,
  or its types will never register.
- `REGISTRY` stores each entry under: normalized name, `func.__name__`,
  and all aliases.
- Module `__getattr__` fallback: any registered type can be called as
  `nc.is_foo(n)` without explicit export.
- Zero external dependencies. Pure Python 3.8+.

## Key modules

| Path | Purpose |
|---|---|
| `numclassify/_registry.py` | `NumberType` dataclass, `REGISTRY`, `@register`, `practice_set()`, `PRACTICE_TYPES`, query helpers |
| `numclassify/__init__.py` | `why()`, `why_hidden()`, `property_info()`, `find()`, `classify()`, `stream()` — public API definition |
| `numclassify/_core/figurate.py` | ~1996 figurate types **auto-generated** via loops `k=3..1000` and `k=21..1000` — don't hand-write |
| `numclassify/_explain_templates.py` | 4 template factories: `digit_power_template`, `divisor_sum_template`, `sequence_membership_template`, `factorization_template` |
| `numclassify/cli.py` | Argparse CLI with 9 commands (`quiz` added in v0.8.0) |
| `tools/scaffold_type.py` | Interactive generator for new type code |
| `tools/generate_docs.py` | Rewrites README's category table, version heading, public API count, and coverage badge from live source + `coverage.json` — never hand-edit these sections |
| `tools/check_repo.py` | 12 checks: BOM, CRLF, mojibake, version consistency, emoji in JS, registry count, API leaks, PRACTICE_TYPES drift, em dash scan, coverage badge freshness, broken imports, CLI smoke |
| `tools/release.py` | Bumps version, regenerates docs, checks changelog entry, runs `check_repo.py --strict` + full test suite, prints git commands. Does not tag or push automatically. |

## Conventions

- Boolean classifiers **must** start with `is_` (e.g. `is_prime`).
- Type hints **required** on all functions.
- Category names are lowercase plural (e.g. `"primes"`, `"digital"`, `"divisors"`).
- `exam_tag=True` groups a type under the "exam_types" pseudo-category
  (ICSE Class 10 syllabus).
- No em dashes in docs/comments/YAML. `check_repo.py` scans for them as a
  warning (not blocking) — CHANGELOG.md and SECURITY.md currently have
  known pre-existing instances, don't let new ones join them.
- `Fraction` arithmetic: never use `Fraction // int`, it silently returns
  a plain `int` and downgrades all subsequent arithmetic on that variable.
  Use `Fraction(numerator_expr, denominator_expr)` explicitly instead. Two
  sites in `_core/sequences.py` (Catalan number generation) hit this —
  it happened to not corrupt output because that specific recurrence
  always divides evenly, but the pattern is a trap for any recurrence
  that doesn't.

## Two verdict conventions exist in explain= strings — know both

Every `explain=` function encodes its YES/NO verdict one of two ways, and
anything that processes explain text (like `why_hidden()`) must handle
both or it will silently leak the answer:

1. **Prefix convention** (most `_core/*.py` functions):
   `"{n} is {Type} because: {reasoning}"` or `"{n} is NOT {Type}: {reasoning}"`
   The verdict is the subject of the sentence.

2. **Suffix convention** (`_explain_templates.py` factories):
   `"{reasoning} -> YES"` / `"{reasoning} -> NO"`
   The verdict is a trailing token.

`why_hidden()` in `__init__.py` strips both. A v0.8.0 bug shipped it only
stripping the suffix convention, leaking the verdict for 12 of 22 practice
types (including Armstrong, Perfect, Prime — the most common ones). Fixed
in v0.8.1 with a fail-loud `RuntimeError` safety net: if the strip can't be
verified safe, it raises instead of returning a possibly-leaking string.
**If you write a new explain= function, run it through `why_hidden()` and
grep the result for the type name before assuming it's safe.**

## Practice/quiz mode

23 types in `PRACTICE_TYPES` (`_registry.py:541`) are available for
`numclassify quiz`. Adding a type there requires:
1. The type must already be registered with a working `explain=`.
2. Run the leak check: `why_hidden(type, n)` for several `n` values, grep
   for `is [NOT] {type_word}` case-insensitively. Zero matches required.
3. `check_repo.py`'s `check_practice_types()` re-verifies this on every run
   but only catches drift after the fact — check it yourself before adding.

`practice_set()` samples from a fixed range (1-200) and guarantees a
roughly balanced YES/NO split per property, because naive random sampling
skews heavily NO for rare properties (e.g. only two Perfect numbers exist
below 200) and lets a student score well by always guessing NO.

## Verification discipline — read this before reporting anything as done

This project has repeatedly had "done" summaries that didn't match what
was actually on `main` when independently re-cloned: phantom commits that
were described but never pushed, a coverage number reported as 79% that
was still 59% in the actual repo, a badge fix that was applied to a local
scratch copy but never committed. None of these were malicious — they were
summaries written before the verification step actually ran, or run
against a stale local checkout instead of a fresh clone.

**Standing rule: before reporting a fix, bug, or feature as complete, run
`git log --oneline -5` and the actual test/check commands against a fresh
`git clone`, not cached local state, and paste the real output.** A
summary claiming a commit hash, a coverage percentage, or a test count is
only as good as the command that produced it. If you can't paste real
output, say what's uncertain rather than asserting it's done.

## Docs

```bash
pip install mkdocs-material
mkdocs gh-deploy --force
```

Deploys via `.github/workflows/docs.yml`, which requires the test job
to pass first (`needs: test`) — a broken commit can no longer redeploy a
broken playground just because it happened to touch a doc file.

## Publishing

Push a `v*` tag -> GitHub Action publishes to PyPI via OIDC trusted
publishing (no token needed, `pypa/gh-action-pypi-publish`).

```bash
pip install hatchling build
python -m build
```

`.github/workflows/publish.yml` requires the test job to pass first
(`needs: test`) before the publish job runs. This exists because a tag
pushed manually (outside `tools/release.py`, e.g. `git tag v0.9.0 && git
push --tags` typed directly) used to ship straight to PyPI with zero
verification. Now any tag, however it was created, gets tested first.

Version is read from `importlib.metadata` at runtime, not hardcoded in
`__init__.py`. Never hardcode a version string anywhere outside
`pyproject.toml` — `check_repo.py` checks for this and will fail if it
finds one.

## Release checklist (what `tools/release.py X.Y.Z` actually does)

1. Validates `X.Y.Z` is proper semver.
2. Checks `CHANGELOG.md` has a `## [X.Y.Z]` entry — **write this first**,
   the script won't invent changelog content for you.
3. Bumps `pyproject.toml`.
4. Updates "What's new" heading in `README.md` and removes stale
   data-version from `docs/playground.html`.
5. Runs `tools/generate_docs.py` (regenerates version heading, API count,
   category table; coverage badge only updates if `coverage.json` exists
   from a prior test run).
6. Runs `pytest --cov-report=json` to produce fresh coverage data.
7. Runs `tools/check_repo.py --strict` — fails loudly on any drift.
8. Runs the full test suite as final confirmation.
9. Prints the exact git commands (add/commit/tag/push) — does not run
   them automatically. You confirm and paste them yourself.

Version bumps are for features or public API changes, not pure bug fixes
or tooling/test-only changes (those still get a normal commit, just no
new tag or `pyproject.toml` bump).
