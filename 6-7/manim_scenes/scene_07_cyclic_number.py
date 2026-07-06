"""Scene 7: the cyclic number 142857."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, digit_wheel, end_scene, equation, label, paced_play
from utils.math_utils import CYCLIC_DIGITS, cyclic_rotation


class Scene07CyclicNumber(MovingCameraScene):
    """Animate the rotated products of 142857."""

    def construct(self) -> None:
        play_scene_07(self)


def play_scene_07(scene: Scene) -> None:
    start = begin_scene(scene)

    heading = label("142857 behaves like a rotating crystal", cfg.GOLD, 38).to_edge(UP, buff=0.48)
    wheel = digit_wheel(CYCLIC_DIGITS, radius=2.1, color=cfg.GOLD).shift(LEFT * 3.05)
    center = equation(r"142857", cfg.WHITE, 52).move_to(wheel.get_center())
    rule = equation(r"142857\times k", cfg.CYAN, 54).shift(RIGHT * 3.05 + UP * 1.8)
    result = equation(r"=142857", cfg.WHITE, 58).next_to(rule, DOWN, buff=0.42)

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.18), run_time=0.55)
    paced_play(scene, Create(wheel[0]), LaggedStart(*[FadeIn(d, scale=0.7) for d in wheel[1:]], lag_ratio=0.08), FadeIn(center), run_time=1.15)
    paced_play(scene, Write(rule), Write(result), run_time=0.8)

    product_lines = VGroup()
    for k in range(1, 7):
        product_lines.add(equation(rf"\times {k}\quad {cyclic_rotation(k)}", cfg.WHITE if k == 1 else cfg.CYAN, 37))
    product_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12).shift(RIGHT * 3.15 + DOWN * 0.65)

    for k, line in enumerate(product_lines, start=1):
        new_result = equation(rf"={cyclic_rotation(k)}", cfg.GOLD, 58).move_to(result)
        scene.play(Transform(result, new_result), Rotate(wheel, angle=-TAU / 6, about_point=wheel.get_center()), run_time=0.45)
        paced_play(scene, FadeIn(line, shift=LEFT * 0.12), run_time=0.22)

    closure = equation(r"7\times142857=999999", cfg.GREEN, 50).to_edge(DOWN, buff=0.48)
    paced_play(scene, Write(closure), run_time=0.75)
    scene.play(Indicate(closure, color=cfg.GREEN, scale_factor=1.04), run_time=0.6)
    end_scene(scene, start)
