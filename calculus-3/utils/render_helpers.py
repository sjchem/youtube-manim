"""Safe-frame, pacing, and field-sampling helpers for mobile-readable compositions."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import Mobject

import config as cfg


def fit_to_safe_frame(mobject: Mobject, padding: float = 0.25) -> Mobject:
    """Shrink a mobject until it fits the central safe zone, never enlarge it."""
    max_width = cfg.SAFE_WIDTH - 2 * padding
    max_height = cfg.SAFE_HEIGHT - 2 * padding
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def is_inside_safe_frame(mobject: Mobject, tolerance: float = 0.05) -> bool:
    return mobject.width <= cfg.SAFE_WIDTH + tolerance and mobject.height <= cfg.SAFE_HEIGHT + tolerance


def slope_field_rows(
    x_range: Sequence[float],
    y_range: Sequence[float],
) -> list[list[tuple[float, float]]]:
    """Group slope-field sample points into rows, bottom row first.

    Revealing a slope field one horizontal band at a time is what makes the
    equation dy/dx = y readable: every tick in a row shares the same slope.
    """
    x_start, x_stop, x_step = x_range
    y_start, y_stop, y_step = y_range
    xs = np.arange(x_start, x_stop + 1e-9, x_step)
    ys = np.arange(y_start, y_stop + 1e-9, y_step)
    return [[(float(x), float(y)) for x in xs] for y in ys]


def disk_slice_positions(count: int, radius: float = 1.0) -> list[tuple[float, float]]:
    """Midpoints and thicknesses for `count` equal disks stacked across a sphere."""
    dx = 2.0 * radius / count
    return [(float(-radius + dx * (index + 0.5)), float(dx)) for index in range(count)]


def temperature_to_color(temperature: float, room: float = 20.0, hot: float = 90.0) -> str:
    """Blend the film's hot and cool accents by how far above room temperature a body is."""
    fraction = float(np.clip((temperature - room) / max(hot - room, 1e-9), 0.0, 1.0))
    hot_rgb = np.array([0xFF, 0x9F, 0x43], dtype=float)
    cool_rgb = np.array([0x8E, 0xD4, 0xFF], dtype=float)
    blended = cool_rgb + (hot_rgb - cool_rgb) * fraction
    return "#{:02X}{:02X}{:02X}".format(*(int(round(channel)) for channel in blended))


def growth_step_labels(values: Sequence[float]) -> list[str]:
    """Whole-organism labels for the discrete growth ladder, e.g. 100, 120, 144."""
    return [f"{int(round(value))}" for value in values]
