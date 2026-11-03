"""The film's one source of numbers: 2D vectors and the ideal projectile.

Nothing in a scene file types a value that this module can supply. Every
worked example of the brief lives here as data — the 3-4-5 walk, the 6-8-10
drone, (5, 3) - (2, 1), 3i + 4j, the 10-unit vector at 30 degrees, (4, 3) +
(-2, 5) — and every projectile number (14.14 m/s, 2.89 s, 10.20 m, 40.82 m,
the 30 / 45 / 60 degree table) is computed from ``Projectile``.

Two extensions go beyond the ideal model, only to show where it stops
applying: a ball with quadratic air drag (integrated with RK4) and a launch
from a ledge above the landing ground (closed form, checked numerically).

Nothing here imports Manim: ``python -m utils.physics_models`` runs the checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import atan, atan2, cos, degrees, hypot, radians, sin, sqrt

import numpy as np

G = 9.8  # m/s^2, the brief's value for gravity near Earth's surface


# ---------------------------------------------------------------------------
# Vectors in the plane
# ---------------------------------------------------------------------------


def add(*vectors) -> tuple[float, float]:
    return (float(sum(v[0] for v in vectors)), float(sum(v[1] for v in vectors)))


def sub(a, b) -> tuple[float, float]:
    return (float(a[0] - b[0]), float(a[1] - b[1]))


def scale(k: float, a) -> tuple[float, float]:
    return (float(k * a[0]), float(k * a[1]))


def magnitude(a) -> float:
    return hypot(a[0], a[1])


def direction_deg(a) -> float:
    """Angle from the positive x-axis, counter-clockwise, by atan2 (any quadrant)."""
    return degrees(atan2(a[1], a[0]))


def naive_direction_deg(a) -> float:
    """The plain inverse tangent of A_y / A_x — right only in quadrants I and IV."""
    return degrees(atan(a[1] / a[0]))


def unit(a) -> tuple[float, float]:
    n = magnitude(a)
    if n == 0:
        raise ValueError("the zero vector has no direction")
    return (a[0] / n, a[1] / n)


def resolve(length: float, angle_deg: float) -> tuple[float, float]:
    """Components of a vector of ``length`` at ``angle_deg`` from +x."""
    return (length * cos(radians(angle_deg)), length * sin(radians(angle_deg)))


def resultant_length(a: float, b: float, phi_deg: float) -> float:
    """Law of cosines for two vectors of lengths a, b with angle phi between them."""
    return sqrt(max(a * a + b * b + 2 * a * b * cos(radians(phi_deg)), 0.0))


# The brief's worked examples, as data.
WALK = ((3.0, 0.0), (0.0, 4.0))            # 3 m east, then 4 m north
DRONE = ((6.0, 0.0), (0.0, 8.0))           # 6 m east, then 8 m north
SAME_WAY = ((5.0, 0.0), (5.0, 0.0))        # 5 m east + 5 m east
OPPOSED = ((5.0, 0.0), (-5.0, 0.0))        # 5 m east + 5 m west
SUBTRACT = ((5.0, 3.0), (2.0, 1.0))        # A - B
SCALED = (3.0, 4.0)                        # A = 3i + 4j
RESOLVED = (10.0, 30.0)                    # length 10 at 30 degrees
QUADRANT_TRAP = (-3.0, 4.0)                # arctan(4 / -3) points the wrong way
COMPONENTS = ((4.0, 3.0), (-2.0, 5.0))     # A = 4i + 3j, B = -2i + 5j
ASSOCIATIVE = ((2.0, 0.5), (0.6, 1.6), (-1.4, 1.0))   # three vectors grouped two ways
COMMUTE = ((3.4, 0.6), (1.0, 2.2))         # A + B = B + A
CORNER_SPEED = 15.0                        # m/s, before and after a right-angle turn
TRACK_LAP = 400.0                          # m, one lap of a standard track
SPRINT = (100.0, 10.0)                     # 100 m in 10 s
CAR_SPEED = 20.0                           # m/s on the speedometer
TWO_CARS = 10.0                            # m/s, one east and one north
SLED_PULL = (60.0, 30.0)                   # newtons along a rope at 30 degrees (illustrative)
SCALARS = (                                # the brief's table of scalar quantities
    ("Mass", "5 kg"), ("Time", "10 s"), ("Temperature", "25 °C"),
    ("Distance", "100 m"), ("Speed", "20 m/s"), ("Energy", "50 J"),
)
COLD = -5.0                                # degrees Celsius: a negative scalar


def corner_delta_v() -> tuple[float, float]:
    """East at 15 m/s, then north at 15 m/s: delta v = v_f - v_i."""
    return sub((0.0, CORNER_SPEED), (CORNER_SPEED, 0.0))


def track_point(s: float, length: float = TRACK_LAP, straight: float = 84.39) -> tuple[float, float]:
    """Position (m) after running ``s`` metres anticlockwise round a standard
    stadium track (two 84.39 m straights joined by semicircles), from the
    middle of the home straight. Origin at the start; x east, y north."""
    radius = (length - 2 * straight) / (2 * np.pi)
    s = s % length
    half = straight / 2
    legs = [half, np.pi * radius, straight, np.pi * radius, half]
    if s <= legs[0]:
        return (s, 0.0)
    s -= legs[0]
    if s <= legs[1]:
        a = s / radius
        return (half + radius * sin(a), radius - radius * cos(a))
    s -= legs[1]
    if s <= legs[2]:
        return (half - s, 2 * radius)
    s -= legs[2]
    if s <= legs[3]:
        a = s / radius
        return (-half - radius * sin(a), radius + radius * cos(a))
    s -= legs[3]
    return (-half + s, 0.0)


# ---------------------------------------------------------------------------
# The ideal projectile
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Projectile:
    """Launch speed ``v0`` (m/s) at ``angle`` degrees above horizontal, from
    height ``y0`` above the landing ground, under constant gravity, no air."""

    v0: float
    angle: float
    g: float = G
    y0: float = 0.0

    @property
    def theta(self) -> float:
        return radians(self.angle)

    @property
    def vx(self) -> float:
        return self.v0 * cos(self.theta)

    @property
    def vy0(self) -> float:
        return self.v0 * sin(self.theta)

    def x(self, t):
        return self.vx * np.asarray(t, dtype=float)

    def y(self, t):
        t = np.asarray(t, dtype=float)
        return self.y0 + self.vy0 * t - 0.5 * self.g * t * t

    def vy(self, t):
        return self.vy0 - self.g * np.asarray(t, dtype=float)

    def speed(self, t) -> float:
        return float(hypot(self.vx, float(self.vy(t))))

    @property
    def flight_time(self) -> float:
        """Time to land on the ground (y = 0); T = 2 v0 sin(theta) / g when y0 = 0."""
        return (self.vy0 + sqrt(self.vy0 ** 2 + 2 * self.g * self.y0)) / self.g

    @property
    def apex_time(self) -> float:
        return self.vy0 / self.g

    @property
    def max_height(self) -> float:
        """Greatest height above the launch point: v0^2 sin^2(theta) / 2g."""
        return self.vy0 ** 2 / (2 * self.g)

    @property
    def range(self) -> float:
        return self.vx * self.flight_time

    def path_y(self, x):
        """The trajectory with time eliminated: y = x tan(theta) - g x^2 / (2 v0^2 cos^2 theta)."""
        x = np.asarray(x, dtype=float)
        return self.y0 + x * np.tan(self.theta) - self.g * x * x / (2 * self.v0 ** 2 * cos(self.theta) ** 2)

    def samples(self, n: int = 120, until: float | None = None) -> np.ndarray:
        """(n, 3) array of (t, x, y) from launch to ``until`` (default: landing)."""
        t = np.linspace(0.0, self.flight_time if until is None else until, n)
        return np.column_stack([t, self.x(t), self.y(t)])


DROP_HEIGHT = 19.6                                    # m: challenge 2, a fall of exactly 2.00 s
SIDE_SPEED = 6.0                                      # m/s: challenge 2, the sideways launch


def fall_time(height: float, g: float = G) -> float:
    """Time to fall ``height`` from rest (or with any purely horizontal launch): sqrt(2h / g)."""
    return sqrt(2 * height / g)


REFERENCE = Projectile(20.0, 45.0)                    # the brief's reference throw
TABLE = tuple(Projectile(20.0, a) for a in (30.0, 45.0, 60.0))
DOUBLED = Projectile(40.0, 45.0)                      # challenge 5: twice the speed


def range_formula(v0: float, angle: float, g: float = G) -> float:
    """R = v0^2 sin(2 theta) / g, for equal launch and landing heights."""
    return v0 * v0 * sin(radians(2 * angle)) / g


# ---------------------------------------------------------------------------
# Where the ideal model stops: a ledge, and air drag
# ---------------------------------------------------------------------------

LEDGE_HEIGHT = 10.0   # m above the landing ground


def best_angle_from_height(v0: float, height: float, g: float = G) -> float:
    """Range-maximising launch angle from a height: tan(theta) = v0 / sqrt(v0^2 + 2 g h)."""
    return degrees(atan(v0 / sqrt(v0 * v0 + 2 * g * height)))


# Quadratic drag a = -g j - k |v| v, with k = rho C_d A / (2 m). For a soft
# foam ball (m = 0.1 kg, d = 0.1 m, C_d = 0.47, rho = 1.2 kg/m^3) k ~ 0.022 /m.
DRAG_K = 0.022


def drag_flight(v0: float, angle: float, k: float = DRAG_K, g: float = G, dt: float = 0.002) -> np.ndarray:
    """RK4 flight with quadratic drag from ground level to landing: (n, 3) of (t, x, y)."""
    state = np.array([0.0, 0.0, v0 * cos(radians(angle)), v0 * sin(radians(angle))])

    def deriv(s: np.ndarray) -> np.ndarray:
        speed = hypot(s[2], s[3])
        return np.array([s[2], s[3], -k * speed * s[2], -g - k * speed * s[3]])

    rows = [(0.0, 0.0, 0.0)]
    t = 0.0
    while True:
        k1 = deriv(state)
        k2 = deriv(state + dt / 2 * k1)
        k3 = deriv(state + dt / 2 * k2)
        k4 = deriv(state + dt * k3)
        nxt = state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
        if nxt[1] < 0 and t > dt:
            f = state[1] / (state[1] - nxt[1])        # interpolate the landing
            land = state + (nxt - state) * f
            rows.append((t - dt + f * dt, land[0], 0.0))
            return np.array(rows)
        state = nxt
        rows.append((t, state[0], state[1]))


def drag_range(v0: float, angle: float, k: float = DRAG_K) -> float:
    return float(drag_flight(v0, angle, k)[-1, 1])


def best_angle_with_drag(v0: float, k: float = DRAG_K) -> float:
    """Scan whole then tenth degrees for the longest drag flight."""
    coarse = max(range(20, 61), key=lambda a: drag_range(v0, a, k))
    fine = np.arange(coarse - 1.0, coarse + 1.01, 0.1)
    return float(max(fine, key=lambda a: drag_range(v0, a, k)))


def ledge_range(v0: float, angle: float, height: float = LEDGE_HEIGHT) -> float:
    return Projectile(v0, angle, y0=height).range


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    close = lambda a, b, tol=1e-9: abs(a - b) <= tol  # noqa: E731

    walk = add(*WALK)
    check(close(magnitude(walk), 5.0), "3-4-5 walk")
    check(close(add(*DRONE)[0] ** 2 + add(*DRONE)[1] ** 2, 100.0), "6-8-10 drone")
    check(close(resultant_length(6, 8, 90), 10.0), "law of cosines at 90 degrees is Pythagoras")
    check(close(resultant_length(6, 8, 0), 14.0) and close(resultant_length(6, 8, 180), 2.0), "law of cosines extremes")
    check(sub(*SUBTRACT) == (3.0, 2.0), "(5, 3) - (2, 1) = (3, 2)")
    check(add(*COMPONENTS) == (2.0, 8.0), "(4, 3) + (-2, 5) = (2, 8)")
    check(add(*COMMUTE) == add(*COMMUTE[::-1]), "commutative")
    a, b, c = ASSOCIATIVE
    check(np.allclose(add(add(a, b), c), add(a, add(b, c))), "associative")
    check(close(magnitude(unit(SCALED)), 1.0) and unit(SCALED) == (0.6, 0.8), "unit vector of 3i + 4j")
    check(np.allclose(resolve(*RESOLVED), (10 * sqrt(3) / 2, 5.0)), "10 at 30 degrees")
    check(close(direction_deg(QUADRANT_TRAP) - naive_direction_deg(QUADRANT_TRAP), 180.0), "atan2 vs atan")
    check(close(magnitude(corner_delta_v()), CORNER_SPEED * sqrt(2)), "corner delta v")
    for s in np.linspace(0, TRACK_LAP, 41):
        p = track_point(float(s))
        check(np.isfinite(p).all(), "track point finite")
    check(np.allclose(track_point(TRACK_LAP), (0.0, 0.0), atol=1e-9), "a lap ends at the start")
    check(np.allclose(track_point(TRACK_LAP - 1e-9), (0.0, 0.0), atol=1e-6), "track closes smoothly")

    p = REFERENCE
    check(close(p.flight_time, 2 * p.vy0 / p.g), "flight time formula")
    check(close(p.range, range_formula(p.v0, p.angle)), "range = v0^2 sin 2theta / g")
    check(close(float(p.y(p.apex_time)), p.max_height), "apex height")
    check(close(float(p.vy(p.apex_time)), 0.0), "vy = 0 at the top")
    check(close(p.speed(p.apex_time), p.vx), "speed at the top = vx")
    xs = np.linspace(0, p.range, 9)
    check(np.allclose(p.path_y(xs), p.y(xs / p.vx)), "y(x) = y(t) with t eliminated")
    check(close(TABLE[0].range, TABLE[2].range), "30 and 60 degrees share a range")
    check(all(TABLE[1].range > q.range for q in (TABLE[0], TABLE[2])), "45 degrees goes furthest")
    check(close(DOUBLED.range / REFERENCE.range, 4.0), "double speed, four times the range")
    side = Projectile(SIDE_SPEED, 0.0, y0=DROP_HEIGHT)
    check(close(side.flight_time, fall_time(DROP_HEIGHT)) and close(fall_time(DROP_HEIGHT), 2.0),
          "sideways launch lands with the dropped ball, after 2.00 s")
    best = best_angle_from_height(REFERENCE.v0, LEDGE_HEIGHT)
    scan = max(np.arange(30, 46, 0.01), key=lambda a: ledge_range(REFERENCE.v0, float(a)))
    check(abs(best - scan) < 0.02, "ledge optimum: formula agrees with a scan")
    check(best < 45.0, "ledge optimum below 45")
    check(best_angle_with_drag(REFERENCE.v0) < 45.0, "drag optimum below 45")
    check(drag_range(REFERENCE.v0, 45.0) < REFERENCE.range, "drag shortens the flight")
    return failures


if __name__ == "__main__":
    problems = verify()
    p = REFERENCE
    print(f"Reference throw: v0 = {p.v0} m/s at {p.angle} deg")
    print(f"  vx = vy0 = {p.vx:.4f} m/s; T = {p.flight_time:.4f} s; t_H = {p.apex_time:.4f} s")
    print(f"  H = {p.max_height:.4f} m; R = {p.range:.4f} m; x(1) = {float(p.x(1)):.4f}; x(2) = {float(p.x(2)):.4f}")
    for q in TABLE:
        print(f"  {q.angle:4.0f} deg: H = {q.max_height:.3f} m, T = {q.flight_time:.3f} s, R = {q.range:.3f} m")
    print(f"  ledge {LEDGE_HEIGHT} m: best angle {best_angle_from_height(p.v0, LEDGE_HEIGHT):.2f} deg")
    print(f"  drag k = {DRAG_K}: range at 45 deg {drag_range(p.v0, 45):.2f} m, best angle "
          f"{best_angle_with_drag(p.v0):.1f} deg")
    print("\n".join(problems) if problems else "physics_models: all checks pass")
    raise SystemExit(1 if problems else 0)
