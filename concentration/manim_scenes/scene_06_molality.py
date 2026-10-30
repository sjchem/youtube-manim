"""Scene 06 — molality: switch the purple volume glow off, light only the
solvent, weigh it, and watch the denominator of the fraction swap while the
numerator stays put.
"""

from manim_scenes.common import *

RX = 3.3


class Scene06Molality(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "06", "Molality: moles per kilogram of solvent")
    stage, glass, swarm = solution_stage([-3.9, -3.35, 0], zoom=1.3, solvent=500, solute=5, seed=7,
                                         style="polished", solvent_radius=0.027)
    glass.reflection_alpha = 0.0
    show(scene, stage, 1.4)
    ignore = txt("a measure that ignores volume?", cfg.FONT["label"], cfg.CYAN).move_to([RX, 0.3, 0])
    fit_width(ignore, 7.4)
    scene.play(FadeIn(ignore, shift=LEFT * 0.2), run_time=0.8)

    # --- 2. Molarity's denominator: the whole volume ----------------------------------------------------------
    beat(scene, t, 1)
    c_rule = fraction("c", r"n_{\text{solute}}", r"V_{\text{solution}}", cfg.AMOUNT, cfg.VOLUME, cfg.FONT["section"])
    c_rule.move_to([RX, 1.9, 0])
    scene.play(FadeOut(ignore), glass.set_glow(1.0), Write(c_rule), run_time=1.6)

    # --- 3. Switch it off; light the solvent -------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(glass.set_glow(0.0), set_attr(stage, swarm, "solute_glow", 0.45), run_time=1.0)
    scene.play(set_attr(stage, swarm, "solvent_glow", 1.0), run_time=1.2)
    just = txt("just the solvent", cfg.FONT["label"], cfg.SOLVENT_MASS).move_to([RX, 0.25, 0])
    scene.play(FadeIn(just, shift=LEFT * 0.2), run_time=0.7)

    # --- 4. Weigh it -----------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    balance = Balance([RX, -2.3, 0], color=cfg.SOLVENT_MASS)
    # These small spheres need only the coloured shading contours; omit the
    # separate reflection layers to keep their staggered animation light.
    water = VGroup(*[VGroup(*Ball(ORIGIN, 1.0, cfg.SOLVENT, layers=12).parts[:13]).scale(0.1)
                     for _ in range(30)])
    for k, b in enumerate(water):
        b.move_to([(k % 10 - 4.5) * 0.24, (k // 10) * 0.2, 0])
    water.next_to(balance.pan_top(), UP, buff=0.02)
    scene.play(FadeOut(just), FadeIn(balance, shift=UP * 0.2), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in water], lag_ratio=0.02), balance.weigh(REF.solvent_g),
               run_time=1.8)
    kg = eq_chip(rf"m_{{\text{{solvent}}}} = {KG}\ \mathrm{{kg}}", cfg.SOLVENT_MASS).move_to([RX, 0.1, 0])
    scene.play(FadeIn(kg, shift=UP * 0.2), run_time=0.9)

    # --- 5. The definition ----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    m_rule = fraction("m", r"n_{\text{solute}}", r"m_{\text{solvent}}", cfg.AMOUNT, cfg.SOLVENT_MASS, cfg.FONT["section"])
    m_rule.move_to([RX, -0.35, 0])
    scene.play(FadeOut(VGroup(balance, water, kg)), run_time=0.6)
    scene.play(Write(m_rule), run_time=1.4)
    unit = VGroup(txt("molality", cfg.FONT["body"], cfg.WHITE),
                  eq(r"\mathrm{mol/kg}\ \ (\text{small } m)", cfg.FONT["label"], cfg.SOLVENT_MASS)).arrange(DOWN, buff=0.15)
    unit.move_to([RX, -2.5, 0])
    scene.play(FadeIn(unit, shift=UP * 0.15), run_time=0.8)

    # --- 6-7. Watch the formula change: only the denominator swaps --------------------------------------------------------
    beat(scene, t, 5)
    before = eq([r"c", "=", r"\frac{", rf"{N_SOLUTE}\ \mathrm{{mol}}", "}{", rf"{V_L}\ \mathrm{{L}}", "}"],
                cfg.FONT["title"]).move_to([RX, 0.6, 0])
    before[3].set_color(cfg.AMOUNT)
    before[5].set_color(cfg.VOLUME)
    tag_before = txt("solution volume", cfg.FONT["small"], cfg.VOLUME).next_to(before[5], DOWN, buff=0.3)
    scene.play(FadeOut(VGroup(c_rule, m_rule, unit)), run_time=0.6)
    scene.play(FadeIn(before), FadeIn(tag_before), glass.set_glow(1.0), set_attr(stage, swarm, "solvent_glow", 0.0),
               run_time=1.2)
    keep = glow_frame(before[3], cfg.AMOUNT, buff=0.1)
    scene.play(Create(keep), run_time=0.8)
    stays = txt("stays", cfg.FONT["small"], cfg.AMOUNT).next_to(keep, UP, buff=0.15)
    scene.play(FadeIn(stays), run_time=0.5)

    beat(scene, t, 6)
    after = eq([r"m", "=", r"\frac{", rf"{N_SOLUTE}\ \mathrm{{mol}}", "}{", rf"{KG}\ \mathrm{{kg}}", "}"],
               cfg.FONT["title"]).move_to(before)
    after[3].set_color(cfg.AMOUNT)
    after[5].set_color(cfg.SOLVENT_MASS)
    after.shift(before[1].get_center() - after[1].get_center())
    tag_after = txt("solvent mass", cfg.FONT["small"], cfg.SOLVENT_MASS).next_to(after[5], DOWN, buff=0.3)
    scene.play(ReplacementTransform(before[5], after[5]), ReplacementTransform(before[0], after[0]),
               fade_through(tag_before, tag_after), glass.set_glow(0.0), set_attr(stage, swarm, "solvent_glow", 1.0),
               run_time=1.8)
    scene.remove(tag_before)
    scene.play(Indicate(after[5], color=cfg.WHITE, scale_factor=1.1), run_time=0.9)

    # --- 8. = 0.556 mol/kg -------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    whole = VGroup(before[1:5], before[6], after[0], after[5])
    full = eq([r"m", "=", r"\frac{", rf"{N_SOLUTE}\ \mathrm{{mol}}", "}{", rf"{KG}\ \mathrm{{kg}}", "}", "=",
               rf"{m_TEXT}\ \mathrm{{mol/kg}}"], cfg.FONT["section"])
    full[3].set_color(cfg.AMOUNT)
    full[5].set_color(cfg.SOLVENT_MASS)
    full[8].set_color(cfg.RESULT)
    fit_width(full, 8.6)
    full.move_to([RX, 0.6, 0])
    scene.play(FadeOut(VGroup(keep, stays, tag_after)), FadeOut(whole), FadeIn(full[:7]), run_time=0.8)
    tail = full[7:]
    scene.play(Write(tail), run_time=1.2)

    # --- 9. The second number: 0.556 m ---------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    molal = boxed(eq(rf"{m_TEXT}\ \mathrm{{m}}", cfg.FONT["title"], cfg.RESULT)).move_to([RX, -2.3, 0])
    scene.play(FadeIn(molal, scale=1.1), run_time=1.0)
    scene.play(Indicate(molal, color=cfg.WHITE, scale_factor=1.05), run_time=1.0)

    # --- 10. Same glucose, two references -------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(VGroup(full, molal)), run_time=0.7)
    pair = VGroup(
        eq([r"c", "=", r"\frac{n_{\text{solute}}}{V_{\text{solution}}}", "=", rf"{M_TEXT}\ \mathrm{{M}}"], cfg.FONT["body"]),
        eq([r"m", "=", r"\frac{n_{\text{solute}}}{m_{\text{solvent}}}", "=", rf"{m_TEXT}\ \mathrm{{m}}"], cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.7).move_to([RX, 0.4, 0])
    pair[0][2].set_color(cfg.VOLUME)
    pair[1][2].set_color(cfg.SOLVENT_MASS)
    scene.play(FadeIn(pair[0]), glass.set_glow(1.0), set_attr(stage, swarm, "solvent_glow", 0.0), run_time=1.2)
    narration_wait(scene, 1.5)
    scene.play(FadeIn(pair[1]), glass.set_glow(0.0), set_attr(stage, swarm, "solvent_glow", 1.0), run_time=1.2)

    # --- 11. The difference is the reference -------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    reference = txt("Same glucose. A different reference.", cfg.FONT["label"], cfg.GOLD).move_to([RX, -2.4, 0])
    fit_width(reference, 8.4)
    scene.play(FadeIn(reference, shift=UP * 0.15), run_time=0.8)
    scene.play(Indicate(pair[0][2], color=cfg.VOLUME), Indicate(pair[1][2], color=cfg.SOLVENT_MASS), run_time=1.4)

    # --- 12. Mass keeps its promise ------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    scene.play(FadeOut(pair), FadeOut(reference), run_time=0.6)
    balance = Balance([RX + 0.9, -1.4, 0], color=cfg.SOLVENT_MASS, grams=REF.solvent_g)
    thermo = Thermometer([0.3, -0.7, 0], low=0, high=100, height=3.6)
    scene.play(FadeIn(balance), FadeIn(thermo), run_time=0.8)
    stamp = txt("mass: unchanged", cfg.FONT["body"], cfg.RESULT).move_to([RX + 0.9, 1.3, 0])
    scene.play(thermo.celsius.to(thermo, 80.0), set_attr(stage, swarm, "speed", 2.4), run_time=1.8)
    scene.play(thermo.celsius.to(thermo, 5.0), set_attr(stage, swarm, "speed", 0.5), FadeIn(stamp), run_time=2.2)
    scene.play(thermo.celsius.to(thermo, 20.0), set_attr(stage, swarm, "speed", 1.0), run_time=1.2)

    # --- 13. Volume doesn't make that promise ---------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    scene.play(FadeOut(VGroup(balance, stamp)), set_attr(stage, swarm, "solvent_glow", 0.0), glass.set_glow(1.0),
               run_time=0.8)
    volume_q = txt("volume?", cfg.FONT["title"], cfg.VOLUME).move_to([RX + 0.6, 0.2, 0])
    scene.play(FadeIn(volume_q, scale=0.8), run_time=0.8)
    scene.play(thermo.celsius.to(thermo, 70.0), glass.set_volume(cd.heated_volume_mL()), set_attr(stage, swarm, "speed", 2.2),
               run_time=4.0)
    scene.play(Indicate(volume_q, color=cfg.WHITE), run_time=1.4)
    scene.play(thermo.celsius.to(thermo, 20.0), glass.set_volume(REF.volume_mL), set_attr(stage, swarm, "speed", 1.0),
               run_time=2.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["06"])
