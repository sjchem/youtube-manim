"""Scene 08 — subtraction. -B is B turned round; A - B = A + (-B) tip to
tail; with numbers, (5, 3) - (2, 1) = (3, 2) (``physics_models.SUBTRACT``),
and the same arrow runs from B's tip to A's tip. Then velocity: a car turns
a corner at a constant 15 m/s, and delta v = v_f - v_i (orange: it will be
the direction of acceleration) is 21.2 m/s pointing north-west.
"""

from manim_scenes.common import *

A_V, B_V = pm.SUBTRACT
DIFF = pm.sub(A_V, B_V)
CORNER = np.array([-1.5, -1.2, 0])      # centre of the turn's arc
TURN_R = 1.3
APPROACH_LENGTH = 5.0
SPEED = pm.CORNER_SPEED


class Scene08Subtraction(Scene):
    def construct(self) -> None:
        play_scene(self)


def corner_pose(s: float) -> tuple[np.ndarray, float]:
    """Position and heading after ``s`` screen units along: east, a quarter turn, then north."""
    straight = APPROACH_LENGTH
    arc = PI / 2 * TURN_R
    entry = CORNER + DOWN * TURN_R
    if s <= straight:
        return entry + LEFT * (straight - s), 0.0
    if s <= straight + arc:
        a = (s - straight) / TURN_R
        return CORNER + TURN_R * np.array([np.sin(a), -np.cos(a), 0]), a
    return CORNER + RIGHT * TURN_R + UP * (s - straight - arc), PI / 2


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", "Subtracting vectors")
    grid = plane((-3, 6), (-2, 5), unit=0.75, at=(-4.9, -2.2, 0))
    A = vec_on(grid, (0, 0), A_V, cfg.VEC_A, width=0.12)
    flip = Knob(0.0)
    b_tip = lambda: (B_V[0] * np.cos(PI * flip.value) - B_V[1] * np.sin(PI * flip.value),  # noqa: E731
                     B_V[0] * np.sin(PI * flip.value) + B_V[1] * np.cos(PI * flip.value))
    B = vec_on(grid, (0, 0), b_tip, cfg.VEC_B, width=0.12)
    scene.add(grid, A, B)
    scene.play(FadeIn(grid), A.grow_in(run_time=1.0), B.grow_in(run_time=1.0), run_time=1.0)
    names = VGroup(eq(r"\vec{A}", cfg.FONT["body"], cfg.VEC_A).move_to(grid.c2p(2.2, 2.3)),
                   eq(r"\vec{B}", cfg.FONT["body"], cfg.VEC_B).move_to(grid.c2p(1.6, 0.25)))
    scene.play(FadeIn(names), run_time=0.6)
    rule = paint(eq([r"\vec{A}", "-", r"\vec{B}", "=", r"\vec{A}", "+", r"(-\vec{B})"], cfg.FONT["section"]),
                 {0: cfg.VEC_A, 2: cfg.VEC_B, 4: cfg.VEC_A, 6: cfg.VEC_B}).move_to([1.4, 2.6, 0], aligned_edge=LEFT)
    scene.play(Write(rule), run_time=1.4)

    # --- 2. -B: same length, opposite way ------------------------------------------------------------------------------------
    beat(scene, t, 1)
    keep = vec_on(grid, (0, 0), B_V, cfg.VEC_B, width=0.12)
    keep.alpha = 0.35
    scene.add(keep)
    scene.play(flip.to(B, 1.0, run_time=2.0), names[1].animate.move_to(grid.c2p(-1.0, -1.5)), run_time=2.0)
    neg = eq(r"-\vec{B}", cfg.FONT["body"], cfg.VEC_B).move_to(names[1])
    scene.play(ReplacementTransform(names[1], neg), run_time=0.6)

    # --- 3. A - B = A + (-B), tip to tail ----------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    moved = vec_on(grid, A_V, (A_V[0] - B_V[0], A_V[1] - B_V[1]), cfg.VEC_B, width=0.12)
    scene.add(moved)
    scene.play(B.fade_to(0.0, run_time=0.8), keep.fade_to(0.0, run_time=0.8),
               FadeOut(neg), moved.grow_in(run_time=1.0), run_time=1.0)
    scene.remove(B, keep)
    keep.clear_updaters()
    D = vec_on(grid, (0, 0), DIFF, cfg.RESULT, width=0.12)
    scene.add(D)
    scene.play(D.grow_in(run_time=1.2), run_time=1.2)
    d_name = eq(r"\vec{A}-\vec{B}", cfg.FONT["body"], cfg.RESULT).move_to(grid.c2p(2.5, 0.65))
    scene.play(FadeIn(d_name), run_time=0.6)

    # --- 4. With numbers: A = (5, 3), B = (2, 1) ------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    vals = VGroup(paint(eq([r"\vec{A}", f"= ({A_V[0]:.0f},\\ {A_V[1]:.0f})"], cfg.FONT["section"]), {0: cfg.VEC_A}),
                  paint(eq([r"\vec{B}", f"= ({B_V[0]:.0f},\\ {B_V[1]:.0f})"], cfg.FONT["section"]), {0: cfg.VEC_B}))
    vals.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([1.4, 0.75, 0], aligned_edge=LEFT)
    scene.play(FadeIn(vals, shift=LEFT * 0.2), run_time=1.0)

    # --- 5. Subtract the matching parts -----------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    parts = eq([r"\vec{A}-\vec{B}", "=", "(", f"{A_V[0]:.0f}-{B_V[0]:.0f}", r",\ ", f"{A_V[1]:.0f}-{B_V[1]:.0f}", ")"],
               cfg.FONT["body"])
    paint(parts, {0: cfg.RESULT, 3: cfg.X_COLOR, 5: cfg.Y_COLOR}).next_to(vals, DOWN, buff=0.5).align_to(vals, LEFT)
    scene.play(Write(parts), run_time=1.6)
    scene.play(Indicate(parts[3], color=cfg.X_COLOR), run_time=0.9)
    scene.play(Indicate(parts[5], color=cfg.Y_COLOR), run_time=0.9)

    # --- 6. = (3, 2) ------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    answer = eq([r"=", f"({DIFF[0]:.0f},\\ {DIFF[1]:.0f})"], cfg.FONT["section"], cfg.RESULT)
    answer.next_to(parts, DOWN, buff=0.35).align_to(parts[1], LEFT)
    scene.play(FadeIn(boxed(answer, cfg.RESULT), scale=1.1), run_time=1.0)

    # --- 7. The arrow from B's tip to A's tip -----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(B.fade_to(1.0, run_time=0.6), flip.to(B, 0.0, run_time=0.6),
               moved.fade_to(0.0, run_time=0.6), run_time=0.6)
    scene.remove(moved)
    bridge = vec_on(grid, B_V, A_V, cfg.RESULT, width=0.12)
    scene.add(bridge)
    scene.play(bridge.grow_in(run_time=1.4), run_time=1.4)
    from_to = txt("from B to A", cfg.FONT["label"], cfg.RESULT).move_to([-2.8, 1.1, 0])
    scene.play(FadeIn(from_to), Indicate(bridge, color=cfg.RESULT, scale_factor=1.05), run_time=1.2)
    scene.play(Indicate(D, color=cfg.RESULT), run_time=1.0)

    # --- 8. Subtraction measures change ---------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    change = result_label('Δ', cfg.GOLD, cfg.FONT["body"]).move_to(DOWN * 3.65)
    scene.play(FadeIn(change, shift=UP * 0.15), run_time=0.8)

    # --- 9. delta v = v_f - v_i ---------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    clear(scene, head)
    dv = paint(eq([r"\Delta\vec{v}", "=", r"\vec{v}_f", "-", r"\vec{v}_i"], cfg.FONT["title"]), {0: cfg.ACCEL, 2: cfg.VELOCITY,
                                                                                               4: cfg.VELOCITY})
    dv.move_to([4.3, 2.6, 0])
    scene.play(Write(dv), run_time=1.4)

    # --- 10. A car turns the corner at 15 m/s ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    entry = CORNER + DOWN * TURN_R
    road = VMobject(stroke_color=cfg.GRAY, stroke_width=56, stroke_opacity=0.32)
    road.set_points_as_corners([entry + LEFT * (APPROACH_LENGTH + 0.35)]
                               + [corner_pose(APPROACH_LENGTH + k * PI / 2 * TURN_R / 20)[0] for k in range(21)]
                               + [CORNER + RIGHT * TURN_R + UP * 4.6])
    car = Car(cfg.CYAN, 1.1)
    s = Knob(0.0)
    car.set_pose(*corner_pose(s.value))
    car.add_updater(lambda m: m.set_pose(*corner_pose(s.value)))
    heading_dir = lambda: np.array([np.cos(corner_pose(s.value)[1]), np.sin(corner_pose(s.value)[1]), 0])  # noqa: E731
    vel = VecArrow(lambda: corner_pose(s.value)[0] + heading_dir() * 0.6,
                   lambda: corner_pose(s.value)[0] + heading_dir() * 1.9, cfg.VELOCITY, width=0.1)
    gauge = Speedometer([-5.3, 1.9, 0], value=SPEED, radius=1.05)
    scene.play(FadeOut(head), FadeIn(road), FadeIn(car), FadeIn(gauge), run_time=0.9)
    scene.add(vel)
    scene.play(vel.grow_in(run_time=0.6), run_time=0.6)
    total = APPROACH_LENGTH + PI / 2 * TURN_R + 2.6
    initial_s = total * 2.4 / (2.4 + 4.0)
    scene.play(s.to(car, initial_s, run_time=2.4, rate_func=linear))
    vi_ghost = VecArrow(corner_pose(initial_s)[0] + RIGHT * 0.6, corner_pose(initial_s)[0] + RIGHT * 1.9,
                        cfg.VELOCITY, width=0.1)
    vi_ghost.alpha = 0.45
    vi_name = eq(r"\vec{v}_i", cfg.FONT["body"], cfg.VELOCITY).next_to(vi_ghost, DOWN, buff=0.2)
    scene.add(vi_ghost)
    scene.play(FadeIn(vi_name), run_time=0.4)
    scene.play(s.to(car, total, run_time=4.0, rate_func=linear))
    vf_name = eq(r"\vec{v}_f", cfg.FONT["body"], cfg.VELOCITY).next_to(vel, RIGHT, buff=0.2)
    scene.play(FadeIn(vf_name), run_time=0.5)

    # --- 11. Same speed. Has the velocity changed? ---------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    same = VGroup(txt("same speed:", cfg.FONT["label"], cfg.WHITE), eq(r"15\ \mathrm{m/s}", cfg.FONT["label"])).arrange(RIGHT, buff=0.25)
    same.next_to(gauge, DOWN, buff=0.45)
    ask = txt("velocity changed?", cfg.FONT["label"], cfg.RED).next_to(same, DOWN, buff=0.3)
    scene.play(FadeIn(same), run_time=0.7)
    scene.play(FadeIn(ask), run_time=0.7)

    # --- 12. Tail to tail: delta v from tip of v_i to tip of v_f --------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    o = np.array([4.6, -1.4, 0])
    k = 0.13
    vi = VecArrow(o, o + RIGHT * SPEED * k, cfg.VELOCITY, width=0.11)
    vf = VecArrow(o, o + UP * SPEED * k, cfg.VELOCITY, width=0.11)
    d_v = VecArrow(o + RIGHT * SPEED * k, o + UP * SPEED * k, cfg.ACCEL, width=0.12)
    tags = VGroup(eq(r"\vec{v}_i", cfg.FONT["body"], cfg.VELOCITY).next_to(vi, DOWN, buff=0.2),
                  eq(r"\vec{v}_f", cfg.FONT["body"], cfg.VELOCITY).next_to(vf, LEFT, buff=0.2))
    scene.play(FadeOut(dv), run_time=0.4)
    scene.add(vi, vf)
    scene.play(vi.grow_in(run_time=0.9), vf.grow_in(run_time=0.9), FadeIn(tags), run_time=0.9)
    scene.add(d_v)
    scene.play(d_v.grow_in(run_time=1.4), run_time=1.4)
    d_name = eq(r"\Delta\vec{v}", cfg.FONT["body"], cfg.ACCEL).move_to(o + (RIGHT + UP) * SPEED * k * 0.5 + UR * 0.45)
    scene.play(FadeIn(d_name), run_time=0.6)

    # --- 13. North-west, 21.2 m/s ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    dv_mag = md.fixed(pm.magnitude(pm.corner_delta_v()), 1)
    size = eq([r"|\Delta\vec{v}|", r"\approx", rf"{dv_mag}\ \mathrm{{m/s}}"], cfg.FONT["section"])
    paint(size, {0: cfg.ACCEL, 2: cfg.ACCEL}).move_to([4.5, 2.7, 0])
    nw = txt("north-west", cfg.FONT["label"], cfg.ACCEL).next_to(size, DOWN, buff=0.3)
    scene.play(Write(size), run_time=1.4)
    scene.play(FadeIn(nw), run_time=0.6)

    # --- 14. The velocity changed; the speed did not -------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    verdict = result_label('Δv ≠ 0', cfg.GOLD, cfg.FONT["body"])
    fit_width(verdict, 8.4)
    verdict.move_to([3.2, -3.65, 0])
    scene.play(FadeOut(ask), FadeIn(verdict, shift=UP * 0.15), run_time=0.9)
    scene.play(Indicate(d_v, color=cfg.ACCEL, scale_factor=1.06), run_time=1.2)

    # --- 15. A seed: acceleration without speeding up (circular motion, next episode) ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    clear(scene)
    centre = np.array([-2.6, -0.3, 0])
    ring = Circle(radius=2.0, stroke_color=cfg.MUTED, stroke_width=3, stroke_opacity=0.6).move_to(centre)
    spin = Knob(0.0)
    where = lambda: centre + 2.0 * np.array([np.cos(spin.value), np.sin(spin.value), 0])  # noqa: E731
    tangent = lambda: np.array([-np.sin(spin.value), np.cos(spin.value), 0])  # noqa: E731
    dot = bead(where(), cfg.BALL, 0.18)
    dot.add_updater(lambda m: m.move_to(where()))
    v_arrow = VecArrow(where, lambda: where() + tangent() * 1.4, cfg.VELOCITY, width=0.1)
    a_arrow = VecArrow(where, lambda: where() + (centre - where()) * 0.45, cfg.ACCEL, width=0.1)
    scene.add(ring, dot, v_arrow, a_arrow)
    scene.play(FadeIn(ring), FadeIn(dot), v_arrow.grow_in(run_time=0.8), a_arrow.grow_in(run_time=0.8), run_time=0.8)
    teaser = VGroup(txt("acceleration", cfg.FONT["section"], cfg.ACCEL), txt('constant speed', cfg.FONT["section"], cfg.WHITE),
                    chip('Circular motion', cfg.CYAN)).arrange(DOWN, buff=0.35).move_to([3.4, 0.0, 0])
    scene.play(FadeIn(teaser[:2], shift=LEFT * 0.2), spin.to(dot, PI, run_time=3.0, rate_func=linear), run_time=3.0)
    scene.play(FadeIn(teaser[2]), spin.to(dot, 2.4 * PI, run_time=4.2, rate_func=linear), run_time=4.2)

    # --- 16. Addition: combined effect. Subtraction: difference -------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 15)
    clear(scene)
    summary = VGroup(
        VGroup(paint(eq([r"\vec{A}", "+", r"\vec{B}"], cfg.FONT["title"]), {0: cfg.VEC_A, 2: cfg.VEC_B}),
               txt('sum', cfg.FONT["body"], cfg.RESULT)).arrange(DOWN, buff=0.35),
        VGroup(paint(eq([r"\vec{A}", "-", r"\vec{B}"], cfg.FONT["title"]), {0: cfg.VEC_A, 2: cfg.VEC_B}),
               txt('difference', cfg.FONT["body"], cfg.ACCEL)).arrange(DOWN, buff=0.35)).arrange(RIGHT, buff=2.0)
    scene.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in summary], lag_ratio=0.4), run_time=1.6)
    scene.wait(6.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["08"])
