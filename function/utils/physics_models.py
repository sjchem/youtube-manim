"""Small physical / statistical models that the closing chapters visualise.

These are deliberately simple closed-form models. Nothing here is fitted to
real data; they exist to make an abstract point concrete on screen.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

# --- time in, position out ---------------------------------------------------

FALL_G = 9.81


def projectile_height(t: float, v0: float = 12.0, h0: float = 0.0) -> float:
    """h(t) = h0 + v0 t - g t^2 / 2, the archetypal 'time in, position out' rule."""
    return h0 + v0 * t - 0.5 * FALL_G * t * t


def projectile_velocity(t: float, v0: float = 12.0) -> float:
    """The exact derivative of projectile_height: how fast the output is changing."""
    return v0 - FALL_G * t


def spring_position(t: float, amplitude: float = 1.6, omega: float = 1.9) -> float:
    """x(t) = A cos(omega t): a second 'one input, one output' physical rule."""
    return amplitude * float(np.cos(omega * t))


# --- data in, probability out ------------------------------------------------


def logistic(x: float, slope: float = 1.4, midpoint: float = 0.0) -> float:
    """P(Y = 1 | x) for a logistic model: a rule whose outputs live in (0, 1)."""
    return 1.0 / (1.0 + float(np.exp(-slope * (x - midpoint))))


# --- a two-input rule, and learning as walking downhill ----------------------


def loss_surface(x: float, y: float) -> float:
    """A smooth two-input rule z = f(x, y) with one clear valley and one ridge.

    Used as a *metaphor* for a machine-learning loss landscape: the shape is
    invented, but the behaviour it illustrates - a rule that turns two numbers
    into one, and an algorithm that walks downhill on it - is real.
    """
    bowl = 0.24 * (x * x + y * y)
    valley = -2.4 * float(np.exp(-((x - 1.1) ** 2 + (y - 0.7) ** 2) / 1.1))
    ridge = 1.5 * float(np.exp(-((x + 1.4) ** 2 + (y + 1.0) ** 2) / 1.6))
    ripple = 0.28 * float(np.sin(1.5 * x) * np.cos(1.5 * y))
    return bowl + valley + ridge + ripple


def loss_gradient(x: float, y: float, step: float = 1e-4) -> tuple[float, float]:
    """Central-difference gradient of loss_surface, accurate enough to animate."""
    dx = (loss_surface(x + step, y) - loss_surface(x - step, y)) / (2 * step)
    dy = (loss_surface(x, y + step) - loss_surface(x, y - step)) / (2 * step)
    return (float(dx), float(dy))


def descent_path(
    start: Sequence[float],
    steps: int = 60,
    learning_rate: float = 0.28,
) -> list[tuple[float, float, float]]:
    """Plain gradient descent on loss_surface, returned as (x, y, z) points."""
    x, y = float(start[0]), float(start[1])
    path = [(x, y, loss_surface(x, y))]
    for _ in range(steps):
        dx, dy = loss_gradient(x, y)
        x -= learning_rate * dx
        y -= learning_rate * dy
        path.append((x, y, loss_surface(x, y)))
    return path


def surface_bounds(
    x_range: Sequence[float] = (-3.0, 3.0),
    y_range: Sequence[float] = (-3.0, 3.0),
    samples: int = 41,
) -> tuple[float, float]:
    """Min and max height of loss_surface over a box, for choosing an axis range."""
    xs = np.linspace(x_range[0], x_range[1], samples)
    ys = np.linspace(y_range[0], y_range[1], samples)
    values = np.array([[loss_surface(float(x), float(y)) for x in xs] for y in ys])
    return (float(values.min()), float(values.max()))
