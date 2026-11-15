"""A check on every number the narrator says, and every claim the film makes.

Nothing in this module imports Manim. ``python -m utils.rotation_data``
recomputes each quoted number from ``utils.physics_models``, converts it to
the words the narrator speaks, and confirms the phrase still appears in that
scene of ``narration.py``. On-screen strings go through the same ``fixed``
helper, so the picture, the voice and the model cannot disagree.
"""

from __future__ import annotations

from fractions import Fraction

from utils import physics_models as pm

# ---------------------------------------------------------------------------
# Numbers as the narrator says them
# ---------------------------------------------------------------------------

_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
         "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
_ORDINAL = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 12: "twelfth"}


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
    """'2.55' -> 'two point five five'; '-1' -> 'minus one'."""
    negative = text.startswith("-")
    whole, _, decimals = text.lstrip("-").partition(".")
    out = integer_words(int(whole))
    if decimals:
        out += " point " + " ".join(_ONES[int(d)] for d in decimals)
    return ("minus " if negative else "") + out


def fixed(value: float, decimals: int) -> str:
    out = f"{value:.{decimals}f}"
    return "0" + out[2:] if out.startswith("-0") and float(out) == 0 else out


def say(value: float, decimals: int = 0) -> str:
    if decimals == 0 and abs(value - round(value)) > 1e-9:
        raise ValueError(f"{value} would be spoken as a whole number")
    return spoken(fixed(value, decimals))


def fraction_words(f: Fraction) -> str:
    """Fraction(2, 5) -> 'two fifths'; Fraction(1, 2) -> 'one half'."""
    if f.denominator == 1:
        return integer_words(f.numerator)
    name = _ORDINAL[f.denominator]
    if f.numerator > 1:
        name += "s"
    return f"{integer_words(f.numerator)} {name}"


def frac_tex(f: Fraction) -> str:
    """LaTeX for an on-screen coefficient: 1 -> '', 1/2 -> '\\tfrac{1}{2}'."""
    if f == 1:
        return ""
    return rf"\tfrac{{{f.numerator}}}{{{f.denominator}}}"


# ---------------------------------------------------------------------------
# The film's numbers, each tied to the scene that speaks it
# ---------------------------------------------------------------------------


def spoken_numbers() -> list[tuple[str, str]]:
    """(scene key, phrase) pairs: the phrase must appear in that scene's narration."""
    c, k, d, s, b = pm.COM_PAIR, pm.CARTS, pm.DOOR, pm.SEESAW, pm.DUMBBELL
    w, dd, sk, inc = pm.WHEEL, pm.DISC, pm.SKATER, pm.INCLINE
    sh = pm.shape
    return [
        ("03", f"A {say(c.m1)} kilogram mass sits at {say(c.x1)}"),
        ("03", f"A {say(c.m2)} kilogram mass sits at {say(c.x2)} metres"),
        ("03", f"{say(c.m1).capitalize()} times {say(c.x1)}, plus {say(c.m2)} times {say(c.x2)}, is {say(c.moment)}"),
        ("03", f"the total mass, {say(c.total)} kilograms"),
        ("03", f"centre of mass is at {say(c.x_cm)} metres"),
        ("03", f"{say(c.x2 - c.x_cm).capitalize()} metre from the heavy mass, {say(c.x_cm - c.x1)} metres from the light one"),
        ("03", f"make one of them {say(c.m2 / c.m1)} times heavier"),
        ("08", f"A {say(k.m1)} kilogram cart moves right at {say(k.v1)} metres per second"),
        ("08", f"A {say(k.m2)} kilogram cart moves left at {say(-k.v2)} metre per second"),
        ("08", f"{say(k.m1)} times {say(k.v1)}, plus {say(k.m2)} times minus {say(-k.v2)}"),
        ("08", f"That's {say(k.momentum)} kilogram metres per second"),
        ("08", f"the total mass, {say(k.total)} kilograms"),
        ("08", f"right at {say(k.v_cm, 1)} metres per second"),
        ("08", f"gliding at {say(k.v_cm, 1)} metres per second"),
        ("11", f"with {say(d.force)} newtons, {say(d.r_far, 1)} metres from the hinges"),
        ("11", f"{say(d.force)} times {say(d.r_far, 1)}: {say(d.tau_far)} newton metres"),
        ("11", f"only {say(d.r_near, 1)} metres from the hinges: {say(d.tau_near)} newton metres"),
        ("11", f"{say(d.tau_far / d.tau_near)} times less torque"),
        ("13", f"weighing {say(s.w_left)} newtons sits {say(s.d_left)} metres to the left"),
        ("13", f"{say(s.w_right)} newtons, sits just {say(s.d_right)} metre from the pivot"),
        ("13", f"{say(s.w_left)} times {say(s.d_left)}, {say(s.tau_ccw)} newton metres, counterclockwise"),
        ("13", f"{say(s.w_right)} times {say(s.d_right)}, {say(s.tau_cw)} newton metres, clockwise"),
        ("13", f"the pivot must push up with {say(s.pivot)} newtons"),
        ("14", f"Take two {say(b.mass)} kilogram masses"),
        ("14", f"each {say(b.r_in)} metre from the axis"),
        ("14", f"{say(b.i_in)} kilogram metres squared"),
        ("14", f"out to {say(b.r_out)} metres"),
        ("14", f"{say(b.i_out)} kilogram metres squared"),
        ("14", f"is {say(b.i_out / b.i_in)} times larger"),
        ("15", f"{fraction_words(sh('disc').coefficient)} M R squared"),
        ("15", f"{fraction_words(sh('sphere').coefficient)} M R squared"),
        ("15", f"{fraction_words(sh('shell').coefficient)} M R squared"),
        ("15", f"{fraction_words(sh('rod_mid').coefficient)} M L squared"),
        ("15", f"{fraction_words(sh('rod_end').coefficient)} M L squared"),
        ("16", f"about {say(pm.GYRATION.disc, 2)} R"),
        ("17", f"{fraction_words(pm.AXES.rod_cm)} plus {fraction_words(pm.AXES.shift)} is {fraction_words(pm.AXES.rod_end)}"),
        ("17", f"each is {fraction_words(pm.AXES.disc_diameter)} M R squared"),
        ("19", f"acceleration of {say(w.alpha)} radians per second squared"),
        ("19", f"after {say(w.duration)} seconds"),
        ("19", f"{say(w.alpha)} times {say(w.duration)}: {say(w.omega)} radians per second"),
        ("19", f"{say(w.duration)} squared: {say(w.angle)} radians"),
        ("19", f"about {say(w.revolutions, 2)} revolutions"),
        ("22", f"mass {say(dd.mass)} kilograms and radius {say(dd.radius, 1)} metres"),
        ("22", f"That's {say(dd.inertia, 1)} kilogram metres squared"),
        ("22", f"a steady {say(dd.string_force)} newtons"),
        ("22", f"a net torque of {say(dd.torque)} newton metre"),
        ("22", f"{say(dd.torque)} divided by {say(dd.inertia, 1)}. {say(dd.alpha).capitalize()} radians per second squared"),
        ("22", f"turning at {say(dd.omega_end)} radians per second"),
        ("22", f"through {say(dd.angle_end)} radians"),
        ("23", f"I is {say(dd.inertia, 1)}"),
        ("23", f"omega is {say(dd.omega_end)}"),
        ("23", f"{say(dd.kinetic)} joules"),
        ("23", f"{say(dd.torque).capitalize()} newton metre, through {say(dd.angle_end)} radians: {say(dd.work)} joules"),
        ("25", f"Moment of inertia: {say(sk.i_out)} kilogram metres squared. Angular speed: {say(sk.omega_out)} radians per second"),
        ("25", f"{say(sk.i_out)} times {say(sk.omega_out)}, {say(sk.momentum)} kilogram metres squared per second"),
        ("25", f"drops to {say(sk.i_in)}"),
        ("25", f"L stays at {say(sk.momentum)}"),
        ("25", f"{say(sk.momentum)} over {say(sk.i_in)}: {say(sk.omega_in)} radians per second"),
        ("25", f"{say(sk.k_out)} joules"),
        ("25", f"{say(sk.k_in)} joules"),
        ("25", f"the extra {say(sk.work)} joules"),
        ("28", f"this {integer_words(int(inc.beta_deg))} degree ramp"),
        ("28", f"about {say(inc.a_cylinder, 2)}, versus {say(inc.a_ring, 2)} metres per second squared"),
        ("28", f"{say(inc.a_block, 1)} metres per second squared"),
        ("28", f"For the cylinder: {fraction_words(Fraction(1) / (1 + sh('cylinder').coefficient))} g sine beta"),
        ("28", f"For the ring: {fraction_words(Fraction(1) / (1 + sh('ring').coefficient))} g sine beta"),
        ("27", f"{fraction_words(pm.shape('cylinder').coefficient / (1 + pm.shape('cylinder').coefficient))} of its kinetic energy is rotation"),
    ]


def claims() -> list[tuple[str, bool]]:
    """Qualitative statements in the narration, checked against the model."""
    t, frames, _ = pm.spring_cluster_run(True)
    import numpy as np

    m = np.asarray(pm.SPRINGS.masses)
    spin = frames[-1][1] - frames[-1][0]
    start = frames[0][1] - frames[0][0]
    turned = abs(np.degrees(np.arctan2(spin[1], spin[0]) - np.arctan2(start[1], start[0]))) > 10
    return [
        ("01/02: rolling is translation plus rotation; the contact point is at rest",
         np.allclose(pm.rolling_point_velocity(np.pi), 0, atol=1e-12)),
        ("03: the heavier side pulls the balance point toward it", pm.COM_PAIR.x_cm > (pm.COM_PAIR.x1 + pm.COM_PAIR.x2) / 2),
        ("06: pushing one particle turns the cluster (a torque about the centre)", turned),
        ("06: the centre still accelerates at F / M",
         np.allclose(pm.com(m, frames[-1]) - pm.com(m, frames[0]), 0.5 * pm.SPRINGS.a_cm * t[-1] ** 2, atol=2e-3)),
        ("07: fragments ride the parabola until the first one lands", pm.first_landing() > pm.FIREWORK.burst_time),
        ("08: the carts' velocities change completely", all(np.sign(a) != np.sign(b) for a, b in
                                                          zip(pm.CARTS.elastic_after, (pm.CARTS.v1, pm.CARTS.v2)))),
        ("11: same force, four times the lever arm, four times the torque", pm.DOOR.r_far / pm.DOOR.r_near == 4),
        ("14: same torque, four times the inertia: a quarter of the angular acceleration",
         pm.DUMBBELL.i_out / pm.DUMBBELL.i_in == 4),
        ("14: same torque, the disc spins up faster than the ring",
         pm.shape("disc").coefficient < pm.shape("ring").coefficient),
        ("15: ring is twice the disc", pm.shape("ring").coefficient == 2 * pm.shape("disc").coefficient),
        ("15: more mass near the rim -> larger I (sphere < disc < shell < ring)",
         pm.shape("sphere").coefficient < pm.shape("disc").coefficient < pm.shape("shell").coefficient
         < pm.shape("ring").coefficient),
        ("17: centre-of-mass axis gives the smallest I", min(pm.rod_inertia_about(x) for x in np.linspace(-0.5, 0.5, 101))
         == pm.rod_inertia_about(0.0)),
        ("19: not quite three full turns", 2 < pm.WHEEL.revolutions < 3),
        ("20: radial part dominates as the wheel speeds up",
         pm.accelerations(1.0, pm.WHEEL.alpha, pm.WHEEL.omega)[1] > 10 * pm.accelerations(1.0, pm.WHEEL.alpha, pm.WHEEL.omega)[0]),
        ("22: the disc's alpha equals the wheel's", pm.DISC.alpha == pm.WHEEL.alpha),
        ("23: work equals the kinetic energy gained", pm.DISC.work == pm.DISC.kinetic),
        ("25: the spin doubles and the energy doubles",
         pm.SKATER.omega_in == 2 * pm.SKATER.omega_out and pm.SKATER.k_in == 2 * pm.SKATER.k_out),
        ("25: pulling the arms in does the extra work", abs(pm.skater_work_by_integration() - pm.SKATER.work) < 1e-4),
        ("26: the top moves at twice the centre's speed", np.allclose(pm.rolling_point_velocity(0.0), [2, 0, 0])),
        ("27: ring shares half its energy with rotation", pm.kinetic_share(1.0) == 0.5),
        ("28: cylinder beats ring; a frictionless block beats both",
         pm.INCLINE.time(0.0) < pm.INCLINE.time(0.5) < pm.INCLINE.time(1.0)),
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
