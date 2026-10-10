"""Measured element properties, with sources, and a check on every spoken claim.

The film shows numbers in two ways, and keeps their definitions apart:

* **Textbook teaching values** (NCERT Chemistry Part I, Class XI, Unit 3,
  "Classification of Elements and Periodicity in Properties"): atomic radii,
  ionic radii and electron gain enthalpies quoted in the narration. NCERT's
  atomic radii use the *metallic* radius for metals and the *covalent* radius
  for non-metals, so lithium (152 pm, metallic) and fluorine (64 pm, covalent)
  come from different measurements; chapter 05 says so on screen.
* **One-definition data sets** for the heat maps, so each map uses a consistent property definition
  (some compiled values are estimates): single-bond covalent radii (Cordero et al. 2008),
  first ionization energies (NIST Atomic Spectra Database), Pauling
  electronegativities, and electron gain enthalpies from electron affinities.

Values are rounded to the nearest whole unit (two decimals for
electronegativity). Nothing in this module imports Manim.

Run ``python -m utils.element_data`` to verify that the data really show every
trend, ratio and exception the narration states, and that each number spoken
in ``narration.py`` matches the data.
"""

from __future__ import annotations

from utils.physics_models import SYMBOLS, symbol_of, z_of

# ---------------------------------------------------------------------------
# Textbook values (NCERT Class XI, Unit 3, Tables 3.6 and 3.7)
# ---------------------------------------------------------------------------

# Atomic radii in pm. Metals: metallic radius. Non-metals: covalent radius.
ATOMIC_RADII_PM: dict[str, int] = {
    "Li": 152, "Be": 111, "B": 88, "C": 77, "N": 74, "O": 66, "F": 64,
    "Na": 186, "Mg": 160, "Al": 143, "Si": 117, "P": 110, "S": 104, "Cl": 99,
    "K": 231, "Rb": 244, "Cs": 262,
    "Br": 114, "I": 133, "At": 140,
}
METALLIC_RADIUS: frozenset[str] = frozenset({"Li", "Be", "Na", "Mg", "Al", "K", "Rb", "Cs"})

# Ionic (crystal) radii in pm, measured in ionic solids — a different convention
# from the atomic radii above, so the film compares them as a pattern only.
# Chloride (181 pm) is Pauling's crystal radius, on the same scale as the others.
IONIC_RADII_PM: dict[str, int] = {"Na+": 95, "F-": 136, "O2-": 140, "Mg2+": 65, "Cl-": 181}

# Protons and electrons of the ions the film draws.
IONS: dict[str, tuple[int, int]] = {
    "O2-": (8, 10), "F-": (9, 10), "Na+": (11, 10), "Mg2+": (12, 10),
}

# Electron gain enthalpy in kJ/mol (negative = energy released). NCERT Table 3.7
# for groups 1, 16, 17 and 18 and hydrogen; the rest are minus the measured
# electron affinities. ``None`` marks an anion that is not stable in the gas
# phase (Be, Mg, N): adding an electron needs energy, and no single value is
# quoted. Polonium is left out: its value is only estimated. Astatine uses
# Leimbach et al. (2020), EA = 2.41578 eV: https://doi.org/10.1038/s41467-020-17599-2
# rather than the older estimated NCERT value. Noble-gas positive values are
# textbook attachment estimates, not energies of stable ground-state anions.
ELECTRON_GAIN_KJ: dict[str, int | None] = {
    "H": -73, "He": 48,
    "Li": -60, "Be": None, "B": -27, "C": -122, "N": None, "O": -141, "F": -328, "Ne": 116,
    "Na": -53, "Mg": None, "Al": -42, "Si": -134, "P": -72, "S": -200, "Cl": -349, "Ar": 96,
    "K": -48, "Ca": -2, "Ga": -29, "Ge": -119, "As": -78, "Se": -195, "Br": -325, "Kr": 96,
    "Rb": -47, "Sr": -5, "In": -37, "Sn": -107, "Sb": -101, "Te": -190, "I": -295, "Xe": 77,
    "Cs": -46, "Ba": -14, "Tl": -31, "Pb": -35, "Bi": -91, "At": -233, "Rn": 68,
}

# ---------------------------------------------------------------------------
# One-definition data sets for the heat maps
# ---------------------------------------------------------------------------

# Single-bond covalent radii in pm: B. Cordero et al., "Covalent radii
# revisited", Dalton Trans. 2008, 2832–2838 (carbon: the sp3 value). Noble
# gases are left out: they form almost no covalent bonds, and mixing their
# van der Waals sizes into a covalent map would compare unlike things.
COVALENT_RADII_PM: dict[str, int] = {
    "H": 31,
    "Li": 128, "Be": 96, "B": 84, "C": 76, "N": 71, "O": 66, "F": 57,
    "Na": 166, "Mg": 141, "Al": 121, "Si": 111, "P": 107, "S": 105, "Cl": 102,
    "K": 203, "Ca": 176, "Ga": 122, "Ge": 120, "As": 119, "Se": 120, "Br": 120,
    "Rb": 220, "Sr": 195, "In": 142, "Sn": 139, "Sb": 139, "Te": 138, "I": 139,
    "Cs": 244, "Ba": 215, "Tl": 145, "Pb": 146, "Bi": 148, "Po": 140, "At": 150,
}

# First ionization energies in eV, Z = 1..86, NIST Atomic Spectra Database
# ground-state values. Converted to kJ/mol by ``ionization_kj``.
_IONIZATION_EV: tuple[float, ...] = (
    13.598434, 24.587389, 5.391715, 9.322699, 8.298019, 11.260288, 14.53413, 13.618054, 17.42282, 21.564541,
    5.139076, 7.646236, 5.985769, 8.15168, 10.486686, 10.36001, 12.967633, 15.759610,
    4.340663, 6.113155, 6.56149, 6.82812, 6.746187, 6.76651, 7.434038, 7.9024678, 7.88101, 7.639877,
    7.726380, 9.394197, 5.999302, 7.899435, 9.78855, 9.752392, 11.81381, 13.9996055,
    4.177128, 5.6948672, 6.21726, 6.634126, 6.75885, 7.09243, 7.11938, 7.36050, 7.45890, 8.336839,
    7.576234, 8.993820, 5.7863554, 7.343918, 8.608389, 9.009808, 10.45126, 12.1298437,
    3.893905, 5.2116646, 5.5769, 5.5386, 5.4702, 5.5250, 5.577, 5.64371, 5.670385, 6.14980,
    5.8638, 5.93905, 6.0215, 6.1077, 6.18431, 6.254160, 5.425871, 6.82507, 7.549571, 7.86403,
    7.83352, 8.43823, 8.96702, 8.95883, 9.225554, 10.437504, 6.1082873, 7.416796, 7.285516,
    8.41807, 9.31751, 10.74850,
)
EV_TO_KJ_PER_MOL = 96.48533

# Pauling electronegativities (Allred's 1961 revision of Pauling's scale).
# Lead uses the Pb(II) value. Noble gases are left out: helium, neon and argon
# form no ordinary compounds, so they have no Pauling value to compare.
ELECTRONEGATIVITY: dict[str, float] = {
    "H": 2.20,
    "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98,
    "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
    "K": 0.82, "Ca": 1.00, "Ga": 1.81, "Ge": 2.01, "As": 2.18, "Se": 2.55, "Br": 2.96,
    "Rb": 0.82, "Sr": 0.95, "In": 1.78, "Sn": 1.96, "Sb": 2.05, "Te": 2.10, "I": 2.66,
    "Cs": 0.79, "Ba": 0.89, "Tl": 1.62, "Pb": 1.87, "Bi": 2.02, "Po": 2.00, "At": 2.20,
}

# The main-group columns (s and p blocks), periods 1–6: the elements every
# heat map colours. Transition and inner-transition tiles stay dim outlines.
MAIN_GROUP_COLUMNS: tuple[int, ...] = (1, 2, 13, 14, 15, 16, 17, 18)
HEAT_MAP_PERIODS: tuple[int, ...] = (1, 2, 3, 4, 5, 6)


def ionization_kj(symbol_or_z: str | int) -> int:
    """First ionization enthalpy in kJ/mol, rounded, for Z = 1..86."""
    z = symbol_or_z if isinstance(symbol_or_z, int) else z_of(symbol_or_z)
    return round(_IONIZATION_EV[z - 1] * EV_TO_KJ_PER_MOL)


def ionization_series() -> list[tuple[int, int]]:
    """(Z, kJ/mol) for every element the ionization graph plots."""
    return [(z, ionization_kj(z)) for z in range(1, len(_IONIZATION_EV) + 1)]


# The four heat-map tabs. ``value`` returns the plotted number (bigger = taller
# tower), or None for a tile with no comparable value. ``exception`` marks a
# tile whose value has the opposite sign to the trend (energy must be supplied).
PROPERTIES: dict[str, dict] = {
    "radius": {"title": "Atomic radius", "unit": "pm", "source": "covalent radius"},
    "ionization": {"title": "Ionization enthalpy", "unit": "kJ/mol", "source": "first ionization"},
    "electronegativity": {"title": "Electronegativity", "unit": "Pauling", "source": "Pauling scale"},
    "electron_gain": {"title": "Electron gain enthalpy", "unit": "kJ/mol", "source": "energy released"},
}


def property_value(prop: str, symbol: str) -> float | None:
    """The quantity a heat-map tower shows for one element (None: no tower)."""
    if prop == "radius":
        return COVALENT_RADII_PM.get(symbol)
    if prop == "ionization":
        return float(ionization_kj(symbol)) if z_of(symbol) <= len(_IONIZATION_EV) else None
    if prop == "electronegativity":
        return ELECTRONEGATIVITY.get(symbol)
    if prop == "electron_gain":
        if symbol not in ELECTRON_GAIN_KJ:
            return None
        value = ELECTRON_GAIN_KJ[symbol]
        # Released energy, so "more negative" rises; required energy stays flat.
        return 0.0 if value is None or value > 0 else float(-value)
    raise KeyError(prop)


def is_exception(prop: str, symbol: str) -> bool:
    """Electron gain that *needs* energy: the tiles the final map marks."""
    if prop != "electron_gain" or symbol not in ELECTRON_GAIN_KJ:
        return False
    value = ELECTRON_GAIN_KJ[symbol]
    return value is None or value > 0


def property_range(prop: str, symbols) -> tuple[float, float]:
    values = [v for v in (property_value(prop, s) for s in symbols) if v is not None]
    return min(values), max(values)


# ---------------------------------------------------------------------------
# Spoken numbers, checked against the data
# ---------------------------------------------------------------------------

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
         "fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def spoken(n: int) -> str:
    """British spoken form: 152 -> 'one hundred and fifty-two'."""
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
    if n < 2000:  # 1402 -> "fourteen hundred and two", the way the numbers are read aloud
        hundreds, rest = divmod(n, 100)
        return f"{spoken(hundreds)} hundred" + (f" and {spoken(rest)}" if rest else "")
    thousands, rest = divmod(n, 1000)
    return f"{spoken(thousands)} thousand" + (f" and {spoken(rest)}" if rest else "")


# (chapter, value) pairs: the narration of that chapter must say the number.
SPOKEN_VALUES: list[tuple[str, int, str]] = [
    ("05", ATOMIC_RADII_PM["Li"], "Li atomic radius"),
    ("05", ATOMIC_RADII_PM["Be"], "Be atomic radius"),
    ("05", ATOMIC_RADII_PM["F"], "F atomic radius"),
    ("05", ATOMIC_RADII_PM["Na"], "Na atomic radius"),
    ("05", ATOMIC_RADII_PM["Cl"], "Cl atomic radius"),
    ("06", ATOMIC_RADII_PM["F"], "F atomic radius"),
    ("06", ATOMIC_RADII_PM["I"], "I atomic radius"),
    ("07", ATOMIC_RADII_PM["Na"], "Na atomic radius"),
    ("07", IONIC_RADII_PM["Na+"], "Na+ ionic radius"),
    ("07", ATOMIC_RADII_PM["F"], "F atomic radius"),
    ("07", IONIC_RADII_PM["F-"], "F- ionic radius"),
    ("08", IONIC_RADII_PM["O2-"], "O2- ionic radius"),
    ("08", IONIC_RADII_PM["F-"], "F- ionic radius"),
    ("08", IONIC_RADII_PM["Na+"], "Na+ ionic radius"),
    ("08", IONIC_RADII_PM["Mg2+"], "Mg2+ ionic radius"),
    ("09", ionization_kj("Li"), "Li first ionization"),
    ("11", ionization_kj("Be"), "Be first ionization"),
    ("11", ionization_kj("B"), "B first ionization"),
    ("11", ionization_kj("N"), "N first ionization"),
    ("11", ionization_kj("O"), "O first ionization"),
    ("13", -ELECTRON_GAIN_KJ["F"], "F electron gain (magnitude)"),
    ("13", -ELECTRON_GAIN_KJ["Cl"], "Cl electron gain (magnitude)"),
]

# Chapter 06 reads the group-1 radii as a list ("one fifty-two, ..."). Chapter
# 09 rounds neon's 2081 to "about two thousand and eighty".
SPOKEN_PHRASES: list[tuple[str, str, bool, str]] = [
    ("06", "one fifty-two, one eighty-six, two thirty-one, two forty-four, two sixty-two",
     [ATOMIC_RADII_PM[s] for s in ("Li", "Na", "K", "Rb", "Cs")] == [152, 186, 231, 244, 262], "group-1 radii"),
    ("09", "about two thousand and eighty", abs(ionization_kj("Ne") - 2080) <= 2, "Ne first ionization"),
    ("14", "two point two", round(ELECTRONEGATIVITY["H"], 1) == 2.2, "H electronegativity"),
    ("14", "three point two", round(ELECTRONEGATIVITY["Cl"], 1) == 3.2, "Cl electronegativity"),
    ("15", "about four", round(ELECTRONEGATIVITY["F"]) == 4, "F electronegativity"),
]


def verify() -> list[str]:
    """Every trend, ratio, exception and number the narration states."""
    from narration import SCRIPT

    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    def falling(values) -> bool:
        return all(a > b for a, b in zip(values, values[1:]))

    r = ATOMIC_RADII_PM
    check(falling([r[s] for s in ("Li", "Be", "B", "C", "N", "O", "F")]), "period-2 radii must shrink")
    check(falling([r[s] for s in ("Na", "Mg", "Al", "Si", "P", "S", "Cl")]), "period-3 radii must shrink")
    check(falling([r[s] for s in ("Cs", "Rb", "K", "Na", "Li")]), "group-1 radii must grow downward")
    check(falling([r[s] for s in ("I", "Br", "Cl", "F")]), "halogen radii must grow downward")
    check(r["F"] < r["Li"] / 2, "fluorine must be less than half of lithium")
    check(1.65 <= r["Cs"] / r["Li"] <= 1.8, "caesium ~1.75x lithium ('one and three quarter')")
    cov = COVALENT_RADII_PM
    check(falling([cov[s] for s in ("Li", "Be", "B", "C", "N", "O", "F")]), "covalent scale must agree across")
    check(falling([cov[s] for s in ("Cs", "Rb", "K", "Na", "Li")]), "covalent scale must agree down")

    ion = IONIC_RADII_PM
    check(ion["Na+"] < r["Na"] and ion["F-"] > r["F"], "cation smaller, anion larger")
    check(falling([ion[s] for s in ("O2-", "F-", "Na+", "Mg2+")]), "isoelectronic ions must shrink with Z")
    check(ion["Mg2+"] < ion["O2-"] / 2, "Mg2+ must be less than half of O2-")
    check(len({electrons for _, electrons in IONS.values()}) == 1, "the four ions must share one electron count")

    ie = {z: v for z, v in ionization_series()}
    nobles = (2, 10, 18, 36, 54, 86)
    alkalis = (3, 11, 19, 37, 55)
    check(max(ie, key=ie.get) == 2, "helium must have the highest first ionization")
    for z in nobles:
        neighbours = [ie[n] for n in (z - 1, z + 1) if n in ie]
        check(all(ie[z] > v for v in neighbours), f"{symbol_of(z)} must be a peak")
    for z in alkalis:
        check(ie[z] < ie[z - 1] and ie[z] < ie[z + 1], f"{symbol_of(z)} must be a cliff")
    check(falling([ie[z] for z in nobles]), "noble-gas peaks must fall down the table")
    check(falling([ie[z] for z in alkalis]), "alkali-metal cliffs must fall down the table")
    check(3.8 <= ie[10] / ie[3] <= 4.2, "neon ~4x lithium")
    for low, high in (("Be", "B"), ("N", "O"), ("Mg", "Al"), ("P", "S")):
        check(ionization_kj(low) > ionization_kj(high), f"{low} > {high} exception")

    eg = ELECTRON_GAIN_KJ
    measured = {s: v for s, v in eg.items() if v is not None}
    check(min(measured, key=measured.get) == "Cl", "chlorine must be the most negative electron gain")
    check(eg["F"] > eg["Cl"], "fluorine less negative than chlorine")
    check(eg["Ne"] > 0 and eg["Cl"] < 0, "neon needs energy, chlorine releases it")
    check(falling([-eg[s] for s in ("Cl", "Br", "I")]), "below chlorine, halogens grow less negative")
    check(ionization_kj("Na") + eg["Cl"] > 0, "isolated Na -> Cl electron transfer must be uphill")

    en = ELECTRONEGATIVITY
    check(max(en, key=en.get) == "F", "fluorine must be the most electronegative")
    check(min(en, key=en.get) == "Cs", "caesium must be the least electronegative mapped")
    check(falling([en[s] for s in ("F", "O", "N", "C", "B", "Be", "Li")]), "electronegativity must rise across")

    for key, value, label in SPOKEN_VALUES:
        text = " ".join(line for _, line in SCRIPT[key]).lower()
        check(spoken(value) in text, f"chapter {key} should say {spoken(value)!r} ({label} = {value})")
    for key, phrase, agrees, label in SPOKEN_PHRASES:
        text = " ".join(line for _, line in SCRIPT[key]).lower()
        check(phrase in text, f"chapter {key} should say {phrase!r}")
        check(agrees, f"chapter {key}: {phrase!r} disagrees with the data ({label})")
    check(len(SYMBOLS) == 118, "symbols")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Data check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print(f"Data check passed: {len(SPOKEN_VALUES) + len(SPOKEN_PHRASES)} spoken numbers match the data, and every")
    print("trend, ratio and exception the narration states holds in the data sets.")
