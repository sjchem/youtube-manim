"""Pure mathematical helpers shared by multiple scenes.

Every function that stands in for an integral or a derivative in this film
has a closed-form antiderivative computed alongside it, so every numeric
readout the animations display (a distance, an area, a slope) is exact —
never a rough numerical estimate presented as if it were precise.
"""

from __future__ import annotations

import numpy as np


# -- Scenes 01-02: a car with continuously changing speed ------------------


def velocity_curve(t: float) -> float:
    """v(t): a smoothly wandering, always-positive velocity in m/s."""
    # Keep the changing-speed example on the same physical scale as the
    # preceding constant 20 m/s example.  The earlier small 2–5 m/s curve
    # collapsed against the x-axis when it replaced the 20 m/s line.
    return 16.0 + 4.5 * np.sin(1.1 * t) + 0.8 * t


def velocity_curve_antiderivative(t: float) -> float:
    """Exact antiderivative of velocity_curve, used only to report true area/distance."""
    return 16.0 * t - (4.5 / 1.1) * np.cos(1.1 * t) + 0.4 * t * t


def distance_traveled(a: float, b: float) -> float:
    """Exact distance covered between times a and b under velocity_curve."""
    return velocity_curve_antiderivative(b) - velocity_curve_antiderivative(a)


def left_riemann_sum(func, a: float, b: float, n: int) -> float:
    """Left-endpoint Riemann sum of func on [a, b] with n equal strips."""
    dx = (b - a) / n
    xs = a + dx * np.arange(n)
    return float(np.sum(func(xs)) * dx)


# -- Scene 03: the meaning of dx --------------------------------------------


def strip_area(func, x0: float, dx: float) -> float:
    """The area f(x0) * dx of one thin rectangular strip."""
    return float(func(x0) * dx)


# -- Scene 04: the accumulation function and the Fundamental Theorem -------


def accumulation_integrand(x: float) -> float:
    """f(x): the curve whose running area builds the accumulation function A(x)."""
    return 0.5 * x + 1.6 * np.sin(0.9 * x) + 2.4


def accumulation_antiderivative(x: float) -> float:
    """Exact antiderivative F(x) of accumulation_integrand, up to a constant."""
    return 0.25 * x * x - (1.6 / 0.9) * np.cos(0.9 * x)


def accumulation_function(x: float, a: float = 0.0) -> float:
    """A(x) = integral of accumulation_integrand from a to x, computed exactly."""
    return accumulation_antiderivative(x) - accumulation_antiderivative(a)


# -- Scene 05: the simplest possible example, f(x) = x ----------------------


def identity_fn(x: float) -> float:
    """f(x) = x."""
    return x


def triangle_area(x: float) -> float:
    """A(x) = x^2 / 2, the exact area under f(x) = x from 0 to x."""
    return 0.5 * x * x


# -- Scene 06: a derivative is itself a new function -------------------------


def square_fn(x: float) -> float:
    """f(x) = x^2."""
    return x * x


def d_square_fn(x: float) -> float:
    """f'(x) = 2x, the exact derivative of square_fn."""
    return 2.0 * x


# -- Scene 07: maxima and minima ---------------------------------------------


def hill_fn(x: float) -> float:
    """A hill-shaped curve with a single interior maximum."""
    return -0.35 * x * x + 3.0


def d_hill_fn(x: float) -> float:
    """Exact derivative of hill_fn."""
    return -0.7 * x


# -- Scene 08: the fenced garden optimization --------------------------------


def garden_area(width: float, fence: float = 100.0) -> float:
    """A(x) = x(fence - 2x): area of a river-bordered rectangle of width x."""
    return width * (fence - 2.0 * width)


def d_garden_area(width: float, fence: float = 100.0) -> float:
    """Exact derivative of garden_area with respect to width."""
    return fence - 4.0 * width


def garden_optimal_width(fence: float = 100.0) -> float:
    """The width where d_garden_area equals zero."""
    return fence / 4.0


# -- Scene 09: reversing differentiation, and the mystery of +C --------------


def linear_velocity(t: float) -> float:
    """v(t) = 2t, chosen so integrating it by hand is immediate."""
    return 2.0 * t


def position_family(t: float, constant: float = 0.0) -> float:
    """s(t) = t^2 + C: every antiderivative of linear_velocity."""
    return t * t + constant


# -- Scene 10: substitution as a change of coordinates ------------------------


def substitution_integrand(x: float) -> float:
    """2x cos(x^2): the integrand that motivates u = x^2."""
    return 2.0 * x * np.cos(x * x)


def substitution_inner(x: float) -> float:
    """u = x^2, the inner function substitution renames as a new variable."""
    return x * x


# -- Scene 12: the area between two curves -------------------------------------


def upper_curve(x: float) -> float:
    """f(x): the higher of the two curves bounding the shaded region."""
    return -0.4 * x * x + 3.6


def lower_curve(x: float) -> float:
    """g(x): the lower of the two curves bounding the shaded region."""
    return 0.35 * x - 0.6


# -- Scene 13: position, velocity, and accumulated displacement ---------------


def position_profile(t: float) -> float:
    """s(t): position of a steadily accelerating object."""
    return 0.4 * t * t + 1.0 * t


def velocity_profile(t: float) -> float:
    """v(t) = s'(t): exact velocity of position_profile."""
    return 0.8 * t + 1.0
