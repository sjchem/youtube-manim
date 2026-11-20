"""A check on every number the narrator says, and every claim the film makes.

Nothing in this module imports Manim. ``python -m utils.spoken_numbers``
recomputes each quoted number from ``utils.physics_models``, converts it to the
words the narrator speaks, and confirms the phrase still appears in that scene
of ``narration.py``. On-screen strings go through the same ``fixed`` helper, so
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

YEAR_VAN_DER_WAALS = 1873
YEAR_ANDREWS = 1869


def spoken_numbers() -> list[tuple[str, str]]:
    """(scene key, phrase) pairs: the phrase must appear in that scene's narration."""
    S, F = pm.SPEEDS, pm.FLASK
    co2_tc, co2_pc = pm.CRITICAL["CO2"]
    return [
        ("06", f"Here is nitrogen, at {say(S.T1)} kelvin"),
        ("06", f"about {say(round(S.mp, -1))} metres per second"),
        ("06", f"about {say(round(S.av, -1))} metres per second"),
        ("06", f"about {say(round(S.rms, -1))} metres per second"),
        ("06", f"in the ratio {say(pm.SPEED_RATIO[0])}, to {say(pm.SPEED_RATIO[1], 3)}, to {say(pm.SPEED_RATIO[2], 3)}"),
        ("06", f"by a factor of about {say(round(S.grams_error))}"),
        ("07", f"from {say(S.T1)} to {say(S.T2)} kelvin"),
        ("07", f"about {say(S.heat_factor, 2)} times"),
        ("13", f"In {year_words(YEAR_VAN_DER_WAALS)}"),
        ("14", f"Its volume is {say(pm.EXCLUSION_RATIO)} times the volume"),
        ("14", f"{say(pm.EXCLUDED_PER_MOLECULE)} times the molecule's own volume"),
        ("14", f"it is about {say(pm.EXCLUDED_PER_MOLECULE)} times larger"),
        ("15", f"at {say(F.T)} kelvin"),
        ("15", f"about {say(F.ideal, 1)} bar"),
        ("15", f"about {say(F.size_only, 1)} bar"),
        ("15", f"about {say(F.attraction, 1)} bar"),
        ("15", f"about {say(F.vdw, 1)} bar"),
        ("15", f"about {say(round(F.percent_below))} percent below"),
        ("16", f"Z of about {say(F.Z, 2)}"),
        ("16", f"at {say(pm.ROOM_T)} kelvin"),
        ("17", f"about {say(pm.BOYLE_T['N2'])} kelvin for nitrogen"),
        ("17", f"only about {say(pm.BOYLE_T['He'])} for helium"),
        ("18", f"at {say(pm.ANDREWS_FOLLOW_C, 1)} degrees Celsius"),
        ("19", f"At about {say(round(pm.celsius(co2_tc)))} degrees Celsius"),
        ("19", f"about {say(co2_tc, 1)} kelvin"),
        ("19", f"about {say(co2_pc, 1)} bar"),
        ("22", f"about {say(round(pm.celsius(co2_tc)))} degrees Celsius"),
        ("22", f"about {say(pm.CRITICAL['N2'][0])} kelvin"),
        ("22", f"nearly {say(round(pm.celsius(pm.CRITICAL['N2'][0]), -1))} degrees Celsius"),
        ("22", f"about {say(pm.CRITICAL['NH3'][0], 1)} kelvin"),
        ("24", f"ether boils at about {say(round(pm.boiling_point('ether', pm.ATM_BAR)))} degrees Celsius"),
        ("24", f"ethanol at about {say(round(pm.boiling_point('ethanol', pm.ATM_BAR)))}"),
        ("24", f"and water at {say(round(pm.boiling_point('water', pm.ATM_BAR)))}"),
        ("24", f"water boils at only about {say(round(pm.boiling_point('water', pm.EVEREST_BAR), -1))} degrees"),
        ("24", f"at about {say(pm.COOKER_BAR)} bar"),
        ("24", f"about {say(round(pm.boiling_point('water', pm.COOKER_BAR), -1))} degrees"),
        ("25", f"at {say(20)} degrees is about {say(round(pm.SURFACE_TENSION_20C['water']))} millinewtons per metre"),
        ("26", f"about {say(round(pm.celsius(pm.WATER_TC)))} degrees Celsius"),
        ("28", f"Water at {say(100)} degrees is less than a third as viscous as at {say(20)}"),
    ]


def claims() -> list[tuple[str, bool]]:
    """Qualitative statements in the narration, checked against the model."""
    S, F = pm.SPEEDS, pm.FLASK
    _, _, p1, p2 = pm.pair_demo()
    return [
        ("03: billions of collisions every second (N2, 1 bar, 300 K)", 1e9 <= pm.N2_COLLISIONS_PER_S < 1e10),
        ("03: an elastic collision leaves one molecule faster and one slower",
         max(pm.COLLISION.speeds_after) > 1.1 * pm.COLLISION.speed > 0.9 * pm.COLLISION.speed > min(pm.COLLISION.speeds_after)),
        ("05: the shell's area grows as 4 pi u^2; the cloud fades faster (MB density falls at high u)",
         float(pm.maxwell_pdf(3.0)) < 0.05 * float(pm.maxwell_pdf(1.0))),
        ("06: u_mp < u_av < u_rms", S.mp < S.av < S.rms),
        ("07: heating lowers the MB peak", pm.mb_pdf(S.mp * S.heat_factor, S.T2, pm.MOLAR_MASS["N2"])
         < pm.mb_pdf(S.mp, S.T1, pm.MOLAR_MASS["N2"])),
        ("07: chlorine is about two and a half times heavier than nitrogen", abs(S.mass_ratio - 2.5) < 0.1),
        ("07: chlorine peaks further left", S.heavy_mp < S.mp),
        ("09: molecules fill less than a thousandth of air", pm.molecular_volume_fraction() < 1e-3),
        ("11: hard spheres hit the walls more often than points (Carnahan-Starling Z > 1)",
         pm.carnahan_starling(0.2) > 1),
        ("12/16: helium and hydrogen show positive deviation at 300 K",
         all(pm.z_vdw(p, pm.ROOM_T, g) >= 0.999 for g in ("He", "H2") for p in (1, 50, 200, 600))),
        ("13: doubling density gives about four times the nearby pairs", 3.8 <= p2 / p1 <= 4.3),
        ("13: a(CO2) is about a hundred times a(He)", 80 <= pm.VDW["CO2"][0] / pm.VDW["He"][0] <= 130),
        ("13: ammonia's a is larger still", pm.VDW["NH3"][0] > pm.VDW["CO2"][0]),
        ("15: in a hundred litres the corrections almost vanish", F.dilute_difference_percent < 0.2),
        ("16: Z 0.8 means 80 percent of the ideal volume; 1.2 means 120 percent", True),
        ("16: methane dips below one at 300 K", min(pm.z_vdw(p, pm.ROOM_T, "CH4") for p in range(5, 400, 5)) < 0.9),
        ("17: helium is far above its Boyle temperature at room temperature", pm.BOYLE_T["He"] * 10 < pm.ROOM_T),
        ("18: Andrews' experiments date from the eighteen sixties", 1860 <= YEAR_ANDREWS < 1870),
        ("20: the vdW critical temperature 8a/27Rb reproduces CO2's (a, b fitted to it)",
         abs(pm.vdw_critical_temperature("CO2") - pm.CRITICAL["CO2"][0]) < 1.0),
        ("22: CO2's T_c is just above room temperature; N2's far below; NH3's far above",
         pm.CRITICAL["N2"][0] < 298.15 < pm.CRITICAL["CO2"][0] < pm.CRITICAL["NH3"][0]),
        ("24: Everest is about a third of an atmosphere", abs(pm.EVEREST_BAR / pm.ATM_BAR - 1 / 3) < 0.02),
        ("24: ether is more volatile than ethanol and water",
         pm.vapour_pressure("ether", 25) > pm.vapour_pressure("ethanol", 25) > pm.vapour_pressure("water", 25)),
        ("26: a sphere has about a fifth less area than a cube of equal volume", 0.18 < 1 - pm.sphere_vs_cube_area() < 0.21),
        ("26: surface tension falls with temperature and vanishes at T_c",
         pm.water_surface_tension(373.15) < pm.water_surface_tension(293.15) and pm.water_surface_tension(pm.WATER_TC) == 0),
        ("28: water at 100 degC is less than a third as viscous as at 20 degC",
         pm.water_viscosity(100) < pm.water_viscosity(20) / 3),
        ("28: honey is thousands of times more viscous than water", pm.honey_to_water()[0] >= 1000),
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
