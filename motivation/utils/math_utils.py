"""Small mathematical models used by the Manim scenes.

These are deliberately simple physics-inspired metaphors. They are not meant
to model clinical psychology or diagnose human behavior.
"""

from __future__ import annotations

import numpy as np


def motivation_decay(t, m0=1.0, k=0.55):
    """Exponential motivation decay: M(t) = M0 e^(-kt)."""
    return m0 * np.exp(-k * np.asarray(t))


def habit_momentum(t, L=1.0, k=1.2, t0=4.0):
    """Logistic growth curve for accumulated habit momentum."""
    t = np.asarray(t)
    return L / (1 + np.exp(-k * (t - t0)))


def feedback_update(momentum, action, drag=0.08):
    """One-step feedback model: next momentum from action minus drag."""
    return momentum + action - drag * momentum


def normalized_curve(values):
    """Normalize a sequence to the [0, 1] range."""
    values = np.asarray(values, dtype=float)
    min_value = values.min()
    span = values.max() - min_value
    if span == 0:
        return np.zeros_like(values)
    return (values - min_value) / span


def potential_energy_barrier(x, barrier_height=1.0, barrier_center=0.0, width=1.0):
    """A smooth double-well potential with a tunable central barrier."""
    x = np.asarray(x, dtype=float)
    wells = 0.18 * (x**2 - 4.0) ** 2
    barrier = barrier_height * np.exp(-((x - barrier_center) ** 2) / (2 * width**2))
    tilt = -0.12 * x
    return wells + barrier + tilt


def lower_barrier(x, amount=0.45):
    """Return a discipline-shaped barrier modifier that lowers the center."""
    x = np.asarray(x, dtype=float)
    return amount * np.exp(-(x**2) / 1.8)


def sample_curve(fn, x_min, x_max, samples=160):
    """Sample a scalar function into x/y arrays."""
    xs = np.linspace(x_min, x_max, samples)
    return xs, fn(xs)

