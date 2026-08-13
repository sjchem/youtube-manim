"""Scene 01: familiar repetition leads backward to trigonometry."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    coordinate_axes,
    end_scene,
    ferris_wheel,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    quarter_turn_labels,
    speaker_icon,
)
from utils.math_utils import point_on_circle


class Scene01Hook(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "01")
    add_cinematic_background(scene)

    # Three familiar repeating systems establish the course's central motif.
    panel_centers = (np.array([-5.0, 0.25, 0]), np.array([0.0, 0.25, 0]), np.array([5.0, 0.25, 0]))
    panels = VGroup(*[
        RoundedRectangle(
            width=4.25,
            height=4.45,
            corner_radius=0.2,
            color=color,
            fill_color=cfg.PANEL,
            fill_opacity=0.72,
            stroke_opacity=0.55,
        ).move_to(center)
        for center, color in zip(panel_centers, (cfg.RED, cfg.GOLD, cfg.CYAN), strict=True)
    ])
    labels = VGroup(
        outlined_text("HEARTBEAT", cfg.FONT["body"], cfg.RED, BOLD),
        outlined_text("PENDULUM", cfg.FONT["body"], cfg.GOLD, BOLD),
        outlined_text("SOUND", cfg.FONT["body"], cfg.CYAN, BOLD),
    )
    for label, panel in zip(labels, panels, strict=True):
        label.next_to(panel.get_top(), DOWN, buff=0.35)
    paced_play(scene, LaggedStart(*[FadeIn(panel, shift=UP * 0.12) for panel in panels], lag_ratio=0.18), FadeIn(labels), run_time=1.2)

    ecg_points = [
        [-6.7, 0.0, 0], [-6.25, 0.0, 0], [-6.05, 0.18, 0], [-5.88, -0.16, 0],
        [-5.66, 1.25, 0], [-5.42, -0.65, 0], [-5.15, 0.0, 0], [-4.65, 0.0, 0],
        [-4.43, 0.18, 0], [-4.26, -0.16, 0], [-4.04, 1.25, 0], [-3.80, -0.65, 0],
        [-3.52, 0.0, 0], [-3.25, 0.0, 0],
    ]
    ecg = VMobject(color=cfg.RED, stroke_width=7).set_points_as_corners(ecg_points)
    heart_progress = ValueTracker(0.0)
    heart_dot = always_redraw(
        lambda: glow_dot(ecg.point_from_proportion(heart_progress.get_value()), cfg.RED, 0.08)
    )

    pendulum_phase = ValueTracker(0.0)
    pivot = np.array([0.0, 1.3, 0.0])
    pendulum_end = lambda: pivot + 2.15 * np.array(
        [np.sin(0.52 * np.sin(pendulum_phase.get_value())), -np.cos(0.52 * np.sin(pendulum_phase.get_value())), 0]
    )
    rod = always_redraw(lambda: Line(pivot, pendulum_end(), color=cfg.WHITE, stroke_width=6))
    bob = always_redraw(lambda: glow_dot(pendulum_end(), cfg.GOLD, 0.14))
    pivot_dot = glow_dot(pivot, cfg.WHITE, 0.07)

    speaker = speaker_icon([3.85, -0.15, 0], 0.62)
    sound_axes = Axes(
        x_range=[0, TAU, PI],
        y_range=[-1.2, 1.2, 1],
        x_length=2.55,
        y_length=2.0,
        tips=False,
        axis_config={"color": cfg.GRAY, "stroke_width": 1.8},
    ).move_to([5.55, -0.05, 0])
    sound_phase = ValueTracker(0.0)
    sound_wave = always_redraw(
        lambda: sound_axes.plot(
            lambda x: np.sin(x - sound_phase.get_value()),
            x_range=[0, TAU],
            color=cfg.CYAN,
            stroke_width=6,
        )
    )
    paced_play(
        scene,
        Create(ecg),
        FadeIn(heart_dot),
        FadeIn(rod),
        FadeIn(bob),
        FadeIn(pivot_dot),
        FadeIn(speaker),
        Create(sound_axes),
        FadeIn(sound_wave),
        run_time=2.2,
    )
    paced_play(
        scene,
        heart_progress.animate.set_value(1.0),
        pendulum_phase.animate.set_value(4 * TAU),
        sound_phase.animate.set_value(4 * TAU),
        run_time=7.7,
        rate_func=linear,
    )

    repeat_caption = bottom_caption("A heartbeat, a pendulum, and sound all repeat.", cfg.WHITE)
    paced_play(scene, FadeIn(repeat_caption), run_time=0.7)
    narration_wait(scene, 1.0)

    paced_play(
        scene,
        FadeOut(VGroup(panels, labels, ecg, heart_dot, rod, bob, pivot_dot, speaker, sound_axes, sound_wave, repeat_caption)),
        run_time=0.9,
    )

    wave_axes = Axes(
        x_range=[0, 2 * TAU, PI],
        y_range=[-1.4, 1.4, 1],
        x_length=11.8,
        y_length=4.8,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.3},
    ).move_to(DOWN * 0.2)
    wave = wave_axes.plot(np.sin, x_range=[0, 2 * TAU], color=cfg.CYAN, stroke_width=7)
    wave_title = outlined_text("REPETITION, DRAWN THROUGH TIME", cfg.FONT["body"], cfg.GOLD, BOLD).to_edge(UP, buff=0.48)
    paced_play(scene, Create(wave_axes), FadeIn(wave_title), run_time=1.0)
    paced_play(scene, Create(wave), run_time=2.0, rate_func=linear)
    wave_caption = bottom_caption("Graph the repetition, and the same shape appears: a wave.", cfg.WHITE)
    paced_play(scene, FadeIn(wave_caption), run_time=0.7)
    narration_wait(scene, 1.0)

    paced_play(scene, VGroup(wave_axes, wave).animate.scale(0.55).to_edge(RIGHT, buff=0.55), FadeOut(wave_title), FadeOut(wave_caption), run_time=1.0)
    reverse_circle = Circle(radius=1.65, color=cfg.CYAN, stroke_width=6).move_to([-3.6, 0.15, 0])
    reverse_point = reverse_circle.point_at_angle(PI / 4)
    reverse_triangle = VGroup(
        Line(reverse_circle.get_center(), [reverse_point[0], reverse_circle.get_center()[1], 0], color=cfg.GREEN, stroke_width=7),
        Line([reverse_point[0], reverse_circle.get_center()[1], 0], reverse_point, color=cfg.CYAN, stroke_width=7),
        Line(reverse_circle.get_center(), reverse_point, color=cfg.WHITE, stroke_width=7),
    )
    backward_arrow = Arrow(RIGHT * 1.0, LEFT * 1.0, color=cfg.GOLD, stroke_width=6).move_to([-0.35, 0.15, 0])
    backward_text = outlined_text("FOLLOW THE WAVE BACKWARD", cfg.FONT["body"], cfg.GOLD, BOLD).to_edge(UP, buff=0.48)
    turn_caption = bottom_caption("A wave. A circle. A triangle. It begins with a turn.", cfg.WHITE)
    paced_play(
        scene,
        GrowArrow(backward_arrow),
        Create(reverse_circle),
        Create(reverse_triangle),
        FadeIn(backward_text),
        FadeIn(turn_caption),
        run_time=1.5,
    )
    narration_wait(scene, 1.0)
    paced_play(
        scene,
        FadeOut(VGroup(wave_axes, wave, reverse_circle, reverse_triangle, backward_arrow, backward_text, turn_caption)),
        run_time=0.8,
    )

    # Reserved blank slot for the channel owner's custom welcome animation.
    # The living background remains visible and the original three-second
    # authored duration is preserved, so narration timing does not change.
    narration_wait(scene, 3.0)

    circle_title = outlined_text("A CIRCLE", 56, cfg.CYAN, BOLD)
    wave_words = VGroup(
        *[outlined_text(word, 56, cfg.GOLD, BOLD) for word in ("CAN", "DRAW", "A", "WAVE")]
    ).arrange(RIGHT, buff=0.32)
    cold_open = VGroup(circle_title, wave_words).arrange(DOWN, buff=0.16)
    paced_play(scene, FadeIn(circle_title, shift=DOWN * 0.12), run_time=0.8)
    paced_play(
        scene,
        LaggedStart(
            *[FadeIn(word, shift=UP * 0.1, scale=0.96) for word in wave_words],
            lag_ratio=0.28,
        ),
        run_time=1.15,
    )
    narration_wait(scene, 1.2)
    paced_play(scene, FadeOut(cold_open, shift=UP * 0.2), run_time=0.7)

    center = np.array([-4.55, 0.35, 0.0])
    radius = 2.05
    wheel = ferris_wheel(center, radius=radius, spokes=12)
    axes = coordinate_axes(x_length=6.5, y_length=3.7).move_to([3.05, 0.35, 0])
    labels = quarter_turn_labels(axes)
    theta = ValueTracker(0.0)

    cabin = always_redraw(lambda: glow_dot(point_on_circle(theta.get_value(), radius, center), cfg.GOLD, 0.1))
    radius_line = always_redraw(
        lambda: Line(center, point_on_circle(theta.get_value(), radius, center), color=cfg.WHITE, stroke_width=5)
    )
    graph_dot = always_redraw(lambda: glow_dot(axes.c2p(theta.get_value(), np.sin(theta.get_value())), cfg.GOLD, 0.08))
    projector = always_redraw(
        lambda: DashedLine(
            point_on_circle(theta.get_value(), radius, center),
            axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=cfg.CYAN,
            stroke_width=2.4,
            dash_length=0.12,
            stroke_opacity=0.65,
        )
    )
    trace = always_redraw(
        lambda: axes.plot(
            np.sin,
            x_range=[0, max(theta.get_value(), 0.001)],
            color=cfg.CYAN,
            stroke_width=6,
        )
    )

    paced_play(scene, LaggedStart(Create(wheel), Create(axes), FadeIn(labels), lag_ratio=0.22), run_time=2.2)
    scene.add(radius_line, cabin, trace, projector, graph_dot)
    caption = bottom_caption("Watch only the cabin's height", cfg.WHITE)
    paced_play(scene, FadeIn(caption, shift=UP * 0.1), run_time=0.6)
    paced_play(scene, theta.animate.set_value(TAU), run_time=9.0, rate_func=linear)
    narration_wait(scene, 1.2)

    question = outlined_text("How did a turn become a wave?", cfg.FONT["section"], cfg.GOLD, BOLD)
    question.to_edge(UP, buff=0.32)
    paced_play(scene, ReplacementTransform(caption, question), run_time=0.8)
    paced_play(scene, Indicate(trace, color=cfg.WHITE, scale_factor=1.02), Indicate(wheel[2], color=cfg.GOLD), run_time=1.5)
    narration_wait(scene, 2.0)

    promise = outlined_text("No memorizing. We will build it.", cfg.FONT["body"], cfg.CYAN, BOLD)
    promise.to_edge(DOWN, buff=0.3)
    paced_play(scene, FadeIn(promise, shift=UP * 0.12), run_time=0.7)
    narration_wait(scene, 2.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["01"])
