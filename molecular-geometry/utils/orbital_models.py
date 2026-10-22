"""Atomic and hybrid orbital shapes, computed rather than drawn.

Nothing in this module imports Manim: ``python -m utils.orbital_models``.

The model
---------
Carbon's 2s and 2p orbitals are written as Slater-type functions that share
one radial factor, R(r) = r e^{-r} (r in units of 1/zeta), times their angular
parts. A hybrid along a unit direction d is the normalised mixture

    psi(r) = R(r) [ cos(alpha) Y_s + sin(alpha) Y_p(d) ],

so, up to a constant, psi = R(r) (cos alpha + sqrt(3) sin alpha cos theta),
with theta measured from d. alpha = 0 is the pure s orbital, alpha = 90
degrees the pure p orbital; sp, sp2 and sp3 hybrids are alpha = arctan(sqrt(n))
for n = 1, 2, 3 (s character 1/2, 1/3, 1/4).

Two ways to draw the same function
-----------------------------------
* **What the film draws** is the textbook picture of an orbital's direction:
  a polar plot of its angular density, r(theta) = A(theta)^2 with
  A = cos(alpha) + sqrt(3) sin(alpha) cos(theta) (``polar_profile``). Every
  mixture is normalised the same way (A^2 averages to 1 over the sphere), so
  the s orbital is a sphere of radius 1, a p lobe reaches 3, and an sp3 lobe
  reaches 4: adding p really does make one side grow and the other shrink.
  Lobes touch the nucleus, which makes their direction unmistakable.
* **The physical cross-check** is a |psi| = constant surface with a shared
  Slater-type radial factor R(r) = r e^{-r} (``lobe_profile``). Such
  isosurfaces are much fatter (an sp3 lobe is wider than it is long), which
  is why they are not used for the pictures, but they agree on everything the
  film claims: each hybrid points along d, its back lobe has the opposite
  phase, and the back lobe grows as the p fraction rises (sp < sp2 < sp3).

The sign of psi (the phase) is shown by colour. Orthogonality fixes the
angles: equivalent hybrids s + sqrt(n) p_i must have zero overlap with each
other, which forces cos(theta_ij) = -1/n. That is checked here, and chapter
14 shows it.
"""

from __future__ import annotations

from functools import lru_cache
from math import atan, degrees, sqrt

import numpy as np

from utils import math_utils as mu
from utils import physics_models as pm

SQRT3 = sqrt(3.0)
_integrate = getattr(np, "trapezoid", None) or np.trapz
RADIAL_POWER = 1                 # R(r) = r^k e^{-r}; k = 1 is the 2s/2p Slater form
R_PEAK = float(RADIAL_POWER)     # where R is largest
R_MAX = R_PEAK ** RADIAL_POWER * np.exp(-R_PEAK)
LEVEL = 0.40 * R_MAX             # the |psi| contour drawn, relative to the pure s orbital's peak
H_LEVEL = 0.30                   # the hydrogen 1s contour (e^{-r} = H_LEVEL)


def radial(r):
    r = np.asarray(r, dtype=float)
    return r ** RADIAL_POWER * np.exp(-r)


@lru_cache(maxsize=1)
def _radial_tables() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    inner = np.linspace(0.0, R_PEAK, 4000)
    outer = np.linspace(R_PEAK, 40.0, 16000)
    return inner, radial(inner), outer[::-1], radial(outer)[::-1]


def radial_inverse(value) -> tuple[np.ndarray, np.ndarray]:
    """Inner and outer radii where R(r) equals ``value`` (NaN where it never does)."""
    r_in, f_in, r_out, f_out = _radial_tables()
    value = np.asarray(value, dtype=float)
    inside = np.interp(value, f_in, r_in, left=np.nan, right=np.nan)
    outside = np.interp(value, f_out, r_out, left=np.nan, right=np.nan)
    impossible = value > R_MAX
    inside = np.where(impossible, np.nan, inside)
    outside = np.where(impossible, np.nan, outside)
    return inside, outside


def angular(theta, alpha: float):
    """Angular factor of the hybrid, theta measured from its own direction."""
    return np.cos(alpha) + SQRT3 * np.sin(alpha) * np.cos(theta)


def mixing_angle(p_per_s: float) -> float:
    """alpha for an sp^n hybrid: tan(alpha) = sqrt(n)."""
    return atan(sqrt(p_per_s))


SP_ALPHA = {"s": 0.0, "sp": mixing_angle(1), "sp2": mixing_angle(2), "sp3": mixing_angle(3), "p": np.pi / 2}


def _edge(alpha: float, sign: int) -> float | None:
    """Largest angle (from the lobe's own axis) at which the lobe still exists;
    None when the lobe is absent, pi when it closes all the way round."""
    need = LEVEL / R_MAX
    a, b = np.cos(alpha), SQRT3 * np.sin(alpha)
    # sign * A(theta) >= need, with theta measured from +d (sign +1) or -d (sign -1):
    # sign=+1: a + b cos(t) >= need;  sign=-1: b cos(t) - a >= need
    peak = (a + b) if sign > 0 else (b - a)
    if peak < need - 1e-12:
        return None
    if b < 1e-12:
        return np.pi if sign > 0 and a >= need else None
    c = (need - a) / b if sign > 0 else (need + a) / b
    if c <= -1:
        return np.pi
    return float(np.arccos(np.clip(c, -1, 1)))


def lobe_profile(alpha: float, sign: int = 1, samples: int = 40) -> np.ndarray | None:
    """Closed boundary of one lobe in its (axial z, radial rho) half-plane.

    The lobe of sign ``sign`` points along +d (sign +1) or -d (sign -1). The
    curve runs out along the outer surface and back along the inner one, so
    revolving it about the axis gives the whole closed lobe.
    """
    edge = _edge(alpha, sign)
    if edge is None:
        return None
    t = np.linspace(0.0, 1.0, samples)
    theta = edge * np.sin(t * np.pi / 2)          # crowd samples near the rim
    A = np.abs(angular(theta, alpha) if sign > 0 else angular(np.pi - theta, alpha))
    r_in, r_out = radial_inverse(LEVEL / np.maximum(A, 1e-12))
    if edge >= np.pi - 1e-9:
        # A closed shell (the s-like case): only the outer surface is visible.
        theta_full = np.linspace(0.0, np.pi, samples * 2)
        A_full = np.abs(angular(theta_full, alpha))
        _, r = radial_inverse(LEVEL / np.maximum(A_full, 1e-12))
        return np.column_stack([r * np.cos(theta_full), r * np.sin(theta_full)])
    keep = ~(np.isnan(r_in) | np.isnan(r_out))
    theta, r_in, r_out = theta[keep], r_in[keep], r_out[keep]
    outer = np.column_stack([r_out * np.cos(theta), r_out * np.sin(theta)])
    inner = np.column_stack([r_in * np.cos(theta), r_in * np.sin(theta)])[::-1]
    return np.vstack([outer, inner])


def revolve(profile: np.ndarray, axis, segments: int = 18) -> np.ndarray:
    """Points of the surface made by spinning a (z, rho) profile about ``axis``."""
    frame = mu.frame_from_axis(axis)
    phi = np.linspace(0, 2 * np.pi, segments, endpoint=False)
    z = profile[:, 0][:, None]
    rho = profile[:, 1][:, None]
    points = (z[..., None] * frame[:, 2]
              + (rho * np.cos(phi))[..., None] * frame[:, 0]
              + (rho * np.sin(phi))[..., None] * frame[:, 1])
    return points.reshape(-1, 3)


def lobe_points(alpha: float, axis, sign: int = 1, samples: int = 32, segments: int = 18) -> np.ndarray | None:
    """Surface points of one lobe in orbital units (centred on the nucleus)."""
    profile = lobe_profile(alpha, sign, samples)
    if profile is None or len(profile) < 3:
        return None
    direction = mu.unit(axis) * sign
    return revolve(profile, direction, segments)


def lobe_reach(alpha: float, sign: int = 1) -> float:
    """How far a lobe extends from the nucleus along its axis (0 if absent)."""
    profile = lobe_profile(alpha, sign)
    return 0.0 if profile is None else float(profile[:, 0].max())


def hydrogen_radius() -> float:
    """Radius of the hydrogen 1s contour e^{-r} = H_LEVEL (same units)."""
    return float(-np.log(H_LEVEL))


# ---------------------------------------------------------------------------
# The drawn picture: polar plots of the angular density
# ---------------------------------------------------------------------------


def polar_profile(alpha: float, sign: int = 1, samples: int = 72) -> np.ndarray | None:
    """(z, rho) boundary of one lobe of r(theta) = A(theta)^2, theta from the lobe's own axis.

    ``sign`` +1 is the lobe where psi > 0 (pointing along +d); -1 is the
    lobe where psi < 0 (pointing along -d). None when that lobe is absent.
    """
    a, b = np.cos(alpha), SQRT3 * np.sin(alpha)
    theta = np.linspace(0.0, np.pi, samples)
    value = a + b * np.cos(theta) if sign > 0 else b * np.cos(theta) - a
    keep = value > 1e-9
    if keep.sum() < 3:
        return None
    th = theta[keep]
    r = value[keep] ** 2
    profile = np.column_stack([r * np.cos(th), r * np.sin(th)])
    if not keep[-1]:
        profile = np.vstack([profile, [[0.0, 0.0]]])   # the lobe closes at the nucleus
    return profile


def polar_points(alpha: float, axis, sign: int = 1, segments: int = 24) -> np.ndarray | None:
    """Surface points of one drawn lobe (orbital units, centred on the nucleus)."""
    profile = polar_profile(alpha, sign)
    if profile is None:
        return None
    return revolve(profile, mu.unit(axis) * sign, segments)


def polar_reach(alpha: float, sign: int = 1) -> float:
    profile = polar_profile(alpha, sign)
    return 0.0 if profile is None else float(profile[:, 0].max())


# ---------------------------------------------------------------------------
# Hybrid sets
# ---------------------------------------------------------------------------

HYBRID_P_PER_S = {"sp": 1, "sp2": 2, "sp3": 3}


def hybrid_directions(kind: str) -> np.ndarray:
    """Directions of the hybrids, in the same orientation as the VSEPR arrangement."""
    return pm.ideal_directions(HYBRID_P_PER_S[kind] + 1)


def leftover_p(kind: str) -> list[np.ndarray]:
    """Axes of the p orbitals left out of the mix (they can form pi bonds)."""
    return {"sp": [np.array([0.0, 1, 0]), np.array([0.0, 0, 1])],
            "sp2": [np.array([0.0, 0, 1])],
            "sp3": []}[kind]


def coefficients(kind: str) -> np.ndarray:
    """Rows: hybrids. Columns: coefficients of s, px, py, pz."""
    n = HYBRID_P_PER_S[kind]
    a, b = 1 / sqrt(n + 1), sqrt(n / (n + 1))
    return np.array([[a, *(b * d)] for d in hybrid_directions(kind)])


def equivalent_hybrid_cosine(p_per_s: float) -> float:
    """cos(angle) between equivalent orthogonal hybrids s + sqrt(n) p: -1/n."""
    return -1.0 / p_per_s


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    for kind, n in HYBRID_P_PER_S.items():
        C = coefficients(kind)
        check(np.allclose(C @ C.T, np.eye(n + 1)), f"{kind} hybrids are orthonormal")
        d = hybrid_directions(kind)
        cosines = [float(np.dot(d[i], d[j])) for i in range(n + 1) for j in range(i + 1, n + 1)]
        check(np.allclose(cosines, equivalent_hybrid_cosine(n)), f"{kind}: cos(angle) = -1/{n}")
        check(abs(np.tan(SP_ALPHA[kind]) ** 2 - n) < 1e-12, f"{kind} mixing angle")
        check(abs(np.cos(SP_ALPHA[kind]) ** 2 - 1 / (n + 1)) < 1e-12, f"{kind} s character is 1/{n + 1}")
        for p in leftover_p(kind):
            check(all(abs(np.dot(p, v)) < 1e-12 for v in d), f"{kind} leftover p is perpendicular")
        check(len(leftover_p(kind)) + n == 3, f"{kind} uses every p orbital once")
    check(abs(degrees(np.arccos(equivalent_hybrid_cosine(3))) - pm.TETRAHEDRAL_DEG) < 1e-12,
          "sp3 angle equals the cube's")

    # Shapes: an s orbital is round, a p orbital is two equal lobes, and a
    # hybrid's big lobe outgrows its small one as soon as any p is mixed in.
    s = lobe_profile(0.0)
    r = np.hypot(s[:, 0], s[:, 1])
    check(np.allclose(r, r[0]), "s contour is a sphere")
    check(lobe_profile(0.0, -1) is None, "s has no negative lobe")
    check(abs(lobe_reach(np.pi / 2, 1) - lobe_reach(np.pi / 2, -1)) < 1e-9, "p lobes are equal")
    for kind in ("sp", "sp2", "sp3"):
        big, small = lobe_reach(SP_ALPHA[kind], 1), lobe_reach(SP_ALPHA[kind], -1)
        check(big > 1.25 * small, f"{kind}: big lobe clearly longer than the small one")
    backs = [lobe_reach(SP_ALPHA[k], -1) for k in ("sp", "sp2", "sp3")]
    check(backs[0] < backs[1] < backs[2], "more p character grows the back lobe")
    reaches = [lobe_reach(SP_ALPHA[k], 1) for k in ("sp", "sp2", "sp3")]
    check(all(x > lobe_reach(0.0) for x in reaches), "hybrids reach further than the s sphere")
    # Continuity: the shape changes smoothly with the mixing angle.
    alphas = np.linspace(0, np.pi / 2, 91)
    reach = np.array([lobe_reach(a) for a in alphas])
    check(np.all(np.abs(np.diff(reach)) < 0.25), "the dial morph is continuous")
    pts = lobe_points(SP_ALPHA["sp3"], [0, 1, 0])
    check(pts is not None and np.dot(pts.mean(axis=0), [0, 1, 0]) > 0, "a lobe points along its axis")

    # The drawn polar plots agree with the isosurfaces on every claim.
    theta = np.linspace(0, np.pi, 20001)
    for alpha in np.linspace(0, np.pi / 2, 7):
        mean_sq = _integrate(angular(theta, alpha) ** 2 * np.sin(theta), theta) / 2
        check(abs(mean_sq - 1) < 1e-6, "every mixture is normalised the same way")
    check(abs(polar_reach(0.0) - 1) < 1e-9 and polar_profile(0.0, -1) is None, "s: a unit sphere")
    check(abs(polar_reach(np.pi / 2) - 3) < 1e-9 and abs(polar_reach(np.pi / 2, -1) - 3) < 1e-9, "p: two lobes of 3")
    drawn_backs = [polar_reach(SP_ALPHA[k], -1) for k in ("sp", "sp2", "sp3")]
    check(drawn_backs[0] < drawn_backs[1] < drawn_backs[2], "drawn back lobes grow with p character too")
    check(abs(polar_reach(SP_ALPHA["sp3"]) - 4) < 1e-9 and abs(polar_reach(SP_ALPHA["sp3"], -1) - 1) < 1e-9,
          "sp3 drawn lobes: 4 forward, 1 back")
    for kind in ("sp", "sp2", "sp3"):
        drawn = polar_points(SP_ALPHA[kind], [1, 0, 0])
        check(drawn is not None and drawn[:, 0].mean() > 0, f"{kind} drawn lobe points along its axis")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Orbital model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("Orbital model check passed: sp, sp2, sp3 hybrids are orthonormal with cos(angle) = -1/n,")
    print("s is round, p has equal lobes, hybrid lobes are lopsided, and the s-to-p dial is continuous.")
    print("The drawn polar plots agree with the isosurfaces on direction, phase and back-lobe growth.")
    for kind in ("s", "sp", "sp2", "sp3", "p"):
        a = SP_ALPHA[kind]
        print(f"  {kind:>3}: alpha = {degrees(a):5.1f} deg | drawn lobes {polar_reach(a):.2f} / {polar_reach(a, -1):.2f}"
              f" | isosurface lobes {lobe_reach(a):.2f} / {lobe_reach(a, -1):.2f}")
