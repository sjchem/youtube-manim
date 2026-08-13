"""Scene 13: pure sine tones combine into richer sound waves."""

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
    speaker_icon,
)
from utils.physics_models import combine_tones


class Scene13RealSound(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "13")
    add_cinematic_background(scene)
    tag = section_tag("13", "Let the wave move air")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    speaker = speaker_icon([-5.4, -0.2, 0], 1.15)
    axes = Axes(
        x_range=[0, 4 * PI, PI],
        y_range=[-1.4, 1.4, 1],
        x_length=8.8,
        y_length=3.9,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.3},
    ).move_to([2.0, -0.15, 0])
    pure_wave = axes.plot(np.sin, x_range=[0, 4 * PI], color=cfg.CYAN, stroke_width=7)
    pure_label = eq(r"y=\sin\theta", cfg.CYAN, cfg.FONT["section"]).move_to([2.0, 2.15, 0])
    paced_play(scene, FadeOut(tag), FadeIn(speaker), Create(axes), run_time=1.3)
    paced_play(scene, Create(pure_wave), Write(pure_label), run_time=4.5)

    vibration = ValueTracker(0.0)
    cone_travel = ValueTracker(0.14)
    diaphragm = always_redraw(
        lambda: Line(
            [-5.78 + cone_travel.get_value() * np.sin(vibration.get_value()), -0.82, 0],
            [-5.78 + cone_travel.get_value() * np.sin(vibration.get_value()), 0.42, 0],
            color=cfg.GOLD,
            stroke_width=10,
        )
    )
    rings = always_redraw(
        lambda: VGroup(*[
            Arc(
                radius=0.55 + 0.28 * i + 0.55 * cone_travel.get_value() * (1 + np.sin(vibration.get_value())),
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                arc_center=[-4.72, -0.2, 0],
                color=cfg.CYAN,
                stroke_width=3,
                stroke_opacity=0.65 / (i + 1),
            )
            for i in range(4)
        ])
    )
    scene.add(diaphragm, rings)
    pure_caption = bottom_caption("A perfect sine wave makes a pure tone.", cfg.WHITE)
    paced_play(scene, FadeIn(pure_caption), vibration.animate.set_value(4 * PI), run_time=5.0, rate_func=linear)
    pitch_caption = bottom_caption("More cycles each second → higher pitch", cfg.CYAN)
    paced_play(
        scene,
        ReplacementTransform(pure_caption, pitch_caption),
        vibration.animate.set_value(12 * PI),
        run_time=4.0,
        rate_func=linear,
    )
    loud_caption = bottom_caption("Larger pressure changes → louder sound", cfg.GOLD)
    paced_play(
        scene,
        ReplacementTransform(pitch_caption, loud_caption),
        cone_travel.animate.set_value(0.26),
        vibration.animate.set_value(18 * PI),
        run_time=3.0,
        rate_func=linear,
    )
    narration_wait(scene, 1.5)

    paced_play(scene, FadeOut(VGroup(speaker, axes, pure_wave, pure_label, diaphragm, rings, loud_caption)), run_time=0.9)

    # Three component tones and their sum.
    component_axes = VGroup()
    curves = VGroup()
    labels = VGroup()
    specs = (
        (1.0, 1.0, cfg.CYAN, r"\sin\theta"),
        (0.52, 2.0, cfg.GREEN, r"0.52\sin(2\theta)"),
        (0.28, 3.0, cfg.PURPLE, r"0.28\sin(3\theta)"),
    )
    y_positions = (2.15, 0.65, -0.85)
    for (amplitude, frequency, color, latex), y_pos in zip(specs, y_positions, strict=True):
        ax = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.25, 1.25, 1],
            x_length=9.7,
            y_length=1.15,
            tips=False,
            axis_config={"color": cfg.GRAY, "stroke_width": 1.6},
        ).move_to([1.0, y_pos, 0])
        curve = ax.plot(lambda x, a=amplitude, f=frequency: a * np.sin(f * x), x_range=[0, 4 * PI], color=color, stroke_width=4.5)
        label = eq(latex, color, cfg.FONT["small"]).next_to(ax, LEFT, buff=0.35)
        component_axes.add(ax)
        curves.add(curve)
        labels.add(label)
    paced_play(scene, LaggedStart(*[Create(ax) for ax in component_axes], lag_ratio=0.2), run_time=1.5)
    for curve, label in zip(curves, labels, strict=True):
        paced_play(scene, Create(curve), FadeIn(label), run_time=2.4)
        narration_wait(scene, 0.8)

    plus_signs = VGroup(
        outlined_text("+", cfg.FONT["section"], cfg.WHITE, BOLD).move_to([-5.6, 1.4, 0]),
        outlined_text("+", cfg.FONT["section"], cfg.WHITE, BOLD).move_to([-5.6, -0.1, 0]),
    )
    paced_play(scene, FadeIn(plus_signs), run_time=0.6)
    narration_wait(scene, 1.4)

    paced_play(scene, VGroup(component_axes, curves, labels, plus_signs).animate.scale(0.76).to_edge(UP, buff=0.72), run_time=1.1)
    sum_axes = Axes(
        x_range=[0, 4 * PI, PI],
        y_range=[-1.8, 1.8, 1],
        x_length=10.8,
        y_length=2.6,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.0},
    ).move_to([0.6, -2.3, 0])
    sum_curve = sum_axes.plot(
        lambda x: combine_tones(x, (1.0, 0.52, 0.28), (1.0, 2.0, 3.0)),
        x_range=[0, 4 * PI],
        color=cfg.GOLD,
        stroke_width=7,
    )
    equals = outlined_text("=", cfg.FONT["section"], cfg.GOLD, BOLD).next_to(sum_axes, LEFT, buff=0.4)
    rich = outlined_text("SUM → A NEW TIMBRE", cfg.FONT["body"], cfg.GOLD, BOLD).next_to(sum_axes, UP, buff=0.15)
    paced_play(scene, Create(sum_axes), FadeIn(equals), FadeIn(rich), run_time=1.2)
    paced_play(scene, Create(sum_curve), run_time=8.0, rate_func=linear)
    timbre_caption = bottom_caption("Change the component strengths → change the sound's character", cfg.WHITE)
    paced_play(scene, FadeIn(timbre_caption), run_time=0.7)
    narration_wait(scene, 1.3)

    paced_play(scene, FadeOut(VGroup(component_axes, curves, labels, plus_signs, sum_axes, sum_curve, equals, rich, timbre_caption)), run_time=0.9)
    cards = VGroup()
    for symbol, name, color in (("≋", "ocean motion", cfg.CYAN), ("♪", "sound", cfg.GOLD), ("↕", "vibration", cfg.GREEN), ("∿", "alternating current", cfg.PURPLE)):
        box = RoundedRectangle(width=3.1, height=2.0, corner_radius=0.18, color=color, fill_color=cfg.PANEL, fill_opacity=0.86)
        icon = outlined_text(symbol, cfg.FONT["hero"], color, BOLD)
        if name == "alternating current":
            text = VGroup(
                outlined_text("alternating", cfg.FONT["small"], cfg.WHITE, BOLD),
                outlined_text("current", cfg.FONT["small"], cfg.WHITE, BOLD),
            ).arrange(DOWN, buff=0.02)
        else:
            text = outlined_text(name, cfg.FONT["small"], cfg.WHITE, BOLD)
        content = VGroup(icon, text).arrange(DOWN, buff=0.12).move_to(box)
        cards.add(VGroup(box, content))
    cards.arrange(RIGHT, buff=0.3).move_to(ORIGIN)
    paced_play(scene, LaggedStart(*[FadeIn(card, shift=UP * 0.18) for card in cards], lag_ratio=0.22), run_time=1.8)
    accurate = bottom_caption("Not every wave is a sine wave—but sine waves are powerful building blocks.", cfg.WHITE)
    paced_play(scene, FadeIn(accurate), run_time=0.8)
    paced_play(scene, LaggedStart(*[Indicate(card, color=cfg.GOLD, scale_factor=1.02) for card in cards], lag_ratio=0.2), run_time=2.0)
    narration_wait(scene, 3.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["13"])
