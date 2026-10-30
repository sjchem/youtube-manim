"""Scene 14 — "percent" needs its little letters: mass percent (w/w) on a
balance, 9.09 %, and mass-per-volume percent (w/v) in the purple-outlined
glass, 9.42 %, for the same solution. A 5 % glucose drip is w/v.
"""

from manim_scenes.common import *
from manim_scenes.scene_02_counting_moles import heap, mini_beaker

RX = 3.3


class Scene14PercentMass(Scene):
    def construct(self) -> None:
        play_scene(self)


def bottle(label: str, color: str = cfg.WHITE) -> VGroup:
    body = RoundedRectangle(width=2.3, height=3.0, corner_radius=0.35, stroke_color=cfg.GLASS, stroke_width=3,
                            fill_color=cfg.LIQUID, fill_opacity=0.3)
    neck = Rectangle(width=0.8, height=0.6, stroke_color=cfg.GLASS, stroke_width=3, fill_opacity=0).next_to(body, UP, buff=0)
    cap = RoundedRectangle(width=1.0, height=0.4, corner_radius=0.08, stroke_width=0, fill_color=cfg.GRAY,
                           fill_opacity=1).next_to(neck, UP, buff=0)
    tag = RoundedRectangle(width=1.9, height=1.0, corner_radius=0.1, stroke_color=cfg.MUTED, stroke_width=2,
                           fill_color="#EDF3F8", fill_opacity=1).move_to(body)
    text = txt(label, cfg.FONT["section"], cfg.BG).move_to(tag)
    text.set_stroke(width=0)
    glints = VGroup(*[RoundedRectangle(width=w,height=2.5,corner_radius=w/2,stroke_width=0,
                                       fill_color=cfg.WHITE,fill_opacity=a).move_to(body.get_center()+RIGHT*x)
                        for x,w,a in ((-.88,.13,.16),(.90,.04,.22))])
    ribs = VGroup(*[Line(cap.get_left()+RIGHT*(.12+k*.11)+DOWN*.12,
                        cap.get_left()+RIGHT*(.12+k*.11)+UP*.12,
                        stroke_color=cfg.GLASS,stroke_width=1.3,stroke_opacity=.55) for k in range(8)])
    group = VGroup(body, neck, cap, glints, ribs, tag, text)
    group.text = text
    return group


def drip_bag() -> VGroup:
    bag = RoundedRectangle(width=1.9, height=2.6, corner_radius=0.5, stroke_color=cfg.GLASS, stroke_width=3,
                           fill_color=cfg.LIQUID, fill_opacity=0.35)
    hook = Circle(radius=0.16, stroke_color=cfg.GLASS, stroke_width=3).next_to(bag, UP, buff=0)
    tube = Line(bag.get_bottom(), bag.get_bottom() + DOWN * 1.0, stroke_color=cfg.GLASS, stroke_width=3)
    chamber = RoundedRectangle(width=0.32, height=0.5, corner_radius=0.1, stroke_color=cfg.GLASS, stroke_width=3,
                               fill_opacity=0).move_to(tube.get_end())
    label = txt("5%", cfg.FONT["body"], cfg.BG).move_to(bag)
    label.set_stroke(width=0)
    tag = RoundedRectangle(width=1.3, height=0.7, corner_radius=0.1, stroke_width=0, fill_color="#EDF3F8",
                           fill_opacity=1).move_to(bag)
    return VGroup(bag, hook, tube, chamber, tag, label)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "14", "Three ways to say percent")
    b = bottle("10%").move_to([-4.3, -0.6, 0])
    scene.play(FadeIn(b, shift=UP * 0.2), run_time=1.0)
    huh = txt("?", 120, cfg.GOLD).next_to(b, RIGHT, buff=0.5)
    scene.play(FadeIn(huh, scale=0.6), run_time=0.7)

    # --- 2. Parts of what, per hundred of what? ---------------------------------------------------------------
    beat(scene, t, 1)
    of_what = VGroup(txt("parts per hundred", cfg.FONT["body"], cfg.WHITE),
                     txt("…of what?", cfg.FONT["body"], cfg.GOLD)).arrange(DOWN, buff=0.25).move_to([RX, 0.4, 0])
    scene.play(FadeIn(of_what[0]), run_time=0.8)
    scene.play(FadeIn(of_what[1], shift=UP * 0.15), run_time=0.8)

    # --- 3. Mass percent ------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    ww = eq([r"\%\,(\text{w/w})", "=", r"\frac{", r"m_{\text{solute}}", "}{", r"m_{\text{solution}}", "}", r"\times 100"],
            cfg.FONT["section"])
    ww[3].set_color(cfg.SOLUTE)
    ww[5].set_color(cfg.SOLUTION_MASS)
    fit_width(ww, 7.6)
    ww.move_to([RX, 2.2, 0])
    scene.play(FadeOut(of_what), Write(ww), run_time=1.6)
    name = txt("mass percent", cfg.FONT["label"], cfg.SOLUTION_MASS).next_to(ww, DOWN, buff=0.3)
    scene.play(FadeIn(name), run_time=0.6)

    # --- 4. Glucose and water on the balance ----------------------------------------------------------------------------
    beat(scene, t, 3)
    balance = Balance([-4.0, -2.3, 0], color=cfg.SOLUTION_MASS)
    scene.play(FadeOut(VGroup(b, huh)), FadeIn(balance, shift=UP * 0.2), run_time=0.8)
    sugar = heap(cfg.SOLUTE_DEEP).next_to(balance.pan_top(), UP, buff=0).shift(LEFT * 0.75)
    cup = mini_beaker().next_to(balance.pan_top(), UP, buff=0).shift(RIGHT * 0.6)
    scene.play(FadeIn(sugar, shift=DOWN * 0.4), balance.weigh(REF.solute_g), run_time=1.2)
    scene.play(FadeIn(cup, shift=DOWN * 0.4), balance.weigh(REF.solution_g), run_time=1.6)

    # --- 5. 18.0 / 198.0 x 100 = 9.09 % -----------------------------------------------------------------------------------
    beat(scene, t, 4)
    nums = eq([r"\frac{", rf"{fx(REF.solute_g, 1)}\ \mathrm{{g}}", "}{", rf"{fx(REF.solution_g, 1)}\ \mathrm{{g}}", "}",
               r"\times 100", "=", rf"{W_TEXT}\%"], cfg.FONT["section"])
    nums[1].set_color(cfg.SOLUTE)
    nums[3].set_color(cfg.SOLUTION_MASS)
    nums[7].set_color(cfg.RESULT)
    fit_width(nums, 7.6)
    nums.move_to([RX, -0.3, 0])
    scene.play(FadeOut(name), Write(nums[:6]), run_time=1.6)
    scene.play(Write(nums[6:]), run_time=0.9)

    # --- 6. The last number from the opening; the whole solution's mass ---------------------------------------------------------
    beat(scene, t, 5)
    result = boxed(eq(rf"{W_TEXT}\%\ (\text{{w/w}})", cfg.FONT["section"], cfg.RESULT)).move_to([RX, -2.3, 0])
    scene.play(FadeIn(result, scale=1.08), run_time=0.9)
    whole = txt("glucose included", cfg.FONT["small"], cfg.SOLUTION_MASS).next_to(nums[3], DOWN, buff=0.15)
    scene.play(Indicate(nums[3], color=cfg.WHITE, scale_factor=1.1), FadeIn(whole), run_time=1.1)

    # --- 7. Mass over volume ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(VGroup(ww, nums, result, whole, balance, sugar, cup)), run_time=0.8)
    stage, glass, swarm = solution_stage([-4.0, -3.3, 0], zoom=1.25, solvent=480, solute=5, seed=14)
    show(scene, stage, 1.0)
    wv = eq([r"\%\,(\text{w/v})", "=", r"\frac{", r"m_{\text{solute}}\,(\mathrm{g})", "}{", r"V_{\text{solution}}\,(\mathrm{mL})", "}",
             r"\times 100"], cfg.FONT["section"])
    wv[3].set_color(cfg.SOLUTE)
    wv[5].set_color(cfg.VOLUME)
    fit_width(wv, 7.8)
    wv.move_to([RX, 2.2, 0])
    scene.play(Write(wv), glass.set_glow(1.0), run_time=1.6)

    # --- 8. Grams per 100 mL of final solution ------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    per = txt("grams per 100 mL of final solution", cfg.FONT["small"], cfg.VOLUME).next_to(wv, DOWN, buff=0.3)
    fit_width(per, 7.6)
    scene.play(FadeIn(per), run_time=0.8)

    # --- 9. 18.0 / 191.0 x 100 = 9.42 % --------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    nums2 = eq([r"\frac{", rf"{fx(REF.solute_g, 1)}\ \mathrm{{g}}", "}{", rf"{V_ML}\ \mathrm{{mL}}", "}", r"\times 100", "=",
                rf"{WV_TEXT}\%"], cfg.FONT["section"])
    nums2[1].set_color(cfg.SOLUTE)
    nums2[3].set_color(cfg.VOLUME)
    nums2[7].set_color(cfg.RESULT)
    fit_width(nums2, 7.6)
    nums2.move_to([RX, -0.3, 0])
    scene.play(Write(nums2[:6]), run_time=1.5)
    scene.play(Write(nums2[6:]), run_time=0.9)
    result2 = boxed(eq(rf"{WV_TEXT}\%\ (\text{{w/v}})", cfg.FONT["section"], cfg.RESULT)).move_to([RX, -2.3, 0])
    scene.play(FadeIn(result2, scale=1.08), run_time=0.9)

    # --- 10. Both percent, not the same comparison ------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    hide(scene, stage, 0.6, FadeOut(VGroup(wv, per, nums2)))
    pair = VGroup(boxed(eq(rf"{W_TEXT}\%\ (\text{{w/w}})", cfg.FONT["title"], cfg.SOLUTION_MASS), cfg.SOLUTION_MASS),
                  eq(r"\neq", cfg.FONT["title"], cfg.WARNING),
                  boxed(eq(rf"{WV_TEXT}\%\ (\text{{w/v}})", cfg.FONT["title"], cfg.VOLUME), cfg.VOLUME)).arrange(RIGHT, buff=0.6)
    fit_width(pair, 13.6)
    pair.move_to([0, 0.4, 0])
    scene.play(ReplacementTransform(result2, pair[2]), FadeIn(pair[0]), run_time=1.2)
    scene.play(FadeIn(pair[1], scale=1.3), run_time=0.6)
    same = caption("Same solution. Different comparisons.", cfg.GOLD)
    scene.play(FadeIn(same, shift=UP * 0.15), run_time=0.8)

    # --- 11. A 5 % glucose drip is w/v ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    bag = drip_bag().move_to([-4.2, -0.2, 0])
    scene.play(FadeOut(VGroup(pair, same)), run_time=0.5)
    scene.play(FadeIn(bag, shift=DOWN * 0.2), run_time=0.6)
    drip = VGroup(eq(r"5\%\ (\text{w/v})", cfg.FONT["section"], cfg.WHITE),
                  eq(r"= 5\ \mathrm{g}\ \text{glucose per}\ 100\ \mathrm{mL}", cfg.FONT["body"], cfg.SOLUTE))
    drip.arrange(DOWN, buff=0.35).move_to([RX - 0.3, 0.0, 0])
    fit_width(drip, 8.2)
    scene.play(Write(drip[0]), run_time=1.0)
    scene.play(FadeIn(drip[1], shift=UP * 0.15), run_time=1.0)

    # --- 12. Look for the little letters -----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    letters = VGroup(*[chip(s, c, cfg.FONT["title"]) for s, c in (("% (w/w)", cfg.SOLUTION_MASS), ("% (w/v)", cfg.VOLUME),
                                                                 ("% (v/v)", cfg.ETHANOL))]).arrange(RIGHT, buff=0.5)
    letters.move_to([0, 0.3, 0])
    scene.play(FadeOut(VGroup(bag, drip)), run_time=0.5)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in letters], lag_ratio=0.3), run_time=1.3)
    scene.play(LaggedStart(*[Indicate(c.label, color=cfg.WHITE, scale_factor=1.12) for c in letters], lag_ratio=0.4),
               run_time=3.5)
    scene.play(Circumscribe(letters, color=cfg.GOLD, buff=0.2), run_time=3.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["14"])
