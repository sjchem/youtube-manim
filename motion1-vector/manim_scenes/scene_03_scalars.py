"""Scene 03 — scalars. The brief's six scalar cards (from
``physics_models.SCALARS``), a thermometer falling to minus five degrees (a
negative scalar is not a direction), a runner covering 100 m in 10 s for an
average speed of 10 m/s, and a speedometer reading 20 m/s that cannot say
which way the car is going.
"""

from manim_scenes.common import *

RUN_M, RUN_S = pm.SPRINT


class Scene03Scalars(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "03")
    opener = txt("Scalars and vectors", cfg.FONT["title"], cfg.WHITE)
    fit_width(opener, 12.4)
    opener.move_to(ORIGIN)
    scene.play(FadeIn(opener, shift=LEFT * 0.3), run_time=0.9)
    scene.wait(1.2)
    scene.play(FadeOut(opener, shift=UP * 0.3), run_time=0.6)
    head = heading("Scalars")
    cards = VGroup(*[scalar_card(name, value, cfg.WHITE, width=3.8) for name, value in pm.SCALARS])
    cards.arrange_in_grid(rows=2, cols=3, buff=(0.45, 0.5)).scale(1.18).move_to(DOWN * 0.1)
    scene.play(FadeIn(head, shift=DOWN * 0.15),
               LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards[:3]], lag_ratio=0.35), run_time=2.0)

    # --- 2. Distance, speed, energy ----------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards[3:]], lag_ratio=0.35), run_time=2.0)

    # --- 3. A scalar: a magnitude and a unit, no direction ---------------------------------------------------------
    beat(scene, t, 2)
    scene.play(*[c.number.animate.set_color(cfg.CYAN) for c in cards], run_time=1.0)
    rule = VGroup(txt("scalar", cfg.FONT["section"], cfg.CYAN), txt("=", cfg.FONT["section"], cfg.WHITE),
                  txt('value + unit', cfg.FONT["section"], cfg.WHITE)).arrange(RIGHT, buff=0.3)
    rule.move_to(DOWN * 3.55)
    scene.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
    no_dir = VGroup(txt("no direction", cfg.FONT["label"], cfg.MUTED), cross_mark(0.22)).arrange(RIGHT, buff=0.3)
    no_dir.next_to(head, DOWN, buff=0.25)
    scene.play(FadeIn(no_dir), run_time=0.8)

    # --- 4. Minus five degrees is still a scalar --------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(VGroup(cards, rule, no_dir)), run_time=0.7)
    thermo = Thermometer([-3.0, -0.3, 0], low=-15, high=35, height=5.0)
    thermo.celsius.value = 25.0
    reading = VGroup(DecimalNumber(25, num_decimal_places=0, font_size=96, color=cfg.WHITE, include_sign=False),
                     txt("°C", cfg.FONT["title"], cfg.WHITE)).arrange(RIGHT, buff=0.24, aligned_edge=UP)
    reading.move_to([1.6, 1.0, 0])
    reading[0].add_updater(lambda m: m.set_value(round(thermo.celsius.value)))
    reading[1].add_updater(lambda m: m.next_to(reading[0], RIGHT, buff=0.24, aligned_edge=UP))
    scene.play(FadeIn(thermo), FadeIn(reading), run_time=0.8)
    scene.play(thermo.celsius.to(thermo, pm.COLD, run_time=3.0))
    reading[0].clear_updaters()
    reading[1].clear_updaters()
    still = VGroup(txt('scalar', cfg.FONT["section"], cfg.CYAN),
                   txt('T < 0 °C', cfg.FONT["small"], cfg.MUTED)).arrange(DOWN, buff=0.3)
    still.next_to(reading, DOWN, buff=0.6)
    scene.play(FadeIn(still[0], shift=UP * 0.15), run_time=0.8)
    scene.play(FadeIn(still[1]), run_time=0.8)

    # --- 5. Speed is a scalar too ---------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    thermo.column.clear_updaters()
    scene.play(FadeOut(VGroup(thermo, reading, still)), run_time=0.7)
    lane_y = -1.6
    left, right = np.array([-6.0, lane_y, 0]), np.array([4.0, lane_y, 0])
    lane = VGroup(Line(left + DOWN * 0.45, right + DOWN * 0.45, stroke_color=cfg.MUTED, stroke_width=3),
                  Line(left + UP * 0.45, right + UP * 0.45, stroke_color=cfg.MUTED, stroke_width=3),
                  Line(left + DOWN * 0.45, left + UP * 0.45, stroke_color=cfg.WHITE, stroke_width=5),
                  Line(right + DOWN * 0.45, right + UP * 0.45, stroke_color=cfg.GREEN, stroke_width=5))
    marks = VGroup(txt("0 m", cfg.FONT["tiny"], cfg.MUTED).next_to(left, DOWN, buff=0.6),
                   txt(f"{RUN_M:.0f} m", cfg.FONT["tiny"], cfg.GREEN).next_to(right, DOWN, buff=0.6))
    run = Knob(0.0)
    runner = bead(left, cfg.POSITION, 0.24, glow=0.8)
    runner.add_updater(lambda m: m.move_to(left + (right - left) * run.value))
    watch = stopwatch([5.6, -1.2, 0], 0.85)
    clock = VGroup(DecimalNumber(0, num_decimal_places=1, font_size=56, color=cfg.WHITE), txt("s", cfg.FONT["label"], cfg.MUTED))
    clock.arrange(RIGHT, buff=0.22, aligned_edge=DOWN).next_to(watch, UP, buff=0.3)
    clock[0].add_updater(lambda m: m.set_value(run.value * RUN_S))
    clock[1].add_updater(lambda m: m.next_to(clock[0], RIGHT, buff=0.22, aligned_edge=DOWN))
    centre = watch.face.get_center()
    watch.hand.add_updater(lambda m: m.put_start_and_end_on(
        centre, centre + 0.62 * np.array([np.sin(TAU * run.value), np.cos(TAU * run.value), 0])))
    scene.play(FadeIn(lane), FadeIn(marks), FadeIn(runner), FadeIn(watch), FadeIn(clock), run_time=1.0)

    # --- 6. Average speed = total distance / elapsed time --------------------------------------------------------------------------------
    beat(scene, t, 5)
    formula = eq([r"\text{average speed}", "=", r"\frac{\text{total distance}}{\text{elapsed time}}"], cfg.FONT["section"])
    formula.move_to([-0.6, 1.9, 0])
    scene.play(Write(formula), run_time=1.6)

    # --- 7. 100 m in 10 s -> 10 m/s ------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(run.to(runner, 1.0, run_time=5.0, rate_func=linear))
    for m in (runner, clock[0], clock[1], watch.hand):
        m.clear_updaters()
    numbers = eq([r"\frac{100\ \mathrm{m}}{10\ \mathrm{s}}", "=", r"10\ \mathrm{m/s}"], cfg.FONT["section"])
    numbers[2].set_color(cfg.GREEN)
    numbers.next_to(formula, DOWN, buff=0.45)
    scene.play(Write(numbers), run_time=1.4)
    scene.play(Indicate(numbers[2], color=cfg.GREEN, scale_factor=1.12), run_time=1.0)

    # --- 8. A speedometer reads 20 m/s ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    scene.play(FadeOut(VGroup(lane, marks, runner, watch, clock, formula, numbers)), run_time=0.7)
    gauge = Speedometer([0, -0.1, 0], radius=2.0, value=0.0)
    scene.play(FadeIn(gauge, scale=0.9), run_time=0.8)
    scene.play(gauge.value.to(gauge, pm.CAR_SPEED, run_time=2.0))

    # --- 9. Which way is the car going? --------------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    centre = gauge.face.get_center()
    guesses = VGroup()
    for d, name in ((UP, "N"), (RIGHT, "E"), (DOWN, "S"), (LEFT, "W")):
        arrow = VecArrow(centre + d * 2.35, centre + d * 3.3, cfg.GOLD, width=0.1)
        tag = VGroup(txt(name, cfg.FONT["label"], cfg.GOLD), txt("?", cfg.FONT["label"], cfg.RED)).arrange(RIGHT, buff=0.08)
        tag.move_to(centre + d * 3.3 + (d if abs(d[1]) < 0.5 else d * 0.0) * 0.6 + (RIGHT * 0.7 if abs(d[1]) > 0.5 else ORIGIN))
        guesses.add(VGroup(arrow, tag))
    scene.play(LaggedStart(*[FadeIn(g, shift=g[0].tip() - g[0].tail()) for g in guesses], lag_ratio=0.3), run_time=2.4)
    scene.play(*[Indicate(g[1][1], color=cfg.RED) for g in guesses], run_time=1.2)

    # --- 10. A magnitude isn't enough for motion through space -----------------------------------------------------------------------------------------
    beat(scene, t, 9)
    scene.play(FadeOut(guesses), gauge.animate.scale(0.7).move_to([-4.2, -0.2, 0]), run_time=1.0)
    gauge.needle.clear_updaters()
    enough = VGroup(txt('mass · temperature', cfg.FONT["label"], cfg.MUTED), txt('value + unit', cfg.FONT["label"], cfg.CYAN),
                    txt('velocity', cfg.FONT["label"], cfg.MUTED), txt('+ direction', cfg.FONT["label"], cfg.GOLD))
    enough.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([2.6, -0.2, 0])
    enough[2].shift(DOWN * 0.3)
    enough[3].shift(DOWN * 0.3)
    scene.play(FadeIn(enough[:2], shift=LEFT * 0.2), run_time=1.0)
    scene.wait(2.5)
    scene.play(FadeIn(enough[2:], shift=LEFT * 0.2), run_time=1.0)

    # --- 11. Direction --------------------------------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(enough, gauge)), FadeOut(head), run_time=0.8)
    word = result_label('Direction', cfg.GOLD, cfg.FONT["hero"]).move_to(UP * 0.9)
    spin = Knob(0.0)
    pointer = VecArrow(DOWN * 1.6, lambda: DOWN * 1.6 + 1.5 * np.array([np.cos(spin.value), np.sin(spin.value), 0]),
                       cfg.GOLD, width=0.12)
    scene.add(pointer)
    scene.play(FadeIn(word, scale=0.9), pointer.grow_in(run_time=1.0), run_time=1.0)
    scene.play(spin.to(pointer, TAU, run_time=4.5, rate_func=smooth))
    end_scene(scene, t, cfg.SCENE_DURATIONS["03"])
