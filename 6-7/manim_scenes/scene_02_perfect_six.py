"""Scene 2: 6 as the first perfect number."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, end_scene, equation, label, number_dot_grid, paced_play, panel


class Scene02PerfectSix(MovingCameraScene):
    """Show divisor harmony for 6."""

    def construct(self) -> None:
        play_scene_02(self)


def play_scene_02(scene: Scene) -> None:
    start = begin_scene(scene)

    heading = label("6 balances with its own pieces", cfg.GREEN, 38).to_edge(UP, buff=0.5)
    six_dots = number_dot_grid(6, cols=3, color=cfg.WHITE, radius=0.11).scale(1.25).shift(UP * 1.25)
    six_box = panel(2.1, 1.6, cfg.GREEN, 0.18).move_to(six_dots)
    six_label = equation("6", cfg.WHITE, 72).next_to(six_box, UP, buff=0.18)
    main_group = VGroup(six_box, six_dots, six_label)

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.2), run_time=0.6)
    paced_play(scene, Create(six_box), LaggedStart(*[GrowFromCenter(dot) for dot in six_dots], lag_ratio=0.08), Write(six_label), run_time=1.1)

    pieces = VGroup()
    for count, text, x in [(1, "1", -3.3), (2, "2", 0.0), (3, "3", 3.3)]:
        dots = number_dot_grid(count, cols=count, color=cfg.CYAN, radius=0.095)
        box = panel(1.55, 1.15, cfg.CYAN, 0.16).move_to([x, -1.35, 0])
        dots.move_to(box)
        tag = equation(text, cfg.CYAN, 42).next_to(box, DOWN, buff=0.12)
        pieces.add(VGroup(box, dots, tag))

    arrows = VGroup(*[Arrow(piece.get_top(), six_box.get_bottom(), buff=0.18, color=cfg.CYAN, stroke_width=4) for piece in pieces])
    paced_play(scene, LaggedStart(*[FadeIn(piece, shift=UP * 0.25) for piece in pieces], lag_ratio=0.18), run_time=1.0)
    paced_play(scene, Create(arrows), run_time=0.75)

    sum_eq = equation(r"1+2+3=6", cfg.WHITE, 56).to_edge(DOWN, buff=0.32)
    paced_play(scene, TransformFromCopy(VGroup(*[piece[-1] for piece in pieces]), sum_eq), run_time=1.0)
    scene.play(Indicate(sum_eq, color=cfg.GREEN, scale_factor=1.05), run_time=0.7)

    product_eq = equation(r"1\times2\times3=6", cfg.GOLD, 44).next_to(sum_eq, UP, buff=0.08)
    paced_play(scene, FadeIn(product_eq, shift=UP * 0.15), main_group.animate.shift(UP * 0.08), run_time=0.75)
    end_scene(scene, start)
