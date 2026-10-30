"""Measured data, with sources, and a check on every number the narrator says.

Sources
-------
* **Definitions** — amount concentration (molarity), molality, mole fraction,
  mass concentration, and the deprecation of "normality" and "equivalent":
  IUPAC *Compendium of Chemical Terminology* (the Gold Book), and the IUPAC
  *Compendium of Analytical Nomenclature* (the Orange Book), section on
  concentration terms.
* **Normality as N = M x z (z equivalents per mole) for a stated reaction**; % (w/w), % (w/v),
  % (v/v); ppm and ppb on a stated basis: D. Harvey, *Analytical Chemistry
  2.1* (LibreTexts), chapter 2.
* **Density of water** at 20, 40 and 70 °C (0.99821, 0.99222, 0.97778 g/mL),
  **density of ethanol** at 20 °C (0.7893 g/mL), and densities of
  ethanol-water mixtures by mass fraction at 20 °C: CRC Handbook of Chemistry
  and Physics, "Concentrative properties of aqueous solutions".
* **Cryoscopic and ebullioscopic constants of water**, Kf = 1.86 and
  Kb = 0.512 K kg/mol: CRC Handbook; OpenStax *Chemistry 2e*, section 11.4.
* **A 5 % dextrose infusion** contains 5 g glucose per 100 mL (% w/v): any
  pharmacopoeia monograph for "Glucose 5 % intravenous infusion".
* **Atmospheric CO2** has been above 400 ppm (by amount, i.e. by molecule
  count in dry air) since 2015: NOAA Global Monitoring Laboratory.

Nothing in this module imports Manim. ``python -m utils.concentration_data``
recomputes every quoted number from ``utils.physics_models`` and the data
above, converts it to the words the narrator speaks, and confirms the phrase
still appears in ``narration.py``.
"""

from __future__ import annotations

from utils import physics_models as pm

# ---------------------------------------------------------------------------
# Measured values
# ---------------------------------------------------------------------------

WATER_DENSITY = {20: 0.99821, 40: 0.99222, 70: 0.97778}   # g/mL
ETHANOL_DENSITY_20C = 0.7893                         # g/mL
# Ethanol-water mixtures at 20 °C: density (g/mL) by mass percent ethanol.
ETHANOL_WATER_DENSITY = {40.0: 0.93518, 50.0: 0.91384}
KF_WATER = 1.86                                      # K kg/mol
KB_WATER = 0.512                                     # K kg/mol
DRIP_PERCENT_WV = 5.0


def heated_volume_mL() -> float:
    """The sealed reference sample at 70 °C, if it expands like pure water."""
    return pm.heated_volume(pm.REFERENCE.volume_mL, WATER_DENSITY[20], WATER_DENSITY[70])


def heated() -> pm.Solution:
    return pm.REFERENCE.at_volume(round(heated_volume_mL(), 1))


def ethanol_water_mix_mL(ethanol_mL: float = 50.0, water_mL: float = 50.0) -> float:
    """Volume after mixing, from the measured density of the mixture."""
    ethanol_g = ethanol_mL * ETHANOL_DENSITY_20C
    water_g = water_mL * WATER_DENSITY[20]
    percent = 100.0 * ethanol_g / (ethanol_g + water_g)
    (p0, d0), (p1, d1) = sorted(ETHANOL_WATER_DENSITY.items())
    density = d0 + (percent - p0) * (d1 - d0) / (p1 - p0)
    return (ethanol_g + water_g) / density


def warm_flask_mL(capacity: float = 1000.0) -> float:
    """A flask filled to its mark at 20 °C, warmed to 40 °C (liquid expands like water)."""
    return pm.heated_volume(capacity, WATER_DENSITY[20], WATER_DENSITY[40])


def wrong_way_mL(water_mL: float = 1000.0, moles: float = 0.5) -> float:
    """1 L of water plus 0.500 mol glucose, with the reference solution's apparent molar volume."""
    return water_mL + moles * pm.apparent_molar_volume()


def ppm_in_ethanol_for_1_mg_per_L() -> float:
    """1 mg in a litre of ethanol (0.7893 kg) is this many mg per kg."""
    return 1.0 / ETHANOL_DENSITY_20C


# ---------------------------------------------------------------------------
# Numbers as the narrator says them
# ---------------------------------------------------------------------------

_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
         "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _integer_words(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + ("-" + _ONES[ones] if ones else "")
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        return f"{_ONES[hundreds]} hundred" + (f" and {_integer_words(rest)}" if rest else "")
    thousands, rest = divmod(n, 1000)
    joiner = " and " if 0 < rest < 100 else " "
    return f"{_integer_words(thousands)} thousand" + (joiner + _integer_words(rest) if rest else "")


def spoken(text: str) -> str:
    """'0.524' -> 'zero point five two four'; '198.0' -> 'one hundred and ninety-eight point zero'."""
    whole, _, decimals = text.partition(".")
    words = _integer_words(int(whole))
    if decimals:
        words += " point " + " ".join(_ONES[int(d)] for d in decimals)
    return words


def fixed(value: float, decimals: int) -> str:
    return f"{value:.{decimals}f}"


# ---------------------------------------------------------------------------
# Every number the narrator quotes: (scene, phrase, true?, label)
# ---------------------------------------------------------------------------

S = pm.REFERENCE
H = heated()
BOX = pm.litre_breakdown()


def _say(value: float, decimals: int, unit: str = "") -> str:
    return (spoken(fixed(value, decimals)) + (" " + unit if unit else "")).strip()


SPOKEN_CLAIMS: list[tuple[str, str, bool, str]] = [
    ("01", _say(S.molarity, 3, "molar"), True, "molarity"),
    ("01", _say(S.molality, 3, "molal"), True, "molality"),
    ("01", "zero point zero zero nine nine zero", fixed(S.x_solute, 5) == "0.00990", "mole fraction"),
    ("01", _say(S.mass_percent, 2, "percent by mass"), True, "mass percent"),
    ("02", _say(S.solute_g, 1, "grams of glucose"), True, "glucose mass"),
    ("02", _say(S.solvent_g, 1, "grams of water"), True, "water mass"),
    ("02", _say(S.solution_g, 1, "grams"), True, "solution mass"),
    ("02", "about " + _say(pm.M_GLUCOSE, 0, "grams per mole"), True, "glucose molar mass"),
    ("02", "about " + _say(pm.M_WATER, 0, "grams per mole"), True, "water molar mass"),
    ("02", _say(S.n_solute, 3, "moles"), True, "glucose amount"),
    ("02", _say(S.n_solvent, 1, "moles"), True, "water amount"),
    ("02", "Ten times more mass", S.solvent_g / S.solute_g == 10, "mass ratio"),
    ("02", "a hundred times more molecules", round(S.n_solvent / S.n_solute) == 100, "molecule ratio"),
    ("03", "Fifty millilitres of ethanol, and fifty millilitres of water", True, "mixing volumes"),
    ("03", "about ninety-six and a half millilitres", abs(ethanol_water_mix_mL() - 96.5) < 0.25, "contraction"),
    ("03", _say(S.volume_mL, 1, "millilitres"), True, "measured volume"),
    ("04", _say(S.n_solute, 3, "moles of glucose"), True, "numerator"),
    ("04", _say(S.volume_L, 4, "litres"), True, "volume in litres"),
    ("04", _say(S.molarity, 3, "moles per litre"), True, "molarity"),
    ("04", _say(S.molarity, 3, "molar"), True, "molarity"),
    ("05", _say(0.5, 3, "molar glucose"), True, "target"),
    ("05", _say(0.5 * pm.M_GLUCOSE, 1, "grams of glucose"), True, "mass to weigh"),
    ("05", "usually twenty degrees Celsius", True, "calibration temperature"),
    ("05", "rises past the one litre mark", wrong_way_mL() > 1000.0, "wrong way overshoots"),
    ("05", "creeps up past the line", warm_flask_mL() > 1000.0, "warm flask expands"),
    ("06", _say(S.solvent_g, 1, "grams"), True, "solvent mass"),
    ("06", _say(S.solvent_kg, 4, "kilograms"), True, "solvent mass in kg"),
    ("06", _say(S.molality, 3, "moles per kilogram"), True, "molality"),
    ("06", _say(S.molality, 3, "molal"), True, "molality"),
    ("07", _say(KF_WATER, 2, "degrees per molal"), True, "Kf"),
    ("07", "About " + _say(pm.freezing_point_drop(S.molality, KF_WATER), 2, "degrees"), True, "freezing drop"),
    ("07", "about three tenths of a degree", round(pm.boiling_point_rise(S.molality, KB_WATER), 1) == 0.3, "boiling rise"),
    ("08", "about seventy degrees Celsius", 70 in WATER_DENSITY, "heating target"),
    ("08", "about " + _say(H.volume_mL, 0, "millilitres"), abs(heated_volume_mL() - 195.0) < 0.1, "heated volume"),
    ("08", _say(H.volume_L, 3, "litres"), True, "heated volume in litres"),
    ("08", _say(H.molarity, 3), H.molarity < S.molarity, "heated molarity"),
    ("08", "Still " + _say(H.molality, 3), H.molality == S.molality, "molality unchanged"),
    ("10", _say(pm.ACID_MOLARITY, 3, "molar"), True, "acid molarity"),
    ("11", "Normality: " + _say(pm.normality(pm.ACID_MOLARITY, pm.REACTIONS["partial"]["protons"]), 3), True, "N partial"),
    ("11", "Normality: " + _say(pm.normality(pm.ACID_MOLARITY, pm.REACTIONS["complete"]["protons"]), 2), True, "N complete"),
    ("12", "one hundred and one molecules", round(S.n_total / S.n_solute) == 101, "crowd size"),
    ("12", "about a hundred and one picks", round(pm.expected_picks(S.x_solute)) == 101, "expected picks"),
    ("12", "zero point zero zero nine nine zero", fixed(S.x_solute, 5) == "0.00990", "x glucose"),
    ("13", _say(S.x_solvent, 5), True, "x water"),
    ("13", "drops by about one percent", round(100 * (1 - pm.vapour_pressure_fraction(S.x_solvent))) == 1, "Raoult"),
    ("14", _say(S.mass_percent, 2, "percent"), True, "w/w"),
    ("14", _say(S.wv_percent, 2, "percent, w over v"), True, "w/v"),
    ("14", "five grams of glucose in every hundred millilitres", DRIP_PERCENT_WV == 5.0, "drip"),
    ("15", "about " + _say(S.mass_concentration, 1, "grams per litre"), True, "gamma"),
    ("15", _say(S.mass_concentration / pm.M_GLUCOSE, 3, "molar"), True, "gamma / M"),
    ("16", "about eleven and a half days", abs(pm.seconds_to_days(1e6) - 11.5) < 0.1, "1 ppm of a second"),
    ("16", "about thirty-two years", round(pm.seconds_to_years(1e9)) == 32, "1 ppb of a second"),
    ("17", _say(S.density_g_per_mL, 3, "grams per millilitre"), True, "density"),
    ("17", "about " + _say(BOX["total_g"], 1, "grams"), True, "litre mass"),
    ("17", "about " + _say(BOX["solute_g"], 1, "grams of glucose"), True, "glucose in a litre"),
    ("17", "about " + _say(BOX["solvent_g"], 1, "grams of water"), True, "water in a litre"),
    ("17", _say(BOX["solvent_g"] / 1000, 4, "kilograms"), True, "water in kg"),
    ("17", _say(BOX["molality"], 3, "molal"), abs(BOX["molality"] - S.molality) < 1e-9, "molality again"),
    ("18", _say(pm.DILUTION["M1"], 2, "molar stock"), True, "stock"),
    ("18", _say(pm.DILUTION["M1"] * pm.DILUTION["V1_mL"] / 1000, 3, "moles"), True, "moles of solute"),
    ("18", _say(pm.dilute(pm.DILUTION["M1"], pm.DILUTION["V1_mL"], pm.DILUTION["V2_mL"]), 3, "molar"), True, "M2"),
    ("19", _say(S.mole_ratio, 4) + ", versus " + "zero point zero zero nine nine zero", True, "ratio vs fraction"),
    ("19", _say(S.molarity, 3, "molar") + ", but " + _say(S.molality, 3, "molal"), True, "M vs m"),
    ("19", "about " + _say(ppm_in_ethanol_for_1_mg_per_L(), 2, "ppm by mass"), True, "ethanol ppm"),
]


def verify() -> list[str]:
    from narration import SCRIPT

    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    def text(key: str) -> str:
        return " ".join(line for _, line in SCRIPT[key]).lower()

    for key, phrase, agrees, label in SPOKEN_CLAIMS:
        check(phrase.lower() in text(key), f"scene {key} no longer says {phrase!r} ({label})")
        check(bool(agrees), f"scene {key} says {phrase!r} but the model or data disagree ({label})")
    check(spoken("1037") == "one thousand and thirty-seven", "spoken thousands")
    check(spoken("198.0") == "one hundred and ninety-eight point zero", "spoken decimals")
    check(H.molality == S.molality and H.molarity < S.molarity, "heating changes M, not m")
    m_dilute, m_strong = pm.molarity_for_molality([0.05, 3.0])
    check(abs(m_dilute - 0.05) / 0.05 < 0.03 and (3.0 - m_strong) / 3.0 > 0.2, "M and m close when dilute, apart when strong")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Data check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print(f"Data check passed: {len(SPOKEN_CLAIMS)} spoken numbers match the model and measured data.")
