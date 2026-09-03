"""Small deterministic models behind the film's physical examples.

Each dataclass owns one differential equation, its exact solution where a
closed form exists, and the derived quantities the animations put on screen.
Scenes ask these models for numbers rather than hard-coding them, so a value
shown in the picture and a value spoken in the narration cannot drift apart.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from utils.math_utils import integrate_ode


@dataclass(frozen=True)
class AcceleratingCar:
    """A car whose speedometer reads v(t) = rate * t and nothing else.

    The opening chapter shows only the velocity and asks the audience to
    rebuild the position, so both halves live together here.
    """

    rate: float = 2.0

    def velocity(self, t: float) -> float:
        return self.rate * t

    def displacement(self, t: float, constant: float = 0.0) -> float:
        """s(t) = (rate/2) t^2 + C, the exact antiderivative of `velocity`."""
        return 0.5 * self.rate * t * t + constant

    def area_under_velocity(self, a: float, b: float) -> float:
        return self.displacement(b) - self.displacement(a)


@dataclass(frozen=True)
class ProportionalProcess:
    """dQ/dt = k Q — one equation that grows or decays with the sign of k.

    Scenes 05 and 06 use the same class with opposite rates so the "same
    mathematics, opposite worlds" comparison is literally the same code.
    """

    initial: float = 100.0
    rate: float = 0.1823

    def derivative(self, quantity: float) -> float:
        return self.rate * quantity

    def value(self, t: float) -> float:
        return self.initial * np.exp(self.rate * t)

    @property
    def doubling_time(self) -> float | None:
        """ln(2)/k when the process grows; None when it decays."""
        return float(np.log(2.0) / self.rate) if self.rate > 0 else None

    @property
    def half_life(self) -> float | None:
        """ln(2)/|k| when the process decays; None when it grows."""
        return float(np.log(2.0) / -self.rate) if self.rate < 0 else None


@dataclass(frozen=True)
class CoolingCup:
    """Newton's law of cooling, dT/dt = -k (T - T_room).

    The rate constant is a rough one-significant-figure value for a mug in
    still air; the point of the chapter is the shape of the curve, not a
    calibrated thermal measurement.
    """

    start: float = 90.0
    room: float = 20.0
    rate: float = 0.05

    def temperature(self, t: float) -> float:
        return self.room + (self.start - self.room) * np.exp(-self.rate * t)

    def gap(self, t: float) -> float:
        """The excess temperature T - T_room that drives the cooling."""
        return (self.start - self.room) * np.exp(-self.rate * t)

    def slope(self, t: float) -> float:
        """dT/dt on the solution curve: proportional to the current gap."""
        return -self.rate * self.gap(t)

    @property
    def gap_half_life(self) -> float:
        """How long the temperature gap takes to halve: ln(2)/k."""
        return float(np.log(2.0) / self.rate)


@dataclass(frozen=True)
class SpringOscillator:
    """A mass on a spring: m x'' = -k x, solved by x(t) = A cos(omega t)."""

    mass: float = 1.0
    stiffness: float = 4.0
    amplitude: float = 1.5

    @property
    def omega(self) -> float:
        return float(np.sqrt(self.stiffness / self.mass))

    @property
    def period(self) -> float:
        return float(2.0 * np.pi / self.omega)

    def position(self, t: float) -> float:
        return self.amplitude * np.cos(self.omega * t)

    def velocity(self, t: float) -> float:
        return -self.amplitude * self.omega * np.sin(self.omega * t)

    def acceleration(self, t: float) -> float:
        """x'' = -(k/m) x — the differential equation, evaluated on the solution."""
        return -(self.omega**2) * self.position(t)

    def restoring_force(self, displacement: float) -> float:
        """Hooke's law, F = -k x."""
        return -self.stiffness * displacement

    def energy(self, t: float) -> float:
        """Total mechanical energy, constant for an undamped oscillator."""
        kinetic = 0.5 * self.mass * self.velocity(t) ** 2
        potential = 0.5 * self.stiffness * self.position(t) ** 2
        return float(kinetic + potential)


@dataclass(frozen=True)
class OrbitingBody:
    """A planet obeying Newton's inverse-square law in the plane.

    m r'' = -G M m r / |r|^3 is a differential equation with no elementary
    formula for r(t), so the closing montage integrates it numerically with
    RK4 instead of drawing a decorative ellipse.
    """

    mu: float = 1.0
    start_radius: float = 2.0
    start_speed: float = 0.62

    def _derivative(self, t: float, state: np.ndarray) -> np.ndarray:
        del t  # The gravitational field does not change with time.
        position, velocity = state[:2], state[2:]
        distance = float(np.linalg.norm(position))
        acceleration = -self.mu * position / distance**3
        return np.concatenate((velocity, acceleration))

    def trajectory(self, duration: float = 26.0, dt: float = 0.004) -> np.ndarray:
        """Positions visited over `duration`, from RK4 with a fixed step."""
        state = (self.start_radius, 0.0, 0.0, self.start_speed)
        return integrate_ode(self._derivative, state, duration, dt)[:, :2]


@dataclass(frozen=True)
class SolidOfRevolution:
    """The unit sphere swept out by rotating y = sqrt(1 - x^2) about the x-axis."""

    radius: float = 1.0

    def profile(self, x: float) -> float:
        return float(np.sqrt(max(self.radius**2 - x * x, 0.0)))

    def disk_area(self, x: float) -> float:
        return float(np.pi * (self.radius**2 - x * x))

    def slice_volume(self, x: float, dx: float) -> float:
        """dV = pi y^2 dx for one disk of thickness dx."""
        return self.disk_area(x) * dx

    @property
    def volume(self) -> float:
        """The exact integral of `disk_area` over [-r, r]."""
        return float(4.0 * np.pi * self.radius**3 / 3.0)
