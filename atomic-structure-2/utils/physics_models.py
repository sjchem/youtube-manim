"""Numerical hydrogen states, Gaussian uncertainties, and filling diagrams.

Atomic units (a0 = hbar = electron mass = 1) unless stated otherwise.

The real angular functions used here are a *real basis*, not individual
magnetic eigenstates except for m = 0. The signed integer indexes the
sine/cosine combinations, which is why the film says on screen that the p_x and
p_y drawings are combinations rather than literal m = -1 and m = +1 states.

Everything in this module is deliberately free of Manim: it produces numbers,
and manim_scenes/common.py decides how they are drawn.
"""

from __future__ import annotations

from functools import lru_cache
from math import factorial, pi, sqrt

import numpy as np
from scipy.special import eval_genlaguerre, lpmv


# ---------------------------------------------------------------------------
# Hydrogen wave functions
# ---------------------------------------------------------------------------


def radial(n: int, l: int, r):
    """The normalized hydrogen radial function R_{n,l}(r) in atomic units."""
    if not (n >= 1 and 0 <= l < n):
        raise ValueError("Require n >= 1 and 0 <= l < n")
    rho = 2 * np.asarray(r) / n
    norm = sqrt((2 / n) ** 3 * factorial(n - l - 1) / (2 * n * factorial(n + l)))
    return norm * np.exp(-rho / 2) * rho**l * eval_genlaguerre(n - l - 1, 2 * l + 1, rho)


def radial_distribution(n: int, l: int, r):
    """The radial distribution function P(r) = r^2 R_{n,l}(r)^2, in atomic units.

    This is the quantity that answers "how far from the nucleus is the electron
    likely to be found", and it is *not* the probability density. For 1s the
    density |psi|^2 is largest at the nucleus, while this function vanishes
    there and peaks at exactly one Bohr radius -- which is the number Bohr
    assumed. The angular factor integrates to one over the sphere, so no
    separate 4*pi appears here; that form is only correct for s states.
    """
    r = np.asarray(r, dtype=float)
    return r * r * radial(n, l, r) ** 2


def most_probable_radius(n: int, l: int, limit: float | None = None) -> float:
    """Where the radial distribution peaks, in Bohr radii, found on a fine grid."""
    span = limit if limit is not None else 4.0 * n * n + 12.0
    r = np.linspace(1e-6, span, 40001)
    return float(r[int(np.argmax(radial_distribution(n, l, r)))])


def real_angular(l: int, m: int, xyz):
    """A normalized real spherical harmonic evaluated on Cartesian points."""
    xyz = np.asarray(xyz)
    r = np.linalg.norm(xyz, axis=-1)
    z = np.divide(xyz[..., 2], r, out=np.zeros_like(r), where=r > 0)
    phi = np.arctan2(xyz[..., 1], xyz[..., 0])
    k = abs(m)
    norm = sqrt((2 * l + 1) / (4 * pi) * factorial(l - k) / factorial(l + k))
    angular = norm * lpmv(k, l, z)
    if m > 0:
        angular = sqrt(2) * angular * np.cos(k * phi)
    elif m < 0:
        angular = sqrt(2) * angular * np.sin(k * phi)
    return angular


def psi(n: int, l: int, m: int, xyz):
    """The real spatial wave function of a hydrogen state, sign included."""
    xyz = np.asarray(xyz)
    return radial(n, l, np.linalg.norm(xyz, axis=-1)) * real_angular(l, m, xyz)


def grid_extent(n: int) -> float:
    """Half-width of the sampling box, in Bohr radii, for principal number n."""
    return {1: 8.0, 2: 20.0, 3: 35.0, 4: 55.0}.get(n, 4 * n * n)


@lru_cache(maxsize=32)
def density_grid(n: int, l: int, m: int, resolution: int = 39):
    """Sample psi on a cubic grid. Cached: a chapter reuses one state heavily."""
    extent = grid_extent(n)
    axis = np.linspace(-extent, extent, resolution)
    xyz = np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1)
    return xyz, psi(n, l, m, xyz), float(axis[1] - axis[0])


# ---------------------------------------------------------------------------
# Isodensity surfaces
# ---------------------------------------------------------------------------


def _taubin_smooth(vertices: np.ndarray, faces: np.ndarray, passes: int) -> np.ndarray:
    """Relax a marching-cubes mesh without shrinking it.

    Plain Laplacian smoothing removes the staircase, but it also contracts the
    surface, and it keeps contracting the narrow neck where two lobes of a d
    state meet until the mesh tears. The tear is not subtle on screen: the
    background shows through the middle of the atom. Taubin's method alternates
    a shrinking pass with a slightly larger inflating one, which smooths the
    facets while holding the volume, so the neck survives.
    """
    if passes <= 0:
        return vertices
    edges = np.vstack([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    edges = np.vstack([edges, edges[:, ::-1]])
    source, target = edges[:, 0], edges[:, 1]
    degree = np.bincount(source, minlength=len(vertices)).astype(float)
    degree[degree == 0] = 1.0
    smoothed = vertices.astype(float)
    for index in range(passes):
        weight = 0.52 if index % 2 == 0 else -0.54
        neighbour_sum = np.zeros_like(smoothed)
        np.add.at(neighbour_sum, source, smoothed[target])
        smoothed = smoothed + weight * (neighbour_sum / degree[:, None] - smoothed)
    return smoothed


@lru_cache(maxsize=32)
def orbital_mesh(n: int, l: int, m: int, fraction: float = 0.90, resolution: int = 33):
    """Isodensity surface enclosing approximately `fraction` of grid probability.

    Discrete quadrature on a finite box; a visualization, not precision data.
    Returns physical coordinates, triangle indices, per-face signs of psi, and
    the enclosed probability actually achieved.
    """
    from skimage.measure import marching_cubes

    _, amplitude, step = density_grid(n, l, m, resolution)
    density = amplitude**2
    ordered = np.sort(density.ravel())[::-1]
    cumulative = np.cumsum(ordered)
    threshold = ordered[np.searchsorted(cumulative, fraction * cumulative[-1])]
    vertices, faces, _, _ = marching_cubes(density, level=float(threshold), spacing=(step,) * 3)
    vertices = vertices - grid_extent(n)
    signs = np.sign(psi(n, l, m, vertices[faces].mean(axis=1)))
    enclosed = float(density[density >= threshold].sum() / density.sum())
    return vertices, faces, signs, enclosed


@lru_cache(maxsize=32)
def orbital_geometry(
    n: int,
    l: int,
    m: int,
    fraction: float = 0.90,
    resolution: int = 33,
    passes: int = 14,
):
    """A shading-ready isosurface: triangles, smooth normals and signs of psi.

    The normals are area-weighted vertex normals averaged back onto each face.
    A renderer that colours a face from that average reads as a curved surface
    rather than as a bag of flat plates, which is what lets the film use a
    coarse grid and still look smooth.
    """
    vertices, faces, _, enclosed = orbital_mesh(n, l, m, fraction, resolution)
    vertices = _taubin_smooth(vertices, faces, passes)
    triangles = vertices[faces]

    face_normals = np.cross(
        triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]
    )
    lengths = np.linalg.norm(face_normals, axis=1)
    lengths[lengths == 0] = 1.0
    face_normals /= lengths[:, None]

    centroids = triangles.mean(axis=1)
    # Point every normal away from the origin so "outward" is unambiguous.
    face_normals[np.einsum("ij,ij->i", face_normals, centroids) < 0] *= -1

    vertex_normals = np.zeros_like(vertices)
    for corner in range(3):
        np.add.at(vertex_normals, faces[:, corner], face_normals)
    lengths = np.linalg.norm(vertex_normals, axis=1)
    lengths[lengths == 0] = 1.0
    vertex_normals /= lengths[:, None]

    smooth_normals = vertex_normals[faces].mean(axis=1)
    lengths = np.linalg.norm(smooth_normals, axis=1)
    lengths[lengths == 0] = 1.0
    smooth_normals /= lengths[:, None]

    signs = np.sign(psi(n, l, m, centroids))
    return triangles, smooth_normals, signs, enclosed


# ---------------------------------------------------------------------------
# Sampling, uncertainty, occupancy
# ---------------------------------------------------------------------------


def sample_positions(n: int = 1, l: int = 0, m: int = 0, count: int = 700, seed: int = 20260913):
    """Independent position samples; 1s uses its exact radial Gamma distribution."""
    rng = np.random.default_rng(seed)
    if (n, l, m) == (1, 0, 0):
        r = rng.gamma(shape=3, scale=0.5, size=count)
        directions = rng.normal(size=(count, 3))
        directions /= np.linalg.norm(directions, axis=1)[:, None]
        return directions * r[:, None]
    xyz, amplitude, step = density_grid(n, l, m, 65)
    weights = amplitude.ravel() ** 2
    weights /= weights.sum()
    chosen = rng.choice(weights.size, count, p=weights)
    return xyz.reshape(-1, 3)[chosen] + rng.uniform(-step / 2, step / 2, (count, 3))


def sigma_p(sigma_x, hbar: float = 1.0):
    """The momentum width of a minimum-uncertainty Gaussian of width sigma_x."""
    return hbar / (2 * np.asarray(sigma_x))


def wave_packet(x, sigma_x: float = 1, k: float = 5):
    """A real component of a Gaussian packet: envelope times a carrier."""
    return (
        (2 * pi * sigma_x**2) ** -0.25
        * np.exp(-np.asarray(x) ** 2 / (4 * sigma_x**2))
        * np.cos(k * np.asarray(x))
    )


def occupancy(z: int):
    """Neutral H through Ar in the displayed ground-state orbital approximation.

    Each subshell is returned as a list of spatial orbitals, and each orbital as
    the list of spins occupying it. Electrons spread singly across equal-energy
    orbitals before pairing, which is Hund's first rule as the diagram shows it.
    """
    if not 0 <= z <= 18:
        raise ValueError("This teaching sequence supports H through Ar")
    result = []
    remaining = z
    for label, orbitals in (("1s", 1), ("2s", 1), ("2p", 3), ("3s", 1), ("3p", 3)):
        electrons = min(remaining, 2 * orbitals)
        remaining -= electrons
        spins: list[list[int]] = [[] for _ in range(orbitals)]
        for index in range(electrons):
            spins[index % orbitals].append(1 if index < orbitals else -1)
        result.append((label, spins))
    return result


def configuration(z: int) -> str:
    """The spectroscopic configuration string for a neutral atom, H through Ar."""
    return " ".join(
        f"{name}^{sum(map(len, states))}" for name, states in occupancy(z) if any(states)
    )


def madelung_order(count: int = 10) -> list[tuple[str, int, int, int]]:
    """Subshells in increasing (n + l), ties broken by lower n: Madelung's rule.

    Returns ``(label, n, l, n + l)`` so a chapter can show the arithmetic that
    produced the order rather than asserting the order itself. The rule is a
    very good guide to the ground configurations of neutral atoms, not a law:
    the real ordering depends on the atom, the configuration and the charge.
    """
    letters = "spdf"
    shells = [
        (n + l, n, f"{n}{letters[l]}", n, l)
        for n in range(1, 8)
        for l in range(min(n, len(letters)))
    ]
    shells.sort(key=lambda item: (item[0], item[1]))
    return [(label, n, l, total) for total, _, label, n, l in shells[:count]]
