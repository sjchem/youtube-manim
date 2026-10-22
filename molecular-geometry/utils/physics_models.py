"""The geometry the film's pictures are computed from (VSEPR, vectors, the cube).

Nothing in this module imports Manim, so every model can be checked with
plain numbers: ``python -m utils.physics_models``.

* **Electron regions repel.** The simple VSEPR model is played out literally:
  n unit vectors on a sphere push each other apart under a Coulomb-like
  1/d repulsion, and ``relax`` follows the gradient flow until they stop. The
  self-check confirms that this finds, on its own, the linear, trigonal planar,
  tetrahedral, trigonal bipyramidal and octahedral arrangements, and the
  chapter 03 and 09/11 animations replay the actual relaxation paths. It is a
  model of the idea, not a quantum calculation.
* **Lone-pair sites** follow the textbook VSEPR rule: among the ideal
  positions, choose the lone-pair placement that first minimises lone-pair /
  lone-pair contacts at about 90 degrees, then lone-pair / bond contacts.
  ``best_lone_pair_sites`` returns every optimal placement, so a chosen
  layout can be asserted optimal rather than asserted by hand.
* **Shapes are named from positions.** ``classify`` looks only at where the
  bonded atoms are, so the name on screen is derived from the same
  coordinates that are drawn.
* **Bond dipoles** are drawn as vectors toward the more electronegative atom,
  with length proportional to the electronegativity difference — an
  illustration of direction and symmetry, not a calculation of dipole moment.
"""

from __future__ import annotations

from itertools import combinations
from math import acos, degrees, sqrt

import numpy as np

from utils import math_utils as mu

TETRAHEDRAL_DEG = degrees(acos(-1 / 3))   # 109.4712...


# ---------------------------------------------------------------------------
# Ideal arrangements, in one canonical orientation per region count
# ---------------------------------------------------------------------------
#
# The orientations chain together, so each arrangement grows out of the
# previous one in chapters 03, 09 and 11 (see RELAXATION_STARTS):
#   2: along the x axis
#   3: in the screen plane, one region straight up
#   4: one region up, three below (back, front-right, front-left)
#   5: axial up/down, equatorial back, front-right, front-left
#   6: +y, -y, +x, -x, +z, -z


def _ring(y: float, azimuths_deg, radius: float) -> list[list[float]]:
    return [[radius * np.sin(np.radians(a)), y, radius * np.cos(np.radians(a))] for a in azimuths_deg]


IDEAL: dict[int, np.ndarray] = {
    2: np.array([[-1.0, 0, 0], [1.0, 0, 0]]),
    3: np.array([[0.0, 1, 0], [np.cos(np.radians(210)), np.sin(np.radians(210)), 0],
                 [np.cos(np.radians(330)), np.sin(np.radians(330)), 0]]),
    4: np.array([[0.0, 1, 0]] + _ring(-1 / 3, (180, 60, 300), sqrt(8 / 9))),
    5: np.array([[0.0, 1, 0], [0.0, -1, 0]] + _ring(0.0, (180, 60, 300), 1.0)),
    6: np.array([[0.0, 1, 0], [0.0, -1, 0], [1.0, 0, 0], [-1.0, 0, 0], [0.0, 0, 1], [0.0, 0, -1]]),
}

ELECTRON_GEOMETRY: dict[int, str] = {
    2: "linear",
    3: "trigonal planar",
    4: "tetrahedral",
    5: "trigonal bipyramidal",
    6: "octahedral",
}

# Positions of the trigonal bipyramid, by index into IDEAL[5].
AXIAL = (0, 1)
EQUATORIAL = (2, 3, 4)


def ideal_directions(n: int) -> np.ndarray:
    return IDEAL[n].copy()


def pair_angles(directions: np.ndarray) -> list[float]:
    return sorted(mu.angle_deg(a, b) for a, b in combinations(directions, 2))


# ---------------------------------------------------------------------------
# Repulsion on a sphere
# ---------------------------------------------------------------------------


def repulsion_energy(directions: np.ndarray, power: float = 1.0) -> float:
    total = 0.0
    for a, b in combinations(np.asarray(directions, dtype=float), 2):
        total += 1.0 / np.linalg.norm(a - b) ** power
    return total


def relax(start: np.ndarray, power: float = 1.0, max_steps: int = 20000, max_move: float = 0.012,
          rate: float = 0.25, tol: float = 1e-7) -> np.ndarray:
    """Follow the repulsion's gradient flow on the unit sphere.

    Returns the whole path, shape (steps, n, 3). Each step moves the regions
    along the tangential part of their net push; the largest move is capped
    so the path is smooth enough to animate directly; near the minimum the
    step is ``rate`` times the push (plain gradient descent).
    """
    U = np.array([mu.unit(v) for v in np.asarray(start, dtype=float)])
    path = [U.copy()]
    n = len(U)
    for _ in range(max_steps):
        diff = U[:, None, :] - U[None, :, :]
        dist = np.linalg.norm(diff, axis=2) + np.eye(n)
        push = (power * diff / dist[:, :, None] ** (power + 2)).sum(axis=1)
        tangential = push - (push * U).sum(axis=1, keepdims=True) * U
        biggest = float(np.abs(tangential).max())
        if biggest < tol:
            break
        U = U + tangential * min(rate, max_move / biggest)
        U /= np.linalg.norm(U, axis=1, keepdims=True)
        path.append(U.copy())
    return np.array(path)


def resample_path(path: np.ndarray, count: int = 120) -> np.ndarray:
    """Re-space a relaxation path evenly by how far the regions actually move,
    so the slow final creep does not dominate the animation's timing."""
    steps = np.linalg.norm(np.diff(path, axis=0), axis=2).max(axis=1)
    progress = np.concatenate([[0.0], np.cumsum(steps)])
    if progress[-1] < 1e-12:
        return np.repeat(path[:1], count, axis=0)
    progress /= progress[-1]
    targets = np.linspace(0, 1, count)
    result = np.empty((count,) + path.shape[1:])
    for k, t in enumerate(targets):
        i = int(np.clip(np.searchsorted(progress, t) - 1, 0, len(path) - 2))
        span = progress[i + 1] - progress[i]
        f = 0.0 if span < 1e-12 else (t - progress[i]) / span
        blend = path[i] * (1 - f) + path[i + 1] * f
        result[k] = blend / np.linalg.norm(blend, axis=1, keepdims=True)
    return result


def _nudge(vector, toward, amount: float) -> np.ndarray:
    return mu.unit(mu.unit(vector) + amount * np.asarray(toward, dtype=float))


# Where each relaxation in the film starts. Every start is chosen so the
# regions settle into IDEAL[n] exactly (in the same orientation), which is
# what lets one arrangement grow continuously into the next.
TIPPED_TRIANGLE = (mu.rotation_x(-np.pi / 2) @ IDEAL[3].T).T   # chapter 03: lay the triangle flat

RELAXATION_STARTS: dict[int, np.ndarray] = {
    # Two regions squeezed together near the top of the atom.
    2: np.array([[np.cos(np.radians(112)), np.sin(np.radians(112)), 0],
                 [np.cos(np.radians(68)), np.sin(np.radians(68)), 0]]),
    # The line, plus a newcomer straight up.
    3: np.array([[-1.0, 0, 0], [1.0, 0, 0], [0.0, 1, 0]]),
    # The triangle laid flat, plus a newcomer on top (the umbrella).
    4: np.vstack([[0.0, 1, 0], TIPPED_TRIANGLE[[0, 1, 2]]]),
    # The tetrahedron, plus a newcomer underneath.
    5: np.vstack([IDEAL[4][:1], [[0.0, -1, 0]], IDEAL[4][1:]]),
    # The bipyramid, plus a newcomer on the equator between two regions.
    6: np.vstack([IDEAL[5], [[0.0, 0, 1]]]),
}


def _match_order(path: np.ndarray, n: int) -> np.ndarray:
    """Reorder the path's regions so its final frame lines up with IDEAL[n]."""
    final = path[-1]
    order = []
    for target in IDEAL[n]:
        scores = [np.dot(final[i], target) if i not in order else -9 for i in range(n)]
        order.append(int(np.argmax(scores)))
    return path[:, order, :]


def settle(directions, count: int = 120) -> np.ndarray:
    """Relax regions given in any order; the path keeps that order.

    Used by the chapters, whose lobes are listed in the order they appeared.
    The final frame snaps each region onto the nearest ideal direction when
    the regions end in the canonical orientation (the film's starts do; a
    random start keeps its own orientation and is not snapped).
    """
    start = np.asarray(directions, dtype=float)
    path = resample_path(relax(start), count)
    n = len(start)
    ideal = IDEAL.get(n)
    if ideal is not None:
        nearest = [ideal[int(np.argmax(ideal @ d))] for d in path[-1]]
        if all(mu.angle_deg(a, b) < 0.5 for a, b in zip(path[-1], nearest)) and len(
                {tuple(v) for v in np.round(nearest, 6)}) == n:
            path[-1] = np.array(nearest)
    return path


def relaxation_path(n: int, count: int = 120) -> np.ndarray:
    """The animated settling of n regions, ending exactly on IDEAL[n]."""
    path = _match_order(relax(RELAXATION_STARTS[n]), n)
    sampled = resample_path(path, count)
    # Remove the last few hundredths of a degree of creep so the final frame
    # is the ideal arrangement itself; ``verify`` bounds that correction.
    sampled[-1] = IDEAL[n]
    return sampled


# ---------------------------------------------------------------------------
# Lone pairs: which positions do they take?
# ---------------------------------------------------------------------------

CROWDED_DEG = 100.0   # "about 90 degrees": the contacts VSEPR counts


def contacts(directions: np.ndarray, lone: set[int] | frozenset[int]) -> tuple[int, int, int]:
    """Count crowded (~90 degree) contacts: (lone-lone, lone-bond, bond-bond)."""
    lp_lp = lp_bp = bp_bp = 0
    for i, j in combinations(range(len(directions)), 2):
        if mu.angle_deg(directions[i], directions[j]) > CROWDED_DEG:
            continue
        kinds = (i in lone) + (j in lone)
        if kinds == 2:
            lp_lp += 1
        elif kinds == 1:
            lp_bp += 1
        else:
            bp_bp += 1
    return lp_lp, lp_bp, bp_bp


def neighbours_at_90(n: int, index: int) -> list[int]:
    """Positions about 90 degrees from position ``index`` of IDEAL[n]."""
    d = IDEAL[n]
    return [j for j in range(n) if j != index and mu.angle_deg(d[index], d[j]) <= CROWDED_DEG]


def best_lone_pair_sites(n: int, lone_pairs: int) -> list[frozenset[int]]:
    """Every lone-pair placement that minimises (lone-lone, lone-bond) contacts."""
    if lone_pairs == 0:
        return [frozenset()]
    scored = []
    for chosen in combinations(range(n), lone_pairs):
        lp_lp, lp_bp, _ = contacts(IDEAL[n], set(chosen))
        scored.append(((lp_lp, lp_bp), frozenset(chosen)))
    best = min(score for score, _ in scored)
    return [choice for score, choice in scored if score == best]


# ---------------------------------------------------------------------------
# Naming a shape from where its atoms are
# ---------------------------------------------------------------------------

MOLECULAR_SHAPES: dict[tuple[int, int], str] = {
    (2, 0): "linear",
    (3, 0): "trigonal planar",
    (2, 1): "bent",
    (4, 0): "tetrahedral",
    (3, 1): "trigonal pyramidal",
    (2, 2): "bent",
    (5, 0): "trigonal bipyramidal",
    (4, 1): "seesaw",
    (3, 2): "T-shaped",
    (2, 3): "linear",
    (6, 0): "octahedral",
    (5, 1): "square pyramidal",
    (4, 2): "square planar",
}


def classify(bond_directions: np.ndarray) -> str:
    """Name the shape made by the bonded atoms around a central atom."""
    d = np.array([mu.unit(v) for v in bond_directions])
    m = len(d)
    angles = pair_angles(d)
    straight = sum(a > 160 for a in angles)
    if m == 2:
        return "linear" if straight else "bent"
    if m == 3:
        planar = abs(np.linalg.det(d)) < 0.05
        if planar:
            return "T-shaped" if straight else "trigonal planar"
        return "trigonal pyramidal"
    if m == 4:
        if straight == 2:
            return "square planar"
        if straight == 1:
            return "seesaw"
        if all(abs(a - TETRAHEDRAL_DEG) < 3 for a in angles):
            return "tetrahedral"
        return "distorted tetrahedral"
    if m == 5:
        return {1: "trigonal bipyramidal", 2: "square pyramidal"}.get(straight, "irregular")
    if m == 6:
        return "octahedral" if straight == 3 else "irregular"
    return "irregular"


def axe_label(bonds: int, lone_pairs: int) -> str:
    """The AXmEn code as LaTeX, e.g. AX_3E or AX_2E_2."""
    x = "X" if bonds == 1 else f"X_{bonds}"
    e = "" if lone_pairs == 0 else ("E" if lone_pairs == 1 else f"E_{lone_pairs}")
    return f"A{x}{e}"


# ---------------------------------------------------------------------------
# Adjusting ideal directions to measured angles (keeping the symmetry)
# ---------------------------------------------------------------------------


def set_pair_angle(a, b, angle_deg: float) -> tuple[np.ndarray, np.ndarray]:
    """Open or close two directions symmetrically about their bisector."""
    a, b = mu.unit(a), mu.unit(b)
    bisector = mu.unit(a + b)
    side = mu.unit(a - bisector * np.dot(a, bisector))
    half = np.radians(angle_deg / 2)
    return bisector * np.cos(half) + side * np.sin(half), bisector * np.cos(half) - side * np.sin(half)


def set_cone_angle(directions: np.ndarray, axis, angle_deg: float) -> np.ndarray:
    """Place directions symmetrically around ``axis`` (keeping their azimuths)
    so that neighbouring pairs make ``angle_deg``; used for C3v pyramids."""
    axis = mu.unit(axis)
    count = len(directions)
    # cos(angle) = cos^2(g) + sin^2(g) cos(2 pi / count), solved for the cone half-angle g.
    c_az = np.cos(2 * np.pi / count)
    sin2 = (1 - np.cos(np.radians(angle_deg))) / (1 - c_az)
    g = np.arcsin(np.sqrt(min(max(sin2, 0.0), 1.0)))
    result = []
    for v in directions:
        perp = mu.unit(v - axis * np.dot(v, axis))
        result.append(axis * np.cos(g) + perp * np.sin(g))
    return np.array(result)


def tilt(direction, toward, degrees_: float) -> np.ndarray:
    """Rotate ``direction`` by ``degrees_`` toward the direction ``toward``."""
    d, t = mu.unit(direction), mu.unit(toward)
    axis = np.cross(d, t)
    if np.linalg.norm(axis) < 1e-9:
        return d
    return mu.rotation_about(axis, np.radians(degrees_)) @ d


# ---------------------------------------------------------------------------
# Vectors: bond dipoles and their sum
# ---------------------------------------------------------------------------


def bond_dipoles(central: str, ligands, electronegativity: dict[str, float]) -> list[np.ndarray]:
    """One vector per bond, pointing to the atom that pulls harder.

    ``ligands`` is a list of (symbol, unit direction from the central atom).
    Length is the electronegativity difference: an illustration only.
    """
    vectors = []
    for symbol, direction in ligands:
        difference = electronegativity[symbol] - electronegativity[central]
        vectors.append(mu.unit(direction) * difference)
    return vectors


def vector_sum(vectors) -> np.ndarray:
    return np.sum(np.asarray(vectors, dtype=float), axis=0)


def tip_to_tail(vectors, start=None) -> list[tuple[np.ndarray, np.ndarray]]:
    """Chain vectors head to tail; returns (start, end) of each link."""
    point = np.zeros(3) if start is None else np.asarray(start, dtype=float)
    links = []
    for v in vectors:
        links.append((point.copy(), point + v))
        point = point + v
    return links


# ---------------------------------------------------------------------------
# The cube: where 109.47 degrees comes from
# ---------------------------------------------------------------------------

CUBE_CORNERS = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float)


def cube_dot_product() -> tuple[float, float, float]:
    """(dot, |a| |b|, cosine) for two alternate cube corners seen from the centre."""
    a, b = CUBE_CORNERS[0], CUBE_CORNERS[1]
    dot = float(np.dot(a, b))
    lengths = float(np.linalg.norm(a) * np.linalg.norm(b))
    return dot, lengths, dot / lengths


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    expected = {2: [180.0], 3: [120.0] * 3, 4: [TETRAHEDRAL_DEG] * 6,
                5: sorted([90.0] * 6 + [120.0] * 3 + [180.0]), 6: sorted([90.0] * 12 + [180.0] * 3)}
    for n, angles in expected.items():
        check(np.allclose(pair_angles(IDEAL[n]), angles, atol=1e-6), f"ideal {n}-region angles")
        check(np.allclose(np.linalg.norm(IDEAL[n], axis=1), 1), f"ideal {n} directions are unit")
        # Repulsion finds the same arrangement from the film's start ...
        path = _match_order(relax(RELAXATION_STARTS[n]), n)
        check(np.allclose(pair_angles(path[-1]), angles, atol=0.05), f"relaxation finds the {n}-region arrangement")
        check(max(mu.angle_deg(a, b) for a, b in zip(path[-1], IDEAL[n])) < 0.5,
              f"relaxation of {n} ends in the canonical orientation")
        # ... and from a random start (an orientation-free check).
        rng = np.random.default_rng(7 + n)
        random_end = relax(rng.normal(size=(n, 3)))[-1]
        check(np.allclose(pair_angles(random_end), angles, atol=0.1), f"random start also gives the {n} arrangement")
        # The ideal arrangement is a minimum: nudging it raises the energy.
        nudged = IDEAL[n] + 0.03 * rng.normal(size=(n, 3))
        nudged /= np.linalg.norm(nudged, axis=1, keepdims=True)
        check(repulsion_energy(nudged) > repulsion_energy(IDEAL[n]), f"{n}-region arrangement is a minimum")
        sampled = relaxation_path(n)
        start_units = np.array([mu.unit(v) for v in RELAXATION_STARTS[n]])
        check(all(np.linalg.norm(start_units - row, axis=1).min() < 1e-6 for row in sampled[0]),
              f"relaxation path {n} begins at the film's start")

    # Lone pairs: the textbook placements fall out of counting 90-degree contacts.
    check(all(c <= set(EQUATORIAL) for c in best_lone_pair_sites(5, 1)), "AX4E lone pair is equatorial")
    check(all(c <= set(EQUATORIAL) for c in best_lone_pair_sites(5, 2)), "AX3E2 lone pairs are equatorial")
    check(best_lone_pair_sites(5, 3) == [frozenset(EQUATORIAL)], "AX2E3 lone pairs fill the equator")
    check(len(neighbours_at_90(5, AXIAL[0])) == 3 and len(neighbours_at_90(5, EQUATORIAL[0])) == 2,
          "axial has 3 neighbours at 90 degrees, equatorial 2")
    trans = {frozenset({0, 1}), frozenset({2, 3}), frozenset({4, 5})}
    check(set(best_lone_pair_sites(6, 2)) == trans, "AX4E2 lone pairs are trans")
    check(len(best_lone_pair_sites(6, 1)) == 6, "every octahedral site is equivalent")

    # Every (bonds, lone pairs) shape name follows from the positions themselves.
    for (bonds, lone), name in MOLECULAR_SHAPES.items():
        n = bonds + lone
        lone_sites = best_lone_pair_sites(n, lone)[0]
        bond_dirs = np.array([IDEAL[n][i] for i in range(n) if i not in lone_sites])
        check(classify(bond_dirs) == name, f"{axe_label(bonds, lone)} should classify as {name}")

    # The cube and the hybrid-orbital argument agree on 109.47 degrees.
    dot, lengths, cosine = cube_dot_product()
    check(dot == -1 and abs(lengths - 3) < 1e-12 and abs(cosine + 1 / 3) < 1e-12, "cube dot product")
    check(abs(degrees(acos(cosine)) - TETRAHEDRAL_DEG) < 1e-12, "cube gives the tetrahedral angle")
    check(all(abs(mu.angle_deg(IDEAL[4][i], IDEAL[4][j]) - TETRAHEDRAL_DEG) < 1e-9
              for i, j in combinations(range(4), 2)), "canonical tetrahedron")

    # Adjustments keep symmetry and hit the requested angles.
    a, b = set_pair_angle(IDEAL[4][2], IDEAL[4][3], 104.5)
    check(abs(mu.angle_deg(a, b) - 104.5) < 1e-9, "pair angle set")
    cone = set_cone_angle(IDEAL[4][1:], -IDEAL[4][0], 106.7)
    check(all(abs(mu.angle_deg(cone[i], cone[j]) - 106.7) < 1e-9 for i, j in combinations(range(3), 2)),
          "cone angle set")

    # Symmetric arrangements of identical bonds cancel; lopsided ones do not.
    en = {"A": 2.0, "X": 3.0}
    for n in (2, 3, 4, 5, 6):
        total = vector_sum(bond_dipoles("A", [("X", d) for d in IDEAL[n]], en))
        check(np.linalg.norm(total) < 1e-9, f"{n} identical bond dipoles cancel")
    bent = vector_sum(bond_dipoles("A", [("X", d) for d in IDEAL[4][2:]], en))
    check(np.linalg.norm(bent) > 0.5, "two tetrahedral bond dipoles do not cancel")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Geometry model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("Geometry model check passed: repulsion relaxation finds all five arrangements (from the film's")
    print("starts and from random ones), lone pairs go where 90-degree contacts are fewest, every AXmEn shape")
    print(f"is named from its own coordinates, the cube gives {TETRAHEDRAL_DEG:.2f} degrees, symmetric dipoles cancel.")
