"""Scene 07 — hotter and lighter. A turning glass box of nitrogen sits on a
hot plate beside its Maxwell-Boltzmann curve. As the plate heats the gas from
300 K to 600 K the curve (live, ``pm.mb_pdf`` at the box's own temperature)
slides right and flattens; its shaded area is integrated every frame and
stays 1.00, which is why the peak must drop. Then the energy bookkeeping:
<K> = 3/2 k_B T, two bars show the average kinetic energy doubling, while the
most probable speed moves only from one dashed marker to the other, x1.41
(``pm.SPEEDS.heat_factor``): speed grows as the square root of temperature.

Mass next: the box now holds nitrogen (blue) and chlorine (green-yellow, 2.53
times heavier, ``pm.SPEEDS.mass_ratio``) at the same temperature; the
chlorine molecules visibly dawdle. Their equal kinetic-energy bars stand side
by side, and chlorine's curve is narrower and peaks further left. The scene
ends on u ∝ sqrt(T / M).
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d
from manim_scenes.kit_d import at_word

S = pm.SPEEDS
M_N2, M_CL2 = pm.MOLAR_MASS["N2"], pm.MOLAR_MASS["Cl2"]
C_N2, C_CL2 = cfg.GAS_COLORS["N2"], cfg.GAS_COLORS["Cl2"]
U_MAX, Y_MAX = 1600.0, 3.4
BOX_AT = (-4.95, -0.45, 0.0)
LEFT_X = -4.95


class Scene07HotterLighter(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "07", TITLES["07"])
    axes = speed_axes(U_MAX, Y_MAX, at=[2.2, -0.35, 0], x_length=8.0, y_length=4.5, ticks=(400, 800, 1200))
    box = GasBox(BOX_AT, count=70, half_x=1.15, half_z=0.9, height=2.3, floor=-1.15, heater=True, zoom=1.18, yaw=-0.6,
                 pitch=0.3, speed=1.3, t_ref=S.T1)
    temp = readout("T =", box.kelvin, 0, "K", cfg.TEMPERATURE, size=46).move_to([LEFT_X, 2.35, 0])

    def live_curve() -> VGroup:
        return mb_curve(axes, box.kelvin(), M_N2, cfg.GOLD, u_max=U_MAX, fill_opacity=0.2)

    curve = live(VGroup(), live_curve)
    ghost = mb_curve(axes, S.T1, M_N2, cfg.MUTED, u_max=U_MAX, width=3)
    ghost_d = DashedVMobject(ghost.core, num_dashes=50)
    us = np.linspace(0, U_MAX * 1.6, 600)
    area_head = txt("area =", cfg.FONT["label"], cfg.GOLD)
    area_value = DecimalNumber(1.0, num_decimal_places=2, font_size=48, color=cfg.GOLD)
    area_value.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
    area = VGroup(area_head, area_value).arrange(RIGHT, buff=0.2).move_to(axes.c2p(1180, 2.75))
    area_value.add_updater(lambda m: m.set_value(float(np.trapezoid(pm.mb_pdf(us, box.kelvin(), M_N2), us))))

    # --- 0. Nitrogen at 300 K, about to be heated ------------------------------------------------------------------------
    show(scene, box.stage, 1.0, Create(axes), FadeIn(temp))
    scene.add(curve)
    scene.play(FadeIn(curve), *box.stage.turn(yaw=-0.45), run_time=1.0)
    at_word(scene, t, 0, "six", lead=0.3)
    play_in(scene, t, 1, *box.heater_on(1.0), run_time=1.0)

    # --- 1. Hotter: the curve shifts right, spreads, and its peak drops (area stays 1) ----------------------------------
    beat(scene, t, 1)
    scene.add(ghost_d)
    scene.play(box.heat_to(S.T2, rate_func=smooth), box.cloud.tween("warmth", 0.5), *box.stage.turn(yaw=-0.2), run_time=3.6)
    at_word(scene, t, 1, "peak", lead=0.3)
    peak_old = glow_dot(axes.c2p(pm.u_mp(S.T1, M_N2), float(pm.mb_pdf(pm.u_mp(S.T1, M_N2), S.T1, M_N2)) * PDF_SCALE), cfg.MUTED)
    peak_new = glow_dot(axes.c2p(pm.u_mp(S.T2, M_N2), float(pm.mb_pdf(pm.u_mp(S.T2, M_N2), S.T2, M_N2)) * PDF_SCALE), cfg.GOLD)
    drop = arrow2d(peak_old.get_center() + RIGHT * 0.12, peak_new.get_center() + UL * 0.12, cfg.WHITE, width=0.05, tip_len=0.16)
    scene.play(FadeIn(peak_old), FadeIn(peak_new), FadeIn(drop), run_time=1.0)
    at_word(scene, t, 1, "area", lead=0.2)
    scene.add(area)
    scene.play(FadeIn(area, shift=DOWN * 0.1), run_time=0.8)
    at_word(scene, t, 1, "one", lead=0.2)
    play_in(scene, t, 2, Indicate(area, color=cfg.WHITE, scale_factor=1.12), run_time=1.2)

    # --- 2. <K> = 3/2 kT doubles; the speeds rise only by sqrt 2 ----------------------------------------------------------
    beat(scene, t, 2)
    area.clear_updaters()
    hide(scene, box.stage, 0.8, FadeOut(VGroup(peak_old, peak_new, drop, area)), FadeOut(temp))
    k_eq = paint(eq([r"\langle K\rangle", "=", r"\tfrac32", "k_B", "T"], cfg.FONT["section"]), {0: cfg.GOLD, 4: cfg.TEMPERATURE})
    k_eq.move_to([LEFT_X, 2.3, 0])
    scene.play(Write(k_eq), run_time=1.4)
    base_y = -0.9
    bar_k1 = Rectangle(width=0.9, height=1.2, stroke_color=cfg.GOLD, stroke_width=3, fill_color=cfg.GOLD, fill_opacity=0.45)
    bar_k2 = Rectangle(width=0.9, height=2.4, stroke_color=cfg.GOLD, stroke_width=3, fill_color=cfg.GOLD, fill_opacity=0.85)
    bar_k1.move_to([LEFT_X - 0.9, base_y + 0.6, 0])
    bar_k2.move_to([LEFT_X + 0.9, base_y + 1.2, 0])
    floor_line = Line([LEFT_X - 1.8, base_y, 0], [LEFT_X + 1.8, base_y, 0], stroke_color=cfg.MUTED, stroke_width=3)
    names = VGroup(txt(f"{fx(S.T1, 0)} K", cfg.FONT["small"], cfg.MUTED).next_to(bar_k1, DOWN, buff=0.2),
                   txt(f"{fx(S.T2, 0)} K", cfg.FONT["small"], cfg.TEMPERATURE).next_to(bar_k2, DOWN, buff=0.2))
    names[1].match_y(names[0])
    twice = txt("×2", cfg.FONT["section"], cfg.GOLD).next_to(bar_k2, RIGHT, buff=0.25).shift(UP * 0.5)
    at_word(scene, t, 2, "doubling", lead=0.3)
    scene.play(Create(floor_line), GrowFromEdge(bar_k1, DOWN), FadeIn(names[0]), run_time=1.0)
    scene.play(GrowFromEdge(bar_k2, DOWN), FadeIn(names[1]), run_time=1.2)
    at_word(scene, t, 2, "kinetic", nth=2, lead=0.3)
    scene.play(FadeIn(twice, scale=1.3), run_time=0.8)
    at_word(scene, t, 2, "speeds", lead=0.3)
    u1, u2 = pm.u_mp(S.T1, M_N2), pm.u_mp(S.T2, M_N2)
    m1 = speed_marker(axes, u1, S.T1, M_N2, cfg.MUTED)
    m2 = speed_marker(axes, u2, S.T2, M_N2, cfg.GOLD)
    y_gain = axes.c2p(0, 0)[1] - 0.9
    gain = arrow2d([axes.c2p(u1, 0)[0], y_gain, 0], [axes.c2p(u2, 0)[0], y_gain, 0], cfg.GOLD, width=0.08, tip_len=0.22)
    factor = txt(f"×{fx(S.heat_factor, 2)}", cfg.FONT["section"], cfg.GOLD).next_to(gain, RIGHT, buff=0.2)
    scene.play(Create(m1.line), FadeIn(m1.dot), Create(m2.line), FadeIn(m2.dot), run_time=1.0)
    scene.play(FadeIn(gain, shift=RIGHT * 0.15), run_time=0.8)
    at_word(scene, t, 2, "four", lead=0.3)
    root2 = eq(r"\times\sqrt2", cfg.FONT["section"], cfg.GOLD).move_to([LEFT_X, -2.75, 0])
    play_in(scene, t, 3, FadeIn(factor, shift=LEFT * 0.1), FadeIn(root2, shift=UP * 0.1), run_time=1.0)

    # --- 3. Speed grows as the square root of temperature --------------------------------------------------------------
    beat(scene, t, 3)
    law_t = boxed(eq(r"u\propto\sqrt{T}", cfg.FONT["title"], cfg.WHITE), cfg.GOLD).move_to([LEFT_X, -2.75, 0])
    paint(law_t.body, {})
    law_t.body[0][-1].set_color(cfg.TEMPERATURE)
    play_in(scene, t, 4, fade_through(root2, law_t.body), Create(law_t.frame), run_time=1.4)

    # --- 4. Mass: nitrogen and chlorine at the same temperature ---------------------------------------------------------
    beat(scene, t, 4)
    curve.clear_updaters()
    left_stuff = VGroup(k_eq, bar_k1, bar_k2, floor_line, names, twice, law_t)
    scene.play(FadeOut(left_stuff), FadeOut(VGroup(curve, ghost_d, m1, m2, gain, factor)), run_time=0.9)
    scene.remove(root2)
    n = 72
    species = np.array([0, 1] * (n // 2))
    mixed = GasBox(BOX_AT, count=n, half_x=1.15, half_z=0.9, height=2.3, floor=-1.15, zoom=1.18, yaw=-0.6, pitch=0.3,
                   speed=1.5, species=species, masses=(1.0, S.mass_ratio), colors=(C_N2, C_CL2), radius=0.08,
                   seed=cfg.SEED + 71)
    n2_curve = mb_curve(axes, S.T1, M_N2, C_N2, u_max=U_MAX, fill_opacity=0.15)
    cl_curve = mb_curve(axes, S.T1, M_CL2, C_CL2, u_max=U_MAX, fill_opacity=0.15)
    legend = VGroup(txt("N₂", cfg.FONT["label"], C_N2), txt("Cl₂", cfg.FONT["label"], C_CL2)).arrange(DOWN, buff=0.25,
                                                                                                    aligned_edge=LEFT)
    legend.move_to(axes.c2p(1300, 3.15))
    same_t = chip(f"same T = {fx(S.T1, 0)} K", cfg.TEMPERATURE, cfg.FONT["small"]).move_to([LEFT_X, 2.35, 0])
    show(scene, mixed.stage, 1.0, FadeIn(same_t, shift=DOWN * 0.1))
    scene.play(Create(n2_curve), FadeIn(legend[0]), run_time=1.2)
    scene.play(Create(cl_curve), FadeIn(legend[1]), run_time=1.2)
    at_word(scene, t, 4, "same", nth=2, lead=0.3)
    k_eq2 = paint(eq([r"\langle K\rangle_{\mathrm{N_2}}", "=", r"\langle K\rangle_{\mathrm{Cl_2}}"], cfg.FONT["label"]),
                  {0: C_N2, 2: C_CL2}).move_to([LEFT_X, -2.75, 0])
    play_in(scene, t, 5, FadeIn(k_eq2, shift=UP * 0.1), *mixed.stage.turn(yaw=-0.4), run_time=1.2)

    # --- 5. Heavier: slower, narrower, further left ------------------------------------------------------------------------
    beat(scene, t, 5)
    heavier = txt(f"Cl₂ ≈ {fx(S.mass_ratio, 1)} × heavier", cfg.FONT["small"], C_CL2).move_to([LEFT_X, -3.55, 0])
    scene.play(FadeIn(heavier, shift=UP * 0.1), run_time=0.8)
    at_word(scene, t, 5, "slowly", lead=0.3)
    scene.play(mixed.cloud.tween("radius", 0.1, rate_func=there_and_back), run_time=1.4)
    at_word(scene, t, 5, "narrower", lead=0.3)
    p_cl = speed_marker(axes, S.heavy_mp, S.T1, M_CL2, C_CL2)
    p_n2 = speed_marker(axes, S.mp, S.T1, M_N2, C_N2)
    scene.play(Indicate(cl_curve, color=cfg.WHITE, scale_factor=1.02), run_time=1.0)
    play_in(scene, t, 6, Create(p_cl.line), FadeIn(p_cl.dot), Create(p_n2.line), FadeIn(p_n2.dot), run_time=1.2)

    # --- 6. u ∝ 1 / sqrt(M) ------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    law_m = boxed(eq(r"u\propto\frac{1}{\sqrt{M}}", cfg.FONT["section"], cfg.WHITE), cfg.GOLD).move_to(axes.c2p(1180, 1.3))
    scene.play(FadeIn(law_m.body, shift=UP * 0.1), Create(law_m.frame), run_time=1.2)
    at_word(scene, t, 6, "Light", lead=0.2)
    scene.play(Indicate(legend[0], color=cfg.WHITE, scale_factor=1.15), run_time=0.9)
    at_word(scene, t, 6, "Heavy", lead=0.2)
    play_in(scene, t, 7, Indicate(legend[1], color=cfg.WHITE, scale_factor=1.15), run_time=0.9)

    # --- 7. Both together -----------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    both = eq([r"u", r"\propto", r"\sqrt{\frac{T}{M}}"], cfg.FONT["title"], cfg.WHITE)
    both_box = boxed(both, cfg.GOLD, buff=0.24).move_to(law_m)
    swap(scene, law_m, both_box, run_time=1.4)
    scene.remove(law_m, law_m.body, law_m.frame)
    finish(scene, t, mixed.stage)
