"""Motion helpers for statistics-as-geometry animations."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def spring_offsets(values: Sequence[float], center: float, strength: float = 0.18) -> list[float]:
    """Return horizontal offsets that can visualize deviation as a spring pull."""
    return [(value - center) * strength for value in values]


def normalized_positions(values: Sequence[float]) -> list[float]:
    """Map values to z-score-like positions for scaling demonstrations."""
    array = np.array(values, dtype=float)
    std = float(array.std())
    if std == 0:
        return [0.0 for _ in values]
    return list((array - float(array.mean())) / std)
