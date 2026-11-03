"""Scene 06 — why vectors add as arrows. 5 m east + 5 m east is 10 m east;
5 m east + 5 m west is zero; in between, a live B swings around A's tip and
the green resultant grows and shrinks. Tip-to-tail both ways round closes a
parallelogram (commutative); three vectors grouped two ways land on one
point (associative). Every vector comes from ``physics_models``.
"""

from manim_scenes.common import *

M = 0.55                       # screen units per metre on the walking lines


class Scene06WhyAdd(Scene):
    def construct(self) -> None:
        play_scene(self)


def path_of(start, vectors, colors, scale: float, width: float = 0.11) -> tuple[list[VecArrow], np.ndarray]:
    """Tip-to-tail arrows from ``start``; returns the arrows and the final point."""
    arrows, here = [], np.asarray(start, dtype=float)
    for v, color in zip(vectors, colors):
        there = here + np.array([v[0], v[1], 0.0]) * scale
        arrows.append(VecArrow(here, there, color, width=width))
        here = there
    return arrows, here


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "06")
    opener = txt("Vector addition and subtraction", cfg.FONT["title"], cfg.WHITE)
    fit_width(opener, 12.4)
    opener.move_to(ORIGIN)
    scene.play(FadeIn(opener, shift=LEFT * 0.3), run_time=0.9)
    scene.wait(1.0)
    scene.play(FadeOut(opener, shift=UP * 0.3), run_time=0.6)
    head = heading("Why add vectors?")
    scene.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.6)

    # --- 2. R = A + B ------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    law = paint(eq([r"\vec{R}", "=", r"\vec{A}", "+", r"\vec{B}"], cfg.FONT["title"]),
                {0: cfg.RESULT, 2: cfg.VEC_A, 4: cfg.VEC_B}).move_to(UP * 2.55)
    scene.play(Write(law), run_time=1.3)

    # --- 3. 5 m east + 5 m east = 10 m east ------------------------------------------------------------------------------------
    beat(scene, t, 2)
    row1 = np.array([-5.6, 0.85, 0])
    a1, b1 = path_of(row1, pm.SAME_WAY, (cfg.VEC_A, cfg.VEC_B), M)[0]
    total1 = pm.add(*pm.SAME_WAY)
    r1 = VecArrow(row1 + DOWN * 0.55, row1 + DOWN * 0.55 + RIGHT * total1[0] * M, cfg.RESULT, width=0.11)
    tag1 = eq(rf"{total1[0]:.0f}\ \mathrm{{m\ east}}", cfg.FONT["body"], cfg.RESULT).next_to(r1, RIGHT, buff=0.35)
    labels1 = VGroup(eq(r"5\ \mathrm{m}", cfg.FONT["small"], cfg.VEC_A).next_to(a1, UP, buff=0.15),
                     eq(r"5\ \mathrm{m}", cfg.FONT["small"], cfg.VEC_B).next_to(b1, UP, buff=0.15))
    scene.add(a1, b1, r1)
    scene.play(a1.grow_in(run_time=1.0), FadeIn(labels1[0]), run_time=1.0)
    scene.play(b1.grow_in(run_time=1.0), FadeIn(labels1[1]), run_time=1.0)
    scene.play(r1.grow_in(run_time=1.0), FadeIn(tag1), run_time=1.0)

    # --- 4. 5 m east + 5 m west = zero ------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    row2 = np.array([-5.6, -1.75, 0])
    a2 = VecArrow(row2, row2 + RIGHT * 5 * M, cfg.VEC_A, width=0.11)
    b2 = VecArrow(row2 + RIGHT * 5 * M + UP * 0.32, row2 + UP * 0.32, cfg.VEC_B, width=0.11)
    labels2 = VGroup(eq(r"5\ \mathrm{m\ east}", cfg.FONT["small"], cfg.VEC_A).next_to(a2, DOWN, buff=0.18),
                     eq(r"5\ \mathrm{m\ west}", cfg.FONT["small"], cfg.VEC_B).next_to(b2, UP, buff=0.18))
    scene.add(a2, b2)
    scene.play(a2.grow_in(run_time=1.0), FadeIn(labels2[0]), run_time=1.0)
    scene.play(b2.grow_in(run_time=1.0), FadeIn(labels2[1]), run_time=1.0)
    zero = VGroup(glow_dot(row2, cfg.RESULT, 0.12),
                  eq(r"\vec{R} = \vec{0}", cfg.FONT["body"], cfg.RESULT).next_to(row2 + RIGHT * 5 * M, RIGHT, buff=0.9))
    scene.play(FadeIn(zero, scale=1.3), run_time=1.0)

    # --- 5. Same distances, different results: direction --------------------------------------------------------------------------------------
    beat(scene, t, 4)
    same = txt('resultant', cfg.FONT["label"], cfg.WHITE).move_to(DOWN * 3.55)
    scene.play(FadeIn(same, shift=UP * 0.15), run_time=0.8)
    scene.play(Indicate(tag1, color=cfg.RESULT), Indicate(zero[1], color=cfg.RESULT), run_time=1.2)

    # --- 6. In between: partly reinforce, partly cancel ------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    clear(scene, head, law)
    o = np.array([-4.2, -1.9, 0])
    a_len, b_len = 3.4, 2.4
    phi = Knob(30 * DEGREES)
    a_tip = o + RIGHT * a_len
    b_tip = lambda: a_tip + b_len * np.array([np.cos(phi.value), np.sin(phi.value), 0])  # noqa: E731
    A = VecArrow(o, a_tip, cfg.VEC_A, width=0.12)
    B = VecArrow(a_tip, b_tip, cfg.VEC_B, width=0.12)
    R = VecArrow(o, b_tip, cfg.RESULT, width=0.12)
    names = VGroup(eq(r"\vec{A}", cfg.FONT["body"], cfg.VEC_A).next_to(o + RIGHT * a_len / 2, DOWN, buff=0.3))
    b_name = eq(r"\vec{B}", cfg.FONT["body"], cfg.VEC_B)
    b_name.add_updater(lambda m: m.move_to(a_tip + 0.5 * (b_tip() - a_tip) + 0.5 * np.array(
        [-np.sin(phi.value), np.cos(phi.value), 0]) * np.sign(np.cos(phi.value) + 1e-6)))
    meter_r = DecimalNumber(0, num_decimal_places=1, font_size=56, color=cfg.RESULT)
    meter_r.add_updater(lambda m: m.set_value(float(np.linalg.norm(b_tip() - o))))
    sums = VGroup(VGroup(eq(r"|\vec{A}| + |\vec{B}| =", cfg.FONT["body"]), eq(f"{a_len + b_len:.1f}", cfg.FONT["body"])),
                  VGroup(eq(r"|\vec{R}| =", cfg.FONT["body"], cfg.RESULT), meter_r))
    for row in sums:
        row.arrange(RIGHT, buff=0.25)
    sums.arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to([4.2, -0.6, 0])
    scene.add(A, B, R)
    scene.play(A.grow_in(run_time=0.8), FadeIn(names), run_time=0.8)
    scene.play(B.grow_in(run_time=0.8), FadeIn(b_name), run_time=0.8)
    scene.play(R.grow_in(run_time=0.8), FadeIn(sums), run_time=0.8)
    scene.play(phi.to(R, 150 * DEGREES, run_time=3.0))
    scene.play(phi.to(R, 60 * DEGREES, run_time=2.0))

    # --- 7. Tip to tail: tail of B on the head of A ----------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    for m in (meter_r, b_name):
        m.clear_updaters()
    scene.play(FadeOut(sums), run_time=0.5)
    clear(scene, head, law)
    av, bv = pm.COMMUTE
    o = np.array([-2.4, -2.6, 0])
    s = 1.05
    (A1, B1), end = path_of(o, (av, bv), (cfg.VEC_A, cfg.VEC_B), s, 0.12)
    R1 = VecArrow(o, end, cfg.RESULT, width=0.12)
    tail_dot = glow_dot(o, cfg.WHITE, 0.07)
    scene.add(A1, B1, R1)
    scene.play(FadeIn(tail_dot), A1.grow_in(run_time=1.0), run_time=1.0)
    scene.play(B1.grow_in(run_time=1.0), run_time=1.0)
    scene.play(R1.grow_in(run_time=1.2), run_time=1.2)
    tags = VGroup(eq(r"\vec{A}", cfg.FONT["body"], cfg.VEC_A).next_to(A1, DOWN, buff=0.2),
                  eq(r"\vec{B}", cfg.FONT["body"], cfg.VEC_B).next_to(B1, RIGHT, buff=0.2),
                  eq(r"\vec{R}", cfg.FONT["body"], cfg.RESULT).move_to((o + end) / 2 + LEFT * 0.5 + UP * 0.3))
    scene.play(FadeIn(tags), run_time=0.8)

    # --- 8. Swap the order: same endpoint ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    (B2, A2), end2 = path_of(o, (bv, av), (cfg.VEC_B, cfg.VEC_A), s, 0.12)
    for arrow in (B2, A2):
        arrow.alpha = 0.75
    scene.add(B2, A2)
    scene.play(B2.grow_in(run_time=1.2), run_time=1.2)
    scene.play(A2.grow_in(run_time=1.2), run_time=1.2)
    land = glow_dot(end2, cfg.RESULT, 0.1, reach=4)
    scene.play(FadeIn(land, scale=1.5), run_time=0.8)
    swap_eq = paint(eq([r"\vec{A}", "+", r"\vec{B}", "=", r"\vec{B}", "+", r"\vec{A}"], cfg.FONT["section"]),
                    {0: cfg.VEC_A, 2: cfg.VEC_B, 4: cfg.VEC_B, 6: cfg.VEC_A}).move_to([4.5, 1.2, 0])
    scene.play(Write(swap_eq), run_time=1.4)

    # --- 9. Commutative ----------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    comm = result_label("commutative", cfg.GOLD, cfg.FONT["section"]).next_to(swap_eq, DOWN, buff=0.4)
    scene.play(FadeIn(comm, shift=UP * 0.15), run_time=0.8)

    # --- 10. Three vectors, grouped two ways ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    clear(scene, head, law)
    av, bv, cv = pm.ASSOCIATIVE
    s = 1.45
    o = np.array([-3.6, -2.7, 0])
    ab = pm.add(av, bv)
    bc = pm.add(bv, cv)
    (A3, B3, C3), end3 = path_of(o, (av, bv, cv), (cfg.VEC_A, cfg.VEC_B, cfg.TEAL), s, 0.11)
    AB = VecArrow(o, o + np.array([*ab, 0]) * s, cfg.ORANGE, width=0.09)
    BC = VecArrow(A3.tip(), A3.tip() + np.array([*bc, 0]) * s, cfg.ROSE, width=0.09)
    R3 = VecArrow(o, end3, cfg.RESULT, width=0.13)
    c_lab = eq(r"\vec{C}", cfg.FONT["body"], cfg.TEAL).next_to(C3.get_center(), DL, buff=0.25)
    scene.add(A3, B3, C3)
    scene.play(A3.grow_in(run_time=0.7), run_time=0.7)
    scene.play(B3.grow_in(run_time=0.7), run_time=0.7)
    scene.play(C3.grow_in(run_time=0.7), FadeIn(c_lab), run_time=0.7)
    first = paint(eq([r"(\vec{A}+\vec{B})", "+", r"\vec{C}"], cfg.FONT["body"]), {0: cfg.ORANGE, 2: cfg.TEAL})
    second = paint(eq([r"\vec{A}", "+", r"(\vec{B}+\vec{C})"], cfg.FONT["body"]), {0: cfg.VEC_A, 2: cfg.ROSE})
    VGroup(first, second).arrange(DOWN, buff=0.5).move_to([3.9, 0.4, 0])
    scene.add(AB)
    scene.play(AB.grow_in(run_time=1.0), FadeIn(first), run_time=1.0)
    scene.wait(1.2)
    scene.add(BC)
    scene.play(BC.grow_in(run_time=1.0), FadeIn(second), run_time=1.0)
    scene.add(R3)
    scene.play(R3.grow_in(run_time=1.2), run_time=1.2)
    scene.play(FadeIn(glow_dot(end3, cfg.RESULT, 0.1, reach=4), scale=1.5), run_time=0.8)

    # --- 11. Associative ------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    assoc = result_label("associative", cfg.GOLD, cfg.FONT["section"]).next_to(second, DOWN, buff=0.5)
    scene.play(FadeIn(assoc, shift=UP * 0.15), run_time=0.8)

    # --- 12. Order and grouping don't matter -----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    only = txt('vector sum', cfg.FONT["label"], cfg.WHITE).move_to(DOWN * 3.6 + RIGHT * 3.6)
    scene.play(FadeIn(only, shift=UP * 0.15), run_time=0.8)
    scene.play(Indicate(R3, color=cfg.RESULT, scale_factor=1.05), run_time=1.2)

    # --- 13. How long, which way? Two geometric tools ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    clear(scene, run_time=0.8)
    question = txt('magnitude · direction', cfg.FONT["title"], cfg.WHITE).move_to(UP * 1.6)
    tools = VGroup(chip("triangle law", cfg.GOLD, cfg.FONT["body"]), chip("parallelogram law", cfg.PURPLE, cfg.FONT["body"]))
    tools.arrange(RIGHT, buff=0.8).next_to(question, DOWN, buff=0.9)
    scene.play(FadeIn(question, shift=UP * 0.15), run_time=0.9)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in tools], lag_ratio=0.4), run_time=1.6)
    a, b = np.array([1.5, 0.0, 0]), np.array([0.6, 1.1, 0])
    tri_o = tools[0].get_bottom() + DOWN * 2.1 + LEFT * 1.0
    par_o = tools[1].get_bottom() + DOWN * 2.1 + LEFT * 1.0
    sketches = VGroup(
        VecArrow(tri_o, tri_o + a, cfg.VEC_A, width=0.07, tip_len=0.2, live=False),
        VecArrow(tri_o + a, tri_o + a + b, cfg.VEC_B, width=0.07, tip_len=0.2, live=False),
        VecArrow(tri_o, tri_o + a + b, cfg.RESULT, width=0.07, tip_len=0.2, live=False),
        VecArrow(par_o, par_o + a, cfg.VEC_A, width=0.07, tip_len=0.2, live=False),
        VecArrow(par_o, par_o + b, cfg.VEC_B, width=0.07, tip_len=0.2, live=False),
        DashedLine(par_o + a, par_o + a + b, stroke_color=cfg.MUTED, stroke_width=3),
        DashedLine(par_o + b, par_o + a + b, stroke_color=cfg.MUTED, stroke_width=3),
        VecArrow(par_o, par_o + a + b, cfg.RESULT, width=0.07, tip_len=0.2, live=False))
    scene.play(LaggedStart(*[FadeIn(m) for m in sketches], lag_ratio=0.15), run_time=2.0)
    scene.wait(4.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
