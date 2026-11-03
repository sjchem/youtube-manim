"""Scene 13 — adding by components (``physics_models.COMPONENTS``). A = 4i + 3j
and B = -2i + 5j are added one axis at a time: blue bars along x
(4 + (-2) = 2), rose bars up y (3 + 5 = 8), so R = 2i + 8j; the tip-to-tail
picture lands exactly on (2, 8), and |R| = root 68 = 8.25. Then four
vectors are summed with two running counters, and the general rule.
"""

from manim_scenes.common import *

A_V, B_V = pm.COMPONENTS
R_V = pm.add(A_V, B_V)
MANY = ((2.0, 1.0), (1.5, -2.0), (-3.0, 0.5), (1.0, 2.5))   # four illustrative steps


class Scene13ComponentSum(Scene):
    def construct(self) -> None:
        play_scene(self)


def term(value: float) -> str:
    return f"{value:.0f}" if value >= 0 else f"({value:.0f})"


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Adding by components")
    question = txt('A + B', cfg.FONT["body"], cfg.WHITE).move_to(UP * 2.4)
    scene.play(FadeIn(question, shift=UP * 0.15), run_time=0.9)

    # --- 2. One axis at a time -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    axes = VGroup(chip("x first", cfg.X_COLOR, cfg.FONT["body"]), chip("then y", cfg.Y_COLOR, cfg.FONT["body"])).arrange(RIGHT, buff=0.9)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in axes], lag_ratio=0.4), run_time=1.4)

    # --- 3. A = 4i + 3j, B = -2i + 5j --------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(question, axes)), run_time=0.5)
    grid = plane((-3, 6), (-1, 9), unit=0.66, at=(-4.6, -3.25, 0), faint=0.35)
    A = vec_on(grid, (0, 0), A_V, cfg.VEC_A, width=0.12)
    B = vec_on(grid, (0, 0), B_V, cfg.VEC_B, width=0.12)
    defs = VGroup(paint(eq([r"\vec{A}", "=", f"{A_V[0]:.0f}", r"\hat{\imath}", "+", f"{A_V[1]:.0f}", r"\hat{\jmath}"], cfg.FONT["section"]),
                        {0: cfg.VEC_A, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR}),
                  paint(eq([r"\vec{B}", "=", f"{B_V[0]:.0f}", r"\hat{\imath}", "+", f"{B_V[1]:.0f}", r"\hat{\jmath}"], cfg.FONT["section"]),
                        {0: cfg.VEC_B, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR}))
    defs.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0.8, 2.3, 0], aligned_edge=LEFT)
    scene.add(grid, A, B)
    scene.play(FadeIn(grid), A.grow_in(run_time=1.0), FadeIn(defs[0]), run_time=1.0)
    scene.play(B.grow_in(run_time=1.0), FadeIn(defs[1]), run_time=1.0)

    # --- 4. Horizontal: 4 + (-2) = 2 ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    lift = 0.0
    bar_a = Line(grid.c2p(0, lift), grid.c2p(A_V[0], lift), stroke_color=cfg.X_COLOR, stroke_width=14)
    bar_b = Line(grid.c2p(A_V[0], lift - 0.35), grid.c2p(R_V[0], lift - 0.35), stroke_color=mu.mix(cfg.X_COLOR, cfg.WHITE, 0.45), stroke_width=14)
    x_sum = paint(eq([r"R_x", "=", term(A_V[0]), "+", term(B_V[0]), "=", f"{R_V[0]:.0f}"], cfg.FONT["section"]), {0: cfg.X_COLOR, 6: cfg.GREEN})
    x_sum.next_to(defs, DOWN, buff=0.6).align_to(defs, LEFT)
    scene.play(Create(bar_a), run_time=0.8)
    scene.play(Create(bar_b), Write(x_sum), run_time=1.4)
    x_dot = glow_dot(grid.c2p(R_V[0], 0), cfg.GREEN, 0.1)
    scene.play(FadeIn(x_dot, scale=1.5), run_time=0.5)

    # --- 5. Vertical: 3 + 5 = 8 -----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    bar_ay = Line(grid.c2p(0, 0), grid.c2p(0, A_V[1]), stroke_color=cfg.Y_COLOR, stroke_width=14)
    bar_by = Line(grid.c2p(-0.35, A_V[1]), grid.c2p(-0.35, R_V[1]), stroke_color=mu.mix(cfg.Y_COLOR, cfg.WHITE, 0.45), stroke_width=14)
    y_sum = paint(eq([r"R_y", "=", term(A_V[1]), "+", term(B_V[1]), "=", f"{R_V[1]:.0f}"], cfg.FONT["section"]), {0: cfg.Y_COLOR, 6: cfg.GREEN})
    y_sum.next_to(x_sum, DOWN, buff=0.4).align_to(x_sum, LEFT)
    scene.play(Create(bar_ay), run_time=0.6)
    scene.play(Create(bar_by), Write(y_sum), run_time=1.4)

    # --- 6. R = 2i + 8j ------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    R = vec_on(grid, (0, 0), R_V, cfg.RESULT, width=0.13)
    scene.add(R)
    result = paint(eq([r"\vec{R}", "=", f"{R_V[0]:.0f}", r"\hat{\imath}", "+", f"{R_V[1]:.0f}", r"\hat{\jmath}"], cfg.FONT["section"]),
                   {0: cfg.RESULT, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR})
    result.next_to(y_sum, DOWN, buff=0.5).align_to(y_sum, LEFT)
    framed = boxed(result, cfg.RESULT)
    scene.play(R.grow_in(run_time=1.2), FadeIn(framed), run_time=1.2)

    # --- 7. Geometric check: tip to tail lands on (2, 8) ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    moved = vec_on(grid, A_V, R_V, cfg.VEC_B, width=0.12)
    scene.add(moved)
    scene.play(B.fade_to(0.3, run_time=0.6), FadeOut(VGroup(bar_a, bar_b, bar_ay, bar_by, x_dot)), run_time=0.6)
    scene.play(moved.grow_in(run_time=1.4), run_time=1.4)
    land = VGroup(glow_dot(grid.c2p(*R_V), cfg.GREEN, 0.11, reach=4),
                  eq(f"({R_V[0]:.0f},\\ {R_V[1]:.0f})", cfg.FONT["body"], cfg.GREEN).next_to(grid.c2p(*R_V), RIGHT, buff=0.3))
    scene.play(FadeIn(land, scale=1.3), run_time=0.8)

    # --- 8. |R| = root 68 = 8.25 ---------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    size = paint(eq([r"|\vec{R}|", "=", r"\sqrt{2^2 + 8^2}", "=", r"\sqrt{68}", r"\approx", md.fixed(pm.magnitude(R_V), 2)], cfg.FONT["body"]),
                 {0: cfg.RESULT, 6: cfg.RESULT})
    fit_width(size, 6.6)
    size.next_to(framed, DOWN, buff=0.4).align_to(framed, LEFT)
    scene.play(Write(size), run_time=1.8)

    # --- 9. Any number of vectors: add all the x parts, all the y parts ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    clear(scene, head)
    grid2 = plane((-3, 4), (-2, 4), unit=0.82, at=(-4.2, -0.7, 0), faint=0.35)
    scene.play(FadeIn(grid2), run_time=0.6)
    here, sx, sy = (0.0, 0.0), Knob(0.0), Knob(0.0)
    tally = VGroup(VGroup(txt("Σ x", cfg.FONT["body"], cfg.X_COLOR), DecimalNumber(0, num_decimal_places=1, font_size=72, color=cfg.WHITE, include_sign=True)),
                   VGroup(txt("Σ y", cfg.FONT["body"], cfg.Y_COLOR), DecimalNumber(0, num_decimal_places=1, font_size=72, color=cfg.WHITE, include_sign=True)))
    for row, knob in zip(tally, (sx, sy)):
        row.arrange(RIGHT, buff=0.4)
        row[1].add_updater(lambda m, k=knob: m.set_value(k.value))
        row[1].add_updater(lambda m, r=row: m.next_to(r[0], RIGHT, buff=0.4))
    tally.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([3.8, 0.6, 0])
    scene.play(FadeIn(tally), run_time=0.6)
    colors = (cfg.VEC_A, cfg.VEC_B, cfg.TEAL, cfg.ORANGE)
    for step, color in zip(MANY, colors):
        nxt = pm.add(here, step)
        arrow = vec_on(grid2, here, nxt, color, width=0.1)
        scene.add(arrow)
        scene.play(arrow.grow_in(run_time=1.0), sx.to(arrow, nxt[0], run_time=1.0), sy.to(arrow, nxt[1], run_time=1.0), run_time=1.0)
        here = nxt
    total = vec_on(grid2, (0, 0), here, cfg.RESULT, width=0.13)
    scene.add(total)
    scene.play(total.grow_in(run_time=1.2), run_time=1.2)

    # --- 10. In general: R_x = A_x + B_x, R_y = A_y + B_y -----------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    general = VGroup(paint(eq([r"R_x", "=", r"A_x + B_x"], cfg.FONT["section"]), {0: cfg.X_COLOR, 2: cfg.X_COLOR}),
                     paint(eq([r"R_y", "=", r"A_y + B_y"], cfg.FONT["section"]), {0: cfg.Y_COLOR, 2: cfg.Y_COLOR}))
    general.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(tally, DOWN, buff=0.7).align_to(tally, LEFT)
    scene.play(Write(general), run_time=1.8)

    # --- 11. Bookkeeping instead of geometry --------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    book = txt('component sum', cfg.FONT["label"], cfg.GOLD).move_to(DOWN * 3.65)
    scene.play(FadeIn(book, shift=UP * 0.15), run_time=0.8)

    # --- 12-14. The sentence to hold on to; next, motion ------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    clear(scene)
    hold = VGroup(txt('Components', cfg.FONT["section"], cfg.WHITE),
                  txt('x · y', cfg.FONT["section"], cfg.GOLD)).arrange(DOWN, buff=0.3).move_to(UP * 0.8)
    scene.play(FadeIn(hold[0], shift=UP * 0.15), run_time=0.9)
    scene.play(FadeIn(hold[1], shift=UP * 0.15), run_time=0.9)
    beat(scene, t, 12)
    key = chip('Projectile motion', cfg.CYAN, cfg.FONT["body"]).next_to(hold, DOWN, buff=0.7)
    scene.play(FadeIn(key, shift=UP * 0.2), Indicate(hold[1], color=cfg.GOLD, scale_factor=1.04), run_time=1.2)
    beat(scene, t, 13)
    trio = VGroup(txt("position", cfg.FONT["body"], cfg.POSITION), txt("velocity", cfg.FONT["body"], cfg.VELOCITY),
                  txt("acceleration", cfg.FONT["body"], cfg.ACCEL)).arrange(RIGHT, buff=0.9).move_to(DOWN * 3.0)
    scene.play(LaggedStart(*[FadeIn(w, shift=UP * 0.2) for w in trio], lag_ratio=0.35), run_time=1.6)
    scene.wait(6.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
