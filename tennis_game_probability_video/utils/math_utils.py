"""Probability utilities for modeling tennis service games."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from random import Random


@dataclass(frozen=True)
class GameBreakdown:
    """Named components of the service-game probability."""

    love: float
    fifteen: float
    thirty: float
    deuce_reached: float
    deuce_win: float

    @property
    def total(self) -> float:
        """Return the full game win probability."""

        return self.love + self.fifteen + self.thirty + self.deuce_reached * self.deuce_win


def point_win_probability(p_s1: float, p_w_s1: float, p_s2: float, p_w_s2: float) -> float:
    """Return the probability that the server wins a point."""

    _validate_probability(p_s1, "p_s1")
    _validate_probability(p_w_s1, "p_w_s1")
    _validate_probability(p_s2, "p_s2")
    _validate_probability(p_w_s2, "p_w_s2")
    return p_s1 * p_w_s1 + (1 - p_s1) * p_s2 * p_w_s2


def deuce_win_probability(p: float) -> float:
    """Return the chance of eventually winning a game from deuce."""

    _validate_probability(p, "p")
    denominator = p**2 + (1 - p) ** 2
    if denominator == 0:
        return 0.0
    return p**2 / denominator


def deuce_reach_probability(p: float) -> float:
    """Return the probability that a service game reaches deuce."""

    _validate_probability(p, "p")
    return comb(6, 3) * p**3 * (1 - p) ** 3


def game_breakdown(p: float) -> GameBreakdown:
    """Return named terms in the closed-form game probability."""

    _validate_probability(p, "p")
    return GameBreakdown(
        love=p**4,
        fifteen=4 * p**4 * (1 - p),
        thirty=10 * p**4 * (1 - p) ** 2,
        deuce_reached=deuce_reach_probability(p),
        deuce_win=deuce_win_probability(p),
    )


def game_win_probability(p: float) -> float:
    """Return the exact probability that the server wins a game."""

    return game_breakdown(p).total


def simulate_service_games(p: float, n_games: int = 100_000, seed: int = 42) -> float:
    """Monte Carlo estimate of a server's game win probability."""

    _validate_probability(p, "p")
    if n_games <= 0:
        raise ValueError("n_games must be positive")

    rng = Random(seed)
    wins = 0
    for _ in range(n_games):
        server_points = 0
        receiver_points = 0
        while True:
            if rng.random() < p:
                server_points += 1
            else:
                receiver_points += 1

            if server_points >= 4 and server_points - receiver_points >= 2:
                wins += 1
                break
            if receiver_points >= 4 and receiver_points - server_points >= 2:
                break

    return wins / n_games


def _validate_probability(value: float, name: str) -> None:
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1")


if __name__ == "__main__":
    p = 0.70464
    assert abs(game_win_probability(0.5) - 0.5) < 1e-12
    assert abs(game_win_probability(p) - 0.9059) < 0.002
    print(f"G(0.5) = {game_win_probability(0.5):.3f}")
    print(f"G({p}) = {game_win_probability(p):.3f}")
    print(f"Simulation = {simulate_service_games(p, n_games=25_000):.3f}")
