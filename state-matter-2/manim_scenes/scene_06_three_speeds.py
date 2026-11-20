"""Scene 06 — three typical speeds. Nitrogen at 300 K: a cyan histogram of
2000 seeded molecular speeds rises bar by bar and the gold Maxwell-Boltzmann
curve (``pm.mb_pdf``) is drawn over it. Three markers follow, each with its
formula and value in a column on the right (every number from ``pm.SPEEDS``):

* the most probable speed at the peak (cyan), sqrt(2RT/M), about 420 m/s;
* the average speed (rose), the balance point of the distribution: a fulcrum
  slides under the axis to where the curve would balance, sqrt(8RT/(pi M)), about 480 m/s;
* the root-mean-square speed (orange), sqrt(3RT/M), about 520 m/s.

Why that order: the long fast tail is shaded and pulls the average right of
the peak; a dashed u²-weighted curve shows how squaring favours the fast
molecules, pulling the rms further still. The ratio 1 : 1.128 : 1.225 is
framed, and the units warning closes the scene: M in kg/mol, never g/mol
(using 28 with SI R makes the speed about 32 times too small).
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d
from manim_scenes.kit_d import at_word

S = pm.SPEEDS
M = pm.MOLAR_MASS[S.light]
T = S.T1
U_MAX, Y_MAX = 1400.0, 2.5
C_MP, C_AV, C_RMS = cfg.CYAN, cfg.ROSE, cfg.ORANGE
COL_X = 4.75
PLOT_X = -3.2


class Scene06ThreeSpeeds(Scene):
    def construct(self) -> None:
        play_scene(self)


def nearest_ten(value: float) -> str:
    return fx(round(value, -1), 0)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "06", TITLES["06"])
    axes = speed_axes(U_MAX, Y_MAX, at=[PLOT_X, -0.15, 0], x_length=7.7, y_length=4.2, ticks=(200, 600, 1000))
    gas = chip(f"N₂ · {fx(T, 0)} K", cfg.GAS_COLORS["N2"], cfg.FONT["small"]).move_to(axes.c2p(1100, 2.05))

    # --- 0. A histogram of speeds and its curve ------------------------------------------------------------------------
    rng = np.random.default_rng(cfg.SEED + 60)
    sigma = np.sqrt(pm.R * T / M)
    speeds = np.linalg.norm(rng.normal(scale=sigma, size=(2000, 3)), axis=1)
    edges = np.linspace(0, U_MAX, 29)
    bars = histogram_bars(axes, speeds, edges, cfg.MOLECULE, scale=PDF_SCALE, fill_opacity=0.4)
    curve = mb_curve(axes, T, M, cfg.GOLD, u_max=U_MAX, width=6)
    scene.play(Create(axes), FadeIn(gas, shift=DOWN * 0.1), run_time=1.4)
    scene.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), run_time=2.6)
    scene.play(Create(curve), run_time=1.6)
    play_in(scene, t, 1, bars.animate.set_fill(opacity=0.18).set_stroke(opacity=0.3), run_time=1.2)

    # Label row above the plot, with leader lines down to each marker.
    top_row = axes.c2p(0, Y_MAX)[1] + 0.42

    def marker(u: float, color: str, latex: str, x_label: float):
        mk = speed_marker(axes, u, T, M, color)
        tag = eq(latex, cfg.FONT["section"], color).move_to([axes.c2p(x_label, 0)[0], top_row, 0])
        lead = DashedLine(tag.get_bottom() + DOWN * 0.05, mk.top + UP * 0.12, stroke_color=color, stroke_width=2.2,
                          stroke_opacity=0.7, dash_length=0.07)
        return mk, tag, lead

    def formula_row(latex: str, value: float, color: str, y: float, glyphs: int = 3) -> VGroup:
        f = eq(latex, cfg.FONT["label"], cfg.WHITE)
        f[0][0:glyphs].set_color(color)
        v = txt(f"≈ {nearest_ten(value)} m/s", cfg.FONT["small"], color)
        row = VGroup(f, v).arrange(DOWN, buff=0.18).move_to([COL_X, y, 0])
        return row

    # --- 1. Most probable speed -----------------------------------------------------------------------------------------
    beat(scene, t, 1)
    mk_mp, tag_mp, lead_mp = marker(S.mp, C_MP, r"u_{\mathrm{mp}}", 230)
    at_word(scene, t, 1, "peak", lead=0.2)
    peak_ring = Circle(radius=0.3, stroke_color=C_MP, stroke_width=5).move_to(mk_mp.top)
    scene.play(Create(peak_ring), run_time=0.8)
    scene.play(Create(mk_mp.line), FadeIn(mk_mp.dot), FadeOut(peak_ring), run_time=1.0)
    scene.play(FadeIn(tag_mp, shift=DOWN * 0.1), Create(lead_mp), run_time=0.9)
    at_word(scene, t, 1, "equals", lead=0.2)
    row_mp = formula_row(r"u_{\mathrm{mp}}=\sqrt{\frac{2RT}{M}}", S.mp, C_MP, 1.95)
    scene.play(Write(row_mp[0]), run_time=1.4)
    at_word(scene, t, 1, "four", lead=0.2)
    play_in(scene, t, 2, FadeIn(row_mp[1], shift=UP * 0.1), Indicate(mk_mp.dot, color=cfg.WHITE, scale_factor=1.5), run_time=1.2)

    # --- 2. Average speed: the balance point ----------------------------------------------------------------------------
    beat(scene, t, 2)
    mk_av, tag_av, lead_av = marker(S.av, C_AV, r"u_{\mathrm{av}}", 520)
    pivot = Knob(S.mp)
    fulcrum = live(VGroup(), lambda: Triangle(stroke_color=C_AV, stroke_width=3, fill_color=C_AV, fill_opacity=0.8)
                   .scale(0.22).move_to(axes.c2p(pivot.value, 0) + DOWN * 0.24))
    balance = txt("balance point", cfg.FONT["small"], C_AV).next_to(axes.c2p(S.av, 0), DOWN, buff=0.62)
    scene.play(FadeIn(fulcrum, shift=UP * 0.2), run_time=0.8)
    at_word(scene, t, 2, "divides", lead=0.2)
    scene.play(pivot.to(fulcrum, S.av + 60, rate_func=smooth), run_time=1.4)
    scene.play(pivot.to(fulcrum, S.av, rate_func=smooth), FadeIn(balance, shift=UP * 0.1), run_time=1.0)
    scene.play(Create(mk_av.line), FadeIn(mk_av.dot), FadeIn(tag_av, shift=DOWN * 0.1), Create(lead_av), run_time=1.1)
    at_word(scene, t, 2, "square", lead=0.2)
    row_av = formula_row(r"u_{\mathrm{av}}=\sqrt{\frac{8RT}{\pi M}}", S.av, C_AV, -0.05)
    scene.play(Write(row_av[0]), run_time=1.4)
    at_word(scene, t, 2, "four", lead=0.2)
    play_in(scene, t, 3, FadeIn(row_av[1], shift=UP * 0.1), run_time=1.0)

    # --- 3. Root mean square speed --------------------------------------------------------------------------------------
    beat(scene, t, 3)
    fulcrum.clear_updaters()
    mk_rms, tag_rms, lead_rms = marker(S.rms, C_RMS, r"u_{\mathrm{rms}}", 830)
    steps = VGroup(*[txt(w, cfg.FONT["small"], C_RMS) for w in ("square", "average", "root")]).arrange(RIGHT, buff=0.55)
    arrows = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.1, stroke_width=4, color=cfg.MUTED,
                            max_tip_length_to_length_ratio=0.35) for k in range(2)])
    recipe = VGroup(steps, arrows).move_to([PLOT_X, -3.45, 0])
    scene.play(FadeOut(balance), run_time=0.35)
    scene.play(FadeIn(steps[0], shift=UP * 0.1), run_time=0.5)
    at_word(scene, t, 3, "averages", lead=0.2)
    scene.play(GrowArrow(arrows[0]), FadeIn(steps[1], shift=UP * 0.1), run_time=0.7)
    at_word(scene, t, 3, "root", nth=2, lead=0.2)
    scene.play(GrowArrow(arrows[1]), FadeIn(steps[2], shift=UP * 0.1), run_time=0.7)
    scene.play(Create(mk_rms.line), FadeIn(mk_rms.dot), FadeIn(tag_rms, shift=DOWN * 0.1), Create(lead_rms), run_time=1.1)
    at_word(scene, t, 3, "equals", lead=0.2)
    row_rms = formula_row(r"u_{\mathrm{rms}}=\sqrt{\frac{3RT}{M}}", S.rms, C_RMS, -2.05, glyphs=4)
    scene.play(Write(row_rms[0]), run_time=1.4)
    at_word(scene, t, 3, "five", lead=0.2)
    play_in(scene, t, 4, FadeIn(row_rms[1], shift=UP * 0.1), run_time=1.0)

    # --- 4. Why this order: the fast tail, and squaring -------------------------------------------------------------------
    beat(scene, t, 4)
    us = np.linspace(700, U_MAX, 60)
    tail = Polygon(axes.c2p(700, 0), *[axes.c2p(u, float(pm.mb_pdf(u, T, M)) * PDF_SCALE) for u in us], axes.c2p(U_MAX, 0),
                   stroke_width=0, fill_color=cfg.FAST, fill_opacity=0.35)
    tail_tag = txt("fast tail", cfg.FONT["small"], cfg.FAST).move_to(axes.c2p(1050, 0.75))
    scene.play(FadeOut(recipe), FadeIn(tail), FadeIn(tail_tag, shift=LEFT * 0.1), run_time=1.0)
    at_word(scene, t, 4, "average", lead=0.2)
    y_arrow = axes.c2p(0, 0)[1] - 1.0
    pull_av = arrow2d([axes.c2p(S.mp, 0)[0], y_arrow, 0], [axes.c2p(S.av, 0)[0] + 0.25, y_arrow, 0], C_AV, width=0.08,
                      tip_len=0.22)
    scene.play(FadeIn(pull_av, shift=RIGHT * 0.1), Indicate(tag_av, color=cfg.WHITE, scale_factor=1.15), run_time=1.0)
    at_word(scene, t, 4, "Squaring", lead=0.2)
    weighted = curve_on(axes, lambda u: float(u * u * pm.mb_pdf(u, T, M)) / S.rms ** 2 * PDF_SCALE, 0, U_MAX, C_RMS, width=4,
                        glow=False)
    weighted_d = DashedVMobject(weighted.core, num_dashes=44)
    w_tag = eq(r"\times u^2", cfg.FONT["label"], C_RMS).move_to(axes.c2p(1000, 1.55))
    scene.play(Create(weighted_d), FadeIn(w_tag, shift=RIGHT * 0.1), run_time=1.6)
    pull_rms = arrow2d([axes.c2p(S.av, 0)[0], y_arrow - 0.35, 0], [axes.c2p(S.rms, 0)[0] + 0.3, y_arrow - 0.35, 0], C_RMS,
                       width=0.08, tip_len=0.22)
    at_word(scene, t, 4, "further", lead=0.3)
    play_in(scene, t, 5, FadeIn(pull_rms, shift=RIGHT * 0.1), Indicate(tag_rms, color=cfg.WHITE, scale_factor=1.15), run_time=1.2)

    # --- 5. The ratio -----------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    r = pm.SPEED_RATIO
    ratio = VGroup(txt("1", cfg.FONT["title"], C_MP), txt(":", cfg.FONT["title"], cfg.MUTED),
                   txt(fx(r[1], 3), cfg.FONT["title"], C_AV), txt(":", cfg.FONT["title"], cfg.MUTED),
                   txt(fx(r[2], 3), cfg.FONT["title"], C_RMS)).arrange(RIGHT, buff=0.3)
    ratio_box = boxed(ratio, cfg.GOLD, buff=0.2).move_to([PLOT_X, -3.4, 0])
    scene.play(FadeOut(VGroup(tail, tail_tag, weighted_d, w_tag, pull_av, pull_rms)), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in ratio], lag_ratio=0.35), run_time=2.4)
    play_in(scene, t, 6, Create(ratio_box.frame), run_time=1.0)

    # --- 6. Units: M in kilograms per mole ----------------------------------------------------------------------------------
    beat(scene, t, 6)
    good = VGroup(eq(r"M = 0.028\ \mathrm{kg\,mol^{-1}}", cfg.FONT["body"], cfg.GREEN), check_mark(0.28)).arrange(RIGHT, buff=0.3)
    bad = VGroup(eq(r"M = 28\ \mathrm{g\,mol^{-1}}", cfg.FONT["body"], cfg.RED), cross_mark(0.24)).arrange(RIGHT, buff=0.3)
    wrong = txt(f"speeds off by ×{fx(S.grams_error, 0)}", cfg.FONT["small"], cfg.RED)
    units = VGroup(good, bad, wrong).arrange(DOWN, buff=0.4).move_to([COL_X - 0.2, 0.1, 0])
    scene.play(FadeOut(VGroup(row_mp, row_av, row_rms)), run_time=0.8)
    at_word(scene, t, 6, "kilograms", lead=0.4)
    scene.play(FadeIn(good, shift=LEFT * 0.15), run_time=1.0)
    at_word(scene, t, 6, "grams", lead=0.3)
    scene.play(FadeIn(bad, shift=LEFT * 0.15), run_time=1.0)
    at_word(scene, t, 6, "factor", lead=0.3)
    scene.play(FadeIn(wrong, shift=UP * 0.1), Wiggle(bad[0], scale_value=1.08), run_time=1.2)
    finish(scene, t, fill=lambda s: [Indicate(good, color=cfg.WHITE, scale_factor=1.06)])
