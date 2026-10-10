"""Small numerical helpers: colour scales, 3D rotation and projection, density fields.

Nothing in this module imports Manim, so every function can be checked with
plain numbers: ``python -m utils.math_utils``.
"""

from __future__ import annotations

from math import pi, sqrt

import numpy as np


def linear_map(value: float, source: tuple[float, float], target: tuple[float, float]) -> float:
    """Map ``value`` from one interval to another (no clamping)."""
    (a, b), (c, d) = source, target
    return c + (value - a) * (d - c) / (b - a)


def unit_interval(value: float, low: float, high: float) -> float:
    """Where ``value`` sits between ``low`` and ``high``, clamped to [0, 1]."""
    if high == low:
        return 0.0
    return float(min(1.0, max(0.0, (value - low) / (high - low))))


def smoothstep(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------------------
# Colour scales (hex in, hex out)
# ---------------------------------------------------------------------------


def _hex_to_rgb(colour: str) -> tuple[float, float, float]:
    colour = colour.lstrip("#")
    return tuple(int(colour[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def _rgb_to_hex(rgb) -> str:
    return "#" + "".join(f"{round(min(1.0, max(0.0, c)) * 255):02X}" for c in rgb)


def scale_color(t: float, stops) -> str:
    """Piecewise-linear colour along evenly spaced hex ``stops``; t in [0, 1]."""
    t = min(1.0, max(0.0, float(t)))
    position = t * (len(stops) - 1)
    index = min(int(position), len(stops) - 2)
    frac = position - index
    a, b = _hex_to_rgb(stops[index]), _hex_to_rgb(stops[index + 1])
    return _rgb_to_hex([x + (y - x) * frac for x, y in zip(a, b)])


# ---------------------------------------------------------------------------
# 3D rotation and orthographic projection, for the hand-projected clouds and
# crystal (cheap in Cairo: no lit surfaces, just dots drawn back to front)
# ---------------------------------------------------------------------------


def rotation_y(angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rotation_x(angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def turn_and_tilt(points: np.ndarray, turn: float, tilt: float) -> np.ndarray:
    """Spin points about the vertical axis, then tip the view by ``tilt``."""
    return points @ (rotation_x(tilt) @ rotation_y(turn)).T


def depth_fade(depth: np.ndarray, reach: float, near: float = 1.0, far: float = 0.28) -> np.ndarray:
    """Opacity per point: nearer (positive depth, toward the viewer) is brighter."""
    t = np.clip((depth / max(reach, 1e-9) + 1) / 2, 0, 1)
    return far + (near - far) * t


def perspective(depth: np.ndarray, distance: float = 9.0) -> np.ndarray:
    """Size factor for a gentle perspective: nearer points draw slightly larger."""
    return distance / np.maximum(distance - depth, 1e-3)


# ---------------------------------------------------------------------------
# Layout and density fields
# ---------------------------------------------------------------------------


def sunflower_points(count: int, spacing: float) -> np.ndarray:
    """Evenly packed points in a disc (Vogel's spiral). Deterministic."""
    golden = pi * (3 - sqrt(5))
    index = np.arange(count)
    radius = spacing * np.sqrt(index + 0.5)
    angle = index * golden
    return np.stack([radius * np.cos(angle), radius * np.sin(angle), np.zeros(count)], axis=1)


def ring_points(count: int, radius: float, phase: float = 0.0) -> np.ndarray:
    angles = phase + np.arange(count) * 2 * pi / count
    return np.stack([radius * np.cos(angles), radius * np.sin(angles), np.zeros(count)], axis=1)


def bond_density(x, y, separation: float, lean: float, width: float = 0.55):
    """A schematic two-atom electron density, for the 3D bond landscape.

    Two atomic humps at x = -separation/2 and +separation/2 plus a shared
    "bond" hump between them. ``lean`` in [-1, 1] slides the shared density
    from the left atom (-1) to the right atom (+1) and makes the receiving
    atom's hump taller. It is an illustration of unequal sharing, not a
    computed molecular density.
    """
    half = separation / 2
    lean = float(np.clip(lean, -1, 1))
    left = (1 - 0.45 * lean) * np.exp(-((x + half) ** 2 + y ** 2) / (2 * width ** 2))
    right = (1 + 0.45 * lean) * np.exp(-((x - half) ** 2 + y ** 2) / (2 * width ** 2))
    centre = lean * half * 0.95
    shared = 0.8 * np.exp(-((x - centre) ** 2) / (2 * (0.5 * width + 0.35 * half) ** 2) - y ** 2 / (2 * (0.8 * width) ** 2))
    return left + right + shared


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    check(scale_color(0, ("#000000", "#FFFFFF")) == "#000000", "scale start")
    check(scale_color(1, ("#000000", "#FFFFFF")) == "#FFFFFF", "scale end")
    check(scale_color(0.5, ("#000000", "#FFFFFF")) in {"#7F7F7F", "#808080"}, "scale middle")
    check(unit_interval(5, 0, 10) == 0.5 and unit_interval(-1, 0, 10) == 0.0, "unit interval")
    p = np.array([[1.0, 0, 0]])
    check(np.allclose(turn_and_tilt(p, pi / 2, 0), [[0, 0, -1]]), "quarter turn about the vertical")
    check(np.allclose(np.linalg.norm(turn_and_tilt(np.eye(3), 0.7, 0.3), axis=1), 1), "rotations keep length")
    fade = depth_fade(np.array([-1.0, 0.0, 1.0]), 1.0)
    check(fade[0] < fade[1] < fade[2], "nearer points are brighter")
    xs = np.linspace(-3, 3, 601)
    even = bond_density(xs, 0, 2.0, 0.0)
    check(np.allclose(even, even[::-1]), "zero lean must be symmetric")
    leaning = bond_density(xs, 0, 2.0, 0.8)
    check(float((xs * leaning).sum() / leaning.sum()) > 0.2, "positive lean moves density to the right atom")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Maths check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("Maths check passed: colour scale, rotations, depth fade and the bond-density illustration.")
