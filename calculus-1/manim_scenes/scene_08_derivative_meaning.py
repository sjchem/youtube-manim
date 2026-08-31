"""Scene 08: a derivative is instantaneous change, in every disguise — and the closing synthesis."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axis_labels,
    calc_axes,
    car_icon,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    population_icon,
    secant_line,
    speedometer_icon,
    tangent_line,
    thermometer_icon,
)
from utils.math_utils import car_position, car_velocity, square


def _hill(x: float) -> float:
    return -0.32 * x * x + 2.0


def _d_hill(x: float) -> float:
    return -0.64 * x


class Scene08DerivativeMeaning(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "08")
    add_cinematic_background(scene)

    slope_word = outlined_text("SLOPE", cfg.FONT["hero"], cfg.MUTED, BOLD)
    paced_play(scene, FadeIn(slope_word, scale=0.9), run_time=1.0)
    narration_wait(scene, 5.65)
    change_word = outlined_text("INSTANTANEOUS CHANGE", cfg.FONT["title"], cfg.GOLD, BOLD)
    if change_word.width > cfg.SAFE_WIDTH:
        change_word.scale_to_fit_width(cfg.SAFE_WIDTH)
    paced_play(scene, ReplacementTransform(slope_word, change_word), run_time=1.1)
    narration_wait(scene, 13.55)
    paced_play(scene, FadeOut(change_word), run_time=0.7)

    # -- Beat 1: the same idea, four disguises --
    car = car_icon(cfg.CYAN, scale=1.0)
    dial = speedometer_icon(cfg.ORANGE, scale=1.0)
    bulb = thermometer_icon(cfg.RED, scale=1.0)
    bars = population_icon(cfg.GREEN, scale=1.0)
    icons = VGroup(car, dial, bulb, bars).arrange(RIGHT, buff=1.7).move_to([0, 1.2, 0])
    formulas = VGroup(
        eq(r"\frac{ds}{dt}=v", cfg.CYAN, cfg.FONT["section"]),
        eq(r"\frac{dv}{dt}=a", cfg.ORANGE, cfg.FONT["section"]),
        eq(r"\frac{dT}{dt}", cfg.RED, cfg.FONT["section"]),
        eq(r"\frac{dP}{dt}", cfg.GREEN, cfg.FONT["section"]),
    )
    for formula, icon in zip(formulas, icons):
        formula.next_to(icon, DOWN, buff=0.5)

    labels = ["moving car", "changing velocity", "warming room", "growing population"]
    for icon, formula, label_text in zip(icons, formulas, labels):
        cap = bottom_caption(f"For a {label_text}...", cfg.WHITE)
        paced_play(scene, FadeIn(icon, scale=1.15), Write(formula), FadeIn(cap), run_time=1.4)
        if icon is not icons[-1]:
            paced_play(scene, FadeOut(cap), run_time=0.5)
        else:
            paced_play(scene, FadeOut(cap), run_time=0.5)
        narration_wait(scene, 5.65)

    narration_wait(scene, 3.39)
    paced_play(scene, FadeOut(VGroup(icons, formulas)), run_time=0.9)

    # -- Beat 2: sign of the derivative --
    axes = calc_axes(x_range=(-3.2, 3.2, 1), y_range=(-1.5, 2.5, 1), x_length=9.6, y_length=5.2).move_to([0, -0.5, 0])
    axis_labels = calc_axis_labels(axes)
    hill = axes.plot(_hill, x_range=[-3, 3], color=cfg.WHITE, stroke_width=6)
    paced_play(scene, Create(axes), FadeIn(axis_labels), Create(hill), run_time=1.4)
    narration_wait(scene, 1.69)

    rising_x, peak_x, falling_x = -1.9, 0.0, 1.9
    rising = tangent_line(axes, _hill, _d_hill, rising_x, cfg.GREEN, half_length=1.1)
    peak = tangent_line(axes, _hill, _d_hill, peak_x, cfg.GOLD, half_length=1.1)
    falling = tangent_line(axes, _hill, _d_hill, falling_x, cfg.RED, half_length=1.1)
    rising_label = eq(r"f'(x)>0", cfg.GREEN, cfg.FONT["body"])
    rising_label.next_to(rising, UP, buff=0.28).shift(LEFT * 0.55)
    peak_label = eq(r"f'(x)=0", cfg.GOLD, cfg.FONT["body"])
    peak_label.next_to(peak, UP, buff=0.3).shift(RIGHT * 1.9)
    falling_label = eq(r"f'(x)<0", cfg.RED, cfg.FONT["body"])
    falling_label.next_to(falling, UP, buff=0.28).shift(RIGHT * 0.55)

    paced_play(scene, FadeIn(rising), FadeIn(rising_label), run_time=1.0)
    narration_wait(scene, 5.65)
    paced_play(scene, FadeIn(falling), FadeIn(falling_label), run_time=1.0)
    narration_wait(scene, 5.65)
    paced_play(scene, FadeIn(peak), FadeIn(peak_label), run_time=1.0)
    narration_wait(scene, 6.78)

    full_stop = bottom_caption("A derivative is instantaneous change. Full stop.", cfg.GOLD)
    paced_play(
        scene,
        FadeOut(VGroup(axes, axis_labels, hill, rising, falling, peak, rising_label, falling_label, peak_label)),
        FadeIn(full_stop),
        run_time=1.1,
    )
    narration_wait(scene, 10.16)
    paced_play(scene, FadeOut(full_stop), run_time=0.6)

    # -- Beat 4: return to the moving car --
    road_y = 2.2
    road = Line([-6.0, road_y, 0], [6.0, road_y, 0], color=cfg.GRAY, stroke_width=5)
    small_axes = calc_axes(x_range=(0, 5, 1), y_range=(0, 16, 4), x_length=9.4, y_length=3.9).move_to([0, -1.5, 0])
    small_axis_labels = calc_axis_labels(small_axes, "t", "s(t)")
    small_curve = small_axes.plot(car_position, x_range=[0, 3.2], color=cfg.CYAN, stroke_width=5)
    car2 = car_icon(cfg.CYAN, scale=0.7).move_to([-6.0 + (car_position(2.6) / 16.0) * 12.0, road_y + 0.2, 0])
    back_caption = bottom_caption("One car, one road, one honest question.", cfg.WHITE)
    paced_play(scene, Create(road), FadeIn(car2), Create(small_axes), FadeIn(small_axis_labels), Create(small_curve), FadeIn(back_caption), run_time=1.8)
    narration_wait(scene, 6.78)

    t0 = 2.0
    h_tracker = ValueTracker(1.0)
    secant = always_redraw(lambda: secant_line(small_axes, car_position, t0, h_tracker.get_value(), cfg.CYAN))
    scene.add(secant)
    interval_caption = bottom_caption("Delta x over delta t... then shrink delta t to zero.", cfg.GOLD)
    paced_play(scene, ReplacementTransform(back_caption, interval_caption), run_time=0.7)
    for target_h in (0.3, 0.05, 0.005):
        paced_play(scene, h_tracker.animate.set_value(target_h), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 6.78)

    tangent2 = tangent_line(small_axes, car_position, car_velocity, t0, cfg.GREEN, half_length=1.6)
    paced_play(scene, FadeIn(tangent2), run_time=0.9)
    narration_wait(scene, 5.65)

    paced_play(scene, FadeOut(VGroup(road, car2, small_axes, small_axis_labels, small_curve, secant, tangent2, interval_caption)), run_time=0.9)

    # -- Beat 5: the formal definition, large and final --
    definition = eq(r"f'(x)=\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}", cfg.WHITE, cfg.FONT["hero"])
    definition.set_color_by_tex(r"\lim", cfg.PURPLE)
    if definition.width > cfg.SAFE_WIDTH:
        definition.scale_to_fit_width(cfg.SAFE_WIDTH)
    definition.move_to([0, 0.6, 0])
    paced_play(scene, Write(definition), run_time=1.8)
    narration_wait(scene, 13.55)

    closing_1 = bottom_caption("Limits tell us what happens as we approach the infinitely small.", cfg.CYAN)
    paced_play(scene, FadeIn(closing_1), run_time=0.8)
    narration_wait(scene, 6.78)
    closing_2 = bottom_caption("Derivatives measure change at a single instant.", cfg.GOLD)
    paced_play(scene, ReplacementTransform(closing_1, closing_2), run_time=0.7)
    narration_wait(scene, 6.78)
    closing_3 = bottom_caption("That one idea is the doorway to all of calculus.", cfg.WHITE)
    paced_play(scene, ReplacementTransform(closing_2, closing_3), run_time=0.7)
    narration_wait(scene, 3.2)

    next_label = outlined_text("NEXT  •  PART 2", cfg.FONT["small"], cfg.CYAN, BOLD)
    next_title = outlined_text("FROM DERIVATIVES TO INTEGRALS", cfg.FONT["section"], cfg.GOLD, BOLD)
    if next_title.width > cfg.SAFE_WIDTH:
        next_title.scale_to_fit_width(cfg.SAFE_WIDTH)
    next_card = VGroup(next_label, next_title).arrange(DOWN, buff=0.22).move_to(ORIGIN)
    paced_play(
        scene,
        FadeOut(VGroup(definition, closing_3)),
        FadeIn(next_card, shift=UP * 0.15),
        run_time=1.1,
    )
    narration_wait(scene, 2.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["08"])
