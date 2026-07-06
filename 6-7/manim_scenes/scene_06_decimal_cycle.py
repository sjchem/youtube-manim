"""Scene 6: long division by 7 creates a six-step cycle."""

from __future__ import annotations

import math

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, digit_wheel, end_scene, equation, label, paced_play
from utils.math_utils import long_division_by_7


class Scene06DecimalCycle(MovingCameraScene):
    """Show the remainder loop behind 1/7."""

    def construct(self) -> None:
        play_scene_06(self)


def play_scene_06(scene: Scene) -> None:
    start = begin_scene(scene)

    heading = label("But 7 hides order in time", cfg.PURPLE, 38).to_edge(UP, buff=0.48)
    frac = equation(r"{1\over7}=0.142857142857\ldots", cfg.WHITE, 58).shift(UP * 2.2)
    wheel = digit_wheel("142857", radius=1.85, color=cfg.GOLD).shift(LEFT * 3.0 + DOWN * 0.35)

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), Write(frac), run_time=1.0)
    paced_play(scene, Create(wheel[0]), LaggedStart(*[FadeIn(d, scale=0.7) for d in wheel[1:]], lag_ratio=0.1), run_time=1.15)

    rows = VGroup()
    for rem_in, digit, rem_out in long_division_by_7():
        rows.add(equation(rf"{rem_in}\times10=7\times{digit}+{rem_out}", cfg.CYAN, 34))
    rows.arrange(DOWN, buff=0.13).shift(RIGHT * 3.15 + DOWN * 0.25)
    rows_box = SurroundingRectangle(rows, color=cfg.CYAN, buff=0.28, stroke_width=2)

    paced_play(scene, Create(rows_box), run_time=0.35)
    for index, row in enumerate(rows):
        paced_play(scene, Write(row), run_time=0.32)
        digit_mob = wheel[index + 1]
        scene.play(Indicate(digit_mob, color=cfg.WHITE, scale_factor=1.22), run_time=0.25)

    arrows = VGroup()
    points = [wheel[i].get_center() for i in range(1, 7)]
    for i in range(6):
        arrows.add(CurvedArrow(points[i], points[(i + 1) % 6], angle=-TAU / 5, color=cfg.PURPLE, stroke_width=3))
    paced_play(scene, LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.08), run_time=0.9)
    loop = label("six remainders, then the loop closes", cfg.GREEN, 31).to_edge(DOWN, buff=0.55)
    paced_play(scene, FadeIn(loop, shift=UP * 0.12), run_time=0.55)
    end_scene(scene, start)
