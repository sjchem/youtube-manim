"""Scene 09: reversing a derivative to recover position — and the mystery of +C."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    calc_axis_labels,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    paced_play,
)
from utils.math_utils import position_family


class Scene09ReverseProblem(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "09")
    add_cinematic_background(scene)

    velocity_label = eq("v(t)=2t", cfg.CYAN, cfg.FONT["title"]).to_edge(UP, buff=0.5)
    question = bottom_caption("We know the velocity. Can we rebuild position?", cfg.WHITE)
    paced_play(scene, Write(velocity_label), FadeIn(question), run_time=1.2)
    narration_wait(scene, 10.36)
    paced_play(scene, FadeOut(question), run_time=0.5)

    chain = VGroup(
        eq(r"s(t)=\int 2t\,dt", cfg.WHITE, cfg.FONT["section"]),
        eq(r"s(t)=t^2+C", cfg.GOLD, cfg.FONT["title"]),
    ).arrange(DOWN, buff=0.3).next_to(velocity_label, DOWN, buff=0.45)
    for line in chain:
        paced_play(scene, Write(line), run_time=1.1)
        narration_wait(scene, 6.91)

    # Keep the conclusion visible: remove only the two setup equations, then
    # promote the existing final result to a centered heading for the graph.
    pinned_formula = chain[1]
    paced_play(
        scene,
        FadeOut(VGroup(velocity_label, chain[0])),
        pinned_formula.animate.to_edge(UP, buff=0.34),
        run_time=1.1,
        rate_func=rate_functions.ease_in_out_sine,
    )

    axes = calc_axes(x_range=(-3, 3, 1), y_range=(-3, 10, 2), x_length=9.2, y_length=4.4).move_to([0, -1.3, 0])
    labels = calc_axis_labels(axes, "t", "s(t)")
    paced_play(scene, Create(axes), FadeIn(labels), run_time=1.1)

    specs = ((-2.0, cfg.CYAN, "t^2-2"), (0.0, cfg.WHITE, "t^2"), (3.0, cfg.GREEN, "t^2+3"))
    curves = VGroup()
    curve_labels = VGroup()
    for constant, color, tex in specs:
        curve = axes.plot(lambda t, c=constant: position_family(t, c), x_range=[-2.7, 2.7], color=color, stroke_width=5)
        tag = eq(tex, color, cfg.FONT["small"]).move_to(axes.c2p(2.35, position_family(2.35, constant)) + RIGHT * 0.55)
        curves.add(curve)
        curve_labels.add(tag)
        paced_play(scene, Create(curve), FadeIn(tag), run_time=0.9)
        narration_wait(scene, 3.80)

    x_tracker = ValueTracker(-2.2)
    guide = always_redraw(
        lambda: DashedLine(
            axes.c2p(x_tracker.get_value(), -3),
            axes.c2p(x_tracker.get_value(), 10),
            color=cfg.MUTED,
            stroke_width=2,
            dash_length=0.1,
        )
    )
    markers = always_redraw(
        lambda: VGroup(
            *(glow_dot(axes.c2p(x_tracker.get_value(), position_family(x_tracker.get_value(), constant)), color, 0.08) for constant, color, _ in specs)
        )
    )

    def tangent_family() -> VGroup:
        t = x_tracker.get_value()
        dt = 0.42
        slope = 2 * t
        lines = VGroup()
        for constant, color, _ in specs:
            y = position_family(t, constant)
            lines.add(
                Line(
                    axes.c2p(t - dt, y - slope * dt),
                    axes.c2p(t + dt, y + slope * dt),
                    color=color,
                    stroke_width=4,
                )
            )
        return lines

    tangents = always_redraw(tangent_family)
    scene.add(guide, markers, tangents)
    paced_play(scene, FadeIn(guide), FadeIn(markers), FadeIn(tangents), run_time=1.0)
    slope_caption = bottom_caption("Same slope everywhere — only the height differs.", cfg.GOLD)
    paced_play(scene, FadeIn(slope_caption), run_time=0.8)
    paced_play(scene, x_tracker.animate.set_value(2.2), run_time=10.66, rate_func=rate_functions.ease_in_out_sine)
    paced_play(scene, FadeOut(slope_caption), run_time=0.5)

    explanation = bottom_caption("Differentiating erases vertical position. Integrating can't recover it alone.", cfg.WHITE)
    paced_play(scene, FadeIn(explanation), run_time=0.9)
    narration_wait(scene, 12.08)

    end_scene(scene, started, cfg.SCENE_DURATIONS["09"])
