"""Measured bond properties, with sources, and a check on every spoken claim.

Values are rounded to the nearest whole unit (two decimals for
electronegativity). Two kinds of number appear, and the film keeps them apart:

* **Properties of particular molecules** (H2, Cl2, HCl, F2, O2, N2): measured
  equilibrium bond lengths r_e (NIST Computational Chemistry Comparison and
  Benchmark Database, from Huber & Herzberg) and bond dissociation enthalpies
  at 298 K (CRC Handbook of Chemistry and Physics, "Bond Dissociation
  Energies", Luo).
* **Average bond enthalpies** for carbon-carbon bonds, which vary a little
  from molecule to molecule; the film uses the common general-chemistry table
  (Brown, LeMay et al., *Chemistry: The Central Science*, Tables 8.4 and 8.5),
  and says "about".

Ionization energy comes from the NIST Atomic Spectra Database; chlorine
electron affinity comes from the NIST Chemistry WebBook (converted with 1 eV = 96.485 kJ/mol). Lattice energies are the
Born-Haber values quoted in the CRC Handbook; published tables differ by one
or two kJ/mol depending on convention, so the narration says "about".

Nothing in this module imports Manim. Run ``python -m utils.bond_data`` to
verify that the data really show every pattern the narration states, and
that each number spoken in ``narration.py`` matches the data.
"""

from __future__ import annotations

from utils import bond_models as bm

# ---------------------------------------------------------------------------
# Molecules: r_e in pm, bond dissociation enthalpy at 298 K in kJ/mol
# ---------------------------------------------------------------------------

BOND_LENGTH_PM: dict[str, int] = {
    "H-H": 74,      # 74.14
    "H-Cl": 127,    # 127.46
    "F-F": 141,     # 141.19
    "Cl-Cl": 199,   # 198.8
    "O=O": 121,     # 120.75
    "N#N": 110,     # 109.77
    # Average values, carbon-carbon bonds in typical molecules (ethane, ethene, ethyne).
    "C-C": 154,
    "C=C": 134,
    "C#C": 120,
}

BOND_ENTHALPY_KJ: dict[str, int] = {
    "H-H": 436,     # 435.8
    "H-Cl": 432,    # 431.6
    "F-F": 159,     # 158.7
    "Cl-Cl": 243,   # 242.6
    "O=O": 498,     # 498.4
    "N#N": 945,     # 945.3
    "C-C": 348,
    "C=C": 614,
    "C#C": 839,
}

BOND_ORDER: dict[str, int] = {
    "H-H": 1, "H-Cl": 1, "F-F": 1, "Cl-Cl": 1, "O=O": 2, "N#N": 3, "C-C": 1, "C=C": 2, "C#C": 3,
}

# Morse width parameter for H2, a = omega_e * sqrt(mu / 2 D_e) = 1.94 per angstrom
# (omega_e = 4401 cm^-1, D_e = 4.75 eV). The plotted curve uses the measured
# bond length and bond enthalpy above for its minimum; the true well depth
# D_e ~ 458 kJ/mol is a little deeper because the molecule always keeps some
# zero-point vibration. The curves are labelled as a model on screen.
MORSE_A_PER_PM: dict[str, float] = {"H-H": 0.0194}

# 2 H2 + ... Standard enthalpy of formation of HCl(g), for the bond-energy check.
HCL_FORMATION_KJ = -92.31     # per mole HCl, CODATA

# ---------------------------------------------------------------------------
# Ionic bonding
# ---------------------------------------------------------------------------

IONIZATION_KJ: dict[str, int] = {"Na": 496}          # 5.139 eV
ELECTRON_AFFINITY_KJ: dict[str, int] = {"Cl": 349}   # 3.613 eV, energy released on gaining one electron
LATTICE_KJ: dict[str, int] = {"NaCl": 787, "MgO": 3791}
NA_CL_DISTANCE_PM: dict[str, int] = {"crystal": 282, "gas molecule": 236}  # a/2 = 564/2; NaCl(g) r_e
MGO_MELTING_C = 2852

# ---------------------------------------------------------------------------
# Electronegativity (Pauling) and molecular shape
# ---------------------------------------------------------------------------

ELECTRONEGATIVITY: dict[str, float] = {
    "H": 2.20, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98,
    "Na": 0.93, "Mg": 1.31, "Cl": 3.16, "Cu": 1.90,
}

BOND_ANGLE_DEG: dict[str, float] = {"H2O": 104.5, "CO2": 180.0}
MOLECULE_BOND_PM: dict[str, int] = {"O-H in H2O": 96, "C=O in CO2": 116}

VALENCE_ELECTRONS: dict[str, int] = {"H": 1, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Cl": 7, "Ne": 8, "Ar": 8, "S": 6}


# ---------------------------------------------------------------------------
# Derived numbers (computed, never typed into a scene)
# ---------------------------------------------------------------------------


def transfer_cost() -> int:
    """Na(g) + Cl(g) -> Na+(g) + Cl-(g): ionization paid, electron affinity returned."""
    return IONIZATION_KJ["Na"] - ELECTRON_AFFINITY_KJ["Cl"]


def salt_from_gas_atoms() -> int:
    """Na(g) + Cl(g) -> NaCl(s): the transfer bill, then the lattice paying it."""
    return transfer_cost() - LATTICE_KJ["NaCl"]


def h2_cl2_ledger() -> tuple[int, int, int]:
    """H2 + Cl2 -> 2 HCl from bond enthalpies: (broken, formed, net)."""
    broken = BOND_ENTHALPY_KJ["H-H"] + BOND_ENTHALPY_KJ["Cl-Cl"]
    formed = 2 * BOND_ENTHALPY_KJ["H-Cl"]
    return broken, formed, broken - formed


def ion_pair_estimate(distance_pm: float) -> float:
    """Point-charge Coulomb energy of one Na+ Cl- pair, kJ/mol (negative = bound)."""
    return bm.coulomb_kj(+1, -1, distance_pm)


def delta_en(a: str, b: str) -> float:
    return abs(ELECTRONEGATIVITY[a] - ELECTRONEGATIVITY[b])


# ---------------------------------------------------------------------------
# Spoken numbers
# ---------------------------------------------------------------------------

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen "
         "fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def spoken(n: int) -> str:
    """British spoken form: 154 -> 'one hundred and fifty-four'."""
    if n < 0:
        return "minus " + spoken(-n)
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + (f"-{_ONES[ones]}" if ones else "")
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        return f"{_ONES[hundreds]} hundred" + (f" and {spoken(rest)}" if rest else "")
    thousands, rest = divmod(n, 1000)
    if rest == 0:
        return f"{spoken(thousands)} thousand"
    if rest < 100:
        return f"{spoken(thousands)} thousand and {spoken(rest)}"
    return f"{spoken(thousands)} thousand {spoken(rest)}"


# (chapter, value, label): the narration of that chapter must say the number.
SPOKEN_VALUES: list[tuple[str, int, str]] = [
    ("04", BOND_LENGTH_PM["H-H"], "H2 bond length"),
    ("05", BOND_ENTHALPY_KJ["H-H"], "H2 bond enthalpy"),
    ("05", h2_cl2_ledger()[0], "bonds broken in H2 + Cl2"),
    ("05", h2_cl2_ledger()[1], "bonds formed in 2 HCl"),
    ("05", -h2_cl2_ledger()[2], "heat released by H2 + Cl2 -> 2 HCl"),
    ("10", IONIZATION_KJ["Na"], "Na first ionization"),
    ("10", ELECTRON_AFFINITY_KJ["Cl"], "Cl electron affinity"),
    ("10", transfer_cost(), "gas-phase transfer cost"),
    ("11", LATTICE_KJ["NaCl"], "NaCl lattice energy"),
    ("14", BOND_LENGTH_PM["C-C"], "C-C length"),
    ("14", BOND_ENTHALPY_KJ["C-C"], "C-C enthalpy"),
    ("14", BOND_LENGTH_PM["C=C"], "C=C length"),
    ("14", BOND_ENTHALPY_KJ["C=C"], "C=C enthalpy"),
    ("14", BOND_LENGTH_PM["C#C"], "C#C length"),
    ("14", BOND_ENTHALPY_KJ["C#C"], "C#C enthalpy"),
    ("14", BOND_LENGTH_PM["F-F"], "F-F length"),
    ("14", BOND_LENGTH_PM["Cl-Cl"], "Cl-Cl length"),
    ("14", BOND_ENTHALPY_KJ["F-F"], "F-F enthalpy"),
    ("14", BOND_ENTHALPY_KJ["Cl-Cl"], "Cl-Cl enthalpy"),
]

# Phrases whose truth is a comparison rather than one rounded number.
SPOKEN_PHRASES: list[tuple[str, str, bool, str]] = [
    ("06", "Hydrogen has one valence electron. Carbon has four. Oxygen, six. Chlorine, seven",
     [VALENCE_ELECTRONS[s] for s in ("H", "C", "O", "Cl")] == [1, 4, 6, 7], "valence counts"),
    ("07", "Oxygen has six valence electrons", VALENCE_ELECTRONS["O"] == 6, "O valence"),
    ("07", "Nitrogen has five", VALENCE_ELECTRONS["N"] == 5, "N valence"),
    ("11", "one point seven five", round(bm.madelung_rock_salt(), 2) == 1.75, "rock-salt Madelung constant"),
    ("11", "almost five times", 4.5 < LATTICE_KJ["MgO"] / LATTICE_KJ["NaCl"] < 5.0, "MgO / NaCl lattice energy"),
    ("11", "above two thousand eight hundred degrees", 2800 < MGO_MELTING_C < 2900, "MgO melting point"),
    ("12", "about three point two", round(ELECTRONEGATIVITY["Cl"], 1) == 3.2, "Cl electronegativity"),
    ("12", "about two point two", round(ELECTRONEGATIVITY["H"], 1) == 2.2, "H electronegativity"),
    ("12", "differ by more than two", 2.0 < delta_en("Na", "Cl") < 2.5, "Na-Cl electronegativity difference"),
    ("15", "Boron brings only three valence electrons", VALENCE_ELECTRONS["B"] == 3, "B valence"),
    ("15", "twelve electrons around it", 6 * 2 == 12, "SF6 Lewis count (six bonding pairs)"),
    ("17", "one hundred and four and a half degrees", BOND_ANGLE_DEG["H2O"] == 104.5, "water bond angle"),
]


def verify() -> list[str]:
    from narration import SCRIPT

    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    def text(key: str) -> str:
        return " ".join(line for _, line in SCRIPT[key])

    # Bond order: within carbon-carbon bonds, more pairs -> shorter and stronger.
    cc = ("C-C", "C=C", "C#C")
    lengths = [BOND_LENGTH_PM[b] for b in cc]
    energies = [BOND_ENTHALPY_KJ[b] for b in cc]
    check(lengths == sorted(lengths, reverse=True), "C-C, C=C, C#C must get shorter")
    check(energies == sorted(energies), "C-C, C=C, C#C must get stronger")
    check(energies[1] < 2 * energies[0] and energies[2] < 3 * energies[0], "multiple bonds must not scale linearly")
    check(energies[1] - energies[0] < energies[0] and energies[2] - energies[1] < energies[0],
          "average multiple-bond enthalpies are not integer multiples of the single-bond average")
    # Shorter is not always stronger: F2 vs Cl2.
    check(BOND_LENGTH_PM["F-F"] < BOND_LENGTH_PM["Cl-Cl"], "F-F must be shorter than Cl-Cl")
    check(BOND_ENTHALPY_KJ["F-F"] < BOND_ENTHALPY_KJ["Cl-Cl"], "F-F must be weaker than Cl-Cl")
    # H2 + Cl2 -> 2 HCl: bond enthalpies reproduce the measured heat within a few kJ.
    broken, formed, net = h2_cl2_ledger()
    check(net < 0, "H2 + Cl2 -> 2 HCl must release energy")
    check(abs(net - 2 * HCL_FORMATION_KJ) < 3, f"bond-energy estimate {net} vs measured {2 * HCL_FORMATION_KJ:.1f}")
    # Ionic: the transfer alone is uphill, the lattice pays.
    check(transfer_cost() > 0, "gas-phase electron transfer must cost energy")
    check(salt_from_gas_atoms() < 0, "the lattice must more than pay the transfer")
    check(-ion_pair_estimate(NA_CL_DISTANCE_PM["gas molecule"]) > transfer_cost(),
          "one ion pair's attraction must exceed the transfer cost")
    check(abs(bm.madelung_rock_salt() - 1.7476) < 2e-3, f"Madelung constant {bm.madelung_rock_salt():.4f}")
    # Polarity: H2 symmetric, HCl in between, NaCl far apart.
    check(delta_en("H", "H") == 0 < delta_en("H", "Cl") < delta_en("Na", "Cl"), "electronegativity ladder")
    # N2 is among the strongest bonds the film names; O2 sits between.
    check(BOND_ENTHALPY_KJ["H-H"] < BOND_ENTHALPY_KJ["O=O"] < BOND_ENTHALPY_KJ["N#N"], "bond-order ladder H2 < O2 < N2")
    check(BOND_LENGTH_PM["N#N"] < BOND_LENGTH_PM["O=O"], "N#N must be shorter than O=O")
    # The Morse model reproduces the H2 minimum it is built on.
    r_min = bm.morse_minimum(BOND_ENTHALPY_KJ["H-H"], BOND_LENGTH_PM["H-H"], MORSE_A_PER_PM["H-H"])
    check(abs(r_min - BOND_LENGTH_PM["H-H"]) < 0.5, f"Morse minimum at {r_min:.1f} pm")

    for key, value, label in SPOKEN_VALUES:
        check(spoken(value) in text(key), f"chapter {key} should say {spoken(value)!r} ({label} = {value})")
    for key, phrase, agrees, label in SPOKEN_PHRASES:
        check(phrase in text(key), f"chapter {key} no longer says {phrase!r} ({label})")
        check(agrees, f"chapter {key} says {phrase!r} but the data disagree ({label})")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Data check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    broken, formed, net = h2_cl2_ledger()
    print(f"Data check passed: {len(SPOKEN_VALUES) + len(SPOKEN_PHRASES)} spoken claims match the data;")
    print(f"C-C < C=C < C#C in strength, F-F shorter yet weaker than Cl-Cl, H2 + Cl2 ledger {broken} - {formed} = {net},")
    print(f"transfer +{transfer_cost()}, salt from gas atoms {salt_from_gas_atoms()}, "
          f"Madelung {bm.madelung_rock_salt():.4f}.")
