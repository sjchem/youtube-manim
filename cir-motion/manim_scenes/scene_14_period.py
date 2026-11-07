"""Scene 14 — period and frequency. The reference particle laps its circle in
real time while a lap timer resets every revolution and a lap counter
climbs. T (seconds per lap) and f (laps per second, hertz) are reciprocals;
one lap sweeps 2 pi rad and covers 2 pi r, so omega = 2 pi / T = 2 pi f and
v = 2 pi r / T. For the particle: T = 2 pi (2) / 4 = pi s ~ 3.14 s (the
timer stops on it), f = 1 / pi ~ 0.318 Hz, and 2 pi f = 2 rad/s. Four tiles
close the scene: four descriptions of one motion.
"""

from manim_scenes.common import *

C = np.array([-3.7, -0.7, 0])
R = 2.2
COL = 3.4


class Scene14Period(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "14", "Period and frequency")
    view = CircleView(C, R, P, phase=PI / 2, kv=1.0 / P.v)
    v_arrow = view.arrow("v", width=0.08)
    timer = number_line(lambda: view.clock.value % P.period, 2, "s", cfg.WHITE, 54, "lap time")
    laps = number_line(lambda: np.floor(view.clock.value / P.period + 1e-9), 0, "laps", cfg.ANGLE, 54)
    clocks = VGroup(timer, laps).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.7, 2.45, 0])
    scene.play(FadeIn(view.ring), FadeIn(view.hub), FadeIn(view.ball), FadeIn(clocks), run_time=0.7)
    scene.add(v_arrow)
    scene.play(v_arrow.grow_in(run_time=0.5), run_time=0.5)
    scene.play(view.run(1.4), run_time=1.4)

    # --- 2. The period T ---------------------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    period = VGroup(eq("T", cfg.FONT["title"], cfg.WHITE), txt("seconds per lap", cfg.FONT["small"], cfg.MUTED))
    period.arrange(RIGHT, buff=0.4).move_to([COL, 3.2, 0])
    scene.play(FadeOut(head), FadeIn(period, shift=DOWN * 0.1), view.run(view.clock.value + 0.8), run_time=0.8)
    scene.play(view.run(view.clock.value + 4.0), run_time=4.0)

    # --- 3. The frequency f, in hertz ----------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    frequency = VGroup(eq("f", cfg.FONT["title"], cfg.ANGLE), txt("laps per second", cfg.FONT["small"], cfg.MUTED))
    frequency.arrange(RIGHT, buff=0.4).next_to(period, DOWN, buff=0.3).align_to(period, LEFT)
    hertz = txt("Hz = cycles/s", cfg.FONT["tiny"], cfg.ANGLE).next_to(frequency, DOWN, buff=0.22).align_to(period, LEFT)
    scene.play(FadeIn(frequency, shift=DOWN * 0.1), view.run(view.clock.value + 0.8), run_time=0.8)
    scene.play(FadeIn(hertz), view.run(view.clock.value + 0.7), run_time=0.7)
    scene.play(view.run(view.clock.value + 6.5), run_time=6.5)

    # --- 4. Reciprocals ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    recip = VGroup(eq(r"f = \frac{1}{T}", cfg.FONT["section"], cfg.ANGLE), eq(r"T = \frac{1}{f}", cfg.FONT["section"], cfg.WHITE))
    recip.arrange(RIGHT, buff=1.0).move_to([COL, 2.6, 0])
    recip.set_x(COL)
    scene.play(FadeOut(VGroup(period, frequency, hertz)), view.run(view.clock.value + 0.4), run_time=0.4)
    scene.play(Write(recip[0]), view.run(view.clock.value + 0.8), run_time=0.8)
    scene.play(Write(recip[1]), view.run(view.clock.value + 1.2), run_time=1.2)
    scene.play(view.run(view.clock.value + 6.0), run_time=6.0)

    # --- 5. omega = 2 pi / T = 2 pi f -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    omega = paint(eq([r"|\omega|", "=", r"\frac{2\pi}{T}", "=", r"2\pi f"], cfg.FONT["section"]), {0: cfg.ANGLE, 4: cfg.ANGLE})
    omega.next_to(recip, DOWN, buff=0.4).set_x(COL)
    scene.play(Write(omega), view.run(view.clock.value + 1.6), run_time=1.6)
    scene.play(view.run(view.clock.value + 7.5), run_time=7.5)

    # --- 6. v = 2 pi r / T ----------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    speed = paint(eq([r"v", "=", r"\frac{2\pi r}{T}"], cfg.FONT["section"]), {0: cfg.VELOCITY}).next_to(omega, DOWN, buff=0.4).set_x(COL)
    scene.play(Write(speed), view.run(view.clock.value + 1.4), run_time=1.4)
    scene.play(view.run(view.clock.value + 6.5), run_time=6.5)

    # --- 7. Our particle: T = pi s ~ 3.14 s ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    general = VGroup(recip, omega, speed)
    scene.play(FadeOut(general), run_time=0.6)
    # Restart the lap so the timer stops exactly when one revolution ends.
    laps_done = np.ceil(view.clock.value / P.period)
    scene.play(view.run(laps_done * P.period), run_time=max(laps_done * P.period - view.clock.value, 0.1))
    timer.clear_updaters()
    lap_clock = Knob(0.0)
    timer.add_updater(lambda m: (m.number.set_value(lap_clock.value), m[-1].next_to(m.number, RIGHT, buff=0.18, aligned_edge=DOWN)))
    ours = eq([r"T", "=", r"\frac{2\pi r}{v}", "=", r"\pi\ \mathrm{s}", r"\approx",
               rf"{PERIOD}\ \mathrm{{s}}"], cfg.FONT["body"])
    fit_width(ours, 6.6)
    ours.move_to([COL, 2.6, 0])
    scene.play(Write(ours), run_time=1.8)
    scene.play(view.run(view.clock.value + P.period), lap_clock.to(view.ball, P.period, run_time=P.period, rate_func=linear),
               run_time=P.period)
    t_box = boxed(ours[6], cfg.RESULT, 0.12)[0]
    scene.play(Indicate(timer, color=cfg.GOLD, scale_factor=1.06), FadeIn(t_box), run_time=1.0)

    # --- 8. f = 1 / pi ~ 0.318 Hz --------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    ours_f = eq([r"f", "=", r"\frac{1}{\pi}", r"\approx", rf"{FREQ}\ \mathrm{{Hz}}"], cfg.FONT["body"])
    paint(ours_f, {0: cfg.ANGLE, 4: cfg.ANGLE}).next_to(ours, DOWN, buff=0.55).set_x(COL)
    scene.play(Write(ours_f), view.run(view.clock.value + 1.4), run_time=1.4)
    scene.play(view.run(view.clock.value + 3.0), run_time=3.0)

    # --- 9. 2 pi f = 2 rad/s ----------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    ours_w = eq([r"|\omega|", "=", r"2\pi f", "=", rf"{OMEGA}\ \mathrm{{rad/s}}"], cfg.FONT["body"])
    paint(ours_w, {0: cfg.ANGLE, 4: cfg.ANGLE}).next_to(ours_f, DOWN, buff=0.5).set_x(COL)
    scene.play(Write(ours_w), view.run(view.clock.value + 1.4), run_time=1.4)
    scene.play(view.run(view.clock.value + 4.0), run_time=4.0)

    # --- 10. Four descriptions of one motion --------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    timer.clear_updaters()
    laps.clear_updaters()
    tiles = VGroup(scalar_tile("speed", rf"{V}\ \mathrm{{m/s}}", cfg.VELOCITY), scalar_tile("angular speed", rf"{OMEGA}\ \mathrm{{rad/s}}", cfg.ANGLE),
                   scalar_tile("period", rf"{PERIOD}\ \mathrm{{s}}", cfg.WHITE), scalar_tile("frequency", rf"{FREQ}\ \mathrm{{Hz}}", cfg.ANGLE))
    tiles.arrange_in_grid(2, 2, buff=0.35).move_to([COL, 0.0, 0])
    scene.play(FadeOut(VGroup(ours, t_box, ours_f, ours_w, clocks)), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(tile, shift=UP * 0.1) for tile in tiles], lag_ratio=0.3), view.run(view.clock.value + 2.0), run_time=2.0)
    one = result_label("one motion", cfg.GOLD, cfg.FONT["section"]).next_to(tiles, DOWN, buff=0.5)
    scene.play(FadeIn(one, shift=UP * 0.1), view.run(view.clock.value + 1.0), run_time=1.0)
    scene.play(view.run(view.clock.value + 5.0), run_time=5.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["14"])
