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
