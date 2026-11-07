"""Scene 09 — a = v^2 / r, derived two ways.

First by the chain in the brief: a_avg = |delta v| / delta t ~ v delta theta /
delta t; the arc delta s = r delta theta = v delta t gives delta theta /
delta t = v / r; so a = v^2 / r, toward the centre. The arc and its length
are drawn on the circle as each step is written.

Then by the velocity circle: the position arrow sweeps a circle of radius r
and its tip moves at v; the velocity arrow sweeps a circle of radius v at the
same angular rate v / r, so its tip moves at v (v / r). The orange arrow at
the velocity's tip is parallel to the inward acceleration on the left: the
speed of the velocity's tip *is* the acceleration. Finally the reference
particle's numbers: 4^2 / 2 = 8 m/s^2, at a constant 4 m/s.
"""

from manim_scenes.common import *

PIC = np.array([-3.9, -0.6, 0])
R = 2.35
THETA1 = 25 * DEGREES
D_THETA = 55 * DEGREES
COL = 3.3


class Scene09Derivation(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "09", "Deriving v² / r")
    view = CircleView(PIC, R, P)
    scene.play(FadeIn(view.ring), FadeIn(view.hub), run_time=0.6)
    s1 = eq([r"a_{\text{avg}}", "=", r"\frac{|\Delta\vec v|}{\Delta t}", r"\approx", r"\frac{v\,\Delta\theta}{\Delta t}"], cfg.FONT["body"])
    paint(s1, {0: cfg.ACCEL, 2: cfg.DELTA_V, 4: cfg.VELOCITY})
    s1.move_to([COL, 2.6, 0])
    scene.play(FadeOut(head), Write(s1), run_time=1.8)

    # --- 2. Need delta theta / delta t: the arc has length r delta theta ----------------------------------------------
    beat(scene, t, 1)
    spoke1 = Line(PIC, view.at_angle(THETA1), stroke_color=cfg.POSITION, stroke_width=4)
    spoke2 = Line(PIC, view.at_angle(THETA1 + D_THETA), stroke_color=cfg.POSITION, stroke_width=4)
    angle = arc_mark(PIC, 0.7, THETA1, THETA1 + D_THETA, cfg.ANGLE)
    d_theta = eq(r"\Delta\theta", cfg.FONT["small"], cfg.ANGLE).move_to(PIC + 1.15 * np.array([np.cos(THETA1 + D_THETA / 2),
                                                                                                  np.sin(THETA1 + D_THETA / 2), 0]))
    arc = arc_mark(PIC, R, THETA1, THETA1 + D_THETA, cfg.CYAN, 9)
    r_tag = eq("r", cfg.FONT["body"], cfg.POSITION).next_to(spoke1.get_center(), DOWN, buff=0.15)
    scene.play(Create(spoke1), Create(spoke2), FadeIn(r_tag), run_time=0.9)
    scene.play(Create(angle), FadeIn(d_theta), run_time=0.7)
    scene.play(Create(arc), run_time=1.0)
    arc_tag = eq(r"\Delta s = r\,\Delta\theta", cfg.FONT["body"], cfg.CYAN)
    arc_tag.next_to(view.at_angle(THETA1 + D_THETA / 2), UR, buff=0.12)
    s2 = eq(r"\Delta s = r\,\Delta\theta", cfg.FONT["body"], cfg.CYAN).next_to(s1, DOWN, buff=0.55)
    scene.play(FadeIn(arc_tag), Write(s2), run_time=1.2)

    # --- 3. At constant speed, delta s = v delta t -----------------------------------------------------------------------------------
    beat(scene, t, 2)
    s3 = eq(r"\Delta s = v\,\Delta t", cfg.FONT["body"], cfg.VELOCITY).next_to(s2, DOWN, buff=0.4)
    travel = Knob(0.0)
    mover = bead(view.at_angle(THETA1), cfg.BALL, 0.15)
    mover.add_updater(lambda m: m.move_to(view.at_angle(THETA1 + D_THETA * travel.value)))
    scene.add(mover)
    scene.play(Write(s3), travel.to(mover, 1.0, run_time=1.6, rate_func=linear), run_time=1.6)

    # --- 4. So delta theta / delta t = v / r ---------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    s4 = eq([r"r\,\Delta\theta = v\,\Delta t", r"\ \Rightarrow\ ", r"\frac{\Delta\theta}{\Delta t} = \frac{v}{r}"], cfg.FONT["body"])
    paint(s4, {2: cfg.ANGLE}).next_to(s3, DOWN, buff=0.45)
    fit_width(s4, 7.4)
    scene.play(Write(s4), run_time=1.6)

    # --- 5. Substitute: a ~ v (v / r) ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    s5 = eq([r"a", r"\approx", r"v \cdot \frac{v}{r}"], cfg.FONT["body"])
    paint(s5, {0: cfg.ACCEL}).next_to(s4, DOWN, buff=0.45)
    scene.play(Write(s5), run_time=1.2)

    # --- 6. In the limit: a_c = v^2 / r, toward the centre --------------------------------------------------------------------------------------
    beat(scene, t, 5)
    steps = VGroup(s1, s2, s3, s4, s5)
    scene.play(FadeOut(steps), FadeOut(VGroup(arc_tag, spoke2, angle, d_theta, arc, mover)), run_time=0.7)
    mover.clear_updaters()
    result = eq([r"a_c", "=", r"\frac{v^2}{r}"], cfg.FONT["hero"])
    paint(result, {0: cfg.ACCEL}).move_to([COL, 0.9, 0])
    framed = boxed(result, cfg.RESULT, buff=0.3)
    limit = eq(r"\Delta t \to 0", cfg.FONT["body"], cfg.MUTED).next_to(result, UP, buff=0.55)
    scene.play(FadeIn(limit), run_time=0.6)
    scene.play(Write(result), run_time=1.4)
    scene.play(FadeIn(framed[0]), run_time=0.6)
    view.clock.value = (THETA1 - view.phase) / P.angular_speed
    a_in = view.arrow("a", width=0.1)
    toward = txt("toward the centre", cfg.FONT["small"], cfg.ACCEL).next_to(framed, DOWN, buff=0.35)
    scene.add(view.ball, a_in)
    scene.play(FadeOut(VGroup(spoke1, r_tag)), FadeIn(view.ball), a_in.grow_in(run_time=0.8), FadeIn(toward), run_time=0.8)
    scene.play(view.run(view.clock.value + 1.5, 4.0), run_time=4.0)

    # --- 7. Second way: the position arrow's tip moves at v ---------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(a_in, limit, toward)), run_time=0.4)
    scene.play(framed.animate.scale(0.55).move_to([COL + 2.6, 3.25, 0]), run_time=0.6)
    a_in.clear_updaters()
    left = CircleView([-4.0, -0.6, 0], 2.0, P, kv=1.1 / P.v)
    right_c = np.array([2.6, -0.6, 0])
    kv_big = 2.0 / P.v                      # the velocity circle drawn at the same size
    # The left tip's speed v is drawn as an arrow of left.kv * v; that is "how far the
    # tip moves in `seconds`". The velocity tip's rate dv/dt gets the same time scale.
    seconds = left.kv / (left.R / P.r)
    left.clock.value = view.clock.value
    scene.remove(view.ball)
    scene.play(FadeOut(VGroup(view.ring, view.hub)), FadeIn(VGroup(left.ring, left.hub, left.ball)), run_time=0.6)
    r_arrow = left.arrow("r", width=0.08)
    tip_speed = left.arrow("v", width=0.08)
    scene.add(r_arrow, tip_speed)
    scene.play(r_arrow.grow_in(run_time=0.6), tip_speed.grow_in(run_time=0.6), run_time=0.6)
    tags_left = VGroup(txt("radius r", cfg.FONT["small"], cfg.POSITION), txt("tip speed v", cfg.FONT["small"], cfg.VELOCITY))
    tags_left.arrange(DOWN, buff=0.2).move_to([-4.0, 2.75, 0])
    scene.play(FadeIn(tags_left), left.run(left.clock.value + 1.6, 6.0), run_time=6.0)

    # --- 8. The velocity arrow's tip moves at v (v / r): that's the acceleration ----------------------------------------------------------------------------------
    beat(scene, t, 7)
    ring_v = Circle(radius=kv_big * P.v, stroke_color=cfg.VELOCITY, stroke_width=3, stroke_opacity=0.55).move_to(right_c)
    hub_v = Dot(right_c, radius=0.06, color=cfg.MUTED)
    v_arrow = VecArrow(lambda: right_c, lambda: right_c + left.vel() * kv_big, cfg.VELOCITY, width=0.09)
    # The velocity tip moves at |dv/dt| = v^2 / r; draw that rate with the same scale as the left tip's speed.
    tip_rate = VecArrow(lambda: right_c + left.vel() * kv_big,
                        lambda: right_c + left.vel() * kv_big + left.acc_radial() * kv_big * seconds, cfg.ACCEL, width=0.09)
    a_left = left.arrow("a", width=0.08)
    a_left.alpha = 0.0
    scene.add(ring_v, hub_v, v_arrow)
    scene.play(FadeIn(ring_v), FadeIn(hub_v), v_arrow.grow_in(run_time=0.8), run_time=0.8)
    tags_right = VGroup(txt("radius v", cfg.FONT["small"], cfg.VELOCITY), eq(r"\text{tip speed } v\cdot\frac{v}{r}", cfg.FONT["small"], cfg.ACCEL))
    tags_right.arrange(DOWN, buff=0.2).move_to([2.6, 2.75, 0])
    scene.play(FadeIn(tags_right[0]), left.run(left.clock.value + 1.0, 3.0), run_time=3.0)
    scene.add(tip_rate)
    scene.play(tip_rate.grow_in(run_time=0.8), FadeIn(tags_right[1]), run_time=0.8)
    scene.play(left.run(left.clock.value + 1.2, 4.2), run_time=4.2)
    scene.add(a_left)
    same = txt("same direction", cfg.FONT["small"], cfg.ACCEL).move_to([-0.7, 2.4, 0])
    scene.play(a_left.fade_to(1.0, run_time=0.8), FadeIn(same), run_time=0.8)
    scene.play(left.run(left.clock.value + 2.0, 7.0), run_time=7.0)

    # --- 9. Numbers: 4 m/s on a 2 m circle ----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    for m in (r_arrow, tip_speed, v_arrow, tip_rate, a_left, left.ball):
        m.clear_updaters()
    clear(scene, framed, run_time=0.7)
    ref = CircleView([-3.8, -0.6, 0], 2.3, P, kv=1.2 / P.v, ka=1.5 / P.accel)
    givens = VGroup(eq(rf"v = {V}\ \mathrm{{m/s}}", cfg.FONT["section"], cfg.VELOCITY),
                    eq(rf"r = {R_M}\ \mathrm{{m}}", cfg.FONT["section"], cfg.POSITION)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    givens.move_to([COL, 1.4, 0])
    v_ref, a_ref = ref.arrow("v", width=0.09), ref.arrow("a", width=0.09)
    a_ref.alpha = 0.0
    scene.add(ref.ring, ref.hub, ref.ball, v_ref, a_ref)
    scene.play(FadeIn(VGroup(ref.ring, ref.hub, ref.ball)), v_ref.grow_in(run_time=0.8), FadeIn(givens[0]), run_time=0.8)
    scene.play(FadeIn(givens[1]), ref.run(0.8, 2.4), run_time=2.4)

    # --- 10. 16 / 2 = 8 m/s^2 ----------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    numbers = eq([r"a_c", "=", rf"\frac{{{V}^2}}{{{R_M}}}", "=", rf"\frac{{{wh(P.v ** 2)}}}{{{R_M}}}", "=",
                  rf"{AC}\ \mathrm{{m/s^2}}"], cfg.FONT["section"])
    paint(numbers, {0: cfg.ACCEL, 6: cfg.ACCEL}).next_to(givens, DOWN, buff=0.7)
    fit_width(numbers, 7.6)
    scene.play(Write(numbers), a_ref.fade_to(1.0, run_time=1.6), ref.run(ref.clock.value + 0.5, 1.6), run_time=1.6)
    scene.play(FadeIn(boxed(numbers[6], cfg.RESULT, 0.14)[0]), ref.run(ref.clock.value + 0.4, 0.8), run_time=0.8)

    # --- 11. The speed never leaves 4 m/s ----------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    speed = number_line(lambda: float(np.linalg.norm(ref.vel())), 2, "m/s", cfg.VELOCITY, 56, "speed")
    speed.move_to([COL, -2.6, 0])
    scene.play(FadeIn(speed), ref.run(ref.clock.value + 0.5, 0.8), run_time=0.8)
    scene.play(ref.run(ref.clock.value + 2.6, 8.0), run_time=8.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
