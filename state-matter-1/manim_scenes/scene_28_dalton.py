"""Scene 28 — Dalton's law. One box holds two ideal gases: 100 blue nitrogen
and 50 rose oxygen molecules (2 mol : 1 mol, oxygen slightly slower). Each
species strikes the walls independently; per-species hit counters measure
it, and each partial pressure is what that gas alone would exert. Stacked
bars add to the total: P_total = P_A + P_B = sum P_i, P_i = n_i RT / V =
x_i P_total. Worked example: 3 bar total gives 2 bar and 1 bar. Back to the
mountain: oxygen is 21 % of air, 0.21 bar at sea level, 0.07 bar on Everest.
"""

from manim_scenes.common import *

X, M = pm.DALTON, pm.MOUNTAIN
N_A, N_B = 100, 50


class Scene28Dalton(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "28", "Mixtures of gases")
    species = np.array([0] * N_A + [1] * N_B)
    box = GasBox((-4.3, -0.7, 0), count=N_A + N_B, seed=cfg.SEED + 28, species=species,
                 masses=(pm.MOLAR_MASS["N2"], pm.MOLAR_MASS["O2"]), colors=(cfg.N2_COLOR, cfg.O2_COLOR), half_x=1.45,
                 half_z=1.1, height=2.9, floor=-1.45, zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.6, p_ref=X.P_total)
    legend = VGroup(txt("N₂", cfg.FONT["label"], cfg.N2_COLOR), txt("O₂", cfg.FONT["label"], cfg.O2_COLOR)).arrange(RIGHT, buff=0.6)
    legend.move_to([-4.3, 3.2, 0])
    show(scene, box.stage, 1.0, FadeIn(legend))
    air = txt("air: mostly N₂ and O₂", cfg.FONT["label"], cfg.WHITE).move_to([3.4, 2.6, 0])
    scene.play(FadeIn(air), run_time=0.9)

    # --- 2. How does each contribute? ---------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    ask = txt("who pushes how much?", cfg.FONT["label"], cfg.GOLD).move_to([3.4, 2.6, 0])
    scene.play(fade_through(air, ask), run_time=1.0)

    # --- 3. Ideal: each gas strikes as if alone (measured hits per species) -------------------------------------------------------------
    beat(scene, t, 2)
    alone = txt("each strikes as if alone", cfg.FONT["label"], cfg.WHITE).move_to([3.4, 2.6, 0])
    rates = [Knob(box.cloud.hit_rate(2.0, species=s)) for s in (0, 1)]
    counters = VGroup()
    for s, color, name in ((0, cfg.N2_COLOR, "N₂ hits/s"), (1, cfg.O2_COLOR, "O₂ hits/s")):
        label = txt(name, cfg.FONT["small"], color)
        number = Integer(int(round(rates[s].value)), font_size=48, color=color)
        counters.add(VGroup(label, number).arrange(RIGHT, buff=0.3))
    counters.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.0, 1.0, 0])
    scene.play(fade_through(ask, alone), FadeIn(counters), run_time=1.2)
    for s in (0, 1):
        def follow(m, dt, s=s):
            rates[s].value += (box.cloud.hit_rate(2.0, species=s) - rates[s].value) * (1 - np.exp(-dt / 0.5))
            m.set_value(int(round(rates[s].value)))
        counters[s][1].add_updater(follow)
    scene.wait(5.0)

    # --- 4. Total push = sum of pushes: stacked bars ----------------------------------------------------------------------------------
    beat(scene, t, 3)
    base = np.array([5.6, -2.9, 0])
    unit = 1.25                                   # screen units per bar
    bar_a = Rectangle(width=1.0, height=X.P_a * unit, stroke_width=2, stroke_color=cfg.N2_COLOR, fill_color=cfg.N2_COLOR,
                      fill_opacity=0.85).move_to(base + UP * X.P_a * unit / 2)
    bar_b = Rectangle(width=1.0, height=X.P_b * unit, stroke_width=2, stroke_color=cfg.O2_COLOR, fill_color=cfg.O2_COLOR,
                      fill_opacity=0.85).next_to(bar_a, UP, buff=0)
    total_line = DashedLine(bar_b.get_corner(UL) + LEFT * 0.4, bar_b.get_corner(UR) + RIGHT * 0.4, stroke_color=cfg.WHITE, stroke_width=3)
    total_tag = eq(r"P_{\text{total}}", cfg.FONT["small"], cfg.WHITE).next_to(total_line, UP, buff=0.12)
    for c in counters:
        c[1].clear_updaters()            # freeze the digits before fading (a changing digit count breaks FadeOut)
    scene.play(FadeOut(counters), GrowFromEdge(bar_a, DOWN), run_time=1.2)
    scene.play(GrowFromEdge(bar_b, DOWN), run_time=1.0)
    scene.play(Create(total_line), FadeIn(total_tag), run_time=0.8)

    # --- 5. P_total = P_A + P_B = sum P_i --------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    law = paint(eq([r"P_{\text{total}}", "=", r"P_A", "+", r"P_B"], cfg.FONT["section"]), {2: cfg.N2_COLOR, 4: cfg.O2_COLOR})
    law.move_to([1.6, 2.65, 0])
    general = eq(r"= \sum_i P_i", cfg.FONT["body"], cfg.WHITE).next_to(law, RIGHT, buff=0.3)
    scene.play(fade_through(alone, law), run_time=1.4)
    scene.play(FadeIn(general, shift=DOWN * 0.1), run_time=1.0)

    # --- 6. Each partial pressure: n_i RT / V -------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    each = eq(r"P_i = \frac{n_i R T}{V}", cfg.FONT["body"], cfg.WHITE).move_to([1.8, 1.25, 0])
    scene.play(FadeIn(each, shift=UP * 0.1), run_time=1.2)
    scene.wait(2.0)

    # --- 7. Mole fraction: P_i = x_i P_total ----------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    frac = VGroup(eq(r"x_i = \frac{n_i}{n_{\text{total}}}", cfg.FONT["body"], cfg.AMOUNT),
                  eq(r"P_i = x_i\,P_{\text{total}}", cfg.FONT["section"], cfg.GOLD)).arrange(DOWN, buff=0.4).move_to([1.8, -1.0, 0])
    scene.play(FadeIn(frac[0], shift=UP * 0.1), run_time=1.2)
    scene.play(FadeIn(frac[1], shift=UP * 0.1), run_time=1.2)
    frac_frame = glow_frame(frac[1], cfg.GOLD)
    scene.play(Create(frac_frame), run_time=0.9)

    # --- 8. Example: 2 mol N2 + 1 mol O2 at 3 bar ---------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(law, general, each, frac, frac_frame)), run_time=0.8)
    example = VGroup(eq(rf"n_{{N_2}} = {fx(X.n_a, 0)}\ \mathrm{{mol}},\ n_{{O_2}} = {fx(X.n_b, 0)}\ \mathrm{{mol}}", cfg.FONT["body"], cfg.WHITE),
                     eq(rf"P_{{\text{{total}}}} = {fx(X.P_total, 0)}\ \mathrm{{bar}}", cfg.FONT["body"], cfg.WHITE)).arrange(DOWN, buff=0.35)
    example.move_to([1.8, 2.3, 0])
    gauge = Gauge(box.pressure, [1.8, -1.0, 0], top=4.0, radius=0.95, step=0.5)
    scene.play(FadeIn(example, shift=DOWN * 0.1), FadeIn(gauge), run_time=1.2)

    # --- 9. x = 2/3 and 1/3: 2 bar and 1 bar ------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    answer = VGroup(eq(rf"x_{{N_2}} = \tfrac{{2}}{{3}} \Rightarrow {fx(X.P_a, 0)}\ \mathrm{{bar}}", cfg.FONT["body"], cfg.N2_COLOR),
                    eq(rf"x_{{O_2}} = \tfrac{{1}}{{3}} \Rightarrow {fx(X.P_b, 0)}\ \mathrm{{bar}}", cfg.FONT["body"], cfg.O2_COLOR))
    answer.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([1.8, 0.25, 0])
    tags = VGroup(txt(f"{fx(X.P_a, 0)} bar", cfg.FONT["small"], cfg.WHITE).move_to(bar_a),
                  txt(f"{fx(X.P_b, 0)} bar", cfg.FONT["small"], cfg.WHITE).move_to(bar_b))
    scene.play(FadeOut(gauge), run_time=0.4)
    scene.play(FadeIn(answer[0], shift=LEFT * 0.2), FadeIn(tags[0]), run_time=0.8)
    scene.play(FadeIn(answer[1], shift=LEFT * 0.2), FadeIn(tags[1]), run_time=1.2)

    # --- 10. Back to the mountain: O2 0.21 bar at sea level, 0.07 bar on Everest -------------------------------------------------------------
    beat(scene, t, 9)
    hide(scene, box.stage, 0.8, FadeOut(VGroup(legend, example, answer, bar_a, bar_b, tags, total_line, total_tag)))
    o2 = bar_chart([M.oxygen_sea_level, M.oxygen_summit], ["sea level", "Everest"], [cfg.O2_COLOR, cfg.O2_COLOR], at=[-3.4, -0.6, 0],
                   width=5.4, height=3.6, value_labels=[f"{fx(M.oxygen_sea_level, 2)} bar", f"{fx(M.oxygen_summit, 2)} bar"], bar_width=1.4)
    title = eq(rf"P_{{O_2}} = {fx(pm.AIR_FRACTION['O2'], 2)} \times P_{{\text{{air}}}}", cfg.FONT["body"], cfg.O2_COLOR).move_to([3.4, 1.6, 0])
    share = txt(f"O₂ ≈ {fx(100 * pm.AIR_FRACTION['O2'], 0)} % of air", cfg.FONT["label"], cfg.WHITE).move_to([3.4, 2.7, 0])
    scene.play(FadeIn(share), FadeIn(title), run_time=1.2)
    scene.play(Create(o2.base), FadeIn(o2.names), run_time=0.8)
    scene.play(GrowFromEdge(o2.bars[0], DOWN), FadeIn(o2.tops[0]), run_time=1.2)
    scene.play(GrowFromEdge(o2.bars[1], DOWN), FadeIn(o2.tops[1]), run_time=1.2)

    # --- 11. Same collisions, Boyle and Dalton -------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    same = result_label("same collisions, same physics", cfg.GOLD, cfg.FONT["body"]).move_to([3.7, -1.6, 0])
    fit_width(same, 6.8)
    scene.play(FadeIn(same, scale=0.95), run_time=1.0)
    finish(scene, t, fill=lambda s: [Indicate(o2.bars[1], color=cfg.WHITE, scale_factor=1.03)])
