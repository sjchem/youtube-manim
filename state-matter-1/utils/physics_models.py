"""The physics the film draws: constants, worked examples and simulations.

Nothing here imports Manim. Every number a scene shows or the narrator says
is computed in this module (``python -m utils.physics_models`` re-checks the
worked examples and the simulations), and ``utils.gas_data`` confirms the
spoken words still match.

Sources
-------
* Exact SI constants: k_B = 1.380649e-23 J/K, N_A = 6.02214076e23 /mol
  (2019 SI redefinition, CODATA); R = N_A k_B = 8.314462618 J/(mol K).
* Gas laws, 22.71 L/mol at 273.15 K and 1 bar, aqueous tension 0.0317 bar at
  298 K: NCERT Chemistry Part I, Unit 5 (States of Matter), sections 5.1-5.6
  and Table 5.2.
* Boiling points of the noble gases, H2O and H2S: CRC Handbook of Chemistry
  and Physics (rounded to the kelvin).
* Lennard-Jones parameters for argon (epsilon / k_B ~ 120 K, sigma ~ 0.34 nm):
  standard textbook fit (Atkins' Physical Chemistry); used only as an order of
  magnitude, and said with "about".
* Dipole-dipole energy, Keesom and Debye averages, London 1/r^6: Atkins'
  Physical Chemistry, "Interactions between molecules".

Visual models
-------------
``IdealGas`` is the film's gas: point molecules with Maxwell-Boltzmann
velocities in a box whose walls reflect them elastically. Positions are folded
analytically from unbounded phases, so the motion is exact, deterministic and
cheap, and every wall hit is detected exactly. ``phase_movie`` is a real 2D
Lennard-Jones molecular-dynamics run (velocity Verlet with a velocity-rescaling
thermostat) that melts and then evaporates a crystal. ``tumbling_dipoles`` is a
Metropolis random walk of two dipoles, so the attractive average of the
Keesom interaction is measured, not asserted.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from functools import lru_cache
from math import exp, pi, sqrt
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
T_ICE = 273.15                # K at 0 degrees Celsius
G = 9.80665                   # m/s^2, standard gravity (for "tonnes per square metre")

# Molar masses, kg/mol
MOLAR_MASS: dict[str, float] = {
    "He": 4.0026e-3,
    "Ne": 20.180e-3,
    "Ar": 39.948e-3,
    "N2": 28.014e-3,
    "O2": 31.998e-3,
    "CO2": 44.009e-3,
    "H2O": 18.015e-3,
}


def celsius_to_kelvin(celsius: float) -> float:
    return celsius + T_ICE


def molecule_mass(molar_mass: float) -> float:
    """Mass of one molecule, kg."""
    return molar_mass / N_A


def mean_kinetic_energy(T: float) -> float:
    """<K> = 3/2 k_B T, per molecule (translational), J."""
    return 1.5 * K_B * T


def rms_speed(T: float, molar_mass: float) -> float:
    """sqrt(<v^2>) = sqrt(3 R T / M), m/s."""
    return sqrt(3 * R * T / molar_mass)


def number_density(P: float, T: float) -> float:
    """N / V = P / (k_B T), molecules per cubic metre."""
    return P / (K_B * T)


def wall_hit_rate(P: float, T: float, molar_mass: float) -> float:
    """Molecular impacts per square metre per second, P / sqrt(2 pi m k_B T)."""
    return P / sqrt(2 * pi * molecule_mass(molar_mass) * K_B * T)


def molar_volume(T: float, P: float) -> float:
    """V_m = R T / P, in litres per mole."""
    return R * T / P * 1000.0


def gas_density(P: float, molar_mass: float, T: float) -> float:
    """rho = P M / (R T), kg per cubic metre (= grams per litre)."""
    return P * molar_mass / (R * T)


# ---------------------------------------------------------------------------
# Worked examples (each one is spoken in the film)
# ---------------------------------------------------------------------------

ROOM_T = 300.0                                   # K, the film's "room temperature"


@dataclass(frozen=True)
class Air:
    """The hook: what one bar of air does."""

    pressure_bar: float = 1.0

    @property
    def tonnes_per_square_metre(self) -> float:
        return self.pressure_bar * BAR / G / 1000.0          # ~10.2 t

    @property
    def nitrogen_rms(self) -> float:
        return rms_speed(ROOM_T, MOLAR_MASS["N2"])           # ~517 m/s

    @property
    def impulse(self) -> float:
        """Momentum handed to the wall by one N2 molecule striking head-on at the rms speed."""
        return 2 * molecule_mass(MOLAR_MASS["N2"]) * self.nitrogen_rms   # ~4.8e-23 kg m/s

    @property
    def hits_per_cm2_per_s(self) -> float:
        return wall_hit_rate(self.pressure_bar * BAR, ROOM_T, MOLAR_MASS["N2"]) / 1e4   # ~2.9e23

    @property
    def molecules_per_cm3(self) -> float:
        return number_density(self.pressure_bar * BAR, ROOM_T) / 1e6                    # ~2.4e19


AIR = Air()


@dataclass(frozen=True)
class Boyle:
    """Isothermal compression of a fixed amount: P1 V1 = P2 V2."""

    V1: float = 4.0     # L
    P1: float = 1.0     # bar
    V2: float = 2.0     # L

    @property
    def P2(self) -> float:
        return self.P1 * self.V1 / self.V2


BOYLE = Boyle()


@dataclass(frozen=True)
class Charles:
    """Heating at constant pressure: V1 / T1 = V2 / T2."""

    T1: float = 300.0   # K
    V1: float = 2.0     # L
    T2: float = 450.0   # K

    @property
    def V2(self) -> float:
        return self.V1 * self.T2 / self.T1

    @property
    def kelvin_rise(self) -> float:
        return self.T2 / self.T1 - 1                         # +50 %

    @property
    def celsius_1(self) -> float:
        return self.T1 - T_ICE                               # 26.85, "about 27"

    @property
    def celsius_2(self) -> float:
        return self.T2 - T_ICE                               # 176.85, "about 177"


CHARLES = Charles()


@dataclass(frozen=True)
class CelsiusTrap:
    """A 50 % rise on the Celsius scale is not a 50 % rise in volume."""

    c1: float = 20.0    # degrees C
    c2: float = 30.0    # degrees C (+50 % in Celsius)
    V1: float = 2.0     # L

    @property
    def V2(self) -> float:
        return self.V1 * celsius_to_kelvin(self.c2) / celsius_to_kelvin(self.c1)

    @property
    def percent(self) -> float:
        return 100 * (self.V2 / self.V1 - 1)                 # ~3.4 %


CELSIUS_TRAP = CelsiusTrap()


@dataclass(frozen=True)
class GayLussac:
    """Heating a sealed rigid container: P1 / T1 = P2 / T2."""

    T1: float = 300.0   # K
    P1: float = 1.0     # bar
    T2: float = 360.0   # K

    @property
    def P2(self) -> float:
        return self.P1 * self.T2 / self.T1


GAY_LUSSAC = GayLussac()


@dataclass(frozen=True)
class Avogadro:
    """Molar volume of an ideal gas at 273.15 K."""

    @property
    def per_bar(self) -> float:
        return molar_volume(T_ICE, BAR)                      # 22.71 L

    @property
    def per_atm(self) -> float:
        return molar_volume(T_ICE, ATM)                      # 22.41 L

    @property
    def two_moles(self) -> float:
        return 2 * self.per_bar                              # 45.42 L


AVOGADRO = Avogadro()


@dataclass(frozen=True)
class Combined:
    """A weather balloon: P1 V1 / T1 = P2 V2 / T2."""

    P1: float = 1.0     # bar
    V1: float = 2.0     # L
    T1: float = 300.0   # K
    P2: float = 0.5     # bar
    T2: float = 250.0   # K

    @property
    def V2(self) -> float:
        return self.P1 * self.V1 / self.T1 * self.T2 / self.P2      # 3.33 L


COMBINED = Combined()


@dataclass(frozen=True)
class Density:
    """rho = P M / (R T) at 1 bar and 300 K: nitrogen against helium."""

    P: float = BAR
    T: float = ROOM_T

    @property
    def nitrogen(self) -> float:
        return gas_density(self.P, MOLAR_MASS["N2"], self.T)        # 1.12 g/L

    @property
    def helium(self) -> float:
        return gas_density(self.P, MOLAR_MASS["He"], self.T)        # 0.160 g/L

    @property
    def ratio(self) -> float:
        return self.nitrogen / self.helium                          # 7.0


DENSITY = Density()


@dataclass(frozen=True)
class Dalton:
    """2 mol N2 + 1 mol O2 sharing 3 bar."""

    n_a: float = 2.0
    n_b: float = 1.0
    P_total: float = 3.0

    @property
    def x_a(self) -> float:
        return self.n_a / (self.n_a + self.n_b)

    @property
    def x_b(self) -> float:
        return self.n_b / (self.n_a + self.n_b)

    @property
    def P_a(self) -> float:
        return self.x_a * self.P_total

    @property
    def P_b(self) -> float:
        return self.x_b * self.P_total


DALTON = Dalton()


@dataclass(frozen=True)
class OverWater:
    """A gas collected over water at 298 K: P_dry = P_total - aqueous tension."""

    P_total: float = 1.000       # bar
    aqueous_tension: float = 0.0317   # bar at 298 K, NCERT Table 5.2

    @property
    def P_dry(self) -> float:
        return self.P_total - self.aqueous_tension


OVER_WATER = OverWater()


@dataclass(frozen=True)
class IdealExample:
    """One mole at 300 K and 1 bar: V = nRT / P."""

    n: float = 1.0
    T: float = 300.0
    P: float = 1.0               # bar

    @property
    def V(self) -> float:
        return self.n * R_L_BAR * self.T / self.P                   # 24.94 L


IDEAL = IdealExample()


def cube_side_cm(litres: float) -> float:
    """Side of a cube holding ``litres`` (24.94 L -> a 29 cm cube)."""
    return (litres * 1000.0) ** (1 / 3)


def molar_mass_from_density(rho: float, P: float, T: float) -> float:
    """M = rho R T / P, in g/mol (rho in g/L = kg/m^3, P in Pa)."""
    return rho * R * T / P * 1000.0


# Thinner air. Summit of Everest ~33.7 kPa (West, J. Appl. Physiol. 1999);
# dry-air mole fractions N2 0.781, O2 0.209, Ar 0.0093 (US Standard Atmosphere).
SEA_LEVEL_BAR = ATM / BAR             # 1.013
EVEREST_BAR = 0.337
AIR_FRACTION: dict[str, float] = {"N2": 0.781, "O2": 0.209, "Ar": 0.0093}


@dataclass(frozen=True)
class Mountain:
    """Boyle at altitude: density follows pressure; Dalton gives the oxygen share."""

    @property
    def pressure_fraction(self) -> float:
        return EVEREST_BAR / SEA_LEVEL_BAR                          # ~1/3

    @property
    def oxygen_sea_level(self) -> float:
        return AIR_FRACTION["O2"] * SEA_LEVEL_BAR                    # 0.21 bar

    @property
    def oxygen_summit(self) -> float:
        return AIR_FRACTION["O2"] * EVEREST_BAR                      # 0.07 bar


MOUNTAIN = Mountain()

# Rapid compression of air (diatomic): P V^gamma = constant, gamma = 7/5.
GAMMA_AIR = 1.4


def adiabatic_pressure(V: float, P1: float = 1.0, V1: float = 1.0, gamma: float = GAMMA_AIR) -> float:
    return P1 * (V1 / V) ** gamma

# ---------------------------------------------------------------------------
# Intermolecular data (rounded; said with "about" where it is approximate)
# ---------------------------------------------------------------------------

NOBLE_BOILING_K: dict[str, float] = {"He": 4.2, "Ne": 27.1, "Ar": 87.3, "Kr": 119.9, "Xe": 165.1}
NOBLE_ELECTRONS: dict[str, int] = {"He": 2, "Ne": 10, "Ar": 18, "Kr": 36, "Xe": 54}
HYDRIDE_BOILING_C: dict[str, float] = {"H2O": 100.0, "H2S": -60.0}
OH_BOND_KJ = 463.0            # average O-H bond enthalpy in water
H_BOND_KJ = 20.0              # a typical hydrogen bond in water (range ~ 10-40)
ARGON_WELL_K = 120.0          # Lennard-Jones epsilon / k_B for argon
ARGON_SIGMA_NM = 0.34


def thermal_energy_per_mole(T: float) -> float:
    """R T in kJ/mol (the thermal-energy scale; 2.49 at 300 K)."""
    return R * T / 1000.0


def lennard_jones(r, epsilon: float = 1.0, sigma: float = 1.0):
    """U(r) = 4 eps [(sigma/r)^12 - (sigma/r)^6]."""
    r = np.asarray(r, dtype=float)
    s6 = (sigma / r) ** 6
    return 4 * epsilon * (s6 * s6 - s6)


LJ_MINIMUM = 2 ** (1 / 6)     # r_min / sigma = 1.122


def dispersion(r, c6: float = 1.0):
    """London attraction, -C6 / r^6."""
    return -c6 / np.asarray(r, dtype=float) ** 6


def dipole_energy(m1, m2, separation) -> float:
    """Energy of two point dipoles (reduced units: mu^2 / 4 pi eps0 = 1).

    U = [m1.m2 - 3 (m1.n)(m2.n)] / r^3, with n the unit vector between them.
    """
    d = np.asarray(separation, dtype=float)
    r = float(np.linalg.norm(d))
    n = d / r
    m1, m2 = np.asarray(m1, dtype=float), np.asarray(m2, dtype=float)
    return float((m1 @ m2 - 3 * (m1 @ n) * (m2 @ n)) / r ** 3)


DIPOLE_POSES: dict[str, tuple[tuple[float, float, float], tuple[float, float, float]]] = {
    # name: (m1, m2) for dipoles separated along +x
    "head_to_tail": ((1, 0, 0), (1, 0, 0)),          # -2 / r^3: strongest attraction
    "antiparallel": ((0, 1, 0), (0, -1, 0)),         # -1 / r^3
    "parallel": ((0, 1, 0), (0, 1, 0)),              # +1 / r^3
    "head_to_head": ((1, 0, 0), (-1, 0, 0)),         # +2 / r^3: repulsion
}


def keesom_average(r: float, kT: float, nodes: int = 48) -> tuple[float, float]:
    """Orientation averages of the dipole energy at separation r.

    Exact quadrature over both dipoles' directions (Gauss-Legendre in cos
    theta, uniform in the azimuth difference). Returns (plain average,
    Boltzmann-weighted average). The plain average of all orientations is
    zero; thermal weighting favours the attractive poses, leaving
    -2/3 / (kT r^6) to leading order (Keesom)."""
    c, w = np.polynomial.legendre.leggauss(nodes)
    phi = np.linspace(0, 2 * pi, 2 * nodes, endpoint=False)
    c1, c2, ph = np.meshgrid(c, c, phi, indexing="ij")
    weight = w[:, None, None] * w[None, :, None] * np.ones_like(ph)
    s1, s2 = np.sqrt(1 - c1 * c1), np.sqrt(1 - c2 * c2)
    U = (s1 * s2 * np.cos(ph) - 2 * c1 * c2) / r ** 3      # separation along each dipole's polar axis
    boltz = weight * np.exp(-U / kT)
    return float((U * weight).sum() / weight.sum()), float((U * boltz).sum() / boltz.sum())


@lru_cache(maxsize=4)
def tumbling_dipoles(frames: int = 900, r: float = 1.6, kT: float = 0.25, step: float = 0.22,
                     seed: int = 20261109) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """A Metropolis random walk of two dipoles on the sphere (smooth tumbling).

    Returns (m1 [frames, 3], m2 [frames, 3], U [frames]) for dipoles at
    separation r along x. Because moves are accepted with exp(-dU / kT), the
    walk spends more time in attractive poses and its running mean of U turns
    negative: the Keesom attraction, measured."""
    rng = np.random.default_rng(seed)
    sep = np.array([r, 0.0, 0.0])

    def rotate(v):
        w = v + rng.normal(scale=step, size=3)
        return w / np.linalg.norm(w)

    a, b = np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])
    u = dipole_energy(a, b, sep)
    out1, out2, energies = [], [], []
    for _ in range(frames):
        for _ in range(3):
            na, nb = rotate(a), rotate(b)
            nu = dipole_energy(na, nb, sep)
            if nu <= u or rng.random() < exp(-(nu - u) / kT):
                a, b, u = na, nb, nu
        out1.append(a.copy())
        out2.append(b.copy())
        energies.append(u)
    return np.array(out1), np.array(out2), np.array(energies)


# ---------------------------------------------------------------------------
# Maxwell-Boltzmann speeds
# ---------------------------------------------------------------------------


def maxwell_pdf(s, rms: float = 1.0):
    """Speed distribution with root-mean-square speed ``rms``."""
    sigma = rms / sqrt(3)
    s = np.asarray(s, dtype=float)
    return sqrt(2 / pi) * s * s / sigma ** 3 * np.exp(-s * s / (2 * sigma * sigma))


# ---------------------------------------------------------------------------
# The film's ideal gas (visual model)
# ---------------------------------------------------------------------------


def fold(phase):
    """Triangle wave: an unbounded phase folded into [0, 1] (period 2).

    A molecule whose phase grows steadily moves 0 -> 1 -> 0 -> 1: it bounces
    elastically between two walls, which is exactly what reflection does."""
    p = np.mod(phase, 2.0)
    return 1.0 - np.abs(p - 1.0)


class IdealGas:
    """Point molecules with Maxwell-Boltzmann velocities in a reflecting box.

    Velocities ``u`` are in units of the root-mean-square speed (so
    <|u|^2> = 1 for a large sample). A molecule's position along each axis is
    ``lo + extent * fold(phase)``; its phase grows at ``speed * u / extent``,
    so when the box shrinks it reaches the walls more often at the same speed
    (Boyle), and when ``heat`` grows it moves faster (temperature).

    ``species`` (0 or 1) lets two gases share the box (Dalton); heavier species
    move more slowly at the same temperature, by sqrt(m_ref / m).
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
        """Velocity of every molecule, in rms units at the reference temperature."""
        return self.u * (heat * self.slow)[:, None]

    def advance(self, dt: float, extent, speed: float, heat: float = 1.0) -> list[tuple[int, int, int]]:
        """Move every active molecule for ``dt`` seconds.

        ``extent`` is the box size along x, y, z (screen units) and ``speed``
        the rms speed in screen units per second. Returns the wall hits as
        (molecule, axis, side) with side 0 for the low wall, 1 for the high."""
        extent = np.asarray(extent, dtype=float)
        step = self.u * (speed * heat * self.slow)[:, None] * dt / extent[None, :]
        step[~self.active] = 0.0
        before = self.phase
        after = before + step
        self.phase = after
        lo, hi = np.floor(before), np.floor(after)
        hits = []
        crossed = np.argwhere(lo != hi)
        for i, axis in crossed:
            a, b = before[i, axis], after[i, axis]
            first, last = (int(np.floor(a)) + 1, int(np.floor(b))) if b > a else (int(np.floor(b)) + 1, int(np.floor(a)))
            for k in range(first, last + 1):
                hits.append((int(i), int(axis), 1 if k % 2 else 0))
        return hits

    def positions(self, lo, extent) -> np.ndarray:
        return np.asarray(lo, dtype=float)[None, :] + np.asarray(extent, dtype=float)[None, :] * fold(self.phase)

    def place(self, index: int, fraction, inward_axis: int = 0) -> None:
        """Put molecule ``index`` at a fractional point of the box (an inlet),
        heading into the box along ``inward_axis``."""
        f = np.clip(np.asarray(fraction, dtype=float), 0.0, 1.0)
        self.phase[index] = f                       # fold(f) = f on the first leg
        self.u[index, inward_axis] = abs(self.u[index, inward_axis])

    def mean_square(self, heat: float = 1.0) -> np.ndarray:
        """<v_x^2>, <v_y^2>, <v_z^2> over the active molecules (mass-weighted to species 0)."""
        v = self.velocities(heat)[self.active]
        weight = (self.masses[self.species[self.active]] / self.masses[0])[:, None]
        return (weight * v * v).mean(axis=0)


def pressure_ratio(n_ratio: float = 1.0, T_ratio: float = 1.0, V_ratio: float = 1.0) -> float:
    """P / P_ref for an ideal gas: (n / n_ref) (T / T_ref) / (V / V_ref)."""
    return n_ratio * T_ratio / V_ratio


def wall_force_trace(count: int, duration: float, bins: int, seed: int, *, length: float = 1.0) -> tuple[np.ndarray, float]:
    """Force on one wall from ``count`` molecules bouncing along x (1D, m = 1).

    Each hit hands the wall 2 |v_x|; molecule i returns every 2L / |v_x|.
    Returns (force per bin / long-run mean, mean) so the curve's spikiness can
    be compared across counts: it shrinks like 1 / sqrt(hits per bin)."""
    rng = np.random.default_rng(seed)
    vx = np.abs(rng.normal(scale=1 / sqrt(3), size=count))
    phase = rng.uniform(0, 2, size=count)          # fold coordinate; hits when phase crosses odd integers
    width = duration / bins
    force = np.zeros(bins)
    for v, p in zip(vx, phase):
        rate = v / length                          # phase units per second
        first = (1.0 - p) / rate if p < 1 else (3.0 - p) / rate
        times = np.arange(first, duration, 2.0 / rate)
        np.add.at(force, (times / width).astype(int).clip(0, bins - 1), 2 * v)
    force /= width
    mean = float(np.sum(vx * vx) / length)
    return force / mean, mean


def representative_seed(count: int, base: int, tolerance: float = 0.15) -> int:
    """The first seed from ``base`` whose |v_x| sample has <v_x^2> within ``tolerance``
    of the population value 1/3, so a small sample is typical rather than a fluke
    (a single molecule that barely moves would show no hits at all)."""
    seed = base
    while True:
        vx = np.random.default_rng(seed).normal(scale=1 / sqrt(3), size=count)
        if abs(float(np.mean(vx * vx)) * 3 - 1) <= tolerance:
            return seed
        seed += 1


def single_molecule_hits(vx: float, length: float, duration: float, start: float = 0.0) -> np.ndarray:
    """Times at which one molecule (fold phase ``start``) strikes the far wall."""
    rate = vx / length
    first = (1.0 - start) / rate if start < 1 else (3.0 - start) / rate
    return np.arange(first, duration, 2.0 / rate)


# ---------------------------------------------------------------------------
# 2D Lennard-Jones molecular dynamics: solid -> liquid -> gas
# ---------------------------------------------------------------------------

PHASE_BOX = (34.0, 19.0)           # sigma units (16:9)
PHASE_DT = 0.005
PHASE_EVERY = 8                    # store one frame every 8 steps (0.04 time units)
# (time, target temperature) in reduced units (k_B T / epsilon), piecewise linear.
# 2D Lennard-Jones: triple point ~0.41, critical point ~0.53 (Smit & Frenkel,
# 1991), so 0.10 is a crystal, 0.47 a liquid droplet and 1.6 a gas.
PHASE_SCHEDULE = ((0.0, 0.10), (10.0, 0.10), (13.0, 0.47), (36.0, 0.47), (40.0, 1.6), (70.0, 1.6))
PHASE_STATES = {"solid": 6.0, "liquid": 30.0, "gas": 64.0}   # times at which each state is well formed
CACHE_DIR = Path(__file__).resolve().parents[1] / "output" / ".cache"


def _hex_cluster(rings: int, spacing: float) -> np.ndarray:
    points = []
    for q in range(-rings, rings + 1):
        for r in range(max(-rings, -q - rings), min(rings, -q + rings) + 1):
            points.append((spacing * (q + r / 2), spacing * r * sqrt(3) / 2))
    return np.array(points)


def _lj_forces(pos: np.ndarray, cutoff: float = 3.0) -> np.ndarray:
    d = pos[:, None, :] - pos[None, :, :]
    r2 = (d * d).sum(-1)
    np.fill_diagonal(r2, np.inf)
    mask = r2 < cutoff * cutoff
    inv6 = np.where(mask, 1.0 / r2 ** 3, 0.0)
    coef = np.where(mask, 24 * (2 * inv6 * inv6 - inv6) / r2, 0.0)
    return (coef[:, :, None] * d).sum(axis=1)


def _schedule_temperature(t: float) -> float:
    times = [p[0] for p in PHASE_SCHEDULE]
    temps = [p[1] for p in PHASE_SCHEDULE]
    return float(np.interp(t, times, temps))


@lru_cache(maxsize=1)
def phase_movie(seed: int = 20261109) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run the melt-and-boil simulation once and cache it (in memory, and in
    output/.cache keyed by every parameter, so audits do not re-run it).

    Returns (positions [frames, N, 2] centred on the box, times [frames],
    kinetic temperatures [frames])."""
    key = hashlib.sha1(repr((seed, PHASE_BOX, PHASE_DT, PHASE_EVERY, PHASE_SCHEDULE, 2)).encode()).hexdigest()[:12]
    cached = CACHE_DIR / f"phase_movie_{key}.npz"
    if cached.is_file():
        data = np.load(cached)
        return data["frames"], data["times"], data["temps"]
    frames, times, temps = _run_phase_movie(seed)
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(cached, frames=frames, times=times, temps=temps)
    except OSError:
        pass   # a read-only checkout still works, only slower
    return frames, times, temps


def _run_phase_movie(seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    W, H = PHASE_BOX
    pos = _hex_cluster(4, LJ_MINIMUM) + np.array([W / 2, H / 2 - 1.2])
    n = len(pos)
    vel = rng.normal(scale=sqrt(0.1), size=(n, 2))
    vel -= vel.mean(axis=0)
    force = _lj_forces(pos)
    t_end = PHASE_SCHEDULE[-1][0]
    steps = int(round(t_end / PHASE_DT))
    frames, times, temps = [], [], []
    for step in range(steps + 1):
        t = step * PHASE_DT
        if step % PHASE_EVERY == 0:
            frames.append(pos - np.array([W / 2, H / 2]))
            times.append(t)
            temps.append(float((vel * vel).sum() / (2 * n)))
        vel += 0.5 * PHASE_DT * force
        pos = pos + PHASE_DT * vel
        for axis, size in ((0, W), (1, H)):           # elastic walls
            low, high = pos[:, axis] < 0.5, pos[:, axis] > size - 0.5
            pos[low, axis] = 1.0 - pos[low, axis]
            pos[high, axis] = 2 * (size - 0.5) - pos[high, axis]
            vel[low | high, axis] *= -1
        force = _lj_forces(pos)
        vel += 0.5 * PHASE_DT * force
        current = (vel * vel).sum() / (2 * n)
        target = _schedule_temperature(t)
        vel *= sqrt(1 + 0.02 * (target / max(current, 1e-9) - 1))   # gentle velocity rescaling
    return np.array(frames), np.array(times), np.array(temps)


def nearest_neighbour_spread(frame: np.ndarray) -> float:
    """Mean distance to the nearest neighbour (sigma units): ~1.1 when condensed."""
    d = np.linalg.norm(frame[:, None, :] - frame[None, :, :], axis=-1)
    np.fill_diagonal(d, np.inf)
    return float(d.min(axis=1).mean())


def internal_motion(frames: np.ndarray, times: np.ndarray, t: float, window: float = 4.0) -> float:
    """Mean displacement over ``window`` with the drift of the whole cluster removed
    (sigma units): an atom in a crystal only vibrates; in a liquid it wanders."""
    i, j = int(np.argmin(np.abs(times - t))), int(np.argmin(np.abs(times - (t - window))))
    a, b = frames[i] - frames[i].mean(axis=0), frames[j] - frames[j].mean(axis=0)
    return float(np.linalg.norm(a - b, axis=1).mean())


def area_fraction_spread(frame: np.ndarray) -> float:
    """Radius of gyration (sigma units): small for a droplet, large for a gas."""
    return float(np.sqrt(((frame - frame.mean(axis=0)) ** 2).sum(axis=1).mean()))


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------


def verify() -> list[str]:
    failures: list[str] = []

    def near(value: float, target: float, tol: float, what: str) -> None:
        if abs(value - target) > tol:
            failures.append(f"{what}: {value:.6g} (expected {target:.6g} +/- {tol})")

    near(R, 8.314462618, 1e-8, "R = N_A k_B")
    near(AIR.tonnes_per_square_metre, 10.2, 0.05, "1 bar as tonnes per m^2")
    near(AIR.nitrogen_rms, 517, 1.0, "N2 rms speed at 300 K")
    near(AIR.impulse * 1e23, 4.8, 0.05, "head-on impulse of one N2 molecule (1e-23 kg m/s)")
    near(AIR.hits_per_cm2_per_s / 1e23, 2.9, 0.05, "wall hits per cm^2 per s (1e23)")
    near(AIR.molecules_per_cm3 / 1e19, 2.4, 0.05, "molecules per cm^3 at 1 bar, 300 K (1e19)")
    near(mean_kinetic_energy(ROOM_T) * 1e21, 6.21, 0.01, "<K> at 300 K (1e-21 J)")
    near(thermal_energy_per_mole(ROOM_T), 2.49, 0.01, "RT at 300 K (kJ/mol)")
    near(BOYLE.P2, 2.0, 1e-12, "Boyle")
    near(CHARLES.V2, 3.0, 1e-12, "Charles")
    near(CHARLES.kelvin_rise, 0.5, 1e-12, "Charles: +50 % kelvin")
    near(CELSIUS_TRAP.percent, 3.41, 0.01, "50 % more Celsius: volume rise in %")
    near(GAY_LUSSAC.P2, 1.2, 1e-12, "Gay-Lussac")
    near(AVOGADRO.per_bar, 22.71, 0.005, "molar volume at 1 bar")
    near(AVOGADRO.per_atm, 22.41, 0.005, "molar volume at 1 atm")
    near(COMBINED.V2, 10 / 3, 1e-9, "combined gas law")
    near(DENSITY.nitrogen, 1.12, 0.005, "density of N2")
    near(DENSITY.helium, 0.160, 0.001, "density of He")
    near(DENSITY.ratio, 7.0, 0.01, "N2 / He density ratio")
    near(DALTON.P_a, 2.0, 1e-12, "Dalton N2")
    near(DALTON.P_b, 1.0, 1e-12, "Dalton O2")
    near(OVER_WATER.P_dry, 0.968, 0.0005, "dry gas over water")
    near(IDEAL.V, 24.94, 0.005, "one mole at 300 K, 1 bar")
    near(cube_side_cm(IDEAL.V), 29.2, 0.05, "a mole at 300 K, 1 bar fills a 29 cm cube")
    near(molar_mass_from_density(DENSITY.nitrogen, BAR, ROOM_T), 28.0, 0.05, "M = rho R T / P")
    near(MOUNTAIN.pressure_fraction, 1 / 3, 0.01, "Everest summit ~ a third of sea-level pressure")
    near(MOUNTAIN.oxygen_sea_level, 0.21, 0.005, "O2 partial pressure at sea level")
    near(MOUNTAIN.oxygen_summit, 0.07, 0.005, "O2 partial pressure on Everest")
    near(adiabatic_pressure(0.5), 2 ** 1.4, 1e-12, "rapid compression to half: 2^1.4")
    near(AIR.molecules_per_cm3 * 1000 / 1e22, 2.4, 0.05, "molecules per litre (1e22)")
    near(LJ_MINIMUM, 1.122, 0.001, "LJ minimum")
    near(float(lennard_jones(LJ_MINIMUM)), -1.0, 1e-12, "LJ well depth")
    near(float(lennard_jones(1.0)), 0.0, 1e-12, "LJ zero at sigma")
    near(R * ARGON_WELL_K / 1000, 1.0, 0.01, "argon's well ~ 1 kJ/mol")
    # Dipole poses
    sep = np.array([1.0, 0.0, 0.0])
    for name, expected in (("head_to_tail", -2), ("antiparallel", -1), ("parallel", 1), ("head_to_head", 2)):
        m1, m2 = DIPOLE_POSES[name]
        near(dipole_energy(m1, m2, sep), expected, 1e-12, f"dipole pose {name}")
    near(dipole_energy((1, 0, 0), (1, 0, 0), 2 * sep) / dipole_energy((1, 0, 0), (1, 0, 0), sep), 1 / 8, 1e-12,
         "fixed dipoles fall as 1/r^3")
    plain, thermal = keesom_average(3.0, 1.0)
    near(plain, 0.0, 2e-4, "all orientations average to zero")
    near(thermal / (-2 / 3 / 3.0 ** 6), 1.0, 0.08, "Keesom: -2/3 / (kT r^6)")
    plain6, thermal6 = keesom_average(6.0, 1.0)
    near(thermal / thermal6, 2 ** 6, 2 ** 6 * 0.2, "Keesom average falls as 1/r^6")
    _, _, U = tumbling_dipoles()
    if not U.mean() < -0.05:
        failures.append(f"tumbling dipoles should average negative, got {U.mean():.3f}")
    # Ideal gas visual model: equipartition and exact wall hits
    gas = IdealGas(4000, 3)
    ms = gas.mean_square()
    near(float(ms.sum()), 1.0, 0.05, "rms speed of the sample")
    near(float(ms[0] / ms.sum()), 1 / 3, 0.02, "<v_x^2> = <v^2> / 3")
    one = IdealGas(1, 5)
    one.phase[:] = 0.25
    one.u[:] = [[0.5, 0.0, 0.0]]
    hits = []
    for _ in range(400):
        hits += one.advance(0.01, (1.0, 1.0, 1.0), 1.0)
    near(len(hits), 2, 0, "one molecule at 0.5 box/s hits twice in 4 s from a quarter")
    times = single_molecule_hits(0.5, 1.0, 20.0)
    near(float(np.diff(times).mean()), 4.0, 1e-9, "round trip 2L / v_x")
    trace, _ = wall_force_trace(2000, 40.0, 40, 11)
    near(float(trace.mean()), 1.0, 0.03, "many molecules: mean force N m <v_x^2> / L")
    few, _ = wall_force_trace(5, 40.0, 40, 11)
    if not few.std() > 4 * trace.std():
        failures.append("five molecules should give a far spikier force than two thousand")
    # The melt-and-boil run reaches three distinct states.
    frames, times, temps = phase_movie()
    def frame_at(t):
        return frames[int(np.argmin(np.abs(times - t)))]
    solid, liquid, gas_f = (frame_at(PHASE_STATES[k]) for k in ("solid", "liquid", "gas"))
    if not nearest_neighbour_spread(solid) < 1.2:
        failures.append(f"solid should stay packed: nn {nearest_neighbour_spread(solid):.2f}")
    if not area_fraction_spread(liquid) < 6.5:
        failures.append(f"liquid should stay a droplet: Rg {area_fraction_spread(liquid):.2f}")
    solid_flow, liquid_flow = (internal_motion(frames, times, PHASE_STATES[k]) for k in ("solid", "liquid"))
    if not liquid_flow > 3 * solid_flow:
        failures.append(f"the liquid should flow, the solid only vibrate: {liquid_flow:.2f} vs {solid_flow:.2f}")
    if not area_fraction_spread(gas_f) > 7.0:
        failures.append(f"gas should fill the box: Rg {area_fraction_spread(gas_f):.2f}")
    if not area_fraction_spread(gas_f) > area_fraction_spread(liquid) + 1.5:
        failures.append("gas should spread far wider than the liquid")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    frames, times, temps = phase_movie()
    print(f"Model check passed: constants, 12 worked examples, dipoles (Keesom measured), ideal-gas hits, "
          f"force traces, melt-and-boil MD ({len(frames)} frames, {frames.shape[1]} atoms).")
