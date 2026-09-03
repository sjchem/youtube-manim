"""Small deterministic models behind the film's motion and optimization metaphors."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class WanderingVelocity:
    """A continuously changing, always-positive velocity used in scenes 01-02.

    v(t) = base + wave_amp*sin(wave_freq*t) + ramp*t gives the hook scene a
    visibly curving velocity graph instead of a flat line — the curve is what
    makes rectangles-under-a-line insufficient and motivates Riemann sums.
    """

    base: float = 16.0
    wave_amp: float = 4.5
    wave_freq: float = 1.1
    ramp: float = 0.8

    def velocity(self, t: float) -> float:
        return self.base + self.wave_amp * np.sin(self.wave_freq * t) + self.ramp * t

    def _antiderivative(self, t: float) -> float:
        return (
            self.base * t
            - (self.wave_amp / self.wave_freq) * np.cos(self.wave_freq * t)
            + 0.5 * self.ramp * t * t
        )

    def distance(self, a: float, b: float) -> float:
        return self._antiderivative(b) - self._antiderivative(a)


@dataclass(frozen=True)
class SteadyMotion:
    """A steadily accelerating object: position and velocity in one place.

    s(t) = a*t^2 + b*t, used for the closing synthesis (scene 13) that
    replays differentiation and integration on the same motion.
    """

    a: float = 0.4
    b: float = 1.0

    def position(self, t: float) -> float:
        return self.a * t * t + self.b * t

    def velocity(self, t: float) -> float:
        return 2.0 * self.a * t + self.b


@dataclass(frozen=True)
class RiverGarden:
    """A rectangular garden against a river, fenced on three sides.

    With `fence_length` metres of fencing and the river forming the fourth
    side, area(width) is maximized exactly where its derivative is zero —
    the scene 08 optimization example.
    """

    fence_length: float = 100.0

    def height_from_width(self, width: float) -> float:
        return self.fence_length - 2.0 * width

    def area(self, width: float) -> float:
        return width * self.height_from_width(width)

    def area_derivative(self, width: float) -> float:
        return self.fence_length - 4.0 * width

    @property
    def optimal_width(self) -> float:
        return self.fence_length / 4.0

    @property
    def optimal_area(self) -> float:
        return self.area(self.optimal_width)
