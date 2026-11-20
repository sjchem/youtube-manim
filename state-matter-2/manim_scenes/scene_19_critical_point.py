"""Scene 19 — the critical point. Andrews' isotherms for carbon dioxide, drawn
as in scene 18 (the van der Waals model with Maxwell's flat coexistence line,
``pm.isotherm``, reduced units), coloured cold blue to hot coral. The flat
stretches, inside a dashed coexistence dome (``pm.binodal``), shorten as the
temperature rises and shrink to a single purple point on the critical
isotherm: the critical point, with T_c and P_c from ``pm.CRITICAL``. Above it
the isotherms have no flat stretch; the region beyond is tinted purple.

Then a sealed glass tube of carbon dioxide filled at the critical volume. As
it warms (reduced temperature 0.85 → 1.03), the lever rule and the Maxwell
construction set everything drawn: the pool's depth, the number of vapour
molecules, and two density bars, liquid (1 / v_liquid) and vapour
(1 / v_vapour), which converge. The meniscus fades with the density
difference and vanishes at T_c; one purple fluid fills the tube.
"""

from manim_scenes.common import *
from manim_scenes.kit_d import at_word, legend_row
from manim_scenes.kit_e import andrews_color

V_MIN, V_MAX = 0.4, 3.0
P_MIN, P_MAX = 0.5, 1.4
TC, PC = pm.CRITICAL["CO2"]
TUBE_AT = (3.6, -0.55, 0.0)
H_TUBE = 4.2
VAPOUR_MAX = 130
TR_START, TR_END = 0.85, 1.03

# Coexistence table for the tube (Maxwell's construction is too slow to solve every frame).
_TRS = np.linspace(TR_START, 0.9995, 70)
_TABLE = np.array([pm.maxwell(float(x)) for x in _TRS])      # (p, v_liquid, v_vapour)


class Scene19CriticalPoint(Scene):
    def construct(self) -> None:
        play_scene(self)


def coexistence(tr: float) -> tuple[float, float]:
    """(v_liquid, v_vapour) at reduced temperature ``tr`` (both 1 at and above the critical point)."""
    if tr >= 0.9995:
        return 1.0, 1.0
    return float(np.interp(tr, _TRS, _TABLE[:, 1])), float(np.interp(tr, _TRS, _TABLE[:, 2]))


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "19", TITLES["19"])
    axes = plot_axes((V_MIN, V_MAX), (P_MIN, P_MAX), x_length=8.4, y_length=5.6, at=[-1.6, -0.35, 0], x_label="V", y_label="P",
                     x_color=cfg.VOLUME, y_color=cfg.PRESSURE)
    vs = np.linspace(V_MIN, V_MAX, 300)

    def isotherm_curve(celsius_value: float, color: str | None = None, width: float = 5.0) -> VGroup:
        tr = pm.co2_reduced_temperature(celsius_value)
        ps = pm.isotherm(tr, vs, flat=True)
        keep = (ps <= P_MAX) & (ps >= P_MIN)
        pts = [axes.c2p(v, p) for v, p in zip(vs[keep], ps[keep])]
        core = polyline(pts, color or andrews_color(celsius_value), width=width)
        return VGroup(core.copy().set_stroke(width=width * 3, opacity=0.14), core)

    legend_rows = {c: legend_row(f"{fx(c, 1)} °C", cfg.CRITICAL if c == round(TC - pm.T_ICE, 1) else andrews_color(c),
                                 cfg.FONT["small"]) for c in pm.ANDREWS_C}
    legend = VGroup(*[legend_rows[c] for c in sorted(pm.ANDREWS_C, reverse=True)]).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
    legend.move_to([4.75, -1.95, 0])

    def label_for(celsius_value: float, curve: VGroup) -> Mobject:
        return legend_rows[celsius_value]

    # --- 0. Andrews repeats the experiment at higher temperatures ------------------------------------------------------
    cold = [c for c in pm.ANDREWS_C if c < TC - pm.T_ICE]
    hot = [c for c in pm.ANDREWS_C if c >= TC - pm.T_ICE]
    curves = {c: isotherm_curve(c) for c in pm.ANDREWS_C}
    co2 = chip("CO₂ · van der Waals model", cfg.GAS_COLORS["CO2"], cfg.FONT["small"]).move_to([-1.4, 3.05, 0])
    scene.play(Create(axes), FadeIn(co2, shift=DOWN * 0.1), run_time=1.2)
    play_in(scene, t, 1, Create(curves[cold[0]]), FadeIn(label_for(cold[0], curves[cold[0]])), run_time=1.6)

    # --- 1. The flat stretch gets shorter -------------------------------------------------------------------------------
    beat(scene, t, 1)
    dome_pts = np.array([q for q in pm.binodal(90, 0.8) if V_MIN <= q[0] <= V_MAX and q[1] >= P_MIN])
    dome = DashedVMobject(polyline([axes.c2p(v, p) for v, p in dome_pts], cfg.COEXIST, width=3.5), num_dashes=70)
    dome_fill = Polygon(*[axes.c2p(v, p) for v, p in dome_pts], stroke_width=0, fill_color=cfg.COEXIST, fill_opacity=0.12)
    both = txt("gas + liquid", cfg.FONT["small"], cfg.COEXIST).move_to(axes.c2p(1.15, 0.64))
    for c in cold[1:]:
        scene.play(Create(curves[c]), FadeIn(label_for(c, curves[c])), run_time=1.3)
    scene.play(FadeIn(dome_fill), Create(dome), FadeIn(both), run_time=1.4)
    flats = VGroup()
    for c in cold:
        p, vl, vg = pm.maxwell(pm.co2_reduced_temperature(c))
        flats.add(Line(axes.c2p(vl, p), axes.c2p(vg, p), stroke_color=cfg.WHITE, stroke_width=9, stroke_opacity=0.5))
    play_in(scene, t, 2, LaggedStart(*[ShowPassingFlash(f.copy().set_stroke(cfg.WHITE, 10), time_width=0.6) for f in flats],
                                    lag_ratio=0.4), run_time=1.8)

    # --- 2. At about 31 °C the flat stretch shrinks to a point: the critical point -------------------------------------
    beat(scene, t, 2)
    crit = isotherm_curve(TC - pm.T_ICE, cfg.CRITICAL, width=6)
    scene.play(Create(crit), run_time=1.8)
    at_word(scene, t, 2, "critical", lead=0.3)
    cp = glow_dot(axes.c2p(1.0, 1.0), cfg.CRITICAL, radius=0.15, reach=4)
    cp_tag = result_label("critical point", cfg.CRITICAL, cfg.FONT["label"]).move_to(axes.c2p(1.9, 1.13))
    play_in(scene, t, 3, FadeIn(cp, scale=2), FadeIn(cp_tag, shift=DOWN * 0.1), run_time=1.2)

    # --- 3. T_c and P_c ----------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    tc_chip = eq_chip(rf"T_c \approx {fx(TC, 1)}\ \mathrm{{K}}", cfg.CRITICAL, cfg.FONT["label"]).move_to([4.6, 1.3, 0])
    pc_chip = eq_chip(rf"P_c \approx {fx(PC, 1)}\ \mathrm{{bar}}", cfg.CRITICAL, cfg.FONT["label"]).move_to([4.6, 0.1, 0])
    at_word(scene, t, 3, "temperature", lead=0.3)
    scene.play(FadeIn(tc_chip, shift=LEFT * 0.2), run_time=1.0)
    at_word(scene, t, 3, "pressure", lead=0.3)
    guide = DashedLine(axes.c2p(V_MIN, 1), axes.c2p(1, 1), stroke_color=cfg.CRITICAL, stroke_width=3, dash_length=0.1)
    play_in(scene, t, 4, FadeIn(pc_chip, shift=LEFT * 0.2), Create(guide), run_time=1.0)

    # --- 4. Above T_c: no flat stretch, no surface ------------------------------------------------------------------------
    beat(scene, t, 4)
    for c in hot:
        scene.play(Create(curves[c]), FadeIn(label_for(c, curves[c])), run_time=1.2)
    tr_crit = 1.0
    top_pts = [axes.c2p(v, float(pm.vdw_reduced(v, tr_crit))) for v in np.linspace(0.55, 1.0, 40)
               if pm.vdw_reduced(v, tr_crit) <= P_MAX]
    region = Polygon(*top_pts, axes.c2p(V_MAX, 1.0), axes.c2p(V_MAX, P_MAX), stroke_width=0,
                     fill_color=cfg.SUPERCRITICAL, fill_opacity=0.12)
    one = txt("one fluid", cfg.FONT["label"], cfg.SUPERCRITICAL).move_to(axes.c2p(2.5, 1.32))
    scene.play(FadeIn(region), FadeIn(one, shift=DOWN * 0.1), run_time=1.2)
    at_word(scene, t, 4, "denser", lead=0.3)
    hot_tr = pm.co2_reduced_temperature(hot[-1])
    path = [axes.c2p(v, float(pm.vdw_reduced(v, hot_tr))) for v in np.linspace(2.9, 0.55, 50)
            if pm.vdw_reduced(v, hot_tr) <= P_MAX]
    tracer = Dot(path[0], radius=0.11, color=cfg.WHITE)
    play_in(scene, t, 5, MoveAlongPath(tracer, polyline(path, cfg.WHITE)), run_time=3.0)

    # --- 5. A sealed tube, warmed toward T_c ------------------------------------------------------------------------------
    beat(scene, t, 5)
    plot = VGroup(axes, *curves.values(), crit, dome, dome_fill, both, cp, cp_tag, guide, region, one, co2, tracer)
    scene.play(plot.animate.scale(0.66).move_to([-3.85, 0.05, 0]), FadeOut(VGroup(tc_chip, pc_chip, legend)), run_time=1.0)
    tr = Knob(TR_START)
    box = TwoPhaseBox(TUBE_AT, lid="glass", count=VAPOUR_MAX, active=0, half_x=0.8, half_z=0.8, height=H_TUBE,
                      floor=-H_TUBE / 2, zoom=1.05, yaw=-0.5, pitch=0.26, speed=1.3, liquid_spacing=0.22, floor_grid=True,
                      seed=cfg.SEED + 190)
    fluid = Face(lambda: [box.chamber.corner(-1, 0, 1), box.chamber.corner(1, 0, 1), box.chamber.corner(1, 1, 1),
                          box.chamber.corner(-1, 1, 1)], cfg.SUPERCRITICAL, opacity=0.22, edge_opacity=0.0)
    fluid.presence = 0.0
    fluid.bias = 900.0
    box.stage.add_body(fluid)
    _, vl0, vg0 = pm.maxwell(TR_START)
    contrast0 = 1 / vl0 - 1 / vg0

    def drive() -> None:
        vl, vg = coexistence(tr.value)
        if vl < vg:
            x = (vg - 1.0) / (vg - vl)               # lever rule at the critical fill, v = 1
            box.level = x * vl * H_TUBE
            box.set_vapour(int(round(VAPOUR_MAX * (1 - x) * min(1.0, 0.35 + 0.65 * (1 - (1 / vl - 1 / vg) / contrast0)))))
        else:
            box.level = 0.0  # one homogeneous fluid; independent of refresh frequency
            box.set_vapour(VAPOUR_MAX)
        contrast = float(np.clip((1 / vl - 1 / vg) / contrast0, 0.0, 1.0))
        a = contrast ** 0.6
        for face in box.liquid_faces:
            face.presence = a
        box.liquid_dots.alpha = a
        fluid.presence = float(np.clip((tr.value - 0.985) / 0.02, 0.0, 1.0))

    box.stage.bodies.insert(0, Ticker(drive))
    show(scene, box.stage, 1.0)
    therm = live(VGroup(), lambda: txt(f"{fx(pm.celsius(tr.value * TC), 1)} °C", cfg.FONT["section"], andrews_color(
        pm.celsius(tr.value * TC))).move_to([TUBE_AT[0], -3.55, 0]))
    bar_base = -2.4
    bar_x = (5.6, 7.15)

    def bars() -> VGroup:
        vl, vg = coexistence(tr.value)
        group = VGroup()
        for x, rho, color in zip(bar_x, (1 / vl, 1 / vg), (cfg.LIQUID, cfg.VAPOUR)):
            h = rho * 1.75
            group.add(Rectangle(width=0.62, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.8)
                      .move_to([x, bar_base + h / 2, 0]))
        return group

    density_bars = live(VGroup(), bars)
    bar_names = VGroup(txt("liquid", cfg.FONT["tiny"], cfg.LIQUID_EDGE), txt("vapour", cfg.FONT["tiny"], cfg.VAPOUR))
    for name, x in zip(bar_names, bar_x):
        name.move_to([x, bar_base - 0.32, 0])
    rho_tag = txt("density", cfg.FONT["small"], cfg.MUTED).move_to([6.4, 2.4, 0])
    scene.add(therm, density_bars)
    scene.play(FadeIn(therm), FadeIn(density_bars), FadeIn(bar_names), FadeIn(rho_tag), run_time=0.9)
    at_word(scene, t, 5, "expands", lead=0.4)
    play_in(scene, t, 6, tr.to(density_bars, 0.975, rate_func=smooth), *box.stage.turn(yaw=-0.35), run_time=5.4)

    # --- 6. At T_c the densities meet; the surface fades and vanishes ---------------------------------------------------------
    beat(scene, t, 6)
    scene.play(tr.to(density_bars, 1.0, rate_func=smooth), run_time=3.6)
    flash = Circle(radius=0.6, stroke_color=cfg.CRITICAL, stroke_width=6).move_to(box.stage.screen_point(
        box.chamber.point(0.5, 0.5, 0.5)))
    equal = txt("equal", cfg.FONT["label"], cfg.CRITICAL).move_to([6.4, 0.2, 0])
    play_in(scene, t, 7, FadeIn(flash), flash.animate.scale(2.4).set_stroke(opacity=0), FadeIn(equal, shift=DOWN * 0.1),
            run_time=1.4)
    scene.remove(flash)

    # --- 7. Below: liquid and vapour. Above: one fluid ---------------------------------------------------------------------------
    beat(scene, t, 7)
    below = VGroup(eq(r"T < T_c", cfg.FONT["label"], cfg.MUTED), txt("two phases can coexist", cfg.FONT["label"], cfg.COEXIST))
    above = VGroup(eq(r"T > T_c", cfg.FONT["label"], cfg.MUTED), txt("one fluid", cfg.FONT["label"], cfg.SUPERCRITICAL))
    for g in (below, above):
        g.arrange(RIGHT, buff=0.3)
    fit_width(below, 6.5)
    summary = VGroup(below, above).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.85, -3.2, 0])
    scene.play(FadeIn(below, shift=UP * 0.1), run_time=0.8)
    scene.play(FadeIn(above, shift=UP * 0.1), tr.to(density_bars, TR_END), run_time=1.6)
    finish(scene, t, box.stage)
