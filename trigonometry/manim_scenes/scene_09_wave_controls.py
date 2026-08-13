"""Scene 09: amplitude, frequency, phase, and vertical shift."""

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
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)


class Scene09WaveControls(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "09")
    add_cinematic_background(scene)
    tag = section_tag("09", "Control the moving wave")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    axes = Axes(
        x_range=[-TAU, TAU, PI / 2],
        y_range=[-3.1, 3.1, 1],
        x_length=12.2,
        y_length=5.1,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.4},
    ).move_to(DOWN * 0.45)
    amplitude = ValueTracker(1.0)
    frequency = ValueTracker(1.0)
    phase = ValueTracker(0.0)
    shift = ValueTracker(0.0)
    wave = always_redraw(
        lambda: axes.plot(
            lambda x: amplitude.get_value() * np.sin(frequency.get_value() * x + phase.get_value()) + shift.get_value(),
            x_range=[-TAU, TAU],
            color=cfg.CYAN,
            stroke_width=7,
        )
    )
    formula = MathTex(
        "y=", "A", r"\sin", "(", "B", r"\theta", "+", "C", ")", "+", "D",
        font_size=cfg.FONT["section"],
        color=cfg.WHITE,
    ).to_edge(UP, buff=0.5)
    formula[1].set_color(cfg.GOLD)
    formula[2].set_color(cfg.CYAN)
    formula[4].set_color(cfg.ORANGE)
    formula[5].set_color(cfg.WHITE)
    formula[7].set_color(cfg.PURPLE)
    formula[10].set_color(cfg.GREEN)
    formula.set_stroke(cfg.BG, width=3, background=True)
    paced_play(scene, FadeOut(tag), Create(axes), Write(formula), run_time=1.6)
    scene.add(wave)

    control_name = outlined_text("A  ·  AMPLITUDE", cfg.FONT["body"], cfg.GOLD, BOLD).move_to([0, 3.0, 0])
    explanation = outlined_text("distance from the middle", cfg.FONT["small"], cfg.WHITE).next_to(control_name, DOWN, buff=0.12)
    paced_play(scene, Indicate(formula[1], color=cfg.WHITE), FadeIn(control_name), FadeIn(explanation), run_time=1.0)
    paced_play(scene, amplitude.animate.set_value(2.4), run_time=6.0, rate_func=smooth)
    paced_play(scene, amplitude.animate.set_value(0.55), run_time=5.0, rate_func=smooth)
    paced_play(scene, amplitude.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
    narration_wait(scene, 1.2)

    next_name = outlined_text("B  ·  FREQUENCY CONTROL", cfg.FONT["body"], cfg.ORANGE, BOLD).move_to(control_name)
    next_explanation = outlined_text("more cycles in the same distance", cfg.FONT["small"], cfg.WHITE).move_to(explanation)
    paced_play(scene, ReplacementTransform(control_name, next_name), ReplacementTransform(explanation, next_explanation), Indicate(formula[4], color=cfg.WHITE), run_time=1.0)
    paced_play(scene, frequency.animate.set_value(2.5), run_time=7.0, rate_func=smooth)
    paced_play(scene, frequency.animate.set_value(0.5), run_time=6.0, rate_func=smooth)
    paced_play(scene, frequency.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
    period = eq(r"\text{period}=\frac{2\pi}{|B|}", cfg.GOLD, cfg.FONT["body"]).move_to([4.65, -2.15, 0])
    period.set_stroke(cfg.BG, width=4, opacity=0.95, background=True)
    paced_play(scene, FadeIn(period), run_time=0.7)
    narration_wait(scene, 1.2)

    phase_name = outlined_text("C  ·  PHASE", cfg.FONT["body"], cfg.PURPLE, BOLD).move_to(next_name)
    phase_explanation = outlined_text("where the cycle begins", cfg.FONT["small"], cfg.WHITE).move_to(next_explanation)
    paced_play(scene, FadeOut(period), ReplacementTransform(next_name, phase_name), ReplacementTransform(next_explanation, phase_explanation), Indicate(formula[7], color=cfg.WHITE), run_time=1.0)
    paced_play(scene, phase.animate.set_value(PI), run_time=7.0, rate_func=smooth)
    paced_play(scene, phase.animate.set_value(-PI / 2), run_time=6.0, rate_func=smooth)
    paced_play(scene, phase.animate.set_value(0), run_time=3.0, rate_func=smooth)
    narration_wait(scene, 1.0)

    shift_name = outlined_text("D  ·  VERTICAL SHIFT", cfg.FONT["body"], cfg.GREEN, BOLD).move_to(phase_name)
    shift_explanation = outlined_text("move the middle line", cfg.FONT["small"], cfg.WHITE).move_to(phase_explanation)
    paced_play(scene, ReplacementTransform(phase_name, shift_name), ReplacementTransform(phase_explanation, shift_explanation), Indicate(formula[10], color=cfg.WHITE), run_time=1.0)
    paced_play(scene, shift.animate.set_value(1.55), run_time=6.0, rate_func=smooth)
    paced_play(scene, shift.animate.set_value(-1.2), run_time=6.0, rate_func=smooth)
    paced_play(scene, shift.animate.set_value(0), run_time=3.0, rate_func=smooth)

    paced_play(scene, FadeOut(VGroup(shift_name, shift_explanation)), run_time=0.6)
    cards = VGroup(
        outlined_text("A  height", cfg.FONT["body"], cfg.GOLD, BOLD),
        outlined_text("B  cycles", cfg.FONT["body"], cfg.ORANGE, BOLD),
        outlined_text("C  start", cfg.FONT["body"], cfg.PURPLE, BOLD),
        outlined_text("D  middle", cfg.FONT["body"], cfg.GREEN, BOLD),
    ).arrange(RIGHT, buff=0.65).move_to([0, 2.55, 0])
    paced_play(scene, LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in cards], lag_ratio=0.2), run_time=1.4)
    paced_play(
        scene,
        amplitude.animate.set_value(1.65),
        frequency.animate.set_value(1.5),
        phase.animate.set_value(PI / 3),
        shift.animate.set_value(0.5),
        run_time=10.0,
        rate_func=smooth,
    )
    takeaway = bottom_caption("Radius. Rotation speed. Starting angle. Axle height.", cfg.WHITE)
    paced_play(scene, FadeIn(takeaway), run_time=0.8)
    narration_wait(scene, 2.5)
    end_scene(scene, started, cfg.SCENE_DURATIONS["09"])
