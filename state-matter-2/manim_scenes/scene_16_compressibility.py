"""Scene 16 — one number for non-ideality. A glass box of gas turns on the
left while the compressibility factor is built large on the right: P V over
n R T, named Z. For the ideal gas the box is squeezed and heated while a live
Z read from the model stays at 1.00 (purple, the idealised limit). The box
becomes the CO2 flask of scene 15 and a bar of length Z falls ten percent short
of the ideal bar (pm.FLASK.Z).

Then Z against pressure at 300 K for CH4, N2, H2 and He, from the van der Waals
model (pm.z_vdw): a dashed purple Z = 1 "ideal" line, a soft green zone below
("attraction wins") and a red zone above ("size wins"). Each curve grows with a
bead at its tip as the gas is named, first to moderate pressure (methane dips,
nitrogen barely, hydrogen and helium rise at once), then all to 600 bar, where
every curve has climbed into the red.

Finally Z = V_real / V_ideal: two 3D boxes under identical weighted pistons
(same P) at the same T and n. The real gas's volume shrinks to 80 % (green
attraction links, green arrows: "pulled tighter") and then swells to 120 %
(bigger molecules, red arrows: "pushed apart"), against a dashed outline of the
ideal volume; a live Z reads the volume ratio.
"""

from manim_scenes.common import *
from manim_scenes.kit_d import *

GASES = ("CH4", "N2", "H2", "He")
NAMES = {"CH4": "CH₄", "N2": "N₂", "H2": "H₂", "He": "He"}
T_PLOT = pm.ROOM_T
P_TOP, P_FIRST = 600.0, 250.0          # beat 4 draws to moderate pressure, beat 5 to the top
Z_RANGE = (0.7, 1.7)
H_IDEAL = 2.0                          # drawn height of the ideal gas in the last beats


class Scene16Compressibility(Scene):
    def construct(self) -> None:
        play_scene(self)


def fraction(top: Mobject, bottom: Mobject, width: float = 6) -> VGroup:
    bar = Line(LEFT, RIGHT, stroke_color=cfg.WHITE, stroke_width=width).set_width(max(top.width, bottom.width) + 0.35)
    group = VGroup(top, bar, bottom).arrange(DOWN, buff=0.2)
    group.top, group.bar, group.bottom = top, bar, bottom
    return group


def z_equation(top: Mobject, bottom: Mobject, size: int) -> VGroup:
    frac = fraction(top, bottom)
    lhs = paint(eq(["Z", "="], size), {0: cfg.GOLD})
    lhs.next_to(frac, LEFT, buff=0.3).match_y(frac.bar)
    group = VGroup(lhs, frac)
    group.lhs, group.frac = lhs, frac
    return group


def value_row(name: str, color: str, x_bar: float, y: float, length: float) -> VGroup:
    label = txt(name, cfg.FONT["label"], color)
    label.next_to([x_bar - 0.22, y, 0], LEFT, buff=0)
    frame = Rectangle(width=length, height=0.46, stroke_color=color, stroke_width=3, fill_opacity=0)
    frame.move_to([x_bar + length / 2, y, 0])
    return VGroup(label, frame)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", TITLES["16"])

    # --- 1. Z = PV / nRT, beside a box of gas ---------------------------------------------------------------------------------
    box = GasBox((-4.3, -0.55, 0), count=60, half_x=1.3, half_z=1.0, height=2.5, floor=-1.25, zoom=1.05, yaw=-0.7,
                 pitch=0.32, speed=1.5)
    show(scene, box.stage, 1.0)
    num = paint(eq(["P", "V"], cfg.FONT["hero"]), {0: cfg.PRESSURE, 1: cfg.VOLUME})
    den = paint(eq(["n", "R", "T"], cfg.FONT["hero"]), {0: cfg.AMOUNT, 2: cfg.TEMPERATURE})
    law = z_equation(num, den, cfg.FONT["hero"]).move_to([3.2, 1.75, 0])
    name = txt("compressibility factor", cfg.FONT["label"], cfg.GOLD).move_to([3.2, 0.05, 0])
    at_word(scene, t, 0, "Divide", lead=0.2)
    scene.play(Write(num), *box.stage.turn(yaw=-0.55), run_time=1.0)
    scene.play(GrowFromCenter(law.frac.bar), Write(den), run_time=1.1)
    at_word(scene, t, 0, "ratio", lead=0.2)
    scene.play(FadeIn(law.lhs, shift=RIGHT * 0.3), run_time=0.8)
    at_word(scene, t, 0, "factor", lead=0.3)
    scene.play(FadeIn(name, shift=UP * 0.15), run_time=0.8)
    scene.play(Circumscribe(law, color=cfg.GOLD, buff=0.18), run_time=1.4)

    # --- 2. Ideal gas: Z = 1 under every condition ------------------------------------------------------------------------------
    beat(scene, t, 1)
    x_bar, length = 1.95, 3.6

    def z_ideal() -> float:
        return box.pressure() * box.chamber.volume_ratio() / (box.kelvin() / box.t_ref)

    ideal_row = value_row("ideal", cfg.LIMIT, x_bar, -1.15, length)
    ideal_fill = always_redraw(lambda: Rectangle(width=length * z_ideal(), height=0.46, stroke_width=0, fill_color=cfg.LIMIT,
                                                 fill_opacity=0.45).move_to([x_bar + length * z_ideal() / 2, -1.15, 0]))
    ideal_value = DecimalNumber(1.0, num_decimal_places=2, font_size=56, color=cfg.LIMIT)
    ideal_value.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
    ideal_value.next_to(ideal_row[1], RIGHT, buff=0.25)
    ideal_value.add_updater(lambda m: m.set_value(z_ideal()))
    scene.play(FadeIn(ideal_row), FadeIn(ideal_fill), FadeIn(ideal_value), run_time=0.9)
    at_word(scene, t, 1, "under", lead=0.4)
    scene.play(box.volume_to(0.55, run_time=2.0), box.heat_to(480.0, run_time=2.0), box.cloud.tween("warmth", 0.45, run_time=2.0),
               run_time=2.0)
    play_in(scene, t, 2, box.volume_to(1.25, run_time=1.6), box.heat_to(380.0, run_time=1.6), run_time=1.6)

    # --- 3. The CO2 flask: Z about 0.90 -----------------------------------------------------------------------------------------
    beat(scene, t, 2)
    flask = chip(f"CO₂ flask: Z ≈ {fx(pm.FLASK.Z, 2)}", cfg.GAS_COLORS["CO2"], cfg.FONT["small"]).move_to([-4.3, 2.45, 0])
    co2_row = value_row("CO₂", cfg.GAS_COLORS["CO2"], x_bar, -2.2, length)
    co2_fill = Rectangle(width=length * pm.FLASK.Z, height=0.46, stroke_width=0, fill_color=cfg.GAS_COLORS["CO2"],
                         fill_opacity=0.55)
    co2_fill.move_to([x_bar + length * pm.FLASK.Z / 2, -2.2, 0])
    co2_value = DecimalNumber(pm.FLASK.Z, num_decimal_places=2, font_size=56, color=cfg.GAS_COLORS["CO2"])
    co2_value.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
    co2_value.next_to(co2_row[1], RIGHT, buff=0.25)
    scene.play(box.volume_to(1.0, run_time=1.2), box.heat_to(pm.FLASK.T, run_time=1.2), box.cloud.tween("warmth", 0.0, run_time=1.2),
               FadeIn(flask, shift=DOWN * 0.15), run_time=1.2)
    scene.play(FadeIn(co2_row), GrowFromEdge(co2_fill, LEFT), run_time=1.4)
    scene.play(FadeIn(co2_value, shift=LEFT * 0.15), run_time=0.6)
    at_word(scene, t, 2, "Ten", lead=0.2)
    gap = Rectangle(width=length * (1 - pm.FLASK.Z), height=0.46, stroke_color=cfg.GOLD, stroke_width=3, fill_color=cfg.GOLD,
                    fill_opacity=0.25).move_to([x_bar + length * (1 + pm.FLASK.Z) / 2, -2.2, 0])
    short = txt(f"−{fx(pm.FLASK.percent_below, 0)} %", cfg.FONT["small"], cfg.GOLD).next_to(gap, DOWN, buff=0.18)
    scene.play(FadeIn(gap), FadeIn(short, shift=UP * 0.1), run_time=0.9)
    scene.play(Indicate(short, color=cfg.WHITE, scale_factor=1.15), run_time=1.1)

    # --- 4. Z against P at 300 K: the van der Waals model ------------------------------------------------------------------------
    beat(scene, t, 3)
    ideal_fill.clear_updaters()
    ideal_value.clear_updaters()
    corner = VGroup(law)
    hide(scene, box.stage, 0.9, FadeOut(VGroup(name, ideal_row, ideal_fill, ideal_value, co2_row, co2_fill, co2_value, gap, short,
                                              flask)),
         corner.animate.scale(0.5).move_to([5.6, 2.9, 0]))
    axes = plot_axes((0, P_TOP), Z_RANGE, x_length=9.6, y_length=5.2, at=[-1.4, -0.45, 0], x_label=r"P\ (\mathrm{bar})",
                     y_label="Z", x_color=cfg.PRESSURE, y_color=cfg.GOLD, x_ticks=(200, 400, 600), y_ticks=(0.8, 1.2, 1.4, 1.6))
    model = chip(f"van der Waals model, {fx(T_PLOT, 0)} K", cfg.MUTED, cfg.FONT["small"]).move_to([-1.4, 3.2, 0])
    green = band(axes, 0, P_TOP, Z_RANGE[0], 1.0, cfg.ATTRACT, 0.1)
    red = band(axes, 0, P_TOP, 1.0, Z_RANGE[1], cfg.SIZE, 0.08)
    one = DashedLine(axes.c2p(0, 1), axes.c2p(P_TOP, 1), stroke_color=cfg.LIMIT, stroke_width=4, dash_length=0.16)
    one_tag = txt("ideal", cfg.FONT["small"], cfg.LIMIT).next_to(axes.c2p(P_TOP, 1), RIGHT, buff=0.38)
    wins_a = txt("attraction wins", cfg.FONT["label"], cfg.ATTRACT).move_to(axes.c2p(440, 0.8))
    wins_b = txt("size wins", cfg.FONT["label"], cfg.SIZE).move_to(axes.c2p(140, 1.58))
    scene.play(Create(axes), FadeIn(model, shift=DOWN * 0.15), run_time=1.6)
    scene.play(Create(one), FadeIn(one_tag), run_time=1.0)
    scene.play(FadeIn(green), FadeIn(wins_a, shift=UP * 0.1), run_time=1.0)
    scene.play(FadeIn(red), FadeIn(wins_b, shift=DOWN * 0.1), run_time=1.0)
    sweep = Knob(0.0)
    ideal_bead = live(VGroup(), lambda: glow_dot(axes.c2p(sweep.value, 1.0), cfg.LIMIT, radius=0.1))
    scene.add(ideal_bead)
    fill_until(scene, t, 4, sweep.to(ideal_bead, P_TOP, rate_func=smooth))
    ideal_bead.clear_updaters()

    ps = np.linspace(0, P_TOP, 241)
    traces = {g: Trace(axes, ps, [pm.z_vdw(p, T_PLOT, g) for p in ps], cfg.GAS_COLORS[g]) for g in GASES}
    legend = VGroup(*[legend_row(NAMES[g], cfg.GAS_COLORS[g]) for g in GASES]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
    legend.move_to([5.75, 0.1, 0])

    # --- 5. Named one by one --------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    tr = traces["CH4"]
    scene.add(tr.curve, tr.bead)
    scene.play(tr.grow(P_FIRST, run_time=2.6, rate_func=smooth), FadeIn(legend[0], shift=LEFT * 0.2), FadeOut(ideal_bead),
               run_time=2.6)
    scene.play(Indicate(wins_a, color=cfg.WHITE, scale_factor=1.1), run_time=0.9)
    at_word(scene, t, 4, "Nitrogen", lead=0.1)
    tr = traces["N2"]
    scene.add(tr.curve, tr.bead)
    scene.play(tr.grow(P_FIRST, run_time=1.9, rate_func=smooth), FadeIn(legend[1], shift=LEFT * 0.2), run_time=1.9)
    at_word(scene, t, 4, "Hydrogen", lead=0.1)
    for g in ("H2", "He"):
        scene.add(traces[g].curve, traces[g].bead)
    scene.play(*[traces[g].grow(P_FIRST, run_time=2.4, rate_func=smooth) for g in ("H2", "He")],
               LaggedStart(FadeIn(legend[2], shift=LEFT * 0.2), FadeIn(legend[3], shift=LEFT * 0.2), lag_ratio=0.5), run_time=2.4)
    fill_until(scene, t, 5, *[set_attr(traces[g].curve, traces[g], "bead_radius", 0.15, rate_func=there_and_back)
                              for g in GASES])

    # --- 6. At very high pressure: size always wins -----------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*[traces[g].grow(P_TOP, run_time=4.0, rate_func=smooth) for g in GASES], red.animate.set_fill(opacity=0.17),
               run_time=4.0)
    at_word(scene, t, 5, "dominate", lead=0.3)
    always = glow_frame(wins_b, cfg.SIZE, buff=0.16)
    scene.play(Create(always), Indicate(wins_b, color=cfg.WHITE, scale_factor=1.15), run_time=1.2)
    fill_until(scene, t, 6, *[traces[g].fade_bead(0.0) for g in GASES])

    # --- 7. Z = V_real / V_ideal at the same P and T -----------------------------------------------------------------------------
    beat(scene, t, 6)
    for g in GASES:
        traces[g].stop()
    plot = VGroup(axes, model, green, red, one, one_tag, wins_a, wins_b, always, legend, corner,
                  *[traces[g].curve for g in GASES], *[traces[g].bead for g in GASES])
    scene.play(FadeOut(plot), run_time=0.8)
    scene.remove(*[traces[g].curve for g in GASES], *[traces[g].bead for g in GASES])
    kw = dict(count=48, half_x=1.15, half_z=0.95, height=H_IDEAL, floor=-1.1, lid="weight", zoom=1.25, pitch=0.3,
                  speed=1.4)
    ideal = GasBox((-4.6, -1.2, 0), seed=cfg.SEED + 16, yaw=-0.5, **kw)
    real = GasBox((4.0, -1.2, 0), seed=cfg.SEED + 17, yaw=-0.5, **kw)
    links = PairLinks(real.cloud, cutoff=0.44)
    real.stage.add_body(links)
    ch = real.chamber
    ghost = [Segment(ch.corner(sx, 0, sz) + np.array([0, H_IDEAL, 0]), ch.corner(tx, 0, tz) + np.array([0, H_IDEAL, 0]),
                     cfg.LIMIT, width=3.5, opacity=0.9, dashed=True)
             for (sx, sz), (tx, tz) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1)))]
    for g_ in ghost:
        g_.presence = 0.0
    real.stage.add_body(*ghost)
    lid_y = lambda: ch.top() + 0.16 + 0.42 / 2   # noqa: E731  (middle of the weight)
    side = ch.half_x + 0.45
    pulls = [Vector(lambda s=s: np.array([s * side, lid_y() + 0.75, 0.0]), lambda s=s: np.array([s * side, lid_y() - 0.15, 0.0]),
                    cfg.ATTRACT, width=0.11, tip=0.3) for s in (-1, 1)]
    pushes = [Vector(lambda s=s: np.array([s * side, lid_y() - 0.35, 0.0]), lambda s=s: np.array([s * side, lid_y() + 0.6, 0.0]),
                     cfg.SIZE, width=0.11, tip=0.3) for s in (-1, 1)]
    for v in (*pulls, *pushes):
        v.presence = 0.0
    real.stage.add_overlay(*pulls, *pushes)
    ideal_tag = txt("ideal gas", cfg.FONT["label"], cfg.LIMIT).move_to([-4.6, -3.6, 0])
    real_tag = txt("real gas", cfg.FONT["label"], cfg.MOLECULE).move_to([4.0, -3.6, 0])
    for stage in (ideal.stage, real.stage):
        stage.presence = 0.0
        stage.refresh()
        scene.add(stage)
    scene.play(ideal.stage.fade(ideal.stage, 1.0), real.stage.fade(real.stage, 1.0), FadeIn(ideal_tag), FadeIn(real_tag),
               run_time=1.1)
    same = VGroup(chip("same P", cfg.PRESSURE, cfg.FONT["small"]), chip("same T", cfg.TEMPERATURE, cfg.FONT["small"]))
    same.arrange(RIGHT, buff=0.3).move_to([-0.3, -1.05, 0])
    at_word(scene, t, 6, "same", lead=0.2)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in same], lag_ratio=0.4), run_time=1.2)
    v_top = eq(r"V_{\text{real}}", cfg.FONT["title"], cfg.VOLUME)
    v_bottom = eq(r"V_{\text{ideal}}", cfg.FONT["title"], cfg.VOLUME)
    ratio = z_equation(v_top, v_bottom, cfg.FONT["title"]).move_to([-0.3, 2.65, 0])
    at_word(scene, t, 6, "real", lead=0.3)
    scene.play(Write(ratio), run_time=1.6)
    fill_until(scene, t, 7, *ideal.stage.turn(yaw=-0.3), *real.stage.turn(yaw=-0.7))

    # --- 8. Z = 0.8: pulled tighter; Z = 1.2: pushed apart -------------------------------------------------------------------------
    beat(scene, t, 7)
    z_live = DecimalNumber(1.0, num_decimal_places=2, font_size=cfg.FONT["title"] * 1.3, color=cfg.WHITE)
    z_live.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
    z_head = paint(eq(["Z", "="], cfg.FONT["title"]), {0: cfg.GOLD})

    def z_now() -> float:
        return ch.height / H_IDEAL

    def place_z(m):
        z = z_now()
        m.set_value(z)
        m.set_color(cfg.ATTRACT if z < 0.995 else (cfg.SIZE if z > 1.005 else cfg.WHITE))
        m.next_to(z_head, RIGHT, buff=0.25)

    readout_row = VGroup(z_head, z_live)
    z_head.move_to([-1.15, 0.85, 0])
    z_live.add_updater(place_z)
    place_z(z_live)
    percent = DecimalNumber(100.0, num_decimal_places=0, unit=r"\%", font_size=cfg.FONT["section"] * 1.2, color=cfg.MUTED)
    percent.set_stroke(cfg.BG, width=0.6, opacity=0.85, background=True)
    percent.add_updater(lambda m: m.set_value(100 * z_now()).move_to([-0.3, -0.1, 0]))
    percent.update()
    scene.play(FadeOut(same), FadeIn(readout_row), FadeIn(percent), *[real.stage.fade(g_, 1.0) for g_ in ghost], run_time=0.9)
    scene.play(real.height_to(0.8 * H_IDEAL, run_time=2.6, rate_func=smooth), set_attr(real.stage, links, "alpha", 1.0, run_time=2.6),
               run_time=2.6)
    at_word(scene, t, 7, "Attraction", lead=0.2)
    tight = txt("pulled tighter", cfg.FONT["section"], cfg.ATTRACT).move_to([-0.3, -1.05, 0])
    scene.play(*[real.stage.fade(v, 1.0) for v in pulls], FadeIn(tight, shift=DOWN * 0.15), run_time=1.0)
    at_word(scene, t, 7, "If", nth=2, lead=0.2)
    apart = txt("pushed apart", cfg.FONT["section"], cfg.SIZE).move_to([-0.3, -1.05, 0])
    scene.play(*[real.stage.fade(v, 0.0) for v in pulls], set_attr(real.stage, links, "alpha", 0.0), FadeOut(tight), run_time=0.7)
    scene.play(real.height_to(1.2 * H_IDEAL, run_time=2.8, rate_func=smooth), real.cloud.tween("radius", 0.12, run_time=2.8),
               run_time=2.8)
    at_word(scene, t, 7, "size", lead=0.2)
    scene.play(*[real.stage.fade(v, 1.0) for v in pushes], FadeIn(apart, shift=UP * 0.15), run_time=1.0)
    finish(scene, t, real.stage, fill=lambda s: ideal.stage.turn(yaw=-0.2, rate_func=smooth))
