"""Scene 03 — masses add, volumes need not: 50 mL ethanol + 50 mL water gives
about 96.5 mL (from measured mixture densities, ``concentration_data``),
so a solution's volume is measured, not added. Then the four quantities every
concentration is built from.

The packing picture (big and small spheres) is a metaphor, labelled so: the
real contraction comes from how the molecules attract and arrange.
"""

from manim_scenes.common import *

CYL = pm.cylinder_profile(radius=0.55, height=4.3, mark_y=3.8, mark_mL=100.0)
MIXED_ML = cd.ethanol_water_mix_mL()


class Scene03VolumeNotAdditive(Scene):
    def construct(self) -> None:
        play_scene(self)


def packing_sphere(point, color: str, radius: float) -> VGroup:
    """Use the molecular sphere material without the old hard highlight dots."""
    sphere = Ball(ORIGIN, 1.0, color, layers=28).mob
    return sphere.scale(radius).move_to(point)


def cylinder(at, volume: float, color: str, zoom: float = 0.95) -> tuple[Stage, Glassware]:
    stage = Stage(at, zoom=zoom, yaw=0.3, pitch=0.28, spin=0.0, sway=0.04)
    glass = Glassware(stage, CYL, volume=volume, liquid_color=color, mark=True,
                      ticks=[CYL.height_for(v) for v in (20, 40, 60, 80)])
    glass.reflection_alpha = 0.0
    return stage, glass


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "03", "Mass adds. Does volume?")

    # --- 1. Mass adds; does volume? ----------------------------------------------------------------------------
    mass = eq([r"m_1 + m_2", "=", r"m_{\text{total}}"], cfg.FONT["section"]).move_to([0, 1.2, 0])
    volume = eq([r"V_1 + V_2", "=", r"V_{\text{total}}", "?"], cfg.FONT["section"]).move_to([0, -0.6, 0])
    mass[2].set_color(cfg.SOLUTION_MASS)
    volume[2].set_color(cfg.VOLUME)
    volume[3].set_color(cfg.GOLD)
    tick = check_mark(0.3).next_to(mass, RIGHT, buff=0.4)
    scene.play(Write(mass), Create(tick), run_time=1.2)
    scene.play(Write(volume), run_time=1.2)

    # --- 2. Two liquids, fifty millilitres each ---------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(VGroup(mass, volume, tick)), run_time=0.6)
    eth_stage, eth = cylinder([-5.6, -3.4, 0], 50.0, cfg.ETHANOL)
    wat_stage, wat = cylinder([-3.0, -3.4, 0], 50.0, cfg.LIQUID)
    mix_stage, mix = cylinder([3.4, -3.4, 0], 0.0, mu.mix(cfg.ETHANOL, cfg.LIQUID, 0.5), zoom=1.15)
    labels = VGroup(VGroup(txt("ethanol", cfg.FONT["small"], cfg.ETHANOL), txt("50 mL", cfg.FONT["small"], cfg.WHITE)),
                    VGroup(txt("water", cfg.FONT["small"], cfg.SOLVENT), txt("50 mL", cfg.FONT["small"], cfg.WHITE)))
    for label, x in zip(labels, (-5.6, -3.0)):
        label.arrange(DOWN, buff=0.1).move_to([x, 1.75, 0])
    mark_label = txt("100 mL mark", cfg.FONT["small"], cfg.MUTED).move_to([5.9, 0.75, 0])
    show(scene, eth_stage, 0.9, FadeIn(labels[0]))
    show(scene, wat_stage, 0.9, FadeIn(labels[1]))
    show(scene, mix_stage, 0.9, FadeIn(mark_label))

    # --- 3. Mix them: about 96.5 mL --------------------------------------------------------------------------------------
    beat(scene, t, 2)
    arrow = glow_arrow([-1.0, -1.2, 0], [1.6, -1.2, 0], cfg.CYAN)
    scene.play(GrowFromEdge(arrow, LEFT), run_time=0.6)
    scene.play(eth.set_volume(0.0), wat.set_volume(0.0), mix.set_volume(MIXED_ML), run_time=4.5)
    result = VGroup(txt(f"{MIXED_ML:.1f} mL", cfg.FONT["section"], cfg.WHITE),
                    txt("not 100", cfg.FONT["label"], cfg.WARNING)).arrange(DOWN, buff=0.12).move_to([0.4, 1.0, 0])
    scene.play(FadeIn(result, shift=UP * 0.2), mix.set_attr("mark_glow", 1.0), Indicate(mark_label, color=cfg.GOLD),
               run_time=1.2)

    # --- 4. Nothing leaked: the molecules pack differently --------------------------------------------------------------------
    beat(scene, t, 3)
    hide(scene, eth_stage, 0.5, FadeOut(labels), FadeOut(arrow))
    hide(scene, wat_stage, 0.3)
    origin = np.array([-3.4, -0.4, 0])
    bigs = VGroup(*[packing_sphere(origin + np.array([x, y, 0]), cfg.ETHANOL, 0.45)
                   for x in (-0.95, 0, 0.95) for y in (0.95, 0, -0.95)])
    holes = [origin + np.array([x, y, 0]) for x in (-0.475, 0.475) for y in (-0.475, 0.475)]
    smalls = VGroup(*[packing_sphere(origin + np.array([-0.9 + 0.6 * k, -1.85, 0]), cfg.SOLVENT, 0.19)
                     for k in range(4)])
    before = Brace(VGroup(bigs, smalls), LEFT, color=cfg.MUTED)
    metaphor = txt("a picture, not to scale", cfg.FONT["tiny"], cfg.MUTED).move_to([-3.4, 2.3, 0])
    scene.play(FadeIn(bigs), FadeIn(smalls), FadeIn(metaphor), run_time=1.0)
    scene.play(GrowFromCenter(before), run_time=0.6)
    scene.play(*[s.animate.move_to(h) for s, h in zip(smalls, holes)], run_time=2.2)
    after = Brace(bigs, LEFT, color=cfg.CYAN)
    scene.play(Transform(before, after), run_time=0.8)
    hold = txt("they hold on and nestle in", cfg.FONT["small"], cfg.CYAN).move_to([-3.4, -2.75, 0])
    scene.play(FadeIn(hold), run_time=0.6)

    # --- 5. Measure the final volume: our glucose solution --------------------------------------------------------------------
    beat(scene, t, 4)
    hide(scene, mix_stage, 0.6, FadeOut(VGroup(bigs, smalls, before, metaphor, hold, result, mark_label)))
    stage, glass, swarm = solution_stage([-3.6, -3.25, 0], zoom=1.2, solvent=500, solute=5, seed=3,
                                         style="polished", solvent_radius=0.027)
    glass.reflection_alpha = 0.0
    show(scene, stage, 1.0)
    scene.play(glass.set_glow(1.0), run_time=1.0)
    measured = VGroup(eq(rf"V = {V_ML}\ \mathrm{{mL}}", cfg.FONT["section"], cfg.VOLUME),
                      chip("measured, not added", cfg.CYAN)).arrange(DOWN, buff=0.3).move_to([3.4, 0.0, 0])
    scene.play(Write(measured[0]), run_time=1.2)
    scene.play(FadeIn(measured[1], shift=UP * 0.15), run_time=0.7)

    # --- 6. Four quantities --------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    rows = [
        (rf"n_{{\text{{glucose}}}} = {N_SOLUTE}\ \mathrm{{mol}}", cfg.AMOUNT, cfg.SOLUTE),
        (rf"n_{{\text{{water}}}} = {N_SOLVENT}\ \mathrm{{mol}}", cfg.AMOUNT, cfg.SOLVENT),
        (rf"m_{{\text{{solution}}}} = {fx(REF.solution_g, 1)}\ \mathrm{{g}}", cfg.SOLUTION_MASS, cfg.SOLUTION_MASS),
        (rf"V_{{\text{{solution}}}} = {V_ML}\ \mathrm{{mL}}", cfg.VOLUME, cfg.VOLUME),
    ]
    chips = VGroup(*[eq_chip(tex, color, stroke=stroke) for tex, color, stroke in rows]).arrange(DOWN, buff=0.28)
    chips.move_to([3.4, 0.35, 0])
    scene.play(FadeOut(measured), run_time=0.5)
    scene.play(FadeIn(chips[0], shift=LEFT * 0.2), set_attr(stage, swarm, "solute_glow", 0.45), glass.set_glow(0.0),
               run_time=0.9)
    scene.play(FadeIn(chips[1], shift=LEFT * 0.2), set_attr(stage, swarm, "solvent_glow", 1.0), run_time=0.9)
    scene.play(FadeIn(chips[2], shift=LEFT * 0.2), set_attr(stage, swarm, "solvent_glow", 0.0), run_time=0.9)
    scene.play(FadeIn(chips[3], shift=LEFT * 0.2), glass.set_glow(1.0), run_time=0.9)

    # --- 7. Every concentration: one of these over another ------------------------------------------------------------------------
    beat(scene, t, 6)
    template = eq([r"\text{concentration}", "=", r"\frac{\text{one of these}}{\text{another}}"], cfg.FONT["label"])
    template[0].set_color(cfg.GOLD)
    fit_width(template, 7.4)
    template.move_to([3.4, -2.95, 0])
    scene.play(Write(template), run_time=1.6)
    scene.play(LaggedStart(*[Indicate(c, color=cfg.WHITE, scale_factor=1.05) for c in chips], lag_ratio=0.3),
               run_time=3.0)
    scene.play(glass.set_glow(0.4), Circumscribe(template, color=cfg.GOLD, buff=0.12), run_time=3.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
