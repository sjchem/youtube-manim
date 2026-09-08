"""Pure mathematical helpers shared by several chapters.

Every function here is exact and independently testable, so that no scene ever
has to invent its own arithmetic on the fly.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

Real = Callable[[float], float]


# --- the film's small cast of rules -----------------------------------------


def double(x: float) -> float:
    """f(x) = 2x — the very first machine the viewer meets."""
    return 2.0 * x


def half(x: float) -> float:
    """The inverse of double: f^-1(x) = x / 2."""
    return x / 2.0


def square(x: float) -> float:
    """f(x) = x^2 — the workhorse of the graphing, testing and inverse chapters."""
    return x * x


def plus_two(x: float) -> float:
    """f(x) = x + 2 — the first machine in the composition pipeline."""
    return x + 2.0


def root(x: float) -> float:
    """The inverse of x^2 restricted to x >= 0."""
    if x < 0:
        raise ValueError("root is defined here only for x >= 0")
    return float(np.sqrt(x))


def circle_area(r: float) -> float:
    """A(r) = pi r^2 — the physical example behind domain and range."""
    return float(np.pi * r * r)


def celsius_to_fahrenheit(c: float) -> float:
    """The everyday converter from the opening chapter: F = 9C/5 + 32."""
    return 9.0 * c / 5.0 + 32.0


# --- composition -------------------------------------------------------------


def compose(outer: Real, inner: Real) -> Real:
    """Return the single rule that is 'inner first, then outer': x -> outer(inner(x))."""

    def composed(x: float) -> float:
        return outer(inner(x))

    return composed


def square_after_plus_two(x: float) -> float:
    """g(f(x)) = (x + 2)^2."""
    return (x + 2.0) ** 2


def plus_two_after_square(x: float) -> float:
    """f(g(x)) = x^2 + 2."""
    return x * x + 2.0


# --- transformations ---------------------------------------------------------


def transformed_parabola(a: float = 1.0, h: float = 0.0, k: float = 0.0) -> Real:
    """The family a(x - h)^2 + k, driving the whole transformation chapter."""

    def curve(x: float) -> float:
        return a * (x - h) ** 2 + k

    return curve


def parabola_window(
    a: float,
    h: float,
    k: float,
    *,
    y_min: float,
    y_max: float,
    x_min: float,
    x_max: float,
) -> tuple[float, float]:
    """Clamp the plotted x-range so a(x - h)^2 + k never leaves the visible box.

    Returned as (left, right); always a non-degenerate interval so that
    Axes.plot cannot be handed an empty range mid-animation.
    """
    if abs(a) < 1e-9:
        return (x_min, x_max)
    limit = y_max if a > 0 else y_min
    span = (limit - k) / a
    if span <= 0:
        # The vertex itself is already outside the box: draw a thin sliver at h.
        left, right = h - 0.05, h + 0.05
    else:
        reach = float(np.sqrt(span))
        left, right = h - reach, h + reach
    left = max(left, x_min)
    right = min(right, x_max)
    if right - left < 0.1:
        centre = min(max(h, x_min + 0.05), x_max - 0.05)
        left, right = centre - 0.05, centre + 0.05
    return (float(left), float(right))


# --- tables and samples ------------------------------------------------------


def sample_pairs(func: Real, inputs: Sequence[float]) -> list[tuple[float, float]]:
    """Every (input, output) pair for the given rule — literally what a graph is."""
    return [(float(x), float(func(x))) for x in inputs]


def format_number(value: float) -> str:
    """Render a number the way it should be spoken: 4 not 4.0, -0.5 not -0.50."""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def pair_tex(x: float, y: float) -> str:
    """LaTeX for the ordered pair (x, f(x))."""
    return rf"\left({format_number(x)},\,{format_number(y)}\right)"


def reflect_across_identity(point: Sequence[float]) -> tuple[float, float]:
    """(a, b) -> (b, a): the algebra behind reflecting a graph in y = x."""
    return (float(point[1]), float(point[0]))


def identity_reflection_matrix() -> np.ndarray:
    """The 2x2 matrix that swaps coordinates, for ApplyMatrix animations."""
    return np.array([[0.0, 1.0], [1.0, 0.0]])
