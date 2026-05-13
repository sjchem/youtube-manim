"""Command-line entry point for the tennis game probability project."""

from __future__ import annotations

import argparse

from config import (
    ZVEREV_ACTUAL_GAME_WIN,
    ZVEREV_FIRST_SERVE_IN,
    ZVEREV_FIRST_SERVE_WIN,
    ZVEREV_SECOND_SERVE_IN,
    ZVEREV_SECOND_SERVE_WIN,
)
from utils.math_utils import game_breakdown, game_win_probability, point_win_probability, simulate_service_games


def print_probabilities(simulate: bool = False) -> None:
    """Print the main numerical claims used in the video."""

    p = point_win_probability(
        ZVEREV_FIRST_SERVE_IN,
        ZVEREV_FIRST_SERVE_WIN,
        ZVEREV_SECOND_SERVE_IN,
        ZVEREV_SECOND_SERVE_WIN,
    )
    g = game_win_probability(p)
    parts = game_breakdown(p)
    print(f"Point win probability from serve stats: {p:.6f} ({100 * p:.2f}%)")
    print(f"Closed-form game win probability G({p:.5f}): {g:.6f} ({100 * g:.2f}%)")
    print(f"Actual reference service-game win percentage: {ZVEREV_ACTUAL_GAME_WIN:.3f} ({100 * ZVEREV_ACTUAL_GAME_WIN:.1f}%)")
    print("Breakdown:")
    print(f"  4-0 term: {parts.love:.6f}")
    print(f"  4-1 term: {parts.fifteen:.6f}")
    print(f"  4-2 term: {parts.thirty:.6f}")
    print(f"  Reach deuce: {parts.deuce_reached:.6f}")
    print(f"  Win from deuce: {parts.deuce_win:.6f}")
    if simulate:
        estimate = simulate_service_games(p, n_games=100_000)
        print(f"Monte Carlo estimate, 100000 games: {estimate:.6f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tennis game probability video utilities")
    parser.add_argument("--probabilities", action="store_true", help="Print the main exact probabilities")
    parser.add_argument("--simulate", action="store_true", help="Also run the Monte Carlo simulation")
    args = parser.parse_args()

    print_probabilities(simulate=args.simulate)


if __name__ == "__main__":
    main()
