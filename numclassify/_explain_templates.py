"""
numclassify._explain_templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Template factories that generate explain= callables for common number-type patterns.
Each factory returns a callable (n: int) -> str suitable for the explain= field
in @register.

Templates:
  digit_power_template       -- e.g. Armstrong, Narcissistic, Disarium
  divisor_sum_template       -- e.g. Abundant, Perfect, Deficient
  sequence_membership_template -- e.g. Fibonacci, Lucas, Tribonacci, Pell
  factorization_template     -- e.g. Squarefree, Powerful, Sphenic, Smooth/Rough
"""

from __future__ import annotations
from typing import Callable, Optional, Sequence


def digit_power_template(
    power_fn: Callable[[int], int],
    label: str,
    *,
    pass_msg: Optional[str] = None,
    fail_msg: Optional[str] = None,
) -> Callable[[int], str]:
    """
    For types where n equals the sum of some power applied to each digit.

    power_fn(digit) -> the power contribution of that digit (e.g. d**len(str(n)) or d**pos)
    label: short description used in the explanation string (e.g. "3rd power", "position-based power")
    """
    def _explain(n: int) -> str:
        if n < 0:
            return f"{n} is negative -- not applicable"
        digits = [int(d) for d in str(abs(n))]
        contributions = [power_fn(d) for d in digits]
        total = sum(contributions)
        digit_str = " + ".join(
            f"{d}[{label}]={c}" for d, c in zip(digits, contributions)
        )
        result = "equals" if total == n else "does not equal"
        verdict = "YES" if total == n else "NO"
        return (
            f"{n}: digits={list(digits)}, "
            f"{' + '.join(str(c) for c in contributions)} = {total} "
            f"{result} {n} -> {verdict}"
        )
    return _explain


def divisor_sum_template(
    comparison: str,
    *,
    include_n: bool = False,
) -> Callable[[int], str]:
    """
    For types defined by comparing sigma(n) (sum of proper divisors) to n.

    comparison: one of "equal", "less", "greater"
    include_n: if True, uses sigma(n) including n itself (e.g. for Superperfect)
    """
    def _get_divisors(n: int):
        if n <= 0:
            return []
        divs = set()
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                if i != n or include_n:
                    divs.add(i)
                if n // i != n or include_n:
                    divs.add(n // i)
        return sorted(divs)

    labels = {
        "equal": ("Perfect", "equals", "does not equal"),
        "greater": ("Abundant", "exceeds", "does not exceed"),
        "less": ("Deficient", "is less than", "is not less than"),
    }
    type_label, yes_word, no_word = labels.get(comparison, ("", "equals", "does not equal"))

    def _explain(n: int) -> str:
        if n <= 0:
            return f"{n} <= 0 -- not applicable"
        divs = _get_divisors(n)
        total = sum(divs)
        div_str = " + ".join(str(d) for d in divs) if divs else "0"
        verdict_word = yes_word if (
            (comparison == "equal" and total == n) or
            (comparison == "greater" and total > n) or
            (comparison == "less" and total < n)
        ) else no_word
        verdict = "YES" if (
            (comparison == "equal" and total == n) or
            (comparison == "greater" and total > n) or
            (comparison == "less" and total < n)
        ) else "NO"
        label = "sigma(n) including n" if include_n else "proper divisors"
        return (
            f"{n}: {label} = [{div_str}] = {total}, "
            f"which {verdict_word} {n} -> {verdict}"
        )
    return _explain


def sequence_membership_template(
    sequence_fn: Callable[[int], Sequence[int]],
    seq_name: str,
    *,
    max_terms: int = 30,
) -> Callable[[int], str]:
    """
    For types defined by membership in a named integer sequence.

    sequence_fn(n) -> list/tuple of sequence values up to or including n
    seq_name: human-readable name (e.g. "Fibonacci", "Lucas", "Pell")
    max_terms: how many terms to generate for the lookup
    """
    def _explain(n: int) -> str:
        try:
            terms = list(sequence_fn(n))
        except Exception as e:
            return f"Could not generate {seq_name} sequence: {e}"
        if n in terms:
            idx = terms.index(n)
            nearby = terms[max(0, idx-2):idx+3]
            return (
                f"{n} is the {idx+1}th term of the {seq_name} sequence. "
                f"Nearby terms: {nearby} -> YES"
            )
        else:
            smaller = [t for t in terms if t < n]
            larger = [t for t in terms if t > n]
            prev = smaller[-1] if smaller else None
            nxt = larger[0] if larger else None
            if prev is not None and nxt is not None:
                return (
                    f"{n} is not in the {seq_name} sequence "
                    f"(consecutive terms: {prev}, {nxt}) -> NO"
                )
            elif prev is not None:
                return f"{n} is beyond computed {seq_name} terms (last computed: {prev}) -> NO"
            else:
                return f"{n} is not in the {seq_name} sequence -> NO"
    return _explain


def factorization_template(
    condition_fn: Callable[[list], bool],
    condition_label: str,
    *,
    show_exponents: bool = False,
) -> Callable[[int], str]:
    """
    For types defined by a property of the prime factorization.

    condition_fn(factors) -> bool, where factors is a sorted list with repetition
    condition_label: short description of the condition
    show_exponents: if True, display factorization as p^e notation
    """
    def _prime_factors_with_exp(n: int):
        factors = []
        if n < 2:
            return factors, {}
        d, temp = 2, n
        while d * d <= temp:
            while temp % d == 0:
                factors.append(d)
                temp //= d
            d += 1
        if temp > 1:
            factors.append(temp)
        from collections import Counter
        return factors, dict(Counter(factors))

    def _explain(n: int) -> str:
        if n <= 1:
            return f"{n} <= 1 -- factorization not applicable"
        factors, exp_dict = _prime_factors_with_exp(n)
        if show_exponents:
            fact_str = " x ".join(
                f"{p}^{e}" if e > 1 else str(p)
                for p, e in sorted(exp_dict.items())
            )
        else:
            fact_str = " x ".join(str(f) for f in factors)
        result = condition_fn(factors)
        verdict = "YES" if result else "NO"
        return (
            f"{n} = {fact_str}; condition '{condition_label}' -> {verdict}"
        )
    return _explain
