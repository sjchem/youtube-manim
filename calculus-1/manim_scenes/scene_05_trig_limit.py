"""Scene 05: the squeeze theorem proves a famous trigonometric limit."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    paced_play,
)
from utils.math_utils import sinc_ratio


class Scene05TrigLimit(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "05")
    add_cinematic_background(scene)

    question = eq(r"\lim_{x\to 0}\frac{\sin x}{x}=\ ?", cfg.WHITE, cfg.FONT["section"])
    question.set_color_by_tex(r"\lim", cfg.PURPLE)
    question.to_edge(UP, buff=0.42)
    paced_play(scene, Write(question), run_time=1.3)
    narration_wait(scene, 9.3)

    # -- Unit circle geometry: sin x, arc x, tan x --
    # Keep the construction and the later squeeze gauge near the visual
    # center so students can compare them without scanning across the frame.
    center = np.array([-2.25, -0.75, 0.0])
    radius = 2.1
    angle = ValueTracker(0.85)

    def point_at(a: float) -> np.ndarray:
        return center + radius * np.array([np.cos(a), np.sin(a), 0.0])

    circle = Circle(radius=radius, color=cfg.MUTED, stroke_width=2.5, stroke_opacity=0.7).move_to(center)
    axis_line = Line(center, center + RIGHT * (radius + 0.5), color=cfg.MUTED, stroke_width=2)
    o_dot = Dot(center, radius=0.05, color=cfg.WHITE)

    radius_line = always_redraw(lambda: Line(center, point_at(angle.get_value()), color=cfg.WHITE, stroke_width=4))
    sin_segment = always_redraw(
        lambda: Line(point_at(angle.get_value()), [point_at(angle.get_value())[0], center[1], 0], color=cfg.CYAN, stroke_width=7)
    )
    arc_segment = always_redraw(
        lambda: Arc(radius=radius, start_angle=0, angle=angle.get_value(), arc_center=center, color=cfg.GOLD, stroke_width=7)
    )
    def tan_top() -> np.ndarray:
        return center + np.array([radius, radius * np.tan(min(angle.get_value(), 1.45)), 0])

    tan_segment = always_redraw(
        lambda: Line(center + RIGHT * radius, tan_top(), color=cfg.ORANGE, stroke_width=7)
    )
    a_dot = Dot(center + RIGHT * radius, radius=0.05, color=cfg.MUTED)

    sin_tag = eq(r"\sin x", cfg.CYAN, cfg.FONT["body"])
    sin_tag.add_updater(lambda m: m.next_to(sin_segment, LEFT, buff=0.22).shift(DOWN * 0.3))
    arc_tag = eq("x", cfg.GOLD, cfg.FONT["small"])
    arc_tag.add_updater(lambda m: m.move_to(center + (radius + 0.42) * np.array([np.cos(angle.get_value() / 2), np.sin(angle.get_value() / 2), 0])))
    tan_tag = eq(r"\tan x", cfg.ORANGE, cfg.FONT["body"])
    tan_tag.add_updater(lambda m: m.next_to(tan_segment, RIGHT, buff=0.12).align_to(tan_segment, UP))

    paced_play(scene, Create(circle), Create(axis_line), FadeIn(o_dot), FadeIn(a_dot), run_time=2.2)
    scene.add(radius_line, sin_segment, arc_segment, tan_segment)
    paced_play(
        scene,
        LaggedStart(
            Create(radius_line),
            Create(arc_segment),
            Create(sin_segment),
            Create(tan_segment),
            lag_ratio=0.24,
        ),
        run_time=4.0,
    )
    paced_play(
        scene,
        LaggedStart(FadeIn(arc_tag), FadeIn(sin_tag), FadeIn(tan_tag), lag_ratio=0.25),
        run_time=1.4,
    )
    # A gentle change in angle keeps the construction alive while the three
    # lengths are narrated instead of freezing immediately after appearing.
    paced_play(scene, angle.animate.set_value(0.70), run_time=8.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 19.53)

    inequality = eq(r"\sin x<x<\tan x", cfg.WHITE, cfg.FONT["body"])
    inequality.set_color_by_tex(r"\sin", cfg.CYAN)
    inequality.set_color_by_tex(r"\tan", cfg.ORANGE)
    inequality.to_corner(UR, buff=0.5).shift(DOWN * 0.3)
    paced_play(scene, FadeIn(inequality, shift=UP * 0.15), run_time=1.0)
    narration_wait(scene, 20.92)

    squeeze = eq(r"\cos x<\frac{\sin x}{x}<1", cfg.GOLD, cfg.FONT["section"])
    squeeze.set_color_by_tex(r"\cos", cfg.CYAN)
    squeeze.move_to(inequality)
    paced_play(scene, ReplacementTransform(inequality, squeeze), run_time=1.2)
    narration_wait(scene, 19.75)

    # -- Squeeze gauge: cos x and sin x / x both climbing toward 1 --
    gauge_axis = NumberLine(x_range=[0.75, 1.05, 0.05], length=3.6, color=cfg.MUTED, rotation=90 * DEGREES)
    gauge_axis.move_to([2.65, -0.55, 0])
    # Keep the fixed upper-bound label away from the two live labels as all
    # three values converge at 1.
    gauge_top = eq("1", cfg.WHITE, cfg.FONT["body"]).next_to(gauge_axis.n2p(1.0), UL, buff=0.28)
    gauge_line = DashedLine(gauge_axis.n2p(1.0) + LEFT * 0.35, gauge_axis.n2p(1.0) + RIGHT * 0.05, color=cfg.WHITE, stroke_width=2.5)
    cos_dot = always_redraw(lambda: glow_dot(gauge_axis.n2p(np.cos(angle.get_value())), cfg.CYAN, 0.075))
    ratio_dot = always_redraw(lambda: glow_dot(gauge_axis.n2p(sinc_ratio(angle.get_value())), cfg.GOLD, 0.075))
    cos_label = eq(r"\cos x", cfg.CYAN, cfg.FONT["body"]).add_updater(lambda m: m.next_to(cos_dot, LEFT, buff=0.18))
    ratio_label = eq(r"\frac{\sin x}{x}", cfg.GOLD, cfg.FONT["body"]).add_updater(lambda m: m.next_to(ratio_dot, RIGHT, buff=0.18))

    paced_play(
        scene,
        FadeOut(VGroup(sin_tag, arc_tag, tan_tag)),
        Create(gauge_axis),
        FadeIn(gauge_top),
        Create(gauge_line),
        run_time=1.0,
    )
    scene.add(cos_dot, ratio_dot, cos_label, ratio_label)
    paced_play(scene, FadeIn(cos_dot), FadeIn(ratio_dot), FadeIn(cos_label), FadeIn(ratio_label), run_time=0.8)

    shrink_caption = bottom_caption("Let x shrink toward zero and watch the squeeze.", cfg.WHITE)
    paced_play(scene, FadeIn(shrink_caption), run_time=0.7)
    paced_play(scene, angle.animate.set_value(0.03), run_time=12.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 18.59)

    limit_reveal = eq(r"\lim_{x\to 0}\frac{\sin x}{x}=1", cfg.GREEN, cfg.FONT["hero"])
    limit_reveal.set_color_by_tex(r"\lim", cfg.PURPLE)
    limit_reveal.to_edge(UP, buff=0.4)
    paced_play(
        scene,
        FadeOut(VGroup(shrink_caption, squeeze)),
        ReplacementTransform(question, limit_reveal),
        Indicate(VGroup(cos_dot, ratio_dot), color=cfg.GREEN, scale_factor=1.5),
        run_time=1.4,
    )
    narration_wait(scene, 23.24)

    end_scene(scene, started, cfg.SCENE_DURATIONS["05"])
