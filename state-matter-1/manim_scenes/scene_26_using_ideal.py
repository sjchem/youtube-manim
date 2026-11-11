"""Scene 26 — using PV = nRT. R = 8.314 J/(mol K) is Avogadro's number
times the Boltzmann constant (the same constant inside the kinetic theory);
in litre-bar units R = 0.08314. One mole at 300 K and 1 bar fills 24.94 L,
a cube about 29 cm on a side (3D box). For a fixed amount the combined law
P1V1/T1 = P2V2/T2 follows; a weather balloon (2 L, 1 bar, 300 K) rises to
0.5 bar and 250 K: halving P doubles V to 4 L, cooling takes a sixth off,
3.33 L. Every number comes from ``physics_models``.
"""

from manim_scenes.common import *
from manim_scenes.scene_01_hook import balloon

K, I = pm.COMBINED, pm.IDEAL


class Scene26UsingIdeal(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "26", "Using PV = nRT")
    r_si = eq(rf"R = {fx(pm.R, 3)}\ \mathrm{{J\,mol^{{-1}}\,K^{{-1}}}}", cfg.FONT["section"], cfg.WHITE).move_to([0, 1.8, 0])
    scene.play(Write(r_si), run_time=2.0)
    universal = txt("the universal gas constant", cfg.FONT["label"], cfg.GOLD).next_to(r_si, DOWN, buff=0.4)
    scene.play(FadeIn(universal), run_time=0.9)

    # --- 2. R = N_A k_B -------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    product = eq(rf"R = N_A\,k_B = ({sci(pm.N_A, 3)})({sci(pm.K_B, 3)})", cfg.FONT["body"], cfg.WHITE).move_to([0, -0.4, 0])
    fit_width(product, 12.6)
    scene.play(FadeOut(universal), Write(product), run_time=2.0)
    same = txt("the constant inside the kinetic theory", cfg.FONT["small"], cfg.MUTED).next_to(product, DOWN, buff=0.35)
    scene.play(FadeIn(same), run_time=0.8)

    # --- 3. In litres and bar: 0.08314 ---------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    r_lbar = eq(rf"R = {fx(pm.R_L_BAR, 5)}\ \mathrm{{L\,bar\,mol^{{-1}}\,K^{{-1}}}}", cfg.FONT["section"], cfg.GOLD).move_to([0, -2.6, 0])
    fit_width(r_lbar, 12.6)
    scene.play(FadeIn(r_lbar, shift=UP * 0.15), run_time=1.2)
    scene.wait(2.5)

    # --- 4. One mole at 300 K, 1 bar: 24.94 L, a 29 cm cube -------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(r_si, product, same)), r_lbar.animate.scale(0.62).move_to([-3.6, 3.3, 0]), run_time=1.0)
    side_cm = pm.cube_side_cm(I.V)
    cube = GasBox((-3.4, -0.6, 0), count=110, seed=cfg.SEED + 26, half_x=1.55, half_z=1.55, height=3.1, floor=-1.55, zoom=1.0,
                  yaw=-0.6, pitch=0.33, speed=1.3)
    ch = cube.chamber
    edge = Tag(txt(f"≈ {fx(side_cm, 0)} cm", cfg.FONT["label"], cfg.VOLUME), ch.corner(-1, 0, 1) + np.array([ch.half_x, -0.45, 0.0]))
    cube.stage.add_overlay(edge)
    show(scene, cube.stage, 1.0)
    numbers = VGroup(eq(rf"n = {fx(I.n, 0)}\ \mathrm{{mol}}", cfg.FONT["body"], cfg.AMOUNT),
                     eq(rf"T = {fx(I.T, 0)}\ \mathrm{{K}},\ P = {fx(I.P, 0)}\ \mathrm{{bar}}", cfg.FONT["body"], cfg.WHITE),
                     eq(rf"V = \frac{{nRT}}{{P}} \approx {fx(I.V, 2)}\ \mathrm{{L}}", cfg.FONT["body"], cfg.GOLD))
    numbers.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.4, 0.2, 0])
    scene.play(LaggedStart(*[FadeIn(n, shift=LEFT * 0.2) for n in numbers], lag_ratio=0.45), run_time=2.6)

    # --- 5. Fixed amount between two states: the combined gas law ------------------------------------------------------------------
    beat(scene, t, 4)
    combined = boxed(paint(eq([r"\frac{P_1V_1}{T_1}", "=", r"\frac{P_2V_2}{T_2}"], cfg.FONT["section"]), {0: cfg.WHITE, 2: cfg.WHITE}), cfg.GOLD)
    combined.move_to([3.4, 0.2, 0])
    fixed = txt("fixed amount: nR constant", cfg.FONT["small"], cfg.AMOUNT).next_to(combined, DOWN, buff=0.4)
    hide(scene, cube.stage, 0.8, FadeOut(numbers))
    scene.play(FadeIn(combined, scale=0.95), FadeIn(fixed), run_time=1.4)
    scene.wait(3.0)

    # --- 6. A weather balloon: 2 L, 1 bar, 300 K -> 0.5 bar, 250 K ------------------------------------------------------------------------
    beat(scene, t, 5)
    ground_y = -3.2
    sky = Line([-7.0, ground_y, 0], [-2.0, ground_y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    bal = balloon([-4.5, ground_y + 2.2, 0], radius=0.75, color=cfg.ROSE)
    low = VGroup(eq(rf"P_1 = {fx(K.P1, 0)}\ \mathrm{{bar}},\ T_1 = {fx(K.T1, 0)}\ \mathrm{{K}}", cfg.FONT["small"], cfg.WHITE),
                 eq(rf"V_1 = {fx(K.V1, 0)}\ \mathrm{{L}}", cfg.FONT["small"], cfg.VOLUME)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    low.next_to([-2.8, -1.4, 0], RIGHT, buff=0)
    high = VGroup(eq(rf"P_2 = {fx(K.P2, 1)}\ \mathrm{{bar}},\ T_2 = {fx(K.T2, 0)}\ \mathrm{{K}}", cfg.FONT["small"], cfg.WHITE),
                  eq(r"V_2 = \ ?", cfg.FONT["small"], cfg.GOLD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    high.next_to([-2.8, 1.9, 0], RIGHT, buff=0)
    scene.play(FadeOut(fixed), FadeOut(r_lbar), combined.animate.scale(0.7).move_to([4.6, 3.0, 0]), run_time=0.7)
    scene.play(Create(sky), FadeIn(bal), FadeIn(low), run_time=0.8)
    scene.play(bal.animate.shift(UP * 3.1), FadeOut(low), run_time=3.0)
    scene.play(FadeIn(high, shift=DOWN * 0.1), run_time=1.0)
    countdown(scene, [4.6, -0.6, 0], 3)

    # --- 7. Halve P: 4 L; cool by a sixth: 3.33 L ---------------------------------------------------------------------------------------
    beat(scene, t, 6)
    doubled = K.V1 * K.P1 / K.P2
    steps = VGroup(eq(rf"{fx(K.V1, 0)}\ \mathrm{{L}} \times \frac{{{fx(K.P1, 0)}}}{{{fx(K.P2, 1)}}} = {fx(doubled, 0)}\ \mathrm{{L}}",
                      cfg.FONT["body"], cfg.PRESSURE),
                   eq(rf"{fx(doubled, 0)}\ \mathrm{{L}} \times \frac{{{fx(K.T2, 0)}}}{{{fx(K.T1, 0)}}} \approx {fx(K.V2, 2)}\ \mathrm{{L}}",
                      cfg.FONT["body"], cfg.TEMPERATURE)).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([3.6, -0.9, 0])
    grow = (doubled / K.V1) ** (1 / 3)
    shrink = (K.V2 / doubled) ** (1 / 3)
    scene.play(FadeIn(steps[0], shift=LEFT * 0.2), bal.animate.scale(grow), run_time=2.0)
    scene.wait(1.5)
    scene.play(FadeIn(steps[1], shift=LEFT * 0.2), bal.animate.scale(shrink), run_time=2.0)
    answer = eq(rf"V_2 \approx {fx(K.V2, 2)}\ \mathrm{{L}}", cfg.FONT["small"], cfg.GOLD).move_to(high[1])
    scene.play(fade_through(high[1], answer), Create(glow_frame(steps[1], cfg.GOLD)), run_time=1.2)
    finish(scene, t, fill=lambda s: [bal.animate.shift(UP * 0.15)])
