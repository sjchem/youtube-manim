"""Scene 09 — the tug of war. A potential-well inset shows the competition:
a level for the thermal energy rises with the simulation's measured
temperature. The main picture is a real 2D Lennard-Jones simulation
(``physics_models.phase_movie``): 61 atoms crystallise at low temperature
(each only vibrates), slip past one another as a liquid droplet, then boil
into a gas that fills the box. Argon's well (~1 kJ/mol) against RT at 300 K
(2.49 kJ/mol) explains why argon is a gas here. Finally a separate ideal-gas
model switches off pair interactions and highlights wall collisions.
"""

from manim_scenes.common import *

MD_AT = np.array([1.6, -0.5, 0.0])


class Scene09TugOfWar(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "09", "The tug of war")
    view = MDView(MD_AT, scale=0.3)
    axes = plot_axes((0.9, 3.0), (-1.2, 1.0), x_length=2.9, y_length=2.6, at=[-5.7, 1.5, 0], x_label="r", y_label="U",
                     label_size=cfg.FONT["small"])
    well = curve_on(axes, lambda r: float(np.clip(pm.lennard_jones(r), -1.2, 1.0)), 0.97, 3.0, cfg.ATTRACT, width=4)

    def level() -> float:
        return float(np.clip(-1.0 + 0.95 * view.temperature(), -0.98, 0.95))

    energy = live(VMobject(), lambda: DashedLine(axes.c2p(0.95, level()), axes.c2p(3.0, level()), stroke_color=cfg.TEMPERATURE,
                                                 stroke_width=4, dash_length=0.1))
    pull = chip("attraction pulls together", cfg.ATTRACT)
    shake = chip("thermal motion shakes apart", cfg.TEMPERATURE)
    vs = VGroup(pull, shake).arrange(RIGHT, buff=0.4).move_to([1.0, 0.2, 0])
    fit_width(vs, 11.5)
    scene.play(Create(axes), Create(well), run_time=1.2)
    scene.add(energy)
    scene.play(FadeIn(pull, shift=RIGHT * 0.2), run_time=0.9)
    scene.play(FadeIn(shake, shift=LEFT * 0.2), run_time=0.9)

    # --- 2. 61 atoms in a real 2D simulation -------------------------------------------------------------------------------
    beat(scene, t, 1)
    label = txt(f"{view.frames.shape[1]} atoms · 2D simulation", cfg.FONT["small"], cfg.MUTED).next_to(view.box, UP, buff=0.18)
    thermo = readout(r"k_BT/\varepsilon", view.temperature, 2, "", cfg.TEMPERATURE, size=34).move_to([-5.8, -0.4, 0])
    scene.play(FadeOut(vs), FadeIn(view), FadeIn(label), FadeIn(thermo), run_time=1.4)

    # --- 3. Small thermal energy: a crystal; each atom vibrates ---------------------------------------------------------------
    beat(scene, t, 2)
    state = result_label("solid", cfg.CYAN, cfg.FONT["section"]).move_to([-5.8, -2.0, 0])
    scene.play(FadeIn(state, scale=0.9), view.clock.to(view, 3.0, run_time=3.0, rate_func=linear), run_time=3.0)
    scene.play(view.clock.to(view, 10.0, run_time=9.5, rate_func=linear), run_time=9.5)

    # --- 4. Warm: atoms slip past one another, still together: a liquid ------------------------------------------------------
    beat(scene, t, 3)
    liquid = result_label("liquid", cfg.ATTRACT, cfg.FONT["section"]).move_to([-5.8, -2.0, 0])
    scene.play(fade_through(state, liquid), view.clock.to(view, 13.0, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(view.clock.to(view, 32.0, run_time=8.0, rate_func=linear), run_time=8.0)

    # --- 5. Far more energy than the well holds: a gas ------------------------------------------------------------------------
    beat(scene, t, 4)
    gas = result_label("gas", cfg.TEMPERATURE, cfg.FONT["section"]).move_to([-5.8, -2.0, 0])
    scene.play(view.clock.to(view, 42.0, run_time=4.0, rate_func=linear), run_time=4.0)
    scene.play(fade_through(liquid, gas), view.clock.to(view, 45.0, run_time=1.2, rate_func=linear), run_time=1.2)
    scene.play(view.clock.to(view, 62.0, run_time=6.5, rate_func=linear), run_time=6.5)

    # --- 6. The balance: attraction vs thermal energy, with pressure ----------------------------------------------------------
    beat(scene, t, 5)
    balance = VGroup(txt("attraction", cfg.FONT["label"], cfg.ATTRACT), txt("vs", cfg.FONT["label"], cfg.WHITE),
                     txt("thermal energy", cfg.FONT["label"], cfg.TEMPERATURE), txt("(+ pressure)", cfg.FONT["small"], cfg.MUTED))
    balance.arrange(RIGHT, buff=0.3).move_to([1.6, 3.1, 0])
    fit_width(balance, 10.0)
    scene.play(FadeOut(label), view.clock.to(view, 63.0, run_time=0.6, rate_func=linear), run_time=0.6)
    scene.play(FadeIn(balance, shift=DOWN * 0.1), view.clock.to(view, 64.0, run_time=1.4, rate_func=linear), run_time=1.4)
    scene.play(view.clock.to(view, 66.0, run_time=5.5, rate_func=linear), run_time=5.5)

    # --- 7. Argon: a shallow well, a gas at room temperature ------------------------------------------------------------------
    beat(scene, t, 6)
    argon_well = pm.R * pm.ARGON_WELL_K / 1000
    rt = pm.thermal_energy_per_mole(pm.ROOM_T)
    chart = bar_chart([argon_well, rt], ["argon's well", "RT at 300 K"], [cfg.ATTRACT, cfg.TEMPERATURE], at=[1.6, -0.35, 0],
                      width=6.4, height=2.5, value_labels=[f"≈ {fx(argon_well, 1)}", f"{fx(rt, 2)}"], bar_width=1.5)
    unit = txt("kJ/mol", cfg.FONT["small"], cfg.MUTED).next_to(chart, UP, buff=0.3)
    boils = txt(f"argon boils near {fx(pm.NOBLE_BOILING_K['Ar'], 0)} K", cfg.FONT["label"], cfg.CYAN).move_to([1.6, -2.9, 0])
    scene.play(FadeOut(balance), view.animate.set_opacity(0.0), run_time=0.8)
    scene.play(Create(chart.base), FadeIn(chart.names), FadeIn(unit), run_time=0.8)
    scene.play(GrowFromEdge(chart.bars[0], DOWN), FadeIn(chart.tops[0]), run_time=1.2)
    scene.play(GrowFromEdge(chart.bars[1], DOWN), FadeIn(chart.tops[1]), run_time=1.2)
    scene.play(FadeIn(boils, shift=UP * 0.1), run_time=0.9)
    scene.wait(4.0)

    # --- 8. Dilute gas: ignore attractions, treat molecules as points: the ideal gas -------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(chart, unit, boils)), view.animate.set_opacity(1.0), run_time=0.9)
    ideal = GasBox((1.6, -0.5, 0), count=61, seed=cfg.SEED + 90,
                   half_x=2.4, half_z=1.0, height=3.2, floor=-1.6,
                   zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.8, radius=0.045,
                   spark_axes=(0,), spark_sides=(1,))
    model = VGroup(txt("ideal gas model", cfg.FONT["section"], cfg.LIMIT),
                   txt("points · no attractions", cfg.FONT["label"], cfg.WHITE)).arrange(DOWN, buff=0.22).move_to([1.6, 3.15, 0])
    scene.play(view.clock.to(view, 68.0, run_time=3.0, rate_func=linear), run_time=3.0)
    view.clear_updaters()
    energy.clear_updaters()
    show(scene, ideal.stage, 2.0, FadeIn(model, shift=DOWN * 0.1),
         FadeOut(VGroup(view, thermo, gas, axes, well, energy)))
    scene.wait(6.0)

    # --- 9. What happens at a wall? ----------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    ask = chip("what happens\nat a wall?", cfg.IMPULSE, cfg.FONT["label"]).move_to([-5.8, -2.0, 0])
    fit_width(ask, 3.4)
    # Collision sparks pick out the right wall of the genuinely ideal model.
    scene.play(ideal.cloud.tween("spark", 1.6), run_time=0.6)
    scene.play(FadeIn(ask, shift=UP * 0.1), run_time=0.6)
    finish(scene, t, ideal.stage)
