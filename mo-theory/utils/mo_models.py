"""Molecular orbital diagrams as data: levels, filling, bond order, magnetism.

Nothing in this module imports Manim: ``python -m utils.mo_models``.

Every diagram in the film is drawn from a ``Diagram`` built here, and every
arrow on it comes from ``placements`` — the Aufbau order with the Pauli limit
of two opposite spins per orbital and Hund's rule (spread out, spins parallel,
before pairing in a degenerate set). Bond orders, unpaired-electron counts and
"paramagnetic / diamagnetic" verdicts are computed from those placements, never
typed into a scene; ``utils.mo_data`` checks them against the literature.

Energies are schematic display units, not electron-volts. Only the *ordering*
is physics, and it is the standard introductory ordering for homonuclear
diatomic molecules of the first two periods:

* ``"1s"``       — H2+, H2, He2+, He2: sigma 1s below sigma* 1s;
* ``"mixed"``    — B2, C2, N2: s-p mixing lifts sigma 2p above the pi 2p pair;
* ``"unmixed"``  — O2, F2 (and Ne2): sigma 2p lies below the pi 2p pair.

The antibonding level always rises a little more than its bonding partner
falls, which is what LCAO with overlap gives (see ``physics_models``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Atoms
# ---------------------------------------------------------------------------

VALENCE_ELECTRONS: dict[str, int] = {"H": 1, "He": 2, "Li": 1, "Be": 2, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7,
                                     "Ne": 8}

# Which valence ordering each second-period element's homonuclear molecule uses.
ORDERING: dict[str, str] = {"H": "1s", "He": "1s", "B": "mixed", "C": "mixed", "N": "mixed", "O": "unmixed",
                            "F": "unmixed", "Ne": "unmixed"}


# ---------------------------------------------------------------------------
# Diagrams
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AOLevel:
    key: str            # "1s", "2s", "2p"
    energy: float
    degeneracy: int     # 1 for s, 3 for p
    tex: str


@dataclass(frozen=True)
class MOLevel:
    key: str            # "s1s", "s1s*", "s2s", "s2s*", "s2p", "p2p", "p2p*", "s2p*"
    energy: float
    degeneracy: int     # 1 for sigma, 2 for pi
    bonding: bool
    parent: str         # the atomic level it comes from
    tex: str            # its LaTeX label
    spoken: str         # how the narrator says it


@dataclass(frozen=True)
class Diagram:
    kind: str
    ao: tuple[AOLevel, ...]
    mo: tuple[MOLevel, ...]

    def level(self, key: str) -> MOLevel:
        for level in self.mo:
            if level.key == key:
                return level
        raise KeyError(key)

    def ao_level(self, key: str) -> AOLevel:
        for level in self.ao:
            if level.key == key:
                return level
        raise KeyError(key)

    def ordered(self) -> list[MOLevel]:
        return sorted(self.mo, key=lambda level: level.energy)

    @property
    def orbital_count(self) -> int:
        return sum(level.degeneracy for level in self.mo)

    @property
    def atomic_orbital_count(self) -> int:
        return 2 * sum(level.degeneracy for level in self.ao)


AO_TEX = {"1s": "1s", "2s": "2s", "2p": "2p"}

MO_TEX = {
    "s1s": r"\sigma_{1s}", "s1s*": r"\sigma^{*}_{1s}",
    "s2s": r"\sigma_{2s}", "s2s*": r"\sigma^{*}_{2s}",
    "s2p": r"\sigma_{2p}", "s2p*": r"\sigma^{*}_{2p}",
    "p2p": r"\pi_{2p}", "p2p*": r"\pi^{*}_{2p}",
}
MO_SPOKEN = {
    "s1s": "sigma one s", "s1s*": "sigma star one s", "s2s": "sigma two s", "s2s*": "sigma star two s",
    "s2p": "sigma two p", "s2p*": "sigma star two p", "p2p": "pi two p", "p2p*": "pi star two p",
}

# Schematic energies (display units). The two valence sets differ only where
# s-p mixing acts: sigma 2s/sigma* 2s are pushed down a little and sigma 2p /
# sigma* 2p up, enough for sigma 2p to cross the pi pair.
_ONE_S = {"s1s": -1.0, "s1s*": 1.35}
_UNMIXED = {"s2s": -0.9, "s2s*": 1.0, "s2p": 2.0, "p2p": 2.95, "p2p*": 4.5, "s2p*": 5.6}
_MIXED = {"s2s": -1.15, "s2s*": 0.75, "s2p": 3.75, "p2p": 2.95, "p2p*": 4.5, "s2p*": 5.9}
AO_ENERGY = {"1s": 0.0, "2s": 0.0, "2p": 3.6}
# One energy window for every valence diagram, so two diagrams side by side
# put the same level at the same height.
VALENCE_WINDOW = (-1.45, 6.2)
ONE_S_WINDOW = (-1.4, 1.75)

_PARENT = {"s1s": "1s", "s1s*": "1s", "s2s": "2s", "s2s*": "2s", "s2p": "2p", "p2p": "2p", "p2p*": "2p",
           "s2p*": "2p"}


def _mo(key: str, energy: float) -> MOLevel:
    return MOLevel(key, energy, 2 if key.startswith("p") else 1, not key.endswith("*"), _PARENT[key], MO_TEX[key],
                   MO_SPOKEN[key])


def diagram(kind: str, mixing: float | None = None) -> Diagram:
    """The diagram for an ordering. ``mixing`` (0..1) blends the two valence
    orderings continuously, for the s-p mixing chapter."""
    if kind == "1s":
        ao = (AOLevel("1s", AO_ENERGY["1s"], 1, AO_TEX["1s"]),)
        return Diagram(kind, ao, tuple(_mo(k, e) for k, e in _ONE_S.items()))
    ao = (AOLevel("2s", AO_ENERGY["2s"], 1, AO_TEX["2s"]), AOLevel("2p", AO_ENERGY["2p"], 3, AO_TEX["2p"]))
    if mixing is None:
        mixing = {"mixed": 1.0, "unmixed": 0.0}[kind]
    energies = {k: _UNMIXED[k] + (_MIXED[k] - _UNMIXED[k]) * mixing for k in _UNMIXED}
    return Diagram(kind, ao, tuple(_mo(k, e) for k, e in energies.items()))


def crossing_mixing() -> float:
    """The mixing strength at which sigma 2p rises level with the pi pair."""
    return (_UNMIXED["p2p"] - _UNMIXED["s2p"]) / (_MIXED["s2p"] - _UNMIXED["s2p"])


# ---------------------------------------------------------------------------
# A toy map from the atom's 2s-2p gap to mixing strength (chapter 13)
# ---------------------------------------------------------------------------
# s-p mixing weakens as the 2s-2p gap widens. The film shows that trend with a
# saturating toy map, m = 1 / (1 + (gap / G0)^4), applied to measured average
# valence-orbital energies (utils.mo_data.ORBITAL_ENERGY_EV). G0 is chosen so
# the crossing falls between nitrogen and oxygen, as observed. It is a
# picture of a trend, not a calculation of any energy.

MIXING_G0_EV = 14.93
MIXING_POWER = 4


def mixing_from_gap(gap_ev: float) -> float:
    return 1.0 / (1.0 + (gap_ev / MIXING_G0_EV) ** MIXING_POWER)


# ---------------------------------------------------------------------------
# Species and electrons
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Species:
    key: str
    element: str
    charge: int
    tex: str
    spoken: str

    @property
    def kind(self) -> str:
        return ORDERING[self.element]

    @property
    def electrons(self) -> int:
        """Electrons drawn on the diagram (all of them for 1s molecules,
        valence only for the second period, where the 1s cores cancel)."""
        return 2 * VALENCE_ELECTRONS[self.element] - self.charge


SPECIES: dict[str, Species] = {s.key: s for s in (
    Species("H2+", "H", 1, r"\mathrm{H_2^{+}}", "H two plus"),
    Species("H2", "H", 0, r"\mathrm{H_2}", "H two"),
    Species("He2+", "He", 1, r"\mathrm{He_2^{+}}", "He two plus"),
    Species("He2", "He", 0, r"\mathrm{He_2}", "He two"),
    Species("B2", "B", 0, r"\mathrm{B_2}", "B two"),
    Species("C2", "C", 0, r"\mathrm{C_2}", "C two"),
    Species("N2", "N", 0, r"\mathrm{N_2}", "N two"),
    Species("O2", "O", 0, r"\mathrm{O_2}", "O two"),
    Species("F2", "F", 0, r"\mathrm{F_2}", "F two"),
    Species("Ne2", "Ne", 0, r"\mathrm{Ne_2}", "Ne two"),
    Species("O2+", "O", 1, r"\mathrm{O_2^{+}}", "O two plus"),
    Species("O2-", "O", -1, r"\mathrm{O_2^{-}}", "O two minus"),
    Species("O2 2-", "O", -2, r"\mathrm{O_2^{2-}}", "O two two minus"),
)}


def species(key: str) -> Species:
    return SPECIES[key]


@dataclass(frozen=True)
class Placement:
    level: str      # MO level key
    orbital: int    # which orbital of a degenerate set (0 or 1 for pi)
    spin: int       # +1 up, -1 down


def placements(dia: Diagram, n: int) -> list[Placement]:
    """Place n electrons: lowest level first (Aufbau); within a degenerate set
    one spin-up electron per orbital before any pairing (Hund); never more
    than two, of opposite spin, per orbital (Pauli)."""
    if n < 0:
        raise ValueError("negative electron count")
    out: list[Placement] = []
    for level in dia.ordered():
        slots = [(i, 1) for i in range(level.degeneracy)] + [(i, -1) for i in range(level.degeneracy)]
        for orbital, spin in slots:
            if len(out) == n:
                return out
            out.append(Placement(level.key, orbital, spin))
    if len(out) < n:
        raise ValueError(f"{n} electrons do not fit in a {dia.kind} diagram")
    return out


def atomic_placements(dia: Diagram, n: int) -> list[tuple[str, int, int]]:
    """Electrons on one isolated atom's valence levels, by the same rules:
    (AO key, orbital, spin). Used to start electrons on the atoms' sides."""
    out: list[tuple[str, int, int]] = []
    for level in sorted(dia.ao, key=lambda a: a.energy):
        slots = [(i, 1) for i in range(level.degeneracy)] + [(i, -1) for i in range(level.degeneracy)]
        for orbital, spin in slots:
            if len(out) == n:
                return out
            out.append((level.key, orbital, spin))
    if len(out) < n:
        raise ValueError("too many electrons for one atom's valence levels")
    return out


@dataclass(frozen=True)
class Filling:
    species: Species
    diagram: Diagram
    electrons: tuple[Placement, ...] = field(default_factory=tuple)

    def occupancy(self) -> dict[str, list[int]]:
        """Electrons per orbital, for every level: e.g. {'p2p*': [1, 1], ...}."""
        table = {level.key: [0] * level.degeneracy for level in self.diagram.mo}
        for p in self.electrons:
            table[p.level][p.orbital] += 1
        return table

    @property
    def bonding(self) -> int:
        return sum(1 for p in self.electrons if self.diagram.level(p.level).bonding)

    @property
    def antibonding(self) -> int:
        return len(self.electrons) - self.bonding

    @property
    def bond_order(self) -> float:
        return (self.bonding - self.antibonding) / 2

    @property
    def unpaired(self) -> int:
        return sum(1 for counts in self.occupancy().values() for c in counts if c == 1)

    def unpaired_placements(self) -> list[Placement]:
        occ = self.occupancy()
        return [p for p in self.electrons if occ[p.level][p.orbital] == 1]

    @property
    def magnetism(self) -> str:
        return "paramagnetic" if self.unpaired else "diamagnetic"

    def configuration_tex(self) -> list[str]:
        """('(\\sigma_{2s})^{2}', ...) in energy order, one string per occupied level."""
        occ = self.occupancy()
        parts = []
        for level in self.diagram.ordered():
            count = sum(occ[level.key])
            if count:
                parts.append(f"({level.tex})^{{{count}}}")
        return parts


def fill(key: str, *, kind: str | None = None) -> Filling:
    """Fill a species' diagram (optionally forcing an ordering)."""
    s = species(key)
    dia = diagram(kind or s.kind)
    return Filling(s, dia, tuple(placements(dia, s.electrons)))


def bond_order(key: str) -> float:
    return fill(key).bond_order


def unpaired(key: str) -> int:
    return fill(key).unpaired


def spoken_bond_order(value: float) -> str:
    """0.5 -> 'one half', 2.5 -> 'two and a half', 3 -> 'three'."""
    words = ["zero", "one", "two", "three", "four"]
    whole = int(value)
    if abs(value - whole) < 1e-9:
        return words[whole]
    if whole == 0:
        return "one half"
    return f"{words[whole]} and a half"


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    for kind in ("1s", "mixed", "unmixed"):
        dia = diagram(kind)
        check(dia.orbital_count == dia.atomic_orbital_count, f"{kind}: orbitals in = orbitals out")
        for level in dia.mo:
            # s-p mixing deliberately breaks the symmetric picture for the
            # sigma levels of B2, C2 and N2; the pi pair keeps it.
            if level.bonding and (kind != "mixed" or level.key == "p2p"):
                partner = dia.level(level.key + "*")
                parent = (dia.ao_level(level.parent)).energy
                check(level.energy < parent < partner.energy, f"{kind}: {level.key} straddles its AO")
                check(partner.energy - parent > parent - level.energy, f"{kind}: antibonding rises more ({level.key})")
    mixed, unmixed = diagram("mixed"), diagram("unmixed")
    check(mixed.level("p2p").energy < mixed.level("s2p").energy, "mixed: pi below sigma 2p")
    check(unmixed.level("s2p").energy < unmixed.level("p2p").energy, "unmixed: sigma 2p below pi")
    m = crossing_mixing()
    halfway = diagram("unmixed", mixing=m)
    check(abs(halfway.level("s2p").energy - halfway.level("p2p").energy) < 1e-9, "crossing mixing")
    # Hund: two electrons into an empty degenerate pair take one orbital each.
    o2 = fill("O2")
    check(o2.occupancy()["p2p*"] == [1, 1], "O2 pi* is singly occupied twice")
    check([p.spin for p in o2.electrons if p.level == "p2p*"] == [1, 1], "O2 pi* spins parallel")
    # Pauli: no orbital ever holds more than two, and a pair has opposite spins.
    for key in SPECIES:
        f = fill(key)
        for level, counts in f.occupancy().items():
            check(all(c <= 2 for c in counts), f"{key}: Pauli in {level}")
        for level in f.diagram.mo:
            for orbital in range(level.degeneracy):
                spins = [p.spin for p in f.electrons if p.level == level.key and p.orbital == orbital]
                check(len(spins) < 2 or sorted(spins) == [-1, 1], f"{key}: opposite spins in {level.key}")
    # Each electron added to O2 lands in pi*.
    previous = fill("O2+")
    for key in ("O2", "O2-", "O2 2-"):
        current = fill(key)
        check(current.electrons[-1].level == "p2p*", f"{key}: the extra electron is antibonding")
        check(current.bond_order == previous.bond_order - 0.5, f"{key}: bond order falls by a half")
        previous = current
    # The film's ordering tags.
    check(fill("N2").diagram.kind == "mixed" and fill("O2").diagram.kind == "unmixed", "N2/O2 orderings")
    check(spoken_bond_order(0.5) == "one half" and spoken_bond_order(2.5) == "two and a half", "spoken orders")
    check(len(atomic_placements(diagram("mixed"), 5)) == 5, "atomic placements")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("MO model check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print("MO model check passed: orbital counts, orderings, Aufbau/Pauli/Hund filling, bond orders.")
    for key in SPECIES:
        f = fill(key)
        print(f"  {key:6s} {f.diagram.kind:8s} e={len(f.electrons):2d}  BO={f.bond_order:3.1f}  unpaired={f.unpaired}"
              f"  {f.magnetism}")
