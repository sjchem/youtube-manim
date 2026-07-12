"""Scene 07 - joint, marginal, and independence."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    equation_box,
    joint_probability_grid,
    label_pill,
    narration_wait,
    paced_play,
    scene_title,
)


class Scene07BayesTheorem(Scene):
    """Show joint tables, marginals, and the independence test."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "07")
    scene.add(cinematic_background())

    title = scene_title("Joint tables show together; marginals zoom out").to_edge(UP, buff=0.34)
    paced_play(scene, FadeIn(title), run_time=0.8)

    values = [[0.18, 0.07], [0.12, 0.63]]
    grid = joint_probability_grid(
        row_labels=["clicks", "no click"],
        col_labels=["buys", "no buy"],
        values=values,
        cell_size=1.12,
    ).move_to(LEFT * 3.55 + UP * 0.12)

    joint_eq = equation_box(r"P(A,B)", cfg.GOLD, font_size=38).move_to(RIGHT * 2.35 + UP * 1.35)
    joint_label = Text("one cell: click and buy", font_size=20, color=cfg.GOLD, weight=BOLD)
    joint_label.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    joint_label.next_to(joint_eq, DOWN, buff=0.2)

    paced_play(scene, FadeIn(grid), run_time=1.0)
    paced_play(scene, Indicate(grid[0][0], color=cfg.WHITE, scale_factor=1.08), FadeIn(joint_eq), FadeIn(joint_label), run_time=1.0)
    narration_wait(scene, 0.45)

    row_cells = VGroup(grid[0][0], grid[0][1])
    marginal_eq = equation_box(r"P(A) = \sum_b P(A,B=b)", cfg.CYAN, font_size=32)
    marginal_eq.move_to(RIGHT * 2.55 + UP * 0.02)
    sum_arrow = Arrow(row_cells.get_right() + RIGHT * 0.12, marginal_eq.get_left() + LEFT * 0.12, color=cfg.CYAN, buff=0.08, stroke_width=3)
    sum_tag = label_pill("sum row", cfg.CYAN, font_size=18).scale(0.84).next_to(sum_arrow, UP, buff=0.08)

    paced_play(scene, FadeOut(joint_label), run_time=0.35)
    paced_play(scene, Indicate(row_cells, color=cfg.CYAN, scale_factor=1.04), run_time=0.65)
    paced_play(scene, Create(sum_arrow), FadeIn(sum_tag), FadeIn(marginal_eq), run_time=0.95)
    narration_wait(scene, 0.5)

    independent = equation_box(r"\text{independent: } P(A,B)=P(A)P(B)", cfg.GREEN, font_size=29)
    dependent = equation_box(r"\text{ML features usually: } P(A,B)\neq P(A)P(B)", cfg.ORANGE, font_size=29)
    relation = VGroup(independent, dependent).arrange(DOWN, buff=0.24).to_edge(DOWN, buff=0.34)

    paced_play(scene, FadeIn(independent, shift=UP * 0.1), run_time=0.8)
    paced_play(scene, FadeIn(dependent, shift=UP * 0.1), run_time=0.8)
    narration_wait(scene, 1.0)

    end_scene(scene, scene_start)
