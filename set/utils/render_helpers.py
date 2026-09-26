"""Safe-frame and layout helpers for mobile-readable compositions.

Every caption, title and boxed statement in the film passes through
``fit_width`` or ``fit_to_safe_frame``, so nothing can silently grow past the
central safe zone when its text changes.
"""

from __future__ import annotations

import numpy as np
from manim import Mobject

import config as cfg


def fit_to_safe_frame(mobject: Mobject, padding: float = 0.25) -> Mobject:
    """Shrink a mobject until it fits the central safe zone, never enlarging it."""
    max_width = cfg.SAFE_WIDTH - 2 * padding
    max_height = cfg.SAFE_HEIGHT - 2 * padding
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def fit_width(mobject: Mobject, max_width: float) -> Mobject:
    """Constrain width only — used for captions and single-line equations."""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


def fit_inside(mobject: Mobject, max_width: float, max_height: float) -> Mobject:
    """Constrain a mobject to a named box, e.g. the inside of a set boundary."""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def is_inside_safe_frame(mobject: Mobject, tolerance: float = 0.05) -> bool:
    """True when a mobject already fits the safe zone unscaled."""
    return mobject.width <= cfg.SAFE_WIDTH + tolerance and mobject.height <= cfg.SAFE_HEIGHT + tolerance


def row_positions(count: int, span: float = 12.0, y: float = 0.0) -> list[np.ndarray]:
    """Evenly spaced centres across a horizontal band, for card rows."""
    if count == 1:
        return [np.array([0.0, y, 0.0])]
    xs = np.linspace(-span / 2, span / 2, count)
    return [np.array([float(x), y, 0.0]) for x in xs]


def column_positions(count: int, span: float = 5.4, x: float = 0.0) -> list[np.ndarray]:
    """Evenly spaced centres down a vertical band, for stacked panels."""
    if count == 1:
        return [np.array([x, 0.0, 0.0])]
    ys = np.linspace(span / 2, -span / 2, count)
    return [np.array([x, float(y), 0.0]) for y in ys]


def grid_positions(
    count: int,
    columns: int,
    *,
    x_step: float = 1.6,
    y_step: float = 1.6,
    center: tuple[float, float] = (0.0, 0.0),
) -> list[np.ndarray]:
    """Centres of a centred grid, for a scattered board of object cards."""
    rows = int(np.ceil(count / columns))
    points: list[np.ndarray] = []
    for index in range(count):
        row, column = divmod(index, columns)
        in_row = min(columns, count - row * columns)
        x = center[0] + (column - (in_row - 1) / 2) * x_step
        y = center[1] - (row - (rows - 1) / 2) * y_step
        points.append(np.array([x, y, 0.0]))
    return points
