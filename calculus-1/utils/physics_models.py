"""Small deterministic models behind the film's motion metaphors."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CarMotion:
    """A steadily accelerating car: position, velocity, and acceleration in one place.

    s(t) = a*t^2 + b*t models a car easing away from a light, which gives the
    hook scene a visibly curving position graph instead of a straight line —
    the curve is what makes "slope changes with time" obvious.
    """

    a: float = 0.55
    b: float = 0.4

    def position(self, t: float) -> float:
        return self.a * t * t + self.b * t

    def average_velocity(self, t: float, h: float) -> float:
        return (self.position(t + h) - self.position(t)) / h

    def velocity(self, t: float) -> float:
        return 2.0 * self.a * t + self.b

    def acceleration(self, _t: float | None = None) -> float:
        return 2.0 * self.a


@dataclass(frozen=True)
class ChangeQuantity:
    """A generic instantaneously-changing quantity, used for the montage in scene 8."""

    label: str
    unit: str
    rate_label: str
    values: tuple[float, ...]
    times: tuple[float, ...]

    def rate_between(self, i: int) -> float:
        return (self.values[i + 1] - self.values[i]) / (self.times[i + 1] - self.times[i])


TEMPERATURE = ChangeQuantity(
    label="Temperature",
    unit="°C",
    rate_label=r"\frac{dT}{dt}",
    values=(18.0, 19.4, 21.6, 24.9, 27.0),
    times=(0.0, 1.0, 2.0, 3.0, 4.0),
)

POPULATION = ChangeQuantity(
    label="Population",
    unit="individuals",
    rate_label=r"\frac{dP}{dt}",
    values=(120.0, 158.0, 210.0, 285.0, 392.0),
    times=(0.0, 1.0, 2.0, 3.0, 4.0),
)
