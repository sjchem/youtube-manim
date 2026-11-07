"""Scene 18 — why cars need friction. A car laps a flat circular road of
radius 50 m (``physics_models.CURVE_RADIUS``) on a 3D ground; static
friction (green, toward the centre) is the only horizontal force. The
derivation runs down the left: N = mg, f_s <= mu_s m g, m v^2 / r <= mu_s m g,
the mass cancels, v_max = sqrt(mu_s g r) ~ 17.15 m/s ~ 61.7 km/h.

A meter compares the acceleration needed with the most friction can give
(mu_s g = 5.88 m/s^2). At 15 m/s (4.5 needed) car A holds the curve. At
20 m/s (8 needed) car B cannot: with friction at its limit, the tightest
bend it can make is r = v^2 / (mu_s g) ~ 68 m, so from its first moment on
the curve it follows that wider circle and drifts off the road. Both cars
run at 2x real time. An idealized model — not a safe-speed guide.
"""

from manim_scenes.common import *

R = 2.8
S = R / pm.CURVE_RADIUS            # stage units per metre
FILM = 2.0                         # model seconds per film second
COL = -4.75
AT = pm.max_friction_accel()       # 5.88 m/s^2


class Scene18CarFriction(Scene):
    def construct(self) -> None:
        play_scene(self)


def meter(needed: float, color: str) -> VGroup:
    """A bar of the acceleration needed against the friction limit (0 to 10 m/s^2)."""
    width, top = 5.2, 10.0
    frame = RoundedRectangle(width=width, height=0.42, corner_radius=0.1, stroke_color=cfg.MUTED, stroke_width=2,
                             fill_color=cfg.PANEL, fill_opacity=0.9)
    fill = Rectangle(width=width * needed / top, height=0.3, stroke_width=0, fill_color=color, fill_opacity=0.95)
    fill.align_to(frame, LEFT).shift(RIGHT * 0.06)
    limit = Line(UP * 0.36, DOWN * 0.36, stroke_color=cfg.FORCE, stroke_width=5).move_to(frame.get_left() + RIGHT * width * AT / top)
    group = VGroup(frame, fill, limit)
    group.limit = limit
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "18", "Why cars need friction")
    stage = field_stage((2.3, -1.15, 0), zoom=1.12, pitch=0.78, yaw=-0.15, half=5.0, step=0.7)
    road = Band(ring_points(ORIGIN, R, 160), 0.34, cfg.ROAD, edge=cfg.MUTED, centre_line=cfg.WHITE)
    stage.add_body(road)
    safe = pm.Circular(1200.0, pm.CURVE_RADIUS, pm.SAFE_SPEED, theta0=-np.pi / 2)
    car_a = Circuit(stage, safe, R=R, body="car", color=cfg.CAR, car_length=0.7, kv=0.06, ka=0.13)
    show(scene, stage, 1.2)
    scene.play(car_a.run(car_a.t + 5.5 * FILM, 5.5), run_time=5.5)

    # --- 2. Direction changes: an inward force, from static friction ----------------------------------------------------
    beat(scene, t, 1)
    friction = Vector(lambda: car_a.world() + UP * 0.25, lambda: car_a.world() + UP * 0.25 + ground_vec(car_a.view.acc_radial(car_a.t)) * 0.24,
                      cfg.FORCE, width=0.09, tip=0.27)
    friction.keep_in_frame = True
    friction.presence = 0.0
    stage.add_overlay(friction)
    tag = Tag(VGroup(eq(r"f_s", cfg.FONT["body"], cfg.FORCE), txt("static friction", cfg.FONT["small"], cfg.FORCE)).arrange(RIGHT, buff=0.2),
              lambda: car_a.world(), UP * 0.75)
    tag.presence = 0.0
    stage.add_overlay(tag)
    scene.play(FadeOut(head), stage.fade(friction, 1.0), car_a.run(car_a.t + 1.0 * FILM, 1.0), run_time=1.0)
    scene.play(stage.fade(tag, 1.0), car_a.run(car_a.t + 0.8 * FILM, 0.8), run_time=0.8)
    scene.play(car_a.run(car_a.t + 11.5 * FILM, 11.5), run_time=11.5)

    # --- 3. N = mg; friction up to mu_s m g ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    lines = VGroup(eq(r"N = mg", cfg.FONT["body"]), eq(r"f_s \le \mu_s N = \mu_s m g", cfg.FONT["body"], cfg.FORCE))
    lines.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([COL, 2.7, 0])
    scene.play(stage.fade(tag, 0.0), FadeIn(lines[0], shift=DOWN * 0.1), car_a.run(car_a.t + 1.0 * FILM, 1.0), run_time=1.0)
    scene.play(Write(lines[1]), car_a.run(car_a.t + 1.6 * FILM, 1.6), run_time=1.6)
    scene.play(car_a.run(car_a.t + 11.0 * FILM, 11.0), run_time=11.0)

    # --- 4. Needed <= available ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    need = eq([r"m", r"\frac{v^2}{r}", r"\le", r"\mu_s", r"m", r"g"], cfg.FONT["section"]).next_to(lines, DOWN, buff=0.55).align_to(lines, LEFT)
    scene.play(Write(need), car_a.run(car_a.t + 1.6 * FILM, 1.6), run_time=1.6)
    scene.play(car_a.run(car_a.t + 10.5 * FILM, 10.5), run_time=10.5)

    # --- 5. The mass cancels: v_max = sqrt(mu_s g r) ------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    cancel = VGroup(strike(need[0]), strike(need[4]))
    scene.play(Create(cancel), car_a.run(car_a.t + 0.8 * FILM, 0.8), run_time=0.8)
    reduced = eq(r"\frac{v^2}{r} \le \mu_s g", cfg.FONT["section"]).next_to(need, DOWN, buff=0.45).align_to(lines, LEFT)
    vmax = eq([r"v_{\max}", "=", r"\sqrt{\mu_s g r}"], cfg.FONT["section"])
    paint(vmax, {0: cfg.VELOCITY}).next_to(reduced, DOWN, buff=0.5).align_to(lines, LEFT)
    scene.play(Write(reduced), car_a.run(car_a.t + 1.2 * FILM, 1.2), run_time=1.2)
    scene.play(Write(vmax), car_a.run(car_a.t + 1.2 * FILM, 1.2), run_time=1.2)
    vmax_box = boxed(vmax, cfg.RESULT)[0]
    scene.play(FadeIn(vmax_box), car_a.run(car_a.t + 0.6 * FILM, 0.6), run_time=0.6)
    scene.play(car_a.run(car_a.t + 9.0 * FILM, 9.0), run_time=9.0)

    # --- 6. r = 50 m, mu_s = 0.6 ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    derivation = VGroup(lines, need, cancel, reduced)
    givens = VGroup(eq(rf"r = {wh(pm.CURVE_RADIUS)}\ \mathrm{{m}}", cfg.FONT["body"], cfg.POSITION),
                    eq(rf"\mu_s = {fx(pm.MU_S, 1)}", cfg.FONT["body"], cfg.FORCE)).arrange(RIGHT, buff=0.8).move_to([COL + 0.4, 2.9, 0])
    scene.play(FadeOut(derivation), car_a.run(car_a.t + 0.45 * FILM, 0.45), run_time=0.45)
    scene.play(VGroup(vmax, vmax_box).animate.move_to([COL + 0.4, 1.3, 0]), car_a.run(car_a.t + 0.45 * FILM, 0.45), run_time=0.45)
    scene.play(FadeIn(givens, shift=DOWN * 0.1), car_a.run(car_a.t + 0.8 * FILM, 0.8), run_time=0.8)
    scene.play(car_a.run(car_a.t + 5.5 * FILM, 5.5), run_time=5.5)

    # --- 7. ~17.15 m/s ~ 61.7 km/h -------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    value = eq(rf"v_{{\max}} = \sqrt{{{fx(pm.MU_S, 1)}\,({fx(pm.G, 1)})\,({wh(pm.CURVE_RADIUS)})}}", cfg.FONT["body"], cfg.VELOCITY)
    value.next_to(VGroup(vmax, vmax_box), DOWN, buff=0.5)
    result = eq(rf"\approx {fx(pm.max_curve_speed(), 2)}\ \mathrm{{m/s}} \approx {fx(pm.kmh(pm.max_curve_speed()), 1)}\ \mathrm{{km/h}}",
                cfg.FONT["body"], cfg.VELOCITY).next_to(value, DOWN, buff=0.35)
    for m in (value, result):
        fit_width(m, 6.2)
    scene.play(Write(value), car_a.run(car_a.t + 1.6 * FILM, 1.6), run_time=1.6)
    scene.play(Write(result), car_a.run(car_a.t + 1.6 * FILM, 1.6), run_time=1.6)
    scene.play(car_a.run(car_a.t + 9.5 * FILM, 9.5), run_time=9.5)

    # --- 8. Car A at 15 m/s: needs 4.5, friction gives up to 5.88: it holds -----------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(value, result, givens)), car_a.run(car_a.t + 0.4 * FILM, 0.4), run_time=0.4)
    scene.play(VGroup(vmax, vmax_box).animate.scale(0.7).move_to([COL + 0.2, 3.4, 0]), car_a.run(car_a.t + 0.4 * FILM, 0.4), run_time=0.4)
    bar_a = meter(pm.required_accel(pm.SAFE_SPEED), cfg.ACCEL).move_to([COL + 0.2, 1.5, 0])
    name_a = eq(rf"{wh(pm.SAFE_SPEED)}\ \mathrm{{m/s}}\ \to\ {fx(pm.required_accel(pm.SAFE_SPEED), 1)}\ \mathrm{{m/s^2}}",
                cfg.FONT["small"], cfg.ACCEL).next_to(bar_a, UP, buff=0.25)
    limit_tag = eq(rf"\mu_s g = {fx(AT, 2)}", cfg.FONT["small"], cfg.FORCE).next_to(bar_a.limit, DOWN, buff=0.2)
    holds = VGroup(check_mark(0.22), txt("holds the curve", cfg.FONT["small"], cfg.GREEN)).arrange(RIGHT, buff=0.2)
    holds.next_to(limit_tag, DOWN, buff=0.3).align_to(bar_a, LEFT)
    scene.play(FadeIn(bar_a), FadeIn(name_a), FadeIn(limit_tag), car_a.run(car_a.t + 1.2 * FILM, 1.2), run_time=1.2)
    scene.play(FadeIn(holds, shift=UP * 0.1), car_a.run(car_a.t + 0.8 * FILM, 0.8), run_time=0.8)
    scene.play(car_a.run(car_a.t + 10.5 * FILM, 10.5), run_time=10.5)

    # --- 9. Car B at 20 m/s: needs 8, more than friction can give: it drifts wide -----------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    # Car B starts on the road, nose along it. With friction at its limit it bends no tighter than
    # rho = v^2 / (mu_s g), so its path is the circle of radius rho that touches the road there.
    rho = pm.widest_bend_radius(pm.FAST_SPEED) * S
    start_angle = -np.pi / 2 + 0.9
    p_start = ground(R * np.cos(start_angle), R * np.sin(start_angle))
    centre_b = p_start + (ORIGIN - p_start) / np.linalg.norm(p_start) * rho
    phi0 = np.arctan2(-(p_start - centre_b)[2], (p_start - centre_b)[0])
    drift = Knob(0.0)                                  # model seconds on car B's path
    phi = lambda: phi0 + pm.FAST_SPEED / pm.widest_bend_radius(pm.FAST_SPEED) * drift.value  # noqa: E731
    where_b = lambda: centre_b + ground(rho * np.cos(phi()), rho * np.sin(phi()))  # noqa: E731
    car_b = car3d(stage, where_b, lambda: phi() + np.pi / 2, cfg.WARNING, 0.7)
    trail_b = Curve(lambda: np.array([centre_b + ground(rho * np.cos(phi0 + a), rho * np.sin(phi0 + a), 0.02)
                                      for a in np.linspace(0, max(phi() - phi0, 1e-3), 40)]), cfg.WARNING, width=4)
    for part in (*car_b, trail_b):
        part.presence = 0.0
    stage.add_body(trail_b)
    bar_b = meter(pm.required_accel(pm.FAST_SPEED), cfg.WARNING).move_to([COL + 0.2, -2.2, 0])
    name_b = eq(rf"{wh(pm.FAST_SPEED)}\ \mathrm{{m/s}}\ \to\ {wh(pm.required_accel(pm.FAST_SPEED))}\ \mathrm{{m/s^2}}",
                cfg.FONT["small"], cfg.WARNING).next_to(bar_b, UP, buff=0.25)
    slides = VGroup(cross_mark(0.2), txt("slides: drifts wide", cfg.FONT["small"], cfg.WARNING)).arrange(RIGHT, buff=0.2)
    slides.next_to(bar_b, DOWN, buff=0.3).align_to(bar_b, LEFT)
    scene.play(*[stage.fade(p, 0.0) for p in car_a.parts], stage.fade(friction, 0.0), FadeIn(bar_b), FadeIn(name_b), run_time=1.0)
    scene.play(*[stage.fade(p, 1.0) for p in car_b], stage.fade(trail_b, 1.0), run_time=0.6)
    span = 3.0                                          # model seconds on the wide path
    scene.play(drift.to(stage, span, run_time=span / FILM, rate_func=linear), FadeIn(slides, run_time=1.0), run_time=span / FILM)
    replay = chip("replay ×0.5", cfg.MUTED, cfg.FONT["tiny"]).move_to([2.3, 3.4, 0])
    scene.play(*[stage.fade(p, 0.0) for p in car_b], FadeIn(replay), run_time=0.4)
    drift.value = 0.0
    scene.play(*[stage.fade(p, 1.0) for p in car_b], run_time=0.3)
    scene.play(drift.to(stage, span, run_time=span / 0.5, rate_func=linear), run_time=span / 0.5)
    wide = Tag(eq(rf"r \approx {wh(round(pm.widest_bend_radius(pm.FAST_SPEED)))}\ \mathrm{{m}}", cfg.FONT["small"], cfg.WARNING),
               lambda: where_b(), RIGHT * 1.3 + UP * 0.3)
    wide.presence = 0.0
    stage.add_overlay(wide)
    scene.play(stage.fade(wide, 1.0), run_time=0.7)

    # --- 10. Demand grows with the square of speed ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    square = eq(r"\text{needed} \propto v^2", cfg.FONT["section"], cfg.ACCEL).move_to([2.3, 3.35, 0])
    scene.play(FadeOut(slides), fade_through(replay, square), Indicate(bar_b[1], color=cfg.WARNING, scale_factor=1.04), run_time=1.2)
    scene.play(*stage.turn(yaw=0.15, run_time=6.0), run_time=6.0)

    # --- 11. An idealized model ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    caveat = chip("idealized model · not a safe-speed guide", cfg.MUTED, cfg.FONT["small"]).move_to([2.3, 3.4, 0])
    scene.play(fade_through(square, caveat), run_time=0.9)
    scene.play(*stage.turn(yaw=-0.1, run_time=6.5), run_time=6.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["18"])
