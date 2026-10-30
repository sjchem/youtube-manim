"""Scene 02 — what is in the glass: masses add on a balance, and moles count
molecules. Glucose and water turn as computed 3D models
(``physics_models.glucose`` is an ideal beta-D-glucopyranose chair).
"""

from manim_scenes.common import *


class Scene02CountingMoles(Scene):
    def construct(self) -> None:
        play_scene(self)


def heap(color: str, rows: int = 4, radius: float = 0.13) -> VGroup:
    """A small pile of crystals, drawn as shaded beads."""
    group = VGroup()
    for row in range(rows):
        count = rows - row
        for k in range(count):
            group.add(bead([(k - (count - 1) / 2) * radius * 2.0, row * radius * 1.7, 0], color, radius))
    return group


def mini_beaker(color: str = cfg.LIQUID, width: float = 1.1, height: float = 1.2) -> VGroup:
    glass = Polygon([-width / 2, height / 2, 0], [-width * 0.42, -height / 2, 0], [width * 0.42, -height / 2, 0],
                    [width / 2, height / 2, 0], stroke_color=cfg.GLASS, stroke_width=3, fill_opacity=0)
    liquid = Polygon([-width * 0.47, height * 0.2, 0], [-width * 0.42, -height / 2, 0], [width * 0.42, -height / 2, 0],
                     [width * 0.47, height * 0.2, 0], stroke_width=0, fill_color=color, fill_opacity=0.6)
    return VGroup(liquid, glass)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "02", "What's in the glass?")

    # --- 1. Two kinds of molecule ------------------------------------------------------------------------------
    left = Stage([-5.0, 1.0, 0], zoom=0.72, yaw=0.4, pitch=0.45, spin=0.32, sway=0.1)
    molecule_model(left, pm.glucose(), scale=0.8)
    right = Stage([5.0, 1.0, 0], zoom=1.6, yaw=0.3, pitch=0.2, spin=0.4, sway=0.1)
    molecule_model(right, pm.water(), scale=0.9)
    show(scene, left, 1.2)
    names = VGroup(VGroup(txt("glucose", cfg.FONT["label"], cfg.SOLUTE), eq(r"\mathrm{C_6H_{12}O_6}", cfg.FONT["small"], cfg.SOLUTE)),
                   VGroup(txt("water", cfg.FONT["label"], cfg.SOLVENT), eq(r"\mathrm{H_2O}", cfg.FONT["small"], cfg.SOLVENT)))
    for name, x in zip(names, (-5.0, 5.0)):
        name.arrange(DOWN, buff=0.12).move_to([x, -1.25, 0])
    scene.play(FadeIn(names[0]), run_time=0.6)
    show(scene, right, 1.0, FadeIn(names[1]))

    # --- 2. Masses add on a balance ------------------------------------------------------------------------------
    beat(scene, t, 1)
    balance = Balance([0, -2.5, 0], color=cfg.SOLUTION_MASS)
    scene.play(FadeIn(balance, shift=UP * 0.2), run_time=0.8)
    sugar = heap(cfg.SOLUTE_DEEP).move_to(balance.pan_top() + UP * 1.6)
    scene.play(FadeIn(sugar, shift=DOWN * 0.3), run_time=0.6)
    scene.play(sugar.animate.next_to(balance.pan_top(), UP, buff=0.0).shift(LEFT * 0.75), balance.weigh(REF.solute_g),
               run_time=1.4)
    cup = mini_beaker().move_to(balance.pan_top() + UP * 1.7 + RIGHT * 0.55)
    scene.play(FadeIn(cup, shift=DOWN * 0.3), run_time=0.6)
    scene.play(cup.animate.next_to(balance.pan_top(), UP, buff=0.0).shift(RIGHT * 0.55), balance.weigh(REF.solution_g),
               run_time=1.6)
    adds = eq([rf"{fx(REF.solute_g, 1)}\ \mathrm{{g}}", "+", rf"{fx(REF.solvent_g, 1)}\ \mathrm{{g}}", "=",
               rf"{fx(REF.solution_g, 1)}\ \mathrm{{g}}"], cfg.FONT["body"]).move_to([0, 1.55, 0])
    adds[0].set_color(cfg.SOLUTE)
    adds[2].set_color(cfg.SOLVENT)
    adds[4].set_color(cfg.SOLUTION_MASS)
    scene.play(Write(adds), run_time=1.6)
    tick = check_mark(0.24).next_to(adds, DOWN, buff=0.3)
    mass_adds = txt("mass simply adds", cfg.FONT["small"], cfg.RESULT).next_to(tick, RIGHT, buff=0.2)
    scene.play(Create(tick), FadeIn(mass_adds), run_time=0.8)

    # --- 3. Chemistry counts molecules, in moles ------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(FadeOut(VGroup(balance, sugar, cup, tick, mass_adds)), adds.animate.scale(0.75).move_to([0, 2.75, 0]),
               run_time=1.0)
    bundle = VGroup(*[bead([0.0, 0.0, 0.0], cfg.SOLVENT, 0.09) for _ in range(36)])
    for k, b in enumerate(bundle):
        b.move_to([(k % 6 - 2.5) * 0.24, (k // 6 - 2.5) * 0.24, 0])
    bundle.move_to([0, -0.55, 0])
    wrap = glow_frame(bundle, cfg.AMOUNT, buff=0.18)
    mole = txt("1 mole = a fixed bundle of molecules", cfg.FONT["small"], cfg.AMOUNT).next_to(wrap, DOWN, buff=0.3)
    scene.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in bundle], lag_ratio=0.03), run_time=1.6)
    scene.play(Create(wrap), FadeIn(mole), run_time=1.0)

    # --- 4. n = mass / molar mass -----------------------------------------------------------------------------------------
    beat(scene, t, 3)
    rule = eq([r"n", "=", r"\frac{\text{mass}}{\text{molar mass}}"], cfg.FONT["section"]).move_to([0, 0.35, 0])
    rule[0].set_color(cfg.AMOUNT)
    scene.play(FadeOut(VGroup(bundle, wrap, mole)), FadeOut(adds), run_time=0.7)
    scene.play(Write(rule), run_time=1.5)
    scene.play(rule.animate.move_to([0, 2.45, 0]).scale(0.85), run_time=0.9)

    # --- 5. Glucose: 0.100 mol ------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    glucose_n = numbers_fraction(rf"{fx(REF.solute_g, 1)}\ \mathrm{{g}}", rf"{fx(pm.M_GLUCOSE, 0)}\ \mathrm{{g/mol}}",
                                 rf"{N_SOLUTE}\ \mathrm{{mol}}", cfg.SOLUTE, cfg.MUTED, cfg.FONT["body"],
                                 result_color=cfg.AMOUNT).move_to([-3.9, -2.75, 0])
    scene.play(Indicate(names[0], color=cfg.WHITE, scale_factor=1.08), run_time=0.9)
    scene.play(Write(glucose_n[:5]), run_time=1.3)
    scene.play(Write(glucose_n[5:]), run_time=0.9)

    # --- 6. Water: 10.0 mol ---------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    water_n = numbers_fraction(rf"{fx(REF.solvent_g, 1)}\ \mathrm{{g}}", rf"{fx(pm.M_WATER, 0)}\ \mathrm{{g/mol}}",
                               rf"{N_SOLVENT}\ \mathrm{{mol}}", cfg.SOLVENT, cfg.MUTED, cfg.FONT["body"],
                               result_color=cfg.AMOUNT).move_to([3.9, -2.75, 0])
    scene.play(Indicate(names[1], color=cfg.WHITE, scale_factor=1.08), run_time=0.9)
    scene.play(Write(water_n[:5]), run_time=1.3)
    scene.play(Write(water_n[5:]), run_time=0.9)

    # --- 7. Ten times the mass, a hundred times the molecules ------------------------------------------------------------------
    beat(scene, t, 6)
    hide(scene, left, 0.6, FadeOut(names), FadeOut(rule), FadeOut(glucose_n), FadeOut(water_n))
    hide(scene, right, 0.4)
    mass_label = txt("mass", cfg.FONT["label"], cfg.MUTED).move_to([-5.9, 1.7, 0])
    gold_bar = Rectangle(width=0.55, height=0.55, stroke_width=0, fill_color=cfg.SOLUTE, fill_opacity=0.9)
    blue_bar = Rectangle(width=5.5, height=0.55, stroke_width=0, fill_color=cfg.SOLVENT, fill_opacity=0.9)
    gold_bar.move_to([-4.5, 2.1, 0], aligned_edge=LEFT)
    blue_bar.move_to([-4.5, 1.3, 0], aligned_edge=LEFT)
    times10 = txt("× 10", cfg.FONT["section"], cfg.WHITE).next_to(blue_bar, RIGHT, buff=0.4)
    scene.play(FadeIn(mass_label), GrowFromEdge(gold_bar, LEFT), GrowFromEdge(blue_bar, LEFT), run_time=1.2)
    scene.play(FadeIn(times10), run_time=0.5)
    count_label = txt("molecules", cfg.FONT["label"], cfg.MUTED).move_to([-5.6, -1.3, 0])
    one = bead([-3.9, -1.3, 0], cfg.SOLUTE_DEEP, 0.16, glow=1.0)
    crowd = VGroup(*[bead([-2.2 + (k % 20) * 0.24, -0.5 - (k // 20) * 0.32, 0], cfg.SOLVENT, 0.09) for k in range(100)])
    times100 = txt("× 100", cfg.FONT["section"], cfg.WHITE).next_to(crowd, RIGHT, buff=0.4)
    scene.play(FadeIn(count_label), FadeIn(one, scale=0.5), LaggedStart(*[FadeIn(b, scale=0.5) for b in crowd], lag_ratio=0.01),
               run_time=1.6)
    scene.play(FadeIn(times100, scale=1.2), run_time=0.6)

    # --- 8. Keep both counters ----------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    counters = VGroup(eq_chip(rf"n_{{\text{{glucose}}}} = {N_SOLUTE}\ \mathrm{{mol}}", cfg.AMOUNT, stroke=cfg.SOLUTE),
                      eq_chip(rf"n_{{\text{{water}}}} = {N_SOLVENT}\ \mathrm{{mol}}", cfg.AMOUNT, stroke=cfg.SOLVENT))
    counters.arrange(RIGHT, buff=0.8).move_to([0, -3.3, 0])
    scene.play(FadeIn(counters, shift=UP * 0.2), run_time=1.0)
    scene.play(Indicate(counters, color=cfg.WHITE, scale_factor=1.04), run_time=1.8)
    scene.play(Circumscribe(counters, color=cfg.AMOUNT, buff=0.12), run_time=3.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["02"])
