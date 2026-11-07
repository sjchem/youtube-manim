"""Scene 08 — the velocity triangle. On the left, the reference circle: in a
short time the radius turns through delta theta, and because v is always
perpendicular to r, the velocity turns through the same angle. On the right,
every velocity arrow is moved to one shared tail: their tips trace a circle
of radius v (the hodograph), and the live arrow goes round it in step with
the particle. Two velocities and delta v make an isosceles triangle; split
in half, |delta v| = 2 v sin(delta theta / 2). The ratio 2 sin(x/2) / x is
tabulated from ``physics_models.chord_ratio`` as the angle shrinks to 5 deg.
"""

from manim_scenes.common import *

LEFT_C = np.array([-3.7, -0.5, 0])
RIGHT_C = np.array([3.5, -0.5, 0])
R = 2.3
KV = 2.2 / P.v                       # the velocity circle has radius 2.2 on screen
THETA1 = 35 * DEGREES
SLOW = 0.4


class Scene08VelocityTriangle(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", "The velocity triangle")
    view = CircleView(LEFT_C, R, P, kv=KV * 0.55, phase=THETA1)
    scene.play(FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), run_time=0.8)
    scene.play(view.run(1.4, 1.4 / SLOW), run_time=1.4 / SLOW)
    view.clock.value = 0.0
    scene.play(FadeOut(view.ball), run_time=0.4)

    # --- 2. In delta t the radius turns through delta theta ------------------------------------------------------------
    beat(scene, t, 1)
    gap = Knob(50 * DEGREES)
    th2 = lambda: THETA1 + gap.value  # noqa: E731
    pts = lambda th: view.at_angle(th)  # noqa: E731
    r1 = VecArrow(LEFT_C, pts(THETA1), cfg.POSITION, width=0.07)
    r2 = VecArrow(LEFT_C, lambda: pts(th2()), cfg.POSITION, width=0.07)
    dots = VGroup(bead(pts(THETA1), cfg.BALL, 0.14), bead(pts(th2()), cfg.BALL, 0.14))
    dots[1].add_updater(lambda m: m.move_to(pts(th2())))
    angle = live(VMobject(), lambda: arc_mark(LEFT_C, 0.75, THETA1, th2(), cfg.ANGLE))
    d_theta = eq(r"\Delta\theta", cfg.FONT["body"], cfg.ANGLE)
    d_theta.add_updater(lambda m: m.move_to(LEFT_C + 1.25 * np.array([np.cos(THETA1 + gap.value / 2), np.sin(THETA1 + gap.value / 2), 0])))
    scene.add(r1, r2)
    scene.play(FadeOut(head), FadeIn(dots), r1.grow_in(run_time=0.8), r2.grow_in(run_time=0.8), run_time=0.8)
    scene.add(angle)
    scene.play(FadeIn(angle), FadeIn(d_theta), run_time=0.8)

    # --- 3. Velocity turns through the same angle ------------------------------------------------------------------------------
    beat(scene, t, 2)
    vel = lambda th: P.v * np.array([-np.sin(th), np.cos(th), 0.0])  # noqa: E731
    k_left = KV * 0.55
    v1 = VecArrow(pts(THETA1), pts(THETA1) + vel(THETA1) * k_left, cfg.VELOCITY, width=0.08)
    v2 = VecArrow(lambda: pts(th2()), lambda: pts(th2()) + vel(th2()) * k_left, cfg.VELOCITY, width=0.08)
    marks = VGroup(right_angle_mark(pts(THETA1), vel(THETA1) / P.v, -np.array([np.cos(THETA1), np.sin(THETA1), 0]), 0.24, cfg.WHITE),
                   right_angle_mark(pts(th2()), vel(th2()) / P.v, -np.array([np.cos(th2()), np.sin(th2()), 0]), 0.24, cfg.WHITE))
    scene.add(v1, v2)
    scene.play(v1.grow_in(run_time=0.8), v2.grow_in(run_time=0.8), run_time=0.8)
    scene.play(Create(marks), run_time=0.8)
    same = eq(r"\vec v \text{ turns by } \Delta\theta", cfg.FONT["body"], cfg.VELOCITY).move_to([3.5, 3.25, 0])
    scene.play(FadeIn(same, shift=DOWN * 0.1), run_time=0.8)

    # --- 4. Collect every velocity arrow at one tail: the velocity circle ----------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(marks, same)), run_time=0.5)
    ring_v = DashedVMobject(Circle(radius=KV * P.v, stroke_color=cfg.VELOCITY, stroke_width=3).move_to(RIGHT_C), num_dashes=48)
    ring_v.set_stroke(opacity=0.6)
    hub = Dot(RIGHT_C, radius=0.06, color=cfg.MUTED)
    copies = []
    for k in range(12):
        th = THETA1 + k * TAU / 12
        move = Knob(0.0)
        tail = lambda th=th, move=move: pts(th) + (RIGHT_C - pts(th)) * move.value
        size = lambda move=move: k_left + (KV - k_left) * move.value
        copies.append((move, VecArrow(tail, lambda th=th, tail=tail, size=size: tail() + vel(th) * size(), cfg.VELOCITY,
                                      width=0.06, glow=False)))
    for _, arrow in copies:
        arrow.alpha = 0.0
        scene.add(arrow)
    scene.play(*[a.fade_to(0.75, run_time=0.8) for _, a in copies], FadeIn(hub), run_time=0.8)
    scene.play(LaggedStart(*[m.to(a, 1.0, run_time=1.6) for m, a in copies], lag_ratio=0.12), run_time=4.0)
    scene.play(Create(ring_v), run_time=1.2)
    radius_v = eq(r"\text{radius } v", cfg.FONT["body"], cfg.VELOCITY).next_to(ring_v, UP, buff=0.2)
    scene.play(FadeIn(radius_v), run_time=0.6)

    # --- 5. Once round the circle, once round the velocity circle, in step --------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(*[a.fade_to(0.0, run_time=0.6) for _, a in copies], FadeOut(VGroup(v1, v2, r1, r2, dots, d_theta, angle)),
               run_time=0.6)
    for m in (dots[1], angle, d_theta):
        m.clear_updaters()
    view.clock.value = 0.0
    r_live = view.arrow("r", width=0.08)
    v_here = view.arrow("v", width=0.08)
    v_hodo = VecArrow(lambda: RIGHT_C, lambda: RIGHT_C + view.vel() * KV, cfg.VELOCITY, width=0.09)
    tip_dot = Dot(radius=0.08, color=cfg.WHITE)
    tip_dot.add_updater(lambda m: m.move_to(RIGHT_C + view.vel() * KV))
    scene.add(view.ball, r_live, v_here, v_hodo, tip_dot)
    scene.play(FadeIn(view.ball), r_live.grow_in(run_time=0.6), v_here.grow_in(run_time=0.6), v_hodo.grow_in(run_time=0.6),
               run_time=0.6)
    scene.play(view.run(P.period, 7.5), run_time=7.5)

    # --- 6. The isosceles triangle --------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    for m in (r_live, v_here, v_hodo, tip_dot):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(view.ball, r_live, v_here, tip_dot, v_hodo, radius_v)), run_time=0.5)
    end1 = RIGHT_C + vel(THETA1) * KV
    end2 = lambda: RIGHT_C + vel(th2()) * KV  # noqa: E731
    h1 = VecArrow(RIGHT_C, end1, cfg.VELOCITY, width=0.09)
    h2 = VecArrow(lambda: RIGHT_C, end2, cfg.VELOCITY, width=0.09)
    chord = VecArrow(end1, end2, cfg.DELTA_V, width=0.09)
    scene.add(h1, h2)
    scene.play(h1.grow_in(run_time=0.7), h2.grow_in(run_time=0.7), run_time=0.7)
    scene.add(chord)
    scene.play(chord.grow_in(run_time=0.8), run_time=0.8)
    apex = live(VMobject(), lambda: arc_mark(RIGHT_C, 0.6, THETA1 + PI / 2, th2() + PI / 2, cfg.ANGLE))
    sides = VGroup(eq("v", cfg.FONT["body"], cfg.VELOCITY), eq("v", cfg.FONT["body"], cfg.VELOCITY),
                   eq(r"\Delta\vec v", cfg.FONT["body"], cfg.DELTA_V), eq(r"\Delta\theta", cfg.FONT["small"], cfg.ANGLE))

    def place_sides(m):
        e2 = end2()
        m[0].move_to(RIGHT_C + (end1 - RIGHT_C) * 0.55 + rotate_vector(mu.unit(end1 - RIGHT_C), -PI / 2) * 0.38)
        m[1].move_to(RIGHT_C + (e2 - RIGHT_C) * 0.55 + rotate_vector(mu.unit(e2 - RIGHT_C), PI / 2) * 0.38)
        m[2].move_to((end1 + e2) / 2 + mu.unit((end1 + e2) / 2 - RIGHT_C) * 0.55)
        mid = THETA1 + PI / 2 + gap.value / 2
        m[3].move_to(RIGHT_C + 1.0 * np.array([np.cos(mid), np.sin(mid), 0]))
        m[3].set_opacity(float(np.clip((gap.value - 14 * DEGREES) / (10 * DEGREES), 0, 1)))  # too small to label

    place_sides(sides)
    sides.add_updater(place_sides)
    scene.add(apex)
    scene.play(FadeIn(sides), FadeIn(apex), run_time=0.8)

    # --- 7. Split it: |delta v| = 2 v sin(delta theta / 2) --------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    split = live(VMobject(), lambda: dashed_path(RIGHT_C, (end1 + end2()) / 2, cfg.WHITE, width=3, opacity=0.75, count=10))
    scene.add(split)
    scene.play(FadeIn(split), run_time=0.8)
    half = eq([r"|\Delta\vec v|", "=", r"2v\sin\frac{\Delta\theta}{2}"], cfg.FONT["section"])
    paint(half, {0: cfg.DELTA_V})
    half.move_to([-3.6, 3.0, 0])
    scene.play(FadeOut(VGroup(view.ring, view.hub)), Write(half), run_time=1.6)
    scene.remove(view.ring, view.hub)

    # --- 8. For small angles: 2 sin(x / 2) ~ x ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    approx = eq(r"2\sin\frac{\Delta\theta}{2} \approx \Delta\theta \quad (\text{radians})", cfg.FONT["body"], cfg.ANGLE)
    approx.next_to(half, DOWN, buff=0.5)
    scene.play(Write(approx), run_time=1.6)

    # --- 9. The ratio as the angle shrinks ---------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    header = VGroup(eq(r"\Delta\theta", cfg.FONT["small"], cfg.ANGLE),
                    eq(r"\frac{2\sin(\Delta\theta/2)}{\Delta\theta}", cfg.FONT["small"], cfg.WHITE))
    header.arrange(RIGHT, buff=1.0).move_to([-3.6, 1.1, 0])
    scene.play(FadeOut(approx), run_time=0.25)
    scene.play(FadeIn(header), run_time=0.25)
    rows = VGroup()
    for k, degrees in enumerate(pm.SHRINKING_ANGLES_DEG):
        row = VGroup(txt(f"{wh(degrees)}°", cfg.FONT["small"], cfg.ANGLE),
                     txt(fx(pm.chord_ratio(degrees * DEGREES), 4), cfg.FONT["small"], cfg.WHITE))
        row[0].move_to([header[0].get_center()[0], 0.1 - 0.6 * k, 0])
        row[1].move_to([header[1].get_center()[0], 0.1 - 0.6 * k, 0])
        rows.add(row)
        scene.play(gap.to(h2, degrees * DEGREES, run_time=1.0), FadeIn(row, shift=UP * 0.08), run_time=1.0)
        scene.wait(0.6)
    goal = txt("→ 1", cfg.FONT["label"], cfg.GOLD).next_to(rows[-1][1], RIGHT, buff=0.4)
    scene.play(FadeIn(goal, shift=LEFT * 0.1), run_time=0.6)

    # --- 10. |delta v| ~ v delta theta ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(header, rows, goal)), run_time=0.4)
    scene.play(gap.to(h2, 50 * DEGREES, run_time=0.8), FadeIn(approx), run_time=0.8)
    result = eq([r"|\Delta\vec v|", r"\approx", r"v\,\Delta\theta"], cfg.FONT["title"])
    paint(result, {0: cfg.DELTA_V, 2: cfg.VELOCITY}).move_to([-3.6, -0.9, 0])
    framed = boxed(result, cfg.RESULT)
    scene.play(Write(result), run_time=1.2)
    scene.play(FadeIn(framed[0]), run_time=0.6)
    scene.play(gap.to(h2, 12 * DEGREES, run_time=3.5, rate_func=there_and_back), run_time=3.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
