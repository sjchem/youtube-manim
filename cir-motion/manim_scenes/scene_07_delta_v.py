"""Scene 07 — which way does delta v point? Two moments on the reference
circle, theta1 fixed and theta2 = theta1 + gap. Their equal-length velocities
slide to a shared tail on a workbench, and delta v runs tip to tip. Carried
back to the circle from the arc's midpoint it aims exactly at the centre
(``physics_models.verify`` checks this for any gap). Then the second moment
closes in on the first: the average acceleration delta v / delta t, drawn
from the first moment at its true size, swings onto the radius and settles
at v^2 / r. Centripetal = centre-seeking; v . a = 0.
"""

from manim_scenes.common import *

C = np.array([-3.4, -0.55, 0])
R = 2.5
THETA1 = 20 * DEGREES
BENCH = np.array([5.2, -2.45, 0])       # shared tail on the workbench, below the equations
KV = 1.9 / P.v
KA = 1.6 / P.accel


class Scene07DeltaV(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "07")
    chapter_open(scene, 3, "Why circular motion requires acceleration")
    head = heading("Where does Δv point?")
    view = CircleView(C, R, P, kv=KV, ka=KA, phase=THETA1 - 1.2)
    v_live = view.arrow("v", width=0.09)
    scene.play(FadeIn(head, shift=DOWN * 0.18), FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), run_time=0.8)
    scene.add(v_live)
    scene.play(v_live.grow_in(run_time=0.6), run_time=0.6)
    scene.play(view.run(1.2 / P.angular_speed + P.period * 0.5, 6.0), run_time=6.0)
    scene.play(v_live.fade_to(0.0, run_time=0.6), FadeOut(view.ball), run_time=0.6)

    # --- 2. v1 at one instant, v2 a moment later ------------------------------------------------------------------------
    beat(scene, t, 1)
    gap = Knob(80 * DEGREES)
    th1 = lambda: THETA1  # noqa: E731
    th2 = lambda: THETA1 + gap.value  # noqa: E731
    point = lambda th: view.at_angle(th)  # noqa: E731
    vel = lambda th: P.v * np.array([-np.sin(th), np.cos(th), 0.0])  # noqa: E731
    dots = VGroup(bead(point(th1()), cfg.BALL, 0.15), bead(point(th2()), cfg.BALL, 0.15))
    dots[1].add_updater(lambda m: m.move_to(point(th2())))
    v1 = VecArrow(lambda: point(th1()), lambda: point(th1()) + vel(th1()) * KV, cfg.VELOCITY, width=0.09)
    v2 = VecArrow(lambda: point(th2()), lambda: point(th2()) + vel(th2()) * KV, cfg.VELOCITY, width=0.09)
    tags = VGroup(eq(r"\vec v_1", cfg.FONT["body"], cfg.VELOCITY), eq(r"\vec v_2", cfg.FONT["body"], cfg.VELOCITY))
    tags[0].next_to(point(th1()) + vel(th1()) * KV, RIGHT, buff=0.15)
    tags[1].next_to(point(th2()) + vel(th2()) * KV, UP, buff=0.15)
    scene.play(FadeOut(head), FadeIn(dots[0]), run_time=0.5)
    scene.add(v1)
    scene.play(v1.grow_in(run_time=0.8), FadeIn(tags[0]), run_time=0.8)
    scene.play(FadeIn(dots[1]), run_time=0.5)
    scene.add(v2)
    scene.play(v2.grow_in(run_time=0.8), FadeIn(tags[1]), run_time=0.8)

    # --- 3. Equal lengths -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    equal = eq(r"|\vec v_1| = |\vec v_2| = v", cfg.FONT["body"], cfg.VELOCITY).move_to([3.6, 3.2, 0])
    scene.play(FadeIn(equal, shift=DOWN * 0.1), run_time=0.8)

    # --- 4. Slide them to a shared tail: delta v from tip to tip ----------------------------------------------------------------------------
    beat(scene, t, 3)
    slide = Knob(0.0)
    tail1 = lambda: point(th1()) + (BENCH - point(th1())) * slide.value  # noqa: E731
    tail2 = lambda: point(th2()) + (BENCH - point(th2())) * slide.value  # noqa: E731
    c1 = VecArrow(tail1, lambda: tail1() + vel(th1()) * KV, cfg.VELOCITY, width=0.09)
    c2 = VecArrow(tail2, lambda: tail2() + vel(th2()) * KV, cfg.VELOCITY, width=0.09)
    c1.alpha = c2.alpha = 0.0
    scene.add(c1, c2)
    scene.play(c1.fade_to(0.7, run_time=0.4), c2.fade_to(0.7, run_time=0.4), run_time=0.4)
    scene.play(slide.to(c1, 1.0, run_time=2.4), run_time=2.4)
    bench_tags = VGroup(eq(r"\vec v_1", cfg.FONT["small"], cfg.VELOCITY), eq(r"\vec v_2", cfg.FONT["small"], cfg.VELOCITY))
    bench_tags[0].next_to(BENCH + vel(th1()) * KV, RIGHT, buff=0.12)
    bench_tags[1].next_to(BENCH + vel(th2()) * KV, DOWN, buff=0.15)
    scene.play(FadeIn(bench_tags), c1.fade_to(1.0, run_time=0.5), c2.fade_to(1.0, run_time=0.5), run_time=0.5)
    dv = VecArrow(lambda: BENCH + vel(th1()) * KV, lambda: BENCH + vel(th2()) * KV, cfg.DELTA_V, width=0.1)
    scene.add(dv)
    scene.play(dv.grow_in(run_time=1.2), run_time=1.2)
    dv_tag = eq(r"\Delta\vec v", cfg.FONT["body"], cfg.DELTA_V).move_to(BENCH + (vel(th1()) + vel(th2())) * KV / 2 + LEFT * 0.75)
    rule = paint(eq([r"\Delta\vec v", "=", r"\vec v_2 - \vec v_1"], cfg.FONT["body"]), {0: cfg.DELTA_V, 2: cfg.VELOCITY})
    rule.next_to(equal, DOWN, buff=0.4)
    scene.play(FadeIn(dv_tag), Write(rule), run_time=1.2)

    # --- 5. a_avg = delta v / delta t -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    avg = paint(eq([r"\vec a_{\text{avg}}", "=", r"\frac{\Delta\vec v}{\Delta t}"], cfg.FONT["body"]), {0: cfg.ACCEL, 2: cfg.DELTA_V})
    avg.next_to(rule, DOWN, buff=0.4)
    scene.play(Write(avg), run_time=1.2)

    # --- 6. Carried to the circle from the arc's midpoint: toward the centre ------------------------------------------------------------------------------------
    beat(scene, t, 5)
    mid = lambda: (th1() + th2()) / 2  # noqa: E731
    arc = live(VMobject(), lambda: arc_mark(C, R, th1(), th2(), cfg.ANGLE, 7).set_stroke(opacity=0.8))
    scene.add(arc)
    scene.play(FadeIn(arc), run_time=0.5)
    anchor = Knob(0.0)       # 0: the arc's midpoint, 1: the first moment
    base = lambda: point(mid()) + (point(th1()) - point(mid())) * anchor.value  # noqa: E731

    def a_avg() -> np.ndarray:
        dt = gap.value / P.angular_speed
        return (vel(th2()) - vel(th1())) / dt

    carried = VecArrow(base, lambda: base() + a_avg() * KA, cfg.DELTA_V, width=0.1)
    to_centre = live(VMobject(), lambda: dashed_path(base(), C, cfg.MUTED, width=3, opacity=0.7, count=12))
    scene.add(to_centre, carried)
    scene.play(FadeOut(VGroup(c1, c2, dv, dv_tag, bench_tags, tags[1])),
               FadeIn(to_centre), carried.grow_in(run_time=1.2), run_time=1.2)
    toward = txt("toward the centre", cfg.FONT["small"], cfg.DELTA_V).move_to([-3.4, 3.35, 0])
    scene.play(FadeIn(toward, shift=DOWN * 0.1), run_time=0.7)
    scene.wait(2.0)
    scene.play(Indicate(carried, color=cfg.DELTA_V, scale_factor=1.05), run_time=1.2)

    # --- 7. Shrink the interval: from the first moment it swings onto the radius ---------------------------------------------------------------------------------------
    beat(scene, t, 6)
    off = DecimalNumber(0, num_decimal_places=0, font_size=46, color=cfg.ANGLE, unit=r"^\circ")
    off_row = VGroup(txt("off the radius:", cfg.FONT["small"], cfg.MUTED), off).arrange(RIGHT, buff=0.25).move_to([-3.4, 2.65, 0])
    off.add_updater(lambda m: m.set_value(np.degrees(gap.value / 2) * anchor.value))
    scene.play(FadeIn(off_row), run_time=0.5)          # 0 degrees: from the midpoint it aims at the centre
    scene.play(anchor.to(carried, 1.0, run_time=1.1), run_time=1.1)
    scene.play(gap.to(carried, 2 * DEGREES, run_time=6.0, rate_func=smooth), v2.fade_to(0.0, run_time=6.0), run_time=6.0)
    scene.wait(0.8)

    # --- 8. In the limit: centripetal acceleration, centre-seeking ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    off.clear_updaters()
    for m in (arc, to_centre):
        m.clear_updaters()
    name = VGroup(txt("centripetal", cfg.FONT["section"], cfg.ACCEL), txt("= centre-seeking", cfg.FONT["label"], cfg.WHITE))
    name.arrange(DOWN, buff=0.18).move_to([3.6, -1.35, 0])
    scene.play(FadeOut(VGroup(toward, off_row)), run_time=0.6)
    a_label = eq(r"\vec a", cfg.FONT["body"], cfg.ACCEL).next_to(point(THETA1) + (C - point(THETA1)) * 0.5, UP, buff=0.2)
    scene.play(FadeIn(name, shift=UP * 0.1), FadeIn(a_label), run_time=1.0)

    # --- 9. A direction, not a cause -----------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    note = chip("a direction, not a cause", cfg.MUTED).move_to([3.3, -2.45, 0])
    scene.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)

    # --- 10. v perpendicular to a -------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(dots[1], arc, to_centre)), FadeOut(VGroup(equal, rule, avg)), run_time=0.6)
    corner = right_angle_mark(point(THETA1), np.array([-np.sin(THETA1), np.cos(THETA1), 0]),
                              -np.array([np.cos(THETA1), np.sin(THETA1), 0]), 0.3, cfg.WHITE)
    dot = paint(eq([r"\vec v", r"\cdot", r"\vec a", "=", "0"], cfg.FONT["title"]), {0: cfg.VELOCITY, 2: cfg.ACCEL}).move_to([3.6, 1.6, 0])
    scene.play(Create(corner), run_time=0.6)
    scene.play(Write(dot), run_time=1.2)

    # --- 11. Turns the velocity, keeps its length ------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(dots[0], v1, tags[0], carried, corner, a_label)), run_time=0.5)
    view.clock.value = (THETA1 - view.phase) / P.angular_speed
    v_now, a_now = view.arrow("v", width=0.09), view.arrow("a", width=0.09)
    scene.add(view.ball, v_now, a_now)
    scene.play(FadeIn(view.ball), v_now.grow_in(run_time=0.5), a_now.grow_in(run_time=0.5), run_time=0.5)
    keeps = VGroup(txt("turns v", cfg.FONT["label"], cfg.ACCEL), txt("keeps |v|", cfg.FONT["label"], cfg.VELOCITY)).arrange(RIGHT, buff=0.6)
    keeps.move_to([3.6, 0.2, 0])
    scene.play(FadeIn(keeps, shift=UP * 0.1), view.run(view.clock.value + 0.4, 1.0), run_time=1.0)
    scene.play(view.run(view.clock.value + 1.6, 6.0), run_time=6.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
