"""Scene 08: the unit circle plots sine and cosine in real time."""

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
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    quarter_turn_labels,
    section_tag,
)
from utils.math_utils import point_on_circle


class Scene08Unrolling(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "08")
    add_cinematic_background(scene)
    tag = section_tag("08", "Record the circle's height")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    center = np.array([-4.65, 0.1, 0.0])
    radius = 1.95
    circle = Circle(radius=radius, color=cfg.WHITE, stroke_width=5).move_to(center)
    cross = VGroup(
        Line(center + LEFT * 2.25, center + RIGHT * 2.25, color=cfg.GRAY, stroke_width=2),
        Line(center + DOWN * 2.25, center + UP * 2.25, color=cfg.GRAY, stroke_width=2),
    )
    axes = coordinate_axes(x_length=7.1, y_length=3.9).move_to([3.1, 0.1, 0])
    labels = quarter_turn_labels(axes)
    theta = ValueTracker(0.0)

    circle_point = always_redraw(lambda: glow_dot(point_on_circle(theta.get_value(), radius, center), cfg.GOLD, 0.1))
    radius_line = always_redraw(lambda: Line(center, point_on_circle(theta.get_value(), radius, center), color=cfg.WHITE, stroke_width=6))
    vertical_height = always_redraw(
        lambda: Line(
            [point_on_circle(theta.get_value(), radius, center)[0], center[1], 0],
            point_on_circle(theta.get_value(), radius, center),
            color=cfg.CYAN,
            stroke_width=8,
        )
    )
    graph_point = always_redraw(lambda: glow_dot(axes.c2p(theta.get_value(), np.sin(theta.get_value())), cfg.GOLD, 0.075))
    transfer = always_redraw(
        lambda: DashedLine(
            point_on_circle(theta.get_value(), radius, center),
            axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=cfg.CYAN,
            stroke_width=2.5,
            dash_length=0.12,
            stroke_opacity=0.72,
        )
    )
    live_curve = always_redraw(
        lambda: axes.plot(np.sin, x_range=[0, max(theta.get_value(), 0.001)], color=cfg.CYAN, stroke_width=7)
    )
    angle_readout = always_redraw(
        lambda: eq(rf"\theta={theta.get_value() / PI:.2f}\pi", cfg.GOLD, cfg.FONT["body"]).move_to([-4.65, -2.75, 0])
    )

    paced_play(
        scene,
        FadeOut(tag),
        LaggedStart(Create(circle), Create(cross), Create(axes), FadeIn(labels), lag_ratio=0.18),
        run_time=2.2,
    )
    scene.add(radius_line, vertical_height, live_curve, transfer, circle_point, graph_point, angle_readout)

    prompt = bottom_caption("Before each stop: predict the height.", cfg.GOLD)
    paced_play(scene, FadeIn(prompt), run_time=0.7)
    stops = (
        (PI / 2, "sin(90°) = 1", cfg.GREEN),
        (PI, "sin(180°) = 0", cfg.WHITE),
        (3 * PI / 2, "sin(270°) = −1", cfg.PURPLE),
        (TAU, "sin(360°) = 0", cfg.WHITE),
    )
    stop_label: Text | None = None
    for value, text, color in stops:
        paced_play(scene, theta.animate.set_value(value), run_time=6.0, rate_func=linear)
        new_label = outlined_text(text, cfg.FONT["body"], color, BOLD).to_edge(DOWN, buff=0.28)
        if stop_label is None:
            paced_play(scene, ReplacementTransform(prompt, new_label), run_time=0.65)
        else:
            paced_play(scene, ReplacementTransform(stop_label, new_label), run_time=0.65)
        stop_label = new_label
        paced_play(scene, Indicate(graph_point, color=cfg.WHITE, scale_factor=1.18), run_time=0.8)
        narration_wait(scene, 1.4)

    sine_name = eq(r"y=\sin\theta", cfg.CYAN, cfg.FONT["hero"]).to_edge(UP, buff=0.42)
    paced_play(scene, FadeIn(sine_name, shift=DOWN * 0.12), FadeOut(stop_label), run_time=1.0)
    narration_wait(scene, 2.2)

    # Re-run the trace continuously so the circle-wave link settles visually.
    theta.set_value(0.001)
    paced_play(scene, theta.animate.set_value(TAU), run_time=16.0, rate_func=linear)
    narration_wait(scene, 1.5)

    # Cosine is the horizontal coordinate and the same wave a quarter turn ahead.
    paced_play(scene, FadeOut(VGroup(transfer, graph_point, live_curve, vertical_height, angle_readout, sine_name)), run_time=0.8)
    horizontal_width = always_redraw(
        lambda: Line(center, [point_on_circle(theta.get_value(), radius, center)[0], center[1], 0], color=cfg.GREEN, stroke_width=8)
    )
    sine_curve = axes.plot(np.sin, x_range=[0, TAU], color=cfg.CYAN, stroke_width=6)
    cosine_curve = axes.plot(np.cos, x_range=[0, TAU], color=cfg.GREEN, stroke_width=6)
    sine_label = eq(r"\sin\theta", cfg.CYAN, cfg.FONT["body"]).move_to(axes.c2p(4.8, -0.72))
    cosine_label = eq(r"\cos\theta", cfg.GREEN, cfg.FONT["body"]).move_to(axes.c2p(5.0, 0.72))
    scene.add(horizontal_width)
    paced_play(scene, Create(sine_curve), run_time=5.0)
    paced_play(scene, Create(cosine_curve), run_time=5.0)
    paced_play(scene, FadeIn(sine_label), FadeIn(cosine_label), run_time=0.8)
    phase = eq(r"\cos\theta=\sin\left(\theta+\frac{\pi}{2}\right)", cfg.WHITE, cfg.FONT["section"]).to_edge(UP, buff=0.4)
    paced_play(scene, Write(phase), run_time=1.2)
    phase_arrow = DoubleArrow(axes.c2p(0, 1.13), axes.c2p(PI / 2, 1.13), color=cfg.GOLD, stroke_width=4, buff=0)
    phase_text = eq(r"\frac{\pi}{2}", cfg.GOLD, cfg.FONT["body"]).next_to(phase_arrow, UP, buff=0.1)
    paced_play(scene, GrowArrow(phase_arrow), FadeIn(phase_text), run_time=1.0)
    narration_wait(scene, 2.5)

    # Expand beyond one turn to make periodicity tangible.
    paced_play(scene, FadeOut(VGroup(circle, cross, radius_line, circle_point, horizontal_width, axes, labels, sine_curve, cosine_curve, sine_label, cosine_label, phase_arrow, phase_text, phase)), run_time=0.9)
    wide_axes = Axes(
        x_range=[-TAU, 2 * TAU, PI],
        y_range=[-1.35, 1.35, 1],
        x_length=13.2,
        y_length=4.4,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.5},
    ).move_to(DOWN * 0.2)
    repeating = wide_axes.plot(np.sin, x_range=[-TAU, 2 * TAU], color=cfg.CYAN, stroke_width=7)
    repeats = VGroup(
        eq(r"-2\pi", cfg.MUTED, cfg.FONT["small"]).next_to(wide_axes.c2p(-TAU, 0), DOWN, buff=0.15),
        eq("0", cfg.MUTED, cfg.FONT["small"]).next_to(wide_axes.c2p(0, 0), DOWN, buff=0.15),
        eq(r"2\pi", cfg.MUTED, cfg.FONT["small"]).next_to(wide_axes.c2p(TAU, 0), DOWN, buff=0.15),
        eq(r"4\pi", cfg.MUTED, cfg.FONT["small"]).next_to(wide_axes.c2p(2 * TAU, 0), DOWN, buff=0.15),
    )
    repeat_title = outlined_text("ONE TURN LATER, THE PATTERN REPEATS", cfg.FONT["body"], cfg.GOLD, BOLD).to_edge(UP, buff=0.46)
    paced_play(scene, Create(wide_axes), FadeIn(repeat_title), FadeIn(repeats), run_time=1.4)
    paced_play(scene, Create(repeating), run_time=12.0, rate_func=linear)
    period_brace = BraceBetweenPoints(wide_axes.c2p(0, -1.15), wide_axes.c2p(TAU, -1.15), color=cfg.GOLD, direction=DOWN)
    period_label = eq(r"\text{period}=2\pi", cfg.GOLD, cfg.FONT["body"]).next_to(period_brace, DOWN, buff=0.15)
    paced_play(scene, GrowFromCenter(period_brace), FadeIn(period_label), run_time=1.0)
    conclusion = bottom_caption("A sine wave is circular height, recorded through angle or time.", cfg.WHITE)
    paced_play(scene, FadeIn(conclusion), run_time=0.8)
    narration_wait(scene, 3.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["08"])
