"""Scene 21 — Gay-Lussac's law. A rigid, bolted box on a hot plate: the
volume and amount cannot change. Heating speeds the molecules: the gold
molecule's velocity arrow lengthens (more momentum per hit) and the measured
hits on the lid per second climb (more hits). The gauge, reading the model,
goes from 1.00 bar at 300 K to 1.20 bar at 360 K, on a P-T line through the
origin. Both effects scale with speed, so P scales with v^2, i.e. with T.
A sealed gas cylinder closes the scene.
"""

from manim_scenes.common import *

G = pm.GAY_LUSSAC


class Scene21GayLussac(Scene):
    def construct(self) -> None:
        play_scene(self)


def gas_cylinder(at) -> VGroup:
    """A spray can with a red 'do not heat' band, over a flame (2D)."""
    at = np.asarray(at, dtype=float)
    body = RoundedRectangle(width=1.3, height=2.6, corner_radius=0.25, stroke_color=cfg.STEEL, stroke_width=3,
                            fill_color="#5A6C7A", fill_opacity=1).move_to(at)
    shoulder = Ellipse(width=1.3, height=0.5, stroke_color=cfg.STEEL, stroke_width=3, fill_color="#6E8291",
                       fill_opacity=1).move_to(at + UP * 1.3)
    cap = RoundedRectangle(width=0.5, height=0.35, corner_radius=0.08, stroke_width=0, fill_color=cfg.STEEL,
                           fill_opacity=1).move_to(at + UP * 1.62)
    band = Rectangle(width=1.3, height=0.55, stroke_width=0, fill_color=cfg.RED, fill_opacity=0.9).move_to(at)
    warning = txt("SEALED GAS", 22, cfg.WHITE).move_to(band)
    decorative(warning)
    flames = VGroup(*[VGroup(Ellipse(width=0.35, height=0.8, stroke_width=0, fill_color=cfg.HOT_COLOR, fill_opacity=0.85),
                             Ellipse(width=0.18, height=0.45, stroke_width=0, fill_color=cfg.GOLD, fill_opacity=0.9).shift(DOWN * 0.12))
                      .move_to(at + np.array([dx, -1.75, 0])) for dx in (-0.4, 0.0, 0.4)])
    return VGroup(flames, body, shoulder, cap, band, warning)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "21", "Heat it, hold it")
    box = GasBox((-4.2, -0.85, 0), count=110, seed=cfg.SEED + 21, half_x=1.35, half_z=1.05, height=2.5, floor=-1.25,
                 lid="rigid", heater=True, follow=5, trail=1.5, zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.5, p_ref=G.P1,
                 spark_axes=(1,), spark_sides=(1,))
    gauge = Gauge(box.pressure, [-0.7, 1.9, 0], top=2.0, radius=0.9, step=0.25)
    therm = Thermo(box.kelvin, [-0.7, -1.6, 0], height=1.8, low=250, high=450)
    show(scene, box.stage, 1.0, FadeIn(gauge), FadeIn(therm))
    stop = txt("what if it cannot expand?", cfg.FONT["label"], cfg.WHITE).move_to([3.6, 2.6, 0])
    scene.play(FadeIn(stop), run_time=0.8)

    # --- 2. Rigid: V fixed, n fixed -----------------------------------------------------------------------------------------
    beat(scene, t, 1)
    fixed = VGroup(txt("V fixed", cfg.FONT["label"], cfg.VOLUME), txt("n fixed", cfg.FONT["label"], cfg.AMOUNT))
    fixed.arrange(RIGHT, buff=0.6).move_to([3.6, 1.6, 0])
    bolts = Tag(txt("rigid, bolted lid", cfg.FONT["small"], cfg.STEEL), lambda: box.lid_point(0.25), UP * 0.35)
    bolts.presence = 0.0
    box.stage.add_overlay(bolts)
    scene.play(FadeIn(fixed), box.stage.fade(bolts, 1.0), run_time=1.2)
    scene.wait(2.5)

    # --- 3. Heat ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(*box.heater_on(1.0), box.stage.fade(bolts, 0.0), FadeOut(stop), run_time=1.0)

    # --- 4. Faster: each hit delivers more momentum --------------------------------------------------------------------------------
    beat(scene, t, 3)
    arrow = Vector(lambda: box.cloud.position(5), lambda: box.cloud.position(5) + box.cloud.velocity(5) * 0.7, cfg.VELOCITY,
                   width=0.06, tip=0.2)
    arrow.presence = 0.0
    box.stage.add_overlay(arrow)
    harder = txt("harder hits", cfg.FONT["label"], cfg.IMPULSE).move_to([3.6, 0.5, 0])
    scene.play(box.stage.fade(arrow, 1.0), run_time=0.6)
    scene.play(box.heat_to(330, run_time=3.0), box.cloud.tween("warmth", 0.25, run_time=3.0), FadeIn(harder), run_time=3.0)

    # --- 5. ... and more often --------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    rate = Knob(box.cloud.hit_rate(2.0, 1, 1))
    count = Integer(int(round(rate.value)), font_size=46, color=cfg.IMPULSE)
    often = VGroup(txt("more often:", cfg.FONT["label"], cfg.VELOCITY), count).arrange(RIGHT, buff=0.3).move_to([3.4, -0.4, 0])
    per = txt("hits on the lid per second", cfg.FONT["tiny"], cfg.MUTED).next_to(often, DOWN, buff=0.28)

    def follow(m, dt):
        rate.value += (box.cloud.hit_rate(2.0, 1, 1) - rate.value) * (1 - np.exp(-dt / 0.5))
        m.set_value(int(round(rate.value)))

    scene.play(FadeIn(often[0]), FadeIn(per), run_time=0.8)
    count.add_updater(follow)
    scene.add(count)
    scene.play(box.heat_to(G.T2, run_time=4.0), box.cloud.tween("warmth", 0.45, run_time=4.0), run_time=4.0)

    # --- 6. More momentum per hit, more hits: the pressure climbs ----------------------------------------------------------------------
    beat(scene, t, 5)
    climbs = result_label("the pressure climbs", cfg.PRESSURE, cfg.FONT["body"]).move_to([3.6, 2.6, 0])
    scene.play(FadeOut(fixed), FadeIn(climbs, scale=0.95), Indicate(gauge.readout, color=cfg.PRESSURE), run_time=1.4)
    scene.wait(2.5)

    # --- 7. P proportional to T: P1/T1 = P2/T2 --------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    count.clear_updaters()
    axes = plot_axes((0, 450), (0, 1.6), x_length=5.4, y_length=3.1, at=[3.7, -0.1, 0], x_label="T", y_label="P",
                     x_color=cfg.TEMPERATURE, y_color=cfg.PRESSURE, x_ticks=(150, 300), y_ticks=(0.5, 1.0, 1.5))
    k = G.P1 / G.T1
    line = DashedLine(axes.c2p(0, 0), axes.c2p(440, k * 440), stroke_color=cfg.PRESSURE, stroke_width=4, dash_length=0.14)
    marks = VGroup(*[glow_dot(axes.c2p(T, k * T), cfg.GOLD, 0.1) for T in (G.T1, G.T2)])
    law = boxed(paint(eq([r"\frac{P_1}{T_1}", "=", r"\frac{P_2}{T_2}"], cfg.FONT["body"]), {0: cfg.PRESSURE, 2: cfg.PRESSURE}), cfg.GOLD)
    law.move_to([3.6, 2.6, 0])
    scene.play(FadeOut(VGroup(harder, often, per)), fade_through(climbs, law), run_time=1.0)
    scene.play(Create(axes), Create(line), run_time=1.4)
    scene.play(FadeIn(marks), run_time=0.8)

    # --- 8. 300 K -> 360 K: 1 bar -> 1.2 bar ---------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    numbers = eq(rf"{fx(G.P1, 2)}\ \mathrm{{bar}} \times \frac{{{fx(G.T2, 0)}\ \mathrm{{K}}}}{{{fx(G.T1, 0)}\ \mathrm{{K}}}} = {fx(G.P2, 2)}\ \mathrm{{bar}}",
                 cfg.FONT["body"], cfg.WHITE)
    fit_width(numbers, 6.4)
    numbers.move_to([3.7, -2.85, 0])
    scene.play(Write(numbers), run_time=2.0)
    scene.play(Indicate(gauge.readout, color=cfg.GOLD), Indicate(marks[1], color=cfg.GOLD), run_time=1.4)

    # --- 9. Both effects scale with speed: P ~ v^2 ~ T ------------------------------------------------------------------------------------
    beat(scene, t, 8)
    chain = eq(r"P \propto \langle v_x^2\rangle \propto T", cfg.FONT["body"], cfg.WHITE)
    fit_width(chain, 6.4)
    chain.move_to([3.7, -2.85, 0])
    scene.play(fade_through(numbers, chain), run_time=1.2)

    # --- 10. Aerosol cans: do not heat --------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    can = gas_cylinder([-4.0, -0.1, 0])
    can_gauge_value = Knob(1.0)
    can_gauge = Gauge(lambda: can_gauge_value.value, [-1.2, 0.4, 0], top=3.0, radius=0.85)
    hide(scene, box.stage, 0.8, FadeOut(VGroup(gauge, therm, axes, line, marks, law, chain)))
    scene.play(FadeIn(can, shift=UP * 0.2), FadeIn(can_gauge), run_time=1.0)
    sealed = VGroup(txt("sealed, rigid:", cfg.FONT["label"], cfg.WHITE),
                    txt("pressure climbs with T", cfg.FONT["label"], cfg.WARNING)).arrange(DOWN, buff=0.25).move_to([3.6, 0.4, 0])
    scene.play(FadeIn(sealed), can_gauge_value.to(can_gauge, 2.6, run_time=4.0), run_time=4.0)
    finish(scene, t, fill=lambda s: [can_gauge_value.to(can_gauge, 2.9, rate_func=linear)])
