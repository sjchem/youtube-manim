"""Scene 15 — the van der Waals equation. PV = nRT stands alone; its P opens
into (P + an²/V²), the attraction correction in green, and its V into
(V − nb), the size correction in red. The result is boxed in gold.

Then a test, every number from ``pm.FLASK``: one mole of carbon dioxide in a
one-litre glass flask at 300 K (molecules fly inside a translucent sphere on a
turning stage). A pressure column reads the ideal prediction, about 24.9 bar;
correcting for size lifts it to about 26.1 bar (a red step); correcting for
attraction takes about 3.6 bar away (a green step), leaving about 22.4 bar,
ten percent below ideal. Given a hundred litres, both corrections shrink (the
green and red terms fade with them) and a live ratio of van der Waals to ideal
pressure climbs from 0.90 to 1.00: the equation becomes the ideal gas
equation. The closing beat labels the two physical ideas under their terms.
"""

from manim_scenes.common import *
from manim_scenes.kit_c import SphereGas, word_cue

F = pm.FLASK
A_CO2, B_CO2 = pm.VDW[F.gas]
STAGE_AT = (-4.1, -0.75, 0.0)
BAR_X = 3.6
BAR_BASE = -3.0
BAR_H = 4.6
P_LOW, P_HIGH = 15.0, 30.0       # the column's axis is broken: it starts at 15 bar (marked with a break)


class Scene15VdwEquation(Scene):
    def construct(self) -> None:
        play_scene(self)


def p_to_y(p: float) -> float:
    return BAR_BASE + 0.25 + max(p - P_LOW, 0.0) / (P_HIGH - P_LOW) * (BAR_H - 0.25)


def ratio_at(volume: float) -> float:
    return pm.vdw_pressure(F.n, volume, F.T, A_CO2, B_CO2) / pm.ideal_pressure(F.n, volume, F.T)


def vdw_tex(size: int) -> MathTex:
    tex = eq(["(", "P", "+", r"\frac{an^2}{V^2}", ")", "(", "V", "-", "nb", ")", "=", "nRT"], size)
    return paint(tex, {1: cfg.PRESSURE, 3: cfg.ATTRACT, 6: cfg.VOLUME, 8: cfg.SIZE})


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "15", TITLES["15"])

    # --- 0. The ideal gas equation ----------------------------------------------------------------------------------------
    law = paint(eq(["P", "V", "=", "nRT"], cfg.FONT["hero"]), {0: cfg.PRESSURE, 1: cfg.VOLUME})
    law.move_to([0, 0.6, 0])
    play_in(scene, t, 1, Write(law), run_time=1.6)

    # --- 1. Replace P and V -------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    vdw = vdw_tex(cfg.FONT["hero"])
    if vdw.width > 14.4:
        vdw.scale_to_fit_width(14.4)
    vdw.move_to([0, 0.6, 0])
    word_cue(scene, t, 1, "pressure", lead=0.2)
    scene.play(ReplacementTransform(law[0], vdw[1]), FadeIn(vdw[0]), FadeIn(vdw[2:5], shift=LEFT * 0.2),
               ReplacementTransform(law[1], vdw[6]), ReplacementTransform(law[2], vdw[10]), ReplacementTransform(law[3], vdw[11]),
               run_time=1.8)
    attract_tag = txt("attraction", cfg.FONT["label"], cfg.ATTRACT).next_to(vdw[3], DOWN, buff=0.35)
    scene.play(FadeIn(attract_tag, shift=UP * 0.1), Indicate(vdw[3], color=cfg.WHITE, scale_factor=1.12), run_time=1.0)
    word_cue(scene, t, 1, "volume", lead=0.2)
    scene.play(FadeIn(vdw[5]), FadeIn(vdw[7:10], shift=LEFT * 0.2), run_time=1.2)
    size_tag = txt("size", cfg.FONT["label"], cfg.SIZE).next_to(vdw[8], DOWN, buff=0.35)
    play_in(scene, t, 2, FadeIn(size_tag, shift=UP * 0.1), Indicate(vdw[8], color=cfg.WHITE, scale_factor=1.15), run_time=1.0)

    # --- 2. The van der Waals equation ----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    framed = glow_frame(vdw, cfg.GOLD, buff=0.3)
    name = result_label("the van der Waals equation", cfg.GOLD, cfg.FONT["section"]).move_to([0, 2.6, 0])
    scene.play(Create(framed), FadeOut(attract_tag), FadeOut(size_tag), run_time=1.4)
    scene.play(FadeIn(name, shift=DOWN * 0.15), run_time=1.0)
    word_cue(scene, t, 2, "times", lead=0.2)
    scene.play(Indicate(vdw[0:5], color=cfg.WHITE, scale_factor=1.05), run_time=1.2)
    word_cue(scene, t, 2, "equals", lead=0.2)
    play_in(scene, t, 3, Indicate(vdw[5:10], color=cfg.WHITE, scale_factor=1.05), run_time=1.2)

    # --- 3. The test flask: the ideal prediction ---------------------------------------------------------------------------------
    beat(scene, t, 3)
    top_eq = VGroup(vdw, framed)
    scene.play(FadeOut(name), run_time=0.4)
    scene.play(top_eq.animate.scale(0.62).move_to([0.9, 2.85, 0]), run_time=0.8)
    stage = Stage(STAGE_AT, zoom=1.25, yaw=-0.4, pitch=0.25, sway=0.04)
    volume = Knob(F.V)

    def radius() -> float:
        return 1.45 + 0.5 * float(np.log10(volume.value))

    flask = glass_sphere(stage, np.zeros(3), radius, cfg.GLASS, fill_opacity=0.08, ring_opacity=0.22, rim_opacity=0.8)
    gas = SphereGas(46, cfg.SEED + 150, radius, speed=1.2, size=0.09)
    stage.add_body(Ticker(lambda: gas.step(stage.clock)))
    stage.add_body(Dots(gas.points, cfg.GAS_COLORS["CO2"], radius=0.085))
    show(scene, stage, 1.0)
    vol_tag = live(VGroup(), lambda: txt(f"{fx(volume.value, 0)} L", cfg.FONT["section"], cfg.VOLUME)
                   .move_to([STAGE_AT[0], -3.45, 0]))
    facts = chip(f"1 mol CO₂ · {fx(F.T, 0)} K", cfg.GAS_COLORS["CO2"], cfg.FONT["small"]).move_to([STAGE_AT[0], 1.5, 0])
    scene.play(FadeIn(facts, shift=DOWN * 0.1), FadeIn(vol_tag), run_time=1.0)

    level = Knob(0.0)
    ground = Line([BAR_X - 1.0, BAR_BASE, 0], [BAR_X + 1.0, BAR_BASE, 0], stroke_color=cfg.MUTED, stroke_width=3)
    column = live(VGroup(), lambda: Rectangle(width=1.1, height=max(p_to_y(level.value) - BAR_BASE, 0.02), stroke_width=2,
                                               stroke_color=cfg.PRESSURE, fill_color=cfg.PRESSURE, fill_opacity=0.7)
                  .move_to([BAR_X, (p_to_y(level.value) + BAR_BASE) / 2, 0]))
    reading = live(VGroup(), lambda: txt(f"{fx(level.value, 1)} bar", cfg.FONT["section"], cfg.WHITE)
                   .next_to([BAR_X + 0.75, p_to_y(level.value), 0], RIGHT, buff=0.15))
    p_head = eq("P", cfg.FONT["section"], cfg.PRESSURE).next_to(ground, LEFT, buff=0.25)
    zig = polyline([[BAR_X - 0.75, BAR_BASE + 0.08, 0], [BAR_X - 0.45, BAR_BASE + 0.2, 0], [BAR_X - 0.15, BAR_BASE + 0.04, 0],
                    [BAR_X + 0.15, BAR_BASE + 0.2, 0], [BAR_X + 0.45, BAR_BASE + 0.04, 0], [BAR_X + 0.75, BAR_BASE + 0.16, 0]],
                   cfg.BG, width=7)
    low_tag = txt(f"{fx(P_LOW, 0)} bar", cfg.FONT["tiny"], cfg.MUTED).next_to(ground, RIGHT, buff=0.2)
    scene.play(Create(ground), FadeIn(p_head), FadeIn(low_tag), run_time=0.8)
    word_cue(scene, t, 3, "ideal", lead=0.2)
    scene.add(column, reading)
    scene.play(level.to(column, F.ideal, rate_func=smooth), run_time=2.0)
    scene.add(zig)
    ideal_line = DashedLine([BAR_X - 0.8, p_to_y(F.ideal), 0], [BAR_X + 0.8, p_to_y(F.ideal), 0], stroke_color=cfg.LIMIT,
                            stroke_width=4, dash_length=0.1)
    ideal_tag = txt("ideal", cfg.FONT["small"], cfg.LIMIT).next_to(ideal_line, LEFT, buff=0.2)
    play_in(scene, t, 4, Create(ideal_line), FadeIn(ideal_tag), run_time=0.9)

    # --- 4. Correct for size: up to about 26.1 bar ---------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(Indicate(vdw[7:10], color=cfg.WHITE, scale_factor=1.1), run_time=0.9)
    word_cue(scene, t, 4, "rises", lead=0.2)
    step_up = Rectangle(width=1.1, height=p_to_y(F.size_only) - p_to_y(F.ideal), stroke_width=0, fill_color=cfg.SIZE,
                        fill_opacity=0.8).move_to([BAR_X, (p_to_y(F.size_only) + p_to_y(F.ideal)) / 2, 0])
    scene.play(level.to(column, F.size_only, rate_func=smooth), FadeIn(step_up), run_time=1.6)
    up_tag = txt("size: +", cfg.FONT["small"], cfg.SIZE).next_to(step_up, LEFT, buff=0.35).shift(UP * 0.4)
    play_in(scene, t, 5, FadeIn(up_tag, shift=RIGHT * 0.1), run_time=0.8)

    # --- 5. Correct for attraction: down by about 3.6 bar, to about 22.4 bar ------------------------------------------------------
    beat(scene, t, 5)
    scene.play(Indicate(vdw[2:4], color=cfg.WHITE, scale_factor=1.1), run_time=0.9)
    word_cue(scene, t, 5, "three", lead=0.3)
    step_down = Rectangle(width=1.1, height=p_to_y(F.size_only) - p_to_y(F.vdw), stroke_width=3, stroke_color=cfg.ATTRACT,
                          fill_color=cfg.ATTRACT, fill_opacity=0.25)
    step_down.move_to([BAR_X, (p_to_y(F.size_only) + p_to_y(F.vdw)) / 2, 0])
    down_tag = txt(f"attraction: −{fx(F.attraction, 1)}", cfg.FONT["small"], cfg.ATTRACT).next_to(step_down, LEFT, buff=0.35)
    down_tag.shift(DOWN * 0.35)
    scene.play(FadeOut(step_up), FadeIn(step_down), level.to(column, F.vdw, rate_func=smooth), fade_through(up_tag, down_tag),
               run_time=1.8)
    scene.remove(up_tag)
    word_cue(scene, t, 5, "ten", lead=0.3)
    below = boxed(txt(f"−{fx(F.percent_below, 0)} % vs ideal", cfg.FONT["label"], cfg.GOLD), cfg.GOLD, buff=0.16)
    below.move_to([BAR_X + 0.3, -3.6, 0])
    play_in(scene, t, 6, FadeIn(below, shift=UP * 0.1), run_time=1.0)

    # --- 6. A hundred litres: the corrections almost vanish ------------------------------------------------------------------------
    beat(scene, t, 6)
    column.clear_updaters()
    reading.clear_updaters()
    scene.play(FadeOut(VGroup(column, reading, step_down, down_tag, ideal_line, ideal_tag, below, ground, p_head, zig, low_tag)),
               run_time=0.8)
    ratio_head = VGroup(eq(r"\frac{P_{\text{vdW}}}{P_{\text{ideal}}}", cfg.FONT["section"], cfg.WHITE),
                        eq("=", cfg.FONT["section"], cfg.WHITE))
    ratio_head.arrange(RIGHT, buff=0.2).move_to([2.3, 0.0, 0])
    ratio_value = live(VGroup(), lambda: txt(fx(ratio_at(volume.value), 2), cfg.FONT["hero"], cfg.GOLD)
                       .next_to(ratio_head, RIGHT, buff=0.3))
    scene.play(FadeIn(ratio_head), FadeIn(ratio_value), run_time=0.9)
    fade_terms = Knob(1.0)
    for idx in (3, 8):
        vdw[idx].add_updater(lambda m, k=fade_terms: m.set_opacity(0.15 + 0.85 * k.value))
    word_cue(scene, t, 6, "hundred", lead=0.3)
    scene.play(volume.to(ratio_value, 100.0, rate_func=lambda a: smooth(a) ** 2), fade_terms.to(vdw, 0.0), stage.zoom_to(0.85),
               run_time=3.6)
    becomes = paint(eq(["P", "V", r"\approx", "nRT"], cfg.FONT["section"]), {0: cfg.PRESSURE, 1: cfg.VOLUME})
    becomes.next_to(ratio_head, DOWN, buff=0.7).align_to(ratio_head, LEFT)
    play_in(scene, t, 7, FadeIn(becomes, shift=UP * 0.15), run_time=1.2)

    # --- 7. Two molecular corrections -------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    for idx in (3, 8):
        vdw[idx].clear_updaters()
    ratio_value.clear_updaters()
    vol_tag.clear_updaters()
    hide(scene, stage, 0.9, FadeOut(VGroup(ratio_head, ratio_value, becomes, facts, vol_tag)), vdw[3].animate.set_opacity(1),
         vdw[8].animate.set_opacity(1))
    scene.play(top_eq.animate.scale(1 / 0.62).move_to([0, 0.6, 0]), run_time=1.2)
    word_cue(scene, t, 7, "approximation", lead=0.2)
    word = txt("two molecular corrections", cfg.FONT["section"], cfg.GOLD).move_to([0, 2.7, 0])
    scene.play(FadeIn(word, shift=DOWN * 0.1), run_time=1.0)
    word_cue(scene, t, 7, "attract", lead=0.3)
    b1 = Brace(vdw[2:4], DOWN, color=cfg.ATTRACT)
    l1 = txt("molecules attract", cfg.FONT["label"], cfg.ATTRACT).next_to(b1, DOWN, buff=0.15)
    scene.play(GrowFromCenter(b1), FadeIn(l1, shift=UP * 0.1), run_time=1.0)
    word_cue(scene, t, 7, "space", lead=0.4)
    b2 = Brace(vdw[7:9], DOWN, color=cfg.SIZE)
    l2 = txt("molecules take up space", cfg.FONT["label"], cfg.SIZE).next_to(b2, DOWN, buff=0.15)
    l2.next_to(l1, DOWN, buff=0.3)
    l2.set_x(min(b2.get_center()[0], 7.4 - l2.width / 2))
    scene.play(GrowFromCenter(b2), FadeIn(l2, shift=UP * 0.1), run_time=1.0)
    finish(scene, t, fill=lambda s: [Indicate(framed, color=cfg.WHITE, scale_factor=1.02)])
