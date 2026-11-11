"""Scene 24 — equal volumes, equal numbers. Three equal boxes at the same
temperature and pressure hold helium, nitrogen and carbon dioxide. Their
molecules move at speeds in the ratio sqrt(M_ref / M) (helium fastest, CO2
slowest) because each carries the same average kinetic energy; each gauge
reads the same pressure, and each box holds the same number of molecules.
Avogadro's statement follows, with the count per litre at 1 bar and 300 K
(2.4e22) and the molar volume at 273.15 K: 22.71 L at 1 bar, 22.41 L at 1 atm.
"""

from manim_scenes.common import *

V = pm.AVOGADRO
GASES = (("He", cfg.HE_COLOR, pm.MOLAR_MASS["He"]), ("N₂", cfg.N2_COLOR, pm.MOLAR_MASS["N2"]),
         ("CO₂", cfg.CO2_COLOR, pm.MOLAR_MASS["CO2"]))
COUNT = 40
BASE_SPEED = 1.1        # rms speed of N2 on screen (stage units per second)


class Scene24EqualVolumes(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "24", "Equal volumes, equal numbers")
    boxes, names, gauges = [], VGroup(), VGroup()
    for k, (name, color, molar) in enumerate(GASES):
        x = -4.6 + 4.6 * k
        speed = BASE_SPEED * float(np.sqrt(pm.MOLAR_MASS["N2"] / molar))
        box = GasBox((x, -0.1, 0), count=COUNT, seed=cfg.SEED + 24 + k, half_x=1.05, half_z=0.85, height=2.0, floor=-1.0,
                     colors=(color,), radius=0.09, zoom=0.95, yaw=-0.5, pitch=0.3, speed=speed, spark_axes=(1,), spark_sides=(1,))
        boxes.append(box)
        names.add(txt(name, cfg.FONT["section"], color).move_to([x, 2.3, 0]))
        gauges.add(Gauge(box.pressure, [x, -2.65, 0], top=2.0, radius=0.55, step=0.5, label_every=1.0))
    founder = txt(f"Amedeo Avogadro, {gd.YEAR_AVOGADRO}", cfg.FONT["label"], cfg.GOLD).move_to([0, -2.9, 0])
    scene.play(FadeIn(founder), run_time=1.0)

    # --- 2. Three gases, same V, T and P ------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    for box, name in zip(boxes, names):
        show(scene, box.stage, 0.7, FadeIn(name))
    same = txt("same V · same T · same P", cfg.FONT["label"], cfg.WHITE).move_to([0, 3.35, 0])
    scene.play(FadeOut(founder), FadeIn(same), run_time=1.0)
    scene.play(FadeIn(gauges), run_time=1.0)
    scene.wait(3.5)

    # --- 3. Light and fast, heavy and slow: the same average kinetic energy ----------------------------------------------------------
    beat(scene, t, 2)
    speeds = VGroup(txt("light, fast", cfg.FONT["small"], cfg.HE_COLOR).move_to([-4.6, 1.6, 0]),
                    txt("heavy, slow", cfg.FONT["small"], cfg.CO2_COLOR).move_to([4.6, 1.6, 0]))
    scene.play(FadeIn(speeds), run_time=1.0)
    scene.wait(3.0)
    energy = eq(r"\text{same } \langle K\rangle = \tfrac{3}{2}k_BT", cfg.FONT["body"], cfg.GOLD).move_to([0, 3.35, 0])
    scene.play(fade_through(same, energy), run_time=1.2)
    scene.wait(3.0)

    # --- 4. Each molecule pushes as hard on average: equal P means equal N ------------------------------------------------------------
    beat(scene, t, 3)
    counts = VGroup(*[txt(f"N = {box.cloud.active_count()}", cfg.FONT["label"], cfg.WHITE).move_to([box.stage.center_point()[0], 1.6, 0])
                      for box in boxes])
    scene.play(FadeOut(speeds), run_time=0.5)
    scene.play(LaggedStart(*[FadeIn(c, scale=1.2) for c in counts], lag_ratio=0.3), run_time=1.6)
    scene.play(*[Indicate(g.readout, color=cfg.PRESSURE) for g in gauges], run_time=1.4)

    # --- 5. Avogadro's statement ----------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    statement = VGroup(txt("equal volumes, same T and P", cfg.FONT["label"], cfg.WHITE),
                       txt("→ equal numbers of molecules", cfg.FONT["label"], cfg.GOLD)).arrange(DOWN, buff=0.22)
    statement = boxed(statement, cfg.GOLD).move_to([0, 3.1, 0])
    scene.play(FadeOut(energy), FadeOut(names), run_time=0.5)
    scene.play(FadeIn(statement, scale=0.95), run_time=0.8)
    scene.wait(3.0)

    # --- 6. How many? 2.4e22 per litre at 1 bar, 300 K ---------------------------------------------------------------------------------
    beat(scene, t, 5)
    per_litre = eq(rf"\approx {sci(pm.AIR.molecules_per_cm3 * 1000, 1)}\ \text{{molecules per litre}}", cfg.FONT["body"], cfg.CYAN)
    fit_width(per_litre, 12.0)
    per_litre.move_to([0, 1.6, 0])
    scene.play(FadeOut(counts), run_time=0.4)
    scene.play(FadeIn(per_litre, shift=UP * 0.1), run_time=0.8)
    scene.wait(3.0)

    # --- 7. Molar volume: 22.71 L at 273.15 K and 1 bar -----------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(*[box.stage.fade(box.stage, 0.0) for box in boxes], FadeOut(VGroup(gauges, per_litre, statement)), run_time=1.0)
    for box in boxes:
        scene.remove(box.stage)
    cube = GasBox((-3.2, -0.6, 0), count=90, seed=cfg.SEED + 240, half_x=1.5, half_z=1.5, height=3.0, floor=-1.5, zoom=0.95,
                  yaw=-0.6, pitch=0.35, speed=1.3)
    show(scene, cube.stage, 1.0)
    molar = VGroup(eq(r"1\ \text{mol}", cfg.FONT["section"], cfg.AMOUNT),
                   eq(rf"V_m = {fx(V.per_bar, 2)}\ \mathrm{{L\,mol^{{-1}}}}", cfg.FONT["section"], cfg.GOLD),
                   txt(f"{fx(pm.T_ICE, 2)} K, 1 bar", cfg.FONT["label"], cfg.MUTED)).arrange(DOWN, buff=0.35).move_to([3.4, 0.6, 0])
    scene.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.2) for m in molar], lag_ratio=0.4), run_time=2.2)
    any_gas = txt("any ideal gas", cfg.FONT["label"], cfg.WHITE).next_to(molar, DOWN, buff=0.45)
    scene.play(FadeIn(any_gas), run_time=0.8)

    # --- 8. 22.4 L belongs to 1 atm ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    atm = VGroup(eq(rf"{fx(V.per_atm, 1)}\ \mathrm{{L}}", cfg.FONT["body"], cfg.LIMIT),
                 txt(f"at 1 atm = {fx(pm.SEA_LEVEL_BAR, 3)} bar", cfg.FONT["small"], cfg.LIMIT)).arrange(RIGHT, buff=0.3)
    atm.move_to([3.4, -2.7, 0])
    scene.play(FadeOut(any_gas), FadeIn(atm, shift=UP * 0.1), run_time=1.2)
    finish(scene, t, cube.stage)
