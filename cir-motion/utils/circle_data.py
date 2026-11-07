"""A check on every number the narrator says.

Sources
-------
* **Uniform circular motion**, v = r|omega|, a_c = v^2 / r, T = 2 pi r / v,
  f = 1 / T, F_c = m v^2 / r, a = -r omega^2 r-hat + r alpha theta-hat:
  the brief, matching OpenStax *University Physics Volume 1*, sections 4.4,
  6.3 and 10.1-10.3.
* **g = 9.8 m/s^2**; level-curve limit v_max = sqrt(mu_s g r): OpenStax
  *University Physics Volume 1*, section 6.3 (mu_s = 0.6 is illustrative).
* **GM of Earth = 3.986004418e14 m^3/s^2**, mean radius 6371 km: NASA Earth
  Fact Sheet; circular-orbit speed and period: OpenStax *University Physics
  Volume 1*, section 13.4. The 400 km orbit is an illustrative low orbit,
  close to a crewed station's.

Nothing in this module imports Manim. ``python -m utils.circle_data``
recomputes every quoted number from ``utils.physics_models``, converts it to
the words the narrator speaks, and confirms the phrase still appears in
``narration.py``. On-screen strings go through the same ``fixed`` helper.
"""

from __future__ import annotations

from math import pi, radians

from utils import physics_models as pm

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
    hundreds, rest = divmod(n, 100)
    return f"{_ONES[hundreds]} hundred" + (f" and {_integer_words(rest)}" if rest else "")


def spoken(text: str) -> str:
    """'7.07' -> 'seven point zero seven'; '0.318' -> 'zero point three one eight'."""
    negative = text.startswith("-")
    whole, _, decimals = text.lstrip("-").partition(".")
    words = _integer_words(int(whole))
    if decimals:
        words += " point " + " ".join(_ONES[int(d)] for d in decimals)
    return ("minus " if negative else "") + words


def fixed(value: float, decimals: int) -> str:
    out = f"{value:.{decimals}f}"
    return "0" + out[2:] if out.startswith("-0") and float(out) == 0 else out


def whole(value: float) -> str:
    if abs(value - round(value)) > 1e-9:
        raise ValueError(f"{value} is not a whole number")
    return str(int(round(value)))


# ---------------------------------------------------------------------------
# Every number the narrator quotes: (scene, value as shown, phrase that must appear)
# ---------------------------------------------------------------------------

P = pm.REFERENCE


def claims() -> list[tuple[str, str, str]]:
    dv = pm.turn_delta_v()
    inner, outer = pm.turntable_speeds()
    items = [
        ("01", whole(pm.HOOK_SPEED), "steady {} metres per second"),
        ("01", whole(pm.HOOK_SPEED), "exactly {} metres per second"),
        ("03", whole(pm.V1[0]), "first is {} metres per second along the x axis"),
        ("03", whole(pm.V2[1]), "second is {} metres per second along the y axis"),
        ("03", whole(dv[0] ** 2), "square root of {} plus"),
        ("03", fixed(pm.magnitude(dv), 2), "about {} metres per second"),
        ("08", whole(pm.SHRINKING_ANGLES_DEG[0]), "shrinks: {} degrees"),
        ("09", whole(P.v), "moves at {} metres per second"),
        ("09", whole(P.r), "radius {} metres"),
        ("09", whole(P.v ** 2), "squared is {}"),
        ("09", whole(P.accel), "acceleration of {} metres per second squared"),
        ("10", whole(pm.DOUBLE_SPEED.v), "moving at {} metres per second instead of"),
        ("10", whole(pm.DOUBLE_SPEED.accel), "take {} metres per second squared"),
        ("10", whole(pm.DOUBLE_RADIUS.accel), "halves, to {} metres per second squared"),
        ("13", whole(pm.TURNTABLE_OMEGA), "At {} radians per second"),
        ("13", whole(inner), "moves at {} metres per second"),
        ("13", whole(outer), "two metres out moves at {}"),
        ("13", whole(P.angular_speed), "four over two: {} radians per second"),
        ("14", fixed(P.period, 2), "about {} seconds"),
        ("14", fixed(P.frequency, 3), "about {} hertz"),
        ("14", whole(P.angular_speed), "gives back {} radians per second"),
        ("15", whole(P.accel), "acceleration of {} metres per second squared"),
        ("16", whole(P.m), "mass of {} kilograms"),
        ("16", whole(P.force), "force of {} newtons"),
        ("18", whole(pm.CURVE_RADIUS), "radius {} metres"),
        ("18", fixed(pm.MU_S, 1), "coefficient of {}"),
        ("18", fixed(pm.G, 1), "times {}, times"),
        ("18", fixed(pm.max_curve_speed(), 2), "about {} metres per second"),
        ("18", fixed(pm.kmh(pm.max_curve_speed()), 1), "roughly {} kilometres per hour"),
        ("18", whole(pm.SAFE_SPEED), "At {} metres per second, the car needs"),
        ("18", fixed(pm.required_accel(pm.SAFE_SPEED), 1), "needs {} metres per second squared"),
        ("18", fixed(pm.max_friction_accel(), 2), "supply up to {}"),
        ("18", whole(pm.FAST_SPEED), "At {} metres per second, it would need"),
        ("18", whole(pm.required_accel(pm.FAST_SPEED)), "it would need {}"),
        ("19", whole(pm.ORBIT_ALTITUDE / 1e3), "orbit {} kilometres above"),
        ("19", fixed(pm.orbital_speed() / 1e3, 2), "about {} kilometres per second"),
        ("19", fixed(pm.gravity_at(), 1), "about {} metres per second squared"),
        ("19", whole(int(pm.orbital_period() / 60)), "about {} minutes"),
        ("22", whole(P.accel), "radial part is {} metres per second squared"),
        ("22", fixed(pm.ALPHA, 1), "acceleration of {} radians per second squared"),
        ("22", whole(pm.tangential_accel()), "{} metre per second squared"),
        ("22", whole(P.accel ** 2), "square root of {} plus"),
        ("22", fixed(pm.total_accel(), 2), "about {} metres per second squared"),
        ("25", whole(P.v), "{} metres per second, two radians"),
        ("25", whole(P.angular_speed), "{} radians per second, a period of pi"),
        ("25", whole(P.accel), "{} metres per second squared, sixteen"),
        ("25", whole(P.force), "{} newtons"),
    ]
    return [(scene, shown, phrase.format(spoken(shown))) for scene, shown, phrase in items]


def truths() -> list[tuple[bool, str]]:
    """Qualitative statements the narration makes, checked against the model."""
    ratios = [pm.chord_ratio(radians(d)) for d in pm.SHRINKING_ANGLES_DEG]
    heavy, light = pm.Circular(450_000.0, P.r, P.v), pm.Circular(4.0, P.r, P.v)
    return [
        (abs(P.period - pi) < 1e-12, "the reference period is exactly pi seconds"),
        (all(x < y for x, y in zip(ratios, ratios[1:])) and ratios[-1] > 0.999, "2 sin(x/2)/x closes in on one"),
        (abs(pm.DOUBLE_SPEED.accel - 4 * P.accel) < 1e-12, "double the speed, four times the acceleration"),
        (abs(pm.DOUBLE_RADIUS.accel - P.accel / 2) < 1e-12, "double the radius, half the acceleration"),
        (heavy.accel == light.accel, "the required acceleration does not depend on mass"),
        (pm.required_accel(pm.SAFE_SPEED) < pm.max_friction_accel(), "15 m/s holds the 50 m curve"),
        (pm.required_accel(pm.FAST_SPEED) > pm.max_friction_accel(), "20 m/s needs more than friction gives"),
        (pm.gravity_at() / pm.G > 0.85, "gravity 400 km up is still most of its surface value"),
        (0 < pm.total_accel_tilt_deg() < 10, "the total arrow tips slightly forward"),
        (pm.TURNTABLE_RADII[1] == P.r and pm.turntable_speeds()[1] == P.v, "the outer turntable point is the reference particle"),
    ]


def main() -> int:
    from narration import SCRIPT

    failed = False
    for scene, shown, phrase in claims():
        text = " ".join(line for _, line in SCRIPT[scene])
        ok = phrase.lower() in text.lower()
        failed |= not ok
        print(f"{'OK  ' if ok else 'MISS'} scene_{scene}  {shown:>8}  «{phrase}»")
    for ok, label in truths():
        failed |= not ok
        print(f"{'OK  ' if ok else 'FAIL'} {label}")
    problems = pm.verify()
    for problem in problems:
        print(f"FAIL model: {problem}")
    print("\ncircle_data: " + ("every spoken number matches the model" if not failed and not problems else "FAILED"))
    return 1 if failed or problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
