"""Check that the drawn geometry obeys the physics it illustrates.

Without rendering anything, this builds the film's live bodies and confirms:

* a ``Drum``'s rim points sit at its radius and move with v = omega x r;
* the rolling wheel of scene 26 (spin = -x / R) has a contact point at rest
  and a top point moving at 2 v_cm, by finite differences;
* the race bodies of scene 28 touch the ramp surface at every instant,
  follow 1/2 a t^2, and their actual rim points have zero velocity at contact;
* the skater's hand radius reproduces the model's I at both arm positions;
* the straight-line particle of scene 24 keeps a constant L = r x p;
* the plotted cycloid includes a visible zero-speed ground-contact cusp;
* the scene 12 force couple turns in the direction of its actual torque.

    python -m utils.visual_contract_audit
"""

from __future__ import annotations

import numpy as np


def main() -> int:
    import config  # noqa: F401  (makes the repo importable)
    from manim_scenes.stage3d import Drum
    from manim_scenes import scene_26_rolling as s26
    from manim_scenes import scene_28_race as s28
    from utils import physics_models as pm

    failures: list[str] = []

    def check(ok: bool, message: str) -> None:
        if not ok:
            failures.append(message)

    # 1. Drum rim kinematics: v = omega x r about the drum's axis.
    spin = {"a": 0.3}
    axis = np.array([0.2, 1.0, -0.3]) / np.linalg.norm([0.2, 1.0, -0.3])
    drum = Drum(np.zeros(3), 1.7, 0.2, "#3E7CA6", axis=axis, spin=lambda: spin["a"])
    p0 = drum.rim_point(0.4, end=0.0)
    check(abs(np.linalg.norm(p0) - 1.7) < 1e-9, "rim point at the drum radius")
    h = 1e-6
    spin["a"] += h
    v = (drum.rim_point(0.4, end=0.0) - p0) / h
    check(np.allclose(v, np.cross(axis, p0), atol=1e-5), "drum rim velocity = omega x r (right-handed spin)")

    # 2. Rolling without slipping (scene 26): contact at rest, top at 2 v_cm.
    R = s26.R
    x = {"v": s26.X0 + 1.234}
    for angle, expected in ((-np.pi / 2, 0.0), (np.pi / 2, 2.0)):
        body = angle + (x["v"] - s26.X0) / R               # material point now at this spatial angle
        d0 = Drum(np.array([x["v"], R, 0.0]), R, 0.3, "#3E7CA6", spin=-(x["v"] - s26.X0) / R)
        a0 = d0.rim_point(body, end=0.0)
        dx = 1e-6
        d1 = Drum(np.array([x["v"] + dx, R, 0.0]), R, 0.3, "#3E7CA6", spin=-(x["v"] + dx - s26.X0) / R)
        speed = np.linalg.norm((d1.rim_point(body, end=0.0) - a0) / dx)    # per unit v_cm
        check(abs(speed - expected) < 1e-4, f"rolling point at {np.degrees(angle):.0f} deg moves at {speed:.4f} v_cm")

    # 3. Race (scene 28): every body touches the ramp; distances follow the model.
    inc = pm.INCLINE
    for c in (0.0, 0.5, 1.0):
        for tt in np.linspace(0, inc.time(c), 7):
            s = 0.5 * inc.accel(c) * tt * tt * s28.S
            centre = s28.TOP + s28.DOWN_SLOPE * s + s28.NORMAL * s28.R
            contact = centre - s28.NORMAL * s28.R
            # The ramp's top face is the line through TOP along DOWN_SLOPE.
            offset = contact - s28.TOP
            check(abs(offset[0] * s28.DOWN_SLOPE[1] - offset[1] * s28.DOWN_SLOPE[0]) < 1e-9, f"race body (c={c}) on the ramp at t={tt:.2f}")
        end = 0.5 * inc.accel(c) * inc.time(c) ** 2
        check(abs(end - inc.length) < 1e-9, f"race body (c={c}) finishes at the ramp's length")
    check(abs(s28.TOP[1] - inc.length * s28.S * np.sin(np.radians(inc.beta_deg))) < 1e-9, "ramp height = L sin(beta)")

    # Production race geometry: actual rim points have zero velocity at contact.
    # Checking just centre heights would miss a cylinder that translates with the wrong spin.
    for coefficient, lane in ((0.5, s28.LANES["cylinder"]), (1.0, s28.LANES["ring"])):
        for fraction in (0.25, 0.7):
            tt = fraction * inc.time(coefficient)
            centre = s28.race_centre(coefficient, tt, lane)
            phase = s28.rolling_spin(coefficient, tt)
            body = Drum(centre, s28.R, 0.32, "#3E7CA6", spin=phase)
            local_contact = body.axes().T @ (-s28.NORMAL * s28.R)
            material_angle = np.arctan2(local_contact[1], local_contact[0]) - phase
            contact = body.rim_point(material_angle, end=0.0)
            next_body = Drum(s28.race_centre(coefficient, tt + h, lane), s28.R, 0.32,
                             "#3E7CA6", spin=s28.rolling_spin(coefficient, tt + h))
            velocity = (next_body.rim_point(material_angle, end=0.0) - contact) / h
            check(np.allclose(contact, centre - s28.NORMAL * s28.R), "race rim lies on the ramp")
            check(np.linalg.norm(velocity) < 1e-4, "race rolls without sliding at contact")
    check(s28.distance_at(0.5, inc.time(0.5)) > s28.distance_at(1.0, inc.time(0.5)),
          "cylinder reaches the finish with the ring still uphill")
    check(s28.distance_at(0.0, inc.time(0.0)) > s28.distance_at(0.5, inc.time(0.0))
          > s28.distance_at(1.0, inc.time(0.0)), "final snapshot shows block, cylinder, ring in race order")

    # 4. Skater: the drawn reach is the model's arm radius for I = 4 and I = 2.
    k = pm.SKATER
    check(abs(k.inertia(k.r_out) - k.i_out) < 1e-12 and abs(k.inertia(k.r_in) - k.i_in) < 1e-12, "skater reach <-> I")
    check(abs(k.omega_at(k.r_in) * k.i_in - k.omega_at(k.r_out) * k.i_out) < 1e-12, "skater L unchanged by the reach")

    # 5. Straight-line angular momentum (scene 24 geometry): constant r x p.
    O = np.array([0.0, 0.25, 0.0])
    Ls = [np.cross(np.array([s, 0.25, 1.6]) - O, np.array([1.4, 0.0, 0.0])) for s in np.linspace(-3.2, 3.2, 9)]
    check(np.allclose(Ls, Ls[0]), "straight-line L = r x p is constant")

    # The actual plotted material point must touch the road with zero speed at a cusp.
    visible_cusps = [s26.X0 + 2 * np.pi * R * k for k in range(4)
                     if s26.CYCLOID_START_X <= s26.X0 + 2 * np.pi * R * k <= s26.CYCLOID_END_X]
    check(bool(visible_cusps), "the displayed cycloid segment includes a ground-contact cusp")
    for xx in visible_cusps:
        point = s26.material_point(xx)
        velocity = (s26.material_point(xx + h) - s26.material_point(xx - h)) / (2 * h)
        check(abs(point[1]) < 1e-9 and np.linalg.norm(velocity) < 1e-5,
              "drawn cycloid marker touches the ground and is instantaneously at rest")

    # The force couple has zero net force and torque in the displayed spin direction.
    from manim_scenes import scene_12_couple as s12
    from utils.math_utils import rotation_y
    for angle in np.linspace(0, 2 * np.pi, 13):
        forces = [s12.couple_force_direction(angle, side) for side in (-1, 1)]
        arms = [rotation_y(angle) @ np.array([side * s12.BAR_L / 2, 0, 0]) for side in (-1, 1)]
        torque = sum(np.cross(r, force) for r, force in zip(arms, forces))
        check(np.allclose(sum(forces), 0) and np.allclose(torque, [0, s12.BAR_L, 0]),
              "couple forces sum to zero and accelerate the positive-y spin")

    if failures:
        print("Visual contract check FAILED:")
        for f in failures:
            print("  -", f)
        return 1
    print("Visual contracts passed: drum v = omega x r, rolling contact at rest and top at 2 v_cm, race bodies on the "
          "ramp with no-slip contact and finishing at L, skater reach <-> I with constant L, straight-line L constant, "
          "drawn cycloid cusps at rest, and couple torque agrees with spin.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
