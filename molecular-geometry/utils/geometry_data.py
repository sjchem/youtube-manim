"""Measured molecular geometry, with sources, and a check on every spoken claim.

Sources
-------
* **Bond angles and lengths** of gas-phase molecules: NIST Computational
  Chemistry Comparison and Benchmark Database (CCCBDB), experimental geometry
  listings, which cite microwave and electron-diffraction studies; cross-checked
  against the CRC Handbook of Chemistry and Physics, "Structure of Free
  Molecules in the Gas Phase". Values are rounded to 0.1 degree and 1 pm.
  Phosphorus pentachloride is quoted for the gas phase (the solid is ionic,
  [PCl4]+[PCl6]-).
* **Electronegativity**: Pauling scale, as tabulated in the CRC Handbook.
* **Dipole moments** (gas phase, debye): CRC Handbook, "Dipole Moments"
  (after Nelson, Lide and Maryott, NSRDS-NBS 10).

The film never derives a bond angle from VSEPR: VSEPR gives the arrangement
and the trend, and the measured numbers come from this table. Nothing in this
module imports Manim. ``python -m utils.geometry_data`` verifies that the data
really show every pattern the narration states, and that each phrase quoted
in ``SPOKEN_CLAIMS`` still appears in ``narration.py``.
"""

from __future__ import annotations

from math import acos, degrees

# ---------------------------------------------------------------------------
# Measured angles (degrees)
# ---------------------------------------------------------------------------

BOND_ANGLE_DEG: dict[str, float] = {
    "CO2": 180.0,     # O=C=O
    "BF3": 120.0,     # F-B-F
    "SO2": 119.3,     # O-S-O
    "CH4": round(degrees(acos(-1 / 3)), 2),   # H-C-H, exactly tetrahedral by symmetry (109.47)
    "NH3": 106.7,     # H-N-H
    "H2O": 104.5,     # H-O-H (104.48)
    "PF3": 97.8,      # F-P-F
    "XeF2": 180.0,    # F-Xe-F
    "SF6": 90.0,      # F-S-F (cis)
    "XeF4": 90.0,     # F-Xe-F (cis)
    "C2H4": 117.4,    # H-C-H in ethene
}

# Angles in the shapes whose positions are not all equivalent.
SF4_AXIAL_DEG = 173.1          # F(ax)-S-F(ax): bent away from the lone pair
SF4_EQUATORIAL_DEG = 101.6     # F(eq)-S-F(eq): closed from 120
CLF3_AX_EQ_DEG = 87.5          # F(ax)-Cl-F(eq)
BRF3_AX_EQ_DEG = 86.2          # F(ax)-Br-F(eq)
BRF5_APICAL_BASAL_DEG = 84.8   # F(apical)-Br-F(basal)
PCL5_AX_EQ_DEG = 90.0          # D3h symmetry in the gas phase
PCL5_EQ_EQ_DEG = 120.0

# ---------------------------------------------------------------------------
# Measured bond lengths (pm)
# ---------------------------------------------------------------------------

BOND_LENGTH_PM: dict[str, int] = {
    "C=O in CO2": 116,
    "O-H in H2O": 96,
    "C-H in CH4": 109,
    "N-H in NH3": 101,
    "B-F in BF3": 131,
    "S=O in SO2": 143,
    "P-F in PF3": 156,
    "P-Cl axial in PCl5": 214,
    "P-Cl equatorial in PCl5": 202,
    "S-F axial in SF4": 165,
    "S-F equatorial in SF4": 155,
    "Cl-F axial in ClF3": 170,
    "Cl-F equatorial in ClF3": 160,
    "Br-F axial in BrF3": 181,
    "Br-F equatorial in BrF3": 172,
    "Xe-F in XeF2": 198,
    "S-F in SF6": 156,
    "Br-F apical in BrF5": 169,
    "Br-F basal in BrF5": 177,
    "Xe-F in XeF4": 195,
    "H-Cl": 127,
    "C=C in C2H4": 134,
    "C-H in C2H4": 109,
    "O=O": 121,
}

# ---------------------------------------------------------------------------
# Atoms
# ---------------------------------------------------------------------------

VALENCE_ELECTRONS: dict[str, int] = {
    "H": 1, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "P": 5, "S": 6, "Cl": 7, "Br": 7, "Xe": 8,
}

ELECTRONEGATIVITY: dict[str, float] = {
    "H": 2.20, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98,
    "P": 2.19, "S": 2.58, "Cl": 3.16, "Br": 2.96, "Xe": 2.60,
}

DIPOLE_DEBYE: dict[str, float] = {
    "HCl": 1.11,
    "H2O": 1.85,
    "NH3": 1.47,
    "CO2": 0.0,
    "BF3": 0.0,
    "CH4": 0.0,
    "SO2": 1.63,
    "PF3": 1.03,
}

ELEMENT_NAMES: dict[str, str] = {
    "H": "hydrogen", "B": "boron", "C": "carbon", "N": "nitrogen", "O": "oxygen", "F": "fluorine",
    "P": "phosphorus", "S": "sulfur", "Cl": "chlorine", "Br": "bromine", "Xe": "xenon",
}


def lone_pairs_on(central: str, bond_orders) -> int:
    """Lone pairs left on the central atom: (valence electrons - electrons it
    puts into bonds) / 2. For neutral molecules with the usual Lewis structure."""
    used = sum(bond_orders)
    remaining = VALENCE_ELECTRONS[central] - used
    if remaining < 0 or remaining % 2:
        raise ValueError(f"{central} with bond orders {list(bond_orders)} leaves {remaining} electrons")
    return remaining // 2


def spoken_angle(value: float) -> str:
    """'104.5' -> 'one hundred and four point five'; whole numbers drop the point."""
    whole = int(value)
    text = _spoken_int(whole)
    tenths = round((value - whole) * 10)
    if tenths:
        text += f" point {_ONES[tenths]}"
    return text


_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _spoken_int(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + (f"-{_ONES[ones]}" if ones else "")
    hundreds, rest = divmod(n, 100)
    return f"{_ONES[hundreds]} hundred" + (f" and {_spoken_int(rest)}" if rest else "")


TETRAHEDRAL = BOND_ANGLE_DEG["CH4"]

# (chapter, phrase that must appear in its narration, does the data agree?, label)
SPOKEN_CLAIMS: list[tuple[str, str, bool, str]] = [
    ("01", "One hundred and eighty degrees", BOND_ANGLE_DEG["CO2"] == 180, "CO2 angle"),
    ("01", f"about {spoken_angle(BOND_ANGLE_DEG['H2O'])} degrees", True, "H2O angle"),
    ("02", f"about {spoken_angle(round(TETRAHEDRAL, 1))} degrees apart", True, "tetrahedral angle"),
    ("05", f"{spoken_angle(BOND_ANGLE_DEG['BF3'])} degrees from the next", True, "BF3 angle"),
    ("06", "one hundred and nine point four seven degrees", round(TETRAHEDRAL, 2) == 109.47,
     "cube angle, two decimals"),
    ("06", "minus one third", True, "cos of the tetrahedral angle"),
    ("07", "Nitrogen has five valence electrons", VALENCE_ELECTRONS["N"] == 5, "N valence"),
    ("07", f"about {spoken_angle(round(BOND_ANGLE_DEG['NH3']))} degrees", True, "NH3 angle"),
    ("08", "with six valence electrons", VALENCE_ELECTRONS["O"] == 6, "O valence"),
    ("08", f"About {spoken_angle(BOND_ANGLE_DEG['H2O'])} degrees", True, "H2O angle"),
    ("08", "For methane, ammonia and water, it explains the decreasing angles",
     BOND_ANGLE_DEG["CH4"] > BOND_ANGLE_DEG["NH3"] > BOND_ANGLE_DEG["H2O"], "lone-pair trend"),
    ("09", "axial bonds are even a little longer",
     BOND_LENGTH_PM["P-Cl axial in PCl5"] > BOND_LENGTH_PM["P-Cl equatorial in PCl5"], "PCl5 ax vs eq"),
    ("10", "nudges the bonds slightly away", SF4_AXIAL_DEG < 180 and SF4_EQUATORIAL_DEG < 120, "SF4 distortion"),
    ("12", "tilt slightly up, away from it", BRF5_APICAL_BASAL_DEG < 90, "BrF5 distortion"),
    ("15", "close to one hundred and twenty degrees", abs(BOND_ANGLE_DEG["C2H4"] - 120) < 4, "ethene angle"),
    ("17", "Chlorine pulls the shared electrons harder",
     ELECTRONEGATIVITY["Cl"] > ELECTRONEGATIVITY["H"], "Cl vs H"),
    ("17", "Oxygen pulls harder than carbon", ELECTRONEGATIVITY["O"] > ELECTRONEGATIVITY["C"], "O vs C"),
    ("17", "Water is a polar molecule", DIPOLE_DEBYE["H2O"] > 0, "water polar"),
    ("17", "A nonpolar molecule", DIPOLE_DEBYE["CO2"] == 0, "CO2 nonpolar"),
    ("18", "pointing in toward carbon", ELECTRONEGATIVITY["C"] > ELECTRONEGATIVITY["H"], "C-H pull"),
    ("18", "pulling toward nitrogen", ELECTRONEGATIVITY["N"] > ELECTRONEGATIVITY["H"], "N-H pull"),
    ("18", "Ammonia is polar", DIPOLE_DEBYE["NH3"] > 0, "NH3 polar"),
    ("18", "Methane is nonpolar", DIPOLE_DEBYE["CH4"] == 0, "CH4 nonpolar"),
    ("18", "boron trifluoride and methane are symmetric",
     DIPOLE_DEBYE["BF3"] == DIPOLE_DEBYE["CH4"] == DIPOLE_DEBYE["CO2"] == 0, "symmetric cancel"),
    ("19", "just under one hundred and twenty degrees", 115 < BOND_ANGLE_DEG["SO2"] < 120, "SO2 angle"),
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
        check(agrees, f"chapter {key} says {phrase!r} but the data disagree ({label})")
    # Lone pairs from valence electrons (neutral molecules, usual Lewis structures).
    expected = {("N", (1, 1, 1)): 1, ("O", (1, 1)): 2, ("C", (2, 2)): 0, ("B", (1, 1, 1)): 0,
                ("S", (1, 1, 1, 1)): 1, ("Cl", (1, 1, 1)): 2, ("Xe", (1, 1)): 3, ("Br", (1,) * 5): 1,
                ("Xe", (1,) * 4): 2, ("P", (1,) * 5): 0, ("S", (1,) * 6): 0, ("S", (2, 2)): 1}
    for (central, orders), lone in expected.items():
        check(lone_pairs_on(central, orders) == lone, f"{central} with {orders} should keep {lone} lone pairs")
    check(spoken_angle(104.5) == "one hundred and four point five", "spoken angle")
    check(spoken_angle(180) == "one hundred and eighty", "spoken whole angle")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Data check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print(f"Data check passed: {len(SPOKEN_CLAIMS)} spoken claims match the measured data, and every")
    print("central atom's lone pairs follow from its valence electrons.")
