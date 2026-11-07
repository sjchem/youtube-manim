"""The film's one source of numbers: circular motion, its forces, and orbits.

Nothing in a scene file types a value that this module can supply. The
brief's reference particle (``REFERENCE``: 2 kg, radius 2 m, 4 m/s) gives
the angular speed (2 rad/s), period (pi s), frequency (0.318 Hz),
centripetal acceleration (8 m/s^2) and inward force (16 N). The other
worked examples live here as data too: the two 5 m/s velocities, the
small-angle table, the doubled speed and radius, the turntable, the flat
curve (r = 50 m, mu_s = 0.6), the circular orbit 400 km up, and the
nonuniform particle (alpha = 0.5 rad/s^2).

Pictures are computed here as well, so they *are* the model: Newton's
polygon of coast-and-nudge steps, the velocity circle (hodograph), the
cannonball trajectories round Earth (RK4 under inverse-square gravity) and
the skidding car.

Nothing here imports Manim: ``python -m utils.physics_models`` runs the checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, degrees, hypot, pi, radians, sin, sqrt

import numpy as np

G = 9.8  # m/s^2, the brief's value for gravity near Earth's surface


# ---------------------------------------------------------------------------
# Plane vectors
# ---------------------------------------------------------------------------


def sub(a, b) -> tuple[float, float]:
    return (float(a[0] - b[0]), float(a[1] - b[1]))


def magnitude(a) -> float:
    return hypot(a[0], a[1])


def direction_deg(a) -> float:
    return degrees(atan2(a[1], a[0]))


# Topic 2.1: equal speeds, different velocities.
V1 = (5.0, 0.0)   # 5 i-hat m/s
V2 = (0.0, 5.0)   # 5 j-hat m/s


def turn_delta_v() -> tuple[float, float]:
    """Delta v = v2 - v1 = -5 i + 5 j."""
    return sub(V2, V1)


# ---------------------------------------------------------------------------
# Uniform circular motion
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Circular:
    """A particle of mass ``m`` on a circle of radius ``r`` at speed ``v``,
    centred on the origin, starting at angle ``theta0`` and moving
    counterclockwise (positive omega) unless ``ccw`` is False."""

    m: float
    r: float
    v: float
    theta0: float = 0.0
    ccw: bool = True

    @property
    def omega(self) -> float:            # signed angular velocity, rad/s
        return (1 if self.ccw else -1) * self.v / self.r

    @property
    def angular_speed(self) -> float:    # |omega|
        return abs(self.omega)

    @property
    def period(self) -> float:           # T = 2 pi r / v
        return 2 * pi * self.r / self.v

    @property
    def frequency(self) -> float:        # f = 1 / T
        return 1 / self.period

    @property
    def accel(self) -> float:            # a_c = v^2 / r
        return self.v ** 2 / self.r

    @property
    def force(self) -> float:            # F_c = m v^2 / r
        return self.m * self.accel

    @property
    def circumference(self) -> float:
        return 2 * pi * self.r

    def theta(self, t):
        return self.theta0 + self.omega * np.asarray(t, dtype=float)

    def position(self, t) -> np.ndarray:
        th = self.theta(t)
        return np.stack([self.r * np.cos(th), self.r * np.sin(th)], axis=-1)

    def velocity(self, t) -> np.ndarray:
        th = self.theta(t)
        w = self.omega
        return np.stack([-self.r * w * np.sin(th), self.r * w * np.cos(th)], axis=-1)

    def acceleration(self, t) -> np.ndarray:
        """a = -omega^2 r (vector): always toward the centre."""
        return -self.omega ** 2 * self.position(t)

    def scaled(self, *, v: float | None = None, r: float | None = None) -> "Circular":
        return Circular(self.m, self.r if r is None else r, self.v if v is None else v, self.theta0, self.ccw)


REFERENCE = Circular(m=2.0, r=2.0, v=4.0)
DOUBLE_SPEED = REFERENCE.scaled(v=2 * REFERENCE.v)     # 8 m/s on 2 m: 32 m/s^2
DOUBLE_RADIUS = REFERENCE.scaled(r=2 * REFERENCE.r)    # 4 m/s on 4 m: 4 m/s^2


def average_acceleration(c: Circular, t1: float, t2: float) -> np.ndarray:
    """Delta v / Delta t over a finite interval."""
    return (c.velocity(t2) - c.velocity(t1)) / (t2 - t1)


def chord_ratio(dtheta: float) -> float:
    """|Delta v| / (v Delta theta) = 2 sin(Delta theta / 2) / Delta theta: tends to 1."""
    return 2 * sin(dtheta / 2) / dtheta


SHRINKING_ANGLES_DEG = (90.0, 45.0, 20.0, 5.0)   # the brief's small-angle limit, shown as a table


# ---------------------------------------------------------------------------
# Newton's polygon: coast in a straight line, then a brief nudge to the centre
# ---------------------------------------------------------------------------


def newton_polygon(c: Circular, sides: int, laps: float = 1.0) -> tuple[np.ndarray, float]:
    """Vertices of the coast-and-nudge path that stays on the circle.

    Between nudges the object coasts along a chord for T / sides. Each nudge
    is an inward Delta v that turns the velocity by 2 pi / sides, so its size
    is 2 v sin(pi / sides). Returns the vertices (n+1, 2) and the nudge size.
    The polygon's vertices all lie on the circle: inward pull never draws the
    object in."""
    step = 2 * pi / sides
    count = int(round(sides * laps))
    angles = c.theta0 + np.arange(count + 1) * step
    vertices = np.stack([c.r * np.cos(angles), c.r * np.sin(angles)], axis=-1)
    chord_speed = 2 * c.r * sin(step / 2) / (c.period / sides)
    return vertices, 2 * chord_speed * sin(step / 2)


def nudge_rate(c: Circular, sides: int) -> float:
    """Average inward Delta v per unit time for the polygon: tends to v^2 / r."""
    _, kick = newton_polygon(c, sides, 1.0 / sides)
    return kick / (c.period / sides)


# ---------------------------------------------------------------------------
# A turntable: one angular velocity, two linear speeds
# ---------------------------------------------------------------------------

TURNTABLE_OMEGA = REFERENCE.angular_speed        # 2 rad/s
TURNTABLE_RADII = (1.0, REFERENCE.r)              # 1 m and 2 m from the axis


def turntable_speeds() -> tuple[float, float]:
    return tuple(r * TURNTABLE_OMEGA for r in TURNTABLE_RADII)


# ---------------------------------------------------------------------------
# Nonuniform circular motion
# ---------------------------------------------------------------------------

ALPHA = 0.5   # rad/s^2, the brief's angular acceleration at the instant v = 4 m/s


def tangential_accel(c: Circular = REFERENCE, alpha: float = ALPHA) -> float:
    return c.r * alpha


def total_accel(c: Circular = REFERENCE, alpha: float = ALPHA) -> float:
    return hypot(c.accel, tangential_accel(c, alpha))


def total_accel_tilt_deg(c: Circular = REFERENCE, alpha: float = ALPHA) -> float:
    """How far the total acceleration tips forward of the inward direction."""
    return degrees(atan2(tangential_accel(c, alpha), c.accel))


@dataclass(frozen=True)
class SpeedingUp:
    """Constant angular acceleration from rest-ish: omega(t) = omega0 + alpha t on radius r."""

    r: float
    omega0: float
    alpha: float

    def theta(self, t):
        t = np.asarray(t, dtype=float)
        return self.omega0 * t + 0.5 * self.alpha * t * t

    def omega(self, t):
        return self.omega0 + self.alpha * np.asarray(t, dtype=float)

    def speed(self, t):
        return self.r * self.omega(t)

    def a_radial(self, t):
        return self.r * self.omega(t) ** 2

    def a_tangential(self) -> float:
        return self.r * self.alpha


# ---------------------------------------------------------------------------
# A car on a flat curve: static friction supplies the inward force
# ---------------------------------------------------------------------------

CURVE_RADIUS = 50.0     # m
MU_S = 0.6              # tyre-road static friction coefficient (dry asphalt, idealised)
SAFE_SPEED = 15.0       # m/s: holds the curve
FAST_SPEED = 20.0       # m/s: needs more than friction can give
HOOK_SPEED = 20.0       # m/s on the speedometer in the opening
# The opening's circular track (radius not spoken): 20 m/s on 80 m needs 5 m/s^2,
# within what this road's friction could supply, so the hook never contradicts scene 18.
HOOK_TRACK = Circular(m=1200.0, r=80.0, v=HOOK_SPEED)


def max_friction_accel(mu: float = MU_S, g: float = G) -> float:
    return mu * g


def max_curve_speed(r: float = CURVE_RADIUS, mu: float = MU_S, g: float = G) -> float:
    """v_max = sqrt(mu_s g r)."""
    return sqrt(mu * g * r)


def kmh(v: float) -> float:
    return v * 3.6


def required_accel(v: float, r: float = CURVE_RADIUS) -> float:
    return v * v / r


def widest_bend_radius(v: float, mu: float = MU_S, g: float = G) -> float:
    """The tightest circle friction can hold at speed v: r = v^2 / (mu g)."""
    return v * v / (mu * g)


# ---------------------------------------------------------------------------
# Satellites: gravity supplies the inward force
# ---------------------------------------------------------------------------

GM_EARTH = 3.986004418e14    # m^3/s^2 (IERS / NASA Earth fact sheet)
R_EARTH = 6.371e6            # m, mean radius
ORBIT_ALTITUDE = 400e3       # m: a low circular orbit, like a crewed station's


def orbit_radius(altitude: float = ORBIT_ALTITUDE) -> float:
    return R_EARTH + altitude


def orbital_speed(r: float | None = None) -> float:
    """v = sqrt(GM / r) for a circular orbit."""
    return sqrt(GM_EARTH / (orbit_radius() if r is None else r))


def orbital_period(r: float | None = None) -> float:
    """T = 2 pi sqrt(r^3 / GM)."""
    r = orbit_radius() if r is None else r
    return 2 * pi * sqrt(r ** 3 / GM_EARTH)


def gravity_at(r: float | None = None) -> float:
    r = orbit_radius() if r is None else r
    return GM_EARTH / r ** 2


# Newton's cannon in dimensionless units: Earth radius 1, GM 1.
CANNON_HEIGHT = 0.12                      # mountain top above the surface, in Earth radii
CANNON_SPEEDS = (0.45, 0.68, 0.86, 1.0)   # as fractions of circular speed at the mountain top


def cannon_shot(fraction: float, steps: int = 2400, laps: float = 1.02) -> np.ndarray:
    """RK4 trajectory (n, 2) of a horizontal shot from the mountain top.

    Stops when it reaches the ground or completes ``laps`` revolutions."""
    r0 = 1.0 + CANNON_HEIGHT
    v0 = fraction / sqrt(r0)
    state = np.array([0.0, r0, -v0, 0.0])   # start at the top, fire to the left (counterclockwise)
    period = 2 * pi * sqrt(r0 ** 3)
    dt = laps * period / steps

    def deriv(s: np.ndarray) -> np.ndarray:
        p = s[:2]
        d = np.linalg.norm(p)
        return np.concatenate([s[2:], -p / d ** 3])

    points = [state[:2].copy()]
    swept = 0.0
    for _ in range(steps):
        k1 = deriv(state)
        k2 = deriv(state + dt / 2 * k1)
        k3 = deriv(state + dt / 2 * k2)
        k4 = deriv(state + dt * k3)
        new = state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        a0, a1 = atan2(state[1], state[0]), atan2(new[1], new[0])
        swept += (a1 - a0 + pi) % (2 * pi) - pi
        state = new
        if np.linalg.norm(state[:2]) < 1.0:
            # Land exactly on the surface.
            points.append(state[:2] / np.linalg.norm(state[:2]))
            break
        points.append(state[:2].copy())
        if swept >= 2 * pi * laps:
            break
    return np.array(points)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    c = REFERENCE
    check(abs(c.angular_speed - 2.0) < 1e-12, "omega = v / r = 2 rad/s")
    check(abs(c.period - pi) < 1e-12, "T = pi s")
    check(abs(c.frequency - 1 / pi) < 1e-12, "f = 1/pi Hz")
    check(abs(2 * pi * c.frequency - c.angular_speed) < 1e-12, "omega = 2 pi f")
    check(abs(c.accel - 8.0) < 1e-12 and abs(c.force - 16.0) < 1e-12, "a = 8, F = 16")
    check(abs(c.m * c.r * c.omega ** 2 - c.force) < 1e-12, "F = m r omega^2")
    ts = np.linspace(0, c.period, 50)
    speeds = np.linalg.norm(c.velocity(ts), axis=-1)
    check(np.allclose(speeds, c.v), "speed constant round the circle")
    check(np.allclose(np.sum(c.velocity(ts) * c.position(ts), axis=-1), 0, atol=1e-12), "v perpendicular to r")
    check(np.allclose(np.sum(c.velocity(ts) * c.acceleration(ts), axis=-1), 0, atol=1e-12), "v . a = 0")
    check(np.allclose(np.linalg.norm(c.acceleration(ts), axis=-1), c.accel), "|a| = v^2/r everywhere")
    # Numerical derivatives agree with the closed forms.
    h = 1e-6
    for t in (0.3, 1.7):
        dv = (c.position(t + h) - c.position(t - h)) / (2 * h)
        da = (c.velocity(t + h) - c.velocity(t - h)) / (2 * h)
        check(np.allclose(dv, c.velocity(t), atol=1e-6), "v = dr/dt")
        check(np.allclose(da, c.acceleration(t), atol=1e-5), "a = dv/dt")
    # Average acceleration over a finite interval points at the centre from the arc's midpoint.
    for dt in (0.8, 0.2, 0.01):
        a_avg = average_acceleration(c, 0.5, 0.5 + dt)
        mid = c.position(0.5 + dt / 2)
        cosang = -np.dot(a_avg, mid) / (np.linalg.norm(a_avg) * np.linalg.norm(mid))
        check(abs(cosang - 1) < 1e-9, "average acceleration aims at the centre from the arc midpoint")
        check(abs(np.linalg.norm(a_avg) - c.accel * chord_ratio(c.angular_speed * dt)) < 1e-9, "|a_avg| = a_c x ratio")
    ratios = [chord_ratio(radians(d)) for d in SHRINKING_ANGLES_DEG]
    check(all(x < y for x, y in zip(ratios, ratios[1:])) and abs(ratios[-1] - 1) < 1e-3, "ratio rises to 1")
    check(abs(magnitude(turn_delta_v()) - 5 * sqrt(2)) < 1e-12, "|delta v| = 5 root 2")
    check(abs(DOUBLE_SPEED.accel / c.accel - 4) < 1e-12, "double speed, four times a")
    check(abs(DOUBLE_RADIUS.accel / c.accel - 0.5) < 1e-12, "double radius, half a")
    # Newton's polygon: vertices on the circle; nudge rate -> v^2 / r.
    verts, _ = newton_polygon(c, 8)
    check(np.allclose(np.linalg.norm(verts, axis=1), c.r), "polygon vertices stay on the circle")
    rates = [nudge_rate(c, n) for n in (6, 12, 48, 400)]
    check(all(x < y for x, y in zip(rates, rates[1:])) and abs(rates[-1] - c.accel) < 1e-3, "nudge rate -> v^2/r")
    check(turntable_speeds() == (2.0, 4.0), "turntable: 2 and 4 m/s")
    check(abs(tangential_accel() - 1.0) < 1e-12 and abs(total_accel() - sqrt(65)) < 1e-12, "a_t = 1, |a| = sqrt 65")
    check(abs(max_curve_speed() - sqrt(294)) < 1e-12, "v_max = sqrt 294")
    check(required_accel(SAFE_SPEED) < max_friction_accel() < required_accel(FAST_SPEED), "15 holds, 20 slides")
    check(widest_bend_radius(FAST_SPEED) > CURVE_RADIUS > widest_bend_radius(SAFE_SPEED), "fast car drifts wide")
    check(HOOK_TRACK.accel < max_friction_accel(), "the opening car could really hold its track")
    check(abs(orbital_speed() * orbital_period() - 2 * pi * orbit_radius()) < 1e-6, "v T = 2 pi r")
    check(abs(gravity_at() * orbit_radius() - orbital_speed() ** 2) < 1e-6, "g' = v^2 / r: gravity is the centripetal pull")
    # Cannon: slower shots land; the circular-speed shot stays at the same height for a lap.
    for f in CANNON_SPEEDS[:-1]:
        path = cannon_shot(f)
        check(abs(np.linalg.norm(path[-1]) - 1) < 1e-9, f"cannon {f} lands")
    circle = cannon_shot(CANNON_SPEEDS[-1])
    check(np.allclose(np.linalg.norm(circle, axis=1), 1 + CANNON_HEIGHT, atol=1e-6), "circular shot keeps its height")
    lands = [atan2(cannon_shot(f)[-1][1], cannon_shot(f)[-1][0]) for f in CANNON_SPEEDS[:-1]]
    check(all(x < y for x, y in zip(lands, lands[1:])), "faster shots land farther round")
    ramp = SpeedingUp(c.r, c.angular_speed, ALPHA)
    check(abs(ramp.a_radial(0) - c.accel) < 1e-12 and abs(ramp.a_tangential() - 1) < 1e-12, "ramp starts at the brief's instant")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    c = REFERENCE
    print(f"Reference particle: m = {c.m} kg, r = {c.r} m, v = {c.v} m/s")
    print(f"  omega = {c.angular_speed:.3f} rad/s, T = {c.period:.4f} s, f = {c.frequency:.4f} Hz")
    print(f"  a_c = {c.accel:.2f} m/s^2, F_c = {c.force:.2f} N")
    print(f"|delta v| for 5i -> 5j: {magnitude(turn_delta_v()):.3f} m/s")
    print("2 sin(x/2)/x:", ", ".join(f"{d:g}° {chord_ratio(radians(d)):.4f}" for d in SHRINKING_ANGLES_DEG))
    print(f"Flat curve: v_max = {max_curve_speed():.3f} m/s = {kmh(max_curve_speed()):.2f} km/h; "
          f"mu g = {max_friction_accel():.2f}; 15 m/s needs {required_accel(SAFE_SPEED):.2f}, 20 needs {required_accel(FAST_SPEED):.2f}")
    print(f"Orbit 400 km: v = {orbital_speed() / 1e3:.3f} km/s, T = {orbital_period() / 60:.2f} min, g = {gravity_at():.3f} m/s^2")
    print(f"Nonuniform: a_t = {tangential_accel():.2f}, |a| = {total_accel():.3f} m/s^2, tilt {total_accel_tilt_deg():.2f}°")
    print("Model check passed.")
