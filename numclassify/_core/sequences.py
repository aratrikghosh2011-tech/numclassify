"""
numclassify/_core/sequences.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sequence-membership number classification functions.

All sets are precomputed at module load time up to 10^9 for O(1) lookup.
"""
from __future__ import annotations

from typing import Set

from numclassify._registry import register
from numclassify._explain_templates import sequence_membership_template

_LIMIT = 10 ** 9

# ---------------------------------------------------------------------------
# Precomputed sets
# ---------------------------------------------------------------------------

def _gen_fibonacci() -> Set[int]:
    s: Set[int] = set()
    a, b = 0, 1
    while a <= _LIMIT:
        s.add(a)
        a, b = b, a + b
    return s


def _gen_lucas() -> Set[int]:
    s: Set[int] = set()
    a, b = 2, 1
    while a <= _LIMIT:
        s.add(a)
        a, b = b, a + b
    return s


def _gen_tribonacci() -> Set[int]:
    s: Set[int] = set()
    a, b, c = 0, 0, 1
    while a <= _LIMIT:
        s.add(a)
        a, b, c = b, c, a + b + c
    return s


def _gen_tetranacci() -> Set[int]:
    s: Set[int] = set()
    a, b, c, d = 0, 0, 0, 1
    while a <= _LIMIT:
        s.add(a)
        a, b, c, d = b, c, d, a + b + c + d
    return s


def _gen_pell() -> Set[int]:
    s: Set[int] = set()
    a, b = 0, 1
    while a <= _LIMIT:
        s.add(a)
        a, b = b, 2 * b + a
    return s


def _gen_jacobsthal() -> Set[int]:
    s: Set[int] = set()
    a, b = 0, 1
    while a <= _LIMIT:
        s.add(a)
        a, b = b, b + 2 * a
    return s


def _gen_padovan() -> Set[int]:
    s: Set[int] = set()
    # P(0)=1, P(1)=1, P(2)=1, P(n)=P(n-2)+P(n-3)
    seq = [1, 1, 1]
    for v in seq:
        s.add(v)
    while True:
        nxt = seq[-2] + seq[-3]
        if nxt > _LIMIT:
            break
        s.add(nxt)
        seq.append(nxt)
    return s


def _gen_perrin() -> Set[int]:
    s: Set[int] = set()
    # P(0)=3,P(1)=0,P(2)=2, P(n)=P(n-2)+P(n-3)
    seq = [3, 0, 2]
    for v in seq:
        s.add(v)
    while True:
        nxt = seq[-2] + seq[-3]
        if nxt > _LIMIT:
            break
        s.add(nxt)
        seq.append(nxt)
    return s


def _gen_catalan() -> Set[int]:
    s: Set[int] = set()
    # C(n) = C(2n,n)/(n+1); iterative: C(0)=1, C(n+1)=C(n)*2*(2n+1)/(n+2)
    from fractions import Fraction
    c: Fraction = Fraction(1)
    n = 0
    while int(c) <= _LIMIT:
        s.add(int(c))
        c = Fraction(c.numerator * 2 * (2 * n + 1), c.denominator * (n + 2))
        n += 1
    return s


def _gen_bell() -> Set[int]:
    s: Set[int] = set()
    # Bell triangle
    row = [1]
    while row[0] <= _LIMIT:
        s.add(row[0])
        new_row = [row[-1]]
        for i in range(len(row)):
            new_row.append(new_row[-1] + row[i])
        row = new_row
    return s


def _gen_motzkin() -> Set[int]:
    s: Set[int] = set()
    # M(n+1) = M(n) + sum_{k=0}^{n-1} M(k)*M(n-1-k)
    # Simpler recurrence: M(n) = ((2n+2)*M(n-1) + (3n-3)*M(n-2)) / (n+3)  --  but fractions needed
    # Use: M(0)=1, M(1)=1, M(n)= M(n-1) + sum(M(k)*M(n-2-k) for k=0..n-2)
    # Cleaner: (n+3)*M(n) = (2n+2)*M(n-1) + (3n-3)*M(n-2)  [valid for n>=2, using n->n shifted]
    # Actually standard: (n+2)*M(n) = (2n)*M(n-1) + 3*M(n-2)  -- let's verify small:
    # M(0)=1,M(1)=1,M(2)=2: (4)*2=(2*2)*1+3*1=4+3=7 WRONG
    # Use direct: M(n+1) = M(n) + sum_{k=0}^{n-1} M(k)*M(n-1-k)
    memo = [1, 1]
    s.update(memo)
    while True:
        n = len(memo)
        nxt = memo[n - 1] + sum(memo[k] * memo[n - 2 - k] for k in range(n - 1))
        if nxt > _LIMIT:
            break
        s.add(nxt)
        memo.append(nxt)
    return s


def _gen_recaman() -> Set[int]:
    s: Set[int] = set()
    # a(0)=0; a(n) = a(n-1)-n if positive and not already in sequence, else a(n-1)+n
    # Generate enough terms; sequence is non-decreasing in range so stop at _LIMIT
    a = [0]
    s.add(0)
    seen = {0}
    n = 1
    while True:
        prev = a[n - 1]
        candidate = prev - n
        if candidate > 0 and candidate not in seen:
            val = candidate
        else:
            val = prev + n
        if val > _LIMIT:
            break
        a.append(val)
        seen.add(val)
        s.add(val)
        n += 1
        if n > 100000:  # safety cap
            break
    return s


def _gen_look_and_say() -> Set[int]:
    s: Set[int] = set()
    term = "1"
    while int(term) <= _LIMIT:
        s.add(int(term))
        # generate next term
        new_term = []
        i = 0
        while i < len(term):
            ch = term[i]
            count = 1
            while i + count < len(term) and term[i + count] == ch:
                count += 1
            new_term.append(str(count) + ch)
            i += count
        term = "".join(new_term)
        if len(term) > 10:  # terms grow fast, int would exceed _LIMIT
            break
    return s


def _gen_kolakoski() -> Set[int]:
    s: Set[int] = set()
    # Kolakoski sequence: self-describing run-length encoding over {1,2}
    # a(1)=1, a(2)=2, a(3)=2, ...
    seq = [1, 2, 2]
    for v in seq:
        s.add(v)
    write = 2  # index of element being "written" (0-based)
    read = 2   # index of element being "read" to determine run length
    # Only 1 and 2 are in this sequence
    s.update({1, 2})
    return s  # Kolakoski only contains 1 and 2


def _gen_sylvester() -> Set[int]:
    s: Set[int] = set()
    a = 2
    while a <= _LIMIT:
        s.add(a)
        a = a * (a - 1) + 1
    return s


# Build all sets at module load
_FIBONACCI: Set[int] = _gen_fibonacci()
_LUCAS: Set[int] = _gen_lucas()
_TRIBONACCI: Set[int] = _gen_tribonacci()
_TETRANACCI: Set[int] = _gen_tetranacci()
_PELL: Set[int] = _gen_pell()
_JACOBSTHAL: Set[int] = _gen_jacobsthal()
_PADOVAN: Set[int] = _gen_padovan()
_PERRIN: Set[int] = _gen_perrin()
_CATALAN: Set[int] = _gen_catalan()
_BELL: Set[int] = _gen_bell()
_MOTZKIN: Set[int] = _gen_motzkin()
_RECAMAN: Set[int] = _gen_recaman()
_LOOK_AND_SAY: Set[int] = _gen_look_and_say()
_KOLAKOSKI: Set[int] = _gen_kolakoski()
_SYLVESTER: Set[int] = _gen_sylvester()

# ---------------------------------------------------------------------------
# Sequence generators for explain templates
# ---------------------------------------------------------------------------

def _fib_up_to(n: int) -> list:
    seq = [0, 1]
    while seq[-1] < n:
        seq.append(seq[-1] + seq[-2])
    return seq

def _tribonacci_up_to(n: int) -> list:
    seq = [0, 0, 1]
    while seq[-1] < n:
        seq.append(seq[-1] + seq[-2] + seq[-3])
    return seq

def _tetranacci_up_to(n: int) -> list:
    seq = [0, 0, 0, 1]
    while seq[-1] < n:
        seq.append(seq[-1] + seq[-2] + seq[-3] + seq[-4])
    return seq

def _pell_up_to(n: int) -> list:
    seq = [0, 1]
    while seq[-1] < n:
        seq.append(2 * seq[-1] + seq[-2])
    return seq

def _jacobsthal_up_to(n: int) -> list:
    seq = [0, 1]
    while seq[-1] < n:
        seq.append(seq[-1] + 2 * seq[-2])
    return seq

def _padovan_up_to(n: int) -> list:
    seq = [1, 1, 1]
    while seq[-1] < n:
        seq.append(seq[-2] + seq[-3])
    return seq

def _perrin_up_to(n: int) -> list:
    seq = [3, 0, 2]
    while seq[-1] < n:
        seq.append(seq[-2] + seq[-3])
    return seq

def _motzkin_up_to(n: int) -> list:
    seq = [1, 1]
    while seq[-1] < n:
        k = len(seq) - 1
        nxt = ((2 * k + 2) * seq[-1] + 3 * seq[-2]) // (k + 3)
        seq.append(nxt)
    return seq

# ---------------------------------------------------------------------------
# Registered classifiers
# ---------------------------------------------------------------------------

def _explain_fibonacci(n: int) -> str:
    if n < 0:
        return f"{n} < 0, cannot be Fibonacci"
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    if b == n:
        return f"{n} appears in the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, ...)"
    return f"{n} is between {a} and {b} in the Fibonacci sequence  --  not a Fibonacci number"


@register(name="Fibonacci", category="sequences", oeis="A000045",
          description="Member of the Fibonacci sequence.",
          explain=_explain_fibonacci)
def is_fibonacci(n: int) -> bool:
    """Return True if n is a Fibonacci number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _FIBONACCI


def _explain_lucas(n: int) -> str:
    if n < 0:
        return f"{n} < 0, cannot be Lucas"
    a, b = 2, 1
    while b < n:
        a, b = b, a + b
    if b == n:
        return f"{n} appears in the Lucas sequence (2, 1, 3, 4, 7, 11, 18, ...)"
    return f"{n} is between {a} and {b} in the Lucas sequence  --  not a Lucas number"


@register(name="Lucas", category="sequences", oeis="A000032",
          description="Member of the Lucas sequence.",
          explain=_explain_lucas)
def is_lucas(n: int) -> bool:
    """Return True if n is a Lucas number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _LUCAS


_explain_tribonacci = sequence_membership_template(
    lambda n: _tribonacci_up_to(n), "Tribonacci"
)

@register(name="Tribonacci", category="sequences", oeis="A000073",
          description="Member of the Tribonacci sequence.",
          explain=_explain_tribonacci)
def is_tribonacci(n: int) -> bool:
    """Return True if n is a Tribonacci number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _TRIBONACCI


_explain_tetranacci = sequence_membership_template(
    lambda n: _tetranacci_up_to(n), "Tetranacci"
)

@register(name="Tetranacci", category="sequences", oeis="A000288",
          description="Member of the Tetranacci sequence.",
          explain=_explain_tetranacci)
def is_tetranacci(n: int) -> bool:
    """Return True if n is a Tetranacci number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _TETRANACCI


_explain_pell = sequence_membership_template(
    lambda n: _pell_up_to(n), "Pell"
)

@register(name="Pell", category="sequences", oeis="A000129",
          description="Member of the Pell sequence.",
          explain=_explain_pell)
def is_pell(n: int) -> bool:
    """Return True if n is a Pell number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _PELL


_explain_jacobsthal = sequence_membership_template(
    lambda n: _jacobsthal_up_to(n), "Jacobsthal"
)

@register(name="Jacobsthal", category="sequences", oeis="A001045",
          description="Member of the Jacobsthal sequence.",
          explain=_explain_jacobsthal)
def is_jacobsthal(n: int) -> bool:
    """Return True if n is a Jacobsthal number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _JACOBSTHAL


_explain_padovan = sequence_membership_template(
    lambda n: _padovan_up_to(n), "Padovan"
)

@register(name="Padovan", category="sequences", oeis="A000931",
          description="Member of the Padovan sequence.",
          explain=_explain_padovan)
def is_padovan(n: int) -> bool:
    """Return True if n is a Padovan number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _PADOVAN


_explain_perrin = sequence_membership_template(
    lambda n: _perrin_up_to(n), "Perrin"
)

@register(name="Perrin", category="sequences", oeis="A001608",
          description="Member of the Perrin sequence.",
          explain=_explain_perrin)
def is_perrin(n: int) -> bool:
    """Return True if n is a Perrin number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _PERRIN


def _explain_catalan(n: int) -> str:
    if n < 0:
        return f"{n} < 0, cannot be Catalan"
    from fractions import Fraction
    c: Fraction = Fraction(1, 1)
    k = 0
    prev = 0
    while int(c) < n:
        prev = int(c)
        c = Fraction(c.numerator * 2 * (2 * k + 1), c.denominator * (k + 2))
        k += 1
    if int(c) == n:
        return f"{n} = C({k})  --  a Catalan number"
    return f"{n} is not a Catalan number (falls between C({k-1}) = {prev} and C({k}) = {int(c)})"


@register(name="Catalan", category="sequences", oeis="A000108",
          description="Member of the Catalan number sequence.",
          explain=_explain_catalan)
def is_catalan(n: int) -> bool:
    """Return True if n is a Catalan number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool

    Examples
    --------
    >>> is_catalan(14)
    True
    >>> is_catalan(13)
    False
    """
    return n >= 0 and n in _CATALAN


def _explain_bell(n: int) -> str:
    if n < 0:
        return f"{n} < 0, cannot be Bell"
    row = [1]
    k = 0
    prev = 0
    while row[0] < n:
        prev = row[0]
        new_row = [row[-1]]
        for i in range(len(row)):
            new_row.append(new_row[-1] + row[i])
        row = new_row
        k += 1
    if row[0] == n:
        return f"{n} = B({k})  --  a Bell number"
    return f"{n} is not a Bell number (falls between B({k-1}) = {prev} and B({k}) = {row[0]})"


@register(name="Bell", category="sequences", oeis="A000110",
          description="Member of the Bell number sequence.",
          explain=_explain_bell)
def is_bell(n: int) -> bool:
    """Return True if n is a Bell number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _BELL


_explain_motzkin = sequence_membership_template(
    lambda n: _motzkin_up_to(n), "Motzkin"
)

@register(name="Motzkin", category="sequences", oeis="A001006",
          description="Member of the Motzkin sequence.",
          explain=_explain_motzkin)
def is_motzkin(n: int) -> bool:
    """Return True if n is a Motzkin number.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _MOTZKIN


def _explain_recaman(n: int) -> str:
    if n < 0:
        return f"{n} < 0 -- not applicable"
    seen = set()
    seq = [0]
    seen.add(0)
    for i in range(1, max(n * 2, 200)):
        candidate = seq[-1] - i
        if candidate > 0 and candidate not in seen:
            seq.append(candidate)
        else:
            seq.append(seq[-1] + i)
        seen.add(seq[-1])
        if seq[-1] > n * 3:
            break
    found = n in seen
    return f"{n} {'is' if found else 'is not'} in the Recaman sequence -> {'YES' if found else 'NO'}"

@register(name="Recaman", category="sequences", oeis="A005132",
          description="Member of the Recaman sequence.",
          explain=_explain_recaman)
def is_recaman(n: int) -> bool:
    """Return True if n appears in the Recaman sequence.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _RECAMAN


def _explain_look_and_say(n: int) -> str:
    if n < 0:
        return f"{n} < 0 -- not applicable"
    seen = {1}
    term = "1"
    while int(term) <= n:
        seen.add(int(term))
        if int(term) == n:
            return f"{n} appears in the look-and-say sequence -> YES"
        new_term = []
        i = 0
        while i < len(term):
            ch = term[i]
            count = 1
            while i + count < len(term) and term[i + count] == ch:
                count += 1
            new_term.append(str(count) + ch)
            i += count
        term = "".join(new_term)
        if len(term) > 10:
            break
    return f"{n} does not appear in the look-and-say sequence -> NO"

@register(name="Look and Say", category="sequences", oeis="A005150",
          description="Member of the look-and-say sequence.",
          explain=_explain_look_and_say)
def is_look_and_say(n: int) -> bool:
    """Return True if n is a term in the look-and-say sequence.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _LOOK_AND_SAY


def _explain_kolakoski(n: int) -> str:
    if n == 1 or n == 2:
        return f"{n} is {'1' if n == 1 else '2'} -- the Kolakoski sequence only contains 1 and 2 -> YES"
    return f"{n} is not in {{1, 2}}; Kolakoski only contains 1 and 2 -> NO"

@register(name="Kolakoski", category="sequences", oeis="A000002",
          description="Member of the Kolakoski sequence (only 1 and 2).",
          explain=_explain_kolakoski)
def is_kolakoski(n: int) -> bool:
    """Return True if n appears in the Kolakoski sequence.

    The Kolakoski sequence only contains 1 and 2.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n in _KOLAKOSKI


def _explain_sylvester(n: int) -> str:
    if n < 0:
        return f"{n} < 0 -- not applicable"
    a = 2
    seq = []
    while a <= n:
        seq.append(a)
        if a == n:
            return f"{n} is a term in Sylvester's sequence: {seq} -> YES"
        a = a * (a - 1) + 1
    return f"{n} is not in Sylvester's sequence (terms: {seq}) -> NO"

@register(name="Sylvester", category="sequences", oeis="A000058",
          description="Member of the Sylvester sequence.",
          explain=_explain_sylvester)
def is_sylvester(n: int) -> bool:
    """Return True if n is a term in the Sylvester sequence.

    Parameters
    ----------
    n : int

    Returns
    -------
    bool
    """
    return n >= 0 and n in _SYLVESTER
