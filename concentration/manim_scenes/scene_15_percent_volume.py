"""Scene 15 — volume percent made the right way (30 mL ethanol, then water up
to the 100 mL mark, never "+ 70 mL"), and mass concentration gamma in g/L,
which turns into molarity on division by the molar mass.

Ethanol is drawn as gold beads among blue water dots: a picture, not a
molecule count.
"""

from manim_scenes.common import *

RX = 3.3
FLASK = pm.flask_profile(capacity=100.0)
ETHANOL_ML = 30.0


class Scene15PercentVolume(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "15", "Volume percent and grams per litre")
    vv = eq([r"\%\,(\text{v/v})", "=", r"\frac{", r"V_{\text{solute}}", "}{", r"V_{\text{solution}}", "}", r"\times 100"],
            cfg.FONT["section"])
    vv[3].set_color(cfg.ETHANOL)
    vv[5].set_color(cfg.VOLUME)
    fit_width(vv, 7.8)
    vv.move_to([RX, 2.2, 0])
    scene.play(Write(vv), run_time=1.8)

    # --- 2. 30 mL ethanol into a 100 mL flask --------------------------------------------------------------------
    beat(scene, t, 1)
    stage, flask, swarm = solution_stage([-3.9, -3.6, 0], profile=FLASK, volume=0.0, zoom=1.08, solvent=360, solute=16,
                                         seed=15, mark=True, solute_radius=0.1, spin=0.1,
                                         liquid_color=mu.mix(cfg.ETHANOL, cfg.LIQUID, 0.5))
    swarm.solvent_alpha, swarm.solute_glow = 0.0, 0.3
    show(scene, stage, 1.0)
    pour = txt(f"{ETHANOL_ML:.0f} mL ethanol", cfg.FONT["label"], cfg.ETHANOL).move_to([-1.0, 0.95, 0])
    scene.play(flask.set_volume(ETHANOL_ML), FadeIn(pour), run_time=2.2)

    # --- 3. Water up to the mark -----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    up_to = txt("water up to the mark", cfg.FONT["label"], cfg.SOLVENT).move_to([-1.0, 0.25, 0])
    scene.play(FadeIn(up_to), run_time=0.6)
    scene.play(flask.set_volume(97.0), set_attr(stage, swarm, "solvent_alpha", 1.0), run_time=3.0)
    scene.play(flask.set_volume(100.0), flask.set_attr("mark_glow", 1.0), run_time=1.8)
    not_70 = txt("not \"+ 70 mL\"", cfg.FONT["small"], cfg.WARNING).next_to(up_to, DOWN, buff=0.2)
    scene.play(FadeIn(not_70), run_time=0.6)

    # --- 4. They shrink when mixed -------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    shrink = eq([r"30 + 70", r"\neq", r"100\ \mathrm{mL}"], cfg.FONT["section"]).move_to([RX + 0.6, -0.6, 0])
    shrink[1].set_color(cfg.WARNING)
    scene.play(Write(shrink), run_time=1.2)
    why = txt("ethanol and water shrink on mixing", cfg.FONT["small"], cfg.MUTED).next_to(shrink, DOWN, buff=0.25)
    fit_width(why, 7.4)
    scene.play(FadeIn(why), run_time=0.7)

    # --- 5. 30 % (v/v), at a stated temperature ---------------------------------------------------------------------------------
    beat(scene, t, 4)
    nums = eq([r"\frac{30\ \mathrm{mL}}{100\ \mathrm{mL}}", r"\times 100", "=", r"30\%\ (\text{v/v})"], cfg.FONT["section"])
    nums[3].set_color(cfg.RESULT)
    fit_width(nums, 7.6)
    nums.move_to([RX, -0.2, 0])
    scene.play(FadeOut(VGroup(shrink, why, pour, up_to, not_70)), flask.set_glow(1.0), run_time=0.6)
    scene.play(Write(nums), run_time=1.5)
    at_t = chip("measured at 20 °C", cfg.GOLD).next_to(nums, DOWN, buff=0.45)
    scene.play(FadeIn(at_t, shift=UP * 0.15), run_time=0.7)

    # --- 6. Alcohol by volume ------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    abv = chip("ABV = alcohol by volume", cfg.ETHANOL, cfg.FONT["body"]).move_to([RX, -2.9, 0])
    scene.play(FadeIn(abv, shift=UP * 0.15), run_time=0.8)

    # --- 7. Mass concentration: grams per litre ------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    hide(scene, stage, 0.6, FadeOut(VGroup(vv, nums, at_t, abv)))
    stage2, glass, swarm2 = solution_stage([-3.9, -3.3, 0], zoom=1.25, solvent=480, solute=5, seed=16)
    show(scene, stage2, 1.0)
    gamma = fraction(r"\gamma", r"m_{\text{solute}}", r"V_{\text{solution}}", cfg.SOLUTE, cfg.VOLUME, cfg.FONT["title"])
    gamma.move_to([RX, 1.9, 0])
    scene.play(Write(gamma), glass.set_glow(1.0), set_attr(stage2, swarm2, "solute_glow", 1.2), run_time=1.6)
    gl = txt("grams per litre", cfg.FONT["label"], cfg.SOLUTE).next_to(gamma, DOWN, buff=0.3)
    scene.play(FadeIn(gl), run_time=0.6)

    # --- 8. 18.0 g / 0.1910 L = 94.2 g/L ----------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    g_nums = numbers_fraction(rf"{fx(REF.solute_g, 1)}\ \mathrm{{g}}", rf"{V_L}\ \mathrm{{L}}",
                              rf"{fx(REF.mass_concentration, 1)}\ \mathrm{{g/L}}", cfg.SOLUTE, cfg.VOLUME, cfg.FONT["section"])
    g_nums[5].become(eq(r"\approx", cfg.FONT["section"]).move_to(g_nums[5]))
    fit_width(g_nums, 7.6)
    g_nums.move_to([RX, -0.6, 0])
    scene.play(FadeOut(gl), Write(g_nums), run_time=1.8)

    # --- 9. Molarity counts, gamma weighs ----------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(FadeOut(g_nums), gamma.animate.scale(0.75).move_to([RX - 1.9, 1.9, 0]), run_time=0.8)
    c_rule = fraction("c", r"n_{\text{solute}}", r"V_{\text{solution}}", cfg.AMOUNT, cfg.VOLUME, cfg.FONT["section"])
    c_rule.scale(0.85).move_to([RX + 2.0, 1.9, 0])
    scene.play(FadeIn(c_rule), run_time=0.8)
    units = VGroup(txt("g / L", cfg.FONT["body"], cfg.SOLUTE).next_to(gamma, DOWN, buff=0.3),
                   txt("mol / L", cfg.FONT["body"], cfg.AMOUNT).next_to(c_rule, DOWN, buff=0.3))
    scene.play(FadeIn(units), run_time=0.7)
    bridge = glow_arrow(units[0].get_right() + RIGHT * 0.2, units[1].get_left() + LEFT * 0.2, cfg.WHITE)
    by_m = eq(r"\div M", cfg.FONT["label"], cfg.WHITE).next_to(bridge, DOWN, buff=0.15)
    scene.play(GrowArrow(bridge[1]), FadeIn(bridge[0]), FadeIn(by_m), run_time=1.0)

    # --- 10. gamma / M = c = 0.524 M --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    back = eq([r"\frac{\gamma}{M_{\text{glucose}}}", "=", "c", r"\approx", rf"{M_TEXT}\ \mathrm{{M}}"], cfg.FONT["section"])
    back[0].set_color(cfg.SOLUTE)
    back[4].set_color(cfg.RESULT)
    fit_width(back, 7.6)
    back_box = boxed(back).move_to([RX, -1.6, 0])
    scene.play(FadeIn(back_box, scale=1.06), run_time=1.2)
    scene.play(Indicate(back[4], color=cfg.WHITE, scale_factor=1.12), run_time=1.2)
    scene.play(Circumscribe(back_box, color=cfg.GOLD, buff=0.1), glass.set_glow(0.5), run_time=8.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["15"])
