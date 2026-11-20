"""Scene 20 — the equation predicts a liquid. The van der Waals equation's
own isotherms (``pm.vdw_reduced``, reduced units). Hot ones (coral) fall
smoothly. Below the critical temperature (blue) each develops a wiggle; on one
of them the stretch between the turning points, where squeezing would lower
the pressure, glows red: no stable fluid behaves that way.

Maxwell's construction (``pm.maxwell``): a flat line at the coexistence
pressure cuts off two lobes, shaded and integrated numerically on screen —
equal areas. The wiggle becomes dashed and the flat line bold, as Andrews
measured. A live isotherm then warms toward T_c; its wiggle and flat line
(from a precomputed Maxwell table) shrink to one purple point, the van der
Waals critical point, T_c = 8a / 27Rb. Run backwards, a and b are chosen from
measured critical constants; for carbon dioxide the CRC constants give
8a/27Rb ≈ 304 K against 304.1 K measured (``pm.vdw_critical_temperature``).
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d
from manim_scenes.kit_d import at_word

V_MIN, V_MAX = 0.4, 3.4
P_MIN, P_MAX = 0.0, 1.7
HOT = (1.3, 1.6)
COLD = (0.93, 0.88)
LOOP = 0.88
COL_X = 4.75
_TRS = np.linspace(0.86, 0.9995, 60)
_TABLE = np.array([pm.maxwell(float(x)) for x in _TRS])


class Scene20VdwLoops(Scene):
    def construct(self) -> None:
        play_scene(self)


def iso_color(tr: float) -> str:
    return mu.mix(cfg.COLD_COLOR, cfg.HOT_COLOR, float(np.clip((tr - 0.85) / 0.8, 0, 1)))


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "20", TITLES["20"])
    axes = plot_axes((V_MIN, V_MAX), (P_MIN, P_MAX), x_length=8.6, y_length=5.8, at=[-1.75, -0.4, 0], x_label="V", y_label="P",
                     x_color=cfg.VOLUME, y_color=cfg.PRESSURE)
    vs = np.linspace(V_MIN + 0.08, V_MAX, 400)

    def curve(tr: float, color: str | None = None, width: float = 5.0) -> VMobject:
        ps = pm.vdw_reduced(vs, tr)
        keep = (ps <= P_MAX) & (ps >= P_MIN)
        return polyline([axes.c2p(v, p) for v, p in zip(vs[keep], ps[keep])], color or iso_color(tr), width=width)

    def glow(m: VMobject) -> VGroup:
        return VGroup(m.copy().set_stroke(width=m.get_stroke_width() * 3, opacity=0.14), m)

    # --- 0. The equation's own isotherms ----------------------------------------------------------------------------------
    title = chip("van der Waals isotherms", cfg.WHITE, cfg.FONT["small"]).move_to([-1.75, 3.1, 0])
    scene.play(Create(axes), FadeIn(title, shift=DOWN * 0.1), run_time=1.4)
    play_in(scene, t, 1, Indicate(title, color=cfg.GOLD, scale_factor=1.05), run_time=1.0)

    # --- 1. Hot: smooth, gas-like ----------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    hot = [glow(curve(tr)) for tr in HOT]
    for c in hot[::-1]:
        scene.play(Create(c), run_time=1.4)
    smooth_tag = txt("smooth", cfg.FONT["label"], cfg.HOT_COLOR).move_to(axes.c2p(2.6, 1.35))
    play_in(scene, t, 2, FadeIn(smooth_tag, shift=DOWN * 0.1), run_time=0.9)

    # --- 2. Cold: a wiggle ------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    cold = {tr: glow(curve(tr)) for tr in COLD}
    for tr in COLD:
        scene.play(Create(cold[tr]), run_time=1.4)
    wiggle_tag = txt("a wiggle", cfg.FONT["label"], cfg.COLD_COLOR).move_to(axes.c2p(1.25, 0.2))
    play_in(scene, t, 3, FadeIn(wiggle_tag, shift=UP * 0.1), run_time=0.8)

    # --- 3. Squeezing lowers the pressure: unstable, the fluid splits ---------------------------------------------------------
    beat(scene, t, 3)
    scene.play(*[c.animate.set_stroke(opacity=0.25) for c in (*hot, cold[COLD[0]])], FadeOut(smooth_tag), FadeOut(wiggle_tag),
               run_time=0.9)
    fine = np.linspace(0.42, 3.0, 4000)
    ps = pm.vdw_reduced(fine, LOOP)
    dp = np.diff(ps)
    turns = np.nonzero(np.sign(dp[1:]) != np.sign(dp[:-1]))[0] + 1
    v_lo, v_hi = fine[turns[0]], fine[turns[1]]
    seg = np.linspace(v_lo, v_hi, 80)
    unstable = polyline([axes.c2p(v, float(pm.vdw_reduced(v, LOOP))) for v in seg], cfg.WARNING, width=9)
    unstable = glow(unstable)
    scene.play(Create(unstable), run_time=1.4)
    at_word(scene, t, 3, "lower", lead=0.3)
    mid = (v_lo + v_hi) / 2
    a_from = axes.c2p(mid + 0.35, float(pm.vdw_reduced(mid + 0.35, LOOP)) + 0.28)
    a_to = axes.c2p(mid - 0.35, float(pm.vdw_reduced(mid - 0.35, LOOP)) + 0.28)
    squeeze = arrow2d(a_from, a_to, cfg.WARNING, width=0.08, tip_len=0.24)
    claim = VGroup(txt("squeeze →", cfg.FONT["label"], cfg.VOLUME), txt("P falls", cfg.FONT["label"], cfg.WARNING)).arrange(RIGHT, buff=0.2)
    claim.move_to([COL_X, 1.9, 0])
    scene.play(FadeIn(squeeze), FadeIn(claim, shift=LEFT * 0.15), run_time=1.2)
    at_word(scene, t, 3, "stable", lead=0.3)
    nope = VGroup(txt("unstable", cfg.FONT["section"], cfg.WARNING), cross_mark(0.26)).arrange(RIGHT, buff=0.25).move_to([COL_X, 1.0, 0])
    scene.play(FadeIn(nope, scale=1.1), run_time=0.9)
    at_word(scene, t, 3, "splits", lead=0.4)
    split = txt("→ two phases", cfg.FONT["section"], cfg.COEXIST).move_to([COL_X, 0.05, 0])
    play_in(scene, t, 4, FadeIn(split, shift=UP * 0.1), run_time=1.0)

    # --- 4. Maxwell's construction: equal areas -------------------------------------------------------------------------------------
    beat(scene, t, 4)
    p_sat, vl, vg = pm.maxwell(LOOP)
    roots = sorted(np.roots([3 * p_sat, -(p_sat + 8 * LOOP), 9.0, -3.0]).real)
    vm = roots[1]
    flat = Line(axes.c2p(vl, p_sat), axes.c2p(vg, p_sat), stroke_color=cfg.GOLD, stroke_width=7)

    def lobe(a: float, b: float) -> tuple[Polygon, float]:
        xs = np.linspace(a, b, 80)
        ys = pm.vdw_reduced(xs, LOOP)
        area = float(abs(np.trapezoid(ys - p_sat, xs)))
        shape = Polygon(*[axes.c2p(x, y) for x, y in zip(xs, ys)], axes.c2p(b, p_sat), axes.c2p(a, p_sat), stroke_width=0,
                        fill_color=cfg.GOLD, fill_opacity=0.42)
        return shape, area

    lobe_1, area_1 = lobe(vl, vm)
    lobe_2, area_2 = lobe(vm, vg)
    scene.play(FadeOut(VGroup(squeeze, claim, nope)), Create(flat), run_time=0.9)
    scene.play(split.animate.move_to([COL_X, 2.3, 0]), run_time=0.5)
    at_word(scene, t, 4, "areas", lead=0.4)
    scene.play(FadeIn(lobe_1), FadeIn(lobe_2), run_time=1.2)
    areas = VGroup(eq(rf"A_1 = {fx(area_1, 3)}", cfg.FONT["label"], cfg.GOLD), eq(rf"A_2 = {fx(area_2, 3)}", cfg.FONT["label"], cfg.GOLD))
    areas.arrange(DOWN, buff=0.25).move_to([COL_X, 0.9, 0])
    tag_1 = eq("A_1", cfg.FONT["small"], cfg.GOLD).move_to(axes.c2p((vl + vm) / 2 + 0.02, p_sat - 0.13))
    tag_2 = eq("A_2", cfg.FONT["small"], cfg.GOLD).move_to(axes.c2p((vm + vg) / 2, p_sat + 0.09))
    scene.play(FadeIn(tag_1), FadeIn(tag_2), FadeIn(areas, shift=LEFT * 0.15), run_time=1.0)
    equal = txt("equal areas", cfg.FONT["section"], cfg.GOLD).move_to([COL_X, -0.3, 0])
    scene.play(FadeIn(equal, scale=1.1), run_time=0.8)
    at_word(scene, t, 4, "coexistence", lead=0.3)
    loop_part = cold[LOOP]
    dashed_loop = DashedVMobject(curve(LOOP, iso_color(LOOP), 3), num_dashes=90)
    coex = txt("coexistence pressure", cfg.FONT["small"], cfg.GOLD).next_to(flat, UP, buff=0.12).shift(RIGHT * 0.6)
    scene.play(FadeOut(loop_part), FadeIn(dashed_loop), FadeOut(VGroup(lobe_1, lobe_2, tag_1, tag_2)), FadeOut(unstable), run_time=0.7)
    play_in(scene, t, 5, FadeIn(coex), run_time=0.7)
    scene.remove(unstable)

    # --- 5. Warm it: the wiggle shrinks to the critical point ----------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(FadeOut(VGroup(areas, equal, split, coex, dashed_loop, flat, cold[COLD[0]])), run_time=0.8)
    tr = Knob(LOOP)

    def live_iso() -> VGroup:
        T = tr.value
        group = VGroup(glow(curve(T, cfg.WHITE, 5)))
        if T < 0.9995:
            p = float(np.interp(T, _TRS, _TABLE[:, 0]))
            a = float(np.interp(T, _TRS, _TABLE[:, 1]))
            b = float(np.interp(T, _TRS, _TABLE[:, 2]))
            group.add(Line(axes.c2p(a, p), axes.c2p(b, p), stroke_color=cfg.GOLD, stroke_width=6))
        return group

    iso = live(VGroup(), live_iso)
    reading = live(VGroup(), lambda: VGroup(eq("T =", cfg.FONT["label"], cfg.TEMPERATURE), txt(f"{fx(tr.value, 2)}", cfg.FONT["section"],
                                                                                               cfg.WHITE),
                                            eq("T_c", cfg.FONT["label"], cfg.WHITE)).arrange(RIGHT, buff=0.15).move_to([COL_X, 2.3, 0]))
    scene.add(iso, reading)
    scene.play(FadeIn(iso), FadeIn(reading), run_time=0.6)
    scene.play(tr.to(iso, 1.0, rate_func=smooth), run_time=4.4)
    cp = glow_dot(axes.c2p(1.0, 1.0), cfg.CRITICAL, radius=0.16, reach=4)
    cp_tag = result_label("critical point", cfg.CRITICAL, cfg.FONT["label"]).move_to(axes.c2p(1.75, 1.2))
    scene.play(FadeIn(cp, scale=2), FadeIn(cp_tag, shift=DOWN * 0.1), run_time=1.0)
    at_word(scene, t, 5, "eight", lead=0.3)
    tc_eq = paint(eq([r"T_c", "=", r"\frac{8a}{27Rb}"], cfg.FONT["title"]), {0: cfg.CRITICAL})
    tc_box = boxed(tc_eq, cfg.GOLD, buff=0.22).move_to([COL_X, 0.85, 0])
    play_in(scene, t, 6, Write(tc_eq), Create(tc_box.frame), run_time=1.6)

    # --- 6. Run it backwards: choose a and b from the measured critical point ------------------------------------------------------
    beat(scene, t, 6)
    iso.clear_updaters()
    reading.clear_updaters()
    scene.play(FadeOut(reading), run_time=0.5)
    at_word(scene, t, 6, "backwards", lead=0.3)
    back = VGroup(eq(r"a = \frac{27R^2T_c^2}{64P_c}", cfg.FONT["label"], cfg.ATTRACT), eq(r"b = \frac{RT_c}{8P_c}", cfg.FONT["label"], cfg.SIZE))
    back.arrange(DOWN, buff=0.35).move_to([COL_X, -1.75, 0])
    scene.play(FadeIn(back, shift=UP * 0.1), run_time=1.2)
    at_word(scene, t, 6, "measured", lead=0.3)
    check = VGroup(txt("CO₂:", cfg.FONT["small"], cfg.GAS_COLORS["CO2"]),
                   txt(f"8a/27Rb ≈ {fx(pm.vdw_critical_temperature('CO2'), 0)} K", cfg.FONT["small"], cfg.WHITE),
                   txt(f"measured {fx(pm.CRITICAL['CO2'][0], 1)} K", cfg.FONT["small"], cfg.GREEN)).arrange(RIGHT, buff=0.25)
    check.move_to([0.2, -3.8, 0])
    scene.play(FadeIn(check, shift=UP * 0.1), run_time=1.0)
    finish(scene, t, fill=lambda s: [Indicate(cp, color=cfg.WHITE, scale_factor=1.3)])
