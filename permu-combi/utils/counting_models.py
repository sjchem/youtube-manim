"""Small models behind the visuals: Pascal rows, growth curves, and a sampler.

Nothing here is decorative. Each function feeds a number the film shows, and
``python -m utils.counting_models`` checks the closed forms against brute force.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from itertools import permutations as _permutations

from utils.math_utils import combinations, factorial, list_combinations, list_permutations, permutations


@dataclass(frozen=True)
class Stage:
    """One step of a staged process: a name and how many options it offers."""

    name: str
    options: int


def multiply_stages(stages: list[Stage]) -> int:
    """The multiplication principle: stages multiply, they never add."""
    total = 1
    for stage in stages:
        total *= stage.options
    return total


def shrinking_pool(n: int, r: int) -> list[int]:
    """The number of choices still open at each of r positions: n, n-1, ..."""
    if not 0 <= r <= n:
        raise ValueError(f"cannot fill {r} positions from {n} objects")
    return [n - step for step in range(r)]


def pascal_row(n: int) -> list[int]:
    """Row n of Pascal's triangle — the combination counts C(n, 0..n)."""
    return [combinations(n, r) for r in range(n + 1)]


def factorial_growth(limit: int = 12) -> list[tuple[int, int]]:
    """(n, n!) pairs for the growth bar in the factorial chapter."""
    return [(n, factorial(n)) for n in range(1, limit + 1)]


def overcount_map(items: str, r: int) -> dict[str, list[str]]:
    """Which ordered arrangements collapse onto which unordered group."""
    groups: dict[str, list[str]] = {group: [] for group in list_combinations(items, r)}
    for word in list_permutations(items, r):
        groups["".join(sorted(word, key=items.index))].append(word)
    return groups


def sample_arrangements(items: str, r: int, trials: int, seed: int = 20260915) -> dict[str, int]:
    """A Monte-Carlo sanity check: random draws should hit every arrangement."""
    rng = random.Random(seed)
    pool = list(items)
    seen: dict[str, int] = {}
    for _ in range(trials):
        rng.shuffle(pool)
        word = "".join(pool[:r])
        seen[word] = seen.get(word, 0) + 1
    return seen


def _self_check() -> None:
    stages = [Stage("shirts", 3), Stage("trousers", 2), Stage("shoes", 2)]
    assert multiply_stages(stages) == 12
    assert multiply_stages(stages[:2]) == 6
    assert shrinking_pool(4, 4) == [4, 3, 2, 1]
    assert multiply_stages([Stage("", value) for value in shrinking_pool(4, 4)]) == factorial(4)
    assert multiply_stages([Stage("", value) for value in shrinking_pool(5, 3)]) == permutations(5, 3)
    row = pascal_row(10)
    assert row == row[::-1], "Pascal rows must be symmetric"
    assert row[3] == row[7] == combinations(10, 3)
    assert sum(row) == 2 ** 10
    assert factorial_growth(4)[-1] == (4, 24)
    groups = overcount_map("ABCDE", 3)
    assert len(groups) == combinations(5, 3)
    assert all(len(words) == factorial(3) for words in groups.values())
    assert sum(len(words) for words in groups.values()) == permutations(5, 3)
    # Brute force, independent of the closed forms above.
    assert len({"".join(p) for p in _permutations("ABCDE", 3)}) == 60
    hits = sample_arrangements("ABCDE", 3, 4000)
    assert len(hits) == permutations(5, 3), "every arrangement should appear in 4000 draws"


if __name__ == "__main__":
    _self_check()
    print("Counting models agree with brute force.")
    print(f"  stages 3x2x2                 = {multiply_stages([Stage('', 3), Stage('', 2), Stage('', 2)])}")
    print(f"  choices left filling 4 slots = {shrinking_pool(4, 4)}")
    print(f"  Pascal row 10                = {pascal_row(10)}")
    print(f"  orderings per 3-person team  = {len(overcount_map('ABCDE', 3)['ABC'])}")
