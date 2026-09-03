"""Scene 07: a ball crosses a hill — the derivative crosses zero exactly at the peak."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    calc_axis_labels,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    paced_play,
    tangent_line,
)
from utils.math_utils import d_hill_fn, hill_fn


def _slope_color(x: float) -> str:
    slope = d_hill_fn(x)
    if slope > 0.12:
        return cfg.GREEN
    if slope < -0.12:
        return cfg.RED
    return cfg.GOLD


class Scene07MaximaMinima(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "07")
    add_cinematic_background(scene)

    top_axes = calc_axes(x_range=(-3, 3, 1), y_range=(-1, 4, 1), x_length=9.4, y_length=3.4).move_to([0, 1.9, 0])
    top_labels = calc_axis_labels(top_axes, "x", "f(x)")
    top_curve = top_axes.plot(hill_fn, x_range=[-2.9, 2.9], color=cfg.WHITE, stroke_width=6)

    bottom_axes = calc_axes(x_range=(-3, 3, 1), y_range=(-2.5, 2.5, 1), x_length=9.4, y_length=2.9).move_to([0, -2.35, 0])
    bottom_labels = calc_axis_labels(bottom_axes, "x", "f'(x)")
    zero_line = Line(bottom_axes.c2p(-3, 0), bottom_axes.c2p(3, 0), color=cfg.GRAY, stroke_width=2)

    paced_play(scene, Create(top_axes), FadeIn(top_labels), Create(top_curve), run_time=1.3)
    paced_play(scene, Create(bottom_axes), FadeIn(bottom_labels), Create(zero_line), run_time=1.0)
    narration_wait(scene, 4.96)

    x_t = ValueTracker(-2.8)
    ball = always_redraw(lambda: glow_dot(top_axes.c2p(x_t.get_value(), hill_fn(x_t.get_value())), _slope_color(x_t.get_value()), 0.1))
    tangent = always_redraw(lambda: tangent_line(top_axes, hill_fn, d_hill_fn, x_t.get_value(), _slope_color(x_t.get_value()), half_length=0.7))
    bottom_dot = always_redraw(lambda: glow_dot(bottom_axes.c2p(x_t.get_value(), d_hill_fn(x_t.get_value())), _slope_color(x_t.get_value()), 0.08))
    bottom_trace = TracedPath(lambda: bottom_axes.c2p(x_t.get_value(), d_hill_fn(x_t.get_value())), stroke_color=cfg.CYAN, stroke_width=5)

    scene.add(bottom_trace, tangent, ball, bottom_dot)
    paced_play(scene, FadeIn(ball), FadeIn(tangent), FadeIn(bottom_dot), run_time=0.6)

    rising_caption = bottom_caption("Rising: f'(x) > 0.", cfg.GREEN)
    paced_play(scene, FadeIn(rising_caption), run_time=0.6)
    paced_play(scene, x_t.animate.set_value(-0.4), run_time=6.5, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 1.89)

    peak_caption = bottom_caption("At the top: f'(x) = 0. The tangent goes flat.", cfg.GOLD)
    paced_play(scene, ReplacementTransform(rising_caption, peak_caption), run_time=0.6)
    paced_play(scene, x_t.animate.set_value(0.0), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 7.29)

    falling_caption = bottom_caption("Falling: f'(x) < 0.", cfg.RED)
    paced_play(scene, ReplacementTransform(peak_caption, falling_caption), run_time=0.6)
    paced_play(scene, x_t.animate.set_value(2.8), run_time=6.5, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 1.89)
    paced_play(scene, FadeOut(falling_caption), run_time=0.5)

    box_text = eq(r"\text{maximum} \;\Longleftrightarrow\; \text{change switches direction}", cfg.GOLD, cfg.FONT["small"])
    box_text.to_edge(DOWN, buff=0.45)
    box_outline = SurroundingRectangle(box_text, color=cfg.GOLD, buff=0.24, corner_radius=0.12)
    paced_play(scene, FadeIn(box_text), Create(box_outline), run_time=1.1)
    narration_wait(scene, 14.46)

    end_scene(scene, started, cfg.SCENE_DURATIONS["07"])
