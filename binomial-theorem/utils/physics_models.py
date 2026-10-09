"""Seeded models for chapter 11: fair coin flips and a Galton board.

A Galton board drops balls through rows of pegs; at each peg a ball goes left
or right. The film treats every bounce as one fair coin flip, independent of
the others. That is an idealisation — a real board has momentum, friction and
imperfect pegs — and the narration says "like a ball bouncing", keeping it a
metaphor. With that idealisation, a ball's route through n rows is a choice
list of length n, and the bin it lands in is the number of right steps.

All randomness comes from one seeded generator, so every render shows the same
balls in the same bins.

    python -m utils.physics_models      # print the seeded sample and checks
"""

from __future__ import annotations

import random
from fractions import Fraction
from math import exp, pi, sqrt

import config as cfg
from utils.math_utils import binomial_probabilities, coefficients, path_cells

# The demonstration in chapter 11: 64 balls through 5 rows, so the expected
# pile in each bin is exactly twice row 5 of the triangle: 2, 10, 20, 20, 10, 2.
DEMO_ROWS = 5
DEMO_BALLS = 64


def flip_sequence(rng: random.Random, flips: int) -> str:
    """One run of fair flips, written in the film's letters: a = heads, b = tails."""
    return "".join(rng.choice("ab") for _ in range(flips))


def galton_drops(rows: int = DEMO_ROWS, balls: int = DEMO_BALLS, seed: int = cfg.SEED) -> list[str]:
    """The route of every ball, as a choice list (a = bounce left, b = bounce right)."""
    rng = random.Random(seed)
    return [flip_sequence(rng, rows) for _ in range(balls)]


def bin_of(route: str) -> int:
    """The bin a ball lands in: how many times it bounced right."""
    return path_cells(route)[-1][1]


def bin_counts(routes: list[str], rows: int = DEMO_ROWS) -> list[int]:
    counts = [0] * (rows + 1)
    for route in routes:
        counts[bin_of(route)] += 1
    return counts


def expected_counts(rows: int = DEMO_ROWS, balls: int = DEMO_BALLS) -> list[Fraction]:
    """What the bins approach on average: balls * (rows choose k) / 2**rows."""
    return [balls * p for p in binomial_probabilities(rows)]


def normal_curve(n: int):
    """The bell curve the binomial row approaches: mean n/2, variance n/4.

    Returns a function of k giving the approximate *count* (scaled by 2**n),
    so it can be drawn over a histogram of the coefficients themselves.
    """
    mean, sigma = n / 2, sqrt(n) / 2

    def height(k: float) -> float:
        return 2 ** n * exp(-((k - mean) ** 2) / (2 * sigma ** 2)) / (sigma * sqrt(2 * pi))

    return height


def self_check() -> list[str]:
    failures = []
    routes = galton_drops()
    if galton_drops() != routes:
        failures.append("the seeded sample is not reproducible")
    counts = bin_counts(routes)
    if sum(counts) != DEMO_BALLS:
        failures.append("balls went missing")
    expected = expected_counts()
    if expected != [2 * c for c in coefficients(DEMO_ROWS)]:
        failures.append("64 balls should expect exactly twice row 5")
    # The sample should look like a binomial pile, not like an accident: the
    # middle two bins hold the most, the edges the least.
    if max(counts[0], counts[-1]) >= min(counts[2], counts[3]):
        failures.append(f"sample {counts} does not pile up in the middle; pick another seed")
    # The bell curve should approximate row 20 to within a few percent at the centre.
    centre = coefficients(20)[10]
    if abs(normal_curve(20)(10) - centre) / centre > 0.03:
        failures.append("normal approximation is off at the centre of row 20")
    return failures


def main() -> int:
    failures = self_check()
    routes = galton_drops()
    print(f"{DEMO_BALLS} balls through {DEMO_ROWS} rows (seed {cfg.SEED}):")
    print("  landed   ", bin_counts(routes))
    print("  expected ", [int(x) for x in expected_counts()])
    for failure in failures:
        print("FAIL", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
