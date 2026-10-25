"""Small numerical helpers: vectors, rotations, projection, hulls, ellipsoids.

Nothing in this module imports Manim, so every function can be checked with
plain numbers: ``python -m utils.math_utils``.

Coordinates follow Manim's screen convention: x to the right, y up, and z
toward the viewer. The film's 3D stage turns a molecule with ``view_rotation``
(yaw about the vertical, then pitch about the horizontal) and projects it with
a gentle perspective.
"""

from __future__ import annotations

from math import acos, degrees, sqrt

import numpy as np


def unit(vector) -> np.ndarray:
    v = np.asarray(vector, dtype=float)
    n = float(np.linalg.norm(v))
    if n < 1e-12:
        raise ValueError("cannot normalise a zero vector")
    return v / n


def angle_deg(a, b) -> float:
    """Angle between two directions, in degrees."""
    c = float(np.clip(np.dot(unit(a), unit(b)), -1.0, 1.0))
    return degrees(acos(c))


def slerp(a, b, t: float) -> np.ndarray:
    """Spherical interpolation between two unit directions (stays on the sphere)."""
    a, b = unit(a), unit(b)
    c = float(np.clip(np.dot(a, b), -1.0, 1.0))
    if c > 0.9999:
        return unit(a + (b - a) * t)
    if c < -0.9999:
        # Opposite directions: go round through any perpendicular.
        side = unit(np.cross(a, [0.0, 0.0, 1.0] if abs(a[2]) < 0.9 else [1.0, 0.0, 0.0]))
        angle = np.pi * t
        return unit(a * np.cos(angle) + side * np.sin(angle))
    omega = np.arccos(c)
    return (np.sin((1 - t) * omega) * a + np.sin(t * omega) * b) / np.sin(omega)


def linear_map(value: float, source: tuple[float, float], target: tuple[float, float]) -> float:
    """Map ``value`` from one interval to another (no clamping)."""
    (a, b), (c, d) = source, target
    return c + (value - a) * (d - c) / (b - a)


def smoothstep(t: float) -> float:
    t = min(1.0, max(0.0, float(t)))
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------------------
# Rotations
# ---------------------------------------------------------------------------


def rotation_x(angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rotation_y(angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rotation_z(angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def rotation_about(axis, angle: float) -> np.ndarray:
    """Rodrigues' rotation matrix about ``axis`` by ``angle`` (right-handed)."""
    k = unit(axis)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)


def rotation_between(a, b) -> np.ndarray:
    """The smallest rotation taking direction ``a`` onto direction ``b``."""
    a, b = unit(a), unit(b)
    axis = np.cross(a, b)
    s = float(np.linalg.norm(axis))
    c = float(np.dot(a, b))
    if s < 1e-10:
        if c > 0:
            return np.eye(3)
        side = np.cross(a, [1.0, 0.0, 0.0])
        if np.linalg.norm(side) < 1e-6:
            side = np.cross(a, [0.0, 1.0, 0.0])
        return rotation_about(side, np.pi)
    return rotation_about(axis, np.arctan2(s, c))


def view_rotation(yaw: float, pitch: float) -> np.ndarray:
    """Turn a model by ``yaw`` about the vertical, then tip it toward the
    viewer by ``pitch`` (positive pitch shows more of the top)."""
    return rotation_x(pitch) @ rotation_y(yaw)


def perspective(depth: np.ndarray, distance: float = 14.0) -> np.ndarray:
    """Size factor for a gentle perspective: nearer (larger z) draws larger."""
    return distance / np.maximum(distance - np.asarray(depth, dtype=float), 1e-3)


def frame_from_axis(axis) -> np.ndarray:
    """An orthonormal frame (columns e1, e2, axis) whose third column is ``axis``."""
    w = unit(axis)
    helper = np.array([0.0, 1.0, 0.0]) if abs(w[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = unit(np.cross(helper, w))
    v = np.cross(w, u)
    return np.column_stack([u, v, w])


# ---------------------------------------------------------------------------
# Projected shapes
# ---------------------------------------------------------------------------


def projected_ellipse(axes: np.ndarray) -> np.ndarray:
    """2x2 matrix mapping the unit circle onto the outline of a projected ellipsoid.

    ``axes`` is 3x3 with the ellipsoid's semi-axes as columns, already in
    view coordinates. Under orthographic projection the ellipsoid
    {A u : |u| <= 1} becomes the ellipse {P u}, P = A[:2]; its outline is
    the unit circle mapped by the symmetric square root of P P^T (using the
    symmetric root keeps the shading from flipping as the ellipse turns).
    """
    P = np.asarray(axes, dtype=float)[:2]
    S = P @ P.T
    values, vectors = np.linalg.eigh(S)
    return vectors @ np.diag(np.sqrt(np.maximum(values, 0.0))) @ vectors.T


try:  # SciPy's Qhull is ~50x faster than the pure-Python chain below.
    from scipy.spatial import ConvexHull as _Qhull
except ImportError:  # pragma: no cover - SciPy is optional
    _Qhull = None


def convex_hull_2d(points: np.ndarray) -> np.ndarray:
    """Convex hull of (N, 2) points, counter-clockwise (Qhull when available)."""
    pts = np.asarray(points, dtype=float)[:, :2]
    if _Qhull is not None and len(pts) >= 4:
        try:
            return pts[_Qhull(pts).vertices]
        except Exception:  # degenerate input (e.g. collinear): fall back
            pass
    return _monotone_chain(pts)


def _monotone_chain(points: np.ndarray) -> np.ndarray:
    """Andrew's monotone-chain hull of (N, 2) points, counter-clockwise."""
    pts = np.unique(np.round(np.asarray(points, dtype=float)[:, :2], 9), axis=0)
    if len(pts) <= 2:
        return pts
    order = np.lexsort((pts[:, 1], pts[:, 0]))
    pts = pts[order]

    def build(sequence):
        chain: list[np.ndarray] = []
        for p in sequence:
            while len(chain) >= 2:
                a, b = chain[-2], chain[-1]
                if (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) > 1e-12:
                    break
                chain.pop()
            chain.append(p)
        return chain

    lower = build(pts)
    upper = build(pts[::-1])
    return np.array(lower[:-1] + upper[:-1])


def polygon_area(points: np.ndarray) -> float:
    x, y = points[:, 0], points[:, 1]
    return 0.5 * float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


# ---------------------------------------------------------------------------
# Colour
# ---------------------------------------------------------------------------


def _hex_to_rgb(colour: str) -> tuple[float, float, float]:
    colour = colour.lstrip("#")
    return tuple(int(colour[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def _rgb_to_hex(rgb) -> str:
    return "#" + "".join(f"{round(min(1.0, max(0.0, c)) * 255):02X}" for c in rgb)


def mix(a: str, b: str, t: float) -> str:
    """Blend two hex colours (t = 0 gives a, t = 1 gives b)."""
    x, y = _hex_to_rgb(a), _hex_to_rgb(b)
    return _rgb_to_hex([p + (q - p) * t for p, q in zip(x, y)])


def shade(colour: str, factor: float) -> str:
    """Scale a colour's brightness (factor < 1 darkens)."""
    return _rgb_to_hex([c * factor for c in _hex_to_rgb(colour)])


def luminance(colour: str) -> float:
    r, g, b = _hex_to_rgb(colour)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    check(abs(angle_deg([1, 0, 0], [0, 1, 0]) - 90) < 1e-9, "right angle")
    check(abs(angle_deg([1, 1, 1], [1, -1, -1]) - degrees(acos(-1 / 3))) < 1e-9, "cube-corner angle")
    for t in (0.0, 0.3, 1.0):
        check(abs(np.linalg.norm(slerp([1, 0, 0], [0, 0, 1], t)) - 1) < 1e-9, "slerp stays on the sphere")
    check(np.allclose(slerp([1, 0, 0], [-1, 0, 0], 0.5) @ [1, 0, 0], 0, atol=1e-9), "slerp through opposite")
    R = rotation_about([1, 2, 3], 0.7)
    check(np.allclose(R @ R.T, np.eye(3)) and abs(np.linalg.det(R) - 1) < 1e-9, "Rodrigues is a rotation")
    check(np.allclose(rotation_between([0, 1, 0], [1, 0, 0]) @ [0, 1, 0], [1, 0, 0]), "rotation between")
    check(np.allclose(rotation_between([0, 1, 0], [0, -1, 0]) @ [0, 1, 0], [0, -1, 0]), "rotation to opposite")
    check(np.allclose(view_rotation(np.pi / 2, 0) @ [1, 0, 0], [0, 0, -1]), "quarter yaw turns x away")
    F = frame_from_axis([0.3, -0.2, 0.9])
    check(np.allclose(F.T @ F, np.eye(3)), "orthonormal frame")
    # A sphere of radius 2 must project to a circle of radius 2 from any view.
    E = projected_ellipse(view_rotation(0.4, 0.9) @ (2 * np.eye(3)))
    check(np.allclose(E, 2 * np.eye(2)), "sphere projects to a circle")
    # A needle along the line of sight projects to (almost) nothing.
    E = projected_ellipse(np.diag([0.0, 0.0, 3.0]))
    check(np.allclose(E, 0), "needle along the view collapses")
    square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0.5], [0.2, 0.7]])
    hull = convex_hull_2d(square)
    check(len(hull) == 4 and abs(polygon_area(hull) - 1) < 1e-9, "hull of a square")
    slow = _monotone_chain(square)
    check(len(slow) == 4 and abs(polygon_area(slow) - 1) < 1e-9, "fallback hull of a square")
    check(mix("#000000", "#FFFFFF", 0.5) in {"#7F7F7F", "#808080"}, "colour mix")
    check(abs(perspective(np.array([0.0]))[0] - 1) < 1e-12, "no perspective at depth 0")
    check(sqrt(3) ** 2 - 3 < 1e-12, "sanity")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Maths check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("Maths check passed: angles, slerp, rotations, projection, ellipsoids, hull, colour.")
