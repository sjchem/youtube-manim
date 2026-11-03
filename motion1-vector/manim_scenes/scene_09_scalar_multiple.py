"""Scene 09 — multiplying a vector by a scalar k. One live arrow k A
(A = 3i + 4j, ``physics_models.SCALED``) stretches for k > 1, shrinks for
0 < k < 1, turns round through zero for k < 0 and vanishes at k = 0. Then
F = m a on a cart: mass is a positive scalar, so the force and acceleration
arrows always point the same way; doubling the mass doubles the force.
"""

from manim_scenes.common import *

AX, AY = pm.SCALED
FORCE = cfg.ROSE


class Scene09ScalarMultiple(Scene):
    def construct(self) -> None:
        play_scene(self)


def cart(mass_blocks: int = 1) -> VGroup:
    body = RoundedRectangle(width=2.2, height=0.6, corner_radius=0.1, stroke_color=cfg.MUTED, stroke_width=3,
                            fill_color="#2A4D6B", fill_opacity=1)
    wheels = VGroup(*[Circle(radius=0.22, stroke_color=cfg.MUTED, stroke_width=3, fill_color="#14212C", fill_opacity=1)
                      .move_to(body.get_bottom() + RIGHT * dx + DOWN * 0.05) for dx in (-0.65, 0.65)])
    blocks = VGroup(*[Square(0.62, stroke_color=mu.shade(cfg.GOLD, 0.6), stroke_width=3, fill_color=cfg.GOLD,
                             fill_opacity=0.85) for _ in range(mass_blocks)]).arrange(RIGHT, buff=0.08)
    blocks.next_to(body, UP, buff=0.02)
    label = txt("m" if mass_blocks == 1 else "2m", cfg.FONT["small"], cfg.WHITE)
    fit_inside(label, body.width - 0.3, body.height - 0.16)
    label.move_to(body)
    return VGroup(wheels, body, blocks, label)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "09")
    show_chapter(scene, 4, "Scalar multiplication and unit vectors", hold=1.0)
    head = heading("Multiplying by a scalar")
    grid = plane((-4, 7), (-5, 9), unit=0.5, at=(-4.4, -1.15, 0))
    k = Knob(1.0)
    kA = vec_on(grid, (0, 0), lambda: (k.value * AX, k.value * AY), cfg.VEC_A, width=0.12)
    zero_dot = glow_dot(grid.c2p(0, 0), cfg.VEC_A, 0.09)
    zero_dot.set_opacity(0)
    k_num = DecimalNumber(1.0, num_decimal_places=2, font_size=96, color=cfg.GOLD, include_sign=True)
    k_num.add_updater(lambda m: m.set_value(k.value))
    k_row = VGroup(eq("k =", cfg.FONT["hero"], cfg.WHITE), k_num).arrange(RIGHT, buff=0.3).move_to([3.4, 2.3, 0])
    k_num.add_updater(lambda m: m.next_to(k_row[0], RIGHT, buff=0.3))
    scene.add(grid, kA)
    scene.play(FadeIn(head, shift=DOWN * 0.15), FadeIn(grid), kA.grow_in(run_time=1.0), run_time=1.0)
    scene.play(FadeIn(k_row), run_time=0.6)
    form = paint(eq([r"\vec{B}", "=", "k", r"\vec{A}"], cfg.FONT["title"]), {0: cfg.VEC_A, 2: cfg.GOLD, 3: cfg.VEC_A})
    form.next_to(k_row, DOWN, buff=0.5)
    scene.play(Write(form), run_time=1.0)

    def case(text: str, color: str) -> Text:
        return txt(text, cfg.FONT["label"], color).move_to([3.4, -1.3, 0])

    # --- 2. k > 1: stretch -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    note = case('k > 1', cfg.GREEN)
    scene.play(FadeIn(note), k.to(kA, 2.0, run_time=2.4), run_time=2.4)

    # --- 3. 0 < k < 1: shrink ------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    note = swap(scene, note, case('0 < k < 1', cfg.CYAN), 0.6)
    scene.play(k.to(kA, 0.5, run_time=2.4))

    # --- 4. k < 0: flips round, length times |k| -------------------------------------------------------------------------------
    beat(scene, t, 3)
    note = swap(scene, note, case('k < 0', cfg.RED), 0.6)
    scene.play(k.to(kA, -1.0, run_time=3.0))
    scale_note = txt("length × |k|", cfg.FONT["small"], cfg.MUTED).next_to(note, DOWN, buff=0.25)
    scene.play(FadeIn(scale_note), run_time=0.6)

    # --- 5. k = 0: the zero vector ---------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(scale_note), run_time=0.4)
    note = swap(scene, note, case('k = 0', cfg.MUTED), 0.6)
    scene.play(k.to(kA, 0.0, run_time=2.0))
    scene.play(zero_dot.animate.set_opacity(1), run_time=0.6)
    nodir = txt('0', cfg.FONT["small"], cfg.MUTED).next_to(note, DOWN, buff=0.25)
    scene.play(FadeIn(nodir), run_time=0.6)

    # --- 6. A = 3i + 4j ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(note, nodir, form)), zero_dot.animate.set_opacity(0), k.to(kA, 1.0, run_time=1.4), run_time=1.4)
    rows = VGroup(paint(eq([r"\vec{A}", "=", f"{AX:.0f}", r"\hat{\imath}", "+", f"{AY:.0f}", r"\hat{\jmath}"], cfg.FONT["section"]),
                        {0: cfg.VEC_A, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR}))
    rows[0].move_to([3.4, 0.6, 0])
    scene.play(Write(rows[0]), run_time=1.2)

    # --- 7. 2A = 6i + 8j: the length doubles ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    two = paint(eq([r"2\vec{A}", "=", f"{2 * AX:.0f}", r"\hat{\imath}", "+", f"{2 * AY:.0f}", r"\hat{\jmath}"], cfg.FONT["section"]),
                {0: cfg.VEC_A, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR})
    two.next_to(rows[0], DOWN, buff=0.4).align_to(rows[0], LEFT)
    scene.play(k.to(kA, 2.0, run_time=1.6), Write(two), run_time=1.6)
    length = eq([r"|2\vec{A}|", "=", f"{2 * pm.magnitude(pm.SCALED):.0f}", "=", r"2\,|\vec{A}|"], cfg.FONT["body"])
    paint(length, {0: cfg.VEC_A, 2: cfg.GREEN}).next_to(two, DOWN, buff=0.35).align_to(two, LEFT)
    scene.play(FadeIn(length), run_time=0.8)

    # --- 8. -A = -3i - 4j ------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    neg = paint(eq([r"-\vec{A}", "=", f"-{AX:.0f}", r"\hat{\imath}", "-", f"{AY:.0f}", r"\hat{\jmath}"], cfg.FONT["section"]),
                {0: cfg.VEC_A, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR})
    neg.next_to(length, DOWN, buff=0.4).align_to(length, LEFT)
    scene.play(k.to(kA, -1.0, run_time=2.0), Write(neg), run_time=2.0)
    flip = txt('−A', cfg.FONT["small"], cfg.RED).next_to(neg, DOWN, buff=0.25).align_to(neg, LEFT)
    scene.play(FadeIn(flip), run_time=0.6)

    # --- 9. Everywhere in physics -------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    clear(scene)

    # --- 10. Newton's second law: F_net = m a ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    newton = paint(eq([r"\vec{F}_{\text{net}}", "=", "m", r"\,\vec{a}"], cfg.FONT["hero"]), {0: FORCE, 2: cfg.GOLD, 3: cfg.ACCEL})
    newton.move_to(UP * 2.2)
    scene.play(Write(newton), run_time=1.6)

    # --- 11. Mass is a positive scalar: same direction ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    ground = Line([-7, -2.35, 0], [7, -2.35, 0], stroke_color=cfg.MUTED, stroke_width=3)
    x = Knob(-4.6)
    one = cart(1)
    one.add_updater(lambda m: m.move_to([x.value, -1.75, 0]))
    f_arrow = VecArrow(lambda: one.get_left() + LEFT * 1.9, lambda: one.get_left() + LEFT * 0.1, FORCE, width=0.12)
    a_arrow = VecArrow(lambda: one.get_top() + UP * 0.35, lambda: one.get_top() + UP * 0.35 + RIGHT * 1.6, cfg.ACCEL, width=0.1)
    tags = VGroup(eq(r"\vec{F}", cfg.FONT["body"], FORCE), eq(r"\vec{a}", cfg.FONT["body"], cfg.ACCEL))
    tags[0].add_updater(lambda m: m.next_to(f_arrow.tail(), UP, buff=0.25).shift(RIGHT * 0.8))
    tags[1].add_updater(lambda m: m.next_to(a_arrow.tip(), RIGHT, buff=0.2))
    scene.add(ground, one, f_arrow, a_arrow)
    scene.play(FadeIn(ground), FadeIn(one), f_arrow.grow_in(run_time=0.8), a_arrow.grow_in(run_time=0.8), FadeIn(tags),
               run_time=0.8)
    same = txt('m > 0', cfg.FONT["label"], cfg.WHITE).move_to([2.6, 0.5, 0])
    scene.play(FadeIn(same), x.to(one, -1.0, run_time=3.0, rate_func=rate_functions.ease_in_quad), run_time=3.0)

    # --- 12. Double the mass: twice the force for the same acceleration -------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    for m in (one, f_arrow, a_arrow, *tags):
        m.clear_updaters()
    scene.play(FadeOut(VGroup(one, f_arrow, a_arrow, tags, same)), run_time=0.6)
    x.value = -4.2
    heavy = cart(2)
    heavy.add_updater(lambda m: m.move_to([x.value, -1.75, 0]))
    f2 = VecArrow(lambda: heavy.get_left() + LEFT * 3.8, lambda: heavy.get_left() + LEFT * 0.1, FORCE, width=0.14)
    a2 = VecArrow(lambda: heavy.get_top() + UP * 0.35, lambda: heavy.get_top() + UP * 0.35 + RIGHT * 1.6, cfg.ACCEL, width=0.1)
    labels = VGroup(eq(r"2\vec{F}", cfg.FONT["body"], FORCE), eq(r"\vec{a}", cfg.FONT["body"], cfg.ACCEL))
    labels[0].add_updater(lambda m: m.next_to(f2.tail(), UP, buff=0.25).shift(RIGHT * 1.6))
    labels[1].add_updater(lambda m: m.next_to(a2.tip(), RIGHT, buff=0.2))
    scene.add(heavy, f2, a2)
    scene.play(FadeIn(heavy), f2.grow_in(run_time=0.8), a2.grow_in(run_time=0.8), FadeIn(labels), run_time=0.8)
    never = txt('F ∥ a', cfg.FONT["label"], cfg.WHITE).move_to([2.6, 0.5, 0])
    scene.play(FadeIn(never), x.to(heavy, 0.6, run_time=3.6, rate_func=rate_functions.ease_in_quad), run_time=3.6)

    # --- 13. What if we only care about direction? -------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    clear(scene)
    lines = VGroup(VGroup(txt("size", cfg.FONT["section"], cfg.GOLD), txt('|kA| = |k||A|', cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.4),
                   VGroup(txt("direction", cfg.FONT["section"], cfg.CYAN), txt('Â', cfg.FONT["body"], cfg.WHITE)).arrange(RIGHT, buff=0.4))
    lines.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.4)
    scene.play(FadeIn(lines[0], shift=UP * 0.15), run_time=0.9)
    scene.wait(3.0)
    scene.play(FadeIn(lines[1], shift=UP * 0.15), run_time=0.9)
    scene.play(Indicate(lines[1][0], color=cfg.CYAN, scale_factor=1.1), run_time=1.2)
    scene.wait(3.4)
    end_scene(scene, t, cfg.SCENE_DURATIONS["09"])
