"""Scene 10 — unit vectors. i-hat and j-hat on the unit circle; A = 3i + 4j
built from 3 copies of i-hat and 4 of j-hat; dividing by |A| = 5 shrinks the
arrow onto the unit circle as A-hat = (3/5) i + (4/5) j; multiplying back by
5 restores A. A-hat then sweeps the circle: every direction is one point.
"""

from manim_scenes.common import *

AX, AY = pm.SCALED
MAG = pm.magnitude(pm.SCALED)
UX, UY = pm.unit(pm.SCALED)


class Scene10UnitVectors(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "10", "Unit vectors")
    grid = plane((-2, 6), (-2, 5), unit=0.82, at=(-4.4, -1.9, 0))
    circle = Circle(radius=grid.unit, stroke_color=cfg.WHITE, stroke_width=4, stroke_opacity=0.8).move_to(grid.c2p(0, 0))
    i_hat = vec_on(grid, (0, 0), (1, 0), cfg.X_COLOR, width=0.1, tip_len=0.26)
    j_hat = vec_on(grid, (0, 0), (0, 1), cfg.Y_COLOR, width=0.1, tip_len=0.26)
    scene.add(grid)
    scene.play(FadeIn(grid), Create(circle), run_time=1.2)
    one = txt("length = 1", cfg.FONT["label"], cfg.WHITE).move_to([4.0, 2.6, 0])
    scene.play(FadeIn(one), run_time=0.6)

    # --- 2. i-hat and j-hat -----------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.add(i_hat, j_hat)
    scene.play(i_hat.grow_in(run_time=0.9), run_time=0.9)
    scene.play(j_hat.grow_in(run_time=0.9), run_time=0.9)
    names = VGroup(eq(r"\hat{\imath}", cfg.FONT["section"], cfg.X_COLOR).next_to(circle, RIGHT, buff=0.3).shift(DOWN * 0.35),
                   eq(r"\hat{\jmath}", cfg.FONT["section"], cfg.Y_COLOR).next_to(circle, UP, buff=0.3).shift(LEFT * 0.4))
    defs = VGroup(eq([r"\hat{\imath} = (1,\ 0)"], cfg.FONT["section"], cfg.X_COLOR),
                  eq([r"\hat{\jmath} = (0,\ 1)"], cfg.FONT["section"], cfg.Y_COLOR)).arrange(DOWN, buff=0.3).move_to([4.0, 1.2, 0])
    scene.play(FadeIn(names), FadeIn(defs), run_time=0.9)

    # --- 3. A x copies of i-hat, A y copies of j-hat ----------------------------------------------------------------------------
    beat(scene, t, 2)
    copies = VGroup(*[VecArrow(grid.c2p(n, 0), grid.c2p(n + 1, 0), cfg.X_COLOR, width=0.08, tip_len=0.22, live=False)
                      for n in range(int(AX))],
                    *[VecArrow(grid.c2p(AX, n), grid.c2p(AX, n + 1), cfg.Y_COLOR, width=0.08, tip_len=0.22, live=False)
                      for n in range(int(AY))])
    scene.play(LaggedStart(*[FadeIn(c, shift=(c.tip() - c.tail()) * 0.5) for c in copies], lag_ratio=0.25), run_time=2.6)
    A = vec_on(grid, (0, 0), (AX, AY), cfg.VEC_A, width=0.12)
    scene.add(A)
    scene.play(A.grow_in(run_time=1.0), run_time=1.0)
    build = paint(eq([r"\vec{A}", "=", f"{AX:.0f}", r"\hat{\imath}", "+", f"{AY:.0f}", r"\hat{\jmath}"], cfg.FONT["section"]),
                  {0: cfg.VEC_A, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR}).move_to([4.0, -0.6, 0])
    scene.play(Write(build), run_time=1.2)

    # --- 4. Unit vector along any arrow: divide by its length ----------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(copies), FadeOut(defs), FadeOut(one), run_time=0.6)
    hat_rule = paint(eq([r"\hat{A}", "=", r"\frac{\vec{A}}{|\vec{A}|}"], cfg.FONT["title"]), {0: cfg.CYAN, 2: cfg.VEC_A})
    hat_rule.move_to([4.0, 1.9, 0])
    scene.play(Write(hat_rule), run_time=1.4)

    # --- 5. |A| = 5 --------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    mag = paint(eq([r"|\vec{A}|", "=", r"\sqrt{3^2 + 4^2}", "=", f"{MAG:.0f}"], cfg.FONT["section"]), {0: cfg.VEC_A, 4: cfg.GREEN})
    mag.next_to(build, DOWN, buff=0.45)
    scene.play(Write(mag), run_time=1.4)

    # --- 6. Divide by five: onto the unit circle --------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    k = Knob(1.0)
    angle = Knob(np.arctan2(AY, AX))
    hat = vec_on(grid, (0, 0), lambda: (k.value * MAG * np.cos(angle.value), k.value * MAG * np.sin(angle.value)), cfg.CYAN,
                 width=0.12, tip_len=0.28)
    scene.add(hat)
    scene.play(A.fade_to(0, run_time=0.5), run_time=0.5)
    scene.remove(A)
    A.clear_updaters()
    scene.play(k.to(hat, 1 / MAG, run_time=2.2))
    hat_vals = paint(eq([r"\hat{A}", "=", r"\tfrac{3}{5}", r"\hat{\imath}", "+", r"\tfrac{4}{5}", r"\hat{\jmath}"], cfg.FONT["section"]),
                     {0: cfg.CYAN, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR})
    hat_vals.next_to(mag, DOWN, buff=0.45)
    scene.play(Write(hat_vals), Indicate(circle, color=cfg.CYAN, scale_factor=1.05), run_time=1.6)
    same_way = txt("same direction", cfg.FONT["small"], cfg.CYAN).next_to(grid.c2p(UX, UY), UR, buff=0.25)
    scene.play(FadeIn(same_way), run_time=0.6)

    # --- 7. Five: how much. A-hat: which way ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(hat_rule, build, mag, hat_vals, same_way)), run_time=0.6)
    split = VGroup(VGroup(eq("5", cfg.FONT["hero"], cfg.GREEN), txt("how much", cfg.FONT["body"], cfg.WHITE)).arrange(DOWN, buff=0.2),
                   VGroup(eq(r"\hat{A}", cfg.FONT["hero"], cfg.CYAN), txt("which way", cfg.FONT["body"], cfg.WHITE)).arrange(DOWN, buff=0.2))
    split.arrange(RIGHT, buff=1.2).move_to([4.1, 1.4, 0])
    scene.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in split], lag_ratio=0.4), run_time=1.4)

    # --- 8. Multiply back: the vector reappears ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    back = paint(eq(["5", r"\,\hat{A}", "=", r"\vec{A}"], cfg.FONT["title"]), {0: cfg.GREEN, 1: cfg.CYAN, 3: cfg.VEC_A})
    back.move_to([4.1, -1.2, 0])
    scene.play(Write(back), k.to(hat, 1.0, run_time=1.8), run_time=1.8)
    scene.play(k.to(hat, 1 / MAG, run_time=1.2), run_time=1.2)

    # --- 9. Every direction is a spot on the circle ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    trace = TracedPath(lambda: hat.tip(), stroke_color=cfg.CYAN, stroke_width=8, stroke_opacity=0.7)
    scene.add(trace)
    scene.play(angle.to(hat, angle.value + TAU, run_time=4.4, rate_func=smooth))
    trace.clear_updaters()

    # --- 10. Size and direction ----------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    clear(scene, head)
    pair = VGroup(VGroup(txt("scalar multiplication", cfg.FONT["body"], cfg.GOLD), txt('kA', cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.2),
                  VGroup(txt("unit vectors", cfg.FONT["body"], cfg.CYAN), txt('Â', cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.2))
    pair.arrange(RIGHT, buff=1.4).move_to(UP * 1.2)
    scene.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pair], lag_ratio=0.4), run_time=1.6)

    # --- 11. Any vector = magnitude x direction. Next: the big idea ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    whole = paint(eq([r"\vec{A}", "=", r"|\vec{A}|", r"\,\hat{A}"], cfg.FONT["hero"]), {0: cfg.VEC_A, 2: cfg.GREEN, 3: cfg.CYAN})
    whole.move_to(DOWN * 1.2)
    scene.play(Write(whole), run_time=1.6)
    scene.play(Indicate(whole, color=cfg.GOLD, scale_factor=1.06), run_time=1.4)
    nxt = chip('Components', cfg.CYAN, cfg.FONT["body"]).move_to(DOWN * 3.3)
    scene.play(FadeIn(nxt, shift=UP * 0.2), run_time=1.0)
    scene.wait(6.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["10"])
