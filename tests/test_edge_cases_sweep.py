"""
tests/test_edge_cases_sweep.py
Broad sweep: every registered predicate function tested at boundary inputs.
Targets scattered uncovered branches (n=0, n=1, negative n) across
_core/*.py that neither CLI tests nor the explain sweep exercise.
"""
import pytest
from numclassify._registry import REGISTRY, _normalize


def _all_predicate_funcs():
    seen_funcs = set()
    result = []
    for key, entry in REGISTRY.items():
        if key != _normalize(entry.name):
            continue
        if entry.func in seen_funcs:
            continue
        seen_funcs.add(entry.func)
        result.append((entry.name, entry.func))
    return result


class TestBoundaryInputsDontCrash:
    """
    Every registered predicate should handle these boundary values
    without raising an unhandled exception. ValueError is acceptable
    for genuinely out-of-domain inputs; anything else indicates a bug.
    """

    ACCEPTABLE_EXCEPTIONS = (ValueError,)

    @pytest.mark.parametrize("n", [0, 1, -1, 2, -2])
    def test_boundary_value(self, n):
        failed = []
        for name, func in _all_predicate_funcs():
            try:
                func(n)
            except self.ACCEPTABLE_EXCEPTIONS:
                pass
            except Exception as e:
                failed.append(f"{name}({n}): {type(e).__name__}: {e}")
        assert not failed, f"{len(failed)} functions crashed on n={n}:\n" + "\n".join(failed[:40])

    def test_large_input_no_hang(self):
        """
        Regression guard for hang-class bugs fixed in v0.4.0/v0.5.0
        (is_untouchable, is_semiperfect, is_weird, is_zumkeller).
        Untouchable is excluded from this sweep; it has its own dedicated
        performance test and is intentionally slow near its ceiling.
        """
        import time
        SLOW_BY_DESIGN = {'Untouchable'}
        failed = []
        for name, func in _all_predicate_funcs():
            if name in SLOW_BY_DESIGN:
                continue
            start = time.time()
            try:
                func(500000)
            except ValueError:
                continue
            except Exception as e:
                failed.append(f"{name}(500000): {type(e).__name__}: {e}")
                continue
            elapsed = time.time() - start
            if elapsed > 5.0:
                failed.append(f"{name}(500000): took {elapsed:.2f}s (possible hang)")
        assert not failed, f"{len(failed)} functions slow or crashed:\n" + "\n".join(failed[:40])


class TestNoBrokenImports:
    def test_computed_extras_uses_fast_divisor_count(self):
        import time
        from numclassify.cli import _computed_extras

        n = 999999937
        start = time.time()
        result = _computed_extras(n)
        elapsed = time.time() - start

        assert result['num_divisors'] == 2
        assert elapsed < 1.0, f"_computed_extras took {elapsed:.2f}s -- fast path may not be active"

    def test_no_broken_internal_imports(self):
        import ast
        import importlib
        from pathlib import Path

        root = Path(__file__).parent.parent / 'numclassify'
        failures = []

        for path in root.rglob('*.py'):
            if '__pycache__' in str(path):
                continue
            src = path.read_text(encoding='utf-8')
            tree = ast.parse(src, filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom) or not node.module:
                    continue
                module_name = node.module
                if node.level > 0 and not module_name.startswith('numclassify'):
                    module_name = f"numclassify.{module_name}"
                if not module_name.startswith('numclassify'):
                    continue
                for alias in node.names:
                    if alias.name == '*':
                        continue
                    try:
                        mod = importlib.import_module(module_name)
                        if not hasattr(mod, alias.name):
                            failures.append(
                                f"{path.relative_to(root.parent)}:{node.lineno}: "
                                f"'{alias.name}' not found in '{module_name}'"
                            )
                    except ImportError:
                        pass

        assert not failures, "Broken internal imports found:\n" + "\n".join(failures)


class TestCatalanFractionPrecision:
    def test_catalan_sequence_correct(self):
        from numclassify._core.sequences import _gen_catalan
        result = sorted(_gen_catalan())
        expected = [1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012]
        assert result[:len(expected)] == expected

    def test_catalan_why_true_case(self):
        import numclassify as nc
        result = nc.why("Catalan", 42)
        assert '42' in result

    def test_catalan_why_false_case(self):
        import numclassify as nc
        result = nc.why("Catalan", 43)
        assert '43' in result

    def test_catalan_larger_values_still_exact(self):
        from numclassify._core.sequences import _gen_catalan
        result = sorted(_gen_catalan())
        assert 742900 in result
        assert 2674440 in result or max(result) < 2674440
