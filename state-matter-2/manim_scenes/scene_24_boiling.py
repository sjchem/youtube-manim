"""Scene 24 — why liquids boil. Vapour-pressure curves of diethyl ether,
ethanol and water (``pm.vapour_pressure``: IAPWS for water, Antoine fits for ether and ethanol) rise with
temperature on the left; on the right a 3D pool evaporates from its surface
(``kit_f.Escapes``), then, on a glowing hot plate, boils: vapour bubbles
nucleate on the floor, grow, rise and burst (``kit_f.Bubbles``).

A bubble cross-section shows the balance: vapour pressure pushing out, the
outside pressure pushing in; ordinary boiling has P_vap approximately P_ext; the narration names curvature and depth corrections. A teal line of
external pressure crosses the three curves at 1 atm (boiling points from
``pm.boiling_point``: about 35, 78 and 100 °C), drops to Everest's summit
pressure (``pm.EVEREST_BAR``: water boils near 70 °C) and rises to a pressure
cooker's 2 bar (``pm.COOKER_BAR``: near 120 °C) while a steel lid drops on the
pool. At 20 °C ether's vapour pressure towers over water's: volatile.
Finally a sealed vessel heated far beyond: the pressure is not atmosphere-fixed, and its saturation pressure
climbs along water's whole curve to its critical point (374 °C, 220.6 bar)
and the surface fades away as a single fluid fills the box. Sealing alone does not forbid boiling.
"""

from manim_scenes.common import *
from manim_scenes.kit_a import arrow2d
from manim_scenes.kit_d import at_word
from manim_scenes.kit_f import Bubbles, Escapes, GlassLid, SteelLid, sink_heater

LIQUIDS = ("ether", "ethanol", "water")
NAMES = {"ether": "ether", "ethanol": "ethanol", "water": "water"}
COLORS = {"ether": cfg.GOLD, "ethanol": cfg.ROSE, "water": cfg.GAS_COLORS["H2O"]}
T_MAX, P_TOP = 130.0, 2.4
BOX_AT = (4.55, -0.3, 0.0)
PLOT_AT = [-3.0, -0.05, 0]


class Scene24Boiling(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "24", TITLES["24"])
    axes = plot_axes((0, T_MAX), (0, P_TOP), x_length=7.6, y_length=4.8, at=PLOT_AT, x_label="T", y_label="P",
                     x_color=cfg.TEMPERATURE, y_color=cfg.PRESSURE, x_ticks=(25, 50, 75, 100, 125), y_ticks=(1, 2))
    t_unit = txt("°C", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.labels[0], RIGHT, buff=0.1, aligned_edge=DOWN)
    p_unit = txt("bar", cfg.FONT["tiny"], cfg.MUTED).next_to(axes.labels[1], RIGHT, buff=0.1)
    axes.add(decorative(t_unit), decorative(p_unit))
    curves = {}
    for liquid in LIQUIDS:
        ts = np.linspace(0, T_MAX, 200)
        ps = np.array([pm.vapour_pressure(liquid, x) for x in ts])
        keep = ps <= P_TOP
        core = polyline([axes.c2p(a, b) for a, b in zip(ts[keep], ps[keep])], COLORS[liquid], width=6)
        p_label = {"ether": 2.25, "ethanol": 1.75, "water": 1.5}[liquid]
        t_label = float(np.interp(p_label, ps, ts))
        name = txt(NAMES[liquid], cfg.FONT["small"], COLORS[liquid]).next_to(axes.c2p(t_label, p_label), LEFT, buff=0.15)
        curves[liquid] = VGroup(core.copy().set_stroke(width=18, opacity=0.14), core, name)

    # --- 0. Vapour pressures rise with temperature -----------------------------------------------------------------------
    scene.play(Create(axes), run_time=1.2)
    for liquid in LIQUIDS:
        at_word(scene, t, 0, liquid if liquid != "ether" else "diethyl", lead=0.2)
        scene.play(Create(curves[liquid][:2]), FadeIn(curves[liquid][2]), run_time=1.1)

    # --- 1. Evaporation at the surface; boiling throughout ------------------------------------------------------------------
    beat(scene, t, 1)
    box = TwoPhaseBox(BOX_AT, lid="open", count=60, active=0, level=1.15, half_x=1.25, half_z=0.95, height=2.6, floor=-1.3,
                      heater=True, zoom=1.15, yaw=-0.55, pitch=0.32, speed=1.4, liquid_spacing=0.22, seed=cfg.SEED + 240)
    sink_heater(box)
    hops = Escapes(box, rate=4.0, fast=0.35)
    bubbles = Bubbles(box, rate=0.0, on_pop=lambda p: hops.burst(p, 1))
    box.stage.add_body(bubbles)
    show(scene, box.stage, 1.0)
    evap = txt("surface evaporation", cfg.FONT["small"], cfg.GOLD).move_to([BOX_AT[0], 3.25, 0]).set_z_index(2)
    scene.play(FadeIn(evap, shift=UP * 0.1), run_time=0.8)
    at_word(scene, t, 1, "Bubbles", lead=0.4)
    boil = txt("bulk boiling", cfg.FONT["small"], cfg.VAPOUR).move_to([BOX_AT[0], 2.5, 0]).set_z_index(2)
    scene.play(*box.heater_on(1.0), bubbles.tween_rate(7.0), FadeIn(boil, shift=UP * 0.1), run_time=1.4)
    play_in(scene, t, 2, *box.stage.turn(yaw=-0.4), run_time=3.0)

    # --- 2. A bubble survives if its vapour pushes back as hard as the outside ------------------------------------------------
    beat(scene, t, 2)
    plot = VGroup(axes, *curves.values())
    scrim = Rectangle(width=plot.width + 1.4, height=plot.height + 1.0, stroke_width=0, fill_color=cfg.BG,
                      fill_opacity=1.0).move_to(plot)
    scene.play(FadeIn(scrim), run_time=0.7)
    centre = np.array([PLOT_AT[0] + 0.2, 0.2, 0])
    bubble = VGroup(Circle(radius=1.25, stroke_color=mu.mix(cfg.LIQUID_EDGE, cfg.WHITE, 0.4), stroke_width=5, fill_color=cfg.VAPOUR,
                           fill_opacity=0.12),
                    Circle(radius=2.6, stroke_width=0, fill_color=cfg.LIQUID, fill_opacity=0.25)).move_to(centre)
    bubble[1].set_z_index(-1)
    outs, ins = VGroup(), VGroup()
    for k in range(8):
        d = np.array([np.cos(k * PI / 4), np.sin(k * PI / 4), 0])
        outs.add(arrow2d(centre + d * 0.45, centre + d * 1.15, cfg.VAPOUR, width=0.08, tip_len=0.22))
        ins.add(arrow2d(centre + d * 2.15, centre + d * 1.4, cfg.PRESSURE, width=0.08, tip_len=0.22))
    scene.play(FadeIn(bubble, scale=0.6), run_time=0.9)
    at_word(scene, t, 2, "vapour", lead=0.3)
    vap_tag = eq(r"P_{\text{vap}}", cfg.FONT["section"], cfg.VAPOUR).move_to(centre + DOWN * 0.05)
    scene.play(LaggedStart(*[FadeIn(a, scale=0.5) for a in outs], lag_ratio=0.08),
               FadeIn(vap_tag), run_time=1.2)
    at_word(scene, t, 2, "outside", lead=0.3)
    ext_tag = eq(r"P_{\text{ext}}", cfg.FONT["section"], cfg.PRESSURE).move_to(centre + UR * 2.05 + RIGHT * 0.4)
    scene.play(LaggedStart(*[FadeIn(a, scale=0.5) for a in ins], lag_ratio=0.08), FadeIn(ext_tag), run_time=1.2)
    at_word(scene, t, 2, "boiling", lead=0.3)
    rule = boxed(paint(eq([r"P_{\text{vap}}", r"\approx", r"P_{\text{ext}}"], cfg.FONT["title"]), {0: cfg.VAPOUR, 2: cfg.PRESSURE}), cfg.GOLD)
    rule.move_to(centre + DOWN * 3.0)
    play_in(scene, t, 3, FadeIn(rule, shift=UP * 0.1), run_time=1.2)

    # --- 3. At one atmosphere ---------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(bubble, outs, ins, vap_tag, ext_tag, rule)), FadeOut(scrim), FadeOut(VGroup(evap, boil)), run_time=0.6)
    rule.scale(0.55).move_to([PLOT_AT[0] + 0.6, 3.1, 0])
    scene.play(FadeIn(rule), run_time=0.4)
    p_ext = Knob(pm.ATM_BAR)
    line = live(VGroup(), lambda: VGroup(Line(axes.c2p(0, p_ext.value), axes.c2p(T_MAX, p_ext.value), stroke_color=cfg.PRESSURE,
                                              stroke_width=5),
                                         txt(f"{fx(p_ext.value, 2)} bar", cfg.FONT["small"], cfg.PRESSURE)
                                         .next_to(axes.c2p(T_MAX, p_ext.value), RIGHT, buff=0.12)))

    def meets() -> VGroup:
        group = VGroup()
        for liquid in LIQUIDS:
            bp = pm.boiling_point(liquid, p_ext.value)
            if bp > T_MAX:
                continue
            pt = axes.c2p(bp, p_ext.value)
            group.add(DashedLine(pt, axes.c2p(bp, 0), stroke_color=COLORS[liquid], stroke_width=3, dash_length=0.1),
                      glow_dot(pt, COLORS[liquid], radius=0.11))
        return group

    hits = live(VGroup(), meets)
    scene.add(line)
    scene.play(FadeIn(line), run_time=0.8)
    scene.add(hits)
    atm = txt("1 atm", cfg.FONT["label"], cfg.PRESSURE).move_to(axes.c2p(9, pm.ATM_BAR) + UP * 0.32)
    scene.play(FadeIn(hits), FadeIn(atm), run_time=0.9)
    readouts = VGroup()
    for liquid, word in zip(LIQUIDS, ("thirty", "seventy", "hundred")):
        at_word(scene, t, 3, word, lead=0.3)
        bp = pm.boiling_point(liquid, pm.ATM_BAR)
        r = txt(f"{fx(bp, 0)} °C", cfg.FONT["small"], COLORS[liquid]).next_to(axes.c2p(bp, 0), DOWN,
                         buff=1.15 if liquid == "water" else 0.55)
        readouts.add(r)
        scene.play(FadeIn(r, shift=UP * 0.1), run_time=0.6)

    # --- 4. Lower pressure: Everest -------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(readouts), FadeOut(atm), run_time=0.6)
    scene.play(p_ext.to(line, pm.EVEREST_BAR, rate_func=smooth), run_time=3.0)
    everest = chip("summit of Everest", cfg.MUTED, cfg.FONT["small"]).move_to([BOX_AT[0], 3.15, 0])
    bp_ev = pm.boiling_point("water", pm.EVEREST_BAR)
    ev_read = txt(f"water ≈ {fx(round(bp_ev, -1), 0)} °C", cfg.FONT["label"], COLORS["water"]).next_to(everest, DOWN, buff=0.2)
    scene.play(FadeIn(everest, shift=DOWN * 0.1), FadeIn(ev_read, shift=DOWN * 0.1), run_time=1.0)
    at_word(scene, t, 4, "slowly", lead=0.3)
    play_in(scene, t, 5, Indicate(ev_read, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)

    # --- 5. Higher pressure: a pressure cooker ------------------------------------------------------------------------------------
    beat(scene, t, 5)
    cooker = SteelLid(box, lift=1.6)
    scene.play(FadeOut(VGroup(everest, ev_read)), p_ext.to(line, pm.COOKER_BAR, rate_func=smooth), *cooker.drop(), run_time=3.0)
    bp_ck = pm.boiling_point("water", pm.COOKER_BAR)
    ck_tag = chip("cooker · 2 bar absolute", cfg.STEEL, cfg.FONT["small"]).move_to([BOX_AT[0], 3.15, 0])
    ck_read = txt(f"water ≈ {fx(round(bp_ck, -1), 0)} °C", cfg.FONT["label"], COLORS["water"]).next_to(ck_tag, DOWN, buff=0.2)
    at_word(scene, t, 5, "twenty", lead=0.4)
    scene.play(FadeIn(ck_tag, shift=DOWN * 0.1), FadeIn(ck_read, shift=DOWN * 0.1), run_time=1.0)
    play_in(scene, t, 6, Indicate(ck_read, color=cfg.WHITE, scale_factor=1.08), run_time=1.0)

    # --- 6. Volatile: a high vapour pressure at room temperature -------------------------------------------------------------------
    beat(scene, t, 6)
    hits.clear_updaters()
    line.clear_updaters()
    scene.play(FadeOut(VGroup(ck_tag, ck_read, hits, line)), *cooker.raise_off(), bubbles.tween_rate(0.0), *box.heater_on(0.0),
               run_time=1.0)
    room = DashedLine(axes.c2p(20, 0), axes.c2p(20, P_TOP * 0.92), stroke_color=cfg.MUTED, stroke_width=3, dash_length=0.1)
    room_tag = txt("20 °C", cfg.FONT["small"], cfg.MUTED).next_to(axes.c2p(20, 0), DOWN, buff=0.55)
    v_e = glow_dot(axes.c2p(20, pm.vapour_pressure("ether", 20)), COLORS["ether"], radius=0.13)
    v_w = glow_dot(axes.c2p(20, pm.vapour_pressure("water", 20)), COLORS["water"], radius=0.13)
    scene.play(Create(room), FadeIn(room_tag), FadeIn(v_e, scale=1.5), FadeIn(v_w, scale=1.5), run_time=1.0)
    at_word(scene, t, 6, "volatile", lead=0.3)
    vol = result_label("volatile", COLORS["ether"], cfg.FONT["section"]).next_to(v_e, RIGHT, buff=0.3)
    play_in(scene, t, 7, FadeIn(vol, shift=LEFT * 0.1), run_time=1.0)

    # --- 7. In a sealed container: no boiling; the pressure climbs to the critical point ------------------------------------------
    beat(scene, t, 7)
    lid = GlassLid(box, lift=1.3)
    scene.play(FadeOut(VGroup(plot, room, room_tag, v_e, v_w, vol, rule)), *lid.lower(), hops.tween_rate(0.0), run_time=1.2)
    tc_water = pm.celsius(pm.WATER_TC)
    big = plot_axes((0, 400), (0, 240), x_length=7.6, y_length=4.8, at=PLOT_AT, x_label="T", y_label="P",
                    x_color=cfg.TEMPERATURE, y_color=cfg.PRESSURE, x_ticks=(100, 200, 300, 400), y_ticks=(100, 200))
    big_units = VGroup(txt("°C", cfg.FONT["tiny"], cfg.MUTED).next_to(big.labels[0], RIGHT, buff=0.1, aligned_edge=DOWN),
                       txt("bar", cfg.FONT["tiny"], cfg.MUTED).next_to(big.labels[1], RIGHT, buff=0.1))
    big.add(decorative(big_units))
    water_ts = np.linspace(0, tc_water, 220)
    water_ps = [pm.vapour_pressure("water", x) for x in water_ts]
    heat = Knob(100.0)
    full = live(VGroup(), lambda: polyline([big.c2p(a, b) for a, b in zip(water_ts, water_ps) if a <= heat.value] +
                                           [big.c2p(heat.value, pm.vapour_pressure("water", heat.value))],
                                           COLORS["water"], width=6))
    dot = live(VGroup(), lambda: glow_dot(big.c2p(heat.value, pm.vapour_pressure("water", heat.value)), COLORS["water"], 0.12))
    sealed = chip("sealed · pressure rises", cfg.GLASS, cfg.FONT["small"]).move_to([PLOT_AT[0], 2.95, 0])
    scene.play(Create(big), FadeIn(sealed, shift=DOWN * 0.1), run_time=1.0)
    scene.add(full, dot)
    at_word(scene, t, 7, "raise", lead=0.3)
    fade_surface = Knob(1.0)

    def surface_alpha() -> None:
        for face in box.liquid_faces:
            face.presence = fade_surface.value
        box.liquid_dots.alpha = fade_surface.value
        box.level = 1.15 * fade_surface.value
        box.set_vapour(int(round(80 * (1 - fade_surface.value))))

    box.stage.bodies.insert(0, Ticker(surface_alpha))
    scene.play(*box.heater_on(1.0), heat.to(full, tc_water, rate_func=smooth), run_time=4.0)
    cp = glow_dot(big.c2p(tc_water, pm.WATER_PC_BAR), cfg.CRITICAL, radius=0.16, reach=4)
    cp_tag = result_label("critical point", cfg.CRITICAL, cfg.FONT["label"]).next_to(cp, LEFT, buff=0.3)
    at_word(scene, t, 7, "vanishes", lead=0.5)
    scene.play(FadeIn(cp, scale=2), FadeIn(cp_tag, shift=RIGHT * 0.1), fade_surface.to(full, 0.0), run_time=1.6)
    finish(scene, t, box.stage, drift=0.15)
