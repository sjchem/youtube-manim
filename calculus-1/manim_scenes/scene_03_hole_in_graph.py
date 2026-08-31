"""Scene 03: a limit can exist exactly where the function does not."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axis_labels,
    calc_axes,
    end_scene,
    eq,
    equation_card,
    glow_dot,
    narration_wait,
    paced_play,
)
from utils.math_utils import removable_hole_simplified


class Scene03HoleInGraph(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "03")
    add_cinematic_background(scene)

    original = eq(r"f(x)=\frac{x^2-1}{x-1}", cfg.WHITE, cfg.FONT["section"]).to_edge(UP, buff=0.42)
    paced_play(scene, Write(original), run_time=1.2)
    narration_wait(scene, 12.98)

    undefined_card = equation_card(r"f(1)=\frac{0}{0}", cfg.RED, cfg.FONT["body"])
    undefined_card.to_corner(UR, buff=0.5)
    undefined_word = eq(r"\text{undefined}", cfg.RED, cfg.FONT["small"]).next_to(undefined_card, DOWN, buff=0.2)
    paced_play(scene, FadeIn(undefined_card, scale=1.08), FadeIn(undefined_word), run_time=0.9)
    narration_wait(scene, 18.17)

    factor_step = eq(
        r"f(x)=\frac{(x-1)(x+1)}{x-1}",
        cfg.WHITE,
        cfg.FONT["section"],
        substrings_to_isolate=("x-1",),
    )
    paced_play(scene, ReplacementTransform(original, factor_step), run_time=1.1)
    narration_wait(scene, 11.68)

    # Manim 0.20 returns one VGroup containing every isolated match.
    cancel_parts = factor_step.get_part_by_tex("x-1")
    assert cancel_parts is not None
    paced_play(scene, cancel_parts.animate.set_color(cfg.RED), run_time=0.8)
    narration_wait(scene, 3.89)

    simplified = eq(r"f(x)=x+1\ \ (x\neq 1)", cfg.GREEN, cfg.FONT["section"])
    paced_play(
        scene,
        FadeOut(VGroup(undefined_card, undefined_word)),
        ReplacementTransform(factor_step, simplified),
        run_time=1.1,
    )
    narration_wait(scene, 18.17)

    # -- Graph: a straight line with one honest hole --
    axes = calc_axes(x_range=(-1.5, 3.5, 1), y_range=(-1.5, 4.5, 1), x_length=9.6, y_length=5.5).move_to([0.1, -0.75, 0])
    axis_labels = calc_axis_labels(axes)
    line = axes.plot(removable_hole_simplified, x_range=[-1.3, 0.85], color=cfg.CYAN, stroke_width=6)
    line_2 = axes.plot(removable_hole_simplified, x_range=[1.15, 3.3], color=cfg.CYAN, stroke_width=6)
    hole = Circle(radius=0.1, color=cfg.RED, fill_color=cfg.BG, fill_opacity=1, stroke_width=4).move_to(axes.c2p(1, 2))
    paced_play(scene, FadeOut(simplified), Create(axes), FadeIn(axis_labels), run_time=1.0)
    paced_play(scene, Create(line), Create(line_2), run_time=1.2)
    paced_play(scene, Create(hole), run_time=0.6)
    narration_wait(scene, 6.49)

    approach_caption = bottom_caption("Walk toward the hole from both sides.", cfg.WHITE)
    paced_play(scene, FadeIn(approach_caption), run_time=0.7)

    left_dot = glow_dot(axes.c2p(0.3, removable_hole_simplified(0.3)), cfg.CYAN, 0.09)
    right_dot = glow_dot(axes.c2p(1.7, removable_hole_simplified(1.7)), cfg.ORANGE, 0.09)
    paced_play(scene, FadeIn(left_dot), FadeIn(right_dot), run_time=0.6)
    paced_play(
        scene,
        left_dot.animate.move_to(axes.c2p(0.94, removable_hole_simplified(0.94))),
        right_dot.animate.move_to(axes.c2p(1.06, removable_hole_simplified(1.06))),
        run_time=4.5,
        rate_func=rate_functions.ease_in_out_sine,
    )
    narration_wait(scene, 5.19)

    limit_readout = eq(r"\lim_{x\to 1}f(x)=2", cfg.GOLD, cfg.FONT["hero"])
    limit_readout.set_color_by_tex(r"\lim", cfg.PURPLE)
    limit_readout.to_edge(UP, buff=0.4)
    paced_play(
        scene,
        FadeOut(approach_caption),
        Write(limit_readout),
        Indicate(hole, color=cfg.GOLD, scale_factor=1.5),
        run_time=1.4,
    )
    narration_wait(scene, 12.98)

    message = bottom_caption("A limit can exist exactly where the function does not.", cfg.GOLD)
    paced_play(scene, FadeIn(message), run_time=0.8)
    narration_wait(scene, 20.77)

    end_scene(scene, started, cfg.SCENE_DURATIONS["03"])
