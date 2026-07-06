"""Lightweight deterministic motion models for animated mathematical objects."""

from __future__ import annotations

import math

import numpy as np


def orbit_point(radius: float, angle: float, center=(0.0, 0.0, 0.0)) -> np.ndarray:
    """Point on a circular orbit in the Manim xy-plane."""

    return np.array(
        [
            center[0] + radius * math.cos(angle),
            center[1] + radius * math.sin(angle),
            center[2],
        ]
    )


def lerp(start: np.ndarray, end: np.ndarray, alpha: float) -> np.ndarray:
    """Linear interpolation for mobject updater paths."""

    return (1 - alpha) * start + alpha * end
