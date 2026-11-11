"""Scene 20 — Kelvin, not Celsius. Worked example at constant pressure: 2 L
at 300 K heated to 450 K. The viewer predicts; the weighted piston rises
and the model gives 3 L (temperature up by half, volume up by half). Then the
trap: 20 C to 30 C is a 50 % rise on the Celsius scale, but on the Kelvin
scale (293.15 K to 303.15 K) it is only about 3 %, and so is the volume
change. Paired bars make the difference visible.
"""

from manim_scenes.common import *

C, T = pm.CHARLES, pm.CELSIUS_TRAP


class Scene20Kelvin(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "20", "Kelvin, not Celsius")
    box = GasBox((-4.3, -1.15, 0), count=100, seed=cfg.SEED + 20, half_x=1.3, half_z=1.0, height=1.9, floor=-0.95,
                 lid="weight", heater=True, zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.5, spark_axes=(1,), spark_sides=(1,))
    volume = readout("V", lambda: C.V1 * box.chamber.volume_ratio(), 2, "L", cfg.VOLUME, size=44).move_to([-4.3, 2.8, 0])
    temp = readout("T", box.kelvin, 0, "K", cfg.TEMPERATURE, size=44).move_to([-4.3, 2.05, 0])
    given = VGroup(eq(rf"V_1 = {fx(C.V1, 0)}\ \mathrm{{L}},\ T_1 = {fx(C.T1, 0)}\ \mathrm{{K}}", cfg.FONT["body"], cfg.WHITE),
                   eq(rf"T_2 = {fx(C.T2, 0)}\ \mathrm{{K}}", cfg.FONT["body"], cfg.TEMPERATURE),
                   eq(r"V_2 = \ ?", cfg.FONT["body"], cfg.GOLD)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.4, 0.9, 0])
    show(scene, box.stage, 1.0, FadeIn(volume), FadeIn(temp))
    scene.play(FadeIn(given[0], shift=LEFT * 0.2), run_time=1.0)
    scene.play(FadeIn(given[1], shift=LEFT * 0.2), run_time=1.0)
    scene.play(FadeIn(given[2], shift=LEFT * 0.2), run_time=0.8)

    # --- 2. Predict -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    countdown(scene, [3.4, -1.8, 0], 3)

    # --- 3. Up by half: 3 L -------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(*box.heater_on(1.0), run_time=0.6)
    scene.play(box.heat_to(C.T2, run_time=3.5), box.volume_to(C.V2 / C.V1, run_time=3.5), box.cloud.tween("warmth", 0.35, run_time=3.5),
               run_time=3.5)
    work = eq(rf"V_2 = V_1\frac{{T_2}}{{T_1}} = {fx(C.V1, 0)} \times \frac{{{fx(C.T2, 0)}}}{{{fx(C.T1, 0)}}} = {fx(C.V2, 0)}\ \mathrm{{L}}",
              cfg.FONT["body"], cfg.WHITE).move_to([3.0, -1.6, 0])
    fit_width(work, 8.0)
    answer = eq(rf"V_2 = {fx(C.V2, 0)}\ \mathrm{{L}}", cfg.FONT["body"], cfg.GOLD).move_to(given[2])
    scene.play(Write(work), fade_through(given[2], answer), run_time=2.0)

    # --- 4. The trap: 20 C -> 30 C is +50 % in Celsius -------------------------------------------------------------------------------
    beat(scene, t, 3)
    hide(scene, box.stage, 0.8, FadeOut(VGroup(volume, temp, given[:2], answer, work)))
    celsius = bar_chart([T.c1, T.c2], [f"{fx(T.c1, 0)} °C", f"{fx(T.c2, 0)} °C"], [cfg.CYAN, cfg.HOT_COLOR], at=[-3.6, -0.2, 0],
                        width=4.4, height=3.6, top=T.c2, bar_width=1.3)
    c_title = txt("Celsius: +50 %", cfg.FONT["label"], cfg.WARNING).next_to(celsius, UP, buff=0.4)
    scene.play(Create(celsius.base), FadeIn(celsius.names), FadeIn(c_title), run_time=0.8)
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in celsius.bars], lag_ratio=0.4), run_time=1.6)

    # --- 5. But the volume grows only ~3 % ---------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    vols = bar_chart([T.V1, T.V2], [f"{fx(T.V1, 2)} L", f"{fx(T.V2, 2)} L"], [cfg.VOLUME, cfg.VOLUME], at=[3.6, -0.2, 0],
                     width=4.4, height=3.6, top=T.V2, bar_width=1.3)
    v_title = txt(f"volume: +{fx(T.percent, 1)} %", cfg.FONT["label"], cfg.VOLUME).next_to(vols, UP, buff=0.4)
    scene.play(Create(vols.base), FadeIn(vols.names), FadeIn(v_title), LaggedStart(*[GrowFromEdge(b, DOWN) for b in vols.bars],
                                                                                    lag_ratio=0.4), run_time=1.6)

    # --- 6. In kelvin: 293.15 K -> 303.15 K -------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    k1, k2 = pm.celsius_to_kelvin(T.c1), pm.celsius_to_kelvin(T.c2)
    kelvin = bar_chart([k1, k2], [f"{fx(k1, 2)} K", f"{fx(k2, 2)} K"], [cfg.CYAN, cfg.HOT_COLOR], at=[-3.6, -0.2, 0], width=4.4,
                       height=3.6, top=k2, bar_width=1.3, name_size=30)
    k_title = txt(f"Kelvin: +{fx(100 * (k2 / k1 - 1), 1)} %", cfg.FONT["label"], cfg.TEMPERATURE).next_to(kelvin, UP, buff=0.4)
    scene.play(FadeOut(celsius), FadeOut(c_title), run_time=0.7)
    scene.play(Create(kelvin.base), FadeIn(kelvin.names), FadeIn(k_title),
               LaggedStart(*[GrowFromEdge(b, DOWN) for b in kelvin.bars], lag_ratio=0.4), run_time=1.8)
    match = txt("the volume follows kelvin", cfg.FONT["label"], cfg.GOLD).move_to([0, -3.0, 0])
    scene.play(FadeIn(match, shift=UP * 0.1), run_time=1.0)

    # --- 7. Only the Kelvin scale starts at zero kinetic energy ------------------------------------------------------------------------------
    beat(scene, t, 6)
    rule = boxed(txt("gas laws need kelvin", cfg.FONT["section"], cfg.GOLD), cfg.GOLD).to_edge(UP, buff=0.4)
    scene.play(FadeIn(rule, scale=0.95), run_time=1.2)
    finish(scene, t, fill=lambda s: [Indicate(VGroup(kelvin.bars, vols.bars), color=cfg.WHITE, scale_factor=1.02)])
