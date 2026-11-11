"""Scene 15 — Boyle's law, from the inside. Boyle's 1662 J-tube: pouring
mercury into the open arm raises the pressure on the trapped air, and with an
extra 760 mm of mercury (one more atmosphere) the air column halves. Then a
3D piston compresses a fixed amount of gas slowly at constant temperature:
the thermometer and the molecules' speed stay put, but the measured hits on
the piston per second double, and so does the model's pressure. A live dot
traces P against V (4 L at 1 bar), a hyperbola; three PV rectangles under it
have the same area.
"""

from manim_scenes.common import *

B = pm.BOYLE
V_REF = B.V1                        # the box starts at 4 L, 1 bar (the same sample as scene 16)


class Scene15Boyle(Scene):
    def construct(self) -> None:
        play_scene(self)


class JTube(VGroup):
    """Boyle's J-tube: trapped air in the sealed short arm, mercury below and in the open arm.

    ``extra`` (0..1) is the added head of mercury as a fraction of one atmosphere
    (760 mm). The air column obeys P V = constant: length = a0 / (1 + extra)."""

    def __init__(self, at=ORIGIN, atm: float = 3.0, air0: float = 2.8) -> None:
        super().__init__()
        self.at, self.atm, self.air0 = np.asarray(at, dtype=float), atm, air0
        self.extra = Knob(0.0)
        self.short_x, self.long_x, self.w = -1.3, 1.3, 0.62
        self.bottom, self.top_short, self.top_long = -3.2, 1.0, 3.75
        glass = VGroup(
            Line([self.short_x - self.w / 2, self.top_short, 0], [self.short_x - self.w / 2, self.bottom, 0]),
            Line([self.short_x + self.w / 2, self.top_short, 0], [self.short_x + self.w / 2, self.bottom + 0.5, 0]),
            Line([self.short_x - self.w / 2, self.top_short, 0], [self.short_x + self.w / 2, self.top_short, 0]),
            Line([self.long_x - self.w / 2, self.top_long, 0], [self.long_x - self.w / 2, self.bottom + 0.5, 0]),
            Line([self.long_x + self.w / 2, self.top_long, 0], [self.long_x + self.w / 2, self.bottom, 0]),
            Line([self.short_x - self.w / 2, self.bottom, 0], [self.long_x + self.w / 2, self.bottom, 0]),
            Line([self.short_x + self.w / 2, self.bottom + 0.5, 0], [self.long_x - self.w / 2, self.bottom + 0.5, 0]),
        ).set_stroke(cfg.GLASS, 4, 0.85)
        self.mercury = VGroup(*[Rectangle(stroke_width=0, fill_color="#C9D2DA", fill_opacity=0.95) for _ in range(3)])
        self.air = Rectangle(stroke_width=0, fill_color=cfg.MOLECULE, fill_opacity=0.35)
        self.dots = VGroup(*[Dot(radius=0.055, color=cfg.MOLECULE) for _ in range(18)])
        self.rng = np.random.default_rng(cfg.SEED)
        self.spots = self.rng.uniform(0, 1, size=(18, 2))
        self.add(self.air, self.dots, self.mercury, glass)
        self.shift(self.at)
        self.add_updater(lambda m: m.refresh())
        self.refresh()

    def air_length(self) -> float:
        return self.air0 / (1 + self.extra.value)

    def refresh(self) -> "JTube":
        o = self.at
        level_short = self.top_short - self.air_length()
        level_long = level_short + self.extra.value * self.atm
        w = self.w - 0.08
        segs = [((self.short_x, (self.bottom + level_short) / 2), w, level_short - self.bottom),
                (((self.short_x + self.long_x) / 2, self.bottom + 0.25), self.long_x - self.short_x + w, 0.42),
                ((self.long_x, (self.bottom + level_long) / 2), w, level_long - self.bottom)]
        for rect, ((x, y), width, height) in zip(self.mercury, segs):
            rect.stretch_to_fit_width(width).stretch_to_fit_height(max(height, 0.02)).move_to(o + np.array([x, y, 0]))
        self.air.stretch_to_fit_width(w).stretch_to_fit_height(self.air_length()).move_to(
            o + np.array([self.short_x, self.top_short - self.air_length() / 2, 0]))
        for dot, (fx_, fy_) in zip(self.dots, self.spots):
            dot.move_to(o + np.array([self.short_x - w / 2 + 0.06 + fx_ * (w - 0.12),
                                      self.top_short - 0.06 - fy_ * (self.air_length() - 0.12), 0]))
        return self


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "15", "Squeeze the gas")
    question = txt("what happens when you squeeze a gas?", cfg.FONT["label"], cfg.WHITE).move_to([0, -2.9, 0])
    scene.play(FadeIn(question, shift=UP * 0.1), run_time=1.0)

    # --- 2. Boyle, 1662: the J-tube -----------------------------------------------------------------------------------------
    beat(scene, t, 1)
    tube = JTube([-3.4, -0.25, 0])
    year = txt(f"Robert Boyle, {gd.YEAR_BOYLE}", cfg.FONT["label"], cfg.GOLD).move_to([3.0, 2.9, 0])
    air = txt("trapped air", cfg.FONT["small"], cfg.MOLECULE).move_to([-6.3, -0.4, 0])
    mercury = txt("mercury", cfg.FONT["small"], "#C9D2DA").move_to([-0.8, -3.0, 0])
    scene.play(FadeOut(question), FadeIn(tube), FadeIn(year), run_time=1.2)
    scene.play(FadeIn(air), FadeIn(mercury), run_time=0.8)
    vol = readout("V", lambda: tube.air_length() / tube.air0, 2, "× V₀", cfg.VOLUME, size=44).move_to([3.0, 1.2, 0])
    prs = readout("P", lambda: 1 + tube.extra.value, 2, "atm", cfg.PRESSURE, size=44).move_to([3.0, 0.1, 0])
    scene.play(FadeIn(vol), FadeIn(prs), run_time=0.8)
    scene.play(tube.extra.to(tube, 0.5, run_time=4.5), run_time=4.5)
    scene.play(tube.extra.to(tube, 1.0, run_time=4.5), run_time=4.5)
    halves = result_label("twice the pressure, half the volume", cfg.GOLD, cfg.FONT["body"]).move_to([3.0, -1.4, 0])
    fit_width(halves, 7.4)
    scene.play(FadeIn(halves, scale=0.95), run_time=1.0)

    # --- 3. Inside: a fixed amount under a piston, constant T; 1 bar --------------------------------------------------------------
    beat(scene, t, 2)
    box = GasBox((-4.4, -0.75, 0), count=120, half_x=1.35, half_z=1.05, height=2.9, floor=-1.45, lid="piston", zoom=1.0,
                 yaw=-0.5, pitch=0.3, speed=1.6, p_ref=B.P1, spark_axes=(1,), spark_sides=(1,))
    gauge = Gauge(box.pressure, [-0.9, 1.75, 0], top=3.0, radius=0.95)
    therm = Thermo(box.kelvin, [-0.9, -1.85, 0], height=1.7)
    volume = readout("V", lambda: V_REF * box.chamber.volume_ratio(), 2, "L", cfg.VOLUME, size=40).move_to([-4.4, 3.3, 0])
    scene.play(FadeOut(VGroup(tube, year, air, mercury, vol, prs, halves)), run_time=0.9)
    tube.clear_updaters()
    show(scene, box.stage, 1.0, FadeIn(gauge), FadeIn(therm), FadeIn(volume))
    fixed = VGroup(txt("fixed amount", cfg.FONT["small"], cfg.AMOUNT), txt("constant T", cfg.FONT["small"], cfg.TEMPERATURE))
    fixed.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.6, 2.6, 0])
    scene.play(FadeIn(fixed, shift=LEFT * 0.2), run_time=0.9)

    # --- 4. Push slowly; heat escapes; T stays ---------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(box.volume_to(0.5, run_time=6.0, rate_func=smooth), run_time=6.0)

    # --- 5. The molecules move as fast as before ------------------------------------------------------------------------------------
    beat(scene, t, 4)
    speed = readout(r"v_{\text{rms}}", lambda: box.cloud.heat * 1.0, 2, "× before", cfg.VELOCITY, size=38).move_to([3.6, 1.0, 0])
    scene.play(FadeIn(speed, shift=LEFT * 0.2), Indicate(therm.readout, color=cfg.TEMPERATURE), run_time=1.4)
    scene.wait(1.5)

    # --- 6. Less room: back to the walls more often ----------------------------------------------------------------------------------
    beat(scene, t, 5)
    hits_label = txt("sampled piston hits / s", cfg.FONT["small"], cfg.IMPULSE).move_to([3.6, -0.5, 0])
    rate = Knob(box.cloud.hit_rate(2.0, 1, 1))
    rate_bar = Rectangle(width=0.1, height=0.42, stroke_width=0, fill_color=cfg.IMPULSE, fill_opacity=0.9)
    rail = Rectangle(width=5.0, height=0.42, stroke_color=cfg.MUTED, stroke_width=2, fill_opacity=0).move_to([3.6, -1.2, 0])

    # Leave room for the expected doubled rate instead of saturating both bars.
    reference_rate = np.sum(np.abs(box.cloud.gas.u[:box.cloud.active_count(), 1])) * box.cloud.speed / (2 * box.chamber.height)

    def fit_bar(m, dt):
        rate.value += (box.cloud.hit_rate(2.0, 1, 1) - rate.value) * (1 - np.exp(-dt / 0.5))
        m.stretch_to_fit_width(max(0.02, min(5.0, 4.8 * rate.value / (2.2 * reference_rate)))).move_to(rail.get_left() + RIGHT * m.width / 2)

    rate_bar.add_updater(fit_bar)
    # Integer changes its digit count as the rate moves: add it with its updater only
    # after the fade (a fading copy with a changing digit count crashes Manim).
    count = Integer(int(round(rate.value)), font_size=48, color=cfg.IMPULSE).next_to(rail, RIGHT, buff=0.25)
    scene.play(FadeIn(hits_label), FadeIn(rail), FadeIn(rate_bar), run_time=1.0)
    count.add_updater(lambda m: m.set_value(int(round(rate.value))).next_to(rail, RIGHT, buff=0.25))
    scene.add(count)
    scene.play(box.volume_to(1.0, run_time=4.0), run_time=4.0)
    scene.wait(2.0)

    # --- 7. Halve the volume: twice the hits, twice the pressure ----------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(box.volume_to(0.5, run_time=4.0), box.cloud.tween("spark", 1.5, run_time=4.0), run_time=4.0)
    scene.wait(3.0)
    double = txt("mean hits × 2 → P × 2", cfg.FONT["label"], cfg.GOLD).move_to([3.6, -2.35, 0])
    scene.play(FadeIn(double, shift=UP * 0.1), Indicate(gauge.readout, color=cfg.PRESSURE), run_time=1.4)

    # --- 8. Pressure rose; no molecule got faster ---------------------------------------------------------------------------------------
    beat(scene, t, 7)
    none = result_label("no molecule got faster", cfg.GOLD, cfg.FONT["body"]).move_to([3.6, 2.6, 0])
    scene.play(fade_through(fixed, none), Indicate(speed, color=cfg.VELOCITY), run_time=1.2)

    # --- 9. P against V: a hyperbola ---------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    rate_bar.clear_updaters(), count.clear_updaters()
    axes = plot_axes((0, 7.0), (0, 3.2), x_length=5.6, y_length=4.4, at=[3.8, -0.3, 0], x_label="V", y_label="P",
                     x_color=cfg.VOLUME, y_color=cfg.PRESSURE, x_ticks=(2, 4, 6), y_ticks=(1, 2, 3))
    k = B.P1 * B.V1
    hyper = curve_on(axes, lambda v: k / v, k / 3.1, 7.0, cfg.PRESSURE)
    dot = glow_dot(axes.c2p(V_REF * box.chamber.volume_ratio(), box.pressure()), cfg.GOLD, 0.1)
    dot.add_updater(lambda m: m.move_to(axes.c2p(V_REF * box.chamber.volume_ratio(), box.pressure())))
    scene.play(FadeOut(VGroup(none, speed, hits_label, rail, rate_bar, count, double)), run_time=0.8)
    scene.play(Create(axes), FadeIn(dot), run_time=1.0)
    scene.play(box.volume_to(1.5, run_time=3.0), Create(hyper), run_time=3.0)
    law = eq(r"P \propto \frac{1}{V}", cfg.FONT["body"], cfg.PRESSURE).move_to([4.6, 2.6, 0])
    scene.play(box.volume_to(0.62, run_time=3.0), FadeIn(law), run_time=3.0)

    # --- 10. Equal rectangles: PV is constant ---------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    colors = (cfg.VOLUME, cfg.GOLD, cfg.ATTRACT)
    rects = VGroup(*[Polygon(axes.c2p(0, 0), axes.c2p(v, 0), axes.c2p(v, k / v), axes.c2p(0, k / v), stroke_color=c,
                             stroke_width=3, fill_color=c, fill_opacity=0.18) for v, c in zip((1.6, 4.0, 6.4), colors)])
    pv = eq(r"PV = \text{constant}", cfg.FONT["body"], cfg.WHITE).move_to([4.6, 2.6, 0])
    for rect in rects:
        scene.play(DrawBorderThenFill(rect), run_time=1.2)
    scene.play(fade_through(law, pv), run_time=1.0)
    scene.play(box.volume_to(1.0, run_time=3.0), run_time=3.0)

    # --- 11. P1 V1 = P2 V2 ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    final = boxed(paint(eq([r"P_1V_1", "=", r"P_2V_2"], cfg.FONT["section"]), {0: cfg.PRESSURE, 2: cfg.PRESSURE}), cfg.GOLD)
    final.move_to([4.6, 2.6, 0])
    scene.play(fade_through(pv, final), run_time=1.2)
    finish(scene, t, box.stage, fill=lambda s: [box.volume_to(0.7, rate_func=there_and_back)])
