"""Scene 4: 7 as a prime outsider."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, end_scene, equation, label, number_dot_grid, paced_play, panel


class Scene04PrimeOutsider(MovingCameraScene):
    """Contrast 6's divisibility with 7's prime behavior."""

    def construct(self) -> None:
        play_scene_04(self)


def play_scene_04(scene: Scene) -> None:
    start = begin_scene(scene)

    heading = label("Then 7 steps outside the pattern", cfg.PURPLE, 38).to_edge(UP, buff=0.5)
    line = NumberLine(x_range=[1, 8, 1], length=9.5, include_numbers=True, color=cfg.GRAY).shift(UP * 1.75)
    marker6 = Dot(line.n2p(6), radius=0.13, color=cfg.GREEN)
    marker7 = Dot(line.n2p(7), radius=0.13, color=cfg.PURPLE)

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.2), Create(line), run_time=0.9)
    paced_play(scene, GrowFromCenter(marker6), run_time=0.35)
    paced_play(scene, TransformFromCopy(marker6, marker7), run_time=0.55)
    scene.play(marker7.animate.scale(1.6), rate_func=there_and_back, run_time=0.55)

    six_panel = panel(3.7, 2.25, cfg.GREEN, 0.16).shift(LEFT * 3.0 + DOWN * 0.55)
    seven_panel = panel(3.7, 2.25, cfg.PURPLE, 0.16).shift(RIGHT * 3.0 + DOWN * 0.55)
    six_dots = number_dot_grid(6, cols=3, color=cfg.GREEN, radius=0.09).move_to(six_panel).shift(UP * 0.18)
    seven_dots = number_dot_grid(7, cols=4, color=cfg.PURPLE, radius=0.09).move_to(seven_panel).shift(UP * 0.18)
    six_eq = equation(r"6=2\times3", cfg.GREEN, 46).next_to(six_panel, DOWN, buff=0.16)
    seven_eq = equation(r"7=1\times7", cfg.PURPLE, 46).next_to(seven_panel, DOWN, buff=0.16)

    divider = Line(six_panel.get_center() + UP * 0.72, six_panel.get_center() + DOWN * 0.72, color=cfg.CYAN, stroke_width=4)
    no_split = Line(seven_panel.get_left() + RIGHT * 0.5 + DOWN * 0.75, seven_panel.get_right() + LEFT * 0.5 + UP * 0.75, color=cfg.ORANGE, stroke_width=7)

    paced_play(scene, Create(six_panel), Create(seven_panel), FadeIn(six_dots), FadeIn(seven_dots), run_time=0.8)
    paced_play(scene, Create(divider), Write(six_eq), run_time=0.75)
    paced_play(scene, Create(no_split), Write(seven_eq), run_time=0.75)

    square_grid = VGroup()
    entries = [r"0^2+0^2=0", r"1^2+0^2=1", r"1^2+1^2=2", r"2^2+0^2=4", r"2^2+1^2=5", r"2^2+2^2=8"]
    for tex in entries:
        square_grid.add(equation(tex, cfg.WHITE, 34))
    square_grid.arrange_in_grid(rows=2, cols=3, buff=(0.38, 0.16)).to_edge(DOWN, buff=0.45)
    seven_miss = equation(r"7\neq a^2+b^2", cfg.ORANGE, 48).next_to(square_grid, UP, buff=0.22)

    paced_play(scene, FadeIn(seven_miss, shift=UP * 0.1), LaggedStart(*[Write(e) for e in square_grid], lag_ratio=0.06), run_time=1.2)
    scene.play(Indicate(seven_miss, color=cfg.ORANGE, scale_factor=1.04), run_time=0.65)
    end_scene(scene, start)
