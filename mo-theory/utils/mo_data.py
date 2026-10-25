"""Measured data, with sources, and a check on every spoken claim.

Sources
-------
* **Bond lengths and dissociation energies** of neutral diatomics and O2+:
  K. P. Huber and G. Herzberg, *Constants of Diatomic Molecules* (1979), as
  tabulated in the NIST Chemistry WebBook and CCCBDB. D0 is the energy to
  separate the ground-state molecule into atoms; values are rounded.
* **H2+**: R_e = 2.00 bohr (106 pm) and D_e = 2.79 eV are the exact
  (Born-Oppenheimer) values for the one-electron molecule; D0 = 2.65 eV.
* **Superoxide and peroxide** O-O distances depend on the salt; typical
  values (KO2 about 128-133 pm, Na2O2 about 149 pm) follow Housecroft and
  Sharpe, *Inorganic Chemistry*, and Miessler, Fischer and Tarr,
  *Inorganic Chemistry*, Table 5.1. The film shows them as approximate.
* **Average valence-orbital energies** (2s and 2p, eV): Miessler, Fischer and
  Tarr, *Inorganic Chemistry*, 5th ed., Table 5.2 (after J. B. Mann, T. L. Meek
  and L. C. Allen, J. Am. Chem. Soc. 122, 2780 (2000)).
* **The helium dimer**: R. E. Grisenti et al., Phys. Rev. Lett. 85, 2284
  (2000): mean separation 52 +- 4 angstrom, binding about 1.1 mK.
* **Magnetism and ground states**: O2 (triplet, two unpaired electrons), B2
  (triplet), C2, N2 and F2 (singlets): OpenStax *Chemistry 2e*, section 8.4,
  and Huber and Herzberg.

Nothing in this module imports Manim. ``python -m utils.mo_data`` verifies
that the MO model reproduces every literature bond order and magnetic
verdict, that the data really show every trend the narration states, and that
each phrase quoted in ``SPOKEN_CLAIMS`` still appears in ``narration.py``.
"""

from __future__ import annotations

from utils import mo_models as mo
from utils import physics_models as pm

# ---------------------------------------------------------------------------
# Measured values
# ---------------------------------------------------------------------------

BOND_LENGTH_PM: dict[str, float] = {
    "H2+": 106.0, "H2": 74.1, "B2": 159.0, "C2": 124.3, "N2": 109.8, "O2": 120.7, "F2": 141.2,
    "O2+": 111.6,
}
# Salt-dependent ions: a representative value and the range it comes from.
ION_BOND_LENGTH_PM: dict[str, tuple[float, tuple[float, float]]] = {
    "O2-": (130.0, (128.0, 133.0)),
    "O2 2-": (149.0, (148.0, 150.0)),
}

DISSOCIATION_EV: dict[str, float] = {
    "H2+": 2.65, "H2": 4.48, "B2": 3.0, "C2": 6.2, "N2": 9.76, "O2": 5.12, "F2": 1.60, "O2+": 6.66,
}

H2PLUS_EXACT_RE_BOHR = 2.00
H2PLUS_EXACT_DE_EV = 2.79

HE2_SEPARATION_PM = 5200.0    # 52 angstrom (Grisenti et al. 2000)
HE2_BINDING_MK = 1.1

ORBITAL_ENERGY_EV: dict[str, tuple[float, float]] = {    # (2s, 2p), average valence-orbital energies
    "B": (-14.05, -8.30), "C": (-19.43, -10.66), "N": (-25.56, -13.18), "O": (-32.38, -15.85), "F": (-40.17, -18.65),
}

# The textbook verdicts the MO model must reproduce: (bond order, unpaired electrons).
LITERATURE: dict[str, tuple[float, int]] = {
    "H2+": (0.5, 1), "H2": (1.0, 0), "He2+": (0.5, 1), "He2": (0.0, 0),
    "B2": (1.0, 2), "C2": (2.0, 0), "N2": (3.0, 0), "O2": (2.0, 2), "F2": (1.0, 0),
    "O2+": (2.5, 1), "O2-": (1.5, 1), "O2 2-": (1.0, 0),
}


def bond_length(key: str) -> float:
    if key in BOND_LENGTH_PM:
        return BOND_LENGTH_PM[key]
    return ION_BOND_LENGTH_PM[key][0]


def gap_ev(symbol: str) -> float:
    s, p = ORBITAL_ENERGY_EV[symbol]
    return p - s


def display_number(value: float) -> str:
    """A bond order as shown on screen: '0.5', '2.5', '3'."""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.1f}"


# ---------------------------------------------------------------------------
# Spoken claims
# ---------------------------------------------------------------------------

def _bo(key: str) -> str:
    return mo.spoken_bond_order(mo.bond_order(key))


def _words(n: int) -> str:
    return ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
            "twelve", "thirteen", "fourteen"][n]


def _filling(key: str) -> mo.Filling:
    return mo.fill(key)


SPOKEN_CLAIMS: list[tuple[str, str, bool, str]] = [
    ("01", "every single electron sits in a pair", True, "Lewis O=O pairs everything (shown, not modelled)"),
    ("01", "the signature of unpaired electrons", mo.fill("O2").magnetism == "paramagnetic", "O2 paramagnetic"),
    ("04", "Two atomic orbitals went in. Two molecular orbitals came out",
     mo.diagram("1s").orbital_count == mo.diagram("1s").atomic_orbital_count == 2, "2 AOs -> 2 MOs"),
    ("04", "Combine four atomic orbitals, and you get four molecular orbitals",
     len(pm.huckel_chain(4)[0]) == 4, "4 AOs -> 4 MOs"),
    ("06", "the rise is a little larger than the drop",
     all((d.level(l.key + "*").energy - d.ao_level(l.parent).energy) > (d.ao_level(l.parent).energy - l.energy)
         for d in (mo.diagram("1s"),) for l in d.mo if l.bonding), "antibonding rises more (diagram)"),
    ("07", "A bond order of one half", _bo("H2+") == "one half", "H2+"),
    ("07", "One minus zero, over two",
     (_filling("H2+").bonding, _filling("H2+").antibonding) == (1, 0), "H2+ counts"),
    ("07", "The exact solution has a deeper one", H2PLUS_EXACT_DE_EV > pm.h2plus_minimum()[1], "H2+ exact vs LCAO"),
    ("08", "Bond order: two minus zero, over two. One.", _bo("H2") == "one", "H2"),
    ("08", "shorter, and much stronger",
     BOND_LENGTH_PM["H2"] < BOND_LENGTH_PM["H2+"] and DISSOCIATION_EV["H2"] > 1.5 * DISSOCIATION_EV["H2+"], "H2 vs H2+"),
    ("08", "not quite twice as strong",
     1.5 < DISSOCIATION_EV["H2"] / DISSOCIATION_EV["H2+"] < 2.0, "D0 ratio H2/H2+"),
    ("08", "hydrogen is diamagnetic", mo.fill("H2").magnetism == "diamagnetic", "H2 diamagnetic"),
    ("09", "Four electrons in total", mo.species("He2").electrons == 4, "He2 electrons"),
    ("09", "Two minus two, over two", (_filling("He2").bonding, _filling("He2").antibonding) == (2, 2), "He2 counts"),
    ("09", "Bond order zero.", _bo("He2") == "zero", "He2"),
    ("09", "Bond order one half. He two plus", _bo("He2+") == "one half", "He2+"),
    ("09", "H two plus, one half. H two, one. He two plus, one half. He two, zero.",
     [_bo(k) for k in ("H2+", "H2", "He2+", "He2")] == ["one half", "one", "one half", "zero"], "line-up"),
    ("09", "more than fifty times farther apart",
     HE2_SEPARATION_PM / BOND_LENGTH_PM["H2"] > 50, "He2 separation vs H2"),
    ("11", "Six p orbitals in, six molecular orbitals out",
     sum(l.degeneracy for l in mo.diagram("unmixed").mo if l.parent == "2p") == 6, "6 from 2p"),
    ("12", "Eight valence atomic orbitals. Eight molecular orbitals",
     mo.diagram("mixed").orbital_count == mo.diagram("mixed").atomic_orbital_count == 8, "8 -> 8"),
    ("13", "for boron, carbon and nitrogen, the pi pair sits below sigma two p",
     all(mo.ORDERING[e] == "mixed" for e in "BCN"), "mixed ordering"),
    ("13", "for oxygen and fluorine, sigma two p drops below the pi pair",
     all(mo.ORDERING[e] == "unmixed" for e in "OF"), "unmixed ordering"),
    ("13", "Across the period, that gap grows",
     gap_ev("B") < gap_ev("C") < gap_ev("N") < gap_ev("O") < gap_ev("F"), "2s-2p gap trend"),
    ("13", "The crossing happens between nitrogen and oxygen",
     mo.mixing_from_gap(gap_ev("N")) > mo.crossing_mixing() > mo.mixing_from_gap(gap_ev("O")), "toy crossing"),
    ("14", "Five plus five: ten", mo.species("N2").electrons == 10, "N2 electrons"),
    ("14", "Two, plus four, plus two: eight. Antibonding: two",
     (_filling("N2").bonding, _filling("N2").antibonding) == (8, 2), "N2 counts"),
    ("14", "Bond order three", _bo("N2") == "three", "N2"),
    ("14", "Every orbital that's occupied holds a pair", _filling("N2").unpaired == 0, "N2 paired"),
    ("15", "among the strongest bonds between two atoms",
     DISSOCIATION_EV["N2"] == max(DISSOCIATION_EV.values()), "N2 strongest in the film's table"),
    ("15", "Paired electrons make nitrogen diamagnetic", mo.fill("N2").magnetism == "diamagnetic", "N2 dia"),
    ("16", "Twelve valence electrons", mo.species("O2").electrons == 12, "O2 electrons"),
    ("16", "That's ten so far, the same ten as nitrogen", mo.species("N2").electrons == 10, "ten"),
    ("16", "Two unpaired electrons, in two antibonding pi star orbitals",
     _filling("O2").unpaired == 2 and all(p.level == "p2p*" for p in _filling("O2").unpaired_placements()), "O2 pi*"),
    ("16", "Oxygen is paramagnetic", mo.fill("O2").magnetism == "paramagnetic", "O2 para"),
    ("17", "two, two, and four. Eight", _filling("O2").bonding == 8, "O2 bonding"),
    ("17", "Eight minus four, over two. Two.", _bo("O2") == "two", "O2"),
    ("18", "Antibonding: now three", _filling("O2+").antibonding == 3, "O2+ antibonding"),
    ("18", "Two and a half", _bo("O2+") == "two and a half", "O2+"),
    ("18", "shorter and stronger than in oxygen itself",
     BOND_LENGTH_PM["O2+"] < BOND_LENGTH_PM["O2"] and DISSOCIATION_EV["O2+"] > DISSOCIATION_EV["O2"], "O2+ data"),
    ("18", "with one unpaired electron instead of two", _filling("O2+").unpaired == 1, "O2+ unpaired"),
    ("19", "Antibonding electrons: five", _filling("O2-").antibonding == 5, "O2- antibonding"),
    ("19", "One and a half", _bo("O2-") == "one and a half", "O2-"),
    ("19", "Bond order one", _bo("O2 2-") == "one", "O2 2-"),
    ("19", "bond stretches as the bond order falls",
     [bond_length(k) for k in ("O2+", "O2", "O2-", "O2 2-")] == sorted(bond_length(k) for k in ("O2+", "O2", "O2-", "O2 2-"))
     and [mo.bond_order(k) for k in ("O2+", "O2", "O2-", "O2 2-")] == [2.5, 2.0, 1.5, 1.0], "length trend"),
    ("19", "One unpaired electron, then two, then one, then none",
     [mo.unpaired(k) for k in ("O2+", "O2", "O2-", "O2 2-")] == [1, 2, 1, 0], "unpaired trend"),
    ("20", "six in total", mo.species("B2").electrons == 6, "B2 electrons"),
    ("20", "Bond order one, and two unpaired electrons. B two is paramagnetic",
     _bo("B2") == "one" and mo.unpaired("B2") == 2, "B2"),
    ("20", "fourteen in total", mo.species("F2").electrons == 14, "F2 electrons"),
    ("20", "Eight bonding, six antibonding. Bond order one.",
     (_filling("F2").bonding, _filling("F2").antibonding) == (8, 6) and _bo("F2") == "one", "F2"),
    ("20", "Boron, one. Nitrogen, three. Oxygen, two. Fluorine, one.",
     [_bo(k) for k in ("B2", "N2", "O2", "F2")] == ["one", "three", "two", "one"], "line-up"),
    ("21", "Bonding electrons: six. Antibonding: two. Bond order two.",
     (_filling("C2").bonding, _filling("C2").antibonding) == (6, 2) and _bo("C2") == "two", "C2"),
    ("21", "so it's diamagnetic", mo.fill("C2").magnetism == "diamagnetic", "C2 dia"),
]


def verify() -> list[str]:
    from narration import SCRIPT

    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    def text(key: str) -> str:
        return " ".join(line for _, line in SCRIPT[key])

    for key, phrase, agrees, label in SPOKEN_CLAIMS:
        check(phrase in text(key), f"chapter {key} no longer says {phrase!r} ({label})")
        check(bool(agrees), f"chapter {key} says {phrase!r} but the model or data disagree ({label})")
    for key, (order, lonely) in LITERATURE.items():
        f = mo.fill(key)
        check(f.bond_order == order, f"{key}: model bond order {f.bond_order} vs literature {order}")
        check(f.unpaired == lonely, f"{key}: model unpaired {f.unpaired} vs literature {lonely}")
    # Bond order and measured length for the second-period molecules: higher
    # order, shorter bond, within this family.
    family = ("B2", "C2", "N2", "O2", "F2")
    by_order = sorted(family, key=lambda k: mo.bond_order(k))
    check(BOND_LENGTH_PM[by_order[-1]] == min(BOND_LENGTH_PM[k] for k in family), "highest order, shortest bond")
    check(display_number(0.5) == "0.5" and display_number(3.0) == "3", "display numbers")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Data check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print(f"Data check passed: {len(SPOKEN_CLAIMS)} spoken claims match the MO model and measured data, and the")
    print(f"model reproduces all {len(LITERATURE)} literature bond orders and unpaired-electron counts.")
