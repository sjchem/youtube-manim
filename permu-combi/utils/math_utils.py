"""Exact combinatorial arithmetic, so the film never quotes a rounded count.

Every number spoken or written in the video is produced here and checked by
``python -m utils.math_utils``.
"""

from __future__ import annotations

from itertools import combinations as _combinations, permutations as _permutations
from math import comb, factorial as _factorial, perm


def factorial(n: int) -> int:
    """n! — the number of ways to arrange all n objects."""
    if n < 0:
        raise ValueError("factorial is not defined for negative n")
    return _factorial(n)


def permutations(n: int, r: int) -> int:
    """nPr = n!/(n-r)! — fill r ordered positions from n objects."""
    if not 0 <= r <= n:
        raise ValueError(f"cannot fill {r} positions from {n} objects")
    return perm(n, r)


def combinations(n: int, r: int) -> int:
    """nCr = n!/(r!(n-r)!) — choose r objects from n, order ignored."""
    if not 0 <= r <= n:
        raise ValueError(f"cannot choose {r} objects from {n}")
    return comb(n, r)


def overcount_factor(r: int) -> int:
    """How many times an ordered count repeats each unordered group: r!."""
    return factorial(r)


def arrangements_with_repetition(total: int, *multiplicities: int) -> int:
    """Distinct arrangements when equal objects occur in known multiplicities."""
    if total < 0 or any(count < 0 for count in multiplicities):
        raise ValueError("counts must be non-negative")
    if sum(multiplicities) != total:
        raise ValueError("multiplicities must add up to the total")
    denominator = 1
    for count in multiplicities:
        denominator *= factorial(count)
    return factorial(total) // denominator


def polygon_diagonals(vertices: int) -> int:
    """Number of diagonals determined by a simple n-vertex polygon."""
    if vertices < 3:
        raise ValueError("a polygon needs at least three vertices")
    return combinations(vertices, 2) - vertices


def list_permutations(items: str | list[str], r: int | None = None) -> list[str]:
    """Every ordered arrangement, as joined strings — used to fill on-screen cards."""
    pool = list(items)
    return ["".join(p) for p in _permutations(pool, r if r is not None else len(pool))]


def list_combinations(items: str | list[str], r: int) -> list[str]:
    """Every unordered selection, as joined strings."""
    pool = list(items)
    return ["".join(c) for c in _combinations(pool, r)]


def grouped_permutations(items: str | list[str], r: int) -> dict[str, list[str]]:
    """Each unordered group mapped to the r! orderings that collapse into it."""
    return {
        group: [word for word in list_permutations(items, r) if sorted(word) == sorted(group)]
        for group in list_combinations(items, r)
    }


def pretty(value: int) -> str:
    """Thousands separators, for numbers the viewer is meant to feel."""
    return f"{value:,}"


def tex_number(value: int) -> str:
    """A thousands-separated number that survives LaTeX math mode."""
    return pretty(value).replace(",", "{,}")


def _self_check() -> None:
    assert factorial(0) == 1
    assert factorial(4) == 24
    assert permutations(5, 3) == 60 == factorial(5) // factorial(2)
    assert combinations(5, 3) == 10 == permutations(5, 3) // factorial(3)
    assert combinations(10, 3) == combinations(10, 7) == 120
    assert combinations(52, 5) == 2_598_960
    assert combinations(5, 5) == 1
    assert factorial(3) * factorial(2) == 12
    assert factorial(3) * combinations(4, 2) * factorial(2) == 72
    assert arrangements_with_repetition(5, 2, 2, 1) == 30
    assert polygon_diagonals(6) == 9
    assert len(list_permutations("ABC")) == 6
    assert len(list_combinations("ABCDE", 3)) == 10
    groups = grouped_permutations("ABCDE", 3)
    assert all(len(orderings) == 6 for orderings in groups.values())
    assert sum(len(orderings) for orderings in groups.values()) == 60


if __name__ == "__main__":
    _self_check()
    print("Every count used in the film checks out:")
    print(f"  4!            = {pretty(factorial(4))}")
    print(f"  12!           = {pretty(factorial(12))}")
    print(f"  5P3           = {pretty(permutations(5, 3))}")
    print(f"  5C3           = {pretty(combinations(5, 3))}")
    print(f"  10C3 = 10C7   = {pretty(combinations(10, 3))}")
    print(f"  52C5          = {pretty(combinations(52, 5))}")
    print(f"  0!            = {pretty(factorial(0))}")
    print(f"  MATH, AT together = {factorial(3) * factorial(2)}")
    print(f"  3 boys, 2 girls apart = {factorial(3) * combinations(4, 2) * factorial(2)}")
    print(f"  LEVEL         = {pretty(arrangements_with_repetition(5, 2, 2, 1))}")
    print(f"  hexagon diagonals = {pretty(polygon_diagonals(6))}")
