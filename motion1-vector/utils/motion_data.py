"""A check on every number the narrator says.

Sources
-------
* **g = 9.8 m/s^2**, ideal projectile equations, time of flight, maximum
  height, range and the 30 / 45 / 60 degree comparison: the brief, matching
  OpenStax *University Physics Volume 1*, sections 2.3, 3.4 and 4.3.
* **Range-maximising angle from a height**, tan(theta) = v0 / sqrt(v0^2 + 2 g h):
  D. B. Lichtenberg and J. G. Wills, "Maximizing the range of the shot put",
  *Am. J. Phys.* 46, 546 (1978).
* **Quadratic drag**, F = (1/2) rho C_d A v^2 with C_d ~ 0.47 for a sphere:
  OpenStax *University Physics Volume 1*, section 6.4. The foam ball's k is
  illustrative; only "the optimum drops below 45 degrees" is spoken.
* **A standard 400 m track** (two 84.39 m straights): World Athletics,
  *Track and Field Facilities Manual*, 2019.

Nothing in this module imports Manim. ``python -m utils.motion_data``
recomputes every quoted number from ``utils.physics_models``, converts it to
the words the narrator speaks, and confirms the phrase still appears in
``narration.py``. On-screen strings go through the same ``fixed`` helper.
"""

from __future__ import annotations

from math import sqrt

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
    """'14.14' -> 'fourteen point one four'; '126.9' -> 'one hundred and twenty-six point nine'."""
    negative = text.startswith("-")
    whole, _, decimals = text.lstrip("-").partition(".")
    words = _integer_words(int(whole))
    if decimals:
        words += " point " + " ".join(_ONES[int(d)] for d in decimals)
    return ("minus " if negative else "") + words


def fixed(value: float, decimals: int) -> str:
    out = f"{value:.{decimals}f}"
    return "0" + out[2:] if out.startswith("-0") and float(out) == 0 else out


def _whole(value: float) -> str:
    if abs(value - round(value)) > 1e-9:
        raise ValueError(f"{value} is not a whole number")
    return str(int(round(value)))


# ---------------------------------------------------------------------------
# Every number the narrator quotes: (scene, value as shown, how it is said)
# ---------------------------------------------------------------------------

P = pm.REFERENCE
LOW, MID, HIGH = pm.TABLE


def claims() -> list[tuple[str, str, str]]:
    walk = pm.add(*pm.WALK)
    drone = pm.add(*pm.DRONE)
    sub = pm.sub(*pm.SUBTRACT)
    comp = pm.add(*pm.COMPONENTS)
    ax, ay = pm.resolve(*pm.RESOLVED)
    items = [
        # (scene, shown, phrase that must appear)
        ("02", _whole(pm.TWO_CARS), "{} metres per second"),
        ("03", _whole(pm.COLD), "{} degrees Celsius"),
        ("03", _whole(pm.SPRINT[0] / pm.SPRINT[1]), "speed of {} metres per second"),
        ("03", _whole(pm.CAR_SPEED), "It reads {} metres per second"),
        ("05", _whole(sum(pm.magnitude(v) for v in pm.WALK)), "four: {} metres"),
        ("05", _whole(pm.magnitude(walk)), "{} metres"),
        ("05", fixed(pm.direction_deg(walk), 1), "about {} degrees north of east"),
        ("05", _whole(pm.TRACK_LAP), "{} metres of distance"),
        ("06", _whole(pm.magnitude(pm.add(*pm.SAME_WAY))), "displacement: {} metres east"),
        ("07", _whole(pm.DRONE[0][0] ** 2), "Six squared is {}"),
        ("07", _whole(pm.DRONE[1][1] ** 2), "Eight squared is {}"),
        ("07", _whole(drone[0] ** 2 + drone[1] ** 2), "Together, {}"),
        ("07", _whole(pm.magnitude(drone)), "a resultant of {} metres"),
        ("07", fixed(pm.direction_deg(drone), 2), "about {} degrees north of east"),
        ("08", f"{_whole(sub[0])}, {_whole(sub[1])}", "A minus B is {}"),
        ("08", fixed(pm.magnitude(pm.corner_delta_v()), 1), "about {} metres per second"),
        ("09", f"{_whole(2 * pm.SCALED[0])} i hat plus {_whole(2 * pm.SCALED[1])}", "Two A is {} j hat"),
        ("10", _whole(pm.magnitude(pm.SCALED)), "Its length is {}"),
        ("12", fixed(ax, 2), "ten cosine thirty: {}"),
        ("12", _whole(ay), "exactly {}"),
        ("12", fixed(pm.naive_direction_deg(pm.QUADRANT_TRAP), 0), "It answers {} degrees"),
        ("12", fixed(pm.direction_deg(pm.QUADRANT_TRAP), 1), "true direction: {} degrees"),
        ("13", f"{_whole(comp[0])} i hat plus {_whole(comp[1])}", "R equals {} j hat"),
        ("13", _whole(comp[0] ** 2 + comp[1] ** 2), "root {}"),
        ("13", fixed(pm.magnitude(comp), 2), "about {}"),
        ("18", fixed(P.g, 1), "about {} metres per second squared"),
        ("19", fixed(P.vx, 2), "Horizontal: twenty cosine forty-five, about {} metres per second"),
        ("19", fixed(P.vy0, 2), "also about {} metres per second"),
        ("20", fixed(float(P.x(1)), 2), "After one second: {} metres"),
        ("20", fixed(float(P.x(2)), 2), "After two seconds: {} metres"),
        ("21", fixed(P.vy0, 2), "starts at {} metres per second"),
        ("21", fixed(P.g, 1), "decreases by {} metres per second"),
        ("22", fixed(P.speed(P.apex_time), 2), "sideways, at {} metres per second"),
        ("24", fixed(P.flight_time, 2), "about {} seconds"),
        ("24", fixed(P.apex_time, 2), "about {} seconds"),
        ("24", fixed(P.max_height, 2), "about {} metres above"),
        ("25", fixed(P.range, 2), "About {} metres"),
        ("25", fixed(P.flight_time, 2), "for {} seconds"),
        ("26", fixed(LOW.range, 2), "about {} metres away"),
        ("26", fixed(LOW.max_height, 2), "peaks at {} metres"),
        ("26", fixed(LOW.flight_time, 2), "after {} seconds"),
        ("26", fixed(HIGH.max_height, 2), "reaches {} metres"),
        ("26", fixed(HIGH.flight_time, 2), "takes {} seconds"),
        ("26", _whole(pm.LEDGE_HEIGHT), "a {} metre ledge"),
        ("26", fixed(pm.best_angle_from_height(P.v0, pm.LEDGE_HEIGHT), 0), "lower too: about {} degrees"),
    ]
    return [(scene, shown, phrase.format(spoken(shown) if "," not in shown and " " not in shown
                                         else _say_pair(shown))) for scene, shown, phrase in items]


def _say_pair(shown: str) -> str:
    """'3, 2' -> 'three, two'; '6 i hat plus 8' -> 'six i hat plus eight'."""
    out = []
    for token in shown.replace(",", " ,").split():
        out.append(spoken(token) if token.lstrip("-").replace(".", "").isdigit() else token)
    return " ".join(out).replace(" ,", ",")


def truths() -> list[tuple[bool, str]]:
    """Qualitative statements the narration makes, checked against the model."""
    p = P
    return [
        (abs(LOW.range - HIGH.range) < 1e-9, "30 and 60 degrees have equal ranges"),
        (MID.range > LOW.range, "45 degrees beats 30 and 60"),
        (abs(pm.DOUBLED.range / p.range - 4) < 1e-9, "double the speed, four times the range"),
        (pm.best_angle_with_drag(p.v0) < 45, "with drag the best angle drops below 45"),
        (pm.best_angle_from_height(p.v0, pm.LEDGE_HEIGHT) < 45, "from a ledge the best angle drops below 45"),
        (abs(p.speed(p.apex_time) - min(p.speed(t) for t in [i * p.flight_time / 400 for i in range(401)])) < 1e-6,
         "the top is the slowest point"),
        (abs(p.apex_time * 2 - p.flight_time) < 1e-12, "rise time equals fall time"),
        (abs(pm.magnitude(pm.corner_delta_v()) - pm.CORNER_SPEED * sqrt(2)) < 1e-12, "corner delta v = 15 root 2"),
        (135.0 == pm.direction_deg(pm.corner_delta_v()), "corner delta v points north-west"),
        (abs(p.vx - p.vy0) < 1e-9, "at 45 degrees the components are equal"),
    ]


def main() -> int:
    from narration import SCRIPT

    failed = False
    for scene, shown, phrase in claims():
        text = " ".join(line for _, line in SCRIPT[scene])
        ok = phrase.lower() in text.lower()
        failed |= not ok
        print(f"{'OK  ' if ok else 'MISS'} scene_{scene}  {shown:>14}  «{phrase}»")
    for ok, label in truths():
        failed |= not ok
        print(f"{'OK  ' if ok else 'FAIL'} {label}")
    problems = pm.verify()
    for problem in problems:
        print(f"FAIL model: {problem}")
    print("\nmotion_data: " + ("every spoken number matches the model" if not failed and not problems else "FAILED"))
    return 1 if failed or problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
