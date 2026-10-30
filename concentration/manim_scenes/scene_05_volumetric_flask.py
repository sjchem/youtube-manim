"""Scene 05 — making 1.000 L of 0.500 M glucose: the tempting way (1 L of
water, which overshoots the litre) beside the right way (a volumetric flask
filled to the mark), then the catch: the mark is calibrated at 20 °C.

Liquid heights follow the real flask shape (``physics_models.Profile``);
the overshoot uses the reference solution's apparent molar volume, and the
warm flask expands like water from 20 to 40 °C (``concentration_data``).
"""

from manim_scenes.common import *

TARGET_M = 0.500
MASS_G = TARGET_M * pm.M_GLUCOSE
BEAKER = pm.Profile((0.0, 4.0), (1.3, 1.3), 3.1, 1000.0)
FLASK = pm.flask_profile()


class Scene05VolumetricFlask(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "05", "Making a solution: fill to the mark")

    # --- 1. The goal --------------------------------------------------------------------------------------
    goal = eq_chip(rf"{fx(1.0, 3)}\ \mathrm{{L}}\ \text{{of}}\ {fx(TARGET_M, 3)}\ \mathrm{{M}}\ \text{{glucose}}", cfg.GOLD)
    goal.move_to([0, 2.55, 0])
    scene.play(FadeIn(goal, shift=DOWN * 0.2), run_time=1.0)

    # --- 2. 0.500 mol = 90.0 g ---------------------------------------------------------------------------------
    beat(scene, t, 1)
    moles = eq([r"n", "=", rf"{fx(TARGET_M, 3)}\ \mathrm{{mol/L}} \times {fx(1.0, 3)}\ \mathrm{{L}}", "=",
                rf"{fx(TARGET_M, 3)}\ \mathrm{{mol}}"], cfg.FONT["body"]).move_to([0, 1.1, 0])
    moles[0].set_color(cfg.AMOUNT)
    moles[4].set_color(cfg.AMOUNT)
    mass = eq([r"m", "=", rf"{fx(TARGET_M, 3)}\ \mathrm{{mol}} \times {fx(pm.M_GLUCOSE, 0)}\ \mathrm{{g/mol}}", "=",
               rf"{fx(MASS_G, 1)}\ \mathrm{{g}}"], cfg.FONT["body"]).move_to([0, -0.2, 0])
    mass[0].set_color(cfg.SOLUTE)
    mass[4].set_color(cfg.SOLUTE)
    for row in (moles, mass):
        fit_width(row, 13.0)
    scene.play(Write(moles), run_time=1.6)
    scene.play(Write(mass), run_time=1.6)
    scene.play(Indicate(mass[4], color=cfg.WHITE, scale_factor=1.15), run_time=0.9)

    # --- 3. The tempting way: into one litre of water -------------------------------------------------------------
    beat(scene, t, 2)
    need = chip(f"{fx(MASS_G, 1)} g glucose", cfg.SOLUTE).move_to([-0.2, 2.55, 0])
    scene.play(FadeOut(moles), FadeOut(mass), fade_through(goal, need), run_time=0.8)
    scene.remove(goal)
    left, beaker, left_swarm = solution_stage([-4.6, -3.45, 0], profile=BEAKER, volume=1000.0, zoom=1.0, solvent=320,
                                              solute=4, seed=5, mark=True, spin=0.1,
                                              style="polished", solvent_radius=0.027)
    beaker.reflection_alpha = 0.0
    left_swarm.mix, left_swarm.solute_alpha = 0.0, 0.0
    left_swarm.drop_from = beaker.top_point() + np.array([0.0, 1.0, 0.0])
    tempting = VGroup(txt("the tempting way", cfg.FONT["label"], cfg.WARNING),
                      txt("1 L of water", cfg.FONT["small"], cfg.SOLVENT)).arrange(DOWN, buff=0.1)
    tempting.move_to([-4.6, 2.55, 0])
    show(scene, left, 1.0, FadeIn(tempting))
    scene.play(set_attr(left, left_swarm, "solute_alpha", 1.0), set_attr(left, left_swarm, "solute_glow", 0.45),
               run_time=0.8)

    # --- 4. It rises past the mark --------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(set_attr(left, left_swarm, "mix", 1.0), beaker.set_volume(cd.wrong_way_mL()), run_time=5.0)
    over = VGroup(txt("more than 1 L", cfg.FONT["label"], cfg.WARNING),
                  eq(rf"< {fx(TARGET_M, 3)}\ \mathrm{{M}}", cfg.FONT["label"], cfg.WARNING)).arrange(DOWN, buff=0.15)
    over.move_to([-1.3, -0.9, 0])
    scene.play(beaker.set_attr("mark_glow", 1.0), FadeIn(over, shift=LEFT * 0.2), run_time=1.0)
    nope = cross_mark(0.35).next_to(tempting, DOWN, buff=0.2)
    scene.play(Create(nope), run_time=0.6)

    # --- 5. The right way: a volumetric flask ------------------------------------------------------------------------------
    beat(scene, t, 4)
    right, flask, swarm = solution_stage([4.1, -3.55, 0], profile=FLASK, volume=0.0, zoom=1.08, solvent=420, solute=5,
                                         seed=6, mark=True, spin=0.1,
                                         style="polished", solvent_radius=0.027)
    flask.reflection_alpha = 0.0
    swarm.mix, swarm.solvent_alpha = 0.0, 0.0
    swarm.drop_from = flask.top_point() + np.array([0.0, 0.3, 0.0])
    name = VGroup(txt("volumetric", cfg.FONT["label"], cfg.CYAN), txt("flask", cfg.FONT["label"], cfg.CYAN))
    name.arrange(DOWN, buff=0.1).move_to([6.35, 0.2, 0])
    scene.play(FadeOut(need), run_time=0.4)
    show(scene, right, 1.2, FadeIn(name))
    line_label = txt("one line", cfg.FONT["small"], cfg.GOLD).move_to([1.4, 1.0, 0])
    scene.play(flask.set_attr("mark_glow", 1.0), FadeIn(line_label, shift=RIGHT * 0.2), run_time=1.0)

    # --- 6. Glucose first, some water, swirl ---------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(flask.set_attr("mark_glow", 0.0), FadeOut(line_label), set_attr(right, swarm, "solute_glow", 0.45),
               run_time=0.6)
    scene.play(set_attr(right, swarm, "mix", 0.34), run_time=1.6)
    scene.play(flask.set_volume(600.0), set_attr(right, swarm, "solvent_alpha", 1.0), run_time=2.4)
    swirl = txt("swirl to dissolve", cfg.FONT["small"], cfg.CYAN).move_to([1.4, 1.0, 0])
    scene.play(set_attr(right, swarm, "mix", 1.0), set_attr(right, swarm, "speed", 3.0), right.rock(UP, 1.2),
               FadeIn(swirl), run_time=3.0)
    scene.play(set_attr(right, swarm, "speed", 1.0), right.rock(UP, -1.2), run_time=1.6)

    # --- 7. Fill slowly to the mark -------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(FadeOut(swirl), flask.set_volume(970.0), run_time=3.0)
    scene.play(flask.set_volume(1000.0), flask.set_attr("mark_glow", 1.0), run_time=3.0, rate_func=rate_functions.ease_out_sine)
    meniscus = txt("meniscus on the line", cfg.FONT["small"], cfg.GOLD).move_to([1.3, 1.0, 0])
    scene.play(FadeIn(meniscus, shift=RIGHT * 0.2), run_time=0.7)

    # --- 8. Stopper and invert ---------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    flask.lid = True
    scene.play(FadeOut(meniscus), flask.set_attr("mark_glow", 0.0), run_time=0.5)
    for angle in (0.55, -1.1, 0.55):
        scene.play(right.rock(OUT, angle), set_attr(right, swarm, "speed", 2.2), run_time=1.0)
    scene.play(set_attr(right, swarm, "speed", 1.0), run_time=0.5)

    # --- 9. Final volume: one litre ----------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    scene.play(flask.set_glow(1.0), run_time=1.0)
    final = eq(rf"V = {fx(1.0, 3)}\ \mathrm{{L}}", cfg.FONT["body"], cfg.VOLUME)
    final_note = txt("final volume", cfg.FONT["small"], cfg.VOLUME)
    final_group = VGroup(final, final_note).arrange(DOWN, buff=0.15).move_to([0.6, 0.75, 0])
    scene.play(FadeIn(final_group, shift=UP * 0.15), run_time=1.2)

    # --- 10. 0.500 M by construction ------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    result = numbers_fraction(rf"{fx(TARGET_M, 3)}\ \mathrm{{mol}}", rf"{fx(1.0, 3)}\ \mathrm{{L}}",
                              rf"{fx(TARGET_M, 3)}\ \mathrm{{M}}", cfg.AMOUNT, cfg.VOLUME, cfg.FONT["section"])
    result_box = boxed(result).move_to([-1.6, 1.0, 0])
    hide(scene, left, 0.6, FadeOut(VGroup(tempting, nope, over, final_group)))
    scene.play(right.glide([3.6, -3.55, 0]), FadeIn(result_box, scale=1.08), run_time=1.4)
    scene.play(Indicate(result[6], color=cfg.WHITE, scale_factor=1.1), run_time=1.0)

    # --- 11. The catch: calibrated at 20 °C ----------------------------------------------------------------------------------------
    beat(scene, t, 10)
    thermo = Thermometer([-2.6, -0.85, 0], low=0, high=60, height=3.6)
    calibrated = chip("calibrated at 20 °C", cfg.GOLD).move_to([-0.2, 1.6, 0])
    scene.play(FadeOut(result_box), flask.set_glow(0.0), flask.set_attr("mark_glow", 1.0), run_time=0.8)
    scene.play(FadeIn(thermo), FadeIn(calibrated, shift=DOWN * 0.15), run_time=1.0)

    # --- 12. Warm it: the liquid creeps past the line --------------------------------------------------------------------------------
    beat(scene, t, 11)
    warm = txt("40 °C", cfg.FONT["label"], cfg.HEAT).next_to(thermo, RIGHT, buff=0.35)
    scene.play(thermo.celsius.to(thermo, 40.0), flask.set_volume(cd.warm_flask_mL()),
               set_attr(right, swarm, "speed", 2.0), FadeIn(warm), run_time=3.5)
    past = txt("past the line", cfg.FONT["small"], cfg.WARNING).move_to([1.5, 0.2, 0])
    scene.play(FadeIn(past), run_time=0.6)

    # --- 13. What if the volume itself changes? ------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    question = VGroup(txt("What happens when", cfg.FONT["body"], cfg.GOLD),
                      txt("the volume itself changes?", cfg.FONT["body"], cfg.GOLD)).arrange(DOWN, buff=0.1)
    question.move_to([-3.4, 2.45, 0])
    scene.play(FadeOut(calibrated), run_time=0.4)
    scene.play(FadeIn(question, shift=UP * 0.15), run_time=0.8)
    scene.play(thermo.celsius.to(thermo, 20.0), flask.set_volume(1000.0), set_attr(right, swarm, "speed", 1.0),
               FadeOut(warm), FadeOut(past), run_time=4.0)
    scene.play(thermo.celsius.to(thermo, 40.0), flask.set_volume(cd.warm_flask_mL()), set_attr(right, swarm, "speed", 2.0),
               run_time=7.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["05"])
