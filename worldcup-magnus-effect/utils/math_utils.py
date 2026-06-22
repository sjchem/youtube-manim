"""Small deterministic math helpers for path and graph construction."""

from __future__ import annotations

from math import sqrt
from typing import Iterable

import numpy as np


def linspace(start: float, end: float, count: int) -> list[float]:
    """Return evenly spaced values as ordinary floats."""
    if count <= 1:
        return [start]
    step = (end - start) / (count - 1)
    return [start + i * step for i in range(count)]


def smoothstep(t: float) -> float:
    """Cubic easing used for visual interpolation."""
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def normalize_2d(vector: tuple[float, float]) -> tuple[float, float]:
    """Normalize a 2D vector, returning zero for near-zero input."""
    x, y = vector
    mag = sqrt(x * x + y * y)
    if mag < 1e-9:
        return (0.0, 0.0)
    return (x / mag, y / mag)


def left_normal(vector: tuple[float, float]) -> tuple[float, float]:
    """Return the left-hand normal of a 2D vector."""
    x, y = normalize_2d(vector)
    return (-y, x)


def cubic_bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    samples: int = 48,
) -> list[tuple[float, float]]:
    """Sample a cubic Bezier curve."""
    pts: list[tuple[float, float]] = []
    for t in linspace(0.0, 1.0, samples):
        u = 1.0 - t
        x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def rescale_points(
    points: Iterable[tuple[float, float]],
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    width: float,
    height: float,
    center: tuple[float, float] = (0.0, 0.0),
) -> list[np.ndarray]:
    """Map model-space 2D points into Manim coordinates."""
    x0, x1 = x_range
    y0, y1 = y_range
    cx, cy = center
    mapped = []
    for x, y in points:
        sx = ((x - x0) / (x1 - x0) - 0.5) * width + cx
        sy = ((y - y0) / (y1 - y0) - 0.5) * height + cy
        mapped.append(np.array([sx, sy, 0.0]))
    return mapped


def clamp(value: float, low: float, high: float) -> float:
    """Clamp value to a closed interval."""
    return max(low, min(high, value))

