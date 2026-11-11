"""Scene 08 — thermal motion. The gas never sits still: live gold velocity
arrows ride a few molecules. Temperature measures the average translational
kinetic energy, <K> = 3/2 k_B T, written step by step. A speed histogram of
a large Maxwell-Boltzmann sample (the same distribution as the box's gas)
shows "average" means a spread of slow and fast; heating to 600 K shifts the
whole distribution right while the box's molecules visibly speed up. Room
temperature numbers (6.2e-21 J per molecule, RT = 2.5 kJ/mol) close it.
"""

from manim_scenes.common import *

SAMPLE = pm.IdealGas(3000, cfg.SEED + 8)
SPEEDS = np.linalg.norm(SAMPLE.u, axis=1)          # rms units at 300 K


class Scene08ThermalMotion(Scene):
    def construct(self) -> None:
        play_scene(self)


def histogram(axes: Axes, heat: Callable[[], float], bins: int = 18, top: float = 3.0) -> VGroup:
    """Bars of the sample's speed distribution at the current temperature (probability density)."""
    edges = np.linspace(0, top, bins + 1)
    counts, _ = np.histogram(SPEEDS * heat(), bins=edges)
    density = counts / (len(SPEEDS) * (edges[1] - edges[0]))
    bars = VGroup()
    for a, b, d in zip(edges[:-1], edges[1:], density):
        if d <= 0:
            continue
        bars.add(Polygon(axes.c2p(a, 0), axes.c2p(b, 0), axes.c2p(b, d), axes.c2p(a, d), stroke_color=cfg.CYAN,
                         stroke_width=1.5, fill_color=cfg.MOLECULE, fill_opacity=0.45))
    return bars


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "08", "Thermal motion")
    box = GasBox((-3.9, -0.5, 0), count=80, half_x=1.5, half_z=1.1, height=2.8, floor=-1.4, zoom=1.15, yaw=-0.5,
                 pitch=0.3, speed=1.5)
    show(scene, box.stage, 1.0)

    # --- 2. Every molecule moves: thermal energy -----------------------------------------------------------------------
    beat(scene, t, 1)
    arrows = []
    for i in (3, 29, 61):
        arrow = Vector(lambda i=i: box.cloud.position(i), lambda i=i: box.cloud.position(i) + box.cloud.velocity(i) * 0.55,
                       cfg.VELOCITY, width=0.05, tip=0.17)
        arrow.presence = 0.0
        arrows.append(arrow)
    box.stage.add_overlay(*arrows)
    word = result_label("thermal energy", cfg.TEMPERATURE, cfg.FONT["section"]).move_to([3.0, 2.9, 0])
    scene.play(*[box.stage.fade(a, 1.0) for a in arrows], run_time=1.2)
    scene.play(FadeIn(word, shift=DOWN * 0.1), run_time=0.9)
    scene.play(*box.stage.turn(yaw=-0.2), run_time=5.0)

    # --- 3. Temperature is its measure ------------------------------------------------------------------------------------
    beat(scene, t, 2)
    therm = Thermo(box.kelvin, [-0.8, 0.2, 0], low=200, high=700, height=2.8)
    measure = txt("average translational energy", cfg.FONT["label"], cfg.WHITE).move_to([3.4, 1.6, 0])
    fit_width(measure, 7.6)
    scene.play(FadeIn(therm, shift=LEFT * 0.2), run_time=1.0)
    scene.play(FadeIn(measure, shift=UP * 0.1), run_time=1.0)
    scene.play(*box.stage.turn(yaw=-0.45), run_time=5.0)

    # --- 4. <K> = 3/2 k_B T -------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    law = paint(eq([r"\langle K\rangle", "=", r"\tfrac{3}{2}", r"k_B", "T"], cfg.FONT["hero"]), {0: cfg.GOLD, 4: cfg.TEMPERATURE})
    law.move_to([3.4, 2.0, 0])
    scene.play(FadeOut(VGroup(word, measure)), *[box.stage.fade(a, 0.0) for a in arrows], run_time=0.6)
    scene.play(Write(law), run_time=2.0)

    # --- 5. k_B and kelvin ---------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    kb = eq(rf"k_B \approx {sci(pm.K_B, 2)}\ \mathrm{{J/K}}", cfg.FONT["body"], cfg.WHITE).next_to(law, DOWN, buff=0.55)
    kelvin = txt("T in kelvin", cfg.FONT["label"], cfg.TEMPERATURE).next_to(kb, DOWN, buff=0.4)
    scene.play(FadeIn(kb, shift=UP * 0.1), Indicate(law[3], color=cfg.WHITE), run_time=1.4)
    scene.play(FadeIn(kelvin), Indicate(law[4], color=cfg.TEMPERATURE), run_time=1.2)
    scene.wait(1.0)

    # --- 6. Average: a distribution of slow and fast ------------------------------------------------------------------------
    beat(scene, t, 5)
    axes = plot_axes((0, 3.0), (0, 1.0), x_length=5.6, y_length=3.0, at=[3.1, -1.15, 0], x_label=r"\text{speed}",
                     y_label="", x_color=cfg.VELOCITY)
    bars = live(VGroup(), lambda: histogram(axes, lambda: box.cloud.heat))
    maxwell = live(VGroup(), lambda: curve_on(axes, lambda s: float(pm.maxwell_pdf(s, box.cloud.heat)), 0.0, 3.0,
                                              cfg.GOLD, width=5, samples=80))
    slow = txt("slow", cfg.FONT["tiny"], cfg.CYAN).move_to(axes.c2p(0.35, 0.95))
    fast = txt("fast", cfg.FONT["tiny"], cfg.HOT_COLOR).move_to(axes.c2p(2.5, 0.45))
    law_small = law.copy()
    scene.play(FadeOut(VGroup(kb, kelvin)), law.animate.scale(0.62).move_to([3.4, 2.75, 0]), run_time=1.0)
    scene.play(Create(axes), FadeIn(bars), run_time=1.4)
    scene.play(Create(maxwell), FadeIn(slow), FadeIn(fast), run_time=1.6)

    # --- 7. Heat: the whole distribution shifts -----------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(box.heat_to(600, run_time=4.0), box.cloud.tween("warmth", 0.55, run_time=4.0),
               FadeOut(VGroup(slow, fast)), run_time=4.0)
    scene.wait(1.6)

    # --- 8. Room temperature: tiny per molecule, 2.5 kJ per mole -----------------------------------------------------------------
    beat(scene, t, 7)
    per_molecule = eq(rf"\langle K\rangle_{{300\,\mathrm{{K}}}} \approx {sci(pm.mean_kinetic_energy(pm.ROOM_T), 1)}\ \mathrm{{J}}",
                      cfg.FONT["label"], cfg.GOLD)
    per_mole = eq(rf"RT \approx {fx(pm.thermal_energy_per_mole(pm.ROOM_T), 1)}\ \mathrm{{kJ/mol}}", cfg.FONT["label"], cfg.TEMPERATURE)
    numbers = VGroup(per_molecule, per_mole).arrange(DOWN, buff=0.4).move_to([3.4, -0.6, 0])
    scene.play(box.heat_to(pm.ROOM_T, run_time=2.0), box.cloud.tween("warmth", 0.0, run_time=2.0),
               FadeOut(VGroup(axes, bars, maxwell)), run_time=2.0)
    bars.clear_updaters(), maxwell.clear_updaters()
    scene.play(FadeIn(per_molecule, shift=UP * 0.1), run_time=1.0)
    scene.wait(3.0)
    scene.play(FadeIn(per_mole, shift=UP * 0.1), run_time=1.0)
    finish(scene, t, box.stage)
