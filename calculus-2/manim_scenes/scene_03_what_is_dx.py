"""Scene 03: dx made visual — one thin strip, then thousands of them."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axes,
    end_scene,
    eq,
    equation_card,
    narration_wait,
    paced_play,
    riemann_group,
    thin_strip,
)
from utils.math_utils import accumulation_integrand


NEON_CYAN = "#62F5FF"
NEON_PINK = "#FF5AD9"
NEON_YELLOW = "#FFF45C"
NEON_GREEN = "#72FF98"


class Scene03WhatIsDx(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "03")
    add_cinematic_background(scene)

    axes = calc_axes(x_range=(0, 5, 1), y_range=(0, 7, 2), x_length=10.4, y_length=4.5).move_to([0, 0.15, 0])
    axes.x_axis.set_stroke(width=3.2)
    axes.y_axis.set_stroke(width=3.2)
    x_label = eq("x", NEON_CYAN, cfg.FONT["section"]).next_to(
        axes.x_axis.get_right(), RIGHT, buff=0.22
    ).shift(DOWN * 0.10)
    y_label = eq("f(x)", NEON_CYAN, cfg.FONT["section"]).next_to(
        axes.y_axis.get_top(), LEFT, buff=0.22
    )
    labels = VGroup(x_label, y_label)
    curve = axes.plot(accumulation_integrand, x_range=[0, 5], color=NEON_CYAN, stroke_width=6)
    curve_glow = curve.copy().set_stroke(NEON_CYAN, width=16, opacity=0.12)
    paced_play(scene, Create(axes), FadeIn(labels), Create(curve_glow), Create(curve), run_time=1.4)
    narration_wait(scene, 3.93)

    x0 = 2.3
    dx_tracker = ValueTracker(0.8)
    strip = always_redraw(lambda: thin_strip(axes, accumulation_integrand, x0, dx_tracker.get_value(), NEON_PINK, 0.9))
    paced_play(scene, FadeIn(strip, scale=1.05), run_time=1.0)
    narration_wait(scene, 2.61)

    width_brace = always_redraw(
        lambda: BraceBetweenPoints(axes.c2p(x0, 0), axes.c2p(x0 + dx_tracker.get_value(), 0), direction=DOWN, color=NEON_YELLOW)
    )
    width_label = always_redraw(lambda: eq("dx", NEON_YELLOW, cfg.FONT["section"]).next_to(width_brace, DOWN, buff=0.14))
    height_brace = always_redraw(
        lambda: BraceBetweenPoints(
            axes.c2p(x0 + dx_tracker.get_value(), 0),
            axes.c2p(x0 + dx_tracker.get_value(), accumulation_integrand(x0)),
            direction=RIGHT,
            color=NEON_GREEN,
        )
    )
    height_label = always_redraw(lambda: eq("f(x)", NEON_GREEN, cfg.FONT["section"]).next_to(height_brace, RIGHT, buff=0.14))
    paced_play(scene, GrowFromCenter(width_brace), FadeIn(width_label), run_time=0.9)
    narration_wait(scene, 4.19)
    paced_play(scene, GrowFromCenter(height_brace), FadeIn(height_label), run_time=0.9)
    paced_play(scene, dx_tracker.animate.set_value(0.16), run_time=4.19, rate_func=rate_functions.ease_in_out_sine)

    da_formula = equation_card(r"dA\approx f(x)\,dx", NEON_YELLOW, cfg.FONT["section"]).to_edge(UP, buff=0.32)
    paced_play(scene, FadeIn(da_formula, shift=DOWN * 0.12), run_time=2.4)
    narration_wait(scene, 6.75)

    paced_play(
        scene,
        FadeOut(VGroup(width_brace, width_label, height_brace, height_label, strip)),
        run_time=0.7,
    )

    many_strips = riemann_group(axes, curve, accumulation_integrand, 0.05, 4.95, 120, NEON_GREEN, 0.60)
    caption = bottom_caption("More and more thin strips build the whole region.", NEON_GREEN)
    paced_play(
        scene,
        LaggedStart(*(GrowFromEdge(rect, DOWN) for rect in many_strips), lag_ratio=0.012),
        FadeIn(caption),
        run_time=4.8,
    )
    narration_wait(scene, 5.97)

    paced_play(scene, FadeOut(caption), run_time=0.5)
    meaning = equation_card(
        r"\int_a^b f(x)\,dx \;\approx\; \text{add every }f(x)\,dx\text{ from }a\text{ to }b",
        NEON_YELLOW,
        cfg.FONT["body"],
    )
    if meaning.width > 13.6:
        meaning.scale_to_fit_width(13.6)
    meaning.next_to(axes, DOWN, buff=0.28)
    paced_play(scene, FadeOut(da_formula), FadeIn(meaning, shift=UP * 0.12), run_time=1.6)
    narration_wait(scene, 10.47)

    end_scene(scene, started, cfg.SCENE_DURATIONS["03"])
