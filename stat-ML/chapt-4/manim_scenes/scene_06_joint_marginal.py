"""Scene 06 - random variables, distributions, and expected value."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    coin_icon,
    distribution_bars,
    end_scene,
    equation_box,
    narration_wait,
    paced_play,
    scene_title,
)


class Scene06JointMarginal(Scene):
    """Show random variables, discrete/continuous distributions, and E[X]."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "06")
    scene.add(cinematic_background())

    title = scene_title("Random variables turn uncertain outcomes into math").to_edge(UP, buff=0.34)
    paced_play(scene, FadeIn(title), run_time=0.8)

    coin = coin_icon("H", cfg.GOLD, radius=0.42).move_to(LEFT * 5.0 + UP * 1.25)
    mapping = equation_box(r"X=\begin{cases}1,& \text{Head}\\0,& \text{Tail}\end{cases}", cfg.GOLD, font_size=33)
    mapping.next_to(coin, RIGHT, buff=0.45)
    feature_note = Text("ML features become random variables.", font_size=19, color=cfg.WHITE, weight=BOLD)
    feature_note.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    feature_note.move_to(RIGHT * 2.9 + UP * 1.35)

    paced_play(scene, FadeIn(coin, scale=0.5), Rotate(coin, angle=PI, axis=UP), run_time=0.8)
    paced_play(scene, FadeIn(mapping, shift=RIGHT * 0.12), FadeIn(feature_note), run_time=0.9)
    narration_wait(scene, 0.45)

    dice_bars = distribution_bars(
        labels=["1", "2", "3", "4", "5", "6"],
        values=[1 / 6] * 6,
        colors=[cfg.CYAN, cfg.CYAN, cfg.CYAN, cfg.CYAN, cfg.CYAN, cfg.CYAN],
        max_height=1.55,
        bar_width=0.34,
        gap=0.62,
    ).move_to(LEFT * 3.45 + DOWN * 1.25)
    dice_label = Text("Discrete: dice outcomes", font_size=20, color=cfg.CYAN, weight=BOLD)
    dice_label.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    dice_label.next_to(dice_bars, UP, buff=0.25)

    axes = Axes(
        x_range=[-3, 3, 1],
        y_range=[0, 1, 0.5],
        x_length=3.3,
        y_length=1.8,
        tips=False,
        axis_config={"stroke_color": cfg.MUTED, "stroke_opacity": 0.65, "stroke_width": 1.6},
    )
    curve = axes.plot(lambda x: np.exp(-(x**2) / 2), color=cfg.GOLD, stroke_width=4)
    bell_group = VGroup(axes, curve).move_to(RIGHT * 2.8 + DOWN * 1.2)
    bell_label = Text("Continuous: normal curve", font_size=20, color=cfg.GOLD, weight=BOLD)
    bell_label.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    bell_label.next_to(bell_group, UP, buff=0.25)

    paced_play(scene, FadeIn(dice_label), LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in dice_bars[0]], lag_ratio=0.08), run_time=1.1)
    paced_play(scene, FadeIn(dice_bars[1]), FadeIn(dice_bars[2]), Create(axes), Create(curve), FadeIn(bell_label), run_time=1.1)
    narration_wait(scene, 0.45)

    expected = equation_box(r"E[X] = \sum_x xP(x)\quad \text{fair die: }3.5", cfg.GREEN, font_size=31)
    expected.to_edge(DOWN, buff=0.55)
    paced_play(scene, FadeIn(expected, shift=UP * 0.12), run_time=1.0)
    narration_wait(scene, 0.9)

    end_scene(scene, scene_start)
