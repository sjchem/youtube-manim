"""Scene 06: a moving tangent on f(x) = x^2 draws an entire new function, f'(x) = 2x."""

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
from utils.math_utils import d_square_fn, square_fn


class Scene06DerivativeNewFunction(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "06")
    add_cinematic_background(scene)

    top_axes = calc_axes(x_range=(-2.5, 2.5, 1), y_range=(-0.5, 5, 1), x_length=9.2, y_length=3.1).move_to([0, 2.0, 0])
    top_labels = calc_axis_labels(top_axes, "x", "f(x)")
    top_title = eq("f(x)=x^2", cfg.WHITE, cfg.FONT["small"]).next_to(top_axes, LEFT, buff=0.3)
    top_curve = top_axes.plot(square_fn, x_range=[-2.3, 2.3], color=cfg.WHITE, stroke_width=6)

    bottom_axes = calc_axes(x_range=(-2.5, 2.5, 1), y_range=(-5, 5, 2.5), x_length=9.2, y_length=3.1).move_to([0, -2.15, 0])
    bottom_labels = calc_axis_labels(bottom_axes, "x", "f'(x)")
    bottom_title = eq("f'(x)=\\;?", cfg.GREEN, cfg.FONT["small"]).next_to(bottom_axes, LEFT, buff=0.3)

    paced_play(scene, Create(top_axes), FadeIn(top_labels), FadeIn(top_title), Create(top_curve), run_time=1.3)
    paced_play(scene, Create(bottom_axes), FadeIn(bottom_labels), FadeIn(bottom_title), run_time=1.0)
    narration_wait(scene, 5.88)

    x_t = ValueTracker(-2.3)
    top_tangent = always_redraw(lambda: tangent_line(top_axes, square_fn, d_square_fn, x_t.get_value(), cfg.CYAN, half_length=0.4))
    top_point = always_redraw(lambda: glow_dot(top_axes.c2p(x_t.get_value(), square_fn(x_t.get_value())), cfg.WHITE, 0.09))
    bottom_point = always_redraw(lambda: glow_dot(bottom_axes.c2p(x_t.get_value(), d_square_fn(x_t.get_value())), cfg.GREEN, 0.09))
    bottom_trace = TracedPath(lambda: bottom_axes.c2p(x_t.get_value(), d_square_fn(x_t.get_value())), stroke_color=cfg.GREEN, stroke_width=5)

    scene.add(bottom_trace, top_tangent, top_point, bottom_point)
    paced_play(scene, FadeIn(top_tangent), FadeIn(top_point), FadeIn(bottom_point), run_time=0.6)

    marks = VGroup()
    for index, (target_x, slope_text) in enumerate(((-2.0, "-4"), (-1.0, "-2"), (0.0, "0"), (1.0, "2"), (2.0, "4"))):
        move_time = 1.8 if index == 0 else 3.0
        hold_time = 2.93 if index == 0 else 1.73
        paced_play(scene, x_t.animate.set_value(target_x), run_time=move_time, rate_func=rate_functions.ease_in_out_sine)
        mark = glow_dot(bottom_axes.c2p(target_x, d_square_fn(target_x)), cfg.GOLD, 0.07)
        tag = eq(slope_text, cfg.GOLD, cfg.FONT["tiny"]).next_to(mark, UP, buff=0.1)
        marks.add(mark, tag)
        paced_play(scene, FadeIn(mark), FadeIn(tag), run_time=0.5)
        narration_wait(scene, hold_time)

    paced_play(scene, x_t.animate.set_value(2.3), run_time=1.4)
    narration_wait(scene, 3.12)

    caption = bottom_caption("Five slopes. One straight pattern: f'(x) = 2x.", cfg.GREEN)
    updated_title = eq("f'(x)=2x", cfg.GREEN, cfg.FONT["small"]).move_to(bottom_title)
    paced_play(scene, ReplacementTransform(bottom_title, updated_title), FadeIn(caption), run_time=1.0)
    narration_wait(scene, 11.75)
    paced_play(scene, FadeOut(caption), run_time=0.5)

    closing = bottom_caption("Not just a slope — an entire new function, describing change everywhere.", cfg.WHITE)
    paced_play(scene, FadeIn(closing), run_time=0.9)
    narration_wait(scene, 13.71)

    end_scene(scene, started, cfg.SCENE_DURATIONS["06"])
