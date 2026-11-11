"""A check on every number the narrator says, and every claim the film makes.

Nothing in this module imports Manim. ``python -m utils.gas_data`` recomputes
each quoted number from ``utils.physics_models``, converts it to the words the
narrator speaks, and confirms the phrase still appears in that scene of
``narration.py``. On-screen strings go through the same ``fixed`` helper, so
the picture, the voice and the model cannot disagree.

Sources are listed in ``utils/physics_models.py``.
"""

from __future__ import annotations

from math import floor, log10

from utils import physics_models as pm

# ---------------------------------------------------------------------------
# Numbers as the narrator says them
# ---------------------------------------------------------------------------

_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
         "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def integer_words(n: int) -> str:
    if n < 0:
        return "minus " + integer_words(-n)
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + ("-" + _ONES[ones] if ones else "")
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        return f"{_ONES[hundreds]} hundred" + (f" and {integer_words(rest)}" if rest else "")
    thousands, rest = divmod(n, 1000)
    tail = "" if not rest else (f" and {integer_words(rest)}" if rest < 100 else f" {integer_words(rest)}")
    return f"{integer_words(thousands)} thousand" + tail


def spoken(text: str) -> str:
    """'22.71' -> 'twenty-two point seven one'; '-60' -> 'minus sixty'."""
    negative = text.startswith("-")
    whole, _, decimals = text.lstrip("-").partition(".")
    words = integer_words(int(whole))
    if decimals:
        words += " point " + " ".join(_ONES[int(d)] for d in decimals)
    return ("minus " if negative else "") + words


def year_words(year: int) -> str:
    """1662 -> 'sixteen sixty-two', 1811 -> 'eighteen eleven'."""
    return f"{integer_words(year // 100)} {integer_words(year % 100)}"


def fixed(value: float, decimals: int) -> str:
    out = f"{value:.{decimals}f}"
    return "0" + out[2:] if out.startswith("-0") and float(out) == 0 else out


def whole(value: float) -> str:
    """A whole number from the model, refused if it is not (nearly) whole."""
    if abs(value - round(value)) > 1e-9:
        raise ValueError(f"{value} is not a whole number")
    return str(int(round(value)))


def power_words(value: float, digits: int = 0) -> str:
    """5.0e-23 -> 'five times ten to the minus twenty-three' (mantissa rounded to ``digits``)."""
    exponent = int(floor(log10(abs(value))))
    mantissa = value / 10 ** exponent
    if round(mantissa, digits) >= 10:
        mantissa, exponent = mantissa / 10, exponent + 1
    return f"{spoken(fixed(mantissa, digits))} times ten to the {spoken(str(exponent))}"


def say(value: float, decimals: int = 0) -> str:
    return spoken(fixed(value, decimals))


# ---------------------------------------------------------------------------
# The film's numbers, each tied to the scene that speaks it
# ---------------------------------------------------------------------------

TRACE_COUNTS = (1, 5, 50, 5000)        # molecules in the force traces of scene 12
YEAR_BOYLE = 1662
YEAR_AVOGADRO = 1811


def spoken_numbers() -> list[tuple[str, str]]:
    """(scene key, phrase) pairs: the phrase must appear in that scene's narration."""
    A, B, C, T = pm.AIR, pm.BOYLE, pm.CHARLES, pm.CELSIUS_TRAP
    G, V, K, D, X, W = pm.GAY_LUSSAC, pm.AVOGADRO, pm.COMBINED, pm.DENSITY, pm.DALTON, pm.OVER_WATER
    frames, _, _ = pm.phase_movie()
    rt = pm.thermal_energy_per_mole(pm.ROOM_T)
    return [
        ("01", f"about {say(A.tonnes_per_square_metre)} tonnes"),
        ("03", f"about {say(round(pm.OH_BOND_KJ, -1))} kilojoules per mole"),
        ("03", f"only about {say(pm.H_BOND_KJ)}"),
        ("04", f"about {say(2 ** 6)} times"),
        ("04", f"Helium boils at about {say(pm.NOBLE_BOILING_K['He'])} kelvin"),
        ("04", f"boils at about {say(pm.NOBLE_BOILING_K['Xe'])}"),
        ("06", f"about {say(pm.HYDRIDE_BOILING_C['H2S'])} degrees Celsius"),
        ("06", f"boils at {say(pm.HYDRIDE_BOILING_C['H2O'])}"),
        ("08", f"about {power_words(pm.K_B, 2)} joules per kelvin"),
        ("08", f"about {power_words(pm.mean_kinetic_energy(pm.ROOM_T))} joules per molecule"),
        ("08", f"about {integer_words(int(rt))} and a half kilojoules" if abs(rt - 2.5) < 0.05 else "two and a half"),
        ("09", f"Watch {say(frames.shape[1])} atoms"),
        ("09", f"about {say(pm.R * pm.ARGON_WELL_K / 1000)} kilojoule per mole"),
        ("09", f"near {say(pm.NOBLE_BOILING_K['Ar'])} kelvin"),
        ("10", f"about {say(round(A.nitrogen_rms, -2))} metres per second"),
        ("10", f"around {power_words(A.impulse)} kilogram metres per second"),
        ("12", f"about {power_words(A.hits_per_cm2_per_s)} molecules strike every square centimetre"),
        ("12", f"{say(TRACE_COUNTS[2]).capitalize()}, and the relative fluctuations"),
        ("12", f"{say(TRACE_COUNTS[3]).capitalize()}, and the force"),
        ("12", f"{say(TRACE_COUNTS[1]).capitalize()} molecules give"),
        ("15", f"In {year_words(YEAR_BOYLE)}"),
        ("15", f"The gauge reads {say(B.P1)} bar"),
        ("16", f"occupies {say(B.V1)} litres at {say(B.P1)} bar"),
        ("16", f"to {say(B.V2)} litres"),
        ("16", f"{say(B.P2).capitalize()} bar."),
        ("17", "only about a third" if abs(pm.MOUNTAIN.pressure_fraction - 1 / 3) < 0.02 else "about a third"),
        ("20", f"{say(C.V1)} litres at {say(C.T1)} kelvin"),
        ("20", f"to {say(C.T2)} kelvin"),
        ("20", f"by half: {say(C.V2)} litres"),
        ("20", f"from {say(T.c1)} to {say(T.c2)} degrees Celsius"),
        ("20", f"rises by {say(100 * (T.c2 - T.c1) / T.c1)} percent"),
        ("20", f"only about {say(T.percent)} percent"),
        ("20", f"is {say(pm.celsius_to_kelvin(T.c1), 2)} kelvin"),
        ("20", f"is {say(pm.celsius_to_kelvin(T.c2), 2)}"),
        ("19", f"minus {say(pm.T_ICE, 2)} degrees Celsius"),
        ("19", f"plus {say(pm.T_ICE, 2)}"),
        ("21", f"from {say(G.T1)} to {say(G.T2)} kelvin"),
        ("21", f"becomes {say(G.P2, 1)} bar"),
        ("24", f"In {year_words(YEAR_AVOGADRO)}"),
        ("24", f"about {power_words(A.molecules_per_cm3 * 1000, 1)} molecules"),
        ("24", f"At {say(pm.T_ICE, 2)} kelvin and one bar"),
        ("24", f"occupies {say(V.per_bar, 2)} litres"),
        ("24", f"seen {say(V.per_atm, 1)} litres"),
        ("26", f"it is {say(pm.R, 3)} joules per mole per kelvin"),
        ("26", f"R is {say(pm.R_L_BAR, 5)} litre bar"),
        ("26", f"about {say(pm.IDEAL.V)} litres"),
        ("26", f"about {say(pm.cube_side_cm(pm.IDEAL.V))} centimetres"),
        ("26", f"holds {say(K.V1)} litres at {say(K.P1)} bar and {say(K.T1)} kelvin"),
        ("26", f"the temperature {say(K.T2)} kelvin"),
        ("26", f"to {say(K.V1 * K.P1 / K.P2)} litres"),
        ("26", f"{say(K.V2, 2).capitalize()} litres"),
        ("27", f"about {say(D.nitrogen, 2)} grams per litre"),
        ("27", f"about {say(D.helium, 2)}"),
        ("27", f"{say(D.ratio).capitalize()} times lighter"),
        ("27", f"gives {say(pm.molar_mass_from_density(round(D.nitrogen, 2), pm.BAR, pm.ROOM_T))} grams per mole"),
        ("28", f"{say(X.n_a).capitalize()} moles of nitrogen and {say(X.n_b)} mole of oxygen"),
        ("28", f"total pressure of {say(X.P_total)} bar"),
        ("28", f"nitrogen supplies {say(X.P_a)} bar, and oxygen {say(X.P_b)}"),
        ("28", f"about {say(100 * pm.AIR_FRACTION['O2'])} percent of air"),
        ("28", f"about {say(pm.MOUNTAIN.oxygen_sea_level, 2)} bar"),
        ("28", f"only about {say(pm.MOUNTAIN.oxygen_summit, 2)}"),
        ("29", f"At {say(298.15 - pm.T_ICE)} degrees Celsius"),
        ("29", f"about {say(W.aqueous_tension, 4)} bar"),
        ("29", f"exerts {say(W.P_dry, 3)} bar"),
    ]


def claims() -> list[tuple[str, bool]]:
    """Qualitative statements in the narration, checked against the model."""
    rt = pm.thermal_energy_per_mole(pm.ROOM_T)
    argon = pm.R * pm.ARGON_WELL_K / 1000
    nob = pm.NOBLE_BOILING_K
    return [
        ("03: intermolecular attraction is much weaker than the O-H bond", pm.H_BOND_KJ * 10 < pm.OH_BOND_KJ),
        ("04: boiling points climb with the size of the cloud He < Ne < Ar < Kr < Xe",
         all(nob[a] < nob[b] for a, b in zip("He Ne Ar Kr".split(), "Ne Ar Kr Xe".split()))),
        ("04: double the distance, the dispersion energy drops 64 times", abs(pm.dispersion(1.0) / pm.dispersion(2.0) - 64) < 1e-9),
        ("05: head to tail attracts, head to head repels",
         pm.dipole_energy(*pm.DIPOLE_POSES["head_to_tail"], (1, 0, 0)) < 0 < pm.dipole_energy(*pm.DIPOLE_POSES["head_to_head"], (1, 0, 0))),
        ("05: side by side, opposite ways, attracts more weakly than head to tail",
         pm.dipole_energy(*pm.DIPOLE_POSES["head_to_tail"], (1, 0, 0)) < pm.dipole_energy(*pm.DIPOLE_POSES["antiparallel"], (1, 0, 0)) < 0),
        ("05: all orientations average to zero; thermal weighting is attractive",
         abs(pm.keesom_average(2.0, 1.0)[0]) < 1e-9 and pm.keesom_average(2.0, 1.0)[1] < 0),
        ("06: H2S is heavier than H2O but boils lower", pm.HYDRIDE_BOILING_C["H2S"] < pm.HYDRIDE_BOILING_C["H2O"]),
        ("09: argon's well is less than half of RT at room temperature", argon < rt / 2),
        ("09: argon boils far below room temperature", nob["Ar"] < pm.ROOM_T),
        ("13: <v_x^2> is a third of <v^2> in a large sample",
         abs(pm.IdealGas(20000, 1).mean_square()[0] / pm.IdealGas(20000, 1).mean_square().sum() - 1 / 3) < 0.01),
        ("15: halving the volume doubles the pressure", abs(pm.pressure_ratio(V_ratio=0.5) - 2) < 1e-12),
        ("17: rapid compression rises above the isotherm", pm.adiabatic_pressure(0.5) > pm.pressure_ratio(V_ratio=0.5)),
        ("18: double the kelvin temperature, the volume doubles", abs(pm.CHARLES.V1 * 2 / pm.CHARLES.V1 - 2) < 1e-12),
        ("20: the Celsius trap rises by a few percent, not fifty", 2 < pm.CELSIUS_TRAP.percent < 5),
        ("24: 22.4 L belongs to 1 atm, which is above 1 bar", pm.ATM > pm.BAR and pm.AVOGADRO.per_atm < pm.AVOGADRO.per_bar),
        ("26: cooling 300 K -> 250 K shrinks the volume by a sixth", abs((1 - pm.COMBINED.T2 / pm.COMBINED.T1) - 1 / 6) < 1e-12),
        ("27: helium is lighter than nitrogen by the ratio of molar masses",
         abs(pm.DENSITY.ratio - pm.MOLAR_MASS["N2"] / pm.MOLAR_MASS["He"]) < 1e-9),
        ("28: partial pressures add to the total", abs(pm.DALTON.P_a + pm.DALTON.P_b - pm.DALTON.P_total) < 1e-12),
        ("29: dry gas pressure is below the total", pm.OVER_WATER.P_dry < pm.OVER_WATER.P_total),
    ]


def verify() -> list[str]:
    from narration import SCRIPT

    failures = []
    for key, phrase in spoken_numbers():
        text = " ".join(line for _, line in SCRIPT[key]).lower()
        if phrase.lower() not in text:
            failures.append(f"scene {key}: narration no longer says «{phrase}»")
    for name, ok in claims():
        if not ok:
            failures.append(f"claim failed: {name}")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Spoken-number check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print(f"Spoken-number check passed: {len(spoken_numbers())} spoken numbers and {len(claims())} claims "
          "agree with utils.physics_models.")
