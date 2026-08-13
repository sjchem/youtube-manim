"""Pure mathematical helpers used by multiple scenes."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np


def point_on_circle(theta: float, radius: float = 1.0, center: Iterable[float] = (0, 0, 0)) -> np.ndarray:
    origin = np.asarray(tuple(center), dtype=float)
    return origin + radius * np.array([np.cos(theta), np.sin(theta), 0.0])


def wave_value(theta: float, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0, shift: float = 0.0) -> float:
    return float(amplitude * np.sin(frequency * theta + phase) + shift)


def scaled_triangle(scale: float, base: float = 4.0, height: float = 3.0) -> tuple[float, float, float]:
    """Return adjacent, opposite and hypotenuse for a scaled 3-4-5 triangle."""
    return base * scale, height * scale, 5.0 * scale


def normalized_wave(samples: np.ndarray) -> np.ndarray:
    peak = float(np.max(np.abs(samples))) if samples.size else 0.0
    return samples if peak == 0 else samples / peak
