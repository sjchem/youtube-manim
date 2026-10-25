"""The physics behind the film's moving pictures, computed rather than drawn.

Nothing in this module imports Manim: ``python -m utils.physics_models``.

* **Waves** (chapter 03): two sinusoids and their sum, for constructive and
  destructive interference.
* **H2+ in the LCAO approximation** (chapters 06-07): the textbook closed
  forms (atomic units, 1s orbitals with exponent 1) for the overlap S, the
  Coulomb integral j and the resonance integral k give the energies of the
  bonding and antibonding states relative to H + H+,

      E+-(R) = 1/R - (j +- k) / (1 +- S),
      S = e^-R (1 + R + R^2/3),  j = 1/R - e^-2R (1 + 1/R),  k = e^-R (1 + R).

  The bonding curve has a minimum near R = 2.49 bohr and 1.76 eV deep — a
  bond, though shallower than the exact 2.79 eV at 2.00 bohr (``mo_data``).
* **Huckel chains** (chapter 04): N equivalent orbitals in a row give exactly
  N combinations, with 0, 1, ..., N-1 nodes.
* **A liquid pour past a magnet** (chapters 01, 15, 17): droplets fall under
  gravity; a paramagnetic liquid also feels F = k grad(B^2) toward the strong
  field between the poles and is captured there, as liquid oxygen is in the
  classic demonstration. A diamagnetic liquid's push is far too weak to see,
  so it falls straight through. Distances and times are screen units, chosen
  for the picture, not scaled from a real magnet.
* **Spins in a field** (chapter 17): unpaired spins jitter about the field
  direction with a Langevin-like spread when the field is on and point every
  which way when it is off.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

import numpy as np

HARTREE_EV = 27.211386
BOHR_PM = 52.917721

# ---------------------------------------------------------------------------
# Waves
# ---------------------------------------------------------------------------


def wave(x, wavelength: float = 4.0, phase: float = 0.0, amplitude: float = 1.0):
    """A sinusoid; ``phase`` in units of a full cycle (0.5 = half a wavelength)."""
    return amplitude * np.sin(2 * np.pi * (np.asarray(x, dtype=float) / wavelength - phase))


def one_s_profile(x, centre: float, zeta: float = 1.0):
    """A 1s orbital along the line through its nucleus: e^{-zeta |x - c|}."""
    return np.exp(-zeta * np.abs(np.asarray(x, dtype=float) - centre))


# ---------------------------------------------------------------------------
# H2+ in the LCAO approximation (atomic units)
# ---------------------------------------------------------------------------


def overlap_1s(R):
    R = np.asarray(R, dtype=float)
    return np.exp(-R) * (1 + R + R * R / 3)


def coulomb_j(R):
    R = np.asarray(R, dtype=float)
    return 1 / R - np.exp(-2 * R) * (1 + 1 / R)


def resonance_k(R):
    R = np.asarray(R, dtype=float)
    return np.exp(-R) * (1 + R)


def h2plus_energies(R):
    """(bonding, antibonding) energies of H2+ relative to H + H+, in hartree."""
    R = np.asarray(R, dtype=float)
    S, j, k = overlap_1s(R), coulomb_j(R), resonance_k(R)
    return 1 / R - (j + k) / (1 + S), 1 / R - (j - k) / (1 - S)


def h2plus_minimum() -> tuple[float, float]:
    """(R in bohr, well depth in eV) of the LCAO bonding curve."""
    R = np.linspace(1.0, 5.0, 40001)
    plus, _ = h2plus_energies(R)
    i = int(np.argmin(plus))
    return float(R[i]), float(-plus[i] * HARTREE_EV)


# ---------------------------------------------------------------------------
# N orbitals in a row (Huckel)
# ---------------------------------------------------------------------------


def huckel_chain(n: int) -> tuple[np.ndarray, np.ndarray]:
    """Energies (in units of |beta|, lowest first) and coefficient columns for
    n equivalent orbitals in a row, each coupled to its neighbours."""
    H = np.zeros((n, n))
    for i in range(n - 1):
        H[i, i + 1] = H[i + 1, i] = -1.0
    energies, vectors = np.linalg.eigh(H)
    # Fix each column's overall sign so the first coefficient is positive.
    for j in range(n):
        if vectors[0, j] < 0:
            vectors[:, j] *= -1
    return energies, vectors


def sign_changes(values) -> int:
    signs = np.sign(np.asarray(values)[np.abs(values) > 1e-9])
    return int(np.sum(signs[1:] != signs[:-1]))


# ---------------------------------------------------------------------------
# A liquid poured past a magnet
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MagnetGeometry:
    """Screen-unit layout of the pole gap, relative to the magnet's centre."""

    gap_y: float = -0.35        # height of the field maximum
    sigma_x: float = 0.55       # how quickly B^2 falls off across the gap
    sigma_y: float = 0.5        # ... and along it
    nozzle_y: float = 2.2       # where the stream leaves the flask
    nozzle_x: float = -0.05
    floor_y: float = -3.1       # where an uncaptured droplet ends


def field_squared(x, y, geo: MagnetGeometry = MagnetGeometry()):
    """B^2 (peak 1) between the poles: a smooth bump centred in the gap."""
    return np.exp(-(np.asarray(x) / geo.sigma_x) ** 2 - ((np.asarray(y) - geo.gap_y) / geo.sigma_y) ** 2)


@dataclass
class Pour:
    """Precomputed droplet paths for one pour.

    ``paths[i]`` holds positions sampled every ``dt`` seconds from the
    droplet's birth at ``births[i]``; captured droplets end at their resting
    spot in the bridge and stay there (``captured[i]``).
    """

    births: np.ndarray
    paths: list[np.ndarray]
    captured: np.ndarray
    dt: float
    duration: float

    def positions(self, t: float) -> tuple[np.ndarray, np.ndarray]:
        """(N, 2) positions at time t, and a visibility per droplet (0 or 1)."""
        pts = np.zeros((len(self.paths), 2))
        seen = np.zeros(len(self.paths))
        for i, (born, path) in enumerate(zip(self.births, self.paths)):
            age = t - born
            if age < 0:
                continue
            k = min(int(age / self.dt), len(path) - 1)
            if k == len(path) - 1 and not self.captured[i]:
                continue   # fell to the floor and boiled away
            f = min(age / self.dt - k, 1.0) if k < len(path) - 1 else 0.0
            nxt = path[min(k + 1, len(path) - 1)]
            pts[i] = path[k] * (1 - f) + nxt * f
            seen[i] = 1.0
        return pts, seen

    def captured_by(self, t: float) -> int:
        """How many droplets have come to rest in the bridge by time t."""
        count = 0
        for born, path, caught in zip(self.births, self.paths, self.captured):
            if caught and t - born >= (len(path) - 1) * self.dt:
                count += 1
        return count


def bridge_spots(count: int, geo: MagnetGeometry, rng: np.random.Generator) -> np.ndarray:
    """Resting places filling the gap from the field maximum outward."""
    spots = []
    while len(spots) < count:
        x = rng.uniform(-0.62, 0.62)
        y = geo.gap_y + rng.uniform(-0.42, 0.42)
        spots.append((x, y, x * x / 0.62 ** 2 + ((y - geo.gap_y) / 0.42) ** 2))
    spots.sort(key=lambda s: s[2])
    return np.array([[x, y] for x, y, _ in spots])


def pour(paramagnetic: bool, *, drops: int = 70, duration: float = 6.0, seed: int = 0,
         geo: MagnetGeometry = MagnetGeometry(), strength: float = 40.0, dt: float = 1 / 60) -> Pour:
    """Simulate a stream of droplets falling past the pole gap.

    Gravity g pulls down; a paramagnetic droplet also feels
    F = strength * grad(B^2). Once inside the strong field (B^2 > 0.55) a
    droplet is captured and glides to the next free spot in the bridge.
    """
    rng = np.random.default_rng(seed)
    g = 9.0
    births = np.sort(rng.uniform(0.0, duration * 0.8, drops))
    spots = bridge_spots(drops, geo, rng)
    next_spot = 0
    paths, captured = [], []
    for born in births:
        p = np.array([geo.nozzle_x + rng.normal(0, 0.03), geo.nozzle_y])
        v = np.array([rng.normal(0, 0.05), -1.2 + rng.normal(0, 0.1)])
        path = [p.copy()]
        caught = False
        for _ in range(int(3.0 / dt)):
            a = np.array([0.0, -g])
            if paramagnetic:
                b2 = float(field_squared(p[0], p[1], geo))
                grad = -2 * b2 * np.array([p[0] / geo.sigma_x ** 2, (p[1] - geo.gap_y) / geo.sigma_y ** 2])
                a = a + strength * grad - 2.5 * v * b2   # drag inside the field: the liquid wets and slows
                if b2 > 0.55:
                    caught = True
                    target = spots[next_spot]
                    next_spot += 1
                    for s in np.linspace(0, 1, 18)[1:]:
                        e = s * s * (3 - 2 * s)
                        path.append(p * (1 - e) + target * e)
                    break
            v = v + a * dt
            p = p + v * dt
            path.append(p.copy())
            if p[1] < geo.floor_y:
                break
        paths.append(np.array(path))
        captured.append(caught)
    return Pour(births, paths, np.array(captured), dt, duration)


# ---------------------------------------------------------------------------
# Spins in a field
# ---------------------------------------------------------------------------


def spin_angles(count: int, field_on: bool, seed: int = 0, spread_deg: float = 22.0) -> np.ndarray:
    """Spin directions (radians from straight up): aligned with jitter in a
    field, uniformly random without one."""
    rng = np.random.default_rng(seed)
    if field_on:
        return np.radians(rng.normal(0.0, spread_deg, count))
    return rng.uniform(-np.pi, np.pi, count)


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    x = np.linspace(0, 8, 401)
    check(np.allclose(wave(x) + wave(x, phase=0.5), 0, atol=1e-12), "half-wave shift cancels")
    check(np.allclose(wave(x) + wave(x), 2 * wave(x)), "in-phase waves double")
    # LCAO H2+: overlap limits, a bound bonding state, a repulsive antibonding state.
    check(abs(float(overlap_1s(1e-9)) - 1) < 1e-6 and float(overlap_1s(30.0)) < 1e-9, "overlap limits")
    R0, depth = h2plus_minimum()
    check(abs(R0 - 2.49) < 0.01 and abs(depth - 1.76) < 0.01, f"LCAO minimum at {R0:.3f} bohr, {depth:.3f} eV")
    R = np.linspace(0.8, 8, 300)
    plus, minus = h2plus_energies(R)
    check(bool(np.all(minus > 0)), "antibonding curve never binds")
    check(bool(np.all(np.diff(minus) < 0)), "antibonding curve only climbs as the nuclei approach")
    i = int(np.argmin(plus))
    check(minus[i] > -plus[i], "at the bond length the antibonding rise exceeds the bonding drop")
    for n in (2, 3, 4, 6):
        energies, vectors = huckel_chain(n)
        check(len(energies) == n, f"{n} orbitals in, {n} out")
        check([sign_changes(vectors[:, j]) for j in range(n)] == list(range(n)), f"{n}-chain nodes 0..n-1")
        check(np.allclose(vectors.T @ vectors, np.eye(n)), f"{n}-chain combinations orthonormal")
    oxygen = pour(True, seed=1)
    nitrogen = pour(False, seed=1)
    check(oxygen.captured.mean() > 0.8, "a paramagnetic liquid is captured in the gap")
    check(not nitrogen.captured.any(), "a diamagnetic liquid falls through")
    check(oxygen.captured_by(oxygen.duration + 3) == int(oxygen.captured.sum()), "every captured drop comes to rest")
    on, off = spin_angles(400, True, 3), spin_angles(400, False, 3)
    check(np.mean(np.cos(on)) > 0.85 and abs(np.mean(np.cos(off))) < 0.1, "spins align only in a field")
    check(abs(exp(0) - 1) < 1e-12, "sanity")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Physics check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    R0, depth = h2plus_minimum()
    print(f"Physics check passed: interference, LCAO H2+ (minimum {R0:.2f} bohr, {depth:.2f} eV), "
          "Huckel chains, magnet pours, spins.")
