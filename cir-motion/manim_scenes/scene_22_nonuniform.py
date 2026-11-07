"""Scene 22 — speeding up on a circle (3D), then the brief's numbers.

A car on a 3D track of radius 2 m speeds up with the brief's alpha = 0.5
rad/s^2 (``physics_models.SpeedingUp``), from omega = 0.6 to 1.6 rad/s,
played at 0.3x: the orange radial part grows with v^2 / r, the purple
tangential part r alpha stays fixed along the motion, and their white sum
tips forward. Slowing down (alpha = -0.5) flips the purple arrow backward.
Every arrow uses one scale, so the parallelogram is the true vector sum.

Then the brief's instant, flat: v = 4 m/s on 2 m (a_r = 8), alpha = 0.5
(a_t = 1), |a| = sqrt(65) ~ 8.06 m/s^2, tipped 7.1 degrees forward of the
centre (``physics_models.total_accel_tilt_deg``).
"""

from manim_scenes.common import *

R = 2.4
KV = 0.5                     # stage units per m/s
KA = 0.36                    # stage units per m/s^2, for every acceleration arrow
SLOW = 0.3
OMEGA0, OMEGA1 = 0.6, 1.6


class Scene22Nonuniform(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "22", "Speeding up on a circle")
    stage = field_stage((1.9, -1.1, 0), zoom=1.25, pitch=0.82, yaw=-0.2, half=3.6)
    track = Band(ring_points(ORIGIN, R, 160), 0.3, cfg.ROAD, edge=cfg.MUTED, centre_line=cfg.WHITE)
    stage.add_body(track)
    ramp = pm.SpeedingUp(P.r, OMEGA0, pm.ALPHA)
    car = Circuit(stage, ramp, R=R, body="car", color=cfg.CAR, car_length=0.62, kv=KV, ka=KA, phase=-np.pi / 2)
    v_arrow = car.add_arrow("v", width=0.08, lift=0.28)
    gauge = Speedometer([-6.2, 2.15, 0], top=4, radius=1.2, value=float(ramp.speed(0)), unit="m/s", step=1, unit_gap=0.22)
    gauge.value.value = float(ramp.speed(0))
    gauge.add_updater(lambda m: setattr(m.value, "value", float(ramp.speed(car.t))))
    show(scene, stage, 1.0, FadeIn(gauge))
    t_ramp = (OMEGA1 - OMEGA0) / pm.ALPHA            # 2 s of model time to go from 0.6 to 1.6 rad/s
    scene.play(stage.fade(v_arrow, 1.0), car.run(t_ramp * 0.3, t_ramp * 0.3 / SLOW), run_time=t_ramp * 0.3 / SLOW)

    # --- 2. Still turning: a_r = v^2 / r ---------------------------------------------------------------------------------------
    beat(scene, t, 1)
    a_r = car.add_arrow("a", width=0.08, lift=0.28)
    radial = eq(r"a_r = \frac{v^2}{r}", cfg.FONT["section"], cfg.ACCEL).move_to([-4.6, -0.2, 0])
    scene.play(FadeOut(head), stage.fade(a_r, 1.0), Write(radial), run_time=1.2)
    scene.play(car.run(t_ramp * 0.65, t_ramp * 0.35 / SLOW), run_time=t_ramp * 0.35 / SLOW)
    scene.play(*stage.turn(yaw=0.15, pitch=0.9, run_time=4.5), run_time=4.5)

    # --- 3. Speed changing too: a_t = dv/dt ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    a_t = car.add_arrow("at", width=0.08, lift=0.28)
    tangential = eq(r"a_t = \frac{dv}{dt}", cfg.FONT["section"], cfg.TANGENTIAL).next_to(radial, DOWN, buff=0.5)
    scene.play(stage.fade(a_t, 1.0), Write(tangential), run_time=1.2)
    scene.play(car.run(t_ramp, t_ramp * 0.35 / SLOW), run_time=t_ramp * 0.35 / SLOW)
    scene.play(*stage.turn(yaw=-0.2, pitch=0.82, run_time=4.5), run_time=4.5)

    # --- 4. Speeding up: along v. Slowing down: against v ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    # Hand over to the slowing-down motion at the same place and speed (alpha = -0.5).
    brake = pm.SpeedingUp(P.r, OMEGA1, -pm.ALPHA)
    here = car.view.theta(car.t)
    slow_car = Circuit(stage, brake, R=R, body="car", color=cfg.CAR, car_length=0.62, kv=KV, ka=KA, phase=here)
    for p in slow_car.parts:
        p.presence = 0.0
    arrows_b = [slow_car.add_arrow(k, width=0.08, lift=0.28) for k in ("v", "a", "at")]
    up = txt("speeding up: along v", cfg.FONT["small"], cfg.TANGENTIAL).move_to([2.0, 3.3, 0])
    scene.play(FadeIn(up), run_time=0.6)
    swap = [stage.fade(p, 0.0, run_time=0.2) for p in car.parts] + [stage.fade(a, 0.0, run_time=0.2) for a in car.arrows.values()]
    swap += [stage.fade(p, 1.0, run_time=0.2) for p in slow_car.parts] + [stage.fade(a, 1.0, run_time=0.2) for a in arrows_b]
    scene.play(*swap, run_time=0.2)
    gauge.clear_updaters()
    gauge.add_updater(lambda m: setattr(m.value, "value", float(brake.speed(slow_car.t))))
    down = txt("slowing down: against v", cfg.FONT["small"], cfg.TANGENTIAL).move_to([2.0, 3.3, 0])
    scene.play(fade_through(up, down), slow_car.run(0.3, 0.6), run_time=0.6)
    scene.play(slow_car.run(t_ramp * 0.8, (t_ramp * 0.8 - 0.3) / SLOW * 0.9), run_time=(t_ramp * 0.8 - 0.3) / SLOW * 0.9)

    # --- 5. On a fixed circle: a_t = r alpha -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    gauge.clear_updaters()
    rate = eq(r"a_\theta = r\,\alpha", cfg.FONT["section"], cfg.TANGENTIAL).next_to(tangential, DOWN, buff=0.5)
    scene.play(FadeOut(down), Write(rate), run_time=1.2)
    scene.play(*stage.turn(yaw=0.05, run_time=2.4), run_time=2.4)

    # --- 6. a = -r omega^2 r-hat + r alpha theta-hat --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    full = eq([r"\vec a", "=", r"-r\omega^2\,\hat r", "+", r"r\alpha\,\hat\theta"], cfg.FONT["section"])
    paint(full, {0: cfg.WHITE, 2: cfg.ACCEL, 4: cfg.TANGENTIAL})
    fit_width(full, 7.6)
    full.move_to([2.0, 3.3, 0])
    scene.play(FadeOut(VGroup(radial, tangential, rate, gauge)), Write(full), run_time=1.6)
    hats = []
    for kind, color, name in (("r", cfg.POSITION, r"\hat r"), ("t", cfg.TANGENTIAL, r"\hat\theta")):
        def tip(kind=kind):
            u = slow_car.view.unit_r(slow_car.t) if kind == "r" else slow_car.view.unit_t(slow_car.t)
            return slow_car.world() + UP * 0.28 + ground_vec(u) * 0.75
        vec = Vector(lambda: slow_car.world() + UP * 0.28, tip, color, width=0.055, tip=0.2, glow=False)
        label = Tag(eq(name, cfg.FONT["body"], color), tip, UP * 0.3)
        vec.presence = label.presence = 0.0
        stage.add_overlay(vec, label)
        hats += [vec, label]
    scene.play(*[stage.fade(a, 0.0) for a in arrows_b], *[stage.fade(h, 1.0) for h in hats], run_time=0.9)
    outward = VGroup(eq(r"\hat r", cfg.FONT["small"], cfg.POSITION), txt("outward", cfg.FONT["tiny"], cfg.WHITE),
                     eq(r"\hat\theta", cfg.FONT["small"], cfg.TANGENTIAL), txt("along +tangent", cfg.FONT["tiny"], cfg.WHITE))
    outward.arrange(RIGHT, buff=0.2).next_to(full, DOWN, buff=0.35)
    scene.play(FadeIn(outward), run_time=0.7)
    scene.play(*stage.turn(yaw=-0.25, pitch=0.95, run_time=3.5), run_time=3.5)

    # --- 7. Perpendicular parts: |a| = sqrt(a_r^2 + a_t^2) ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    total = slow_car.add_arrow("atot", width=0.09, lift=0.28)
    scene.play(*[stage.fade(h, 0.0) for h in hats], *[stage.fade(a, 1.0) for a in arrows_b], stage.fade(total, 1.0), FadeOut(outward), run_time=0.9)
    size = eq(r"|\vec a| = \sqrt{a_r^2 + a_t^2}", cfg.FONT["section"], cfg.WHITE).move_to([-4.4, 2.2, 0])
    scene.play(Write(size), run_time=1.4)
    scene.play(slow_car.run(slow_car.t + 0.4, 0.4 / SLOW), run_time=0.4 / SLOW)

    # --- 8. The brief's instant: v = 4 m/s on 2 m: a_r = 8 ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    hide(scene, stage, 0.8, FadeOut(VGroup(full, size)))
    instant = pm.SpeedingUp(P.r, P.angular_speed, pm.ALPHA)       # at t = 0: v = 4 m/s, alpha = 0.5
    flat = CircleView([-3.6, -0.5, 0], 2.3, instant, kv=1.0 / P.v, ka=1.7 / P.accel, phase=0.45)
    a_r2, a_t2, a_tot = flat.arrow("a", width=0.09), flat.arrow("at", width=0.09), flat.arrow("atot", width=0.09)
    v2 = flat.arrow("v", width=0.09)
    for a in (a_t2, a_tot):
        a.alpha = 0.0
    scene.add(flat.ring, flat.hub, flat.ball, v2, a_r2, a_t2, a_tot)
    scene.play(FadeIn(VGroup(flat.ring, flat.hub, flat.ball)), v2.grow_in(run_time=0.8), a_r2.grow_in(run_time=0.8), run_time=0.8)
    s1 = eq([r"a_r", "=", rf"\frac{{{V}^2}}{{{R_M}}}", "=", rf"{AC}\ \mathrm{{m/s^2}}"], cfg.FONT["body"])
    paint(s1, {0: cfg.ACCEL, 4: cfg.ACCEL}).move_to([3.4, 2.6, 0])
    scene.play(Write(s1), run_time=1.4)

    # --- 9. alpha = 0.5: a_t = 2 (0.5) = 1 -----------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    s2 = eq([r"a_t", "=", r"r\,\alpha", "=", rf"{R_M}\,({fx(pm.ALPHA, 1)})", "=", rf"{wh(pm.tangential_accel())}\ \mathrm{{m/s^2}}"], cfg.FONT["body"])
    paint(s2, {0: cfg.TANGENTIAL, 6: cfg.TANGENTIAL}).next_to(s1, DOWN, buff=0.55)
    given = eq(rf"\alpha = {fx(pm.ALPHA, 1)}\ \mathrm{{rad/s^2}}", cfg.FONT["small"], cfg.ANGLE).next_to(s2, DOWN, buff=0.3)
    scene.play(FadeIn(given), Write(s2), a_t2.fade_to(1.0, run_time=1.4), run_time=1.4)

    # --- 10. |a| = sqrt(64 + 1) ~ 8.06, tipped forward ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    s3 = eq([r"|\vec a|", "=", rf"\sqrt{{{wh(P.accel ** 2)} + {wh(pm.tangential_accel() ** 2)}}}", r"\approx",
             rf"{fx(pm.total_accel(), 2)}\ \mathrm{{m/s^2}}"], cfg.FONT["body"])
    paint(s3, {0: cfg.WHITE, 4: cfg.WHITE}).next_to(given, DOWN, buff=0.55)
    scene.play(Write(s3), a_tot.fade_to(1.0, run_time=1.4), run_time=1.4)
    p = flat.point()
    inward = np.arctan2(*(flat.c - p)[1::-1])
    # Counterclockwise motion: the velocity is 90 degrees clockwise of inward, so "forward" is clockwise.
    tilt = arc_mark(p, 0.95, inward - np.radians(pm.total_accel_tilt_deg()), inward, cfg.WHITE, 4)
    tilt_tag = eq(rf"{fx(pm.total_accel_tilt_deg(), 1)}^\circ\ \text{{forward}}", cfg.FONT["small"], cfg.WHITE)
    tilt_tag.next_to(s3, DOWN, buff=0.4)
    scene.play(Create(tilt), FadeIn(tilt_tag), run_time=0.9)
    scene.play(FadeIn(boxed(s3[4], cfg.RESULT, 0.12)[0]), run_time=0.7)

    # --- 11. One part turns v; the other stretches it ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    roles = VGroup(txt("turns v", cfg.FONT["label"], cfg.ACCEL), txt("stretches v", cfg.FONT["label"], cfg.TANGENTIAL)).arrange(RIGHT, buff=0.8)
    roles.move_to([-3.6, 3.3, 0])
    scene.play(FadeIn(roles, shift=DOWN * 0.1), Indicate(a_r2, color=cfg.ACCEL, scale_factor=1.05), run_time=1.2)
    scene.play(Indicate(a_t2, color=cfg.TANGENTIAL, scale_factor=1.3), run_time=1.2)
    scene.wait(1.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["22"])
