"""Scene 07 — a delivery drone (``physics_models.DRONE``) flies 6 m east and
8 m north over a 3D field; the single straight flight between the same two
points is the resultant. The triangle and parallelogram laws are drawn in
2D, then a live angle phi between A and B checks the law of cosines against
the measured arrow, through phi = 0, 180 and 90 degrees (Pythagoras). The
drone's numbers close it: 36 + 64 = 100, R = 10 m at 53.13 degrees.
"""

from manim_scenes.common import *

S = 0.42                                   # stage units per metre
ALT = 1.25                                 # flight altitude (stage units)
HOME = np.array([-1.6, 0.0, 1.7])
EAST, NORTH = (np.array(v) for v in pm.DRONE)
RES = np.array(pm.add(*pm.DRONE))


class Scene07Drone(Scene):
    def construct(self) -> None:
        play_scene(self)


def sky(east: float, north: float, height: float = ALT) -> np.ndarray:
    return HOME + np.array([east * S, height, -north * S])


def drone_stage(at, zoom: float = 1.55):
    stage = field_stage(at, zoom=zoom, yaw=-0.42, pitch=0.62, x_range=(-2.6, 2.6), z_range=(-2.4, 2.4), step=0.42,
                        sway=0.03)
    leg = Knob(0.0)          # 0..1 along east, 1..2 along north
    direct = Knob(-1.0)      # >= 0: flying the straight resultant instead

    def where():
        if direct.value >= 0:
            p = RES * direct.value
        elif leg.value <= 1:
            p = EAST * leg.value
        else:
            p = EAST + NORTH * (leg.value - 1)
        return sky(p[0], p[1])

    drone_model(stage, where, cfg.CYAN, size=0.46)
    shadow = Disc(lambda: where() * np.array([1, 0, 1]) + np.array([0, 0.01, 0]), 0.3, cfg.BG, opacity=0.55, soft=True,
                  bias=-5e3)
    stage.add_body(shadow)
    return stage, leg, direct, where


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "07", "Triangle and parallelogram")
    stage, leg, direct, where = drone_stage((0.4, -1.9, 0))
    show(scene, stage, 0.8)
    a_arrow = Vector(sky(0, 0, 0.03), lambda: sky(*(EAST * min(leg.value, 1)), 0.03), cfg.VEC_A, width=0.1)
    b_arrow = Vector(sky(*EAST, 0.03), lambda: sky(*(EAST + NORTH * max(leg.value - 1, 0)), 0.03), cfg.VEC_B, width=0.1)
    b_arrow.presence = 0.0
    stage.add_overlay(a_arrow, b_arrow)
    scene.play(leg.to(stage, 1.0, run_time=3.0))
    six = Tag(eq(r"6\ \mathrm{m\ E}", cfg.FONT["body"], cfg.VEC_A), sky(3, 0, 0), DOWN * 0.55)
    six.presence = 0.0
    stage.add_overlay(six)
    scene.play(stage.fade(six, 1.0), run_time=0.6)

    # --- 2. Then 8 m north -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    b_arrow.presence = 1.0
    scene.play(leg.to(stage, 2.0, run_time=2.4))

    # --- 3. One straight flight: the resultant --------------------------------------------------------------------------
    beat(scene, t, 2)
    eight = Tag(eq(r"8\ \mathrm{m\ N}", cfg.FONT["body"], cfg.VEC_B), sky(6, 4, 0), RIGHT * 1.0)
    eight.presence = 0.0
    stage.add_overlay(eight)
    scene.play(stage.fade(eight, 1.0), run_time=0.6)
    grow = Knob(0.0)
    r_arrow = Vector(sky(0, 0, 0.03), lambda: sky(*(RES * grow.value), 0.03), cfg.RESULT, width=0.12)
    stage.add_overlay(r_arrow)
    scene.play(grow.to(stage, 1.0, run_time=1.4))
    scene.play(*[stage.fade(p, 0.0) for p in stage.bodies[-18:]], run_time=0.5)
    direct.value = 0.0
    scene.play(*[stage.fade(p, 1.0) for p in stage.bodies[-18:]], run_time=0.5)
    scene.play(direct.to(stage, 1.0, run_time=3.5))

    # --- 4. Triangle law ----------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    hide(scene, stage, 0.8)
    o = np.array([-5.6, -3.0, 0])
    k = 0.56
    a_tip = o + RIGHT * EAST[0] * k
    r_tip = a_tip + UP * NORTH[1] * k
    A = VecArrow(o, a_tip, cfg.VEC_A, width=0.12)
    B = VecArrow(a_tip, r_tip, cfg.VEC_B, width=0.12)
    R = VecArrow(o, r_tip, cfg.RESULT, width=0.12)
    names = VGroup(eq(r"\vec{A}", cfg.FONT["body"], cfg.VEC_A).next_to(A, DOWN, buff=0.2),
                   eq(r"\vec{B}", cfg.FONT["body"], cfg.VEC_B).next_to(B, RIGHT, buff=0.2),
                   eq(r"\vec{R}", cfg.FONT["body"], cfg.RESULT).move_to((o + r_tip) / 2 + UL * 0.45))
    scene.add(A, B, R)
    scene.play(A.grow_in(run_time=0.8), FadeIn(names[0]), run_time=0.8)
    scene.play(B.grow_in(run_time=0.8), FadeIn(names[1]), run_time=0.8)
    joint = glow_dot(a_tip, cfg.WHITE, 0.08)
    tip_tail = txt('tip → tail', cfg.FONT["small"], cfg.WHITE).next_to(a_tip, RIGHT, buff=0.5).shift(DOWN * 0.1)
    scene.play(FadeIn(joint, scale=1.4), FadeIn(tip_tail), run_time=0.8)
    scene.play(R.grow_in(run_time=1.2), FadeIn(names[2]), run_time=1.2)
    tri = chip("triangle law", cfg.GOLD).move_to([-3.4, 2.9, 0])
    scene.play(FadeIn(tri, shift=DOWN * 0.15), run_time=0.7)

    # --- 5. Parallelogram law ---------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    o2 = np.array([1.4, -3.0, 0])
    A2 = VecArrow(o2, o2 + RIGHT * EAST[0] * k, cfg.VEC_A, width=0.12)
    B2 = VecArrow(o2, o2 + UP * NORTH[1] * k, cfg.VEC_B, width=0.12)
    far = o2 + RIGHT * EAST[0] * k + UP * NORTH[1] * k
    sides = VGroup(DashedLine(A2.tip(), far, stroke_color=cfg.VEC_B, stroke_width=3, stroke_opacity=0.7),
                   DashedLine(B2.tip(), far, stroke_color=cfg.VEC_A, stroke_width=3, stroke_opacity=0.7))
    R2 = VecArrow(o2, far, cfg.RESULT, width=0.12)
    fill = Polygon(o2, A2.tip(), far, B2.tip(), stroke_width=0, fill_color=cfg.RESULT, fill_opacity=0.08)
    scene.add(A2, B2, R2)
    scene.play(FadeOut(tip_tail), A2.grow_in(run_time=0.8), B2.grow_in(run_time=0.8), run_time=0.8)
    scene.play(Create(sides), FadeIn(fill), run_time=1.0)
    scene.play(R2.grow_in(run_time=1.2), run_time=1.2)
    par = chip("parallelogram law", cfg.PURPLE).move_to([3.2, 2.9, 0])
    scene.play(FadeIn(par, shift=DOWN * 0.15), run_time=0.7)

    # --- 6. They always agree ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    same = eq(r"=", cfg.FONT["hero"], cfg.RESULT).move_to([-0.6, 0.2, 0])
    scene.play(FadeIn(same, scale=1.4), Indicate(R, color=cfg.RESULT), Indicate(R2, color=cfg.RESULT), run_time=1.2)

    # --- 7. Let the angle between them change: phi -------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    clear(scene)
    o = np.array([-4.3, -2.2, 0])
    a_len, b_len = 3.2, 2.2
    phi = Knob(70 * DEGREES)
    b_end = lambda: o + b_len * np.array([np.cos(phi.value), np.sin(phi.value), 0])  # noqa: E731
    a_end = o + RIGHT * a_len
    r_end = lambda: a_end + (b_end() - o)  # noqa: E731
    A = VecArrow(o, a_end, cfg.VEC_A, width=0.12)
    B = VecArrow(o, b_end, cfg.VEC_B, width=0.12)
    R = VecArrow(o, r_end, cfg.RESULT, width=0.12)
    ghost = always_redraw(lambda: VGroup(
        DashedLine(a_end, r_end(), stroke_color=cfg.VEC_B, stroke_width=3, stroke_opacity=0.6),
        DashedLine(b_end(), r_end(), stroke_color=cfg.VEC_A, stroke_width=3, stroke_opacity=0.6)))
    arc = always_redraw(lambda: angle_arc(o, 0, np.degrees(phi.value), 0.75, cfg.WHITE, 4))
    phi_lab = eq(r"\phi", cfg.FONT["body"], cfg.WHITE)
    phi_lab.add_updater(lambda m: m.move_to(o + 1.15 * np.array([np.cos(phi.value / 2), np.sin(phi.value / 2), 0])))
    scene.add(A, B, R)
    scene.play(A.grow_in(run_time=0.8), B.grow_in(run_time=0.8), run_time=0.8)
    scene.play(R.grow_in(run_time=0.8), FadeIn(ghost), Create(arc), FadeIn(phi_lab), run_time=0.8)
    scene.play(phi.to(R, 120 * DEGREES, run_time=1.6))
    scene.play(phi.to(R, 50 * DEGREES, run_time=1.6))

    # --- 8. Same way: lengths add. Opposite: they subtract ---------------------------------------------------------------------------------------
    beat(scene, t, 7)
    r_now = lambda: float(np.linalg.norm(r_end() - o)) / 0.4  # noqa: E731
    readout = VGroup(eq(r"|\vec{R}| =", cfg.FONT["body"], cfg.RESULT), DecimalNumber(r_now(), num_decimal_places=2,
                                                                                    font_size=64, color=cfg.RESULT))
    readout[1].add_updater(lambda m: m.set_value(r_now()))
    readout[1].add_updater(lambda m: m.next_to(readout[0], RIGHT, buff=0.25))
    readout.move_to([4.0, 3.3, 0])
    lengths = eq([r"|\vec{A}| = 8", r"\qquad", r"|\vec{B}| = 5.5"], cfg.FONT["label"])
    paint(lengths, {0: cfg.VEC_A, 2: cfg.VEC_B}).next_to(readout, DOWN, buff=0.35)
    scene.play(FadeIn(readout), FadeIn(lengths), run_time=0.8)
    scene.play(phi.to(R, 0.0, run_time=1.8))
    plus = eq(r"8 + 5.5 = 13.5", cfg.FONT["label"], cfg.RESULT).next_to(lengths, DOWN, buff=0.3)
    scene.play(FadeIn(plus), run_time=0.5)
    scene.play(phi.to(R, PI, run_time=2.2))
    minus = eq(r"8 - 5.5 = 2.5", cfg.FONT["label"], cfg.RESULT).next_to(plus, DOWN, buff=0.25)
    scene.play(FadeIn(minus), run_time=0.5)

    # --- 9. Law of cosines -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(VGroup(plus, minus)), phi.to(R, 65 * DEGREES, run_time=1.4), run_time=1.4)
    law = eq([r"R", "=", r"\sqrt{A^2 + B^2", r"+\,2AB\cos\phi", "}"], cfg.FONT["body"])
    paint(law, {0: cfg.RESULT})
    box = on_panel(law, cfg.GOLD)
    fit_width(box, 6.8)
    box.move_to([3.6, 0.75, 0])
    scene.play(FadeIn(box.back), Write(law), run_time=2.0)
    check = VGroup(txt("formula", cfg.FONT["small"], cfg.MUTED),
                   DecimalNumber(r_now(), num_decimal_places=2, font_size=56, color=cfg.GOLD))
    check[1].add_updater(lambda m: m.set_value(pm.resultant_length(8, 5.5, np.degrees(phi.value))))
    check[1].add_updater(lambda m: m.next_to(check[0], RIGHT, buff=0.25))
    check.next_to(box, DOWN, buff=0.35)
    scene.play(FadeIn(check), run_time=0.6)
    scene.play(phi.to(R, 140 * DEGREES, run_time=2.4))
    scene.play(phi.to(R, 30 * DEGREES, run_time=2.4))

    # --- 10. Extremes: phi = 0 and phi = 180 ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    ends = VGroup(eq([r"\phi = 0^\circ:", r"\ \cos\phi = 1", r"\ \Rightarrow\ R = A + B"], cfg.FONT["small"]),
                  eq([r"\phi = 180^\circ:", r"\ \cos\phi = -1", r"\ \Rightarrow\ R = |A - B|"], cfg.FONT["small"]))
    ends.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    fit_width(ends, 6.8)
    ends.move_to([3.6, -2.75, 0])
    scene.play(phi.to(R, 0.0, run_time=1.5), FadeIn(ends[0]), run_time=1.5)
    scene.wait(2.5)
    scene.play(phi.to(R, PI, run_time=2.0), FadeIn(ends[1]), run_time=2.0)

    # --- 11. Perpendicular: cos 90 = 0, the middle term vanishes ---------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(phi.to(R, PI / 2, run_time=1.8))
    square = right_angle_mark(o, RIGHT, UP, 0.32, cfg.WHITE)
    scene.play(Create(square), run_time=0.5)
    gone = strike(law[3])
    zero = eq(r"0", cfg.FONT["body"], cfg.RED).next_to(law, DOWN, buff=0.3).align_to(law[3], LEFT)
    check[1].clear_updaters()
    scene.play(FadeOut(check), run_time=0.3)
    scene.play(Create(gone), FadeIn(zero), run_time=0.7)

    # --- 12. R = sqrt(A^2 + B^2): Pythagoras ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    pyth = eq([r"R", "=", r"\sqrt{A^2 + B^2}"], cfg.FONT["section"])
    paint(pyth, {0: cfg.RESULT}).move_to(law)
    pyth_box = boxed(pyth, cfg.RESULT)
    fit_width(pyth_box, 6.8)
    pyth_box.move_to(box)
    scene.play(fade_through(VGroup(law, gone, zero, box.back), pyth_box), run_time=1.0)
    name = txt('Pythagoras', cfg.FONT["small"], cfg.RESULT).next_to(pyth_box, DOWN, buff=0.3)
    scene.play(FadeIn(name), run_time=0.7)

    # --- 13. The drone: 36 + 64 = 100 ---------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    clear(scene)
    stage2, leg2, direct2, _ = drone_stage((-3.7, -1.6, 0), zoom=1.3)
    leg2.value = 2.0
    stage2.add_overlay(Vector(sky(0, 0, 0.03), sky(*EAST, 0.03), cfg.VEC_A, width=0.09),
                       Vector(sky(*EAST, 0.03), sky(*RES, 0.03), cfg.VEC_B, width=0.09),
                       Vector(sky(0, 0, 0.03), sky(*RES, 0.03), cfg.RESULT, width=0.11))
    show(scene, stage2, 0.8)
    lines = VGroup(eq([r"6^2", "+", r"8^2", "=", "36", "+", "64", "=", "100"], cfg.FONT["section"]),
                   eq([r"R", "=", r"\sqrt{100}", "=", r"10\ \mathrm{m}"], cfg.FONT["section"]),
                   eq([r"\theta", "=", r"\tan^{-1}\!\left(\tfrac{8}{6}\right)", r"\approx",
                       rf"{md.fixed(pm.direction_deg(RES), 2)}^\circ"], cfg.FONT["section"]))
    paint(lines[0], {0: cfg.VEC_A, 2: cfg.VEC_B, 4: cfg.VEC_A, 6: cfg.VEC_B})
    paint(lines[1], {0: cfg.RESULT, 4: cfg.RESULT})
    paint(lines[2], {0: cfg.GOLD, 4: cfg.GOLD})
    lines.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.9, 0.9, 0])
    scene.play(Write(lines[0]), run_time=2.2)

    # --- 14. sqrt(100) = 10 m --------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(Write(lines[1]), run_time=1.6)

    # --- 15. Direction: 53.13 degrees north of east ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 14)
    scene.play(Write(lines[2]), run_time=1.8)
    noe = txt("north of east", cfg.FONT["small"], cfg.GOLD).next_to(lines[2], DOWN, buff=0.25).align_to(lines[2], RIGHT)
    scene.play(FadeIn(noe), run_time=0.6)

    # --- 16. Two flights, one arrow ------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 15)
    direct2.value = 0.0
    scene.play(direct2.to(stage2, 1.0, run_time=3.5))
    summary = result_label(f"10 m at {md.fixed(pm.direction_deg(RES), 2)}°", cfg.RESULT, cfg.FONT["section"])
    summary.move_to([3.6, -2.9, 0])
    scene.play(FadeIn(summary, shift=UP * 0.15), run_time=0.8)

    # --- 17. Next: subtraction -----------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 16)
    hide(scene, stage2, 0.8, FadeOut(VGroup(lines, noe, summary)))
    teaser = paint(eq([r"\vec{A}", "-", r"\vec{B}", "=", r"\ ?"], cfg.FONT["hero"]), {0: cfg.VEC_A, 2: cfg.VEC_B, 4: cfg.RED})
    scene.play(Write(teaser), run_time=1.6)
    scene.play(Indicate(teaser[4], color=cfg.RED, scale_factor=1.3), run_time=1.2)
    scene.wait(3.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["07"])
