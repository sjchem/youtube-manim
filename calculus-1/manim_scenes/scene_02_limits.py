"""Scene 02: limits, visualized before they are ever formalized."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    dashed_ring,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    paced_play,
)
from utils.math_utils import square


def _guides(axes: Axes, x: float, color: str) -> VGroup:
    point = axes.c2p(x, square(x))
    foot_x = axes.c2p(x, 0)
    foot_y = axes.c2p(0, square(x))
    return VGroup(
        DashedLine(point, foot_x, color=color, stroke_width=2.5, dash_length=0.1, stroke_opacity=0.75),
        DashedLine(point, foot_y, color=color, stroke_width=2.5, dash_length=0.1, stroke_opacity=0.75),
    )


def _value_readout(x: float, color: str, center) -> VGroup:
    """Two-line value panel that remains readable above the caption lane."""
    x_line = eq(rf"x={x:.3f}", color, cfg.FONT["body"])
    fx_line = eq(rf"f(x)={square(x):.3f}", color, cfg.FONT["body"])
    values = VGroup(x_line, fx_line).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    panel = RoundedRectangle(
        width=3.2,
        height=1.5,
        corner_radius=0.16,
        stroke_color=color,
        stroke_width=2.5,
        stroke_opacity=0.65,
        fill_color=cfg.PANEL,
        fill_opacity=0.9,
    )
    return VGroup(panel, values).move_to(center)


class Scene02Limits(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "02")
    add_cinematic_background(scene)

    axes = calc_axes(x_range=(-0.5, 3.5, 1), y_range=(-0.5, 9.5, 2), x_length=9.6, y_length=6.0).move_to([0.1, -0.35, 0])
    axis_label_size = cfg.FONT["section"] + 4
    x_axis_label = eq("x", cfg.WHITE, axis_label_size).next_to(axes.x_axis.get_right(), UP, buff=0.14)
    y_axis_label = eq("f(x)", cfg.WHITE, axis_label_size).next_to(axes.y_axis.get_top(), RIGHT, buff=0.14)
    axis_labels = VGroup(x_axis_label, y_axis_label)
    curve = axes.plot(square, x_range=[-0.4, 3.15], color=cfg.WHITE, stroke_width=6)
    f_label = eq("f(x)=x^2", cfg.WHITE, cfg.FONT["section"]).to_edge(UP, buff=0.42)
    paced_play(scene, Create(axes), FadeIn(axis_labels), Write(f_label), run_time=1.3)
    paced_play(scene, Create(curve), run_time=1.4)
    narration_wait(scene, 5.0)

    question = bottom_caption("What happens as x approaches 2?", cfg.GOLD)
    paced_play(scene, FadeIn(question), run_time=0.7)
    narration_wait(scene, 7.51)

    target_ring = dashed_ring(axes.c2p(2, 4), 0.14, cfg.GOLD, num_dashes=14)
    paced_play(scene, Create(target_ring), run_time=0.8)
    narration_wait(scene, 6.25)

    left_values = (1.0, 1.5, 1.9, 1.99, 1.999)
    right_values = (3.0, 2.5, 2.1, 2.01)
    left_readout_center = [-6.15, -1.1, 0]
    right_readout_center = [6.15, -1.1, 0]

    left_dot = glow_dot(axes.c2p(left_values[0], square(left_values[0])), cfg.CYAN, 0.09)
    left_readout = _value_readout(left_values[0], cfg.CYAN, left_readout_center)
    left_guides = _guides(axes, left_values[0], cfg.CYAN)
    paced_play(scene, FadeIn(left_dot), FadeIn(left_readout), Create(left_guides), run_time=0.85)
    narration_wait(scene, 3.75)

    for x in left_values[1:]:
        new_dot = glow_dot(axes.c2p(x, square(x)), cfg.CYAN, 0.09)
        new_readout = _value_readout(x, cfg.CYAN, left_readout_center)
        new_guides = _guides(axes, x, cfg.CYAN)
        paced_play(
            scene,
            Transform(left_dot, new_dot),
            ReplacementTransform(left_readout, new_readout),
            Transform(left_guides, new_guides),
            run_time=1.0,
        )
        left_readout = new_readout
        narration_wait(scene, 5.0)

    right_dot = glow_dot(axes.c2p(right_values[0], square(right_values[0])), cfg.ORANGE, 0.09)
    right_readout = _value_readout(right_values[0], cfg.ORANGE, right_readout_center)
    right_guides = _guides(axes, right_values[0], cfg.ORANGE)
    paced_play(scene, FadeIn(right_dot), FadeIn(right_readout), Create(right_guides), run_time=0.85)
    narration_wait(scene, 3.75)

    for x in right_values[1:]:
        new_dot = glow_dot(axes.c2p(x, square(x)), cfg.ORANGE, 0.09)
        new_readout = _value_readout(x, cfg.ORANGE, right_readout_center)
        new_guides = _guides(axes, x, cfg.ORANGE)
        paced_play(
            scene,
            Transform(right_dot, new_dot),
            ReplacementTransform(right_readout, new_readout),
            Transform(right_guides, new_guides),
            run_time=1.0,
        )
        right_readout = new_readout
        narration_wait(scene, 5.63)

    both_caption = bottom_caption("From both sides, the output heads toward 4.", cfg.WHITE)
    paced_play(scene, ReplacementTransform(question, both_caption), run_time=0.7)
    narration_wait(scene, 5.0)

    limit_statement = eq(r"\lim_{x\to 2}x^2=4", cfg.GOLD, cfg.FONT["hero"])
    limit_statement.set_color_by_tex(r"\lim", cfg.PURPLE)
    limit_statement.to_edge(UP, buff=0.4)
    paced_play(
        scene,
        FadeOut(VGroup(left_guides, right_guides, left_readout, right_readout)),
        ReplacementTransform(f_label, limit_statement),
        Indicate(target_ring, color=cfg.GOLD, scale_factor=1.4),
        run_time=1.3,
    )
    narration_wait(scene, 7.51)

    message = bottom_caption("A limit is not about reaching. It's about heading toward.", cfg.GOLD)
    paced_play(scene, ReplacementTransform(both_caption, message), run_time=0.75)
    narration_wait(scene, 21.5)

    end_scene(scene, started, cfg.SCENE_DURATIONS["02"])
