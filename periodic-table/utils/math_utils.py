"""Small numerical helpers: real spherical harmonics and layout arithmetic.

The 3D orbital silhouettes in this film are polar plots of the *angular*
probability density ``|Y_lm(theta, phi)|^2`` — the distance from the centre in
each direction is proportional to how likely the electron is to be found in
that direction. That is the familiar sphere / dumbbell / clover / f-flower
family. Part 2 drew full isodensity surfaces including the radial part; here
only the angular shape matters, because the shape is what tells the families
apart and the count of orientations is what sets the table's widths.

Nothing in this module imports Manim.
"""

from __future__ import annotations

from math import factorial, pi, sqrt

import numpy as np
from scipy.special import lpmv


def real_spherical_harmonic(l: int, m: int, theta, phi):
    """Normalized real spherical harmonic. ``theta`` is polar, ``phi`` azimuthal.

    Uses the same sign convention as Part 2's renderer (no Condon–Shortley
    removal), so a lobe that was cyan there is cyan here.
    """
    if not (l >= 0 and -l <= m <= l):
        raise ValueError("Require l >= 0 and |m| <= l")
    k = abs(m)
    norm = sqrt((2 * l + 1) / (4 * pi) * factorial(l - k) / factorial(l + k))
    base = norm * lpmv(k, l, np.cos(theta))
    if m > 0:
        return sqrt(2) * base * np.cos(k * phi)
    if m < 0:
        return sqrt(2) * base * np.sin(k * phi)
    return base


def angular_density_radius(l: int, m: int, theta, phi):
    """Polar radius of the angular-density silhouette, scaled to peak at 1."""
    value = real_spherical_harmonic(l, m, theta, phi) ** 2
    theta_grid, phi_grid = np.meshgrid(np.linspace(0, pi, 181), np.linspace(0, 2 * pi, 361))
    peak = float((real_spherical_harmonic(l, m, theta_grid, phi_grid) ** 2).max())
    return value / peak


def direction_sign(l: int, m: int, direction) -> float:
    """Sign of Y_lm along a Cartesian direction (used to colour the lobes)."""
    x, y, z = np.asarray(direction, dtype=float)
    r = float(np.sqrt(x * x + y * y + z * z))
    if r < 1e-12:
        return 1.0
    theta = np.arccos(np.clip(z / r, -1.0, 1.0))
    phi = np.arctan2(y, x)
    return 1.0 if real_spherical_harmonic(l, m, theta, phi) >= 0 else -1.0


def sunflower_points(count: int, spacing: float) -> np.ndarray:
    """Evenly packed points in a disc (Vogel's spiral), for drawing nuclei.

    Deterministic, so a nucleus of 79 protons is the same picture every render.
    """
    golden = pi * (3 - sqrt(5))
    index = np.arange(count)
    radius = spacing * np.sqrt(index + 0.5)
    angle = index * golden
    return np.stack([radius * np.cos(angle), radius * np.sin(angle), np.zeros(count)], axis=1)


def linear_map(value: float, source: tuple[float, float], target: tuple[float, float]) -> float:
    """Map ``value`` from one interval to another (no clamping)."""
    (a, b), (c, d) = source, target
    return c + (value - a) * (d - c) / (b - a)
