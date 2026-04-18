# === numclassify/_core/figurate.py ===

# =============================================================================
# Section 1: Imports
# =============================================================================
from numclassify._registry import register, REGISTRY
import math
from functools import partial
from typing import Optional


# =============================================================================
# Section 2: Core math functions (NOT registered, used internally)
# =============================================================================

def _is_perfect_square(n: int) -> bool:
    """Integer perfect square check — no float errors."""
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def kth_polygonal(k: int, n: int) -> int:
    """Return the n-th k-gonal number. Formula: n*((k-2)*n - (k-4)) // 2"""
    return n * ((k - 2) * n - (k - 4)) // 2


def is_k_gonal(m: int, k: int) -> bool:
    """
    Check if m is a k-gonal number.

    Solves P(k,n)=m via quadratic inverse. Returns True iff n is a positive integer.
    Edge case: m<=0 returns False. m=1 returns True for all k (1 is always 1st k-gonal).
    """
    if m < 1:
        return False
    if m == 1:
        return True
    # discriminant: (k-4)^2 + 8*(k-2)*m
    # n = ((k-4) + sqrt(disc)) / (2*(k-2))
    disc = (k - 4) ** 2 + 8 * (k - 2) * m
    if not _is_perfect_square(disc):
        return False
    sqrt_disc = math.isqrt(disc)
    numerator = (k - 4) + sqrt_disc
    denominator = 2 * (k - 2)
    if numerator <= 0 or numerator % denominator != 0:
        return False
    n = numerator // denominator
    return n >= 1


def nth_centered_kgonal(k: int, n: int) -> int:
    """Return the n-th centered k-gonal number. Formula: k*n*(n-1)//2 + 1"""
    return k * n * (n - 1) // 2 + 1


def is_centered_k_gonal(m: int, k: int) -> bool:
    """
    Check if m is a centered k-gonal number.

    Inverse: solve k*n*(n-1)/2 + 1 = m → n^2 - n - 2*(m-1)/k = 0
    Use quadratic formula, check n is positive integer.
    Edge case: m=1 is always True (n=0 term gives C(k,0)=1... actually n=1 gives 1 too).
    """
    if m < 1:
        return False
    if m == 1:
        return True
    # k*n*(n-1)/2 + 1 = m
    # k*n*(n-1) = 2*(m-1)
    # k*n^2 - k*n - 2*(m-1) = 0
    # discriminant: k^2 + 4*k*2*(m-1) = k^2 + 8*k*(m-1)
    val = m - 1
    if 2 * val % k != 0:
        # Check if 2*(m-1) is divisible by k for integer n check via disc
        pass  # disc check handles this
    disc = k * k + 8 * k * val
    if not _is_perfect_square(disc):
        return False
    sqrt_disc = math.isqrt(disc)
    numerator = k + sqrt_disc
    denominator = 2 * k
    if numerator <= 0 or numerator % denominator != 0:
        return False
    n = numerator // denominator
    return n >= 1


# =============================================================================
# Section 3: Polygon name table
# =============================================================================

POLYGON_NAMES: dict = {
    3:  ("triangular",      "A000217", "A005448"),
    4:  ("square",          "A000290", "A001844"),
    5:  ("pentagonal",      "A000326", "A005891"),
    6:  ("hexagonal",       "A000384", "A003215"),
    7:  ("heptagonal",      "A000566", "A069099"),
    8:  ("octagonal",       "A000567", "A016754"),
    9:  ("nonagonal",       "A001106", "A060544"),
    10: ("decagonal",       "A001107", "A062786"),
    11: ("hendecagonal",    "A051682", "A069125"),
    12: ("dodecagonal",     "A051624", "A003154"),
    13: ("tridecagonal",    "A051865", ""),
    14: ("tetradecagonal",  "A051866", ""),
    15: ("pentadecagonal",  "A051867", ""),
    16: ("hexadecagonal",   "A051868", ""),
    17: ("heptadecagonal",  "A051869", ""),
    18: ("octadecagonal",   "A051870", ""),
    19: ("enneadecagonal",  "A051871", ""),
    20: ("icosagonal",      "A051872", ""),
}

for _k in range(21, 1001):
    POLYGON_NAMES[_k] = (f"{_k}_gonal", "", "")


# =============================================================================
# Section 4: Auto-registration loop
# =============================================================================

for k in range(3, 1001):
    _name, _oeis_p, _oeis_c = POLYGON_NAMES[k]

    # --- Register polygonal ---
    _func_name = f"is_{_name}"
    _description = f"Numbers that can be arranged as a regular {_name} polygon"
    _display_name = _name.capitalize() if not _name[0].isdigit() else _name

    def _make_polygonal_func(k_=k, name_=_name):
        def _fn(n: int) -> bool:
            """Return True if n is a k-gonal figurate number."""
            return is_k_gonal(n, k_)
        _fn.__name__ = f"is_{name_}"
        _fn.__doc__ = f"Return True if n is a {name_} number (k={k_}-gonal)."
        return _fn

    _poly_fn = _make_polygonal_func()
    register(
        name=_display_name,
        category="figurate",
        oeis=_oeis_p,
        description=_description,
        aliases=[_func_name, _name],
    )(_poly_fn)

    # --- Register centered polygonal ---
    _center_name_str = f"centered_{_name}"
    _center_display = f"Centered {_name}"

    def _make_centered_func(k_=k, name_=_name):
        def _fn(n: int) -> bool:
            """Return True if n is a centered k-gonal figurate number."""
            return is_centered_k_gonal(n, k_)
        _fn.__name__ = f"is_centered_{name_}"
        _fn.__doc__ = f"Return True if n is a centered {name_} number (centered k={k_}-gonal)."
        return _fn

    _cent_fn = _make_centered_func()
    register(
        name=_center_display,
        category="figurate_centered",
        oeis=_oeis_c,
        description=f"Centered {_name} numbers",
        aliases=[f"is_centered_{_name}", _center_name_str],
    )(_cent_fn)


# Module-level names for the 8 most common figurate types
is_triangular         = REGISTRY["triangular"].func
is_square             = REGISTRY["square"].func
is_pentagonal         = REGISTRY["pentagonal"].func
is_hexagonal          = REGISTRY["hexagonal"].func
is_heptagonal         = REGISTRY["heptagonal"].func
is_octagonal          = REGISTRY["octagonal"].func
is_centered_triangular = REGISTRY["centered_triangular"].func
is_centered_square    = REGISTRY["centered_square"].func


# =============================================================================
# Section 5: Extra figurate types
# =============================================================================

def is_pronic(n: int) -> bool:
    """
    Return True if n is a pronic (oblong) number: n = k*(k+1) for some k >= 0.

    Also known as oblong numbers or heteromecic numbers. OEIS A002378.
    Inverse check: solve k^2 + k - n = 0, discriminant = 1 + 4*n, check perfect square.
    """
    if n < 0:
        return False
    if n == 0:
        return True
    disc = 1 + 4 * n
    if not _is_perfect_square(disc):
        return False
    sqrt_disc = math.isqrt(disc)
    # k = (-1 + sqrt(1+4n)) / 2
    numerator = -1 + sqrt_disc
    if numerator < 0 or numerator % 2 != 0:
        return False
    return True


register(
    name="Pronic",
    category="figurate",
    oeis="A002378",
    description="Pronic (oblong) numbers: k*(k+1) for non-negative integer k",
    aliases=["is_pronic", "pronic", "oblong", "is_oblong"],
)(is_pronic)


def is_star(n: int) -> bool:
    """
    Return True if n is a star number: 6*k*(k-1) + 1 for k >= 1.

    Star numbers: 1, 13, 37, 73, ... OEIS A003154.
    """
    if n < 1:
        return False
    if n == 1:
        return True
    # 6*k*(k-1) + 1 = n  →  6k^2 - 6k + (1-n) = 0
    # disc = 36 - 24*(1-n) = 36 + 24*(n-1) = 12 + 24n - 12 = 24n - 12 + 24 ... let me redo:
    # 6k^2 - 6k - (n-1) = 0
    # disc = 36 + 24*(n-1)
    disc = 36 + 24 * (n - 1)
    if not _is_perfect_square(disc):
        return False
    sqrt_disc = math.isqrt(disc)
    numerator = 6 + sqrt_disc
    if numerator % 12 != 0:
        return False
    k = numerator // 12
    return k >= 1


register(
    name="Star",
    category="figurate",
    oeis="A003154",
    description="Star numbers: 6*k*(k-1) + 1",
    aliases=["is_star", "star"],
)(is_star)


def is_tetrahedral(n: int) -> bool:
    """
    Return True if n is a tetrahedral number: k*(k+1)*(k+2) // 6 for k >= 1.

    Tetrahedral numbers: 1, 4, 10, 20, 35, ... OEIS A000292.
    Uses iterative check to avoid floating-point errors with cube roots.
    """
    if n < 1:
        return False
    k = 1
    while True:
        t = k * (k + 1) * (k + 2) // 6
        if t == n:
            return True
        if t > n:
            return False
        k += 1


register(
    name="Tetrahedral",
    category="figurate",
    oeis="A000292",
    description="Tetrahedral numbers: k*(k+1)*(k+2)/6",
    aliases=["is_tetrahedral", "tetrahedral"],
)(is_tetrahedral)


def is_square_pyramidal(n: int) -> bool:
    """
    Return True if n is a square pyramidal number: k*(k+1)*(2*k+1) // 6 for k >= 1.

    Square pyramidal numbers: 1, 5, 14, 30, 55, ... OEIS A000330.
    Uses iterative check.
    """
    if n < 1:
        return False
    k = 1
    while True:
        t = k * (k + 1) * (2 * k + 1) // 6
        if t == n:
            return True
        if t > n:
            return False
        k += 1


register(
    name="Square Pyramidal",
    category="figurate",
    oeis="A000330",
    description="Square pyramidal numbers: k*(k+1)*(2k+1)/6",
    aliases=["is_square_pyramidal", "square_pyramidal"],
)(is_square_pyramidal)


def is_pentatope(n: int) -> bool:
    """
    Return True if n is a pentatope number: k*(k+1)*(k+2)*(k+3) // 24 for k >= 1.

    Pentatope numbers (4-simplex numbers): 1, 5, 15, 35, 70, ... OEIS A000332.
    Uses iterative check.
    """
    if n < 1:
        return False
    k = 1
    while True:
        t = k * (k + 1) * (k + 2) * (k + 3) // 24
        if t == n:
            return True
        if t > n:
            return False
        k += 1


register(
    name="Pentatope",
    category="figurate",
    oeis="A000332",
    description="Pentatope numbers (4-simplex): k*(k+1)*(k+2)*(k+3)/24",
    aliases=["is_pentatope", "pentatope"],
)(is_pentatope)


# =============================================================================
# Section 6: Verification block
# =============================================================================

if __name__ == "__main__":
    # These must all print True:
    print(is_k_gonal(1, 3))            # 1 is triangular
    print(is_k_gonal(10, 3))           # 10 is triangular
    print(not is_k_gonal(11, 3))       # 11 is NOT triangular
    print(is_k_gonal(16, 4))           # 16 is square
    print(is_k_gonal(22, 5))           # 22 is pentagonal
    print(is_centered_k_gonal(7, 6))   # 7 is centered hexagonal
    print(is_triangular(21))           # True
    print(is_square(25))               # True
    print(is_pronic(6))                # True (2*3)
    print(is_tetrahedral(10))          # True (k=3: 3*4*5/6=10)

    # Registry size check
    figurate_count = sum(
        1 for v in REGISTRY.values()
        if v.category in ("figurate", "figurate_centered")
    )
    print(f"Figurate types registered: {figurate_count}")  # should be ~2000
