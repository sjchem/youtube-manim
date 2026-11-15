"""The physics behind every picture and every spoken number in the film.

Nothing here imports Manim. Each worked example from the brief lives in one
frozen dataclass, each simulation is seeded and deterministic, and
``python -m utils.physics_models`` re-derives every result (including the
moment-of-inertia table, by numerical integration) and fails loudly if a
value drifts.

Units are SI throughout. Screen scaling is done by the scenes, never here.

References used to shape the explanations (no numbers are copied from them
that are not recomputed below):

* NCERT Physics, Class XI, Part I, Chapter 6 (2023 rationalised edition;
  Chapter 7 in older editions), "System of Particles and Rotational Motion".
* D. Kleppner and R. Kolenkow, *An Introduction to Mechanics*, 2nd ed.,
  chapters on rigid-body motion and angular momentum.
* H. C. Verma, *Concepts of Physics*, Vol. 1, Chapter 10 (Rotational Mechanics).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from functools import lru_cache
from math import pi, radians, sin, sqrt

import numpy as np

G = 9.8  # m/s^2, the value used in NCERT worked examples


# ---------------------------------------------------------------------------
# Chapter 2 — centre of mass of two particles
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ComPair:
    m1: float = 2.0
    x1: float = 0.0
    m2: float = 6.0
    x2: float = 4.0

    @property
    def total(self) -> float:
        return self.m1 + self.m2

    @property
    def moment(self) -> float:
        return self.m1 * self.x1 + self.m2 * self.x2

    @property
    def x_cm(self) -> float:
        return self.moment / self.total


COM_PAIR = ComPair()


def com(masses, positions) -> np.ndarray:
    """Mass-weighted average position (any dimension)."""
    m = np.asarray(masses, dtype=float)
    r = np.asarray(positions, dtype=float)
    return (m[:, None] * r).sum(axis=0) / m.sum() if r.ndim == 2 else float((m * r).sum() / m.sum())


# A small 3D cloud of unequal masses (scene 05). Seeded, so every render agrees.
@lru_cache(maxsize=1)
def particle_cloud(n: int = 11, seed: int = 20261113) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    masses = rng.choice([1.0, 2.0, 3.0, 4.0], size=n, p=[0.35, 0.3, 0.2, 0.15])
    positions = rng.normal(size=(n, 3)) * np.array([1.5, 1.0, 1.1]) + np.array([0.6, 0.4, 0.0])
    return masses, positions


# ---------------------------------------------------------------------------
# Chapter 3 — internal forces, an exploding shell, two carts
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SpringCluster:
    """Five particles joined by springs, pushed on one particle only (scene 06).

    Internal spring forces obey Newton's third law exactly, so the centre of
    mass must accelerate at F / M whatever the cluster does inside."""

    masses: tuple[float, ...] = (1.0, 2.0, 1.5, 1.0, 2.5)
    force: tuple[float, float] = (1.2, 0.0)   # N, applied to particle 0 only
    push_on: int = 0
    stiffness: float = 26.0
    duration: float = 12.0
    dt: float = 1 / 600
    every: int = 10                          # store one frame per 1/60 s

    @property
    def total(self) -> float:
        return float(sum(self.masses))

    @property
    def a_cm(self) -> np.ndarray:
        return np.asarray(self.force) / self.total


SPRINGS = SpringCluster()

_CLUSTER_START = np.array([[-0.9, 0.55], [0.25, 0.95], [1.0, 0.05], [0.15, -0.85], [-0.85, -0.5]])
_CLUSTER_EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 3), (2, 4))


def cluster_edges() -> tuple[tuple[int, int], ...]:
    return _CLUSTER_EDGES


@lru_cache(maxsize=4)
def spring_cluster_run(pushed: bool = True, duration: float | None = None,
                       push_on: int | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Velocity-Verlet run. Returns (times, positions (frames, 5, 2), spring force pairs (frames, edges, 2))."""
    s = SPRINGS
    duration = s.duration if duration is None else duration
    m = np.asarray(s.masses)
    x = _CLUSTER_START.copy()
    x -= com(m, x)                                  # start with the centre of mass at the origin
    rest = {e: float(np.linalg.norm(x[e[0]] - x[e[1]])) for e in _CLUSTER_EDGES}
    # A little internal wobble with zero total momentum, so only F moves the centre.
    rng = np.random.default_rng(7)
    v = rng.normal(scale=0.35, size=x.shape)
    v -= (m[:, None] * v).sum(axis=0) / m.sum()
    # ...and zero angular momentum about the centre, so only the push can make it turn.
    spin = (m * (x[:, 0] * v[:, 1] - x[:, 1] * v[:, 0])).sum() / (m * (x ** 2).sum(axis=1)).sum()
    v -= spin * np.column_stack([-x[:, 1], x[:, 0]])
    external = np.zeros_like(x)
    if pushed:
        external[s.push_on if push_on is None else push_on] = s.force

    def forces(pos):
        f = external.copy()
        pairs = np.zeros((len(_CLUSTER_EDGES), 2))
        for k, (i, j) in enumerate(_CLUSTER_EDGES):
            d = pos[j] - pos[i]
            n = float(np.linalg.norm(d))
            fij = s.stiffness * (n - rest[(i, j)]) * d / n     # force on i, toward j when stretched
            f[i] += fij
            f[j] -= fij                                         # Newton's third law, exactly
            pairs[k] = fij
        return f, pairs

    steps = int(round(duration / s.dt))
    times, frames, pair_frames = [], [], []
    f, pairs = forces(x)
    for step in range(steps + 1):
        if step % s.every == 0:
            times.append(step * s.dt)
            frames.append(x.copy())
            pair_frames.append(pairs.copy())
        v_half = v + 0.5 * s.dt * f / m[:, None]
        x = x + s.dt * v_half
        f, pairs = forces(x)
        v = v_half + 0.5 * s.dt * f / m[:, None]
    return np.array(times), np.array(frames), np.array(pair_frames)


@dataclass(frozen=True)
class Firework:
    """A shell that bursts at the top of its arc (scene 07), no air resistance."""

    v0: tuple[float, float, float] = (7.0, 14.0, 0.0)    # m/s
    burst_time: float = 14.0 / G                          # at the apex
    masses: tuple[float, ...] = (0.30, 0.22, 0.18, 0.16, 0.14)
    kick: float = 5.5                                     # typical fragment speed after the burst, m/s
    seed: int = 31

    @property
    def total(self) -> float:
        return float(sum(self.masses))


FIREWORK = Firework()


@lru_cache(maxsize=1)
def fragment_kicks() -> np.ndarray:
    """Velocity changes at the burst. The mass-weighted sum is exactly zero
    (the burst forces are internal), and no fragment is thrown downward faster
    than the shell can stay airborne for the shot."""
    f = FIREWORK
    rng = np.random.default_rng(f.seed)
    m = np.asarray(f.masses)
    directions = rng.normal(size=(len(m), 3))
    directions[:, 2] *= 0.8
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    kicks = directions * f.kick
    kicks -= (m[:, None] * kicks).sum(axis=0) / m.sum()
    return kicks


def shell_position(t: float) -> np.ndarray:
    f = FIREWORK
    v0 = np.asarray(f.v0)
    return v0 * t + np.array([0.0, -0.5 * G * t * t, 0.0])


def fragment_positions(t: float) -> np.ndarray:
    """Every fragment's position at time ``t`` (before the burst they ride together).
    Fragments stop at the ground (y = 0); the ground's push is an external force."""
    f = FIREWORK
    centre = shell_position(min(t, f.burst_time))
    v_burst = np.asarray(f.v0) + np.array([0.0, -G * f.burst_time, 0.0])
    if t <= f.burst_time:
        return np.repeat(centre[None, :], len(f.masses), axis=0)
    out = []
    for kick in fragment_kicks():
        v = v_burst + kick
        landed = _landing_time(centre, v)
        tau = min(t - f.burst_time, landed)
        out.append(centre + v * tau + np.array([0.0, -0.5 * G * tau * tau, 0.0]))
    return np.array(out)


def _landing_time(start: np.ndarray, v: np.ndarray) -> float:
    a, b, c = -0.5 * G, v[1], start[1]
    return float((-b - sqrt(b * b - 4 * a * c)) / (2 * a))


def first_landing() -> float:
    """Time (from launch) at which the first fragment reaches the ground."""
    f = FIREWORK
    centre = shell_position(f.burst_time)
    v_burst = np.asarray(f.v0) + np.array([0.0, -G * f.burst_time, 0.0])
    return f.burst_time + min(_landing_time(centre, v_burst + k) for k in fragment_kicks())


def fragment_com(t: float) -> np.ndarray:
    return com(FIREWORK.masses, fragment_positions(t))


@dataclass(frozen=True)
class Carts:
    """Two carts on a frictionless track with a spring bumper (scene 08)."""

    m1: float = 2.0
    v1: float = 3.0
    m2: float = 3.0
    v2: float = -1.0
    bumper_k: float = 900.0      # N/m
    x1: float = -3.4             # starting centres, m
    x2: float = 1.2
    half_length: float = 0.35    # m

    @property
    def momentum(self) -> float:
        return self.m1 * self.v1 + self.m2 * self.v2

    @property
    def total(self) -> float:
        return self.m1 + self.m2

    @property
    def v_cm(self) -> float:
        return self.momentum / self.total

    @property
    def elastic_after(self) -> tuple[float, float]:
        m1, m2, u1, u2 = self.m1, self.m2, self.v1, self.v2
        return ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2), ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)


CARTS = Carts()


@lru_cache(maxsize=1)
def cart_run(duration: float = 4.0, dt: float = 1 / 2400) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(times, x (frames, 2), v (frames, 2)) for the bumper collision, sampled at 120 Hz."""
    c = CARTS
    m = np.array([c.m1, c.m2])
    x = np.array([c.x1, c.x2])
    v = np.array([c.v1, c.v2])

    def force(pos):
        overlap = 2 * c.half_length - (pos[1] - pos[0])
        push = c.bumper_k * overlap if overlap > 0 else 0.0
        return np.array([-push, push])

    times, xs, vs = [], [], []
    f = force(x)
    every = int(round(1 / (120 * dt)))
    for step in range(int(round(duration / dt)) + 1):
        if step % every == 0:
            times.append(step * dt)
            xs.append(x.copy())
            vs.append(v.copy())
        v_half = v + 0.5 * dt * f / m
        x = x + dt * v_half
        f = force(x)
        v = v_half + 0.5 * dt * f / m
    return np.array(times), np.array(xs), np.array(vs)


# ---------------------------------------------------------------------------
# Chapter 5 — torque and equilibrium
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Door:
    force: float = 20.0      # N, perpendicular to the door
    r_far: float = 0.8       # m from the hinges
    r_near: float = 0.2
    width: float = 0.9       # m, the door itself

    @property
    def tau_far(self) -> float:
        return self.force * self.r_far

    @property
    def tau_near(self) -> float:
        return self.force * self.r_near


DOOR = Door()


def torque_z(r, f) -> float:
    """z component of r x F for vectors in the xy plane."""
    return float(r[0] * f[1] - r[1] * f[0])


@dataclass(frozen=True)
class Seesaw:
    w_left: float = 100.0    # N
    d_left: float = 2.0      # m left of the pivot
    w_right: float = 200.0
    d_right: float = 1.0

    @property
    def tau_ccw(self) -> float:
        return self.w_left * self.d_left

    @property
    def tau_cw(self) -> float:
        return self.w_right * self.d_right

    @property
    def net_torque(self) -> float:
        return self.tau_ccw - self.tau_cw

    @property
    def pivot(self) -> float:
        return self.w_left + self.w_right


SEESAW = Seesaw()


# ---------------------------------------------------------------------------
# Chapter 6 — moment of inertia
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Dumbbell:
    mass: float = 1.0        # kg, each
    r_in: float = 1.0        # m from the axis
    r_out: float = 2.0

    @property
    def i_in(self) -> float:
        return 2 * self.mass * self.r_in ** 2

    @property
    def i_out(self) -> float:
        return 2 * self.mass * self.r_out ** 2


DUMBBELL = Dumbbell()


@dataclass(frozen=True)
class Shape:
    key: str
    name: str
    axis: str
    coefficient: Fraction
    length: str               # "R" or "L": which size the coefficient multiplies
    latex: str


SHAPES: tuple[Shape, ...] = (
    Shape("ring", "Thin ring", "centre, perpendicular to plane", Fraction(1), "R", r"MR^2"),
    Shape("disc", "Solid disc", "centre, perpendicular to plane", Fraction(1, 2), "R", r"\tfrac12 MR^2"),
    Shape("cylinder", "Solid cylinder", "central symmetry axis", Fraction(1, 2), "R", r"\tfrac12 MR^2"),
    Shape("rod_mid", "Thin rod", "midpoint, perpendicular", Fraction(1, 12), "L", r"\tfrac1{12} ML^2"),
    Shape("rod_end", "Thin rod", "one end, perpendicular", Fraction(1, 3), "L", r"\tfrac13 ML^2"),
    Shape("sphere", "Solid sphere", "a diameter", Fraction(2, 5), "R", r"\tfrac25 MR^2"),
    Shape("shell", "Spherical shell", "a diameter", Fraction(2, 3), "R", r"\tfrac23 MR^2"),
)


def shape(key: str) -> Shape:
    return next(s for s in SHAPES if s.key == key)


def numeric_coefficient(key: str, n: int = 4000) -> float:
    """I / (M R^2) or I / (M L^2) by direct numerical integration of r_perp^2 dm."""
    u = (np.arange(n) + 0.5) / n                     # midpoint rule on [0, 1]
    if key == "ring":
        return 1.0                                   # every element at r = R
    if key in {"disc", "cylinder"}:                  # dm proportional to r dr
        return float((u ** 3).sum() / u.sum())
    if key == "rod_mid":                             # x from -1/2 to 1/2
        x = u - 0.5
        return float((x ** 2).mean())
    if key == "rod_end":
        return float((u ** 2).mean())
    if key == "sphere":                              # shells of radius r, r_perp^2 averages to 2/3 r^2
        return float(((2 / 3) * u ** 2 * u ** 2).sum() / (u ** 2).sum())
    if key == "shell":                               # r_perp^2 = 1 - z^2, z uniform on [-1, 1]
        z = 2 * u - 1
        return float((1 - z ** 2).mean())
    raise KeyError(key)


@dataclass(frozen=True)
class Gyration:
    @property
    def ring(self) -> float:          # k / R
        return 1.0

    @property
    def disc(self) -> float:          # k / R
        return sqrt(0.5)


GYRATION = Gyration()


@dataclass(frozen=True)
class AxisTheorems:
    rod_cm: Fraction = Fraction(1, 12)

    @property
    def shift(self) -> Fraction:      # M (L/2)^2 in units of M L^2
        return Fraction(1, 4)

    @property
    def rod_end(self) -> Fraction:
        return self.rod_cm + self.shift

    @property
    def disc_z(self) -> Fraction:
        return Fraction(1, 2)

    @property
    def disc_diameter(self) -> Fraction:
        return self.disc_z / 2


AXES = AxisTheorems()


def rod_inertia_about(offset: float) -> float:
    """I / (M L^2) of a uniform rod about a perpendicular axis ``offset * L`` from its centre."""
    return float(AXES.rod_cm) + offset ** 2


# ---------------------------------------------------------------------------
# Chapters 7 and 8 — the spinning wheel and the driven disc share one alpha
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SpinUp:
    alpha: float = 2.0       # rad/s^2
    duration: float = 4.0    # s, from rest

    @property
    def omega(self) -> float:
        return self.alpha * self.duration

    @property
    def angle(self) -> float:
        return 0.5 * self.alpha * self.duration ** 2

    @property
    def revolutions(self) -> float:
        return self.angle / (2 * pi)

    def theta_at(self, t: float) -> float:
        return 0.5 * self.alpha * min(max(t, 0.0), self.duration) ** 2

    def omega_at(self, t: float) -> float:
        return self.alpha * min(max(t, 0.0), self.duration)


WHEEL = SpinUp()


@dataclass(frozen=True)
class DrivenDisc:
    mass: float = 4.0        # kg
    radius: float = 0.5      # m
    torque: float = 1.0      # N m, net, about the fixed axle

    @property
    def inertia(self) -> float:
        return 0.5 * self.mass * self.radius ** 2

    @property
    def string_force(self) -> float:
        return self.torque / self.radius

    @property
    def alpha(self) -> float:
        return self.torque / self.inertia

    @property
    def omega_end(self) -> float:
        return self.alpha * WHEEL.duration

    @property
    def angle_end(self) -> float:
        return 0.5 * self.alpha * WHEEL.duration ** 2

    @property
    def kinetic(self) -> float:
        return 0.5 * self.inertia * self.omega_end ** 2

    @property
    def work(self) -> float:
        return self.torque * self.angle_end

    @property
    def power_end(self) -> float:
        return self.torque * self.omega_end


DISC = DrivenDisc()


def accelerations(r: float, alpha: float, omega: float) -> tuple[float, float, float]:
    """(tangential, radial, total) acceleration of a point at r_perp from a fixed axis."""
    at, ar = r * alpha, r * omega ** 2
    return at, ar, float(np.hypot(at, ar))


# ---------------------------------------------------------------------------
# Chapter 9 — angular momentum: the skater
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Skater:
    """Body (I_body) plus two arms modelled as point masses at radius r."""

    i_body: float = 1.0      # kg m^2
    arm_mass: float = 2.0    # kg, each arm's effective mass
    i_out: float = 4.0       # arms out
    i_in: float = 2.0        # arms in
    omega_out: float = 2.0   # rad/s

    def inertia(self, r: float) -> float:
        return self.i_body + 2 * self.arm_mass * r * r

    def radius_for(self, inertia: float) -> float:
        return sqrt((inertia - self.i_body) / (2 * self.arm_mass))

    @property
    def r_out(self) -> float:
        return self.radius_for(self.i_out)

    @property
    def r_in(self) -> float:
        return self.radius_for(self.i_in)

    @property
    def momentum(self) -> float:
        return self.i_out * self.omega_out

    @property
    def omega_in(self) -> float:
        return self.momentum / self.i_in

    @property
    def k_out(self) -> float:
        return 0.5 * self.i_out * self.omega_out ** 2

    @property
    def k_in(self) -> float:
        return 0.5 * self.i_in * self.omega_in ** 2

    @property
    def work(self) -> float:
        return self.k_in - self.k_out

    def omega_at(self, r: float) -> float:
        return self.momentum / self.inertia(r)


SKATER = Skater()


def skater_work_by_integration(n: int = 20000) -> float:
    """Work done pulling the arms in, as the integral of (inward pull) x (inward step).

    Each arm needs the inward force m omega^2 r to stay on its circle; with
    L fixed, omega = L / I(r). Summing F dr from r_out to r_in must equal the
    gain in kinetic energy, K_in - K_out."""
    s = SKATER
    r = np.linspace(s.r_out, s.r_in, n + 1)
    mid = 0.5 * (r[1:] + r[:-1])
    pull = 2 * s.arm_mass * np.array([s.omega_at(x) ** 2 for x in mid]) * mid
    return float((pull * -(r[1:] - r[:-1])).sum())


# ---------------------------------------------------------------------------
# Chapter 10 — rolling
# ---------------------------------------------------------------------------


def rolling_point_velocity(phi: float, v_cm: float = 1.0) -> np.ndarray:
    """Velocity of the rim point at angle ``phi`` from the top (clockwise), for a
    wheel rolling to +x without slipping (omega clockwise, |omega| R = v_cm)."""
    # Position relative to the centre: R (sin phi, cos phi). Rotation clockwise
    # gives v_rel = v_cm (cos phi, -sin phi).
    return np.array([v_cm + v_cm * np.cos(phi), -v_cm * np.sin(phi), 0.0])


def kinetic_share(coefficient: float) -> float:
    """Fraction of a rolling body's kinetic energy that is rotational."""
    return coefficient / (1 + coefficient)


@dataclass(frozen=True)
class Incline:
    beta_deg: float = 30.0
    length: float = 3.0      # m along the slope

    @property
    def g_sin(self) -> float:
        return G * sin(radians(self.beta_deg))

    def accel(self, coefficient: float) -> float:
        """a_cm = g sin(beta) / (1 + I_cm / (M R^2)); 0 is a frictionless slide."""
        return self.g_sin / (1 + coefficient)

    @property
    def a_block(self) -> float:
        return self.accel(0.0)

    @property
    def a_cylinder(self) -> float:
        return self.accel(0.5)

    @property
    def a_ring(self) -> float:
        return self.accel(1.0)

    def time(self, coefficient: float) -> float:
        return sqrt(2 * self.length / self.accel(coefficient))


INCLINE = Incline()


def roll_down_by_energy(coefficient: float, height: float) -> float:
    """v at the bottom from M g h = 1/2 M v^2 (1 + c), for cross-checking the force law."""
    return sqrt(2 * G * height / (1 + coefficient))


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------


@dataclass
class Report:
    failures: list[str] = field(default_factory=list)

    def check(self, ok: bool, message: str) -> None:
        if not ok:
            self.failures.append(message)


def verify() -> list[str]:
    r = Report()
    close = lambda a, b, tol=1e-9: abs(a - b) <= tol  # noqa: E731

    r.check(close(COM_PAIR.x_cm, 3.0), "x_cm = 3 m")
    r.check(close(COM_PAIR.moment, 24.0) and close(COM_PAIR.total, 8.0), "24 / 8")
    r.check(close((COM_PAIR.x_cm - COM_PAIR.x1) / (COM_PAIR.x2 - COM_PAIR.x_cm), COM_PAIR.m2 / COM_PAIR.m1),
            "distances in the inverse ratio of the masses")
    masses, positions = particle_cloud()
    shift = np.array([2.0, -1.0, 0.5])
    r.check(np.allclose(com(masses, positions + shift), com(masses, positions) + shift),
            "centre of mass does not depend on the origin")

    times, frames, pairs = spring_cluster_run(True)
    m = np.asarray(SPRINGS.masses)
    expected = 0.5 * SPRINGS.a_cm * times[-1] ** 2
    drift = com(m, frames[0])
    v0 = (com(m, frames[1]) - com(m, frames[0])) / (times[1] - times[0])
    actual = com(m, frames[-1]) - drift
    r.check(np.linalg.norm(v0) < 0.02, "cluster starts with its centre at rest")
    r.check(np.allclose(actual, expected, atol=2e-3), f"cluster centre follows F/M: {actual} vs {expected}")

    r.check(np.allclose(fragment_com(FIREWORK.burst_time + 0.5), shell_position(FIREWORK.burst_time + 0.5)),
            "fragments' centre stays on the parabola after the burst")
    r.check(first_landing() > FIREWORK.burst_time + 0.4, "fragments stay airborne for the shot")
    r.check(np.allclose((np.asarray(FIREWORK.masses)[:, None] * fragment_kicks()).sum(axis=0), 0), "burst is internal")

    c = CARTS
    r.check(close(c.momentum, 3.0) and close(c.total, 5.0) and close(c.v_cm, 0.6), "P = 3, v_cm = 0.6")
    r.check(np.allclose(c.elastic_after, (-1.8, 2.2)), "elastic outcome -1.8, 2.2")
    t, xs, vs = cart_run()
    mm = np.array([c.m1, c.m2])
    p = vs @ mm
    r.check(np.allclose(p, c.momentum, atol=1e-6), "bumper conserves momentum")
    r.check(np.allclose(vs[-1], c.elastic_after, atol=0.02), f"bumper ends elastic: {vs[-1]}")
    xcm = xs @ mm / mm.sum()
    r.check(np.allclose(np.diff(xcm) / np.diff(t), c.v_cm, atol=1e-3), "cart centre glides at 0.6 m/s")

    d = DOOR
    r.check(close(d.tau_far, 16.0) and close(d.tau_near, 4.0), "door 16 and 4 N m")
    r.check(close(torque_z((d.r_far, 0), (0, d.force)), 16.0), "r x F for the door")
    r.check(close(torque_z((d.r_far, 0), (-d.force, 0)), 0.0), "push at the hinge gives no torque")
    s = SEESAW
    r.check(close(s.tau_ccw, 200) and close(s.tau_cw, 200) and close(s.net_torque, 0) and close(s.pivot, 300),
            "seesaw 200 / 200 / 300")
    taus = torque_z((-s.d_left, 0), (0, -s.w_left)) + torque_z((s.d_right, 0), (0, -s.w_right))
    r.check(close(taus, 0.0), "seesaw torques as cross products")

    b = DUMBBELL
    r.check(close(b.i_in, 2.0) and close(b.i_out, 8.0), "dumbbell 2 -> 8 kg m^2")
    for sh in SHAPES:
        r.check(abs(numeric_coefficient(sh.key) - float(sh.coefficient)) < 1e-5,
                f"{sh.key}: integral {numeric_coefficient(sh.key):.6f} vs {sh.coefficient}")
    r.check(close(shape("ring").coefficient / shape("disc").coefficient, 2), "ring = 2 x disc")
    r.check(close(GYRATION.disc, 1 / sqrt(2)), "disc k = R / sqrt 2")
    r.check(AXES.rod_end == Fraction(1, 3) and AXES.rod_end == shape("rod_end").coefficient, "parallel axis 1/3")
    r.check(close(rod_inertia_about(0.5), 1 / 3), "rod about its end")
    r.check(AXES.disc_diameter == Fraction(1, 4), "perpendicular axis 1/4")
    # Perpendicular axis theorem, numerically, on a disc lamina.
    n = 600
    xs_, ys_ = np.meshgrid((np.arange(n) + 0.5) / n * 2 - 1, (np.arange(n) + 0.5) / n * 2 - 1)
    inside = xs_ ** 2 + ys_ ** 2 <= 1
    ix = float((ys_[inside] ** 2).mean())
    iz = float((xs_[inside] ** 2 + ys_[inside] ** 2).mean())
    r.check(abs(ix - 0.25) < 2e-3 and abs(iz - 0.5) < 2e-3, f"lamina integrals {ix:.4f}, {iz:.4f}")

    w = WHEEL
    r.check(close(w.omega, 8) and close(w.angle, 16) and f"{w.revolutions:.2f}" == "2.55", "wheel 8, 16, 2.55")
    dd = DISC
    r.check(close(dd.inertia, 0.5) and close(dd.alpha, 2.0) and close(dd.alpha, w.alpha), "disc I 0.5, alpha 2")
    r.check(close(dd.string_force, 2.0), "string pulls 2 N")
    r.check(close(dd.kinetic, 16) and close(dd.work, 16) and close(dd.power_end, 8), "K = W = 16 J; P = 8 W")
    at, ar, a = accelerations(1.0, 2.0, 8.0)
    r.check(close(a, np.hypot(at, ar)), "a = sqrt(at^2 + ar^2)")

    k = SKATER
    r.check(close(k.inertia(k.r_out), 4) and close(k.inertia(k.r_in), 2), "skater I 4 -> 2")
    r.check(close(k.momentum, 8) and close(k.omega_in, 4), "L 8, omega 4")
    r.check(close(k.k_out, 8) and close(k.k_in, 16) and close(k.work, 8), "K 8 -> 16, arms do 8 J")
    r.check(abs(skater_work_by_integration() - k.work) < 1e-4, f"pull work {skater_work_by_integration():.5f}")

    r.check(np.allclose(rolling_point_velocity(0.0), [2, 0, 0]), "top moves at 2 v_cm")
    r.check(np.allclose(rolling_point_velocity(pi), [0, 0, 0], atol=1e-12), "contact point at rest")
    r.check(close(kinetic_share(0.5), 1 / 3) and close(kinetic_share(1.0), 0.5), "energy shares 1/3 and 1/2")
    inc = INCLINE
    r.check(f"{inc.a_cylinder:.2f}" == "3.27" and f"{inc.a_ring:.2f}" == "2.45" and f"{inc.a_block:.1f}" == "4.9",
            "incline 3.27, 2.45, 4.9")
    r.check(close(inc.a_cylinder / inc.g_sin, 2 / 3) and close(inc.a_ring / inc.g_sin, 0.5), "2/3 and 1/2 g sin")
    h = inc.length * sin(radians(inc.beta_deg))
    for coef in (0.0, 0.5, 1.0):
        v_kin = inc.accel(coef) * inc.time(coef)
        r.check(close(v_kin, roll_down_by_energy(coef, h), 1e-9), f"force law agrees with energy for c={coef}")
    r.check(inc.time(0.0) < inc.time(0.5) < inc.time(1.0), "block, then cylinder, then ring")
    return r.failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Physics check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("Physics check passed: centres of mass, spring cluster (a_cm = F/M), firework, carts, torques, "
          "seesaw, seven moments of inertia by integration, axis theorems, spin-up, disc, skater work, rolling, race.")
