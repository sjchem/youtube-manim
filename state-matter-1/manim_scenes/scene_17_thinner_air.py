"""Scene 17 — thinner air. The same molecules squeezed into half the room
are packed twice as densely: at constant temperature, density is
proportional to pressure. A mountain's air column thins with height (a
schematic, density falling with altitude); on Everest's summit the pressure
is about a third of sea level, so each breath holds far fewer oxygen
molecules. Then the warning: fast compression in a bicycle pump warms the
gas. The 3D box is squeezed quickly to half volume (adiabatic: T rises by
2^0.4), and its P-V path climbs above the isotherm (P V^1.4 constant).
"""

from manim_scenes.common import *

M = pm.MOUNTAIN


class Scene17ThinnerAir(Scene):
    def construct(self) -> None:
        play_scene(self)


def mountain_air(at, width: float = 6.0, height: float = 5.2, seed: int = cfg.SEED) -> VGroup:
    """A mountain silhouette under an air column whose dots thin out with altitude
    (density falling off exponentially; scale height ~ the peak's height)."""
    rng = np.random.default_rng(seed)
    at = np.asarray(at, dtype=float)
    base_y = at[1] - height / 2
    peak = Polygon(at + np.array([-width / 2, -height / 2, 0]), at + np.array([-0.4, height * 0.18, 0]),
                   at + np.array([0.3, height * 0.05, 0]), at + np.array([1.0, height * 0.28, 0]),
                   at + np.array([width / 2, -height / 2, 0]), stroke_color="#7FA3B8", stroke_width=3,
                   fill_color="#2B4558", fill_opacity=1)
    snow = Polygon(at + np.array([0.62, height * 0.12, 0]), at + np.array([1.0, height * 0.28, 0]),
                   at + np.array([1.38, height * 0.12, 0]), stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.9)
    heights = rng.exponential(scale=height * 0.42, size=420)
    heights = heights[heights < height * 0.98][:260]
    xs = rng.uniform(-width / 2, width / 2, len(heights))
    dots = VGroup(*[Dot(at + np.array([x, -height / 2 + h, 0]), radius=0.035, color=cfg.MOLECULE, fill_opacity=0.85)
                    for x, h in zip(xs, heights)])
    group = VGroup(dots, peak, snow)
    group.peak_point = at + np.array([1.0, height * 0.28, 0])
    group.base_y = base_y
    return group


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "17", "Thinner air")
    loose = GasBox((-3.6, -0.8, 0), count=70, seed=cfg.SEED + 17, half_x=1.2, half_z=0.95, height=2.8, floor=-1.4,
                   zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.4)
    dense = GasBox((2.6, -0.8, 0), count=70, seed=cfg.SEED + 17, half_x=1.2, half_z=0.95, height=1.4, floor=-1.4,
                   zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.4)
    show(scene, loose.stage, 0.9)
    show(scene, dense.stage, 0.9)
    labels = VGroup(eq(r"\rho", cfg.FONT["section"], cfg.WHITE).move_to([-3.6, 2.4, 0]),
                    eq(r"2\rho", cfg.FONT["section"], cfg.GOLD).move_to([2.6, 2.4, 0]))
    same = txt("same molecules, half the space", cfg.FONT["label"], cfg.WHITE).move_to([0, -2.9, 0])
    scene.play(FadeIn(labels), FadeIn(same), run_time=1.2)
    scene.wait(3.5)

    # --- 2. Density proportional to pressure --------------------------------------------------------------------------------
    beat(scene, t, 1)
    law = eq(r"\rho \propto P \quad (\text{constant } T)", cfg.FONT["body"], cfg.PRESSURE).move_to([0, -2.9, 0])
    scene.play(fade_through(same, law), run_time=1.2)

    # --- 3. A mountain: air squeezed by the air above; thinner with height ---------------------------------------------------------
    beat(scene, t, 2)
    hide(scene, loose.stage, 0.6)
    hide(scene, dense.stage, 0.6, FadeOut(VGroup(labels, law)))
    hill = mountain_air([-2.6, -0.5, 0], width=7.2, height=6.0)
    scene.play(FadeIn(hill[1]), FadeIn(hill[2]), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(d) for d in hill[0]], lag_ratio=0.004), run_time=2.6)
    sea = txt(f"sea level ≈ {fx(pm.SEA_LEVEL_BAR, 2)} bar", cfg.FONT["small"], cfg.PRESSURE).move_to([3.9, -3.2, 0])
    weight = VGroup(*[VecArrow([x, 2.6, 0], [x, 1.6, 0], cfg.IMPULSE, width=0.06, tip_len=0.18, live=False)
                      for x in (-5.2, -3.8, -2.4, -1.0)])
    above = txt("the air above presses down", cfg.FONT["small"], cfg.IMPULSE).move_to([3.9, 2.4, 0])
    scene.play(FadeIn(weight, shift=DOWN * 0.2), FadeIn(above), run_time=1.2)
    scene.play(FadeIn(sea), run_time=0.8)
    thinner = txt("higher: less air above, thinner air", cfg.FONT["small"], cfg.WHITE).move_to([3.9, 1.6, 0])
    fit_width(thinner, 6.2)
    scene.play(FadeIn(thinner), run_time=0.9)

    # --- 4. Everest: about a third of the pressure; far fewer O2 per breath ---------------------------------------------------------------
    beat(scene, t, 3)
    flag = VGroup(Line(hill.peak_point, hill.peak_point + UP * 0.6, stroke_color=cfg.WHITE, stroke_width=3),
                  Polygon(hill.peak_point + UP * 0.6, hill.peak_point + UP * 0.42 + RIGHT * 0.32, hill.peak_point + UP * 0.24,
                          stroke_width=0, fill_color=cfg.RED, fill_opacity=1))
    summit = txt(f"Everest summit ≈ {fx(pm.EVEREST_BAR, 2)} bar", cfg.FONT["small"], cfg.PRESSURE).move_to([3.9, 1.4, 0])
    third = result_label("about a third", cfg.GOLD, cfg.FONT["body"]).move_to([3.9, 0.65, 0])
    scene.play(FadeOut(VGroup(weight, above, thinner)), FadeIn(flag), run_time=0.8)
    scene.play(FadeIn(summit), run_time=0.8)
    scene.play(FadeIn(third, scale=0.95), run_time=0.9)
    breaths = VGroup()
    for x, n, name in ((2.6, 21, "sea level"), (5.2, 7, "summit")):
        ring = Circle(radius=0.75, stroke_color=cfg.MUTED, stroke_width=3).move_to([x, -1.55, 0])
        rng = np.random.default_rng(int(x * 10))
        pts = [ring.get_center() + 0.55 * np.sqrt(rng.uniform()) * np.array([np.cos(a), np.sin(a), 0])
               for a in rng.uniform(0, TAU, n)]
        breaths.add(VGroup(ring, VGroup(*[Dot(p, radius=0.05, color=cfg.O2_COLOR) for p in pts]),
                           txt(name, cfg.FONT["tiny"], cfg.MUTED).next_to(ring, DOWN, buff=0.12)))
    o2 = txt("O₂ per breath", cfg.FONT["small"], cfg.O2_COLOR).next_to(breaths, UP, buff=0.2)
    scene.play(FadeOut(sea), run_time=0.5)
    scene.play(FadeIn(breaths), FadeIn(o2), run_time=1.0)
    scene.wait(5.0)

    # --- 5. A warning: pump quickly, and the pump gets warm --------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(FadeOut(VGroup(hill, flag, summit, third, breaths, o2)), run_time=0.8)
    box = GasBox((-4.4, -0.75, 0), count=110, seed=cfg.SEED + 18, half_x=1.35, half_z=1.05, height=2.9, floor=-1.45,
                 lid="piston", zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.6, spark_axes=(1,), spark_sides=(1,))
    therm = Thermo(box.kelvin, [-0.9, -1.8, 0], height=1.8, low=250, high=450)
    gauge = Gauge(box.pressure, [-0.9, 2.2, 0], top=3.0, radius=0.8)
    show(scene, box.stage, 0.9, FadeIn(therm), FadeIn(gauge))
    warm = txt("fast compression: the gas warms", cfg.FONT["label"], cfg.TEMPERATURE).move_to([3.4, 2.9, 0])
    fit_width(warm, 7.0)
    scene.play(FadeIn(warm), run_time=0.8)

    # --- 6. Work faster than heat escapes: hotter, higher pressure than Boyle ---------------------------------------------------------------
    beat(scene, t, 5)
    axes = plot_axes((0, 1.2), (0, 3.0), x_length=5.0, y_length=4.0, at=[3.6, -0.6, 0], x_label="V", y_label="P",
                     x_color=cfg.VOLUME, y_color=cfg.PRESSURE, y_ticks=(1, 2, 3))
    iso = curve_on(axes, lambda v: 1 / v, 0.4, 1.2, cfg.PRESSURE, width=5)
    adiabat = curve_on(axes, lambda v: pm.adiabatic_pressure(v), 0.5, 1.2, cfg.TEMPERATURE, width=5)
    names = VGroup(txt("slow (Boyle)", cfg.FONT["tiny"], cfg.PRESSURE).next_to(axes.c2p(0.75, 1 / 0.75), LEFT, buff=0.25).shift(DOWN * 0.2),
                   txt("fast", cfg.FONT["tiny"], cfg.TEMPERATURE).next_to(axes.c2p(0.55, pm.adiabatic_pressure(0.55)), RIGHT, buff=0.28).shift(UP * 0.1))
    dot = glow_dot(axes.c2p(1, 1), cfg.GOLD, 0.1)
    dot.add_updater(lambda m: m.move_to(axes.c2p(box.chamber.volume_ratio(), box.pressure())))
    scene.play(Create(axes), Create(iso), FadeIn(names[0]), FadeIn(dot), run_time=1.4)
    # Adiabatic: temperature is driven by the volume, T = T0 V^(1 - gamma), so every frame sits on P V^1.4 = constant.
    base_height = box.chamber.height

    def squeeze(e: float) -> None:
        v = 1.0 - 0.5 * e
        box.chamber.height = base_height * v
        box.cloud.heat = float(np.sqrt(v ** (1 - pm.GAMMA_AIR)))

    scene.play(Param(box.stage, lambda: 0.0, squeeze, 1.0, rate_func=rate_functions.ease_in_quad),
               box.cloud.tween("warmth", 0.45, run_time=1.6), Create(adiabat), run_time=1.6)
    scene.play(FadeIn(names[1]), Indicate(gauge.readout, color=cfg.TEMPERATURE), run_time=1.2)
    above = txt("above Boyle's curve", cfg.FONT["small"], cfg.TEMPERATURE).move_to([4.6, 1.8, 0])
    scene.play(FadeIn(above), run_time=0.8)

    # --- 7. Ask first: what is held constant? -----------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    ask = chip("what stays fixed?", cfg.GOLD, cfg.FONT["label"]).move_to([3.6, 2.9, 0])
    scene.play(fade_through(warm, ask), run_time=1.0)
    finish(scene, t, box.stage)
