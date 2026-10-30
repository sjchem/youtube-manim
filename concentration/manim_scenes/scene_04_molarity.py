"""Scene 04 — molarity: isolate the glucose (numerator), outline the whole
liquid in purple (denominator), and turn the picture into c = n / V.
"""

from manim_scenes.common import *

RIGHT_X = 3.3


class Scene04Molarity(Scene):
    def construct(self) -> None:
        play_scene(self)


def solute_sphere(point, radius: float = 0.1) -> VGroup:
    """Match the beaker's soft sphere material in the sample-cube pictures."""
    sphere = Ball(ORIGIN, 1.0, cfg.SOLUTE_DEEP, layers=28).mob
    return sphere.scale(radius).move_to(point)


def cube_icon(side: float, color: str) -> VGroup:
    """An oblique cube: a sample of solution."""
    d = side * 0.32
    front = Square(side, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.16)
    top = Polygon(front.get_corner(UL), front.get_corner(UR), front.get_corner(UR) + [d, d, 0],
                  front.get_corner(UL) + [d, d, 0], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.28)
    side_face = Polygon(front.get_corner(UR), front.get_corner(DR), front.get_corner(DR) + [d, d, 0],
                        front.get_corner(UR) + [d, d, 0], stroke_color=color, stroke_width=3, fill_color=color,
                        fill_opacity=0.08)
    return VGroup(side_face, top, front)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "04", "Molarity: moles per litre of solution")
    stage, glass, swarm = solution_stage([-3.7, -3.35, 0], zoom=1.35, solvent=500, solute=5, seed=4,
                                         style="polished", solvent_radius=0.027)
    glass.reflection_alpha = 0.0
    show(scene, stage, 1.4)

    # --- 2. Light up the glucose ---------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(set_attr(stage, swarm, "solvent_alpha", 0.15), set_attr(stage, swarm, "solute_glow", 0.45), run_time=1.6)
    counting = txt("what we count", cfg.FONT["label"], cfg.SOLUTE).move_to([RIGHT_X, 2.6, 0])
    scene.play(FadeIn(counting, shift=LEFT * 0.2), run_time=0.7)

    # --- 3. 0.100 mol: the numerator -----------------------------------------------------------------------------
    beat(scene, t, 2)
    n_chip = eq_chip(rf"n_{{\text{{glucose}}}} = {N_SOLUTE}\ \mathrm{{mol}}", cfg.AMOUNT, stroke=cfg.SOLUTE)
    n_chip.move_to([RIGHT_X, 1.6, 0])
    scene.play(FadeIn(n_chip, shift=UP * 0.2), run_time=0.9)
    numerator = txt("numerator", cfg.FONT["small"], cfg.MUTED).next_to(n_chip, DOWN, buff=0.25)
    scene.play(FadeIn(numerator), run_time=0.6)

    # --- 4. The denominator: the whole solution ----------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(set_attr(stage, swarm, "solvent_alpha", 0.8), glass.set_glow(1.0), FadeOut(numerator), run_time=1.6)
    whole = txt("the whole solution", cfg.FONT["label"], cfg.VOLUME).move_to([RIGHT_X, 0.15, 0])
    scene.play(FadeIn(whole, shift=LEFT * 0.2), run_time=0.7)
    v_chip = eq_chip(rf"V_{{\text{{solution}}}} = {fx(REF.volume_mL, 0)}\ \mathrm{{mL}}", cfg.VOLUME)
    v_chip.move_to([RIGHT_X, -1.0, 0])
    scene.play(FadeIn(v_chip, shift=UP * 0.2), run_time=0.9)

    # --- 5. ... = 0.1910 L --------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    v_litre = eq_chip(rf"V_{{\text{{solution}}}} = {V_L}\ \mathrm{{L}}", cfg.VOLUME).move_to(v_chip)
    scene.play(fade_through(v_chip, v_litre), run_time=1.0)
    scene.remove(v_chip)

    # --- 6. The definition -------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    rule = fraction("c", r"n_{\text{solute}}", r"V_{\text{solution}}", cfg.AMOUNT, cfg.VOLUME, cfg.FONT["title"])
    rule.move_to([RIGHT_X, 1.3, 0])
    scene.play(FadeOut(counting), FadeOut(whole), FadeOut(n_chip), FadeOut(v_litre), run_time=0.6)
    scene.play(Write(rule), run_time=1.6)
    names = VGroup(txt("molarity", cfg.FONT["body"], cfg.WHITE),
                   txt("(amount concentration)", cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.12)
    names.move_to([RIGHT_X, -0.6, 0])
    scene.play(FadeIn(names, shift=UP * 0.15), run_time=0.8)
    unit = eq(r"\mathrm{mol/L} = \mathrm{M}", cfg.FONT["body"], cfg.GOLD).move_to([RIGHT_X, -1.9, 0])
    scene.play(Write(unit), run_time=1.0)

    # --- 7. Put in our numbers ------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    numbers = numbers_fraction(rf"{N_SOLUTE}\ \mathrm{{mol}}", rf"{V_L}\ \mathrm{{L}}", rf"{M_TEXT}\ \mathrm{{mol/L}}",
                               cfg.AMOUNT, cfg.VOLUME, cfg.FONT["section"])
    fit_width(numbers, 7.4)
    numbers.move_to([RIGHT_X, -1.3, 0])
    scene.play(FadeOut(names), FadeOut(unit), run_time=0.5)
    scene.play(TransformFromCopy(rule[3], numbers[1]), TransformFromCopy(rule[5], numbers[3]), FadeIn(numbers[0]),
               FadeIn(numbers[2]), FadeIn(numbers[4]), run_time=1.6)
    scene.play(FadeIn(numbers[5]), run_time=0.5)

    # --- 8. 0.524 M ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(Write(numbers[6]), run_time=0.9)
    molar = eq(rf"= {M_TEXT}\ \mathrm{{M}}", cfg.FONT["title"], cfg.RESULT)
    molar_box = boxed(molar).move_to([RIGHT_X, -3.05, 0])
    scene.play(FadeIn(molar_box, scale=1.1), run_time=1.0)
    scene.play(Indicate(molar, color=cfg.WHITE, scale_factor=1.06), run_time=1.0)

    # --- 9. Scoop out one litre -------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(VGroup(rule, numbers)), run_time=0.5)
    scene.play(molar_box.animate.scale(0.8).move_to([RIGHT_X, 2.65, 0]), run_time=0.6)
    big = cube_icon(2.2, cfg.VOLUME).move_to([2.2, -0.2, 0])
    big_label = txt("1 L", cfg.FONT["body"], cfg.VOLUME).next_to(big, DOWN, buff=0.25)
    big_moles = eq(rf"{M_TEXT}\ \mathrm{{mol}}", cfg.FONT["label"], cfg.AMOUNT).next_to(big_label, DOWN, buff=0.18)
    dots = VGroup(*[solute_sphere(big[2].get_center() + np.array([x, y, 0]))
                    for x, y in ((-0.65, 0.65), (0, 0.65), (0.65, 0.65),
                                 (-0.65, 0), (0, 0), (0.65, 0),
                                 (-0.65, -0.65), (0, -0.65), (0.65, -0.65), (0.325, 0.325))])
    scene.play(DrawBorderThenFill(big), FadeIn(big_label), run_time=1.2)
    scene.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.2), FadeIn(big_moles), run_time=1.4)

    # --- 10. A hundred millilitres: a tenth -------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    small = cube_icon(2.2 * 0.1 ** (1 / 3), cfg.VOLUME).move_to([5.7, -0.55, 0])
    small_label = txt("100 mL", cfg.FONT["body"], cfg.VOLUME).move_to([5.7, big_label.get_y(), 0])
    small_moles = eq(rf"{fx(REF.molarity / 10, 4)}\ \mathrm{{mol}}", cfg.FONT["label"], cfg.AMOUNT)
    small_moles.move_to([5.7, big_moles.get_y(), 0])
    speck = solute_sphere(small[2].get_center())
    scene.play(TransformFromCopy(big, small), FadeIn(small_label), run_time=1.2)
    scene.play(FadeIn(speck, scale=0.4), FadeIn(small_moles), run_time=0.9)
    same_ratio = txt("same ratio", cfg.FONT["label"], cfg.RESULT).move_to([4.0, -3.35, 0])
    scene.play(FadeIn(same_ratio), Indicate(molar_box, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)

    # --- 11. Solution, not solvent --------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(big, big_label, big_moles, dots, small, small_label, small_moles, speck, same_ratio)),
               run_time=0.7)
    rule2 = fraction("c", r"n_{\text{solute}}", r"V_{\text{solution}}", cfg.AMOUNT, cfg.VOLUME, cfg.FONT["title"])
    rule2.move_to([RIGHT_X, 0.6, 0])
    scene.play(FadeIn(rule2), run_time=0.8)
    yes = VGroup(check_mark(0.22), txt("solution", cfg.FONT["label"], cfg.RESULT)).arrange(RIGHT, buff=0.2)
    no = VGroup(cross_mark(0.18), txt("solvent", cfg.FONT["label"], cfg.WARNING)).arrange(RIGHT, buff=0.2)
    VGroup(yes, no).arrange(RIGHT, buff=0.9).move_to([RIGHT_X, -1.25, 0])
    scene.play(Circumscribe(rule2[5], color=cfg.VOLUME, buff=0.08), FadeIn(yes), run_time=1.3)
    scene.play(FadeIn(no), run_time=0.7)

    # --- 12. The wrong denominator ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    wrong = eq([r"c", r"\neq", r"\frac{n_{\text{solute}}}{V_{\text{water}}}"], cfg.FONT["section"]).move_to([RIGHT_X, -2.55, 0])
    wrong[2].set_color(cfg.WARNING)
    scene.play(FadeOut(VGroup(yes, no)), run_time=0.5)
    scene.play(Write(wrong), set_attr(stage, swarm, "solvent_glow", 1.0), glass.set_glow(0.0), run_time=1.4)
    slash = strike(wrong[2])
    scene.play(Create(slash), run_time=0.6)
    begins = txt("where many mistakes begin", cfg.FONT["small"], cfg.WARNING).next_to(wrong, DOWN, buff=0.25)
    scene.play(FadeIn(begins), set_attr(stage, swarm, "solvent_glow", 0.0), glass.set_glow(1.0), run_time=1.0)

    # --- 13. How do chemists make one? -------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    scene.play(FadeOut(VGroup(rule2, wrong, slash, begins, molar_box)), run_time=0.8)
    flask_stage = Stage([RIGHT_X, -3.45, 0], zoom=1.05, yaw=0.3, pitch=0.25, spin=0.0, sway=0.05)
    flask = Glassware(flask_stage, pm.flask_profile(), volume=0.0, mark=True)
    flask.reflection_alpha = 0.0
    show(scene, flask_stage, 1.2)
    ask = txt("?", 120, cfg.GOLD).move_to([RIGHT_X + 2.4, 0.6, 0])
    scene.play(FadeIn(ask, scale=0.6), flask.set_attr("mark_glow", 1.0), run_time=1.0)
    scene.play(flask.set_attr("mark_glow", 0.3), Indicate(ask, color=cfg.WHITE), run_time=1.6)
    scene.play(flask.set_attr("mark_glow", 1.0), stage.zoom_to(1.3), run_time=10.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["04"])
