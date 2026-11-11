"""Scene 27 — weighing a gas. Writing n = m / M turns PV = nRT into
rho = PM / RT: at the same pressure and temperature, density follows molar
mass. Two equal boxes of nitrogen and helium (same number of molecules,
helium's moving faster) have densities of 1.12 and 0.160 g/L at 1 bar and
300 K, a ratio of 7; a helium balloon rises. Reversed, a measured density
gives the molar mass: 1.12 g/L -> 28 g/mol, nitrogen. The model's two
assumptions are named in purple: no size, no attractions.
"""

from manim_scenes.common import *
from manim_scenes.scene_01_hook import balloon

D = pm.DENSITY


class Scene27Density(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "27", "Weighing a gas")
    scale = VGroup(Triangle(stroke_color=cfg.STEEL, stroke_width=3, fill_color=cfg.PANEL, fill_opacity=1).scale(0.5),
                   Line(LEFT * 2.2, RIGHT * 2.2, stroke_color=cfg.STEEL, stroke_width=6).shift(UP * 0.45))
    scale.move_to([0, -2.6, 0])
    scene.play(FadeIn(scale), run_time=1.0)

    # --- 2. n = m/M: rho = PM/RT -----------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    lines = VGroup(eq(r"n = \frac{m}{M}", cfg.FONT["body"], cfg.AMOUNT),
                   eq(r"PV = \frac{m}{M}\,RT", cfg.FONT["body"], cfg.WHITE),
                   eq(r"\rho = \frac{m}{V} = \frac{PM}{RT}", cfg.FONT["section"], cfg.GOLD)).arrange(DOWN, buff=0.45).move_to([0, 0.9, 0])
    for line in lines:
        scene.play(FadeIn(line, shift=DOWN * 0.15), run_time=1.3)
        scene.wait(2.0)
    frame = glow_frame(lines[2], cfg.GOLD)
    scene.play(Create(frame), run_time=1.0)

    # --- 3. Same P and T: density proportional to M -------------------------------------------------------------------------------
    beat(scene, t, 2)
    prop = eq(r"\rho \propto M\quad(\text{same } P, T)", cfg.FONT["body"], cfg.GOLD).move_to([0, 3.3, 0])
    scene.play(FadeOut(VGroup(lines, scale, frame)), run_time=0.5)
    scene.play(FadeIn(prop), run_time=0.6)

    # --- 4. Nitrogen 1.12 g/L, helium 0.160 g/L: seven times lighter ------------------------------------------------------------------
    beat(scene, t, 3)
    n2 = GasBox((-4.4, -0.4, 0), count=50, seed=cfg.SEED + 27, half_x=1.15, half_z=0.9, height=2.1, floor=-1.05, colors=(cfg.N2_COLOR,),
                radius=0.1, zoom=0.95, yaw=-0.5, pitch=0.3, speed=1.0)
    he = GasBox((-0.6, -0.4, 0), count=50, seed=cfg.SEED + 28, half_x=1.15, half_z=0.9, height=2.1, floor=-1.05, colors=(cfg.HE_COLOR,),
                radius=0.07, zoom=0.95, yaw=-0.5, pitch=0.3, speed=1.0 * float(np.sqrt(pm.MOLAR_MASS["N2"] / pm.MOLAR_MASS["He"])))
    tags = VGroup(txt("N₂", cfg.FONT["section"], cfg.N2_COLOR).move_to([-4.4, 2.3, 0]), txt("He", cfg.FONT["section"], cfg.HE_COLOR).move_to([-0.6, 2.3, 0]))
    show(scene, n2.stage, 0.7, FadeIn(tags[0]))
    show(scene, he.stage, 0.7, FadeIn(tags[1]))
    chart = bar_chart([D.nitrogen, D.helium], ["N₂", "He"], [cfg.N2_COLOR, cfg.HE_COLOR], at=[4.4, -0.6, 0], width=3.8, height=3.4,
                      value_labels=[f"{fx(D.nitrogen, 2)} g/L", f"{fx(D.helium, 3)} g/L"], bar_width=1.1)
    scene.play(Create(chart.base), FadeIn(chart.names), run_time=0.8)
    scene.play(GrowFromEdge(chart.bars[0], DOWN), FadeIn(chart.tops[0]), run_time=1.2)
    scene.play(GrowFromEdge(chart.bars[1], DOWN), FadeIn(chart.tops[1]), run_time=1.2)
    seven = txt(f"density N₂ / He ≈ {fx(D.ratio, 0)}", cfg.FONT["label"], cfg.GOLD).move_to([4.4, 2.25, 0])
    scene.play(FadeIn(seven, scale=1.1), run_time=0.9)
    bal = balloon([6.8, -0.3, 0], radius=0.42, color=cfg.HE_COLOR)
    bal.scale(0.9)
    bal.keep_in_frame = True
    scene.play(FadeIn(bal), run_time=0.6)
    scene.play(bal.animate.shift(UP * 0.6), run_time=2.4)

    # --- 5. Reverse it: M = rho RT / P -> 28 g/mol, nitrogen ---------------------------------------------------------------------------
    beat(scene, t, 4)
    hide(scene, he.stage, 0.6, FadeOut(VGroup(tags, bal)))
    hide(scene, n2.stage, 0.6, FadeOut(VGroup(chart, seven)))
    rho = round(D.nitrogen, 2)
    molar = pm.molar_mass_from_density(rho, pm.BAR, pm.ROOM_T)
    reverse = VGroup(eq(r"M = \frac{\rho R T}{P}", cfg.FONT["section"], cfg.WHITE),
                     eq(rf"= \frac{{{fx(rho, 2)} \times {fx(pm.R_L_BAR, 5)} \times {fx(pm.ROOM_T, 0)}}}{{{fx(1.0, 0)}}}", cfg.FONT["body"], cfg.WHITE),
                     eq(rf"\approx {fx(molar, 0)}\ \mathrm{{g/mol}}", cfg.FONT["section"], cfg.GOLD)).arrange(DOWN, buff=0.4).move_to([-1.0, -0.2, 0])
    scene.play(Write(reverse[0]), run_time=1.4)
    scene.play(FadeIn(reverse[1], shift=DOWN * 0.1), run_time=1.4)
    scene.play(FadeIn(reverse[2], shift=DOWN * 0.1), run_time=1.2)
    nitrogen = result_label("nitrogen", cfg.N2_COLOR, cfg.FONT["section"]).move_to([4.4, -1.6, 0])
    scene.play(FadeIn(nitrogen, scale=0.95), run_time=1.0)

    # --- 6. The assumptions: no size, no attractions ------------------------------------------------------------------------------------
    beat(scene, t, 5)
    assume = VGroup(chip("negligible size", cfg.LIMIT), chip("no attractions", cfg.LIMIT)).arrange(RIGHT, buff=0.4).move_to([0, -2.9, 0])
    scene.play(LaggedStart(*[FadeIn(a, shift=UP * 0.15) for a in assume], lag_ratio=0.4), run_time=1.4)
    finish(scene, t, fill=lambda s: [Indicate(assume, color=cfg.WHITE, scale_factor=1.04)])
