"""The bonding physics the film's pictures are computed from.

Nothing in this module imports Manim, so every model can be checked with
plain numbers: ``python -m utils.bond_models``.

* **The energy curve** is a Morse potential, E(r) = D[(1 - e^{-a(r - r_e)})^2 - 1],
  built on H2's measured bond length and bond enthalpy. Algebraically it is
  the sum of a short-range push, D e^{-2a(r-r_e)}, and a longer-range pull,
  -2D e^{-a(r-r_e)}; chapter 04 draws those two terms. It is an empirical
  model of the total energy, not a derivation of it.
* **Ionic attraction** is Coulomb's law between point charges, and the
  crystal's collective attraction is the rock-salt Madelung constant, summed
  here with Evjen's neutral-cube method rather than typed in.
* **Orbital pictures** are isosurfaces of simple LCAO densities: hydrogen-like
  s and p functions on each nucleus, added with their overlap normalisation.
  At large separation the bonding density approaches the two separate
  atomic densities, so one surface morphs continuously from "two atoms" to
  "one bond". These are illustrations of overlap, not solutions of the
  Schrödinger equation for a real molecule.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt

import numpy as np

# e^2 N_A / (4 pi eps0), in kJ mol^-1 pm: two unit charges 1 pm apart.
COULOMB_KJ_PM = 138_935.5


# ---------------------------------------------------------------------------
# The energy of two atoms versus their separation
# ---------------------------------------------------------------------------


def morse(r, depth: float, r_e: float, a: float):
    """Total energy (same unit as ``depth``) at separation ``r`` (same unit as ``r_e``)."""
    x = np.asarray(r, dtype=float) - r_e
    return depth * ((1 - np.exp(-a * x)) ** 2 - 1)


def morse_terms(r, depth: float, r_e: float, a: float):
    """The two terms whose sum is the Morse curve: (push, pull)."""
    x = np.asarray(r, dtype=float) - r_e
    return depth * np.exp(-2 * a * x), -2 * depth * np.exp(-a * x)


def morse_minimum(depth: float, r_e: float, a: float) -> float:
    """Numerically locate the minimum (a self-check: it must sit at r_e)."""
    rs = np.linspace(r_e * 0.3, r_e * 4, 40_001)
    return float(rs[np.argmin(morse(rs, depth, r_e, a))])


def morse_inverse(energy: float, depth: float, r_e: float, a: float, inner: bool = True) -> float:
    """Separation at which the curve reaches ``energy`` on the inner wall (or outer slope)."""
    # D[(1-u)^2 - 1] = E  ->  u = 1 -/+ sqrt(1 + E/D),  u = e^{-a x}
    root = sqrt(max(1 + energy / depth, 0.0))
    u = 1 + root if inner else 1 - root
    if u <= 0:
        return float("inf")
    return r_e - np.log(u) / a


def vibration(t: float, amplitude: float, period: float = 1.4) -> float:
    """A gentle oscillation about the minimum, for the 'spring' picture."""
    return amplitude * np.sin(2 * np.pi * t / period)


# ---------------------------------------------------------------------------
# Charges and crystals
# ---------------------------------------------------------------------------


def coulomb_kj(q1: float, q2: float, distance_pm: float) -> float:
    """Coulomb energy of two point charges (in units of e), kJ/mol. Negative = attraction."""
    return COULOMB_KJ_PM * q1 * q2 / distance_pm


@lru_cache(maxsize=None)
def madelung_rock_salt(n: int = 8) -> float:
    """Rock-salt Madelung constant by Evjen's method (charge-neutral cubes).

    Sites on a cube face carry weight 1/2, on an edge 1/4, at a corner 1/8, so
    every partial sum is over a neutral block and the series converges fast.
    Positive result = net attraction on the central ion.
    """
    total = 0.0
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                if i == j == k == 0:
                    continue
                weight = 1.0
                for c in (i, j, k):
                    if abs(c) == n:
                        weight *= 0.5
                sign = -1.0 if (i + j + k) % 2 == 0 else 1.0   # like charges repel (negative)
                total += weight * sign / sqrt(i * i + j * j + k * k)
    return total


def rock_salt_sites(n: int = 1) -> tuple[np.ndarray, list[str]]:
    """Lattice sites of a (2n+1)^3 rock-salt block; even parity = cation."""
    sites, kinds = [], []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                sites.append((i, j, k))
                kinds.append("+" if (i + j + k) % 2 == 0 else "-")
    return np.array(sites, dtype=float), kinds


def fcc_sites(n: int = 1) -> np.ndarray:
    """Face-centred cubic sites (copper's lattice) in a block, in units of the cube edge."""
    base = np.array([[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]])
    points = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                for b in base:
                    points.append(b + (i, j, k))
    return np.unique(np.round(np.array(points), 6), axis=0)


def neighbour_shells(sites: np.ndarray, kinds: list[str] | None = None, centre: int | None = None,
                     shells: int = 3) -> list[tuple[float, int, bool]]:
    """(distance, how many, same kind as the centre?) for the nearest ``shells`` shells."""
    if centre is None:
        centre = int(np.argmin(np.linalg.norm(sites, axis=1)))
    d = np.linalg.norm(sites - sites[centre], axis=1)
    found: list[tuple[float, int, bool]] = []
    for value in np.unique(np.round(d[d > 1e-9], 6))[:shells]:
        members = np.where(np.abs(d - value) < 1e-6)[0]
        same = kinds is not None and all(kinds[m] == kinds[centre] for m in members)
        found.append((float(value), len(members), bool(same)))
    return found


# ---------------------------------------------------------------------------
# Orbitals: hydrogen-like s and p functions and LCAO isosurfaces
# ---------------------------------------------------------------------------

ZETA_S = 1.0     # 1s exponent (Bohr-radius units)
ZETA_P = 0.85    # p exponent: a soft, readable lobe
S_BOND = 1.4     # H2 bond length in Bohr radii (74 pm)
P_BOND = 5.5     # display p-p bond distance: zeta_p * R ~ 4.7, like carbon 2p at a C-C bond


def s_function(x, y, z, centre: float):
    return np.exp(-ZETA_S * np.sqrt((x - centre) ** 2 + y ** 2 + z ** 2))


def p_function(x, y, z, centre: float, axis: str, sign: float = 1.0):
    """A p orbital on a nucleus at (centre, 0, 0), pointing along ``axis``."""
    dx = x - centre
    r = np.sqrt(dx ** 2 + y ** 2 + z ** 2)
    lever = {"x": dx, "y": y, "z": z}[axis]
    return sign * lever * np.exp(-ZETA_P * r)


def s_overlap(separation: float) -> float:
    """Closed-form overlap of two 1s functions (zeta = 1)."""
    R = ZETA_S * separation
    return float(np.exp(-R) * (1 + R + R * R / 3))


@lru_cache(maxsize=512)
def p_overlap(separation: float, kind: str) -> float:
    """Overlap of two normalised p functions: 'sigma' (head-on) or 'pi' (side by side).

    Head-on, the facing lobes are given the same sign so the overlap is
    positive (the bonding combination). Integrated in cylindrical coordinates.
    """
    half = separation / 2
    xs = np.linspace(-half - 14, half + 14, 900)
    rs = np.linspace(0, 14, 450)
    X, P = np.meshgrid(xs, rs, indexing="ij")
    ra = np.sqrt((X + half) ** 2 + P ** 2)
    rb = np.sqrt((X - half) ** 2 + P ** 2)
    ga, gb = np.exp(-ZETA_P * ra), np.exp(-ZETA_P * rb)
    if kind == "sigma":
        fa, fb = (X + half) * ga, -(X - half) * gb
        cross = np.trapezoid(np.trapezoid(fa * fb * P, rs, axis=1), xs)
        self_ = np.trapezoid(np.trapezoid(fa * fa * P, rs, axis=1), xs)
    else:
        cross = np.trapezoid(np.trapezoid(P ** 3 * ga * gb, rs, axis=1), xs)
        self_ = np.trapezoid(np.trapezoid(P ** 3 * ga * ga, rs, axis=1), xs)
    return float(cross / self_)


def _bisect_radius(field, lo, hi, c, iterations: int = 26):
    """Vectorised bisection: largest radius where field(radius) >= c (field decreasing)."""
    lo, hi = np.array(lo, dtype=float), np.array(hi, dtype=float)
    for _ in range(iterations):
        mid = (lo + hi) / 2
        inside = field(mid) >= c
        lo = np.where(inside, mid, lo)
        hi = np.where(inside, hi, mid)
    return lo


def revolution_profile(amplitude, x_values: np.ndarray, c: float, rho_max: float = 8.0) -> np.ndarray:
    """Radius rho(x) of the isosurface |amplitude(x, rho)| = c, symmetric about the x axis.

    ``amplitude(x, rho)`` must fall off with rho at fixed x. Where the axis
    itself is below the contour, the radius is zero (the surface is absent).
    """
    xs = np.asarray(x_values, dtype=float)
    on_axis = np.abs(amplitude(xs, np.zeros_like(xs)))
    radius = _bisect_radius(lambda rho: np.abs(amplitude(xs, rho)), np.zeros_like(xs),
                            np.full_like(xs, rho_max), c)
    return np.where(on_axis >= c, radius, 0.0)


def sigma_s_amplitude(separation: float):
    """sqrt(density) of two electrons in the 1s + 1s bonding combination."""
    half, norm = separation / 2, 1 / sqrt(1 + s_overlap(separation))

    def amplitude(x, rho):
        return norm * (s_function(x, rho, 0, -half) + s_function(x, rho, 0, half))

    return amplitude


def sigma_p_amplitude(separation: float):
    """Head-on p + p bonding combination; the facing lobes share a sign."""
    half, norm = separation / 2, 1 / sqrt(1 + p_overlap(round(separation, 3), "sigma"))

    def amplitude(x, rho):
        return norm * (p_function(x, rho, 0, -half, "x") + p_function(x, rho, 0, half, "x", -1.0))

    return amplitude


def single_p_amplitude(x, rho):
    """One p orbital at the origin along x (a two-lobed surface of revolution)."""
    return p_function(x, rho, 0, 0.0, "x")


def revolution_grid(profile: np.ndarray, xs: np.ndarray, segments: int) -> np.ndarray:
    """Points of a surface of revolution about x: shape (len(xs), segments + 1, 3)."""
    angles = np.linspace(0, 2 * np.pi, segments + 1)
    grid = np.zeros((len(xs), len(angles), 3))
    grid[:, :, 0] = xs[:, None]
    grid[:, :, 1] = profile[:, None] * np.cos(angles)[None, :]
    grid[:, :, 2] = profile[:, None] * np.sin(angles)[None, :]
    return grid


def pi_lobe_grid(separation: float, c: float, xs: np.ndarray, segments: int, upper: bool = True,
                 bonded: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """One lobe (upper or lower) of the side-by-side p + p combination.

    The p orbitals point along z. For each x, the lobe's cross-section is
    traced around the point where the amplitude peaks above (or below) the
    axis. Returns (points of shape (len(xs), segments + 1, 3), alive per x).
    """
    half = separation / 2
    norm = 1 / sqrt(1 + p_overlap(round(separation, 3), "pi")) if bonded else 1.0
    side = 1.0 if upper else -1.0

    def amplitude(x, y, z):
        return side * norm * (p_function(x, y, z, -half, "z") + p_function(x, y, z, half, "z"))

    heights = np.linspace(0.02, 8.0, 260)
    field = amplitude(xs[:, None], np.zeros((1, len(heights))), side * heights[None, :])
    best = np.argmax(field, axis=1)
    peak = field[np.arange(len(xs)), best]
    centre = side * heights[best]
    alive = peak >= c
    angles = np.linspace(0, 2 * np.pi, segments + 1)
    X = np.repeat(xs[:, None], len(angles), axis=1)
    Zc = np.repeat(centre[:, None], len(angles), axis=1)
    cos, sin = np.cos(angles)[None, :], np.sin(angles)[None, :]

    def along(s):
        return amplitude(X, s * cos, Zc + s * sin)

    reach = _bisect_radius(along, np.zeros_like(X), np.full_like(X, 8.0), c)
    reach = np.where(alive[:, None], reach, 0.0)
    grid = np.zeros(X.shape + (3,))
    grid[..., 0] = X
    grid[..., 1] = reach * cos
    grid[..., 2] = Zc + reach * sin
    return grid, alive


def contour_for_radius(radius: float) -> float:
    """1s contour level whose isolated-atom sphere has the given radius."""
    return float(np.exp(-ZETA_S * radius))


def p_contour(fraction: float = 0.3) -> float:
    """A p contour as a fraction of the lobe's peak amplitude, 1 / (zeta e)."""
    return fraction / (ZETA_P * np.e)


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    rs = np.linspace(30, 400, 2000)
    e = morse(rs, 436, 74, 0.0194)
    check(abs(rs[np.argmin(e)] - 74) < 0.5, "Morse minimum at r_e")
    check(abs(e.min() + 436) < 0.5, "Morse depth equals the bond energy")
    check(abs(morse(1e6, 436, 74, 0.0194)) < 1e-6, "separated atoms at zero energy")
    push, pull = morse_terms(rs, 436, 74, 0.0194)
    check(np.allclose(push + pull, e), "push + pull = total")
    check(push[-1] / -pull[-1] < 0.05, "the pull reaches farther than the push")
    check(abs(morse_inverse(0.0, 436, 74, 0.0194) - (74 - np.log(2) / 0.0194)) < 1e-9, "inner zero crossing")
    check(abs(coulomb_kj(1, -1, 282) + 492.7) < 0.5, "Na+ Cl- point-charge pair at 282 pm")
    m = madelung_rock_salt()
    check(abs(m - 1.74756) < 2e-3, f"Madelung constant {m:.5f}")
    sites, kinds = rock_salt_sites(2)
    shells = neighbour_shells(sites, kinds)
    check([(n, same) for _, n, same in shells] == [(6, False), (12, True), (8, False)], f"rock-salt shells {shells}")
    fcc = fcc_sites(1)
    check(neighbour_shells(fcc, shells=1)[0][1] == 12, "copper (fcc) has twelve nearest neighbours")
    check(abs(s_overlap(0.0) - 1) < 1e-12 and s_overlap(10) < 0.01, "1s overlap limits")
    # At a realistic bond distance (zeta R ~ 4.7, as for carbon 2p at a C-C bond) head-on
    # overlap beats sideways overlap: the narration's "pi is usually weaker" claim.
    check(p_overlap(P_BOND, "sigma") > p_overlap(P_BOND, "pi") > 0.1, "sigma overlap must exceed pi overlap")
    # Far apart, the bonding density is the two atomic densities: a sphere of the chosen radius.
    c = contour_for_radius(2.0)
    xs = np.linspace(-14, 14, 561)
    far = revolution_profile(sigma_s_amplitude(20.0), xs, c)
    check(abs(far.max() - 2.0) < 0.02, f"isolated 1s contour radius {far.max():.3f}")
    check(far[np.argmin(np.abs(xs))] == 0.0, "no density between far-apart atoms")
    near = revolution_profile(sigma_s_amplitude(1.4), xs, c)
    check(near[np.argmin(np.abs(xs))] > 1.0, "bonded hydrogen has density between the nuclei")
    grid, alive = pi_lobe_grid(3.0, p_contour(), np.linspace(-6, 6, 41), 12)
    check(alive.any() and (grid[alive][..., 2] > 0).all(), "upper pi lobe stays above the axis")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Bond model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print(f"Bond model check passed: Morse curve and its two terms, Coulomb pair energy, Madelung "
          f"{madelung_rock_salt():.4f}, rock-salt shells 6/12/8, fcc 12 neighbours, LCAO isosurfaces.")
