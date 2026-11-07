"""Scene 13 — angular velocity. omega = d theta / dt beside v = dr / dt, its
unit and sign, and theta(t) = theta0 + omega t drawn live as a straight line
on a small theta-t graph. Differentiating s = r theta gives v = r|omega|.
Then a 3D turntable spinning at ``physics_models.TURNTABLE_OMEGA`` (2 rad/s,
played at 0.3x): two markers 1 m and 2 m from the axis finish every turn
together, but the outer one traces the longer path. Their velocity arrows
are drawn at true length: 2 m/s and 4 m/s. The outer marker is the
reference particle: 4 / 2 = 2 rad/s.
"""

from manim_scenes.common import *

C = np.array([-3.6, -0.5, 0])
R = 2.3
COL = 3.5
S3 = 1.25                                  # turntable: stage units per metre
SLOW = 0.3


class Scene13AngularVelocity(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Angular velocity")
    view = CircleView(C, R, P)
    r_arrow = view.arrow("r", width=0.08)
    angle = live(VMobject(), lambda: arc_mark(C, 0.6, 0.0, max(view.theta() % TAU, 1e-3), cfg.ANGLE))
    scene.play(FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), run_time=0.6)
    scene.add(r_arrow, angle)
    scene.play(r_arrow.grow_in(run_time=0.6), view.run(0.6, 0.6 / SLOW * 0.5), run_time=1.0)
    scene.play(view.run(1.3, 0.7 / SLOW), run_time=0.7 / SLOW)

    # --- 2. omega = d theta / dt, beside v = dr / dt -----------------------------------------------------------------------
    beat(scene, t, 1)
    pair = VGroup(paint(eq([r"\vec v", "=", r"\frac{d\vec r}{dt}"], cfg.FONT["section"]), {0: cfg.VELOCITY, 2: cfg.POSITION}),
                  paint(eq([r"\omega", "=", r"\frac{d\theta}{dt}"], cfg.FONT["section"]), {0: cfg.ANGLE, 2: cfg.ANGLE}))
    pair.arrange(RIGHT, buff=1.0).move_to([COL, 2.5, 0])
    scene.play(FadeOut(head), FadeIn(pair[0], shift=DOWN * 0.1), run_time=0.8)
    scene.play(Write(pair[1]), run_time=1.2)
    framed = boxed(pair[1], cfg.ANGLE)
    scene.play(FadeIn(framed[0]), view.run(view.clock.value + 0.6, 2.0), run_time=2.0)

    # --- 3. rad/s; counterclockwise positive ------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    unit = VGroup(txt("rad/s", cfg.FONT["label"], cfg.ANGLE), txt("counterclockwise: +", cfg.FONT["small"], cfg.WHITE),
                  txt("clockwise: −", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.22).next_to(pair, DOWN, buff=0.5)
    scene.play(FadeIn(unit, shift=UP * 0.1), view.run(view.clock.value + 0.5, 1.5), run_time=1.5)

    # --- 4. theta(t) = theta0 + omega t ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(unit), run_time=0.4)
    graph = Axes(x_range=(0, 3.2, 1), y_range=(0, 7, 2), x_length=4.4, y_length=2.6, tips=False,
                 axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3}).move_to([COL, -1.3, 0])
    labels = VGroup(eq("t", cfg.FONT["small"], cfg.TIME).next_to(graph.x_axis, RIGHT, buff=0.15),
                    eq(r"\theta", cfg.FONT["small"], cfg.ANGLE).next_to(graph.y_axis, UP, buff=0.12))
    line_eq = paint(eq([r"\theta(t)", "=", r"\theta_0 + \omega t"], cfg.FONT["body"]), {0: cfg.ANGLE, 2: cfg.ANGLE})
    line_eq.next_to(pair, DOWN, buff=0.5)
    view.clock.value = 0.0
    trace = live(VMobject(), lambda: VMobject(stroke_color=cfg.ANGLE, stroke_width=5).set_points_as_corners(
        [graph.c2p(s, float(view.theta(s))) for s in np.linspace(0, max(view.clock.value, 1e-3), 40)]))
    scene.play(FadeIn(graph), FadeIn(labels), Write(line_eq), run_time=1.2)
    scene.add(trace)
    scene.play(view.run(P.period, 5.5), run_time=5.5)
    straight = txt("a straight line: constant ω", cfg.FONT["tiny"], cfg.ANGLE).next_to(graph, DOWN, buff=0.25)
    scene.play(FadeIn(straight), run_time=0.6)

    # --- 5. From s = r theta ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    trace.clear_updaters()
    scene.play(FadeOut(VGroup(graph, labels, trace, straight, line_eq)), run_time=0.6)
    d1 = eq(r"s = r\,\theta", cfg.FONT["section"], cfg.CYAN).next_to(pair, DOWN, buff=0.6)
    d2 = eq(r"\frac{ds}{dt} = r\,\frac{d\theta}{dt}", cfg.FONT["section"]).next_to(d1, DOWN, buff=0.45)
    scene.play(Write(d1), run_time=1.0)
    scene.play(Write(d2), run_time=1.4)

    # --- 6. v = r |omega| ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    result = paint(eq([r"v", "=", r"r\,|\omega|"], cfg.FONT["title"]), {0: cfg.VELOCITY, 2: cfg.ANGLE}).next_to(d2, DOWN, buff=0.55)
    scene.play(Write(result), run_time=1.2)
    scene.play(FadeIn(boxed(result, cfg.RESULT)[0]), view.run(view.clock.value + 0.4, 1.0), run_time=1.0)

    # --- 7. A spinning turntable ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    angle.clear_updaters()
    clear(scene, run_time=0.7)
    stage = Stage((0.0, -0.9, 0), zoom=1.35, yaw=-0.2, pitch=0.78, sway=0.03)
    spin = Knob(0.0)                                   # seconds of turntable time
    turn = lambda: pm.TURNTABLE_OMEGA * spin.value    # noqa: E731
    radius = 2.7
    base = Disc(np.array([0, -0.14, 0]), radius + 0.1, "#0B2236", opacity=1.0, stroke=cfg.MUTED)
    platter = Disc(np.array([0, 0.0, 0]), radius, cfg.PANEL_2, opacity=0.97, stroke=mu.mix(cfg.MUTED, cfg.WHITE, 0.3))
    spokes = [Segment(np.array([0, 0.01, 0]), lambda k=k: ground(radius * np.cos(turn() + k * PI / 3), radius * np.sin(turn() + k * PI / 3), 0.01),
                      cfg.MUTED, width=2.4, opacity=0.55) for k in range(6)]
    spindle = Ball(np.array([0, 0.1, 0]), 0.12, "#9DB4C7", layers=14)
    where = lambda r_m: (lambda: ground(r_m * S3 * np.cos(turn()), r_m * S3 * np.sin(turn()), 0.16))  # noqa: E731
    inner, outer = (Ball(where(r_m), 0.16, color) for r_m, color in zip(pm.TURNTABLE_RADII, (cfg.CYAN, cfg.BALL)))
    for m in (inner, outer):
        m.keep_in_frame = True
    stage.add_body(base, platter, *spokes, spindle, inner, outer)
    show(scene, stage, 1.0)
    scene.play(spin.to(stage, 1.2, run_time=1.2 / SLOW, rate_func=linear))

    # --- 8. Both finish every turn together: the same omega ------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    same = paint(eq([r"\text{same }", r"\omega"], cfg.FONT["section"]), {1: cfg.ANGLE}).move_to([4.6, 3.2, 0])
    scene.play(FadeIn(same, shift=DOWN * 0.1), spin.to(stage, 1.5, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(spin.to(stage, 2.6, run_time=1.1 / SLOW, rate_func=linear))

    # --- 9. The outer marker travels the longer path ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    a0 = turn()           # the paths traced in the room, from this moment on
    trails = [Curve(lambda r_m=r_m: ring_points(ORIGIN, r_m * S3, 80, a0, max(turn(), a0 + 1e-3), h=0.03, closed=False),
                    color, width=5)
              for r_m, color in zip(pm.TURNTABLE_RADII, (cfg.CYAN, cfg.BALL))]
    stage.add_body(*trails)
    arrows = []
    for r_m, ball in zip(pm.TURNTABLE_RADII, (inner, outer)):
        speed = r_m * pm.TURNTABLE_OMEGA
        vec = Vector(lambda b=ball: b.where(), lambda b=ball, sp=speed: b.where() + ground_vec([-np.sin(turn()) * sp * 0.33,
                                                                                                 np.cos(turn()) * sp * 0.33]),
                     cfg.VELOCITY, width=0.08, tip=0.24)
        vec.keep_in_frame = True
        vec.presence = 0.0
        stage.add_overlay(vec)
        arrows.append(vec)
    scene.play(*[stage.fade(a, 1.0) for a in arrows], spin.to(stage, spin.value + 0.4, run_time=1.0, rate_func=linear), run_time=1.0)
    scene.play(spin.to(stage, spin.value + 2.6, run_time=2.6 / SLOW * 0.95, rate_func=linear))

    # --- 10. 1 m -> 2 m/s; 2 m -> 4 m/s ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    inner_v, outer_v = pm.turntable_speeds()
    speeds = VGroup(eq(rf"r = {wh(pm.TURNTABLE_RADII[0])}\ \mathrm{{m}}:\ \ v = {wh(inner_v)}\ \mathrm{{m/s}}", cfg.FONT["body"], cfg.CYAN),
                    eq(rf"r = {wh(pm.TURNTABLE_RADII[1])}\ \mathrm{{m}}:\ \ v = {wh(outer_v)}\ \mathrm{{m/s}}", cfg.FONT["body"], cfg.BALL))
    speeds.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-4.3, 3.0, 0])
    rate = eq(rf"\omega = {OMEGA}\ \mathrm{{rad/s}}", cfg.FONT["body"], cfg.ANGLE).next_to(same, DOWN, buff=0.3)
    scene.play(FadeIn(rate), FadeIn(speeds[0]), spin.to(stage, spin.value + 0.4, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(FadeIn(speeds[1]), spin.to(stage, spin.value + 0.4, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(spin.to(stage, spin.value + 2.6, run_time=2.6 / SLOW, rate_func=linear))

    # --- 11. The outer point is our particle: 4 / 2 = 2 rad/s ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    ours = eq([r"|\omega|", "=", r"\frac{v}{r}", "=", rf"\frac{{{V}}}{{{R_M}}}", "=", rf"{OMEGA}\ \mathrm{{rad/s}}"], cfg.FONT["section"])
    paint(ours, {0: cfg.ANGLE, 6: cfg.ANGLE})
    fit_width(ours, 7.4)
    ours.move_to([-3.9, 3.0, 0])
    halo_outer = Halo(outer, cfg.BALL, reach=2.6, peak=0.22)
    halo_outer.presence = 0.0
    stage.add_body(halo_outer)
    scene.play(FadeOut(speeds), run_time=0.4)
    scene.play(stage.fade(halo_outer, 1.0), stage.fade(arrows[0], 0.0), stage.fade(trails[0], 0.0),
               Write(ours), spin.to(stage, spin.value + 0.5, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(spin.to(stage, spin.value + 3.4, run_time=3.4 / SLOW, rate_func=linear))
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
