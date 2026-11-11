"""Scene 18 — Charles' law. A free piston loaded with a weight holds the
pressure; a hot plate heats the gas. The molecules warm and speed up; the
piston lags the heating a little, so the gauge first rises above 1 bar
(the push beats the weight), then falls back as the volume grows and the
hits thin out. V follows absolute temperature: 2 L at 300 K, 3 L at 450 K,
4 L at 600 K, all on a line through the origin. A hot-air balloon closes it:
heated air expands, spills out, and the lighter air inside floats.
"""

from manim_scenes.common import *
from manim_scenes.hot_air_balloon import HotAirBalloon

C = pm.CHARLES


class Scene18Charles(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "18", "Heat it, let it grow")
    box = GasBox((-4.3, -1.15, 0), count=110, seed=cfg.SEED + 18, half_x=1.3, half_z=1.0, height=1.9, floor=-0.95,
                 lid="weight", heater=True, zoom=1.0, yaw=-0.5, pitch=0.3, speed=1.5, spark_axes=(1,), spark_sides=(1,))
    gauge = Gauge(box.pressure, [-0.8, 2.0, 0], top=2.0, radius=0.9, step=0.25)
    therm = Thermo(box.kelvin, [-0.8, -1.85, 0], height=1.7, low=250, high=650)
    volume = readout("V", lambda: C.V1 * box.chamber.volume_ratio(), 2, "L", cfg.VOLUME, size=40).move_to([-4.3, 3.4, 0])
    show(scene, box.stage, 1.0, FadeIn(gauge), FadeIn(therm), FadeIn(volume))
    question = txt("heat it at constant pressure?", cfg.FONT["label"], cfg.WHITE).move_to([3.6, 2.6, 0])
    scene.play(FadeIn(question), run_time=0.8)

    # --- 2. A free piston with a weight: the gas must push with the same pressure ----------------------------------------------
    beat(scene, t, 1)
    weight = Tag(txt("weight", cfg.FONT["small"], cfg.GOLD), lambda: box.lid_point(0.75), UP * 0.25)
    free_text = txt("free\npiston", cfg.FONT["small"], cfg.WHITE)
    free_text.add_background_rectangle(color=cfg.BG, opacity=0.92, buff=0.08)
    free = Tag(free_text, lambda: box.lid_point(0.0) + np.array([-1.3, 0, 1.0]), LEFT * 1.05 + UP * 0.15)
    for tag in (weight, free):
        tag.presence = 0.0
    box.stage.add_overlay(weight, free)
    scene.play(box.stage.fade(weight, 1.0), run_time=0.8)
    scene.play(box.stage.fade(free, 1.0), run_time=0.8)
    same = txt("fixed external pressure", cfg.FONT["label"], cfg.PRESSURE).move_to([3.6, 1.6, 0])
    scene.play(FadeIn(same), Indicate(gauge.readout, color=cfg.PRESSURE), run_time=1.4)

    # --- 3. Heat --------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(*box.heater_on(1.0), box.stage.fade(weight, 0.0), box.stage.fade(free, 0.0), FadeOut(question), run_time=1.0)

    # --- 4. Faster, harder hits: the push beats the weight, the piston rises -------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(box.heat_to(450, run_time=3.0), box.cloud.tween("warmth", 0.35, run_time=3.0),
               box.volume_to(1.2, run_time=3.0, rate_func=rate_functions.ease_in_quad), run_time=3.0)
    beats_weight = txt("heating → expansion", cfg.FONT["label"], cfg.IMPULSE).move_to([3.6, 0.6, 0])
    scene.play(FadeIn(beats_weight), run_time=0.7)
    scene.play(box.volume_to(1.5, run_time=3.5), run_time=3.5)

    # --- 5. Farther to travel: hits thin out until balanced --------------------------------------------------------------------------------
    beat(scene, t, 4)
    balanced = txt("expansion restores balance", cfg.FONT["label"], cfg.PRESSURE).move_to([3.6, 0.6, 0])
    scene.play(fade_through(beats_weight, balanced), box.heat_to(600, run_time=3.0), box.cloud.tween("warmth", 0.6, run_time=3.0),
               box.volume_to(1.6, run_time=3.0, rate_func=rate_functions.ease_in_quad), run_time=3.0)
    scene.play(box.volume_to(2.0, run_time=4.0), run_time=4.0)

    # --- 6. Higher T, same P, larger V ----------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    summary = result_label("hotter · same P · bigger V", cfg.GOLD, cfg.FONT["body"]).move_to([3.6, 2.6, 0])
    scene.play(FadeOut(VGroup(same, balanced)), FadeIn(summary, scale=0.95), run_time=1.0)

    # --- 7. V in step with absolute temperature: a line through the origin ------------------------------------------------------------------
    beat(scene, t, 6)
    axes = plot_axes((0, 700), (0, 5.0), x_length=5.6, y_length=3.8, at=[3.7, -0.7, 0], x_label="T", y_label="V",
                     x_color=cfg.TEMPERATURE, y_color=cfg.VOLUME, x_ticks=(300, 600), y_ticks=(2, 4))
    k = C.V1 / C.T1
    line = DashedLine(axes.c2p(0, 0), axes.c2p(680, k * 680), stroke_color=cfg.VOLUME, stroke_width=4, dash_length=0.14)
    points = VGroup(*[glow_dot(axes.c2p(T, k * T), cfg.GOLD, 0.1) for T in (C.T1, C.T2, 2 * C.T1)])
    scene.play(Create(axes), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in points], lag_ratio=0.4), run_time=1.6)
    scene.play(Create(line), run_time=1.4)
    double = txt("2 × T  →  2 × V", cfg.FONT["small"], cfg.GOLD).next_to(axes.c2p(150, 4.5), RIGHT, buff=0)
    scene.play(FadeIn(double), run_time=0.8)

    # --- 8. V proportional to T: V1/T1 = V2/T2 --------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    law = boxed(paint(eq([r"\frac{V_1}{T_1}", "=", r"\frac{V_2}{T_2}"], cfg.FONT["section"]), {0: cfg.VOLUME, 2: cfg.VOLUME}), cfg.GOLD)
    law.move_to([3.6, 2.5, 0])
    scene.play(fade_through(summary, law), run_time=1.2)

    # --- 9. A hot-air balloon: Charles' law you can ride --------------------------------------------------------------------------------------
    beat(scene, t, 8)
    hide(scene, box.stage, 0.9, FadeOut(VGroup(gauge, therm, volume, axes, line, points, double)), FadeOut(law))
    balloon = HotAirBalloon([-2.6, 0.1, 0], 1.25)
    rng = np.random.default_rng(cfg.SEED + 181)
    outside = VGroup(*[Dot([x, y, 0], radius=0.05, color=cfg.MOLECULE) for x, y in
                       zip(rng.uniform(-7.4, 0.5, 90), rng.uniform(-3.8, 3.4, 90))
                       if abs(x + 2.6) > 2.3 or abs(y - 0.3) > 2.9])
    show(scene, balloon, 1.4, FadeIn(outside))
    scene.play(balloon.fade(balloon.air, 1.0), run_time=0.8)
    scene.play(balloon.release_air(), run_time=1.6)
    lighter = VGroup(txt("hot air inside: less dense", cfg.FONT["label"], cfg.HOT_COLOR),
                     txt("so the balloon floats", cfg.FONT["label"], cfg.GOLD)).arrange(DOWN, buff=0.25).move_to([3.6, -0.8, 0])
    scene.play(FadeIn(lighter, shift=UP * 0.1), run_time=1.0)
    finish(scene, t, fill=lambda s: [balloon.glide(balloon.center_point() + UP * 0.55)])
