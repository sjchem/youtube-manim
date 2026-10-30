"""The chemistry behind every number and every moving picture in the film.

Nothing in this module imports Manim, so it can be checked with plain
numbers: ``python -m utils.physics_models``.

* **The reference solution** (most chapters): 18.0 g glucose dissolved in
  180.0 g water, with a measured final volume of 191.0 mL. ``Solution``
  derives every concentration from those three measurements and two molar
  masses — molarity, molality, mole fraction, mass percent, % (w/v), mass
  concentration, density — so no scene ever types one of those numbers.
  Molar masses are the brief's rounded values (180 and 18 g/mol); the exact
  values (180.16 and 18.015 g/mol) move nothing at the precision shown.
* **Heating** (chapter 08): a sealed sample keeps its masses; its volume
  grows. The film assumes it expands like pure water between 20 and 70 °C
  (``concentration_data.WATER_DENSITY``), which takes 191.0 mL to 195 mL.
* **Molarity <-> molality** (chapters 09, 17): m = c / (rho - c M_s). The
  divergence plot uses a constant apparent molar volume for glucose,
  calibrated on the reference solution itself — a simple model, labelled so.
* **Normality** (chapters 10-11): N = M z, where z (equivalents per mole) is fixed by the
  stated reaction, never by the substance alone.
* **Dilution** (chapter 18): moles are conserved, so M1 V1 = M2 V2.
* **Glassware** (many chapters): a beaker, a volumetric flask and a
  graduated cylinder are solids of revolution. ``Profile`` integrates
  pi r(y)^2 so a liquid rises by *volume* — fast in a thin neck, slow in a
  wide bulb — exactly as in real glassware.
* **Molecules** (chapters 01, 02, 10-11): beta-D-glucopyranose is built as an
  ideal 4C1 chair with every OH and the CH2OH group equatorial; water and
  sulfuric acid from bond lengths and angles. Coordinates in angstrom.
* **Thermal motion** (every swarm): each particle drifts around a home
  position on smooth incommensurate sinusoids, a deterministic stand-in for
  Brownian motion (it looks right and renders identically every time).
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import acos, cos, pi, radians, sin, sqrt

import numpy as np

# ---------------------------------------------------------------------------
# Molar masses (g/mol) — the brief's rounded values
# ---------------------------------------------------------------------------

M_GLUCOSE = 180.0
M_WATER = 18.0
M_H2SO4 = 98.0
M_GLUCOSE_EXACT = 180.156
M_WATER_EXACT = 18.015

# ---------------------------------------------------------------------------
# The reference solution and everything derived from it
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Solution:
    """A binary solution described by three measurements."""

    solute_g: float
    solvent_g: float
    volume_mL: float
    solute_molar_mass: float = M_GLUCOSE
    solvent_molar_mass: float = M_WATER

    # --- amounts -------------------------------------------------------------
    @property
    def n_solute(self) -> float:
        return self.solute_g / self.solute_molar_mass

    @property
    def n_solvent(self) -> float:
        return self.solvent_g / self.solvent_molar_mass

    @property
    def n_total(self) -> float:
        return self.n_solute + self.n_solvent

    # --- masses and volume ---------------------------------------------------
    @property
    def solution_g(self) -> float:
        return self.solute_g + self.solvent_g

    @property
    def volume_L(self) -> float:
        return self.volume_mL / 1000.0

    @property
    def solvent_kg(self) -> float:
        return self.solvent_g / 1000.0

    @property
    def density_g_per_mL(self) -> float:
        return self.solution_g / self.volume_mL

    # --- the concentrations ----------------------------------------------------
    @property
    def molarity(self) -> float:
        """Amount concentration c: mol of solute per litre of solution."""
        return self.n_solute / self.volume_L

    @property
    def molality(self) -> float:
        """mol of solute per kg of solvent."""
        return self.n_solute / self.solvent_kg

    @property
    def x_solute(self) -> float:
        return self.n_solute / self.n_total

    @property
    def x_solvent(self) -> float:
        return self.n_solvent / self.n_total

    @property
    def mole_ratio(self) -> float:
        """Solute over solvent — the classic mistake in place of a mole fraction."""
        return self.n_solute / self.n_solvent

    @property
    def mass_percent(self) -> float:
        return 100.0 * self.solute_g / self.solution_g

    @property
    def wv_percent(self) -> float:
        """% (w/v): grams of solute per 100 mL of final solution."""
        return 100.0 * self.solute_g / self.volume_mL

    @property
    def mass_concentration(self) -> float:
        """gamma: grams of solute per litre of solution."""
        return self.solute_g / self.volume_L

    def at_volume(self, volume_mL: float) -> "Solution":
        """The same masses in a different volume (heating a sealed sample)."""
        return replace(self, volume_mL=volume_mL)


REFERENCE = Solution(solute_g=18.0, solvent_g=180.0, volume_mL=191.0)


def molality_from_molarity(c: float, density_kg_per_L: float, solute_kg_per_mol: float) -> float:
    """m = c / (rho - c M_s) for a binary solution (c in mol/L, rho in kg/L)."""
    return c / (density_kg_per_L - c * solute_kg_per_mol)


def litre_breakdown(solution: Solution = REFERENCE) -> dict[str, float]:
    """One litre of the solution: its total mass, the glucose in it, the water left over."""
    total = 1000.0 * solution.density_g_per_mL
    solute = solution.molarity * solution.solute_molar_mass
    return {"total_g": total, "solute_g": solute, "solvent_g": total - solute,
            "molality": solution.molarity / ((total - solute) / 1000.0)}


# ---------------------------------------------------------------------------
# Heating a sealed sample
# ---------------------------------------------------------------------------


def heated_volume(volume_mL: float, density_cold: float, density_hot: float) -> float:
    """Mass is conserved, so V_hot = V_cold * rho_cold / rho_hot."""
    return volume_mL * density_cold / density_hot


# ---------------------------------------------------------------------------
# Molarity vs molality as a solution gets stronger (illustrative model)
# ---------------------------------------------------------------------------


def apparent_molar_volume(solution: Solution = REFERENCE, water_density: float = 0.99821) -> float:
    """mL/mol of glucose implied by the reference solution's measured volume."""
    return (solution.volume_mL - solution.solvent_g / water_density) / solution.n_solute


def molarity_for_molality(m: np.ndarray | float, phi_v: float | None = None, water_density: float = 0.99821):
    """Molarity of a glucose solution of molality m, assuming a constant apparent molar volume."""
    phi_v = apparent_molar_volume() if phi_v is None else phi_v
    m = np.asarray(m, dtype=float)
    volume_L = (1000.0 / water_density + m * phi_v) / 1000.0
    return m / volume_L


# ---------------------------------------------------------------------------
# Colligative properties (dilute, ideal)
# ---------------------------------------------------------------------------


def freezing_point_drop(molality: float, kf: float) -> float:
    return kf * molality


def boiling_point_rise(molality: float, kb: float) -> float:
    return kb * molality


def vapour_pressure_fraction(x_solvent: float) -> float:
    """Raoult's law for an involatile solute: P / P_pure = x_solvent."""
    return x_solvent


# ---------------------------------------------------------------------------
# Normality and dilution
# ---------------------------------------------------------------------------

# Equivalents per mole of H2SO4 for each named reaction: the reaction decides.
REACTIONS: dict[str, dict] = {
    "partial": {"protons": 1, "base": 1,
                "tex": r"\mathrm{H_2SO_4 + NaOH \rightarrow NaHSO_4 + H_2O}"},
    "complete": {"protons": 2, "base": 2,
                 "tex": r"\mathrm{H_2SO_4 + 2\,NaOH \rightarrow Na_2SO_4 + 2\,H_2O}"},
}
ACID_MOLARITY = 0.500


def normality(molarity: float, equivalents_per_mole: int) -> float:
    """Reaction capacity per litre; z is equivalents per mole, not IUPAC f_eq."""
    return molarity * equivalents_per_mole


def dilute(m1: float, v1: float, v2: float) -> float:
    """M2 from M1 V1 = M2 V2 (any consistent volume unit)."""
    return m1 * v1 / v2


DILUTION = {"M1": 2.00, "V1_mL": 100.0, "V2_mL": 500.0}

# ---------------------------------------------------------------------------
# Glassware: solids of revolution
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Profile:
    """Inner radius r(y) of a piece of glassware, sampled from y = 0 (base) up.

    ``ys`` and ``rs`` are in screen units; ``mark_y`` is the calibration line
    (or the brim) and ``capacity`` the volume (mL) it stands for, so volumes
    convert to liquid heights with the real shape of the glass.
    """

    ys: tuple[float, ...]
    rs: tuple[float, ...]
    mark_y: float
    capacity: float

    @property
    def height(self) -> float:
        return self.ys[-1]

    def radius(self, y: float) -> float:
        return float(np.interp(y, self.ys, self.rs))

    def _cumulative(self) -> tuple[np.ndarray, np.ndarray]:
        y = np.linspace(0, self.height, 600)
        r = np.interp(y, self.ys, self.rs)
        area = pi * r * r
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (area[1:] + area[:-1]) * np.diff(y))])
        return y, cum

    def volume_below(self, y: float) -> float:
        """mL of liquid filling the glass up to height y."""
        ys, cum = self._cumulative()
        mark = float(np.interp(self.mark_y, ys, cum))
        return float(np.interp(y, ys, cum)) * self.capacity / mark

    def height_for(self, volume_mL: float) -> float:
        ys, cum = self._cumulative()
        mark = float(np.interp(self.mark_y, ys, cum))
        return float(np.interp(volume_mL * mark / self.capacity, cum, ys))


def beaker_profile(radius: float = 1.45, height: float = 3.3, brim_mL: float = 250.0) -> Profile:
    return Profile((0.0, height), (radius, radius), height, brim_mL)


def cylinder_profile(radius: float = 0.62, height: float = 4.6, mark_y: float = 4.2, mark_mL: float = 200.0) -> Profile:
    return Profile((0.0, height), (radius, radius), mark_y, mark_mL)


def flask_profile(bulb: float = 1.35, neck: float = 0.24, neck_top: float = 5.0, mark_y: float = 4.1,
                  capacity: float = 1000.0) -> Profile:
    """A volumetric flask: a round bulb (flattened base) and a long thin neck."""
    centre = bulb * 0.92
    ys, rs = [0.0], [bulb * 0.55]
    for y in np.linspace(0.05, centre + bulb, 40):
        r = sqrt(max(bulb * bulb - (y - centre) ** 2, 0.0))
        ys.append(float(y))
        rs.append(max(r, neck) if y > centre else max(r, bulb * 0.55))
    # Shoulder into the neck, then a straight neck.
    join = ys[-1]
    for y, r in ((join + 0.12, neck), (neck_top, neck)):
        ys.append(float(y))
        rs.append(float(r))
    clean_y, clean_r = [ys[0]], [rs[0]]
    for y, r in zip(ys[1:], rs[1:]):
        if y > clean_y[-1] + 1e-6:
            clean_y.append(y)
            clean_r.append(r)
        if r <= neck + 1e-9 and y > centre:
            clean_r[-1] = neck
    return Profile(tuple(clean_y), tuple(clean_r), mark_y, capacity)


# ---------------------------------------------------------------------------
# Molecules (angstrom)
# ---------------------------------------------------------------------------


def _unit(v) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


def _bent_from(direction, angle_deg: float, helper=(0.0, 1.0, 0.0)) -> np.ndarray:
    """A direction making ``angle_deg`` with ``direction`` (for X-O-H bends)."""
    d = _unit(direction)
    side = np.cross(d, helper)
    if np.linalg.norm(side) < 1e-6:
        side = np.cross(d, (1.0, 0.0, 0.0))
    side = _unit(side)
    a = radians(angle_deg)
    return _unit(cos(a) * d + sin(a) * side)


def _tetra_around(back, first_hint) -> list[np.ndarray]:
    """Three directions at 109.47 degrees from ``back``, 120 degrees apart."""
    b = _unit(back)
    u = _unit(np.cross(b, first_hint) if np.linalg.norm(np.cross(b, first_hint)) > 1e-6 else np.cross(b, (1, 0, 0)))
    v = np.cross(b, u)
    theta = acos(-1 / 3)
    return [_unit(cos(theta) * b + sin(theta) * (cos(phi) * u + sin(phi) * v))
            for phi in (0.0, 2 * pi / 3, 4 * pi / 3)]


@dataclass(frozen=True)
class Molecule:
    elements: tuple[str, ...]
    positions: np.ndarray            # (n, 3), angstrom, centred
    bonds: tuple[tuple[int, int, int], ...]   # (i, j, order)
    acidic: tuple[int, ...] = ()     # indices of acidic hydrogens

    def formula_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self.elements:
            counts[e] = counts.get(e, 0) + 1
        return counts


def _centred(points: list[np.ndarray]) -> np.ndarray:
    arr = np.array(points, dtype=float)
    return arr - arr.mean(axis=0)


def glucose() -> Molecule:
    """beta-D-glucopyranose: an ideal 4C1 chair, every substituent equatorial."""
    ring_names = ["O5", "C1", "C2", "C3", "C4", "C5"]
    r_ring, pucker = 1.44, 0.25
    ring = []
    for k in range(6):
        a = pi / 3 * k
        ring.append(np.array([r_ring * cos(a), pucker * (1 if k % 2 == 0 else -1), r_ring * sin(a)]))
    elements = ["O", "C", "C", "C", "C", "C"]
    points = list(ring)
    bonds = [(k, (k + 1) % 6, 1) for k in range(6)]

    def add(element: str, at: np.ndarray, parent: int) -> int:
        elements.append(element)
        points.append(at)
        bonds.append((parent, len(points) - 1, 1))
        return len(points) - 1

    def equatorial(k: int) -> np.ndarray:
        radial = _unit([ring[k][0], 0.0, ring[k][2]])
        axial_sign = 1 if k % 2 == 0 else -1
        return _unit(radial - 0.33 * axial_sign * np.array([0.0, 1.0, 0.0]))

    def axial(k: int) -> np.ndarray:
        return np.array([0.0, 1.0 if k % 2 == 0 else -1.0, 0.0])

    # Ring carbons C1..C4 carry an equatorial OH and an axial H.
    for k in (1, 2, 3, 4):
        o = add("O", ring[k] + 1.43 * equatorial(k), k)
        add("H", points[o] + 0.96 * _bent_from(equatorial(k), 71.0, helper=axial(k)), o)
        add("H", ring[k] + 1.09 * axial(k), k)
    # C5 carries an equatorial CH2OH and an axial H.
    c6 = add("C", ring[5] + 1.52 * equatorial(5), 5)
    add("H", ring[5] + 1.09 * axial(5), 5)
    d6 = _tetra_around(ring[5] - points[c6], (0.0, 1.0, 0.0))
    o6 = add("O", points[c6] + 1.43 * d6[0], c6)
    add("H", points[c6] + 1.09 * d6[1], c6)
    add("H", points[c6] + 1.09 * d6[2], c6)
    add("H", points[o6] + 0.96 * _bent_from(d6[0], 71.0), o6)
    return Molecule(tuple(elements), _centred(points), tuple(bonds))


def water() -> Molecule:
    half = radians(104.5 / 2)
    o = np.zeros(3)
    h1 = 0.96 * np.array([sin(half), -cos(half), 0.0])
    h2 = 0.96 * np.array([-sin(half), -cos(half), 0.0])
    return Molecule(("O", "H", "H"), _centred([o, h1, h2]), ((0, 1, 1), (0, 2, 1)))


def sulfuric_acid() -> Molecule:
    """H2SO4: tetrahedral S, two S=O (1.42 A), two S-OH (1.57 A), O-H 0.97 A."""
    tet = [_unit(v) for v in ((1, 1, 1), (-1, 1, -1), (1, -1, -1), (-1, -1, 1))]
    s = np.zeros(3)
    pts = [s, 1.42 * tet[0], 1.42 * tet[1], 1.57 * tet[2], 1.57 * tet[3]]
    h1 = pts[3] + 0.97 * _bent_from(tet[2], 72.0, helper=(0.0, 0.0, 1.0))
    h2 = pts[4] + 0.97 * _bent_from(tet[3], 72.0, helper=(0.0, 0.0, 1.0))
    pts += [h1, h2]
    return Molecule(("S", "O", "O", "O", "O", "H", "H"), _centred(pts),
                    ((0, 1, 2), (0, 2, 2), (0, 3, 1), (0, 4, 1), (3, 5, 1), (4, 6, 1)), acidic=(5, 6))


# ---------------------------------------------------------------------------
# Particle populations and thermal motion
# ---------------------------------------------------------------------------


def disc_cylinder_samples(count: int, rng: np.random.Generator, margin: float = 0.86) -> np.ndarray:
    """Normalised homes inside a cylinder: (u, v, w), u^2 + w^2 <= margin^2, v in [0, 1]."""
    out = np.zeros((count, 3))
    k = 0
    while k < count:
        u, w = rng.uniform(-1, 1, 2)
        if u * u + w * w <= 1:
            out[k] = (u * margin, rng.uniform(0.06, 0.94), w * margin)
            k += 1
    return out


def thermal_offsets(t: float, freqs: np.ndarray, phases: np.ndarray, amplitude: float) -> np.ndarray:
    """Smooth deterministic jiggle: three incommensurate sinusoids per particle."""
    return amplitude * np.sin(freqs * t + phases)


def expected_picks(x: float) -> float:
    """Mean number of random picks until the first hit (geometric distribution)."""
    return 1.0 / x


def seconds_to_days(seconds: float) -> float:
    return seconds / 86400.0


def seconds_to_years(seconds: float) -> float:
    return seconds / (365.25 * 86400.0)


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    s = REFERENCE
    check(abs(s.n_solute - 0.100) < 1e-12 and abs(s.n_solvent - 10.0) < 1e-12, "amounts 0.100 and 10.0 mol")
    check(f"{s.molarity:.3f}" == "0.524", "molarity 0.524 M")
    check(f"{s.molality:.3f}" == "0.556", "molality 0.556 mol/kg")
    check(f"{s.x_solute:.5f}" == "0.00990" and f"{s.x_solvent:.5f}" == "0.99010", "mole fractions")
    check(abs(s.x_solute + s.x_solvent - 1) < 1e-12, "mole fractions sum to one")
    check(f"{s.mass_percent:.2f}" == "9.09" and f"{s.wv_percent:.2f}" == "9.42", "percentages")
    check(f"{s.mass_concentration:.1f}" == "94.2" and f"{s.density_g_per_mL:.3f}" == "1.037", "gamma and density")
    m = molality_from_molarity(s.molarity, s.density_g_per_mL, s.solute_molar_mass / 1000)
    check(abs(m - s.molality) < 1e-9, "density formula recovers the molality exactly")
    box = litre_breakdown()
    check(abs(box["molality"] - s.molality) < 1e-9, "one-litre cube recovers the molality")
    check(abs(s.mass_concentration / s.solute_molar_mass - s.molarity) < 1e-12, "gamma / M = c")
    check(f"{s.at_volume(195.0).molarity:.3f}" == "0.513", "heated molarity 0.513 M")
    check(abs(molarity_for_molality(s.molality) - s.molarity) < 1e-9, "divergence model passes through the reference")
    check(normality(ACID_MOLARITY, 1) == 0.5 and normality(ACID_MOLARITY, 2) == 1.0, "normalities")
    check(abs(dilute(2.0, 100.0, 500.0) - 0.4) < 1e-12, "dilution 0.400 M")
    check(abs(expected_picks(s.x_solute) - 101.0) < 1e-9, "101 picks on average")
    for prof in (beaker_profile(), flask_profile(), cylinder_profile()):
        check(abs(prof.volume_below(prof.mark_y) - prof.capacity) < 1e-6, "mark holds the capacity")
        check(abs(prof.volume_below(prof.height_for(0.4 * prof.capacity)) - 0.4 * prof.capacity) < 0.5,
              "height_for inverts volume_below")
        check(all(b > a for a, b in zip(prof.ys, prof.ys[1:])), "profile heights increase")
    fp = flask_profile()
    check(fp.radius(fp.mark_y) < fp.radius(1.2) / 3, "flask neck much narrower than its bulb")
    g = glucose()
    check(g.formula_counts() == {"C": 6, "O": 6, "H": 12}, "glucose is C6H12O6")
    for i, j, _ in g.bonds:
        d = float(np.linalg.norm(g.positions[i] - g.positions[j]))
        check(0.9 < d < 1.6, f"glucose bond {i}-{j} length {d:.2f}")
    bonded = {(min(i, j), max(i, j)) for i, j, _ in g.bonds}
    for i in range(len(g.elements)):
        for j in range(i + 1, len(g.elements)):
            if (i, j) not in bonded:
                d = float(np.linalg.norm(g.positions[i] - g.positions[j]))
                check(d > 1.45, f"glucose atoms {i} and {j} clash ({d:.2f} A)")
    w = water()
    hoh = np.degrees(acos(np.dot(_unit(w.positions[1] - w.positions[0]), _unit(w.positions[2] - w.positions[0]))))
    check(abs(hoh - 104.5) < 1e-6, "water angle 104.5")
    a = sulfuric_acid()
    check(a.formula_counts() == {"S": 1, "O": 4, "H": 2} and len(a.acidic) == 2, "H2SO4 with two acidic H")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("Model check passed: reference solution, conversions, heating, normality, dilution, glassware, molecules.")
