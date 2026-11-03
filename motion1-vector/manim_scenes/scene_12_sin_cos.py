"""Scene 12 — components from sine and cosine. One live vector (length A,
angle theta) drops its components into a right triangle: A_x = A cos(theta),
A_y = A sin(theta), read off live as the angle sweeps flat, upright and past
90 degrees (where A_x turns negative). The brief's example, 10 at 30 degrees
(``physics_models.RESOLVED``), gives 8.66 i + 5 j. Then the quadrant trap:
for (-3, 4) the plain inverse tangent answers -53 degrees; atan2 gives 126.9.
"""

from manim_scenes.common import *

L0, DEG0 = pm.RESOLVED
TRAP = pm.QUADRANT_TRAP


class Scene12SinCos(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "12", "Sine, cosine, components")
    grid = plane((-9, 9), (-6, 8), unit=0.4, at=(-3.6, -0.6, 0), faint=0.35)
    length, theta = Knob(8.0), Knob(38 * DEGREES)
    tip = lambda: (length.value * np.cos(theta.value), length.value * np.sin(theta.value))  # noqa: E731
    A = vec_on(grid, (0, 0), tip, cfg.VEC_A, width=0.12)
    arc = always_redraw(lambda: angle_arc(grid.c2p(0, 0), 0, np.degrees(theta.value), 0.75, cfg.WHITE, 4))
    th_lab = eq(r"\theta", cfg.FONT["body"], cfg.WHITE)
    th_lab.add_updater(lambda m: m.move_to(grid.c2p(0, 0) + 1.15 * np.array([np.cos(theta.value / 2), np.sin(theta.value / 2), 0])))
    scene.add(grid, A)
    scene.play(FadeIn(grid), A.grow_in(run_time=1.0), run_time=1.0)
    scene.play(Create(arc), FadeIn(th_lab), run_time=0.8)
    a_lab = eq("A", cfg.FONT["body"], cfg.VEC_A)
    a_lab.add_updater(lambda m: m.move_to(grid.c2p(*tip()) * 0.55 + grid.c2p(0, 0) * 0.45 + 0.45 * np.array(
        [-np.sin(theta.value), np.cos(theta.value), 0])))
    scene.play(FadeIn(a_lab), run_time=0.5)

    # --- 2. Drop the components: a right triangle ----------------------------------------------------------------------------
    beat(scene, t, 1)
    cx = vec_on(grid, (0, 0), lambda: (tip()[0], 0), cfg.X_COLOR, width=0.1)
    cy = vec_on(grid, lambda: (tip()[0], 0), tip, cfg.Y_COLOR, width=0.1)
    scene.add(cx, cy)
    scene.play(cx.grow_in(run_time=0.9), run_time=0.9)
    scene.play(cy.grow_in(run_time=0.9), run_time=0.9)
    square = always_redraw(lambda: right_angle_mark(grid.c2p(tip()[0], 0), LEFT * np.sign(tip()[0] + 1e-9), UP, 0.26))
    hyp = txt("hypotenuse", cfg.FONT["small"], cfg.VEC_A).move_to(grid.c2p(1.2, 6.0))
    scene.play(FadeIn(square), FadeIn(hyp), run_time=0.7)

    # --- 3. cos theta = A_x / A -------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    cos_eq = VGroup(paint(eq([r"\cos\theta", "=", r"\frac{A_x}{A}"], cfg.FONT["label"]), {2: cfg.X_COLOR}),
                    paint(eq([r"A_x", "=", r"A\cos\theta"], cfg.FONT["label"]), {0: cfg.X_COLOR, 2: cfg.X_COLOR}))
    cos_eq.arrange(RIGHT, buff=0.7).move_to([4.3, 1.6, 0])
    scene.play(FadeOut(hyp), Write(cos_eq[0]), run_time=1.3)
    cos_box = boxed(cos_eq[1], cfg.X_COLOR)
    scene.play(FadeIn(cos_box), run_time=1.0)

    # --- 4. sin theta = A_y / A -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    sin_eq = VGroup(paint(eq([r"\sin\theta", "=", r"\frac{A_y}{A}"], cfg.FONT["label"]), {2: cfg.Y_COLOR}),
                    paint(eq([r"A_y", "=", r"A\sin\theta"], cfg.FONT["label"]), {0: cfg.Y_COLOR, 2: cfg.Y_COLOR}))
    sin_eq.arrange(RIGHT, buff=0.7).next_to(cos_eq, DOWN, buff=0.55)
    scene.play(Write(sin_eq[0]), run_time=1.3)
    sin_box = boxed(sin_eq[1], cfg.Y_COLOR)
    scene.play(FadeIn(sin_box), run_time=1.0)

    # --- 5. How strongly it points along each axis --------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    meters = VGroup()
    for name, fn, color in ((r"\cos\theta =", np.cos, cfg.X_COLOR), (r"\sin\theta =", np.sin, cfg.Y_COLOR)):
        number = DecimalNumber(fn(theta.value), num_decimal_places=2, font_size=42, color=color, include_sign=True)
        number.add_updater(lambda m, f=fn: m.set_value(f(theta.value)))
        meters.add(VGroup(eq(name, cfg.FONT["small"], color), number).arrange(RIGHT, buff=0.25))
    meters.arrange(RIGHT, buff=0.7).move_to([4.3, -1.6, 0])
    for row in meters:
        row[1].add_updater(lambda m, r=row: m.next_to(r[0], RIGHT, buff=0.25))
    scene.play(FadeIn(meters), run_time=0.8)

    # --- 6. Flat: cos = 1. Upright: sin = 1 ------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(theta.to(A, 0.0, run_time=2.2))
    scene.wait(1.0)
    scene.play(theta.to(A, PI / 2, run_time=2.6))

    # --- 7. Past ninety degrees: cos turns negative ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(theta.to(A, 140 * DEGREES, run_time=2.6))
    left = txt('Aₓ < 0', cfg.FONT["small"], cfg.X_COLOR).next_to(meters, DOWN, buff=0.35)
    scene.play(FadeIn(left), Indicate(meters[0][1], color=cfg.X_COLOR), run_time=1.0)
    scene.play(theta.to(A, 215 * DEGREES, run_time=2.4))
    scene.play(theta.to(A, 38 * DEGREES, run_time=2.2))

    # --- 8. An example: 10 at 30 degrees ---------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    for row in meters:
        for m in row:
            m.clear_updaters()
    scene.play(FadeOut(VGroup(cos_eq[0], sin_eq[0], cos_box, sin_box, left)), FadeOut(meters), FadeOut(head),
               length.to(A, L0, run_time=1.6), theta.to(A, DEG0 * DEGREES, run_time=1.6), run_time=1.6)
    given = eq([r"A = 10", r",\quad", rf"\theta = {DEG0:.0f}^\circ"], cfg.FONT["section"]).move_to([4.3, 2.9, 0])
    scene.play(FadeIn(given), run_time=0.8)

    # --- 9. A_x = 8.66, A_y = 5 -----------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    ax, ay = pm.resolve(L0, DEG0)
    work = VGroup(paint(eq([r"A_x", "=", rf"10\cos {DEG0:.0f}^\circ", r"\approx", md.fixed(ax, 2)], cfg.FONT["section"]), {0: cfg.X_COLOR, 4: cfg.X_COLOR}),
                  paint(eq([r"A_y", "=", rf"10\sin {DEG0:.0f}^\circ", "=", md.fixed(ay, 0)], cfg.FONT["section"]), {0: cfg.Y_COLOR, 4: cfg.Y_COLOR}))
    work.arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(given, DOWN, buff=0.5)
    scene.play(Write(work[0]), run_time=1.5)
    scene.play(Write(work[1]), run_time=1.5)

    # --- 10. A = 8.66 i + 5 j ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    whole = paint(eq([r"\vec{A}", r"\approx", md.fixed(ax, 2), r"\,\hat{\imath}", "+", md.fixed(ay, 0), r"\,\hat{\jmath}"], cfg.FONT["section"]),
                  {0: cfg.VEC_A, 2: cfg.X_COLOR, 3: cfg.X_COLOR, 5: cfg.Y_COLOR, 6: cfg.Y_COLOR})
    whole.next_to(work, DOWN, buff=0.5)
    boxed_whole = boxed(whole, cfg.VEC_A)
    scene.play(FadeIn(boxed_whole), run_time=1.2)

    # --- 11. Backwards: Pythagoras gives the length -----------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(given, work)), boxed_whole.animate.move_to([4.3, -3.2, 0]), run_time=0.5)
    back = VGroup(paint(eq([r"A", "=", r"\sqrt{A_x^2 + A_y^2}"], cfg.FONT["section"]), {0: cfg.VEC_A}),
                  eq([r"\theta", "=", r"\operatorname{atan2}(A_y,\ A_x)"], cfg.FONT["section"]))
    back.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([4.3, 2.4, 0])
    scene.play(Write(back[0]), run_time=1.4)
    scene.play(Write(back[1]), run_time=1.4)

    # --- 12. The trap: (-3, 4) ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(boxed_whole), run_time=0.4)
    trap_len, trap_deg = pm.magnitude(TRAP), pm.direction_deg(TRAP)
    scene.play(length.to(A, trap_len, run_time=1.6), theta.to(A, trap_deg * DEGREES, run_time=1.6), run_time=1.6)
    point = eq(rf"({TRAP[0]:.0f},\ {TRAP[1]:.0f})", cfg.FONT["body"], cfg.VEC_A).next_to(grid.c2p(*TRAP), UP, buff=0.25)
    scene.play(FadeIn(point), run_time=0.6)
    naive = pm.naive_direction_deg(TRAP)
    wrong_eq = eq([r"\tan^{-1}\!\left(\tfrac{4}{-3}\right)", r"\approx", rf"{md.fixed(naive, 0)}^\circ"], cfg.FONT["body"])
    paint(wrong_eq, {2: cfg.RED}).next_to(back, DOWN, buff=0.6).align_to(back, LEFT)
    scene.play(Write(wrong_eq), run_time=1.4)
    wrong = vec_on(grid, (0, 0), (trap_len * np.cos(np.radians(naive)), trap_len * np.sin(np.radians(naive))), cfg.RED, width=0.1)
    wrong.alpha = 0.85
    scene.add(wrong)
    scene.play(wrong.grow_in(run_time=1.2), run_time=1.2)
    quad = txt("wrong quadrant", cfg.FONT["label"], cfg.RED).next_to(grid.c2p(2.5, -4.0), RIGHT, buff=0.2)
    scene.play(FadeIn(quad), run_time=0.6)

    # --- 13. atan2 looks at both signs: 126.9 degrees ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    right_eq = eq([r"\operatorname{atan2}(4,\ -3)", "=", rf"{md.fixed(trap_deg, 1)}^\circ"], cfg.FONT["body"])
    paint(right_eq, {2: cfg.GREEN}).next_to(wrong_eq, DOWN, buff=0.5).align_to(wrong_eq, LEFT)
    scene.play(Write(right_eq), run_time=1.4)
    scene.play(Create(cross_mark(0.22).next_to(wrong_eq, RIGHT, buff=0.3)), Create(check_mark(0.24).next_to(right_eq, RIGHT, buff=0.3)),
               wrong.fade_to(0.25, run_time=0.8), run_time=0.8)
    scene.play(Indicate(A, color=cfg.GREEN, scale_factor=1.04), run_time=1.2)

    # --- 14. Two descriptions of one vector -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    clear(scene)
    pair = paint(eq([r"(A,\ \theta)", r"\ \Longleftrightarrow\ ", r"(A_x,\ A_y)"], cfg.FONT["hero"]), {0: cfg.VEC_A, 2: cfg.CYAN})
    scene.play(Write(pair), run_time=1.4)
    scene.wait(2.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["12"])
