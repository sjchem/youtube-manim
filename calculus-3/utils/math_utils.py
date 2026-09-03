"""Pure mathematical helpers shared by multiple scenes.

Every quantity this film displays on screen is computed here from a closed
form wherever one exists, so no readout is a rough numerical estimate dressed
up as an exact result.  The single exception is the two-body orbit in the
closing montage, which is integrated with the explicit RK4 step below; that
is a genuine numerical solution of the differential equation and is described
as one in `concept_summary.md`.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

# -- Scene 01: the reverse problem, v(t) = 2t -------------------------------


def linear_velocity(t: float) -> float:
    """v(t) = 2t in metres per second: the only thing the driver can see."""
    return 2.0 * t


def position_family(t: float, constant: float = 0.0) -> float:
    """s(t) = t^2 + C: every antiderivative of `linear_velocity`."""
    return t * t + constant


def travelled_distance(a: float, b: float) -> float:
    """Exact displacement under v(t) = 2t between times a and b."""
    return position_family(b) - position_family(a)


# -- Scene 02: one derivative, a whole family of curves ---------------------


def shifted_parabola(x: float, constant: float = 0.0) -> float:
    """y = x^2 + C, the family that motivates the integration constant."""
    return x * x + constant


def parabola_slope(x: float) -> float:
    """dy/dx = 2x, identical for every member of `shifted_parabola`."""
    return 2.0 * x


# -- Scenes 03, 04, 09: the equation dy/dx = y ------------------------------


def self_slope(x: float, y: float) -> float:
    """The right-hand side of dy/dx = y: the slope depends only on height."""
    del x  # The field is horizontally uniform; that is the whole point.
    return y


def exponential_solution(x: float, constant: float = 1.0) -> float:
    """y = C e^x, the exact solution family of dy/dx = y."""
    return constant * np.exp(x)


def slope_field_points(
    x_range: Sequence[float],
    y_range: Sequence[float],
) -> list[tuple[float, float]]:
    """Grid sample points (x, y) for a slope field, in row-major order.

    Rows are yielded bottom to top so a scene can reveal the field one
    horizontal band at a time.
    """
    x_start, x_stop, x_step = x_range
    y_start, y_stop, y_step = y_range
    xs = np.arange(x_start, x_stop + 1e-9, x_step)
    ys = np.arange(y_start, y_stop + 1e-9, y_step)
    return [(float(x), float(y)) for y in ys for x in xs]


def normalized_slope_step(slope: float, half_length: float) -> tuple[float, float]:
    """Half-width and half-height of a segment of fixed length with `slope`.

    Drawing every tick at the same visual length keeps a slope field readable:
    direction carries the information, not stroke length.
    """
    scale = half_length / np.hypot(1.0, slope)
    return float(scale), float(scale * slope)


# -- Scene 05: proportional growth ------------------------------------------

GROWTH_RATIO = 1.2
GROWTH_RATE = float(np.log(GROWTH_RATIO))  # k in dP/dt = kP, per generation


def discrete_growth(steps: int, start: float = 100.0, ratio: float = GROWTH_RATIO) -> list[float]:
    """The stepwise colony sizes 100, 120, 144, ... used before the smooth curve."""
    values = [start]
    for _ in range(steps):
        values.append(values[-1] * ratio)
    return values


def exponential_growth(t: float, start: float = 100.0, rate: float = GROWTH_RATE) -> float:
    """P(t) = P0 e^{kt}, the continuous solution of dP/dt = kP."""
    return start * np.exp(rate * t)


# -- Scene 06: proportional decay -------------------------------------------

DECAY_HALF_LIFE = 2.0
DECAY_RATE = float(np.log(2.0) / DECAY_HALF_LIFE)  # k in dN/dt = -kN


def exponential_decay(t: float, start: float = 100.0, rate: float = DECAY_RATE) -> float:
    """N(t) = N0 e^{-kt}, the solution of dN/dt = -kN."""
    return start * np.exp(-rate * t)


def half_life(rate: float = DECAY_RATE) -> float:
    """The exact time for `exponential_decay` to halve: ln(2)/k."""
    return float(np.log(2.0) / rate)


def surviving_count(t: float, total: int = 60, rate: float = DECAY_RATE) -> int:
    """How many of `total` particles remain at time t, rounded to a whole particle."""
    return int(round(total * np.exp(-rate * t)))


# -- Scene 07: Newton's law of cooling ---------------------------------------

ROOM_TEMPERATURE = 20.0
COFFEE_START = 90.0
# A mug of coffee cooling in still air loses roughly 5% of its excess
# temperature per minute; k is quoted to one significant figure on purpose.
COOLING_RATE = 0.05


def cooling_temperature(
    t: float,
    start: float = COFFEE_START,
    room: float = ROOM_TEMPERATURE,
    rate: float = COOLING_RATE,
) -> float:
    """T(t) = T_room + (T0 - T_room) e^{-kt}: the solution of Newton's law of cooling."""
    return room + (start - room) * np.exp(-rate * t)


def cooling_slope(
    t: float,
    start: float = COFFEE_START,
    room: float = ROOM_TEMPERATURE,
    rate: float = COOLING_RATE,
) -> float:
    """dT/dt = -k (T - T_room), evaluated on the solution curve."""
    return -rate * (cooling_temperature(t, start, room, rate) - room)


def temperature_gap(
    t: float,
    start: float = COFFEE_START,
    room: float = ROOM_TEMPERATURE,
    rate: float = COOLING_RATE,
) -> float:
    """The shrinking excess T - T_room that drives the whole process."""
    return cooling_temperature(t, start, room, rate) - room


# -- Scene 10: the spring, x'' = -(k/m) x -------------------------------------

SPRING_MASS = 1.0
SPRING_STIFFNESS = 4.0
SPRING_AMPLITUDE = 1.5


def angular_frequency(stiffness: float = SPRING_STIFFNESS, mass: float = SPRING_MASS) -> float:
    """omega = sqrt(k/m), the exact frequency of the simple harmonic oscillator."""
    return float(np.sqrt(stiffness / mass))


def spring_position(t: float, amplitude: float = SPRING_AMPLITUDE, phase: float = 0.0) -> float:
    """x(t) = A cos(omega t + phi)."""
    return amplitude * np.cos(angular_frequency() * t + phase)


def spring_velocity(t: float, amplitude: float = SPRING_AMPLITUDE, phase: float = 0.0) -> float:
    """v(t) = x'(t) = -A omega sin(omega t + phi)."""
    omega = angular_frequency()
    return -amplitude * omega * np.sin(omega * t + phase)


def spring_acceleration(t: float, amplitude: float = SPRING_AMPLITUDE, phase: float = 0.0) -> float:
    """a(t) = x''(t) = -omega^2 x(t), which is exactly the differential equation."""
    return -(angular_frequency() ** 2) * spring_position(t, amplitude, phase)


# -- Scene 11: the sphere as a stack of disks ---------------------------------


def semicircle(x: float, radius: float = 1.0) -> float:
    """y = sqrt(r^2 - x^2), the upper half of a circle of the given radius."""
    return float(np.sqrt(max(radius * radius - x * x, 0.0)))


def disk_area(x: float, radius: float = 1.0) -> float:
    """pi y^2 = pi (r^2 - x^2): the face area of one slice at position x."""
    return float(np.pi * (radius * radius - x * x))


def sphere_volume(radius: float = 1.0) -> float:
    """The exact value of the integral of `disk_area` over [-r, r]: 4 pi r^3 / 3."""
    return float(4.0 * np.pi * radius**3 / 3.0)


def disk_sum_volume(n: int, radius: float = 1.0) -> float:
    """Midpoint disk-stack approximation of the sphere volume with n slices."""
    dx = 2.0 * radius / n
    centers = -radius + dx * (np.arange(n) + 0.5)
    return float(np.sum(np.pi * (radius**2 - centers**2)) * dx)


# -- Scene 13: a general rule, instantiated as saturating growth ---------------

LOGISTIC_CAPACITY = 3.0
LOGISTIC_RATE = 0.9


def logistic_slope(t: float, y: float, capacity: float = LOGISTIC_CAPACITY, rate: float = LOGISTIC_RATE) -> float:
    """f(y, t) = r y (1 - y/K): growth that runs out of room."""
    del t  # This particular rule happens not to depend on time.
    return rate * y * (1.0 - y / capacity)


def logistic_solution(
    t: float,
    start: float,
    capacity: float = LOGISTIC_CAPACITY,
    rate: float = LOGISTIC_RATE,
) -> float:
    """The exact solution of the logistic equation through (0, start)."""
    growth = np.exp(rate * t)
    return capacity * start * growth / (capacity + start * (growth - 1.0))


# -- Scene 13: solving an equation of motion numerically ----------------------


def rk4_step(
    derivative: Callable[[float, np.ndarray], np.ndarray],
    t: float,
    state: np.ndarray,
    dt: float,
) -> np.ndarray:
    """One classical fourth-order Runge-Kutta step of the system y' = f(t, y)."""
    k1 = derivative(t, state)
    k2 = derivative(t + 0.5 * dt, state + 0.5 * dt * k1)
    k3 = derivative(t + 0.5 * dt, state + 0.5 * dt * k2)
    k4 = derivative(t + dt, state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate_ode(
    derivative: Callable[[float, np.ndarray], np.ndarray],
    state: Sequence[float],
    duration: float,
    dt: float = 0.002,
) -> np.ndarray:
    """Integrate y' = f(t, y) with fixed-step RK4 and return every visited state."""
    current = np.array(state, dtype=float)
    steps = max(int(round(duration / dt)), 1)
    trail = np.empty((steps + 1, current.size))
    trail[0] = current
    time = 0.0
    for index in range(steps):
        current = rk4_step(derivative, time, current, dt)
        time += dt
        trail[index + 1] = current
    return trail
