"""The exact combinatorics behind every number on screen.

Nothing in the film is typed in by hand. A coefficient is obtained the way the
film argues it should be: by writing out every *choice list* — one letter, a or
b, picked from each bracket — and counting how many lists contain k b's. That
brute-force count is then cross-checked against ``math.comb`` and against
Pascal's addition rule, so the picture, the algebra and the triangle cannot
drift apart.

    python -m utils.math_utils      # run the self-check
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import comb, factorial

LETTERS = "ab"


# ----------------------------------------------------------------------------
# Choice lists: one letter from each bracket
# ----------------------------------------------------------------------------


@lru_cache(maxsize=None)
def choice_words(n: int) -> tuple[str, ...]:
    """Every way n brackets can each pick a or b, in dictionary order (2**n of them)."""
    return tuple("".join(letters) for letters in product(LETTERS, repeat=n))


def b_positions(word: str) -> tuple[int, ...]:
    """Which brackets (0-based) said b."""
    return tuple(index for index, letter in enumerate(word) if letter == "b")


def word_from_positions(n: int, positions) -> str:
    """The choice list in which exactly the brackets in ``positions`` say b."""
    chosen = set(positions)
    return "".join("b" if index in chosen else "a" for index in range(n))


@lru_cache(maxsize=None)
def words_with_b(n: int, k: int) -> tuple[str, ...]:
    """Lists with exactly k b's, ordered by which brackets say b: (1,2), (1,3), ..."""
    return tuple(word_from_positions(n, pair) for pair in combinations(range(n), k))


def sort_into_piles(n: int) -> dict[int, list[str]]:
    """All 2**n lists, sorted into piles by how many b's each contains."""
    piles: dict[int, list[str]] = {k: [] for k in range(n + 1)}
    for word in choice_words(n):
        piles[word.count("b")].append(word)
    return piles


# ----------------------------------------------------------------------------
# Coefficients — by brute force, by formula, by addition
# ----------------------------------------------------------------------------


@lru_cache(maxsize=None)
def coefficients(n: int) -> tuple[int, ...]:
    """Coefficients of (a+b)^n, found by expanding the product as choice lists.

    The coefficient of a^(n-k) b^k is the number of lists with k b's. This is
    the film's definition; ``self_check`` proves it equals n choose k.
    """
    counts = Counter(word.count("b") for word in choice_words(n))
    return tuple(counts[k] for k in range(n + 1))


def choose(n: int, k: int) -> int:
    """n choose k, from the factorial formula the film derives in chapter 6."""
    if k < 0 or k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))


def ordered_picks(n: int, k: int) -> int:
    """Picks of k brackets one after another, where order still matters: n(n-1)..."""
    return factorial(n) // factorial(n - k)


@lru_cache(maxsize=None)
def pascal_rows(rows: int) -> tuple[tuple[int, ...], ...]:
    """Rows 0..rows-1 of Pascal's triangle, built only by adding the two above."""
    triangle = [(1,)]
    for _ in range(1, rows):
        above = triangle[-1]
        triangle.append(tuple(1 if k in (0, len(above)) else above[k - 1] + above[k]
                              for k in range(len(above) + 1)))
    return tuple(triangle)


def shifted_copies(row) -> tuple[list[int], list[int], list[int]]:
    """Multiply (a+b)^n by a and by b: the two copies, offset by one, and their sum.

    Chapter 4's algebraic reason for Pascal's rule: ``times_a`` keeps every
    term in place, ``times_b`` slides it one place along, and the sum is the
    next row.
    """
    times_a = list(row) + [0]
    times_b = [0] + list(row)
    return times_a, times_b, [x + y for x, y in zip(times_a, times_b)]


def split_by_last(n: int, k: int) -> tuple[list[str], list[str]]:
    """Chapter 9's sort: lists whose last bracket says b, and lists where it says a."""
    lists = words_with_b(n, k)
    return [w for w in lists if w[-1] == "b"], [w for w in lists if w[-1] == "a"]


def row_sum(n: int) -> int:
    return sum(coefficients(n))


# ----------------------------------------------------------------------------
# Paths through the triangle: a left step is a, a right step is b
# ----------------------------------------------------------------------------


def path_cells(word: str) -> list[tuple[int, int]]:
    """The (row, position) cells a path visits, starting at the apex (0, 0)."""
    cells = [(0, 0)]
    for letter in word:
        row, position = cells[-1]
        cells.append((row + 1, position + (letter == "b")))
    return cells


def paths_to(n: int, k: int) -> tuple[str, ...]:
    """Every path from the apex to cell (n, k) — the same lists as ``words_with_b``."""
    return tuple(w for w in choice_words(n) if path_cells(w)[-1] == (n, k))


def path_counts(rows: int) -> list[list[int]]:
    """Paths into each cell, counted by flowing down from the apex."""
    counts = [[1]]
    for row in range(1, rows):
        above = counts[-1]
        counts.append([(above[k - 1] if k >= 1 else 0) + (above[k] if k < row else 0)
                       for k in range(row + 1)])
    return counts


# ----------------------------------------------------------------------------
# Probability
# ----------------------------------------------------------------------------


def binomial_probabilities(n: int) -> list[Fraction]:
    """Chance of exactly k tails in n fair flips: (n choose k) / 2**n."""
    total = 2 ** n
    return [Fraction(c, total) for c in coefficients(n)]


# ----------------------------------------------------------------------------
# LaTeX for terms
# ----------------------------------------------------------------------------


def power_tex(letter: str, exponent: int) -> str | None:
    """'a', 'a^{3}', or None when the exponent is zero."""
    if exponent == 0:
        return None
    return letter if exponent == 1 else f"{letter}^{{{exponent}}}"


def term_parts(coefficient: int, a_exp: int, b_exp: int) -> list[tuple[str, str]]:
    """A term as (tex, role) pieces; role is 'coef', 'a' or 'b'.

    A coefficient of 1 is left unwritten, exactly as the expansion is printed,
    except for the lone constant term of (a+b)^0.
    """
    parts: list[tuple[str, str]] = []
    if coefficient != 1 or (a_exp == 0 and b_exp == 0):
        parts.append((str(coefficient), "coef"))
    for letter, exponent in (("a", a_exp), ("b", b_exp)):
        tex = power_tex(letter, exponent)
        if tex:
            parts.append((tex, letter))
    return parts


def expansion_terms(n: int) -> list[list[tuple[str, str]]]:
    """The expansion of (a+b)^n as a list of terms, k = 0..n."""
    return [term_parts(c, n - k, k) for k, c in enumerate(coefficients(n))]


def big_number(value: int) -> str:
    """Thousands separators for spoken-size numbers: 1024 -> '1,024'."""
    return f"{value:,}"


# ----------------------------------------------------------------------------
# Self-check
# ----------------------------------------------------------------------------


def self_check(max_n: int = 12) -> list[str]:
    """Every identity the film states, verified exactly. Returns failures."""
    failures: list[str] = []
    rows = pascal_rows(max_n + 1)
    flow = path_counts(max_n + 1)
    for n in range(max_n + 1):
        brute = coefficients(n)
        if list(brute) != [comb(n, k) for k in range(n + 1)]:
            failures.append(f"n={n}: brute-force expansion != math.comb")
        if list(brute) != [choose(n, k) for k in range(n + 1)]:
            failures.append(f"n={n}: factorial formula disagrees")
        if tuple(brute) != rows[n]:
            failures.append(f"n={n}: Pascal's addition rule disagrees")
        if list(brute) != flow[n]:
            failures.append(f"n={n}: path flow disagrees")
        if list(brute) != list(reversed(brute)):
            failures.append(f"n={n}: row is not symmetric")
        if row_sum(n) != 2 ** n:
            failures.append(f"n={n}: row sum is not 2^n")
        for k in range(n + 1):
            if len(words_with_b(n, k)) != brute[k] or len(paths_to(n, k)) != brute[k]:
                failures.append(f"n={n}, k={k}: listing count disagrees")
            if n and k and brute[k] != choose(n - 1, k - 1) + choose(n - 1, k):
                failures.append(f"n={n}, k={k}: Pascal's rule fails")
            if n >= 1 and 1 <= k <= n:
                with_b, with_a = split_by_last(n, k)
                if (len(with_b), len(with_a)) != (choose(n - 1, k - 1), choose(n - 1, k)):
                    failures.append(f"n={n}, k={k}: last-bracket split is wrong")
            if k and ordered_picks(n, k) // factorial(k) != brute[k]:
                failures.append(f"n={n}, k={k}: ordered picks / k! is wrong")
        if n:
            if shifted_copies(rows[n - 1])[2] != list(rows[n]):
                failures.append(f"n={n}: shifted copies do not add to the next row")
    if sum(binomial_probabilities(5)) != 1:
        failures.append("probabilities of 5 flips do not sum to 1")
    # Chapter 12: with a = 10, b = 1 the digits of 11^n are row n while no entry carries.
    for n in range(5):
        if str(11 ** n) != "".join(str(c) for c in coefficients(n)):
            failures.append(f"11^{n} does not spell row {n}")
    return failures


def main() -> int:
    failures = self_check()
    for failure in failures:
        print("FAIL", failure)
    if failures:
        return 1
    print("Expansion by choice lists == n choose k == Pascal's rule == path counts, for n = 0..12.")
    print("Symmetry, row sums 2^n, the last-bracket split, n(n-1)../k! and 11^n (n <= 4) all check out.")
    print("Row 5:", coefficients(5), "  pile for a^3 b^2:", ", ".join(words_with_b(5, 2)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
