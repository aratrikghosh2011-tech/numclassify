"""
tests/test_registry.py
~~~~~~~~~~~~~~~~~~~~~~
Full pytest test suite for numclassify.

All tests are self-contained and must pass with no warnings on Python 3.8+.
"""
from __future__ import annotations

import json
import subprocess
import sys

import pytest

# ---------------------------------------------------------------------------
# Imports under test
# ---------------------------------------------------------------------------

import numclassify as nc
from numclassify._registry import (
    REGISTRY,
    NumberType,
    get_all_properties,
    get_true_properties,
    find_in_range,
    register,
)
from numclassify._core.primes import is_prime
from numclassify._core.digital import (
    is_armstrong,
    is_spy,
    is_harshad,
    is_happy,
    is_disarium,
)
from numclassify._core.recreational import is_kaprekar, is_palindrome, is_automorphic
from numclassify._core.divisors import (
    is_perfect, is_abundant, is_deficient, is_squarefree,
    is_powerful, is_sphenic, is_practical,
)
from numclassify._core.sequences import is_fibonacci, is_lucas, is_catalan
from numclassify._core.powers import (
    is_perfect_square, is_perfect_cube, is_taxicab, is_sum_of_two_squares,
)
from numclassify._core.number_theory import (
    is_evil, is_carmichael, is_self_number, is_autobiographical, is_keith,
)
from numclassify._core.combinatorial import is_factorial


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

def test_register_decorator():
    """A function decorated with @register must appear in REGISTRY."""

    @register(name="Test Dummy XYZ", category="test")
    def _dummy(n: int) -> bool:
        return n == 42

    assert "test_dummy_xyz" in REGISTRY
    entry = REGISTRY["test_dummy_xyz"]
    assert isinstance(entry, NumberType)
    assert entry.func(42) is True
    assert entry.func(1) is False


def test_get_all_properties_returns_dict():
    """get_all_properties must return a dict for any integer."""
    result = get_all_properties(6)
    assert isinstance(result, dict)
    assert len(result) > 0


def test_get_true_properties_all_true():
    """Every value in get_true_properties must be True."""
    result = get_true_properties(28)
    assert len(result) > 0
    assert all(v is True for v in result.values())


def test_find_in_range_primes():
    """find_in_range with is_prime must match the known primes up to 20."""
    result = find_in_range(is_prime, 1, 20)
    assert result == [2, 3, 5, 7, 11, 13, 17, 19]


# ---------------------------------------------------------------------------
# is_prime
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 97])
def test_is_prime_true(n: int):
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [1, 4, 6, 9, 15, 561])
def test_is_prime_false(n: int):
    """561 is a Carmichael number — it must be identified as composite."""
    assert is_prime(n) is False


def test_is_prime_large():
    assert is_prime(1_000_000_007) is True
    assert is_prime(1_000_000_006) is False


# ---------------------------------------------------------------------------
# is_armstrong
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n", [153, 370, 371, 407])
def test_is_armstrong_true(n: int):
    assert is_armstrong(n) is True


@pytest.mark.parametrize("n", [100, 200])
def test_is_armstrong_false(n: int):
    assert is_armstrong(n) is False


# ---------------------------------------------------------------------------
# is_spy
# ---------------------------------------------------------------------------

def test_is_spy_true():
    assert is_spy(1124) is True


def test_is_spy_false():
    assert is_spy(124) is False


# ---------------------------------------------------------------------------
# is_harshad
# ---------------------------------------------------------------------------

def test_is_harshad_true():
    assert is_harshad(18) is True


def test_is_harshad_false():
    assert is_harshad(19) is False


# ---------------------------------------------------------------------------
# is_happy
# ---------------------------------------------------------------------------

def test_is_happy_true():
    assert is_happy(19) is True


def test_is_happy_false():
    assert is_happy(4) is False


# ---------------------------------------------------------------------------
# is_disarium
# ---------------------------------------------------------------------------

def test_is_disarium_true():
    assert is_disarium(135) is True


def test_is_disarium_false():
    assert is_disarium(136) is False


# ---------------------------------------------------------------------------
# is_kaprekar
# ---------------------------------------------------------------------------

def test_is_kaprekar_true_45():
    assert is_kaprekar(45) is True


def test_is_kaprekar_true_9():
    assert is_kaprekar(9) is True


def test_is_kaprekar_false_100():
    assert is_kaprekar(100) is False


def test_kaprekar_leading_zero_splits():
    """Kaprekar numbers whose square splits with a leading zero in right part."""
    from numclassify._core.recreational import is_kaprekar
    # 99²=9801 → 98+01=99, 999²=998001 → 998+001=999, 9999²=99980001 → 9998+0001=9999
    assert is_kaprekar(99) is True
    assert is_kaprekar(999) is True
    assert is_kaprekar(9999) is True
    # Standard ones still work
    assert is_kaprekar(45) is True
    assert is_kaprekar(297) is True
    assert is_kaprekar(703) is True
    # Non-Kaprekar
    assert is_kaprekar(100) is False
    assert is_kaprekar(98) is False


# ---------------------------------------------------------------------------
# is_palindrome
# ---------------------------------------------------------------------------

def test_is_palindrome_true():
    assert is_palindrome(121) is True


def test_is_palindrome_false():
    assert is_palindrome(123) is False


# ---------------------------------------------------------------------------
# is_automorphic
# ---------------------------------------------------------------------------

def test_is_automorphic_true():
    assert is_automorphic(5) is True
    assert is_automorphic(6) is True


def test_is_automorphic_false():
    assert is_automorphic(7) is False


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

def test_cli_check_runs():
    """The CLI must exit with code 0 for 'check 153'."""
    result = subprocess.run(
        [sys.executable, "-m", "numclassify", "check", "153"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"CLI exited with {result.returncode}.\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


# ---------------------------------------------------------------------------
# NEW TESTS: divisors
# ---------------------------------------------------------------------------

def test_is_perfect():
    assert is_perfect(6) is True
    assert is_perfect(28) is True
    assert is_perfect(12) is False


def test_is_abundant():
    assert is_abundant(12) is True
    assert is_abundant(8) is False


def test_is_deficient():
    assert is_deficient(8) is True
    assert is_deficient(6) is False


def test_is_squarefree():
    assert is_squarefree(6) is True
    assert is_squarefree(4) is False


def test_is_powerful():
    assert is_powerful(4) is True
    assert is_powerful(6) is False


def test_is_sphenic():
    assert is_sphenic(30) is True   # 2 * 3 * 5
    assert is_sphenic(12) is False


def test_is_practical():
    assert is_practical(12) is True
    assert is_practical(10) is False


# ---------------------------------------------------------------------------
# NEW TESTS: sequences
# ---------------------------------------------------------------------------

def test_is_fibonacci():
    assert is_fibonacci(13) is True
    assert is_fibonacci(14) is False


def test_is_lucas():
    assert is_lucas(7) is True
    assert is_lucas(6) is False


def test_is_catalan():
    assert is_catalan(14) is True
    assert is_catalan(13) is False


# ---------------------------------------------------------------------------
# NEW TESTS: powers
# ---------------------------------------------------------------------------

def test_is_perfect_square():
    assert is_perfect_square(16) is True
    assert is_perfect_square(15) is False


def test_is_perfect_cube():
    assert is_perfect_cube(27) is True
    assert is_perfect_cube(26) is False


def test_is_taxicab():
    assert is_taxicab(1729) is True   # 12^3 + 1^3 = 10^3 + 9^3
    assert is_taxicab(1728) is False


def test_is_sum_of_two_squares():
    assert is_sum_of_two_squares(5) is True   # 1^2 + 2^2
    assert is_sum_of_two_squares(3) is False


# ---------------------------------------------------------------------------
# NEW TESTS: number_theory
# ---------------------------------------------------------------------------

def test_is_evil():
    assert is_evil(9) is True    # 1001 -> two 1-bits (even)
    assert is_evil(7) is False   # 111  -> three 1-bits (odd)


def test_is_carmichael():
    assert is_carmichael(561) is True
    assert is_carmichael(562) is False


def test_is_self_number():
    assert is_self_number(20) is True
    assert is_self_number(21) is False


def test_is_autobiographical():
    assert is_autobiographical(1210) is True
    assert is_autobiographical(1211) is False


def test_is_keith():
    assert is_keith(14) is True
    assert is_keith(15) is False


# ---------------------------------------------------------------------------
# NEW TESTS: combinatorial
# ---------------------------------------------------------------------------

def test_is_factorial():
    assert is_factorial(24) is True
    assert is_factorial(25) is False


# ---------------------------------------------------------------------------
# Auto-generated crash tests — every registered type, 4 inputs
# ---------------------------------------------------------------------------

def _get_all_registered_funcs():
    """Return list of (name, func) for canonical registry entries.

    Samples at most 10 entries from figurate / figurate_centered (since all
    use the same parametric functions) and all entries from other categories.
    """
    from numclassify._registry import REGISTRY, _normalize
    seen = set()
    result = []
    sample = {"figurate", "figurate_centered"}
    sample_count = {cat: 0 for cat in sample}
    max_per_cat = 10
    for key, entry in REGISTRY.items():
        if key == _normalize(entry.name):
            if key not in seen:
                seen.add(key)
                cat = entry.category
                if cat in sample:
                    if sample_count[cat] < max_per_cat:
                        sample_count[cat] += 1
                        result.append((entry.name, entry.func))
                else:
                    result.append((entry.name, entry.func))
    return result


@pytest.mark.parametrize("name,func", _get_all_registered_funcs())
def test_no_crash_on_edge_inputs(name, func):
    """Every registered type must not raise on inputs 0, 1, 2."""
    for n in [0, 1, 2]:
        try:
            result = func(n)
            assert isinstance(result, bool), (
                f"{name}({n}) returned {type(result)}, expected bool"
            )
        except Exception as e:
            pytest.fail(f"{name}({n}) raised {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# v0.4.0 regression tests
# ---------------------------------------------------------------------------

def test_classify_has_notable_score():
    """classify() must include 'notable_score' key."""
    result = nc.classify(7)
    assert "notable_score" in result
    assert isinstance(result["notable_score"], int)
    assert result["notable_score"] <= result["score"]


def test_classify_n1_notable_score_reasonable():
    """n=1 notable_score must be much less than total score (no figurate inflation)."""
    result = nc.classify(1)
    # notable_score excludes figurate and figurate_centered
    assert result["notable_score"] < 100
    # Total score will still be large (mathematically correct)
    assert result["score"] > 1000


def test_is_unique_negative():
    """is_unique must return False for negative integers."""
    from numclassify._core.exam_types import is_unique
    assert is_unique(-5) is False
    assert is_unique(-1) is False
    assert is_unique(-123) is False


def test_is_practical_zero():
    """is_practical(0) must return False."""
    from numclassify._core.divisors import is_practical
    assert is_practical(0) is False


def test_no_leaked_names():
    """Optional, _version, _PackageNotFoundError must not be in dir(nc)."""
    public_names = [n for n in dir(nc) if not n.startswith("__")]
    assert "Optional" not in public_names
    assert "_version" not in public_names
    assert "_PackageNotFoundError" not in public_names


# ---------------------------------------------------------------------------
# v0.4.1 regression tests
# ---------------------------------------------------------------------------


def test_achilles_not_one():
    """1 is not an Achilles number — first is 72."""
    from numclassify._core.divisors import is_achilles
    assert is_achilles(1) is False
    assert is_achilles(72) is True
    assert is_achilles(108) is True


def test_perfect_power_one():
    """1 must be considered a perfect power (1 = 1^2)."""
    from numclassify._core.divisors import _is_perfect_power
    assert _is_perfect_power(1) is True
    assert _is_perfect_power(4) is True
    assert _is_perfect_power(6) is False


def test_stream_min_score_uses_notable():
    """stream min_score must filter on notable_score, not raw score."""
    results = list(nc.stream(1, 10, min_score=40))
    numbers = [r['number'] for r in results]
    assert 4 not in numbers   # notable_score=35
    assert 9 not in numbers   # notable_score=38
    assert 1 in numbers       # notable_score=63
    assert 2 in numbers       # notable_score=63


def test_spy_not_zero():
    """is_spy(0) must return False."""
    from numclassify._core.digital import is_spy
    assert is_spy(0) is False
    assert is_spy(1) is True


# ---------------------------------------------------------------------------
# v0.5.0 — Part A: performance hang regression tests
# ---------------------------------------------------------------------------

import time


def test_semiperfect_large_n_fast():
    times = []
    for _ in range(5):
        start = time.time()
        nc.is_semiperfect(999999999)
        times.append(time.time() - start)
    max_time = max(times)
    assert max_time < 6.0, f"is_semiperfect(999999999) took {max_time:.2f}s"


def test_zumkeller_large_n_fast():
    times = []
    for _ in range(5):
        start = time.time()
        nc.is_zumkeller(999999999)
        times.append(time.time() - start)
    max_time = max(times)
    # CI runners are slower and noisier than local machines.
    # Threshold has 3x margin over observed local max.
    assert max_time < 6.0, f"is_zumkeller(999999999) took {max_time:.2f}s, expected < 6.0s"


def test_weird_large_n_fast():
    times = []
    for _ in range(5):
        start = time.time()
        nc.is_weird(999999999)
        times.append(time.time() - start)
    max_time = max(times)
    assert max_time < 6.0, f"is_weird(999999999) took {max_time:.2f}s"


def test_untouchable_large_n_fast():
    start = time.time()
    nc.is_untouchable(50000)
    assert time.time() - start < 5.0


def test_untouchable_raises_above_ceiling():
    with pytest.raises(ValueError):
        nc.is_untouchable(600_000)


def test_semiperfect_correctness_unchanged():
    for k in [6, 12, 18, 20, 24, 28, 30, 36]:
        assert nc.is_semiperfect(k) is True
    for k in [2, 3, 4, 5, 7, 8, 9, 10, 11]:
        assert nc.is_semiperfect(k) is False


def test_zumkeller_correctness_unchanged():
    for k in [6, 12, 20, 24, 28, 30, 40]:
        assert nc.is_zumkeller(k) is True


# ---------------------------------------------------------------------------
# v0.5.0 — Part B: why / property_info / find tests
# ---------------------------------------------------------------------------


def test_why_true_case():
    result = nc.why("armstrong", 153)
    assert "153" in result
    assert "Armstrong" in result or "armstrong" in result.lower()


def test_why_false_case():
    result = nc.why("perfect", 12)
    assert "NOT" in result


def test_why_unknown_property_raises():
    with pytest.raises(ValueError):
        nc.why("nonexistent_property_xyz", 5)


def test_why_fallback_for_no_explain():
    result = nc.why("heptagonal", 7)
    assert "7" in result


def test_property_info_structure():
    info = nc.property_info("armstrong")
    assert set(info.keys()) == {"name", "description", "category", "oeis", "oeis_url", "examples"}
    assert 153 in info["examples"] or len(info["examples"]) > 0


def test_property_info_unknown_raises():
    with pytest.raises(ValueError):
        nc.property_info("nonexistent_property_xyz")


def test_find_has():
    results = nc.find(1, 1000, has=["harshad", "palindrome"])
    assert all(nc.is_harshad(r) for r in results)
    assert all(nc.is_palindrome(r) for r in results)


def test_find_not_has():
    results = nc.find(1, 500, has=["prime"], not_has=["emirp"])
    emirps = nc.find(1, 500, has=["emirp"])
    assert all(r not in emirps for r in results)


def test_find_any_of():
    results = nc.find(1, 10000, any_of=["perfect", "amicable"])
    assert len(results) > 0


# ---------------------------------------------------------------------------
# v0.5.0 — Part C: exam_type tagging test
# ---------------------------------------------------------------------------


def test_exam_types_category_works():
    from numclassify._registry import get_exam_types
    exam_entries = get_exam_types()
    assert len(exam_entries) == 9
    names = {e.name for e in exam_entries}
    assert "Strong" in names
    assert "Magic" in names
    assert "Composite" in names


# ---------------------------------------------------------------------------
# v0.5.0 — Part J: CLI integration tests
# ---------------------------------------------------------------------------


def test_cli_why_command():
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "-m", "numclassify", "why", "armstrong", "153"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "153" in result.stdout


def test_cli_why_json():
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "-m", "numclassify", "why", "armstrong", "153", "--json"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["number"] == 153


def test_cli_query_command():
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "-m", "numclassify", "query", "1", "100", "--has", "prime", "--json"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)


def test_cli_no_args_shows_footer():
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "-m", "numclassify"],
        capture_output=True, text=True
    )
    assert "github.com" in result.stdout.lower()


def test_cli_info_shows_examples():
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "-m", "numclassify", "info", "armstrong"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "153" in result.stdout or "Example" in result.stdout


# ---------------------------------------------------------------------------
# v0.6.0 tests
# ---------------------------------------------------------------------------

class TestExplainCoverage:
    def test_coverage_above_50_percent(self):
        from numclassify._registry import REGISTRY, _normalize
        has, total = 0, 0
        for key, entry in REGISTRY.items():
            if key != _normalize(entry.name):
                continue
            cat = entry.category.lower().replace(' ', '_')
            if any(x in cat for x in ['figurate', 'polygonal', 'centered']):
                continue
            total += 1
            if entry.explain is not None:
                has += 1
        assert total > 0
        assert has / total >= 0.50, f"Explain coverage {has}/{total} below 50%"

    def test_sequence_explains(self):
        for prop in ['Fibonacci', 'Tribonacci', 'Pell', 'Padovan', 'Perrin']:
            result = nc.why(prop, 1)
            assert isinstance(result, str)
            assert len(result) > 5

    def test_factorization_explains(self):
        for prop in ['Squarefree', 'Powerful', 'Sphenic']:
            result = nc.why(prop, 30)
            assert isinstance(result, str)

    def test_similar_numbers_returns_list(self):
        result = nc.similar_numbers(6, top_k=3)
        assert isinstance(result, list)
        assert len(result) <= 3
        for item in result:
            assert 'number' in item
            assert 'similarity' in item
            assert 'shared_properties' in item
            assert 0 <= item['similarity'] <= 1

    def test_specialness_percentile_range(self):
        pct = nc.specialness_percentile(1729, sample_size=100)
        assert 0 <= pct <= 100

    def test_property_info_oeis_url(self):
        info = nc.property_info('prime')
        assert 'oeis_url' in info
        assert info['oeis_url'].startswith('https://oeis.org/')

    def test_audit_explain_runs(self):
        from pathlib import Path
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, 'tools/audit_explain.py', '--missing-only'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert 'coverage' in result.stdout.lower()
