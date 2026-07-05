"""Scene 02 - mean, median, and mode as different centers."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, deterministic_values, end_scene, equation_box, label_pill, narration_wait, number_line_with_dots, paced_play, scene_title


class Scene02Center(Scene):
    """Show center as balance, split, and repeated value."""

    def construct(self) -> None:
        play_scene(self)


def center_callout(line: NumberLine, value: float, label: str, detail: str, color: str, position: np.ndarray) -> VGroup:
    """Create a clean upper callout connected to a number-line marker."""
    base = line.n2p(value)
    marker = Line(base + DOWN * 0.34, base + UP * 0.72, color=color, stroke_width=5)
    label_mob = label_pill(label, color=color, font_size=23)
    detail_mob = Text(detail, font_size=20, color=cfg.WHITE, weight=BOLD)
    detail_mob.set_stroke("#02111D", width=3, opacity=0.75, background=True)
    card = VGroup(label_mob, detail_mob).arrange(DOWN, buff=0.1).move_to(position)
    connector = Line(card.get_bottom() + DOWN * 0.04, marker.get_top(), color=color, stroke_width=2.5, stroke_opacity=0.65)
    return VGroup(marker, connector, card)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "02")
    scene.add(cinematic_background())

    values = deterministic_values()
    mean = float(np.mean(values))
    median = float(np.median(values))
    line, dots = number_line_with_dots(values, x_min=0, x_max=8)
    group = VGroup(line, dots).move_to(DOWN * 1.25)
    title = scene_title("Three Kinds of Center", "balance point, middle point, repeated point").to_edge(UP, buff=0.42)

    paced_play(scene, FadeIn(title), run_time=0.7)
    paced_play(scene, Create(line), LaggedStart(*[FadeIn(dot, scale=0.3) for dot in dots], lag_ratio=0.05), run_time=1.45)

    mean_marker = center_callout(line, mean, "mean", "balance", cfg.CYAN, RIGHT * 4.0 + UP * 1.2)
    median_marker = center_callout(line, median, "median", "middle", cfg.GREEN, UP * 1.25)
    mode_marker = center_callout(line, 2.0, "mode", "most frequent", cfg.GOLD, LEFT * 4.0 + UP * 1.2)

    balance = Triangle(color=cfg.CYAN, fill_color=cfg.CYAN, fill_opacity=0.35).scale(0.22).rotate(PI).move_to(line.n2p(mean) + DOWN * 0.55)
    split_left = BraceBetweenPoints(line.n2p(values[0]) + DOWN * 0.06, line.n2p(median) + DOWN * 0.06, color=cfg.GREEN)
    split_right = BraceBetweenPoints(line.n2p(median) + DOWN * 0.06, line.n2p(values[-1]) + DOWN * 0.06, color=cfg.GREEN)
    split_labels = VGroup(
        Text("half", font_size=22, color=cfg.GREEN, weight=BOLD).next_to(split_left, DOWN, buff=0.08),
        Text("half", font_size=22, color=cfg.GREEN, weight=BOLD).next_to(split_right, DOWN, buff=0.08),
    )

    paced_play(scene, FadeIn(mean_marker), FadeIn(balance, shift=UP * 0.15), run_time=0.8)
    paced_play(scene, Indicate(balance, color=cfg.WHITE, scale_factor=1.2), run_time=0.65)
    paced_play(scene, FadeIn(median_marker), GrowFromCenter(split_left), GrowFromCenter(split_right), FadeIn(split_labels), run_time=0.95)

    repeated = VGroup(*[Dot(line.n2p(2.0) + UP * (0.26 + i * 0.12), radius=0.075, color=cfg.GOLD) for i in range(3)])
    paced_play(scene, FadeIn(mode_marker), LaggedStart(*[Flash(dot, color=cfg.GOLD, flash_radius=0.25) for dot in repeated], lag_ratio=0.08), run_time=1.0)

    equation = equation_box(r"\bar{x}={1\over n}\sum_{i=1}^{n}x_i", cfg.CYAN, font_size=44).to_edge(DOWN, buff=0.32)
    caption = Text("One word, center, can mean three different operations.", font_size=26, color=cfg.WHITE, weight=BOLD)
    caption.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    caption.next_to(equation, UP, buff=0.16)
    lower_guides = VGroup(split_left, split_right, split_labels)
    paced_play(scene, FadeOut(lower_guides, shift=DOWN * 0.1), FadeIn(equation, shift=UP * 0.18), FadeIn(caption), run_time=0.9)
    narration_wait(scene, 0.4)
    end_scene(scene, scene_start)
