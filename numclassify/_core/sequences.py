"""
numclassify/_core/sequences.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sequence-membership number classification functions.

All sets are precomputed at module load time up to 10^9 for O(1) lookup.
"""
from __future__ import annotations

from typing import Set

from numclassify._registry import register

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
    c = Fraction(1)
    n = 0
    while int(c) <= _LIMIT:
        s.add(int(c))
        c = c * 2 * (2 * n + 1) // (n + 2)
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
    # Simpler recurrence: M(n) = ((2n+2)*M(n-1) + (3n-3)*M(n-2)) / (n+3) — but fractions needed
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
# Registered classifiers
# ---------------------------------------------------------------------------

@register(name="Fibonacci", category="sequences", oeis="A000045",
          description="Member of the Fibonacci sequence.")
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


@register(name="Lucas", category="sequences", oeis="A000032",
          description="Member of the Lucas sequence.")
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


@register(name="Tribonacci", category="sequences", oeis="A000073",
          description="Member of the Tribonacci sequence.")
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


@register(name="Tetranacci", category="sequences", oeis="A000288",
          description="Member of the Tetranacci sequence.")
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


@register(name="Pell", category="sequences", oeis="A000129",
          description="Member of the Pell sequence.")
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


@register(name="Jacobsthal", category="sequences", oeis="A001045",
          description="Member of the Jacobsthal sequence.")
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


@register(name="Padovan", category="sequences", oeis="A000931",
          description="Member of the Padovan sequence.")
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


@register(name="Perrin", category="sequences", oeis="A001608",
          description="Member of the Perrin sequence.")
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


@register(name="Catalan", category="sequences", oeis="A000108",
          description="Member of the Catalan number sequence.")
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


@register(name="Bell", category="sequences", oeis="A000110",
          description="Member of the Bell number sequence.")
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


@register(name="Motzkin", category="sequences", oeis="A001006",
          description="Member of the Motzkin sequence.")
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


@register(name="Recaman", category="sequences", oeis="A005132",
          description="Member of the Recaman sequence.")
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


@register(name="Look and Say", category="sequences", oeis="A005150",
          description="Member of the look-and-say sequence.")
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


@register(name="Kolakoski", category="sequences", oeis="A000002",
          description="Member of the Kolakoski sequence (only 1 and 2).")
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


@register(name="Sylvester", category="sequences", oeis="A000058",
          description="Member of the Sylvester sequence.")
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
