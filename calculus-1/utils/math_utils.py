"""Pure mathematical helpers shared by multiple scenes."""

from __future__ import annotations

import numpy as np


def square(x: float) -> float:
    """f(x) = x^2, used for the limit and secant/tangent chapters."""
    return x * x


def d_square(x: float) -> float:
    """Exact derivative of x^2, used only to draw analytic tangent lines."""
    return 2.0 * x


def cubic_wiggle(x: float) -> float:
    """f(x) = x^3 - x, used for the local-linearity zoom."""
    return x**3 - x


def d_cubic_wiggle(x: float) -> float:
    """Exact derivative of x^3 - x."""
    return 3.0 * x**2 - 1.0


def removable_hole(x: float) -> float:
    """f(x) = (x^2 - 1) / (x - 1), undefined exactly at x = 1."""
    if abs(x - 1.0) < 1e-9:
        raise ValueError("removable_hole is undefined at x = 1")
    return (x**2 - 1.0) / (x - 1.0)


def removable_hole_simplified(x: float) -> float:
    """The algebraically simplified form x + 1, valid everywhere including x = 1."""
    return x + 1.0


def secant_slope(func, x0: float, h: float) -> float:
    """Average rate of change of func over [x0, x0 + h]."""
    return (func(x0 + h) - func(x0)) / h


def approaching_sequence(target: float, steps: tuple[float, ...]) -> list[float]:
    """Build an explicit sequence of inputs marching toward a target value."""
    return [target - step for step in steps]


def car_position(t: float, a: float = 0.55, b: float = 0.4) -> float:
    """Position of the demonstration car: s(t) = a*t^2 + b*t (steadily accelerating)."""
    return a * t * t + b * t


def car_velocity(t: float, a: float = 0.55, b: float = 0.4) -> float:
    """Exact instantaneous velocity s'(t) = 2*a*t + b, used only to draw the tangent."""
    return 2.0 * a * t + b


def sinc_ratio(x: float) -> float:
    """sin(x)/x with the removable point at x = 0 filled by its limit, 1."""
    if abs(x) < 1e-9:
        return 1.0
    return float(np.sin(x) / x)


def squeeze_bounds(x: float) -> tuple[float, float, float]:
    """Return (cos x, sin x / x, 1) — the squeeze theorem's three quantities near 0."""
    return float(np.cos(x)), sinc_ratio(x), 1.0


def local_linear_approx(func, dfunc, x0: float, dx: float) -> float:
    """First-order Taylor estimate f(x0) + f'(x0) * dx."""
    return func(x0) + dfunc(x0) * dx
