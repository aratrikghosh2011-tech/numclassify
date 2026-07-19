# numclassify — agent guidance

## Build & install

```bash
pip install -e .                        # editable install (hatchling backend)
pip install hatchling && pip install -e .
```

## Test

```bash
python -m pytest tests/ -v --cov=numclassify --cov-report=term-missing --cov-fail-under=75
```

Coverage gate is **75%** (enforced in CI). 9 test files under `tests/`.

## Repo health

```bash
python tools/check_repo.py          # full (includes CLI smoke tests)
python tools/check_repo.py --fast   # skip slow smoke tests
python tools/check_repo.py --strict # drift warnings → errors (pre-release)
```

## CLI entry points

- `numclassify` → `numclassify.cli:main` (pyproject.toml `[project.scripts]`)
- `python -m numclassify` → `numclassify/__main__.py` → same

CLI uses **lazy imports** of `numclassify` (inside each `cmd_*` function).

## Architecture

- **`@register(name, category, ...)`** decorator in `_core/*.py` adds to `REGISTRY` (flat dict keyed by normalized name).
- Importing `numclassify` imports all `_core/*` submodules, triggering `@register` at import time.
- Adding a new `_core/*.py` module? Add its import to `numclassify/__init__.py`.
- `REGISTRY` stores each entry under: normalized name, `func.__name__`, and all aliases.
- Module `__getattr__` fallback: any registered type can be called as `nc.is_foo(n)` without explicit export.
- Zero external dependencies. Pure Python 3.8+.

## Key modules

| Path | Purpose |
|---|---|
| `numclassify/_registry.py` | `NumberType` dataclass, `REGISTRY`, `@register`, query helpers |
| `numclassify/_core/figurate.py` | ~1003 polygonal types **auto-generated** via loop `k=3..1005` — don't hand-write |
| `numclassify/_explain_templates.py` | Template factories for `explain=` field |
| `numclassify/cli.py` | Argparse CLI with 8 commands |
| `tools/scaffold_type.py` | Interactive generator for new type code |
| `tools/generate_docs.py` | Updates README badges, category table, version |

## Conventions

- Boolean classifiers **must** start with `is_` (e.g. `is_prime`).
- Type hints **required** on all functions.
- Category names are lowercase plural (e.g. `"primes"`, `"digital"`, `"divisors"`).
- `exam_tag=True` groups a type under the "exam_types" pseudo-category (ICSE Class 10 syllabus).
- `why_hidden()` strips the verdict from explanations for quiz mode — when adding explain templates, make sure `why_hidden()` can safely strip the verdict.

## Practice/quiz mode

Only 23 types in `PRACTICE_TYPES` (`_registry.py:541`) are available for `numclassify quiz`. Adding a type there requires ensuring no verdict-leaks in `why_hidden()`.

## Docs

```bash
pip install mkdocs-material
mkdocs gh-deploy --force
```

## Publishing

Push a `v*` tag → GitHub Action publishes to PyPI via OIDC trusted publishing (no token needed, `pypa/gh-action-pypi-publish`).

```bash
pip install hatchling build
python -m build
```

Version is read from `importlib.metadata` at runtime, not hardcoded in `__init__.py`.
