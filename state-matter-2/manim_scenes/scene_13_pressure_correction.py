"""Scene 13 — correcting the pressure. PV = nRT returns with the two repairs
van der Waals made in 1873 waiting beneath it: attraction (green, for P) and
size (red, for V). Attraction first. Two bars: the pressure we measure (teal)
falls short of the ideal pressure (dashed purple) by a green gap, so
P_* = P_real + an attraction correction, retaining excluded volume in the reference.

How big? A turning 3D cube holds a dilute gas; every pair of molecules close
enough to attract is joined by a green link, and a live count reads the
pairs. Doubling the density (the same molecules plus as many again,
``pm.pair_demo``) multiplies the pairs by about four: twice the molecules,
each with about twice the neighbours. So the correction grows as (n/V)²,
written a n²/V². Bars of the constant a (``pm.VDW``) for helium, carbon dioxide
and ammonia show how much it depends on the molecule. Finally a fog of links
across the whole cube: the correction is a mean-field average.
"""

from manim_scenes.common import *
from manim_scenes.kit_c import PairLinks, word_cue

CUBE = 3.2
DILUTE, DENSE, P1, P2 = pm.pair_demo()
CUT = 0.42 * CUBE
EQ_Y = 1.6


class Scene13PressureCorrection(Scene):
    def construct(self) -> None:
        play_scene(self)


def cube_edges(stage: Stage, half: float) -> list[Segment]:
    edges = []
    for a in (-1, 1):
        for b in (-1, 1):
            edges.append(Segment(np.array([-half, a * half, b * half]), np.array([half, a * half, b * half]), cfg.GLASS, 2.6, 0.55))
            edges.append(Segment(np.array([a * half, -half, b * half]), np.array([a * half, half, b * half]), cfg.GLASS, 2.6, 0.55))
            edges.append(Segment(np.array([a * half, b * half, -half]), np.array([a * half, b * half, half]), cfg.GLASS, 2.6, 0.55))
    stage.add_body(*edges)
    return edges


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "13", TITLES["13"])

    # --- 0. Two repairs, one for each thing the model ignores -------------------------------------------------------------
    law = paint(eq(["P", "V", "=", "n", "R", "T"], cfg.FONT["hero"]), {0: cfg.PRESSURE, 1: cfg.VOLUME, 3: cfg.AMOUNT,
                                                                        5: cfg.TEMPERATURE})
    law.move_to([0, EQ_Y, 0])
    who = chip("van der Waals · 1873", cfg.GOLD, cfg.FONT["small"]).move_to([0, 3.0, 0])
    fix_p = chip("attraction", cfg.ATTRACT, cfg.FONT["label"]).move_to([-2.6, -0.6, 0])
    fix_v = chip("size", cfg.SIZE, cfg.FONT["label"]).move_to([2.6, -0.6, 0])
    to_p = Arrow(fix_p.get_top(), law[0].get_bottom(), buff=0.15, color=cfg.ATTRACT, stroke_width=5)
    to_v = Arrow(fix_v.get_top(), law[1].get_bottom(), buff=0.15, color=cfg.SIZE, stroke_width=5)
    scene.play(Write(law), run_time=1.6)
    word_cue(scene, t, 0, "eighteen", lead=0.2)
    scene.play(FadeIn(who, shift=DOWN * 0.1), run_time=0.9)
    word_cue(scene, t, 0, "two", lead=0.2)
    scene.play(FadeIn(fix_p, shift=UP * 0.2), GrowArrow(to_p), run_time=1.0)
    scene.play(FadeIn(fix_v, shift=UP * 0.2), GrowArrow(to_v), run_time=1.0)
    play_in(scene, t, 1, Indicate(fix_p, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)

    # --- 1. Attraction lowers what we measure: P_ideal = P_real + correction ------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeOut(VGroup(fix_v, to_v, to_p, who)), run_time=0.5)
    scene.play(fix_p.animate.move_to([-4.6, 2.9, 0]), law.animate.scale(0.7).move_to([0, 2.9, 0]), run_time=0.6)
    base_y = -2.9
    ideal_bar = DashedVMobject(Rectangle(width=1.3, height=4.0, stroke_color=cfg.LIMIT, stroke_width=4), num_dashes=44)
    ideal_bar.move_to([-3.2, base_y + 2.0, 0])
    real_bar = Rectangle(width=1.3, height=3.0, stroke_color=cfg.PRESSURE, stroke_width=3, fill_color=cfg.PRESSURE,
                         fill_opacity=0.75).move_to([-3.2, base_y + 1.5, 0])
    gap = Rectangle(width=1.3, height=1.0, stroke_color=cfg.ATTRACT, stroke_width=3, fill_color=cfg.ATTRACT,
                    fill_opacity=0.45).move_to([-3.2, base_y + 3.5, 0])
    ground = Line([-4.6, base_y, 0], [-1.8, base_y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    tags = VGroup(eq(r"P_*", cfg.FONT["label"], cfg.LIMIT).next_to(ideal_bar, LEFT, buff=0.25).align_to(ideal_bar, UP),
                  eq(r"P_{\text{real}}", cfg.FONT["label"], cfg.PRESSURE).next_to(real_bar, LEFT, buff=0.25))
    scene.play(Create(ground), Create(ideal_bar), FadeIn(tags[0]), run_time=1.2)
    word_cue(scene, t, 1, "measured", lead=0.2)
    scene.play(GrowFromEdge(real_bar, DOWN), FadeIn(tags[1]), run_time=1.2)
    word_cue(scene, t, 1, "equals", lead=0.3)
    split = paint(eq([r"P_*", "=", r"P_{\text{real}}", "+", r"\Delta P_{\mathrm{attr}}"], cfg.FONT["section"]),
                  {0: cfg.LIMIT, 2: cfg.PRESSURE, 4: cfg.ATTRACT}).move_to([2.6, 0.6, 0])
    reference = txt("P*: attraction switched off", cfg.FONT["small"], cfg.LIMIT).move_to([2.6, -1.2, 0])
    fit_width(split, 7.3)
    scene.play(Write(split[:3]), FadeIn(reference), run_time=1.2)
    play_in(scene, t, 2, FadeIn(gap, shift=DOWN * 0.2), FadeIn(split[3:], shift=LEFT * 0.15), run_time=1.2)

    # --- 2. Attraction acts between pairs: count the nearby pairs -------------------------------------------------------------
    beat(scene, t, 2)
    stage = Stage((-3.75, -0.7, 0), zoom=1.22, yaw=-0.5, pitch=0.3, spin=0.12, sway=0.02)
    half = CUBE / 2
    edges = cube_edges(stage, half)
    dil = (DILUTE - 0.5) * CUBE
    den = (DENSE - 0.5) * CUBE
    links_1 = PairLinks(dil, CUT, width=3.6)
    links_2 = PairLinks(den, CUT, width=3.6)
    links_2.presence = 0.0
    first = Dots(dil, cfg.MOLECULE, radius=0.13)
    extra = Dots(den[len(dil):], cfg.MOLECULE, radius=0.13)
    extra.presence = 0.0
    stage.add_body(links_1, links_2, first, extra)
    hide_group = VGroup(ideal_bar, real_bar, gap, ground, tags)
    scene.play(FadeOut(hide_group), FadeOut(reference), split.animate.scale(0.75).move_to([3.4, 1.4, 0]), run_time=0.9)
    show(scene, stage, 1.0)
    pairs_row = VGroup(txt("pairs", cfg.FONT["label"], cfg.ATTRACT), txt(str(P1), cfg.FONT["title"], cfg.WHITE)).arrange(RIGHT, buff=0.3)
    mols_row = VGroup(txt("molecules", cfg.FONT["label"], cfg.MOLECULE), txt(str(len(dil)), cfg.FONT["title"], cfg.WHITE)).arrange(RIGHT, buff=0.3)
    stats = VGroup(mols_row, pairs_row).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.4, -0.95, 0])
    word_cue(scene, t, 2, "Count", lead=0.2)
    scene.play(FadeIn(mols_row, shift=LEFT * 0.15), run_time=0.8)
    play_in(scene, t, 3, FadeIn(pairs_row, shift=LEFT * 0.15), stage.fade(links_1, 1.0, rate_func=there_and_back_with_pause),
            run_time=2.0)

    # --- 3. Double the density: about four times the pairs -----------------------------------------------------------------------
    beat(scene, t, 3)
    word_cue(scene, t, 3, "Twice", lead=0.3)
    mols_2 = txt(str(len(den)), cfg.FONT["title"], cfg.WHITE).move_to(mols_row[1]).align_to(mols_row[1], LEFT)
    times_2 = txt("×2", cfg.FONT["section"], cfg.MOLECULE).next_to(mols_row, RIGHT, buff=0.4)
    old_count = mols_row[1]
    scene.play(stage.fade(extra, 1.0), fade_through(old_count, mols_2), FadeIn(times_2, shift=LEFT * 0.1), run_time=1.4)
    mols_row.remove(old_count)
    scene.remove(old_count)
    word_cue(scene, t, 3, "neighbours", lead=0.3)
    pairs_2 = txt(str(P2), cfg.FONT["title"], cfg.WHITE).move_to(pairs_row[1]).align_to(pairs_row[1], LEFT)
    times_4 = txt(f"×{fx(P2 / P1, 1)}", cfg.FONT["section"], cfg.ATTRACT).next_to(pairs_row, RIGHT, buff=0.4).align_to(times_2, LEFT)
    old_pairs = pairs_row[1]
    scene.play(stage.fade(links_1, 0.0), stage.fade(links_2, 1.0), fade_through(old_pairs, pairs_2), run_time=1.4)
    pairs_row.remove(old_pairs)
    scene.remove(old_pairs)
    word_cue(scene, t, 3, "four", lead=0.3)
    play_in(scene, t, 4, FadeIn(times_4, scale=1.3), Circumscribe(VGroup(pairs_row, times_4), color=cfg.ATTRACT, buff=0.15),
            run_time=1.6)

    # --- 4. The correction grows as (n/V)^2: a n^2 / V^2 ----------------------------------------------------------------------------
    beat(scene, t, 4)
    grows = paint(eq([r"\Delta P_{\mathrm{attr}}", r"\propto", r"\left(\frac{n}{V}\right)^2"], cfg.FONT["section"]),
                  {0: cfg.ATTRACT, 2: cfg.AMOUNT}).move_to([3.4, -2.75, 0])
    scene.play(Write(grows), run_time=1.6)
    word_cue(scene, t, 4, "wrote", lead=0.3)
    final = paint(eq([r"P_*", "=", "P", "+", r"\frac{a n^2}{V^2}"], cfg.FONT["section"]),
                  {0: cfg.LIMIT, 2: cfg.PRESSURE, 4: cfg.ATTRACT}).move_to([3.4, 1.4, 0])
    framed = boxed(final, cfg.GOLD, buff=0.2)
    play_in(scene, t, 5, fade_through(split, final), Create(framed.frame), run_time=1.6)
    scene.remove(split)

    # --- 5. The constant a depends on the molecule ------------------------------------------------------------------------------------
    beat(scene, t, 5)
    gases = ("He", "CO2", "NH3")
    names = ("He", "CO₂", "NH₃")
    values = [pm.VDW[g][0] for g in gases]
    chart = bar_chart(values, names, [cfg.GAS_COLORS[g] for g in gases], at=[3.3, -1.7, 0], width=5.0, height=2.3,
                      value_labels=[fx(v, 2 if v < 1 else 1) for v in values], bar_width=0.95, name_size=cfg.FONT["label"])
    a_tag = eq("a", cfg.FONT["title"], cfg.ATTRACT).next_to(chart, LEFT, buff=0.3).shift(UP * 0.6)
    unit = txt("L² bar / mol²", cfg.FONT["tiny"], cfg.MUTED).next_to(chart, DOWN, buff=0.3)
    scene.play(FadeOut(VGroup(stats, times_2, times_4, mols_2, pairs_2, grows)), run_time=0.8)
    scene.play(Create(chart.base), FadeIn(a_tag), FadeIn(chart.names), FadeIn(unit), run_time=1.0)
    word_cue(scene, t, 5, "helium", lead=0.2)
    scene.play(GrowFromEdge(chart.bars[0], DOWN), FadeIn(chart.tops[0]), run_time=0.8)
    word_cue(scene, t, 5, "carbon", lead=0.2)
    scene.play(GrowFromEdge(chart.bars[1], DOWN), FadeIn(chart.tops[1]), run_time=1.0)
    hundred = txt(f"≈ ×{fx(round(values[1] / values[0], -2), 0)}", cfg.FONT["label"], cfg.GOLD)
    hundred.next_to(chart.bars[1], LEFT, buff=0.15).shift(UP * 0.5)
    scene.play(FadeIn(hundred, shift=UP * 0.1), run_time=0.8)
    word_cue(scene, t, 5, "ammonia", lead=0.2)
    play_in(scene, t, 6, GrowFromEdge(chart.bars[2], DOWN), FadeIn(chart.tops[2]), run_time=1.0)

    # --- 6. A mean-field estimate ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    fog = PairLinks(den, CUT * 1.9, width=2.0, opacity=0.35)
    fog.presence = 0.0
    stage.add_body(fog)
    scene.play(stage.fade(fog, 1.0), stage.zoom_to(1.3), run_time=1.6)
    word_cue(scene, t, 6, "mean", lead=0.3)
    mf = chip("mean-field average", cfg.ATTRACT, cfg.FONT["small"]).move_to([-3.75, -3.6, 0])
    scene.play(FadeIn(mf, shift=UP * 0.1), run_time=0.9)
    word_cue(scene, t, 6, "scales", lead=0.3)
    scene.play(Indicate(final[4], color=cfg.WHITE, scale_factor=1.2), run_time=1.2)
    finish(scene, t, stage)
