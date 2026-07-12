"""Motion helpers for probability-as-geometry animations."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def belief_shift(prior: float, posterior: float, steps: int = 24) -> list[float]:
    """Return an eased interpolation path from a prior to a posterior belief."""
    t = np.linspace(0.0, 1.0, steps)
    eased = t * t * (3 - 2 * t)
    return list(prior + (posterior - prior) * eased)


def jitter_positions(count: int, spread: float = 0.12, seed: int = 7) -> list[np.ndarray]:
    """Return small deterministic random offsets to make icons feel alive."""
    rng = np.random.default_rng(seed)
    return [rng.uniform(-spread, spread, size=2) for _ in range(count)]


def evidence_pulse(strength: float, steps: int = 20) -> list[float]:
    """Return a decaying pulse curve used to animate 'new evidence' flashes."""
    t = np.linspace(0.0, 1.0, steps)
    return list(strength * np.exp(-3 * t) * np.sin(2 * np.pi * t))


def scaled_bar_heights(values: Sequence[float], max_height: float = 3.2) -> list[float]:
    """Scale raw scores into bar heights capped at max_height."""
    peak = max(values) if values else 1.0
    peak = peak if peak > 0 else 1.0
    return [max_height * (value / peak) for value in values]
