"""Atomic and molecular orbitals as computed wave functions and surfaces.

Nothing in this module imports Manim: ``python -m utils.orbital_models``.

The model
---------
Two atoms sit on the x axis at x = -R/2 (A) and x = +R/2 (B), in orbital
units (bohr for hydrogen). Each carries one atomic orbital (AO):

* ``"s"``  — a 1s orbital, phi = e^{-r} / sqrt(pi);
* ``"ps"`` — a 2p orbital pointing *along* the bond, toward the other atom
  (head-on overlap, sigma);
* ``"py"`` / ``"pz"`` — a 2p orbital standing *sideways*, perpendicular to the
  bond (pi). The p orbitals use the hydrogen-like radial factor r e^{-r/2}.

The molecular orbital is the linear combination of atomic orbitals (LCAO)

    psi = (phi_A + c phi_B) / sqrt(1 + c^2 + 2 c S),

with c = +1 (in phase, bonding) or c = -1 (out of phase, antibonding); the
denominator normalises psi using the overlap S. For "ps", phi_B is defined
pointing toward A, so in-phase means *facing lobes of the same sign*, and
c = +1 is again the bonding combination. Sliding c continuously from +1 to -1
is how the film flips a phase on screen.

Surfaces
--------
An orbital is drawn as the surface |psi| = level, split into connected lobes
of each sign (``lobes``): blue where psi > 0 and rose where psi < 0. Each lobe
is extracted with marching cubes on a grid and handed to the 3D stage as a
cloud of surface points. The ``level`` is a fixed fraction of one isolated AO's
peak, so a bonding and an antibonding orbital are drawn at the same contour
and can be compared honestly.

Maps
----
``section`` samples psi on a plane through both nuclei, for the 2D phase and
density maps in chapters 02-04.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np

try:  # marching cubes and connected components
    from scipy import ndimage
    from skimage.measure import marching_cubes
except ImportError as error:  # pragma: no cover - listed in requirements.txt
    raise ImportError("orbital surfaces need scipy and scikit-image (pip install -r requirements.txt)") from error

S_NORM = 1 / np.sqrt(np.pi)
P_NORM = 1 / np.sqrt(32 * np.pi)

# Display separations (orbital units). H2's real bond is 1.4 bohr; the film
# draws 1s pairs a little wider so the node between them has room to show.
R_S = 2.0
R_P = 8.5           # p orbitals: zeta * R near 4, as for real second-period bonds, so head-on
                    # overlap beats sideways overlap (at short R the p-sigma overlap turns negative)
S_LEVEL = 0.22      # contour as a fraction of one AO's peak |psi|
P_LEVEL = 0.26


@dataclass(frozen=True)
class MOSpec:
    kind: str = "s"         # "s", "ps", "py", "pz"
    c: float = 1.0          # coefficient of phi_B (+1 bonding, -1 antibonding)
    R: float = R_S
    level: float | None = None
    single: str = ""        # "A" or "B": draw that atom's AO alone (c ignored)

    def rounded(self) -> "MOSpec":
        return MOSpec(self.kind, round(self.c, 3), round(self.R, 3), self.level, self.single)


def ao(kind: str, x, y, z, centre: float, toward: float = 1.0):
    """One atomic orbital at (centre, 0, 0). ``toward`` = +1 points a sigma p
    orbital's positive lobe along +x, -1 along -x."""
    dx = np.asarray(x) - centre
    r = np.sqrt(dx * dx + np.asarray(y) ** 2 + np.asarray(z) ** 2)
    if kind == "s":
        return S_NORM * np.exp(-r)
    radial = P_NORM * np.exp(-r / 2)
    if kind == "ps":
        return radial * dx * toward
    if kind == "py":
        return radial * np.asarray(y)
    if kind == "pz":
        return radial * np.asarray(z)
    raise ValueError(kind)


def ao_peak(kind: str) -> float:
    """Largest |phi| of one atomic orbital (the 2p peak is at r = 2)."""
    return S_NORM if kind == "s" else P_NORM * 2 * np.exp(-1)


def pair(spec: MOSpec, x, y, z) -> tuple[np.ndarray, np.ndarray]:
    a = ao(spec.kind, x, y, z, -spec.R / 2, +1.0)
    b = ao(spec.kind, x, y, z, +spec.R / 2, -1.0)
    return a, b


@lru_cache(maxsize=64)
def overlap(kind: str, R: float) -> float:
    """S = <phi_A|phi_B>, by quadrature on a fine grid (exact closed form for s)."""
    if kind == "s":
        return float(np.exp(-R) * (1 + R + R * R / 3))
    xs, h = _axis(R, kind, 0.25)
    X, Y, Z = np.meshgrid(xs, np.arange(-14, 14.01, 0.25), np.arange(-14, 14.01, 0.25), indexing="ij")
    a, b = pair(MOSpec(kind, 1.0, R), X, Y, Z)
    return float(np.sum(a * b) * h ** 3)


def psi(spec: MOSpec, x, y, z):
    a, b = pair(spec, x, y, z)
    if spec.single == "A":
        return a
    if spec.single == "B":
        return b
    S = overlap(spec.kind, round(spec.R, 3))
    norm = np.sqrt(max(1 + spec.c * spec.c + 2 * spec.c * S, 1e-9))
    return (a + spec.c * b) / norm


def level_for(spec: MOSpec) -> float:
    if spec.level is not None:
        return spec.level
    return (S_LEVEL if spec.kind == "s" else P_LEVEL) * ao_peak(spec.kind)


def _axis(R: float, kind: str, step: float) -> tuple[np.ndarray, float]:
    reach = 5.0 if kind == "s" else 12.0
    xs = np.arange(-R / 2 - reach, R / 2 + reach + 1e-9, step)
    return xs, step


def _grid(spec: MOSpec, step: float):
    xs, _ = _axis(spec.R, spec.kind, step)
    reach = 5.0 if spec.kind == "s" else 12.0
    ys = np.arange(-reach, reach + 1e-9, step)
    return xs, ys, ys


@lru_cache(maxsize=256)
def _lobes_cached(spec: MOSpec, step: float, max_points: int) -> tuple[tuple[int, np.ndarray], ...]:
    xs, ys, zs = _grid(spec, step)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    field = psi(spec, X, Y, Z)
    level = level_for(spec)
    found: list[tuple[int, float, np.ndarray]] = []
    origin = np.array([xs[0], ys[0], zs[0]])
    for sign in (1, -1):
        mask = sign * field > level
        labels, count = ndimage.label(mask)
        for k in range(1, count + 1):
            component = labels == k
            if component.sum() < 6:
                continue
            # Pad so the surface closes even if a lobe touches the grid edge.
            values = np.pad(np.where(component, sign * field, 0.0), 1)
            verts, _, _, _ = marching_cubes(values, level, spacing=(step, step, step))
            verts = verts - step + origin
            if len(verts) > max_points:
                verts = verts[np.linspace(0, len(verts) - 1, max_points).astype(int)]
            found.append((sign, float(verts[:, 0].mean()), verts))
    # Stable order: positive lobes first, then left to right.
    found.sort(key=lambda item: (-item[0], round(item[1], 2)))
    return tuple((sign, verts) for sign, _, verts in found)


def lobes(spec: MOSpec, *, step: float | None = None, max_points: int = 1600) -> list[tuple[int, np.ndarray]]:
    """[(sign, (N, 3) surface points)] for every connected lobe of |psi| = level."""
    if step is None:
        step = 0.16 if spec.kind == "s" else 0.32
    return list(_lobes_cached(spec.rounded(), step, max_points))


def section(spec: MOSpec, xs: np.ndarray, ys: np.ndarray, plane: str = "xy") -> np.ndarray:
    """psi on a plane through the bond axis: rows follow ys, columns xs."""
    X, Y = np.meshgrid(xs, ys)
    zero = np.zeros_like(X)
    if plane == "xy":
        return psi(spec, X, Y, zero)
    return psi(spec, X, zero, Y)


def axis_profile(spec: MOSpec, xs: np.ndarray, offset: float = 0.0) -> np.ndarray:
    """psi along a line parallel to the bond axis (offset sideways in y)."""
    xs = np.asarray(xs, dtype=float)
    return psi(spec, xs, np.full_like(xs, offset), np.zeros_like(xs))


@lru_cache(maxsize=32)
def _density_cached(spec: MOSpec, count: int, seed: int) -> np.ndarray:
    step = 0.2 if spec.kind == "s" else 0.4
    xs, ys, zs = _grid(spec, step)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    weight = psi(spec, X, Y, Z) ** 2
    weight = weight.ravel() / weight.sum()
    rng = np.random.default_rng(seed)
    picks = rng.choice(weight.size, size=count, p=weight)
    points = np.column_stack([X.ravel()[picks], Y.ravel()[picks], Z.ravel()[picks]])
    return points + rng.uniform(-step / 2, step / 2, points.shape)


def density_samples(spec: MOSpec, count: int = 600, seed: int = 0) -> np.ndarray:
    """Points drawn at random with probability |psi|^2: where the electron is likely to be."""
    return _density_cached(spec.rounded(), count, seed)


def chain_section(coefficients, spacing: float, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """A 1s LCAO over a row of atoms (Huckel coefficients), sampled at grid points X, Y."""
    n = len(coefficients)
    X, Y = np.asarray(X, dtype=float), np.asarray(Y, dtype=float)
    total = np.zeros_like(X)
    for i, c in enumerate(coefficients):
        centre = (i - (n - 1) / 2) * spacing
        total += c * S_NORM * np.exp(-np.sqrt((X - centre) ** 2 + Y ** 2))
    return total


def node_between(spec: MOSpec) -> bool:
    """True when psi changes sign on the bond axis between the nuclei."""
    xs = np.linspace(-spec.R / 2 + 0.05, spec.R / 2 - 0.05, 400)   # even: never sample psi = 0 exactly
    values = axis_profile(spec, xs, offset=0.0 if spec.kind in ("s", "ps") else 1.0)
    return bool(np.any(values[:-1] * values[1:] < 0))


def midpoint_density(spec: MOSpec) -> float:
    offset = 0.0 if spec.kind in ("s", "ps") else 1.5
    return float(psi(spec, 0.0, offset, 0.0) ** 2)


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    # Normalisation of single AOs, and of the combinations.
    h = 0.12
    g = np.arange(-9, 9.0001, h)
    X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
    check(abs(np.sum(ao("s", X, Y, Z, 0.0) ** 2) * h ** 3 - 1) < 0.01, "1s normalised")
    h = 0.3
    g = np.arange(-24, 24.0001, h)
    X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
    check(abs(np.sum(ao("py", X, Y, Z, 0.0) ** 2) * h ** 3 - 1) < 0.01, "2p normalised")
    check(abs(overlap("s", 2.0) - 0.5865) < 1e-3, "1s overlap at R = 2")
    check(overlap("ps", R_P) > overlap("py", R_P) > 0, "head-on p overlap beats sideways overlap at the film's R")
    for kind in ("s", "ps", "py"):
        R = R_S if kind == "s" else R_P
        bond, anti = MOSpec(kind, 1.0, R), MOSpec(kind, -1.0, R)
        check(midpoint_density(bond) > midpoint_density(anti), f"{kind}: bonding piles density in the middle")
        check(not node_between(bond) and node_between(anti), f"{kind}: node only in the antibonding orbital")
    # Lobe counts: the shapes the film describes.
    count = lambda spec, sign=None: len([1 for s, _ in lobes(spec) if sign is None or s == sign])  # noqa: E731
    check(count(MOSpec("s", 1.0)) == 1, "sigma 1s: one lobe")
    check(count(MOSpec("s", -1.0), 1) == 1 and count(MOSpec("s", -1.0), -1) == 1, "sigma* 1s: one + and one -")
    check(count(MOSpec("s", 1.0, 9.0)) == 2, "far apart, the two 1s orbitals are still two spheres")
    check(count(MOSpec("ps", 1.0, R_P), 1) == 1 and count(MOSpec("ps", 1.0, R_P), -1) == 2,
          "sigma 2p: one big middle lobe, two small back lobes")
    check(count(MOSpec("ps", -1.0, R_P), 1) == 2 and count(MOSpec("ps", -1.0, R_P), -1) == 2, "sigma* 2p: four lobes")
    check(count(MOSpec("py", 1.0, R_P)) == 2, "pi 2p: two sausages")
    check(count(MOSpec("py", -1.0, R_P)) == 4, "pi* 2p: four lobes")
    # A pi orbital and its partner turned by 90 degrees are the same shape.
    a = np.array(sorted(map(len, (v for _, v in lobes(MOSpec("py", 1.0, R_P))))))
    b = np.array(sorted(map(len, (v for _, v in lobes(MOSpec("pz", 1.0, R_P))))))
    check(np.allclose(a, b, rtol=0.05), "the two pi orbitals are rotated copies")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Orbital check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("Orbital check passed: normalisation, overlap, bonding density vs antibonding nodes, lobe counts.")
