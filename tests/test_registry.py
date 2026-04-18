"""
tests/test_registry.py
~~~~~~~~~~~~~~~~~~~~~~
Full pytest test suite for numclassify.

All tests are self-contained and must pass with no warnings on Python 3.8+.
"""
from __future__ import annotations

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
