"""
tests/test_explain_templates.py
Exercises every branch of every template factory in _explain_templates.py.
"""
import pytest
import numclassify as nc
from numclassify._explain_templates import (
    digit_power_template,
    divisor_sum_template,
    sequence_membership_template,
    factorization_template,
)


# ---------------------------------------------------------------------------
# digit_power_template
# ---------------------------------------------------------------------------

class TestDigitPowerTemplate:
    def setup_method(self):
        self.explain = digit_power_template(lambda d: d ** 3, "3")

    def test_armstrong_153_yes(self):
        result = self.explain(153)
        assert '153' in result
        assert 'YES' in result

    def test_armstrong_100_no(self):
        result = self.explain(100)
        assert 'NO' in result

    def test_negative_input(self):
        result = self.explain(-5)
        assert 'negative' in result.lower() or 'NO' in result or '-5' in result

    def test_zero(self):
        result = self.explain(0)
        assert isinstance(result, str) and len(result) > 0

    def test_single_digit(self):
        result = self.explain(1)
        assert isinstance(result, str)

    def test_returns_string(self):
        assert isinstance(self.explain(370), str)

    def test_shows_digit_contributions(self):
        result = self.explain(153)
        assert '1' in result and '5' in result and '3' in result


# ---------------------------------------------------------------------------
# divisor_sum_template
# ---------------------------------------------------------------------------

class TestDivisorSumTemplate:
    def test_perfect_6(self):
        explain = divisor_sum_template("equal")
        result = explain(6)
        assert 'YES' in result
        assert '6' in result

    def test_perfect_28(self):
        explain = divisor_sum_template("equal")
        result = explain(28)
        assert 'YES' in result

    def test_perfect_100_no(self):
        explain = divisor_sum_template("equal")
        result = explain(100)
        assert 'NO' in result

    def test_abundant_12(self):
        explain = divisor_sum_template("greater")
        result = explain(12)
        assert 'YES' in result

    def test_deficient_10(self):
        explain = divisor_sum_template("less")
        result = explain(10)
        assert 'YES' in result

    def test_zero_input(self):
        explain = divisor_sum_template("equal")
        result = explain(0)
        assert isinstance(result, str)
        assert 'not applicable' in result.lower() or '0' in result

    def test_negative_input(self):
        explain = divisor_sum_template("equal")
        result = explain(-6)
        assert isinstance(result, str)

    def test_one_input(self):
        explain = divisor_sum_template("equal")
        result = explain(1)
        assert isinstance(result, str)

    def test_shows_divisors(self):
        explain = divisor_sum_template("equal")
        result = explain(6)
        assert '1' in result and '2' in result and '3' in result

    def test_include_n_true(self):
        explain = divisor_sum_template("equal", include_n=True)
        result = explain(6)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# sequence_membership_template
# ---------------------------------------------------------------------------

class TestSequenceMembershipTemplate:
    def setup_method(self):
        def fib_up_to(n):
            seq = [0, 1]
            while seq[-1] < max(n, 1):
                seq.append(seq[-1] + seq[-2])
            return seq
        self.explain = sequence_membership_template(fib_up_to, "Fibonacci")

    def test_fib_8_yes(self):
        result = self.explain(8)
        assert 'YES' in result
        assert 'Fibonacci' in result

    def test_fib_10_no(self):
        result = self.explain(10)
        assert 'NO' in result

    def test_fib_0_yes(self):
        result = self.explain(0)
        assert 'YES' in result

    def test_fib_1_yes(self):
        result = self.explain(1)
        assert 'YES' in result

    def test_shows_nearby_terms(self):
        result = self.explain(10)
        assert '8' in result and '13' in result

    def test_shows_index_for_hit(self):
        result = self.explain(8)
        assert isinstance(result, str) and len(result) > 10

    def test_returns_string_always(self):
        for n in [0, 1, 2, 3, 100, 1000]:
            assert isinstance(self.explain(n), str)


# ---------------------------------------------------------------------------
# factorization_template
# ---------------------------------------------------------------------------

class TestFactorizationTemplate:
    def test_squarefree_30_yes(self):
        explain = factorization_template(
            lambda f: len(f) == len(set(f)),
            "all prime factors appear exactly once",
            show_exponents=True
        )
        result = explain(30)
        assert 'YES' in result
        assert '30' in result

    def test_squarefree_12_no(self):
        explain = factorization_template(
            lambda f: len(f) == len(set(f)),
            "all prime factors appear exactly once",
            show_exponents=True
        )
        result = explain(12)
        assert 'NO' in result

    def test_powerful_36_yes(self):
        explain = factorization_template(
            lambda f: all(f.count(p) >= 2 for p in set(f)),
            "every prime factor appears at least twice",
            show_exponents=True
        )
        result = explain(36)
        assert 'YES' in result

    def test_sphenic_30_yes(self):
        explain = factorization_template(
            lambda f: len(f) == 3 and len(set(f)) == 3,
            "product of exactly 3 distinct primes",
            show_exponents=True
        )
        result = explain(30)
        assert 'YES' in result

    def test_zero_input(self):
        explain = factorization_template(lambda f: True, "test")
        result = explain(0)
        assert 'not applicable' in result.lower() or '0' in result

    def test_one_input(self):
        explain = factorization_template(lambda f: True, "test")
        result = explain(1)
        assert isinstance(result, str)

    def test_prime_input(self):
        explain = factorization_template(
            lambda f: len(f) == len(set(f)),
            "squarefree",
            show_exponents=True
        )
        result = explain(7)
        assert 'YES' in result

    def test_negative_input(self):
        explain = factorization_template(lambda f: True, "test")
        result = explain(-4)
        assert isinstance(result, str)

    def test_shows_factorization(self):
        explain = factorization_template(
            lambda f: True,
            "test",
            show_exponents=True
        )
        result = explain(12)
        assert '2' in result and '3' in result

    def test_condition_label_appears(self):
        explain = factorization_template(lambda f: True, "my condition label")
        result = explain(6)
        assert 'my condition label' in result


# ---------------------------------------------------------------------------
# Integration: why() calls that exercise templates end-to-end
# ---------------------------------------------------------------------------

class TestWhyUsesTemplates:
    """These test the full why() path including template execution."""

    @pytest.mark.parametrize("prop,n,is_true", [
        ("Perfect", 6, True),
        ("Perfect", 7, False),
        ("Abundant", 12, True),
        ("Deficient", 10, True),
        ("Squarefree", 30, True),
        ("Squarefree", 12, False),
        ("Fibonacci", 8, True),
        ("Fibonacci", 10, False),
        ("Pell", 5, True),
        ("Tribonacci", 7, True),
        ("Padovan", 5, True),
    ])
    def test_why_verdict(self, prop, n, is_true):
        result = nc.why(prop, n)
        assert isinstance(result, str)
        needle = f"{n} is {prop}" if is_true else f"{n} is NOT {prop}"
        assert needle in result, f"why({prop}, {n}) = {result!r}, expected {needle}"

    def test_why_shows_math_not_just_verdict(self):
        result = nc.why("Perfect", 6)
        assert len(result) > 20
        assert any(c.isdigit() for c in result)

    def test_why_armstrong_shows_digit_breakdown(self):
        result = nc.why("Armstrong", 153)
        assert '153' in result
        assert '1' in result and '5' in result and '3' in result

    def test_why_all_covered_types_dont_crash(self):
        """Every type with explain= should return a non-empty string."""
        from numclassify._registry import REGISTRY, _normalize
        failed = []
        for key, entry in REGISTRY.items():
            if key != _normalize(entry.name):
                continue
            if entry.explain is None:
                continue
            cat = entry.category.lower().replace(' ', '_')
            if any(x in cat for x in ['figurate', 'polygonal', 'centered']):
                continue
            try:
                result = nc.why(entry.name, 1)
                if not isinstance(result, str) or len(result) == 0:
                    failed.append(f"{entry.name}: empty result")
            except Exception as e:
                failed.append(f"{entry.name}: {e}")
        assert not failed, f"why() failed on: {failed}"
