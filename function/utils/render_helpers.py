"""Safe-frame and layout helpers for mobile-readable compositions."""

from __future__ import annotations

from collections.abc import Sequence

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


def is_inside_safe_frame(mobject: Mobject, tolerance: float = 0.05) -> bool:
    return mobject.width <= cfg.SAFE_WIDTH + tolerance and mobject.height <= cfg.SAFE_HEIGHT + tolerance


def row_positions(count: int, span: float = 12.0, y: float = 0.0) -> list[np.ndarray]:
    """Evenly spaced centres across a horizontal band, for pipeline layouts."""
    if count == 1:
        return [np.array([0.0, y, 0.0])]
    xs = np.linspace(-span / 2, span / 2, count)
    return [np.array([float(x), y, 0.0]) for x in xs]


def column_positions(count: int, span: float = 5.4, x: float = 0.0) -> list[np.ndarray]:
    """Evenly spaced centres down a vertical band, for fan-out diagrams."""
    if count == 1:
        return [np.array([x, 0.0, 0.0])]
    ys = np.linspace(span / 2, -span / 2, count)
    return [np.array([x, float(y), 0.0]) for y in ys]


def stagger(animations: Sequence, lag: float = 0.12):
    """Convenience wrapper so scenes read as 'these, slightly apart'."""
    from manim import AnimationGroup

    return AnimationGroup(*animations, lag_ratio=lag)
