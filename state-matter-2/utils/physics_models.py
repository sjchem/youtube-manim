"""The physics the film draws: constants, data, worked examples and simulations.

Nothing here imports Manim. Every number a scene shows or the narrator says
is computed in this module (``python -m utils.physics_models`` re-checks the
worked examples and the simulations), and ``utils.spoken_numbers`` confirms
the spoken words still match.

Sources
-------
* Exact SI constants: k_B = 1.380649e-23 J/K, N_A = 6.02214076e23 /mol
  (2019 SI redefinition, CODATA); R = N_A k_B = 8.314462618 J/(mol K).
* Characteristic speeds u_mp, u_av, u_rms and their ratio; kinetic molecular
  theory; van der Waals equation; compressibility factor; critical constants
  of H2, N2, O2, CO2, NH3, H2O; vapour pressure, surface tension, viscosity:
  NCERT Chemistry Part I, Class 11, Unit 5 (States of Matter), sections 5.7-5.11
  and its tables of critical constants.
* Van der Waals constants a (L^2 bar mol^-2) and b (L mol^-1): CRC Handbook of
  Chemistry and Physics, "Van der Waals constants for gases".
* Boyle temperatures (N2 327.2 K, He 22.64 K): Atkins' Physical Chemistry,
  table of second virial coefficients and Boyle temperatures.
* Andrews' carbon-dioxide isotherms (13.1, 21.5, 31.1, 35.5, 48.1 degC):
  T. Andrews, Phil. Trans. R. Soc. 159, 575 (1869), the Bakerian Lecture.
* Water saturation pressure: IAPWS SR1-86(1992), up to the critical point.
* Antoine constants (P in mmHg, T in degC) for ethanol and diethyl
  ether: the widely tabulated Dortmund Data Bank fits (e.g. Lange's Handbook).
* Surface tension of water: IAPWS Revised Release on Surface Tension of
  Ordinary Water Substance (2014), gamma = 235.8 tau^1.256 (1 - 0.625 tau) mN/m.
* Viscosity of liquid water at 0.1 MPa, 0-100 degC: CRC Handbook (mPa s).
* Saturated CO2 at 20 degC (57.3 bar) and the normal and standard boiling
  points of water: NIST Chemistry WebBook (fluid properties).

Visual models
-------------
``IdealGas`` (point molecules with Maxwell-Boltzmann velocities, exact wall
reflections) is the same model as in Part 1. ``HardSphereGas`` is a live,
deterministic gas of equal-mass hard spheres: real excluded volume, real
sphere-sphere collisions, real wall hits. ``disk_movie`` is a 2D hard-disk
simulation started with every disk at the same speed; collisions relax it to
the 2D equilibrium (Rayleigh) distribution. The van der Waals model is used in
reduced units with Maxwell's equal-area construction; on screen it is always
called a model.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from functools import lru_cache
from math import ceil, log10, pi, sqrt
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Constants (exact SI values)
# ---------------------------------------------------------------------------

K_B = 1.380649e-23            # J/K
N_A = 6.02214076e23           # 1/mol
R = K_B * N_A                 # 8.314462618 J/(mol K)
R_L_BAR = R / 100.0           # 0.08314 L bar/(mol K)  (1 L bar = 100 J)
BAR = 1.0e5                   # Pa
ATM = 101325.0                # Pa
ATM_BAR = ATM / BAR           # 1.01325
T_ICE = 273.15                # K at 0 degC
MMHG_BAR = ATM_BAR / 760.0    # 1 mmHg in bar

ROOM_T = 300.0                # K, the film's "room temperature" in worked examples

# Molar masses, kg/mol (IUPAC standard atomic weights).
MOLAR_MASS: dict[str, float] = {
    "H2": 2.016e-3, "He": 4.0026e-3, "CH4": 16.043e-3, "NH3": 17.031e-3, "H2O": 18.015e-3,
    "N2": 28.014e-3, "O2": 31.998e-3, "CO2": 44.009e-3, "Cl2": 70.906e-3,
}


def celsius(kelvin: float) -> float:
    return kelvin - T_ICE


def kelvin(celsius_value: float) -> float:
    return celsius_value + T_ICE


# ---------------------------------------------------------------------------
# Chapter 2 — speeds: Maxwell-Boltzmann in SI units
# ---------------------------------------------------------------------------


def u_mp(T: float, M: float) -> float:
    """Most probable speed sqrt(2RT/M), m/s (M in kg/mol)."""
    return sqrt(2 * R * T / M)


def u_av(T: float, M: float) -> float:
    """Average (mean) speed sqrt(8RT/(pi M)), m/s."""
    return sqrt(8 * R * T / (pi * M))


def u_rms(T: float, M: float) -> float:
    """Root-mean-square speed sqrt(3RT/M), m/s."""
    return sqrt(3 * R * T / M)


SPEED_RATIO = (1.0, sqrt(4 / pi), sqrt(3 / 2))    # u_mp : u_av : u_rms = 1 : 1.128 : 1.225


def mb_pdf(u, T: float, M: float):
    """3D Maxwell-Boltzmann speed density f(u) = 4 pi (m / 2 pi kT)^1.5 u^2 exp(-m u^2 / 2kT), per (m/s)."""
    u = np.asarray(u, dtype=float)
    m_over_kT = M / (R * T)                       # m/(k_B T) = M/(R T)
    return 4 * pi * (m_over_kT / (2 * pi)) ** 1.5 * u * u * np.exp(-m_over_kT * u * u / 2)


def maxwell_pdf(s, rms: float = 1.0):
    """3D speed distribution with root-mean-square speed ``rms`` (any units)."""
    sigma = rms / sqrt(3)
    s = np.asarray(s, dtype=float)
    return sqrt(2 / pi) * s * s / sigma ** 3 * np.exp(-s * s / (2 * sigma * sigma))


def rayleigh_pdf(s, rms: float = 1.0):
    """2D equilibrium speed distribution with root-mean-square speed ``rms``."""
    s = np.asarray(s, dtype=float)
    return 2 * s / rms ** 2 * np.exp(-s * s / rms ** 2)


def gaussian_component_pdf(v, rms: float = 1.0):
    """One Cartesian velocity component of a 3D Maxwellian with total rms speed ``rms``."""
    sigma = rms / sqrt(3)
    v = np.asarray(v, dtype=float)
    return np.exp(-v * v / (2 * sigma * sigma)) / (sigma * sqrt(2 * pi))


@dataclass(frozen=True)
class SpeedExample:
    """Nitrogen at 300 K (and heated to 600 K) against chlorine at 300 K."""

    T1: float = 300.0
    T2: float = 600.0
    light: str = "N2"
    heavy: str = "Cl2"

    @property
    def mp(self) -> float:
        return u_mp(self.T1, MOLAR_MASS[self.light])

    @property
    def av(self) -> float:
        return u_av(self.T1, MOLAR_MASS[self.light])

    @property
    def rms(self) -> float:
        return u_rms(self.T1, MOLAR_MASS[self.light])

    @property
    def heat_factor(self) -> float:
        return sqrt(self.T2 / self.T1)

    @property
    def mass_ratio(self) -> float:
        return MOLAR_MASS[self.heavy] / MOLAR_MASS[self.light]

    @property
    def heavy_mp(self) -> float:
        return u_mp(self.T1, MOLAR_MASS[self.heavy])

    @property
    def grams_error(self) -> float:
        """Factor by which a speed comes out wrong if M is entered in g/mol."""
        return sqrt(1000.0)


SPEEDS = SpeedExample()

# Kinetic (collision) diameter of N2, used only for the collision frequency.
N2_COLLISION_DIAMETER = 0.364e-9    # m (Hirschfelder, Curtiss & Bird)


def number_density(P: float, T: float) -> float:
    """Molecules per m^3 for an ideal gas at P (Pa) and T (K)."""
    return P / (K_B * T)


def collision_frequency(P: float, T: float, M: float, diameter: float) -> float:
    """Collisions per second for one molecule: sqrt(2) pi d^2 n <u>."""
    return sqrt(2) * pi * diameter ** 2 * number_density(P, T) * u_av(T, M)


N2_COLLISIONS_PER_S = collision_frequency(BAR, ROOM_T, MOLAR_MASS["N2"], N2_COLLISION_DIAMETER)


# ---------------------------------------------------------------------------
# Chapter 2 — one elastic collision between equal masses (scene 03)
# ---------------------------------------------------------------------------


def elastic_collision(v1, v2, normal) -> tuple[np.ndarray, np.ndarray]:
    """Equal masses: exchange the velocity components along the contact normal."""
    v1, v2 = np.asarray(v1, dtype=float), np.asarray(v2, dtype=float)
    n = np.asarray(normal, dtype=float)
    n = n / np.linalg.norm(n)
    exchange = float(np.dot(v1 - v2, n))
    return v1 - exchange * n, v2 + exchange * n


@dataclass(frozen=True)
class CollisionExample:
    """Two identical molecules, same speed, meeting off-centre (2D, in the plane of the drawing)."""

    speed: float = 1.0
    angle_1: float = 0.0                     # molecule 1 moves to the right
    angle_2: float = np.radians(212.0)       # molecule 2 moves left and slightly down
    normal_angle: float = np.radians(70.0)   # contact normal, from molecule 1 toward molecule 2 (above right)

    @property
    def before(self) -> tuple[np.ndarray, np.ndarray]:
        a, b = self.angle_1, self.angle_2
        return (self.speed * np.array([np.cos(a), np.sin(a)]), self.speed * np.array([np.cos(b), np.sin(b)]))

    @property
    def normal(self) -> np.ndarray:
        return np.array([np.cos(self.normal_angle), np.sin(self.normal_angle)])

    @property
    def after(self) -> tuple[np.ndarray, np.ndarray]:
        return elastic_collision(*self.before, self.normal)

    @property
    def speeds_after(self) -> tuple[float, float]:
        a, b = self.after
        return float(np.linalg.norm(a)), float(np.linalg.norm(b))


COLLISION = CollisionExample()


# ---------------------------------------------------------------------------
# Chapter 2 — a 2D hard-disk gas that starts with one speed (scene 04)
# ---------------------------------------------------------------------------

DISK_BOX = (48.0, 27.0)       # simulation units (16:9)
DISK_COUNT = 240
DISK_RADIUS = 0.42
DISK_SPEED = 1.0              # every disk starts at this speed
DISK_DT = 0.01
DISK_EVERY = 5                # store one frame every 5 steps
DISK_DURATION = 60.0
CACHE_DIR = Path(__file__).resolve().parents[1] / "output" / ".cache"


def _disk_start(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    W, H = DISK_BOX
    cols = int(np.ceil(np.sqrt(DISK_COUNT * W / H)))
    rows = int(np.ceil(DISK_COUNT / cols))
    xs, ys = (np.arange(cols) + 0.5) * W / cols, (np.arange(rows) + 0.5) * H / rows
    grid = np.array([(x, y) for y in ys for x in xs])[:DISK_COUNT]
    jitter = rng.uniform(-0.25, 0.25, size=grid.shape) * np.array([W / cols, H / rows]) * 0.4
    pos = grid + jitter
    angle = rng.uniform(0, 2 * pi, size=DISK_COUNT)
    vel = DISK_SPEED * np.column_stack([np.cos(angle), np.sin(angle)])
    return pos, vel


def _disk_step(pos: np.ndarray, vel: np.ndarray, dt: float) -> None:
    W, H = DISK_BOX
    r = DISK_RADIUS
    pos += vel * dt
    for axis, size in ((0, W), (1, H)):
        low, high = pos[:, axis] < r, pos[:, axis] > size - r
        pos[low, axis] = 2 * r - pos[low, axis]
        pos[high, axis] = 2 * (size - r) - pos[high, axis]
        vel[low, axis] = np.abs(vel[low, axis])
        vel[high, axis] = -np.abs(vel[high, axis])
    d = pos[:, None, :] - pos[None, :, :]
    dist2 = (d * d).sum(-1)
    i, j = np.nonzero(np.triu(dist2 < (2 * r) ** 2, 1))
    for a, b in zip(i, j):
        delta = pos[a] - pos[b]
        dist = float(np.linalg.norm(delta))
        if dist < 1e-12:
            continue
        n = delta / dist
        approach = float(np.dot(vel[a] - vel[b], n))
        if approach < 0:                     # moving together: exchange normal components
            vel[a] -= approach * n
            vel[b] += approach * n
        overlap = 2 * r - dist               # separate, so pairs never stick
        pos[a] += n * overlap / 2
        pos[b] -= n * overlap / 2


@lru_cache(maxsize=1)
def disk_movie(seed: int = 20261115) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run the one-speed start once and cache it (memory and output/.cache).

    Returns (positions [frames, N, 2] centred on the box, velocities
    [frames, N, 2], times [frames]). Total kinetic energy is conserved."""
    key = hashlib.sha1(repr((seed, DISK_BOX, DISK_COUNT, DISK_RADIUS, DISK_SPEED, DISK_DT, DISK_EVERY,
                             DISK_DURATION, 1)).encode()).hexdigest()[:12]
    cached = CACHE_DIR / f"disk_movie_{key}.npz"
    if cached.is_file():
        data = np.load(cached)
        return data["pos"], data["vel"], data["times"]
    rng = np.random.default_rng(seed)
    pos, vel = _disk_start(rng)
    centre = np.array(DISK_BOX) / 2
    frames_p, frames_v, times = [], [], []
    steps = int(round(DISK_DURATION / DISK_DT))
    for step in range(steps + 1):
        if step % DISK_EVERY == 0:
            frames_p.append((pos - centre).astype(np.float32))
            frames_v.append(vel.astype(np.float32))
            times.append(step * DISK_DT)
        _disk_step(pos, vel, DISK_DT)
    out = (np.array(frames_p), np.array(frames_v), np.array(times))
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(cached, pos=out[0], vel=out[1], times=out[2])
    except OSError:
        pass   # a read-only checkout still works, only slower
    return out


def rayleigh_distance(speeds: np.ndarray, rms: float = 1.0) -> float:
    """Largest gap between the sample's cumulative distribution and the 2D equilibrium one."""
    s = np.sort(np.asarray(speeds, dtype=float))
    empirical = np.arange(1, len(s) + 1) / len(s)
    model = 1 - np.exp(-s * s / rms ** 2)
    return float(np.max(np.abs(empirical - model)))


# ---------------------------------------------------------------------------
# The film's gases (visual models)
# ---------------------------------------------------------------------------


def fold(phase):
    """Triangle wave: an unbounded phase folded into [0, 1] (period 2): elastic reflection."""
    p = np.mod(phase, 2.0)
    return 1.0 - np.abs(p - 1.0)


class IdealGas:
    """Point molecules with Maxwell-Boltzmann velocities in a reflecting box.

    Velocities ``u`` are in units of the root-mean-square speed. A molecule's
    position along each axis is ``lo + extent * fold(phase)``; its phase grows
    at ``speed * u / extent``. ``species`` (0 or 1) lets two gases share the
    box; heavier species move more slowly at the same temperature.
    """

    def __init__(self, count: int, seed: int, *, species: np.ndarray | None = None,
                 masses: tuple[float, float] = (1.0, 1.0)) -> None:
        rng = np.random.default_rng(seed)
        self.count = count
        self.u = rng.normal(scale=1 / sqrt(3), size=(count, 3))
        self.phase = rng.uniform(0.0, 2.0, size=(count, 3))
        self.species = np.zeros(count, dtype=int) if species is None else np.asarray(species, dtype=int)
        self.masses = np.asarray(masses, dtype=float)
        self.slow = np.sqrt(self.masses[0] / self.masses[self.species])
        self.active = np.ones(count, dtype=bool)

    def velocities(self, heat: float = 1.0) -> np.ndarray:
        return self.u * (heat * self.slow)[:, None]

    def advance(self, dt: float, extent, speed: float, heat: float = 1.0) -> list[tuple[int, int, int]]:
        """Move every active molecule for ``dt``; return wall hits (molecule, axis, side)."""
        extent = np.asarray(extent, dtype=float)
        step = self.u * (speed * heat * self.slow)[:, None] * dt / extent[None, :]
        step[~self.active] = 0.0
        before = self.phase
        after = before + step
        self.phase = after
        lo, hi = np.floor(before), np.floor(after)
        hits = []
        for i, axis in np.argwhere(lo != hi):
            a, b = before[i, axis], after[i, axis]
            first, last = (int(np.floor(a)) + 1, int(np.floor(b))) if b > a else (int(np.floor(b)) + 1, int(np.floor(a)))
            for k in range(first, last + 1):
                hits.append((int(i), int(axis), 1 if k % 2 else 0))
        return hits

    def positions(self, lo, extent) -> np.ndarray:
        return np.asarray(lo, dtype=float)[None, :] + np.asarray(extent, dtype=float)[None, :] * fold(self.phase)

    def place(self, index: int, fraction, inward_axis: int = 0) -> None:
        """Put molecule ``index`` at a fractional point of the box, heading inward along ``inward_axis``."""
        f = np.clip(np.asarray(fraction, dtype=float), 0.0, 1.0)
        self.phase[index] = f
        self.u[index, inward_axis] = abs(self.u[index, inward_axis])

    def mean_square(self, heat: float = 1.0) -> np.ndarray:
        v = self.velocities(heat)[self.active]
        weight = (self.masses[self.species[self.active]] / self.masses[0])[:, None]
        return (weight * v * v).mean(axis=0)


class HardSphereGas:
    """Equal-mass hard spheres of radius ``radius`` (stage units) in a box.

    The same interface as ``IdealGas``, so a ``GasCloud`` can draw it, but the
    spheres have real size: they collide elastically with each other (normal
    velocity components exchanged) and their centres reflect at ``radius``
    from each wall. Positions are stored relative to the box's low corner;
    when the box shrinks (a piston), spheres are pushed inside it. Motion is
    deterministic: each frame is split into fixed sub-steps.
    """

    def __init__(self, count: int, seed: int, radius: float, extent, *, max_step: float = 1 / 240) -> None:
        rng = np.random.default_rng(seed)
        self.count, self.radius, self.max_step = count, float(radius), float(max_step)
        self.u = rng.normal(scale=1 / sqrt(3), size=(count, 3))
        self.species = np.zeros(count, dtype=int)
        self.masses = np.array([1.0, 1.0])
        self.slow = np.ones(count)
        self.active = np.ones(count, dtype=bool)
        extent = np.asarray(extent, dtype=float)
        self.pos = self._insert(rng, extent)

    def _insert(self, rng: np.random.Generator, extent: np.ndarray) -> np.ndarray:
        r = self.radius
        placed: list[np.ndarray] = []
        tries = 0
        while len(placed) < self.count:
            tries += 1
            if tries > 200000:
                raise ValueError("box too small for the requested hard spheres")
            p = r + rng.uniform(0, 1, 3) * (extent - 2 * r)
            if all(np.linalg.norm(p - q) >= 2.05 * r for q in placed):
                placed.append(p)
        return np.array(placed)

    def velocities(self, heat: float = 1.0) -> np.ndarray:
        return self.u * heat

    def advance(self, dt: float, extent, speed: float, heat: float = 1.0) -> list[tuple[int, int, int]]:
        extent = np.asarray(extent, dtype=float)
        r = self.radius
        hits: list[tuple[int, int, int]] = []
        np.clip(self.pos, r, extent - r, out=self.pos)          # a moving piston pushes spheres in
        steps = max(1, int(ceil(dt / self.max_step)))
        h = dt / steps
        scale = speed * heat
        for _ in range(steps):
            self.pos += self.u * scale * h
            for axis in range(3):
                low, high = self.pos[:, axis] < r, self.pos[:, axis] > extent[axis] - r
                self.pos[low, axis] = 2 * r - self.pos[low, axis]
                self.pos[high, axis] = 2 * (extent[axis] - r) - self.pos[high, axis]
                self.u[low, axis] = np.abs(self.u[low, axis])
                self.u[high, axis] = -np.abs(self.u[high, axis])
                hits += [(int(i), axis, 0) for i in np.nonzero(low)[0]]
                hits += [(int(i), axis, 1) for i in np.nonzero(high)[0]]
            d = self.pos[:, None, :] - self.pos[None, :, :]
            dist2 = (d * d).sum(-1)
            i_idx, j_idx = np.nonzero(np.triu(dist2 < (2 * r) ** 2, 1))
            for a, b in zip(i_idx, j_idx):
                delta = self.pos[a] - self.pos[b]
                dist = float(np.linalg.norm(delta))
                if dist < 1e-12:
                    continue
                n = delta / dist
                approach = float(np.dot(self.u[a] - self.u[b], n))
                if approach < 0:
                    self.u[a] -= approach * n
                    self.u[b] += approach * n
                push = (2 * r - dist) / 2
                self.pos[a] += n * push
                self.pos[b] -= n * push
            np.clip(self.pos, r, extent - r, out=self.pos)
        return hits

    def positions(self, lo, extent) -> np.ndarray:
        return np.asarray(lo, dtype=float)[None, :] + self.pos

    def place(self, index: int, fraction, inward_axis: int = 0) -> None:
        raise NotImplementedError("hard spheres are never injected")

    def mean_square(self, heat: float = 1.0) -> np.ndarray:
        v = self.velocities(heat)[self.active]
        return (v * v).mean(axis=0)

    def packing_fraction(self, extent) -> float:
        return float(self.count * 4 / 3 * pi * self.radius ** 3 / np.prod(np.asarray(extent, dtype=float)))


def carnahan_starling(eta: float) -> float:
    """Hard-sphere compressibility Z = (1 + eta + eta^2 - eta^3) / (1 - eta)^3."""
    return (1 + eta + eta * eta - eta ** 3) / (1 - eta) ** 3


def pressure_ratio(n_ratio: float = 1.0, T_ratio: float = 1.0, V_ratio: float = 1.0) -> float:
    """P / P_ref for an ideal gas."""
    return n_ratio * T_ratio / V_ratio


# ---------------------------------------------------------------------------
# Chapter 3 — how empty is air? (scene 09)
# ---------------------------------------------------------------------------

# Van der Waals constants: a in L^2 bar / mol^2, b in L / mol (CRC Handbook).
VDW: dict[str, tuple[float, float]] = {
    "He": (0.0346, 0.0238),
    "H2": (0.2476, 0.02661),
    "N2": (1.370, 0.0387),
    "O2": (1.382, 0.03186),
    "CH4": (2.283, 0.04278),
    "CO2": (3.640, 0.04267),
    "NH3": (4.225, 0.0371),
    "H2O": (5.536, 0.03049),
}


def molecular_volume_fraction(gas: str = "N2", P_bar: float = 1.0, T: float = ROOM_T) -> float:
    """Fraction of a gas's volume filled by the molecules themselves, taking each
    molecule's volume as b / (4 N_A) (hard-sphere relation b = 4 N_A v_molecule)."""
    _, b = VDW[gas]
    per_mole = b / 4                         # L/mol of molecular volume
    molar_volume = R_L_BAR * T / P_bar       # L/mol
    return per_mole / molar_volume


# ---------------------------------------------------------------------------
# Chapter 4 — attraction near a wall, the tug of war (scenes 10-12)
# ---------------------------------------------------------------------------


def lennard_jones(r, epsilon: float = 1.0, sigma: float = 1.0):
    r = np.asarray(r, dtype=float)
    q = (sigma / r) ** 6
    return 4 * epsilon * (q * q - q)


LJ_MINIMUM = 2 ** (1 / 6)

# Two molecules passing each other in the Lennard-Jones potential (scene 09):
# reduced units (sigma = epsilon = mass = 1), impact parameter LJ_IMPACT.
LJ_IMPACT = 1.9
LJ_FAST, LJ_SLOW = 3.0, 0.4      # relative speeds: a hot pass barely bends, a cold one swings round


@lru_cache(maxsize=4)
def lj_encounter(v: float, b: float = LJ_IMPACT, x0: float = 5.0, dt: float = 0.002,
                 t_max: float = 40.0) -> tuple[np.ndarray, np.ndarray]:
    """Relative path r(t) of two equal molecules (reduced mass 1/2) that approach from
    x = -x0 with speed ``v`` and impact parameter ``b``. Velocity Verlet; returns
    (times, r) until the pair separates beyond x0 again. Each molecule sits at -/+ r/2."""

    def acc(r: np.ndarray) -> np.ndarray:
        d2 = float(r @ r)
        q6 = d2 ** -3
        return 48 * (2 * q6 * q6 - q6) / d2 * r      # -(2 / m) dU/dr along r, m = 1

    r = np.array([-x0, b], dtype=float)
    u = np.array([v, 0.0])
    a = acc(r)
    times, path = [0.0], [r.copy()]
    t = 0.0
    while t < t_max:
        u += 0.5 * dt * a
        r += dt * u
        a = acc(r)
        u += 0.5 * dt * a
        t += dt
        times.append(t)
        path.append(r.copy())
        if np.linalg.norm(r) > x0 + 0.2 and r @ u > 0:
            break
    return np.array(times), np.array(path)


# ---------------------------------------------------------------------------
# Chapter 5 — van der Waals (scenes 13-15)
# ---------------------------------------------------------------------------


def vdw_pressure(n: float, V: float, T: float, a: float, b: float) -> float:
    """(P + a n^2/V^2)(V - n b) = n R T solved for P (bar, L, K)."""
    return n * R_L_BAR * T / (V - n * b) - a * n * n / (V * V)


def ideal_pressure(n: float, V: float, T: float) -> float:
    return n * R_L_BAR * T / V


@dataclass(frozen=True)
class FlaskExample:
    """One mole of CO2 in a one-litre flask at 300 K, and the same mole in 100 L."""

    gas: str = "CO2"
    n: float = 1.0
    V: float = 1.0
    T: float = ROOM_T
    V_dilute: float = 100.0

    @property
    def ideal(self) -> float:
        return ideal_pressure(self.n, self.V, self.T)

    @property
    def size_only(self) -> float:
        """n R T / (V - n b): the volume correction alone."""
        _, b = VDW[self.gas]
        return self.n * R_L_BAR * self.T / (self.V - self.n * b)

    @property
    def attraction(self) -> float:
        """a n^2 / V^2: the pressure the attraction takes away."""
        a, _ = VDW[self.gas]
        return a * self.n ** 2 / self.V ** 2

    @property
    def vdw(self) -> float:
        a, b = VDW[self.gas]
        return vdw_pressure(self.n, self.V, self.T, a, b)

    @property
    def percent_below(self) -> float:
        return 100 * (self.ideal - self.vdw) / self.ideal

    @property
    def Z(self) -> float:
        return self.vdw / self.ideal

    @property
    def dilute_difference_percent(self) -> float:
        a, b = VDW[self.gas]
        ideal = ideal_pressure(self.n, self.V_dilute, self.T)
        return 100 * abs(vdw_pressure(self.n, self.V_dilute, self.T, a, b) - ideal) / ideal


FLASK = FlaskExample()

# Hard spheres of diameter d: the forbidden sphere around one centre has radius d,
# i.e. 8 times one molecule's volume; shared by a pair, 4 times per molecule.
EXCLUSION_RATIO = 8
EXCLUDED_PER_MOLECULE = 4


def pair_count(points: np.ndarray, cutoff: float) -> int:
    """Number of pairs closer than ``cutoff``."""
    d = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
    return int(np.count_nonzero(np.triu(d < cutoff, 1)))


@lru_cache(maxsize=4)
def pair_demo(count: int = 18, cutoff: float = 0.42, base_seed: int = 7) -> tuple[np.ndarray, np.ndarray, int, int]:
    """Random points in a unit cube at density n and 2n, chosen (seed search) so that the
    nearby-pair count grows by close to the expected factor (2n)(2n - 1) / (n (n - 1)) ~ 4.

    Returns (dilute points, dense points, dilute pairs, dense pairs). The dense
    set contains the dilute one, so 'double the density' adds molecules."""
    seed = base_seed
    while True:
        rng = np.random.default_rng(seed)
        dense = rng.uniform(0, 1, size=(2 * count, 3))
        dilute = dense[:count]
        p1, p2 = pair_count(dilute, cutoff), pair_count(dense, cutoff)
        if p1 >= 6 and 3.8 <= p2 / p1 <= 4.3:
            return dilute, dense, p1, p2
        seed += 1


# ---------------------------------------------------------------------------
# Chapter 6 — compressibility factor (scenes 16-17)
# ---------------------------------------------------------------------------


def z_vdw(P_bar: float, T: float, gas: str) -> float:
    """Z = P V_m / R T of the van der Waals gas (largest real molar-volume root)."""
    a, b = VDW[gas]
    RT = R_L_BAR * T
    if P_bar <= 0:
        return 1.0
    roots = np.roots([P_bar, -(P_bar * b + RT), a, -a * b])
    real = roots[np.abs(roots.imag) < 1e-9].real
    real = real[real > b]
    Vm = float(real.max())
    return P_bar * Vm / RT


BOYLE_T: dict[str, float] = {"N2": 327.2, "He": 22.64}     # K, measured (Atkins)
VDW_BOYLE_REDUCED = 27 / 8                                    # T_B / T_c for a van der Waals gas


def vdw_reduced(vr, tr):
    """Reduced van der Waals isotherm: p_r = 8 t_r / (3 v_r - 1) - 3 / v_r^2."""
    vr = np.asarray(vr, dtype=float)
    return 8 * tr / (3 * vr - 1) - 3 / (vr * vr)


def _reduced_volumes(pr: float, tr: float) -> np.ndarray:
    """Real roots v_r > 1/3 of 3 p v^3 - (p + 8 t) v^2 + 9 v - 3 = 0, ascending."""
    roots = np.roots([3 * pr, -(pr + 8 * tr), 9.0, -3.0])
    real = np.sort(roots[np.abs(roots.imag) < 1e-7].real)
    return real[real > 1 / 3 + 1e-9]


def z_reduced(pr: float, tr: float) -> float:
    """Compressibility factor of a van der Waals fluid at reduced (p, t).

    Below the critical temperature the stable phase is chosen with Maxwell's
    construction (vapour below the coexistence pressure, liquid above)."""
    if pr <= 0:
        return 1.0
    vols = _reduced_volumes(pr, tr)
    if tr < 1 and len(vols) > 1:
        p_sat, _, _ = maxwell(tr)
        v = vols[-1] if pr < p_sat else vols[0]
    else:
        v = vols[-1]
    return 3 / 8 * pr * v / tr


@lru_cache(maxsize=256)
def maxwell(tr: float) -> tuple[float, float, float]:
    """Maxwell's equal-area construction below the critical point (t_r < 1).

    Returns (coexistence pressure p_r, liquid v_r, vapour v_r)."""
    if not 0.3 < tr < 1:
        raise ValueError("Maxwell construction needs 0.3 < t_r < 1")

    def roots_at(p: float) -> np.ndarray:
        return _reduced_volumes(p, tr)

    def area_gap(p: float) -> float:
        v = roots_at(p)
        vl, vg = v[0], v[-1]
        # integral of p_r dv from vl to vg minus p (vg - vl)
        integral = 8 * tr / 3 * np.log((3 * vg - 1) / (3 * vl - 1)) + 3 / vg - 3 / vl
        return integral - p * (vg - vl)

    # The spinodal pressures bound the search.
    vs = np.linspace(0.34, 8, 40000)
    ps = vdw_reduced(vs, tr)
    dp = np.diff(ps)
    turns = np.nonzero(np.sign(dp[1:]) != np.sign(dp[:-1]))[0] + 1
    p_min, p_max = ps[turns[0]], ps[turns[1]]
    lo, hi = max(p_min, 1e-9) + 1e-9, p_max - 1e-9
    for _ in range(200):
        mid = (lo + hi) / 2
        if area_gap(mid) > 0:
            lo = mid
        else:
            hi = mid
    p = (lo + hi) / 2
    v = roots_at(p)
    return float(p), float(v[0]), float(v[-1])


def isotherm(tr: float, vr: np.ndarray, flat: bool = True) -> np.ndarray:
    """Reduced pressure along an isotherm; below t_r = 1 the loop is replaced by
    the flat coexistence line when ``flat`` (as Andrews measured)."""
    vr = np.asarray(vr, dtype=float)
    p = vdw_reduced(vr, tr)
    if flat and tr < 1:
        p_sat, vl, vg = maxwell(tr)
        p = np.where((vr > vl) & (vr < vg), p_sat, p)
    return p


def binodal(samples: int = 60, t_low: float = 0.6) -> np.ndarray:
    """The coexistence dome as (v_r, p_r) points, liquid side up to the critical point and back."""
    trs = np.linspace(t_low, 0.9995, samples)
    liquid, vapour = [], []
    for tr in trs:
        p, vl, vg = maxwell(float(tr))
        liquid.append((vl, p))
        vapour.append((vg, p))
    return np.array(liquid + [(1.0, 1.0)] + vapour[::-1])


def liquid_fraction(tr: float, vr: float) -> float:
    """Lever rule: the fraction of molecules in the liquid at overall reduced volume v_r."""
    if tr >= 1:
        return 0.0
    _, vl, vg = maxwell(tr)
    if vr >= vg:
        return 0.0
    if vr <= vl:
        return 1.0
    return float((vg - vr) / (vg - vl))


# ---------------------------------------------------------------------------
# Chapter 7 — critical constants and Andrews' isotherms (scenes 18-22)
# ---------------------------------------------------------------------------

# (T_c in K, P_c in bar) — NCERT's critical-constant table; CO2 and NH3 as in the brief.
CRITICAL: dict[str, tuple[float, float]] = {
    "H2": (33.2, 12.97),
    "N2": (126.0, 33.98),
    "O2": (154.3, 50.43),
    "CO2": (304.1, 73.8),
    "NH3": (405.5, 113.0),
    "H2O": (647.1, 220.6),
}

ANDREWS_C = (13.1, 21.5, 31.1, 35.5, 48.1)     # degC, Andrews (1869)
ANDREWS_FOLLOW_C = 21.5
CO2_SAT_20C_BAR = 57.3                          # NIST: saturated CO2 at 20 degC


def co2_reduced_temperature(celsius_value: float) -> float:
    return kelvin(celsius_value) / CRITICAL["CO2"][0]


def vdw_critical_temperature(gas: str) -> float:
    """T_c = 8 a / (27 R b) for the van der Waals constants of ``gas``."""
    a, b = VDW[gas]
    return 8 * a / (27 * R_L_BAR * b)


# ---------------------------------------------------------------------------
# Chapter 8 — vapour pressure and boiling (scenes 23-24)
# ---------------------------------------------------------------------------

# Antoine: log10(P / mmHg) = A - B / (C + T / degC). Each entry lists (T_max, A, B, C).
ANTOINE: dict[str, list[tuple[float, float, float, float]]] = {
    "water": [(100.0, 8.07131, 1730.63, 233.426), (374.0, 8.14019, 1810.94, 244.485)],
    "ethanol": [(240.0, 8.20417, 1642.89, 230.300)],
    "ether": [(190.0, 6.92032, 1064.07, 228.800)],
}
EVEREST_BAR = 0.337          # summit barometric pressure (West, J. Appl. Physiol. 1999)
COOKER_BAR = 2.0             # absolute pressure inside a typical pressure cooker (~1 bar above ambient)


def _antoine(liquid: str, T_C: float) -> tuple[float, float, float]:
    for t_max, A, B, C in ANTOINE[liquid]:
        if T_C <= t_max:
            return A, B, C
    return ANTOINE[liquid][-1][1:]


def vapour_pressure(liquid: str, T_C: float) -> float:
    """Equilibrium vapour pressure in bar."""
    if liquid == "water":
        return water_saturation_pressure(kelvin(T_C))
    A, B, C = _antoine(liquid, T_C)
    return 10 ** (A - B / (C + T_C)) * MMHG_BAR


def boiling_point(liquid: str, P_bar: float) -> float:
    """Temperature (degC) at which the vapour pressure equals ``P_bar``."""
    if liquid == "water":
        lo, hi = kelvin(0.0), WATER_TC
        if not water_saturation_pressure(lo) <= P_bar <= WATER_PC_BAR:
            raise ValueError("Water saturation pressure is outside the liquid-vapour range")
        for _ in range(64):
            mid = (lo + hi) / 2
            if water_saturation_pressure(mid) < P_bar:
                lo = mid
            else:
                hi = mid
        return celsius((lo + hi) / 2)
    mmhg = P_bar / MMHG_BAR
    for t_max, A, B, C in ANTOINE[liquid]:
        T = B / (A - log10(mmhg)) - C
        if T <= t_max + 1e-6:
            return T
    return T


# ---------------------------------------------------------------------------
# Chapter 9 — surface tension (scenes 25-26)
# ---------------------------------------------------------------------------

WATER_TC = 647.096           # K (IAPWS)
WATER_PC_BAR = 220.64        # bar (IAPWS: 22.064 MPa)


def water_saturation_pressure(T: float) -> float:
    """Water saturation pressure, bar, from IAPWS SR1-86(1992).

    https://iapws.org/public/documents/6dGkr/Supp-sat.pdf
    Used to the critical point; no Antoine extrapolation or piecewise jump.
    The film also draws 0 degC, a 0.01 K continuation below the triple point.
    """
    if not T_ICE <= T <= WATER_TC + 1e-9:
        raise ValueError("Water saturation curve requires 0 degC <= T <= T_c")
    tau = max(1.0 - T / WATER_TC, 0.0)
    powers = (1.0, 1.5, 3.0, 3.5, 4.0, 7.5)
    coefficients = (-7.85951783, 1.84408259, -11.7866497, 22.6807411, -15.9618719, 1.80122502)
    exponent = WATER_TC / T * sum(a * tau ** power for a, power in zip(coefficients, powers))
    return float(WATER_PC_BAR * np.exp(exponent))


def water_surface_tension(T: float) -> float:
    """IAPWS: surface tension of water in mN/m at T (K); zero at the critical point."""
    tau = 1 - T / WATER_TC
    if tau <= 0:
        return 0.0
    return 235.8 * tau ** 1.256 * (1 - 0.625 * tau)


SURFACE_TENSION_20C = {"water": water_surface_tension(293.15), "ethanol": 22.3, "mercury": 485.5}   # mN/m


def sphere_vs_cube_area() -> float:
    """Surface area of a sphere divided by that of a cube of equal volume: (36 pi)^(1/3) / 6."""
    return (36 * pi) ** (1 / 3) / 6


@lru_cache(maxsize=2)
def liquid_snapshot(seed: int = 25, nx: int = 7, ny: int = 4, nz: int = 5, spacing: float = 1.0) -> np.ndarray:
    """A disordered, densely packed slab of molecule centres (a schematic liquid).

    A jittered close-packed lattice relaxed so no two centres come closer than
    0.9 spacing. Returns (n, 3) points with the free surface at the top (max y)."""
    rng = np.random.default_rng(seed)
    pts = []
    for j in range(ny):
        for k in range(nz):
            for i in range(nx):
                x = i + (0.5 if (j + k) % 2 else 0.0)
                pts.append((x * spacing, j * spacing * 0.82, k * spacing * 0.87))
    pts = np.array(pts, dtype=float)
    pts += rng.normal(scale=0.09 * spacing, size=pts.shape)
    for _ in range(60):
        d = pts[:, None, :] - pts[None, :, :]
        dist = np.linalg.norm(d, axis=-1)
        np.fill_diagonal(dist, np.inf)
        close = dist < 0.9 * spacing
        if not close.any():
            break
        safe = np.where(close, dist, 1.0)
        push = np.where(close[:, :, None], d / safe[:, :, None] * (0.9 * spacing - safe)[:, :, None] * 0.5, 0.0)
        pts += push.sum(axis=1)
    return pts - pts.mean(axis=0)


def neighbour_counts(points: np.ndarray, cutoff: float = 1.35) -> np.ndarray:
    d = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
    np.fill_diagonal(d, np.inf)
    return (d < cutoff).sum(axis=1)


# ---------------------------------------------------------------------------
# Chapter 10 — viscosity (scenes 27-28)
# ---------------------------------------------------------------------------

WATER_VISCOSITY = (                       # (degC, mPa s), CRC Handbook
    (0, 1.792), (10, 1.306), (20, 1.002), (30, 0.797), (40, 0.653), (50, 0.547),
    (60, 0.466), (70, 0.404), (80, 0.354), (90, 0.314), (100, 0.282),
)
HONEY_VISCOSITY_PA_S = (2.0, 20.0)        # typical range at 20-25 degC, depending on water content


def water_viscosity(T_C: float) -> float:
    """Viscosity of liquid water (mPa s), interpolated in log space."""
    ts, etas = zip(*WATER_VISCOSITY)
    return float(np.exp(np.interp(T_C, ts, np.log(etas))))


def honey_to_water() -> tuple[float, float]:
    low, high = HONEY_VISCOSITY_PA_S
    water = water_viscosity(20.0) / 1000
    return low / water, high / water


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------


def verify() -> list[str]:
    failures: list[str] = []

    def near(value: float, target: float, tol: float, what: str) -> None:
        if abs(value - target) > tol:
            failures.append(f"{what}: {value:.6g} (expected {target:.6g} +/- {tol})")

    def check(ok: bool, what: str) -> None:
        if not ok:
            failures.append(what)

    near(R, 8.314462618, 1e-8, "R = N_A k_B")
    # Speeds of N2 at 300 K and the ratio
    near(SPEEDS.mp, 422, 1.0, "u_mp of N2 at 300 K")
    near(SPEEDS.av, 476, 1.0, "u_av of N2 at 300 K")
    near(SPEEDS.rms, 517, 1.0, "u_rms of N2 at 300 K")
    near(SPEED_RATIO[1], 1.128, 0.0005, "u_av / u_mp")
    near(SPEED_RATIO[2], 1.225, 0.0005, "u_rms / u_mp")
    near(SPEEDS.heat_factor, 1.414, 0.001, "300 -> 600 K: speeds x sqrt 2")
    near(SPEEDS.mass_ratio, 2.53, 0.01, "Cl2 / N2 molar mass")
    near(SPEEDS.grams_error, 31.6, 0.1, "grams instead of kilograms: sqrt(1000)")
    us = np.linspace(0, 4000, 40001)
    f = mb_pdf(us, 300, MOLAR_MASS["N2"])
    near(float(np.trapezoid(f, us)), 1.0, 1e-4, "MB density integrates to one")
    near(float(us[np.argmax(f)]), SPEEDS.mp, 0.2, "MB peak is u_mp")
    near(float(np.trapezoid(f * us, us)), SPEEDS.av, 0.2, "MB mean is u_av")
    near(float(np.sqrt(np.trapezoid(f * us * us, us))), SPEEDS.rms, 0.2, "MB rms is u_rms")
    g = mb_pdf(us, 600, MOLAR_MASS["N2"])
    check(g.max() < f.max(), "heating lowers the peak of the MB curve")
    near(float(np.trapezoid(g, us)), 1.0, 1e-4, "hot MB density integrates to one")
    check(1e9 < N2_COLLISIONS_PER_S < 1e10, f"N2 collisions per second are billions: {N2_COLLISIONS_PER_S:.2e}")
    # One collision: KE and momentum conserved, speeds become unequal
    (a0, b0), (a1, b1) = COLLISION.before, COLLISION.after
    near(float(a1 @ a1 + b1 @ b1), float(a0 @ a0 + b0 @ b0), 1e-12, "collision conserves kinetic energy")
    near(float(np.linalg.norm(a1 + b1 - a0 - b0)), 0.0, 1e-12, "collision conserves momentum")
    s1, s2 = COLLISION.speeds_after
    check(s1 > 1.2 and s2 < 0.75, f"after the collision one leaves faster, one slower: {s1:.2f}, {s2:.2f}")
    check(float(np.dot(a0 - b0, COLLISION.normal)) > 0, "the two molecules approach along the normal")
    # 2D hard disks: energy conserved, spike relaxes to the 2D equilibrium
    pos, vel, times = disk_movie()
    speeds0 = np.linalg.norm(vel[0], axis=1)
    speeds_end = np.linalg.norm(vel[-1], axis=1)
    near(float(speeds0.std()), 0.0, 1e-6, "disks start with one speed")
    near(float((speeds_end ** 2).mean()), DISK_SPEED ** 2, 1e-3, "disk gas conserves kinetic energy")
    check(rayleigh_distance(np.concatenate([np.linalg.norm(v, axis=1) for v in vel[-120:]])) < 0.05,
          "disk speeds relax to the 2D equilibrium distribution")
    half = np.linalg.norm(vel[len(vel) // 2], axis=1)
    check(abs(half.std() - speeds_end.std()) < 0.12, "the spread stops changing once relaxed")
    gap = np.linalg.norm(pos[-1][:, None, :] - pos[-1][None, :, :], axis=-1)
    np.fill_diagonal(gap, np.inf)
    check(float(gap.min()) > 1.8 * DISK_RADIUS, "disks never overlap")
    # Hard spheres press harder than points at the same density
    extent = np.array([2.6, 1.4, 2.0])
    spheres = HardSphereGas(70, 3, 0.15, extent)
    points = IdealGas(70, 3)
    hs = sum(len(spheres.advance(1 / 30, extent, 1.5)) for _ in range(900))
    ip = sum(len(points.advance(1 / 30, extent, 1.5)) for _ in range(900))
    eta = spheres.packing_fraction(extent)
    check(hs > 1.25 * ip, f"hard spheres strike the walls more often than points: {hs} vs {ip} (eta {eta:.2f})")
    gap3 = np.linalg.norm(spheres.pos[:, None] - spheres.pos[None], axis=-1)
    np.fill_diagonal(gap3, np.inf)
    check(float(gap3.min()) > 1.6 * spheres.radius, "hard spheres keep apart")
    # Air is nearly empty
    check(molecular_volume_fraction() < 1e-3, "molecules fill less than a thousandth of air")
    # Van der Waals flask
    near(FLASK.ideal, 24.94, 0.01, "ideal pressure, 1 mol CO2 in 1 L at 300 K")
    near(FLASK.size_only, 26.05, 0.01, "size correction alone")
    near(FLASK.attraction, 3.64, 1e-9, "attraction correction a n^2 / V^2")
    near(FLASK.vdw, 22.41, 0.01, "van der Waals pressure")
    near(FLASK.percent_below, 10.1, 0.1, "vdW below ideal, percent")
    near(FLASK.Z, 0.90, 0.005, "Z of the flask")
    check(FLASK.dilute_difference_percent < 0.2, "in 100 L the corrections almost vanish")
    near(VDW["CO2"][0] / VDW["He"][0], 105, 1.0, "a(CO2) / a(He)")
    check(VDW["NH3"][0] > VDW["CO2"][0], "ammonia attracts more strongly than CO2")
    dilute, dense, p1, p2 = pair_demo()
    check(3.8 <= p2 / p1 <= 4.3, f"doubling density multiplies nearby pairs ~4: {p1} -> {p2}")
    near(EXCLUSION_RATIO, (2.0 / 1.0) ** 3, 0, "forbidden sphere radius d: 8 molecular volumes")
    # Z curves at 300 K (vdW): methane dips, nitrogen dips a little, H2 and He rise
    Ps = np.linspace(1, 600, 300)
    z = {g: np.array([z_vdw(p, ROOM_T, g) for p in Ps]) for g in ("CH4", "N2", "H2", "He")}
    check(z["CH4"].min() < 0.9, f"methane dips below one: {z['CH4'].min():.2f}")
    check(0.9 < z["N2"].min() < 1.0, f"nitrogen dips a little: {z['N2'].min():.3f}")
    check(z["H2"].min() >= 0.999 and z["He"].min() >= 0.999, "hydrogen and helium rise from the start")
    check(all(z[g][-1] > 1 for g in z), "at very high pressure every Z exceeds one")
    # Boyle temperature of the van der Waals fluid: zero initial slope
    eps = 1e-4
    near((z_reduced(eps, VDW_BOYLE_REDUCED) - 1) / eps, 0.0, 1e-3, "flat start at the vdW Boyle temperature")
    check(z_reduced(0.5, 1.5) < 1 < z_reduced(0.5, 5.0), "below T_B Z dips, above it Z rises")
    check(BOYLE_T["He"] < ROOM_T < BOYLE_T["N2"] + 50, "helium is far above its Boyle temperature at room T")
    # Maxwell construction: equal areas, and the dome closes at the critical point
    for tr in (0.85, 0.94, 0.97):
        p, vl, vg = maxwell(tr)
        vs = np.linspace(vl, vg, 20001)
        near(float(np.trapezoid(vdw_reduced(vs, tr) - p, vs)), 0.0, 1e-6, f"equal areas at t_r = {tr}")
        check(vl < 1 < vg, f"coexisting volumes straddle v_c at t_r = {tr}")
    p97 = maxwell(0.97)
    p999 = maxwell(0.999)
    check(p999[2] - p999[1] < p97[2] - p97[1], "the flat stretch shrinks toward the critical point")
    near(float(vdw_reduced(1.0, 1.0)), 1.0, 1e-12, "critical point at (1, 1, 1)")
    near(vdw_critical_temperature("CO2"), 304, 1.0, "vdW T_c from CO2's a and b (they were fitted to it)")
    near(liquid_fraction(0.97, (p97[1] + p97[2]) / 2), 0.5, 1e-9, "lever rule halfway")
    # Critical constants
    near(celsius(CRITICAL["CO2"][0]), 31.0, 0.1, "CO2 T_c in degC")
    near(celsius(CRITICAL["N2"][0]), -147.15, 0.01, "N2 T_c in degC")
    check(CRITICAL["N2"][0] < ROOM_T < CRITICAL["CO2"][0] + 1 < CRITICAL["NH3"][0], "T_c order around room T")
    # Vapour pressure and boiling points
    near(boiling_point("water", ATM_BAR), 100.0, 0.05, "water boils at 100 degC at 1 atm")
    near(boiling_point("water", 1.0), 99.6, 0.05, "water boils at 99.6 degC at 1 bar")
    near(boiling_point("ethanol", ATM_BAR), 78.3, 0.3, "ethanol normal boiling point")
    near(boiling_point("ether", ATM_BAR), 34.6, 0.3, "diethyl ether normal boiling point")
    near(boiling_point("water", EVEREST_BAR), 72, 1.0, "water on Everest")
    near(boiling_point("water", COOKER_BAR), 120, 1.0, "water in a pressure cooker")
    near(vapour_pressure("water", 25.0), 0.0317, 0.0003, "aqueous tension at 25 degC (Part 1)")
    near(EVEREST_BAR / ATM_BAR, 1 / 3, 0.01, "Everest ~ a third of an atmosphere")
    check(vapour_pressure("ether", 20) > vapour_pressure("ethanol", 20) > vapour_pressure("water", 20),
          "volatility order ether > ethanol > water")
    # Surface tension
    near(water_surface_tension(293.15), 72.7, 0.1, "water surface tension at 20 degC")
    near(water_surface_tension(373.15), 58.9, 0.1, "water surface tension at 100 degC")
    near(water_surface_tension(WATER_TC), 0.0, 1e-12, "surface tension vanishes at T_c")
    near(celsius(WATER_TC), 374.0, 0.1, "water's critical temperature in degC")
    near(1 - sphere_vs_cube_area(), 0.194, 0.001, "sphere has ~a fifth less area than a cube")
    slab = liquid_snapshot()
    counts = neighbour_counts(slab)
    top = slab[:, 1] > slab[:, 1].max() - 0.3
    middle = np.abs(slab[:, 1] - np.median(slab[:, 1])) < 0.35
    check(counts[top].mean() < counts[middle].mean() - 2, "surface molecules have fewer neighbours")
    gap_l = np.linalg.norm(slab[:, None] - slab[None], axis=-1)
    np.fill_diagonal(gap_l, np.inf)
    check(float(gap_l.min()) > 0.85, "liquid snapshot keeps molecules apart")
    # Viscosity
    near(water_viscosity(20), 1.002, 1e-9, "water viscosity at 20 degC")
    near(water_viscosity(100) / water_viscosity(20), 0.281, 0.002, "water at 100 degC: less than a third")
    check(honey_to_water()[0] > 1000, "honey is thousands of times more viscous than water")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    pos, _, _ = disk_movie()
    print(f"Model check passed: speeds, collision, {pos.shape[1]}-disk relaxation ({len(pos)} frames), "
          "hard spheres, van der Waals + Maxwell, Z, critical data, vapour pressure, surface tension, viscosity.")
