"""The physics the film's pictures are computed from.

Two models live here, and no scene file types a number either could compute:

**The table** (carried over unchanged from Part 3). Every tile position, block,
period length and configuration is computed from three ingredients —

1. subshells ``(n, l)`` with ``l = 0, 1, 2, 3`` for ``s, p, d, f``;
2. a subshell holds ``2 (2l + 1)`` electrons (2l + 1 orbitals, two spins each);
3. subshells fill in Madelung order: increasing ``n + l``, ties to smaller ``n``.

— plus documented layout conventions (helium and the group-3/f boundary)
and selected ground-state exceptions, which change *configurations*
but never *positions*.

**The atom** (new in Part 4). The outer electron's "felt" charge comes from
Slater's shielding rules — a rough, classic estimate used here only to scale
the pull arrows, never shown as a precise number — and every electron cloud is
a seeded random sample of a hydrogen-like radial density, so the clouds are
statistics rather than decoration. Coulomb's law sets the pull-versus-distance
picture of chapter 03.

Run ``python -m utils.physics_models`` for a self-check. Nothing in this module
imports Manim.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np

L_LETTERS = "spdf"

SYMBOLS: tuple[str, ...] = tuple(
    """H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni
    Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe
    Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg
    Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg
    Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og""".split()
)

# Only the elements the narration names out loud need a name.
NAMES: dict[str, str] = {
    "H": "Hydrogen", "He": "Helium", "Li": "Lithium", "Be": "Beryllium",
    "B": "Boron", "C": "Carbon", "N": "Nitrogen", "O": "Oxygen",
    "F": "Fluorine", "Ne": "Neon", "Na": "Sodium", "Mg": "Magnesium",
    "Cl": "Chlorine", "Ar": "Argon", "K": "Potassium", "Ca": "Calcium",
    "Sc": "Scandium", "Ti": "Titanium", "V": "Vanadium", "Cr": "Chromium",
    "Mn": "Manganese", "Fe": "Iron", "Co": "Cobalt", "Ni": "Nickel",
    "Cu": "Copper", "Zn": "Zinc", "Ga": "Gallium", "Br": "Bromine",
    "Kr": "Krypton", "Rb": "Rubidium", "Sr": "Strontium", "I": "Iodine",
    "Xe": "Xenon", "Cs": "Caesium", "Ba": "Barium", "La": "Lanthanum",
    "Yb": "Ytterbium", "Lu": "Lutetium", "Au": "Gold", "Ac": "Actinium",
    "No": "Nobelium", "Lr": "Lawrencium", "Rn": "Radon", "Og": "Oganesson",
}

NOBLE_GASES: tuple[int, ...] = (2, 10, 18, 36, 54, 86, 118)


def z_of(symbol: str) -> int:
    return SYMBOLS.index(symbol) + 1


def symbol_of(z: int) -> str:
    return SYMBOLS[z - 1]


# ---------------------------------------------------------------------------
# Subshells and the Madelung order
# ---------------------------------------------------------------------------


@dataclass(frozen=True, order=True)
class Subshell:
    n: int
    l: int

    @property
    def letter(self) -> str:
        return L_LETTERS[self.l]

    @property
    def label(self) -> str:
        return f"{self.n}{self.letter}"

    @property
    def orbitals(self) -> int:
        return 2 * self.l + 1

    @property
    def capacity(self) -> int:
        return 2 * self.orbitals

    @property
    def madelung(self) -> int:
        return self.n + self.l


def subshell(label: str) -> Subshell:
    return Subshell(int(label[:-1]), L_LETTERS.index(label[-1]))


@lru_cache(maxsize=None)
def madelung_order(max_electrons: int = 118) -> tuple[Subshell, ...]:
    """Subshells sorted by n + l, ties broken by smaller n, until Z is covered."""
    candidates = [Subshell(n, l) for n in range(1, 9) for l in range(min(n, 4))]
    candidates.sort(key=lambda s: (s.madelung, s.n))
    order: list[Subshell] = []
    total = 0
    for shell in candidates:
        if total >= max_electrons:
            break
        order.append(shell)
        total += shell.capacity
    return tuple(order)


@lru_cache(maxsize=None)
def filling_step(z: int) -> tuple[Subshell, int]:
    """Subshell and seat for the idealized Madelung grid, not every real atom."""
    if not 1 <= z <= len(SYMBOLS):
        raise ValueError(f"Z must lie in 1..{len(SYMBOLS)}")
    seen = 0
    for shell in madelung_order():
        if z <= seen + shell.capacity:
            return shell, z - seen
        seen += shell.capacity
    raise AssertionError("Madelung order does not cover Z")


def aufbau_configuration(z: int) -> list[tuple[Subshell, int]]:
    """The idealized Madelung configuration, in filling order."""
    config: list[tuple[Subshell, int]] = []
    remaining = z
    for shell in madelung_order():
        if remaining <= 0:
            break
        take = min(shell.capacity, remaining)
        config.append((shell, take))
        remaining -= take
    return config


# Neutral-atom ground configurations that differ from the Madelung idealization
# (NIST Atomic Spectra Database ground levels). Only the subshells that change
# are listed; a zero removes a subshell. These change configurations, never the
# position of an element in the table.
EXCEPTIONS: dict[int, dict[str, int]] = {
    24: {"3d": 5, "4s": 1},             # Cr
    29: {"3d": 10, "4s": 1},            # Cu
    41: {"4d": 4, "5s": 1},             # Nb
    42: {"4d": 5, "5s": 1},             # Mo
    44: {"4d": 7, "5s": 1},             # Ru
    45: {"4d": 8, "5s": 1},             # Rh
    46: {"4d": 10, "5s": 0},            # Pd
    47: {"4d": 10, "5s": 1},            # Ag
    57: {"4f": 0, "5d": 1},             # La
    58: {"4f": 1, "5d": 1},             # Ce
    64: {"4f": 7, "5d": 1},             # Gd
    78: {"5d": 9, "6s": 1},             # Pt
    79: {"5d": 10, "6s": 1},            # Au
    89: {"5f": 0, "6d": 1},             # Ac
    90: {"5f": 0, "6d": 2},             # Th
    91: {"5f": 2, "6d": 1},             # Pa
    92: {"5f": 3, "6d": 1},             # U
    93: {"5f": 4, "6d": 1},             # Np
    96: {"5f": 7, "6d": 1},             # Cm
    103: {"6d": 0, "7p": 1},            # Lr
}


def ground_configuration(z: int) -> list[tuple[Subshell, int]]:
    """Teaching configuration with selected exceptions, sorted by (n, l).

    Heavy-element defaults are Madelung predictions, not a complete database.
    """
    counts = {shell: count for shell, count in aufbau_configuration(z)}
    for label, count in EXCEPTIONS.get(z, {}).items():
        counts[subshell(label)] = count
    config = sorted(((s, c) for s, c in counts.items() if c > 0), key=lambda item: (item[0].n, item[0].l))
    if sum(c for _, c in config) != z:
        raise AssertionError(f"Configuration for Z={z} does not hold Z electrons")
    return config


def noble_core(z: int) -> int:
    """The largest noble gas strictly lighter than ``z`` (0 for H and He)."""
    cores = [g for g in NOBLE_GASES if g < z]
    return cores[-1] if cores else 0


def config_latex(z: int, *, core: bool = True, actual: bool = True) -> str:
    """LaTeX for a configuration, e.g. ``[\\mathrm{Ar}]\\,4s^{1}``."""
    full = ground_configuration(z) if actual else sorted(aufbau_configuration(z), key=lambda i: (i[0].n, i[0].l))
    parts: list[str] = []
    skip: dict[Subshell, int] = {}
    if core and noble_core(z):
        gas = noble_core(z)
        skip = {s: c for s, c in aufbau_configuration(gas)}
        parts.append(rf"[\mathrm{{{symbol_of(gas)}}}]")
    for shell, count in full:
        if skip.get(shell) == count:
            continue
        parts.append(rf"{shell.n}{shell.letter}^{{{count}}}")
    return r"\,".join(parts)


def outer_latex(z: int) -> str:
    """Only the outermost s and p electrons — the pattern a group shares."""
    config = ground_configuration(z)
    top = max(s.n for s, _ in config)
    return r"\,".join(rf"{s.n}{s.letter}^{{{c}}}" for s, c in config if s.n == top and s.l <= 1)


def generic_outer_latex(z: int) -> str:
    """The shell-free form of the outer pattern: ``ns^{2}np^{5}``."""
    config = ground_configuration(z)
    top = max(s.n for s, _ in config)
    return "".join(rf"n{s.letter}^{{{c}}}" for s, c in config if s.n == top and s.l <= 1)


# ---------------------------------------------------------------------------
# Where an element sits — computed, never typed
# ---------------------------------------------------------------------------


def block(z: int) -> str:
    """Structural block in the chosen idealized grid (Madelung plus conventions)."""
    return filling_step(z)[0].letter


def period(z: int) -> int:
    shell, _ = filling_step(z)
    return shell.n + {0: 0, 1: 0, 2: 1, 3: 2}[shell.l]


# Column offsets inside each layout. ``standard`` is the familiar 18-column
# table with the f block parked below; ``wide`` is the expanded 32-column form.
_OFFSETS = {
    "standard": {"s": 0, "f": 2, "d": 2, "p": 12},
    "wide": {"s": 0, "f": 2, "d": 16, "p": 26},
}
_LAST_COLUMN = {"standard": 18, "wide": 32}


def position(z: int, layout: str = "standard") -> tuple[int, int]:
    """(row, column), both 1-based.

    In the standard layout the f block occupies rows 8 and 9, under columns
    3–16. The chosen group-3 boundary is a layout convention. Helium also uses
    chemical placement: its
    configuration 1s² is an s-block one, but its closed shell gives it noble-gas
    chemistry, so chemists place it at the top of the last column.
    """
    shell, seat = filling_step(z)
    if z == 2:
        return 1, _LAST_COLUMN[layout]
    row = period(z)
    column = _OFFSETS[layout][shell.letter] + seat
    if layout == "standard" and shell.letter == "f":
        row = 2 + row  # period 6 -> row 8, period 7 -> row 9
    return row, column


def elements_in_block(letter: str) -> list[int]:
    return [z for z in range(1, len(SYMBOLS) + 1) if block(z) == letter]


def block_width(letter: str, layout: str = "standard") -> int:
    """How many distinct columns a block occupies — the table's widths."""
    zs = [z for z in elements_in_block(letter) if z != 2]
    return len({position(z, layout)[1] for z in zs})


def period_members(p: int) -> list[int]:
    return [z for z in range(1, len(SYMBOLS) + 1) if period(z) == p]


def period_lengths() -> list[int]:
    return [len(period_members(p)) for p in range(1, 8)]


def period_recipe(p: int) -> list[tuple[Subshell, int]]:
    """Subshells filled during one period, with how many elements each adds."""
    recipe: list[tuple[Subshell, int]] = []
    for z in period_members(p):
        shell, _ = filling_step(z)
        if recipe and recipe[-1][0] == shell:
            recipe[-1] = (shell, recipe[-1][1] + 1)
        else:
            recipe.append((shell, 1))
    return recipe


def group_members(column: int) -> list[int]:
    """Main-table column members, top to bottom (f block excluded)."""
    members = [z for z in range(1, len(SYMBOLS) + 1) if position(z)[1] == column and position(z)[0] <= 7]
    return sorted(members, key=lambda z: position(z)[0])


# ---------------------------------------------------------------------------
# Orbital-box filling
# ---------------------------------------------------------------------------


def hund_slots(l: int, count: int) -> list[tuple[int, int]]:
    """(orbital index, spin) for each successive electron in a subshell.

    Singly occupy every orbital with parallel spin first, then pair — the
    ground-state preference Part 2 introduced as Hund's first rule.
    """
    orbitals = 2 * l + 1
    if not 0 <= count <= 2 * orbitals:
        raise ValueError("Count exceeds the subshell's capacity")
    slots = [(i, +1) for i in range(orbitals)] + [(i, -1) for i in range(orbitals)]
    return slots[:count]


# ---------------------------------------------------------------------------
# The felt charge: Slater's shielding rules for an outer s or p electron
# ---------------------------------------------------------------------------


def outer_shell(z: int) -> int:
    """Principal number of the outermost occupied shell."""
    return max(shell.n for shell, _ in ground_configuration(z))


def slater_zeff(z: int, electrons: int | None = None) -> float:
    """Effective nuclear charge felt by one outermost s/p electron.

    Slater (1930): another electron in the same (ns, np) group screens 0.35
    (0.30 within 1s); each electron in shell n - 1 screens 0.85; each electron
    deeper in screens 1.00. ``electrons`` lets an ion be estimated (its
    electrons fill the neutral sequence of that many electrons). A model, used
    only to scale arrows; real Z_eff values (e.g. Clementi's) differ in detail.
    """
    config = ground_configuration(z if electrons is None else electrons)
    n = max(shell.n for shell, _ in config)
    partners = sum(count for shell, count in config if shell.n == n and shell.l <= 1) - 1
    shielding = partners * (0.30 if n == 1 else 0.35)
    for shell, count in config:
        if shell.n == n and shell.l <= 1:
            continue
        shielding += count * (0.85 if shell.n == n - 1 else 1.00)
    return z - shielding


# ---------------------------------------------------------------------------
# Electron clouds: seeded samples of a hydrogen-like radial density
# ---------------------------------------------------------------------------

# A 1s-like radial probability density P(r) ~ r^2 exp(-2r/a) is a Gamma(3, a/2)
# distribution. Its 90 % quantile, in units of a/2, is 5.3223; dividing by it
# puts the "90 % of the cloud" contour at radius 1.
GAMMA3_Q90 = 5.322320
CLOUD_REACH = 1.45  # samples beyond 1.45 contour radii are redrawn (too faint to matter)


def cloud_samples(count: int, seed: int) -> np.ndarray:
    """Schematic radial probability samples with ~90 % inside a unit sphere.

    The same seed always gives the same cloud, so every render matches.
    """
    rng = np.random.default_rng(seed)
    points = []
    while len(points) < count:
        r = rng.gamma(3.0, 1.0) / GAMMA3_Q90
        if r > CLOUD_REACH:
            continue
        direction = rng.normal(size=3)
        direction /= np.linalg.norm(direction)
        points.append(direction * r)
    return np.array(points)


def coulomb_pull(charge: float, distance: float) -> float:
    """Relative attraction between a charge and one electron: F ~ q / r^2."""
    return charge / distance ** 2


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------


def verify() -> list[str]:
    """Return a list of failures; an empty list means the model is consistent."""
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    check(len(SYMBOLS) == 118, "118 element symbols")
    order = " ".join(s.label for s in madelung_order())
    check(order == "1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s 5f 6d 7p", f"Madelung order: {order}")
    check(period_lengths() == [2, 8, 8, 18, 18, 32, 32], f"period lengths {period_lengths()}")
    for letter, width in zip("spdf", (2, 6, 10, 14)):
        check(block_width(letter) == width, f"{letter} block width {block_width(letter)}")
        check(block_width(letter, "wide") == width, f"{letter} block wide width")
    expected = {
        "H": (1, 1), "He": (1, 18), "Li": (2, 1), "Ne": (2, 18), "K": (4, 1),
        "Sc": (4, 3), "Fe": (4, 8), "Zn": (4, 12), "Ga": (4, 13), "Kr": (4, 18),
        "Y": (5, 3), "Lu": (6, 3), "Au": (6, 11), "Lr": (7, 3), "La": (8, 3),
        "Yb": (8, 16), "Ac": (9, 3), "No": (9, 16), "U": (9, 6), "Og": (7, 18),
    }
    for sym, place in expected.items():
        check(position(z_of(sym)) == place, f"{sym} at {position(z_of(sym))}, expected {place}")
    for z in range(1, 119):
        configuration = ground_configuration(z)
        check(sum(c for _, c in configuration) == z, f"electron count for Z={z}")
        check(all(0 < c <= shell.capacity for shell, c in configuration), f"subshell overflow for Z={z}")
    for p in range(1, 8):
        columns = [position(z, "wide")[1] for z in period_members(p)]
        check(columns == sorted(columns), f"atomic-number order in expanded period {p}")
    positions = [position(z) for z in range(1, 119)]
    check(len(set(positions)) == 118, "two elements share a tile")
    check(len({position(z, 'wide') for z in range(1, 119)}) == 118, "wide layout collision")
    check(config_latex(19) == r"[\mathrm{Ar}]\,4s^{1}", f"K config {config_latex(19)}")
    check(config_latex(24) == r"[\mathrm{Ar}]\,3d^{5}\,4s^{1}", f"Cr config {config_latex(24)}")
    check(config_latex(29) == r"[\mathrm{Ar}]\,3d^{10}\,4s^{1}", f"Cu config {config_latex(29)}")
    check(config_latex(3) == r"[\mathrm{He}]\,2s^{1}", f"Li config {config_latex(3)}")
    check(outer_latex(35) == r"4s^{2}\,4p^{5}", f"Br outer {outer_latex(35)}")
    check(generic_outer_latex(9) == "ns^{2}np^{5}", f"F generic {generic_outer_latex(9)}")
    check([symbol_of(z) for z in group_members(1)] == ["H", "Li", "Na", "K", "Rb", "Cs", "Fr"], "group 1")
    check(hund_slots(1, 4) == [(0, 1), (1, 1), (2, 1), (0, -1)], "Hund slots for oxygen")
    recipe = [(s.label, k) for s, k in period_recipe(6)]
    check(recipe == [("6s", 2), ("4f", 14), ("5d", 10), ("6p", 6)], f"period 6 recipe {recipe}")

    # Slater's rules reproduce the textbook estimates the arrows are scaled by.
    for sym, expected in {"Li": 1.30, "Be": 1.95, "C": 3.25, "F": 5.20, "Ne": 5.85,
                          "Na": 2.20, "K": 2.20, "Cs": 2.20, "Cl": 6.10}.items():
        check(abs(slater_zeff(z_of(sym)) - expected) < 1e-9, f"Slater Z_eff {sym} {slater_zeff(z_of(sym)):.2f}")
    across = [slater_zeff(z) for z in range(3, 10)]
    check(all(a < b for a, b in zip(across, across[1:])), "Z_eff must rise across period 2")
    ions = [slater_zeff(8, 10), slater_zeff(9, 10), slater_zeff(11, 10), slater_zeff(12, 10)]
    check(all(a < b for a, b in zip(ions, ions[1:])), "Z_eff must rise along O2-, F-, Na+, Mg2+")
    check([outer_shell(z_of(s)) for s in ("Li", "Na", "K", "Rb", "Cs")] == [2, 3, 4, 5, 6], "outer shells")

    samples = cloud_samples(4000, 7)
    inside = float((np.linalg.norm(samples, axis=1) <= 1).mean())
    check(0.88 <= inside <= 0.94, f"the radius-1 contour should hold ~90 % of the cloud, holds {inside:.3f}")
    check(np.array_equal(cloud_samples(50, 3), cloud_samples(50, 3)), "clouds must be reproducible")
    check(abs(coulomb_pull(1, 2) / coulomb_pull(1, 1) - 0.25) < 1e-12, "double distance, quarter pull")
    check(abs(coulomb_pull(2, 1) / coulomb_pull(1, 1) - 2.0) < 1e-12, "double charge, double pull")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("Model check passed: 118 elements, Madelung order, block widths 2/6/10/14,")
    print(f"period lengths {period_lengths()}, tile positions, Slater Z_eff estimates,")
    print("reproducible radial probability samples and the Coulomb pull ratios.")
