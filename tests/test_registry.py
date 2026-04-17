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
    # 1+1+2+4=8  and  1*1*2*4=8
    assert is_spy(1124) is True


def test_is_spy_false():
    # 1+2+3=6, 1*2*3=6 — actually True; use 124: sum=7, product=8
    assert is_spy(124) is False


# ---------------------------------------------------------------------------
# is_harshad
# ---------------------------------------------------------------------------

def test_is_harshad_true():
    assert is_harshad(18) is True   # digit_sum=9, 18%9==0


def test_is_harshad_false():
    assert is_harshad(19) is False  # digit_sum=10, 19%10!=0


# ---------------------------------------------------------------------------
# is_happy
# ---------------------------------------------------------------------------

def test_is_happy_true():
    assert is_happy(19) is True


def test_is_happy_false():
    assert is_happy(4) is False   # enters cycle through 4


# ---------------------------------------------------------------------------
# is_disarium
# ---------------------------------------------------------------------------

def test_is_disarium_true():
    # 1^1 + 3^2 + 5^3 = 1 + 9 + 125 = 135
    assert is_disarium(135) is True


def test_is_disarium_false():
    assert is_disarium(136) is False


# ---------------------------------------------------------------------------
# is_kaprekar
# ---------------------------------------------------------------------------

def test_is_kaprekar_true_45():
    # 45²=2025; (20, 25) → 20+25=45
    assert is_kaprekar(45) is True


def test_is_kaprekar_true_9():
    # 9²=81; (8, 1) → 8+1=9
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
    assert is_automorphic(5) is True   # 5²=25 ends in 5
    assert is_automorphic(6) is True   # 6²=36 ends in 6


def test_is_automorphic_false():
    assert is_automorphic(7) is False  # 7²=49 does not end in 7


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
