"""Scene 04: continuity is the moment a limit meets its function."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    end_scene,
    equation_card,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
)


def _mini_axes(center) -> Axes:
    return Axes(
        x_range=[-2.2, 2.2, 1],
        y_range=[-1.8, 2.2, 1],
        x_length=3.9,
        y_length=3.4,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.0},
    ).move_to(center)


def _panel_smooth(center) -> VGroup:
    axes = _mini_axes(center)
    curve = axes.plot(lambda x: 0.32 * x**2 - 0.2, x_range=[-2.1, 2.1], color=cfg.GREEN, stroke_width=5)
    dot = Dot(axes.c2p(0, -0.2), radius=0.09, color=cfg.GREEN)
    verdict = outlined_text("CONTINUOUS", cfg.FONT["tiny"], cfg.GREEN, BOLD).next_to(axes, DOWN, buff=0.22)
    return VGroup(axes, curve, dot, verdict)


def _panel_hole(center) -> VGroup:
    axes = _mini_axes(center)
    left = axes.plot(lambda x: 0.55 * x + 0.4, x_range=[-2.1, -0.15], color=cfg.ORANGE, stroke_width=5)
    right = axes.plot(lambda x: 0.55 * x + 0.4, x_range=[0.15, 2.1], color=cfg.ORANGE, stroke_width=5)
    hole = Circle(radius=0.09, color=cfg.ORANGE, fill_color=cfg.BG, fill_opacity=1, stroke_width=3.5).move_to(axes.c2p(0, 0.4))
    verdict = outlined_text("NOT CONTINUOUS", cfg.FONT["tiny"], cfg.ORANGE, BOLD).next_to(axes, DOWN, buff=0.22)
    return VGroup(axes, left, right, hole, verdict)


def _panel_jump(center) -> VGroup:
    axes = _mini_axes(center)
    left = axes.plot(lambda x: -0.35 * x - 1.0, x_range=[-2.1, 0], color=cfg.RED, stroke_width=5)
    right = axes.plot(lambda x: 0.35 * x + 1.0, x_range=[0, 2.1], color=cfg.RED, stroke_width=5)
    left_dot = Dot(axes.c2p(0, -1.0), radius=0.09, color=cfg.RED)
    right_hole = Circle(radius=0.09, color=cfg.RED, fill_color=cfg.BG, fill_opacity=1, stroke_width=3.5).move_to(axes.c2p(0, 1.0))
    right_dot = Dot(axes.c2p(0, 1.0), radius=0.09, color=cfg.RED)
    verdict = outlined_text("NOT CONTINUOUS", cfg.FONT["tiny"], cfg.RED, BOLD).next_to(axes, DOWN, buff=0.22)
    return VGroup(axes, left, right, left_dot, right_hole, right_dot, verdict)


class Scene04Continuity(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "04")
    add_cinematic_background(scene)

    definition_card = equation_card(
        r"f\ \text{continuous at } a \iff \lim_{x\to a}f(x)=f(a)",
        cfg.WHITE,
        cfg.FONT["section"],
    )
    definition = definition_card[2]
    definition.set_color_by_tex(r"\lim", cfg.PURPLE)
    definition_card[0].set_stroke(cfg.PURPLE, opacity=0.1)
    definition_card[1].set_stroke(cfg.PURPLE, opacity=0.7)
    definition_card.move_to([0, 3.05, 0])
    paced_play(
        scene,
        FadeIn(VGroup(definition_card[0], definition_card[1]), scale=1.03),
        Write(definition),
        run_time=1.6,
    )
    narration_wait(scene, 10.03)

    agree = bottom_caption("Three things must agree: left limit, right limit, value.", cfg.GOLD)
    paced_play(scene, FadeIn(agree), run_time=0.8)
    narration_wait(scene, 15.04)

    # Leave a full caption-height lane below the three verdicts.
    panel_1 = _panel_smooth([-4.9, -0.75, 0])
    panel_2 = _panel_hole([0.0, -0.75, 0])
    panel_3 = _panel_jump([4.9, -0.75, 0])

    caption_2 = bottom_caption("Watch three cases, side by side.", cfg.WHITE)
    paced_play(scene, ReplacementTransform(agree, caption_2), run_time=0.7)
    paced_play(scene, LaggedStart(FadeIn(panel_1, shift=UP * 0.2), FadeIn(panel_2, shift=UP * 0.2), FadeIn(panel_3, shift=UP * 0.2), lag_ratio=0.28), run_time=1.8)
    narration_wait(scene, 1.88)

    caption_smooth = bottom_caption("Smooth curve: limit matches value exactly.", cfg.GREEN)
    paced_play(scene, ReplacementTransform(caption_2, caption_smooth), Indicate(panel_1, color=cfg.GREEN, scale_factor=1.06), run_time=0.9)
    narration_wait(scene, 11.91)

    caption_hole = bottom_caption("A hole: the limit exists, but the value is missing.", cfg.ORANGE)
    paced_play(scene, ReplacementTransform(caption_smooth, caption_hole), Indicate(panel_2, color=cfg.ORANGE, scale_factor=1.06), run_time=0.9)
    narration_wait(scene, 17.55)

    caption_jump = bottom_caption("A jump: left and right approach different heights.", cfg.RED)
    paced_play(scene, ReplacementTransform(caption_hole, caption_jump), Indicate(panel_3, color=cfg.RED, scale_factor=1.06), run_time=0.9)
    narration_wait(scene, 26.33)

    message = bottom_caption("Continuity becomes something your eyes can simply check.", cfg.WHITE)
    paced_play(scene, ReplacementTransform(caption_jump, message), run_time=0.8)
    narration_wait(scene, 20.06)

    end_scene(scene, started, cfg.SCENE_DURATIONS["04"])
