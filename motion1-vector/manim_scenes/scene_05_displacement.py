"""Scene 05 — distance vs displacement, on a 3D field seen from above.

The brief's walk (``physics_models.WALK``): 3 m east, then 4 m north. The
path is counted (7 m), the green displacement arrow is measured (5 m at
53.1 degrees north of east). Then one lap of a standard 400 m track
(``physics_models.track_point``): two live counters show distance growing
without pause while the displacement arrow stretches, swings and shrinks
back to zero.
"""

from manim_scenes.common import *

WALK_S = 0.85                      # stage units per metre for the walk
START = np.array([-1.5, 0.0, 1.55])
TRACK_S = 0.058                    # stage units per metre for the track


class Scene05Displacement(Scene):
    def construct(self) -> None:
        play_scene(self)


def ground_point(east: float, north: float, scale: float, origin=START) -> np.ndarray:
    """Metres east / north -> a stage point on the ground (north runs away from the viewer)."""
    return np.asarray(origin, dtype=float) + np.array([east * scale, 0.0, -north * scale])


def counter(name: str, color: str, getter, decimals: int = 0) -> VGroup:
    title = txt(name, cfg.FONT["small"], color)
    value = DecimalNumber(getter(), num_decimal_places=decimals, font_size=84, color=cfg.WHITE)
    unit = txt("m", cfg.FONT["label"], cfg.MUTED)
    row = VGroup(title, value, unit)

    def follow(m):   # one updater, so the unit always moves after the number has changed width
        value.set_value(getter())
        unit.next_to(value, RIGHT, buff=0.34, aligned_edge=DOWN)

    row.add_updater(follow)
    value.next_to(title, DOWN, buff=0.24, aligned_edge=LEFT)
    unit.next_to(value, RIGHT, buff=0.34, aligned_edge=DOWN)
    row.value = value
    return row


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "Distance vs displacement")
    stage = field_stage((-3.6, -0.75, 0), zoom=1.24, yaw=0.0, pitch=0.95, x_range=(-3.0, 3.4), z_range=(-3.0, 2.6),
                        step=0.85 / 2, sway=0.03)
    show(scene, stage, 1.2)
    rose = compass([-6.5, -2.9, 0], 0.5)
    scene.play(FadeIn(rose), run_time=0.6)

    # --- 2. Distance: the whole path. Displacement: start to finish -----------------------------------------------
    beat(scene, t, 1)
    walked = Knob(0.0)                     # metres walked along the path
    legs = [np.array(v) for v in pm.WALK]

    def walker_metres(d: float) -> np.ndarray:
        first = pm.magnitude(legs[0])
        if d <= first:
            return legs[0] * d / first
        return legs[0] + legs[1] * (d - first) / pm.magnitude(legs[1])

    here = lambda: ground_point(*walker_metres(walked.value), WALK_S)  # noqa: E731
    walker = Ball(lambda: here() + np.array([0, 0.18, 0]), 0.18, cfg.POSITION)
    start_pin = Disc(START + np.array([0, 0.01, 0]), 0.16, cfg.WHITE, opacity=0.9)

    def trail():
        d = walked.value
        pts = [walker_metres(x) for x in np.linspace(0, d, 30)] if d > 0.01 else []
        return [ground_point(*p, WALK_S) + np.array([0, 0.02, 0]) for p in pts]

    path = Curve(trail, cfg.CYAN, width=5)
    stage.add_body(start_pin, path, walker)
    labels = VGroup(txt("distance:", cfg.FONT["label"], cfg.CYAN), txt("the whole path", cfg.FONT["label"], cfg.WHITE),
                    txt("displacement:", cfg.FONT["label"], cfg.POSITION),
                    txt("start → finish", cfg.FONT["label"], cfg.WHITE))
    for a, b in ((0, 1), (2, 3)):
        labels[b].next_to(labels[a], RIGHT, buff=0.25)
    VGroup(labels[0], labels[1]).move_to([0, 3.6, 0])
    VGroup(labels[2], labels[3]).move_to([0, 2.7, 0])
    scene.play(FadeOut(head), FadeIn(VGroup(labels[0], labels[1]), shift=DOWN * 0.15), run_time=0.9)
    scene.wait(2.0)
    scene.play(FadeIn(VGroup(labels[2], labels[3]), shift=DOWN * 0.15), run_time=0.9)

    # --- 3. delta r = r_f - r_i ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    delta = eq([r"\Delta\vec{r}", "=", r"\vec{r}_f", "-", r"\vec{r}_i"], cfg.FONT["section"], cfg.POSITION)
    delta.move_to([0, 2.55, 0])
    scene.play(FadeOut(labels), run_time=0.5)
    scene.play(Write(delta), run_time=1.4)

    # --- 4. Walk 3 m east ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(delta.animate.scale(0.75).move_to([-4.7, 3.5, 0]), run_time=0.8)
    east_len = pm.magnitude(legs[0])
    scene.play(walked.to(stage, east_len, run_time=2.4, rate_func=linear))
    leg1 = Tag(eq(r"3\ \mathrm{m}", cfg.FONT["body"], cfg.CYAN), ground_point(1.5, 0, WALK_S), DOWN * 0.5)
    leg1.presence = 0.0
    stage.add_overlay(leg1)
    scene.play(stage.fade(leg1, 1.0), run_time=0.5)

    # --- 5. Then 4 m north ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(walked.to(stage, east_len + pm.magnitude(legs[1]), run_time=3.0, rate_func=linear))
    leg2 = Tag(eq(r"4\ \mathrm{m}", cfg.FONT["body"], cfg.CYAN), ground_point(3, 2, WALK_S), RIGHT * 0.75)
    leg2.presence = 0.0
    stage.add_overlay(leg2)
    scene.play(stage.fade(leg2, 1.0), run_time=0.5)

    # --- 6. Distance: 3 + 4 = 7 m -------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    total = sum(pm.magnitude(v) for v in legs)
    dist_eq = eq([r"d", "=", r"3 + 4", "=", rf"{total:.0f}\ \mathrm{{m}}"], cfg.FONT["body"])
    paint(dist_eq, {0: cfg.CYAN, 4: cfg.CYAN})
    dist_eq.move_to([0.9, 2.0, 0], aligned_edge=LEFT)
    scene.play(Write(dist_eq), run_time=1.4)

    # --- 7. Displacement: the straight arrow, 5 m by Pythagoras -------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    end_pt = ground_point(*pm.add(*pm.WALK), WALK_S)
    disp = Vector(START + np.array([0, 0.03, 0]), end_pt + np.array([0, 0.03, 0]), cfg.RESULT, width=0.11, tip=0.34)
    disp_grow = Knob(0.0)
    disp.end = lambda: START + (end_pt - START) * disp_grow.value + np.array([0, 0.03, 0])
    stage.add_overlay(disp)
    scene.play(disp_grow.to(stage, 1.0, run_time=1.4))
    magnitude = pm.magnitude(pm.add(*pm.WALK))
    pyth = eq([r"|\Delta\vec{r}|", "=", r"\sqrt{3^2 + 4^2}", "=", rf"{magnitude:.0f}\ \mathrm{{m}}"], cfg.FONT["body"])
    paint(pyth, {0: cfg.RESULT, 4: cfg.RESULT})
    pyth.next_to(dist_eq, DOWN, buff=0.5).align_to(dist_eq, LEFT)
    scene.play(Write(pyth), run_time=1.8)
    five = Tag(eq(r"5\ \mathrm{m}", cfg.FONT["body"], cfg.RESULT), (START + end_pt) / 2, LEFT * 0.8 + UP * 0.25)
    five.presence = 0.0
    stage.add_overlay(five)
    scene.play(stage.fade(five, 1.0), run_time=0.6)

    # --- 8. Direction: tan^-1(4/3) = 53.1 degrees north of east -------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    theta = pm.direction_deg(pm.add(*pm.WALK))
    arc_pts = [START + 0.95 * np.array([np.cos(np.radians(a)), 0.02, -np.sin(np.radians(a))]) for a in np.linspace(0, theta, 24)]
    arc = Curve(arc_pts, cfg.GOLD, width=4)
    stage.add_body(arc)
    angle_eq = eq([r"\theta", "=", r"\tan^{-1}\!\left(\tfrac{4}{3}\right)", r"\approx", rf"{md.fixed(theta, 1)}^\circ"],
                  cfg.FONT["body"])
    paint(angle_eq, {0: cfg.GOLD, 4: cfg.GOLD})
    angle_eq.next_to(pyth, DOWN, buff=0.5).align_to(pyth, LEFT)
    scene.play(Write(angle_eq), run_time=1.6)
    noe = txt("north of east", cfg.FONT["small"], cfg.GOLD).next_to(angle_eq, DOWN, buff=0.25).align_to(angle_eq, RIGHT)
    scene.play(FadeIn(noe), run_time=0.6)

    # --- 9. 7 m travelled, 5 m of displacement ----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(Indicate(dist_eq[4], color=cfg.CYAN, scale_factor=1.2), run_time=1.0)
    scene.play(Indicate(pyth[4], color=cfg.RESULT, scale_factor=1.2), run_time=1.0)
    two_q = txt('distance · displacement', cfg.FONT["label"], cfg.WHITE).move_to([3.6, -2.6, 0])
    scene.play(FadeIn(two_q, shift=UP * 0.15), run_time=0.8)

    # --- 10. One lap of a 400 m track ----------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    hide(scene, stage, 0.8, FadeOut(VGroup(dist_eq, pyth, angle_eq, noe, two_q, delta, rose)))
    track = field_stage((-1.4, -1.1, 0), zoom=1.0, yaw=0.0, pitch=0.85, x_range=(-6.0, 6.0), z_range=(-3.2, 3.2),
                        step=0.5, sway=0.03)
    centre_y = pm.track_point(pm.TRACK_LAP / 2)[1] / 2
    on_track = lambda e, n: np.array([e * TRACK_S, 0.0, -(n - centre_y) * TRACK_S])  # noqa: E731
    loop = [on_track(*pm.track_point(s)) + np.array([0, 0.01, 0]) for s in np.linspace(0, pm.TRACK_LAP, 120)]
    lane = Curve(loop, "#C0583F", width=26, glow=False, opacity=0.9, bias=-2e3)
    line = Curve(loop, cfg.WHITE, width=2, glow=False, opacity=0.55, bias=-1.9e3)
    run = Knob(0.0)
    runner_at = lambda: on_track(*pm.track_point(run.value))  # noqa: E731
    runner = Ball(lambda: runner_at() + np.array([0, 0.17, 0]), 0.17, cfg.POSITION)
    origin_pt = on_track(*pm.track_point(0.0))
    flag = Disc(origin_pt + np.array([0, 0.02, 0]), 0.14, cfg.WHITE, opacity=0.95)
    track.add_body(lane, line, flag, runner)
    arrow = Vector(origin_pt + np.array([0, 0.05, 0]), lambda: runner_at() + np.array([0, 0.05, 0]), cfg.RESULT,
                   width=0.09, tip=0.28)
    track.add_overlay(arrow)
    show(scene, track, 1.0)
    dist_c = counter("distance", cfg.CYAN, lambda: run.value)
    disp_c = counter("displacement", cfg.RESULT, lambda: pm.magnitude(pm.track_point(run.value)))
    readouts = VGroup(dist_c, disp_c).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([5.5, 0.4, 0])
    back = panel(3.9, readouts.height + 0.8).move_to(readouts)
    scene.play(FadeIn(back), FadeIn(readouts), run_time=0.8)

    # --- 11-12. Distance only grows; displacement stretches, swings, shrinks ------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(run.to(track, pm.TRACK_LAP, run_time=19.5, rate_func=linear))

    # --- 13. 400 m of distance, zero displacement ----------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    for m in (dist_c, disp_c):
        m.clear_updaters()
    scene.play(Indicate(dist_c[1], color=cfg.CYAN, scale_factor=1.1), run_time=1.0)
    scene.play(Indicate(disp_c[1], color=cfg.RESULT, scale_factor=1.1), run_time=1.0)
    zero = result_label("zero displacement", cfg.RESULT, cfg.FONT["section"]).move_to([-1.4, 3.3, 0])
    scene.play(FadeIn(zero, shift=DOWN * 0.15), run_time=0.8)

    # --- 14. Scalars vs vectors ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    hide(scene, track, 0.9, FadeOut(VGroup(readouts, back, zero)))
    left = VGroup(txt("scalar", cfg.FONT["title"], cfg.CYAN), txt("magnitude", cfg.FONT["body"], cfg.WHITE),
                  txt("distance: 400 m", cfg.FONT["label"], cfg.CYAN)).arrange(DOWN, buff=0.35)
    right = VGroup(txt("vector", cfg.FONT["title"], cfg.RESULT), txt("magnitude + direction", cfg.FONT["body"], cfg.WHITE),
                   txt("displacement: 0", cfg.FONT["label"], cfg.RESULT)).arrange(DOWN, buff=0.35)
    pair = VGroup(left, right).arrange(RIGHT, buff=1.6).move_to(UP * 0.2)
    divider_x = (left.get_right()[0] + right.get_left()[0]) / 2
    divider = Line(UP * 1.6, DOWN * 1.6, stroke_color=cfg.MUTED, stroke_width=2)
    divider.move_to([divider_x, pair.get_center()[1], 0])
    scene.play(FadeIn(left, shift=RIGHT * 0.2), FadeIn(right, shift=LEFT * 0.2), Create(divider), run_time=1.4)
    scene.play(LaggedStart(Indicate(left[2], color=cfg.CYAN), Indicate(right[2], color=cfg.RESULT), lag_ratio=0.5),
               run_time=2.0)
    scene.wait(5.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
