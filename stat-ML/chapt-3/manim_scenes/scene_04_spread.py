"""Scene 04 - variance and standard deviation."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, deterministic_values, end_scene, equation_box, label_pill, narration_wait, number_line_with_dots, paced_play, scene_title, vertical_marker


class Scene04Spread(Scene):
    """Turn deviations into variance and standard deviation."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "04")
    scene.add(cinematic_background())

    values = deterministic_values()
    mean = float(np.mean(values))
    line, dots = number_line_with_dots(values, x_min=0, x_max=8)
    VGroup(line, dots).move_to(DOWN * 1.25)
    title = scene_title("Spread Measures the Room Around Center", "deviations become squared distance").to_edge(UP, buff=0.42)
    title.scale(0.82).to_edge(UP, buff=0.22)
    mean_marker = vertical_marker(line, mean, "mean", cfg.CYAN)
    mean_marker[1].next_to(mean_marker[0], DOWN, buff=0.12)

    paced_play(scene, FadeIn(title), Create(line), LaggedStart(*[FadeIn(dot, scale=0.35) for dot in dots], lag_ratio=0.04), FadeIn(mean_marker), run_time=1.35)

    deviations = VGroup()
    squares = VGroup()
    for dot, value in zip(dots, values):
        start = line.n2p(mean) + UP * 0.05
        end = dot.get_center() + DOWN * 0.1
        deviations.add(Line(start, end, color=cfg.GOLD, stroke_width=2.4, stroke_opacity=0.75))
        side = min(0.42, 0.08 + abs(value - mean) * 0.13)
        sq = Square(side_length=side, fill_color=cfg.GOLD, fill_opacity=0.16, stroke_color=cfg.GOLD, stroke_width=1.5).move_to(dot.get_center() + UP * 0.45)
        squares.add(sq)

    paced_play(scene, LaggedStart(*[Create(dev) for dev in deviations], lag_ratio=0.03), run_time=1.0)
    paced_play(scene, LaggedStart(*[FadeIn(sq, scale=0.4) for sq in squares], lag_ratio=0.03), run_time=0.9)

    busy_layer = VGroup(deviations, squares)
    variance = equation_box(r"\sigma^2={1\over n}\sum (x_i-\mu)^2", cfg.GOLD, font_size=40).move_to(LEFT * 2.65 + UP * 0.62)
    std = equation_box(r"\sigma=\sqrt{\sigma^2}", cfg.GREEN, font_size=42).move_to(RIGHT * 3.05 + UP * 0.62)
    arrow = Arrow(variance.get_right(), std.get_left(), color=cfg.GREEN, stroke_width=6, buff=0.18)
    note = label_pill("standard units again", cfg.GREEN, font_size=21).next_to(std, DOWN, buff=0.12)

    paced_play(scene, FadeOut(busy_layer, shift=DOWN * 0.08), FadeIn(variance, shift=DOWN * 0.15), run_time=0.75)
    paced_play(scene, GrowArrow(arrow), FadeIn(std, shift=LEFT * 0.16), FadeIn(note), run_time=0.9)
    paced_play(scene, Indicate(std, color=cfg.WHITE), run_time=0.7)

    caption = VGroup(
        Text("Variance exaggerates distance.", font_size=27, color=cfg.WHITE, weight=BOLD),
        Text("Standard deviation brings it back to scale.", font_size=27, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.08)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.32)
    paced_play(scene, FadeIn(caption), run_time=0.7)
    narration_wait(scene, 0.45)
    end_scene(scene, scene_start)
