"""Safe-frame fitting, deterministic sampling, and pacing helpers.

These functions keep the composition mobile-readable and every render
reproducible. They depend on `config` for the frame, but never on Manim's
scene machinery, so the audit tools can call them freely.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import Mobject

import config as cfg


def fit_to_safe_frame(mobject: Mobject, padding: float = 0.25) -> Mobject:
    """Shrink a mobject until it fits the central safe zone; never enlarge it."""
    max_width = cfg.SAFE_WIDTH - 2 * padding
    max_height = cfg.SAFE_HEIGHT - 2 * padding
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def fit_to_width(mobject: Mobject, limit: float) -> Mobject:
    """Shrink a mobject to a width limit; never enlarge it.

    This is the single most repeated gesture in the film: a caption or a formula
    is composed at an authored point size, then held to the safe frame so it
    stays inside the picture on a phone.
    """
    if mobject.width > limit:
        mobject.scale_to_fit_width(limit)
    return mobject


def lattice_points(rows: int, columns: int, spacing: float, jitter: float = 0.0, seed: int = cfg.SEED) -> list[tuple[float, float]]:
    """A staggered atomic lattice for the gold foil, deterministic under `seed`."""
    rng = np.random.default_rng(seed)
    points: list[tuple[float, float]] = []
    for row in range(rows):
        offset = 0.5 * spacing * (row % 2)
        for column in range(columns):
            x = (column - (columns - 1) / 2) * spacing + offset
            y = (row - (rows - 1) / 2) * spacing
            if jitter:
                x += float(rng.uniform(-jitter, jitter))
                y += float(rng.uniform(-jitter, jitter))
            points.append((float(x), float(y)))
    return points


def spectrum_positions(
    wavelengths: Sequence[float],
    low_nm: float,
    high_nm: float,
    bar_width: float,
) -> list[float]:
    """Map wavelengths onto x-offsets along a spectrum bar centred on the origin.

    Every chapter that draws a line spectrum needs exactly this mapping, and a
    line drawn at a different offset from the tick that labels it is a lie about
    a number, so it lives in one place.
    """
    span = high_nm - low_nm
    return [float((wavelength - low_nm) / span - 0.5) * bar_width for wavelength in wavelengths]
