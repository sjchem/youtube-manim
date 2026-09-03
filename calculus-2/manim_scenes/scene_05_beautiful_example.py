"""Scene 05: f(x) = x, a triangle, and a formula that closes the loop on itself."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    area_region,
    begin_scene,
    bottom_caption,
    calc_axes,
    end_scene,
    eq,
    narration_wait,
    paced_play,
)
from utils.math_utils import identity_fn


NEON_CYAN = "#62F5FF"
NEON_PINK = "#FF5AD9"
NEON_YELLOW = "#FFF45C"
NEON_GREEN = "#72FF98"


class Scene05BeautifulExample(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "05")
    add_cinematic_background(scene)

    f_label = eq("f(x)=x", NEON_CYAN, cfg.FONT["section"]).to_edge(UP, buff=0.5)
    paced_play(scene, Write(f_label), run_time=1.0)
    narration_wait(scene, 4.01)

    axes = calc_axes(x_range=(0, 4, 1), y_range=(0, 4, 1), x_length=6.4, y_length=4.9).move_to([-3.6, -0.5, 0])
    axes.x_axis.set_stroke(width=3.1)
    axes.y_axis.set_stroke(width=3.1)
    x_axis_label = eq("x", NEON_CYAN, cfg.FONT["section"]).next_to(
        axes.x_axis.get_right(), RIGHT, buff=0.20
    ).shift(DOWN * 0.22)
    y_axis_label = eq("f(x)", NEON_CYAN, cfg.FONT["section"]).next_to(
        axes.y_axis.get_top(), LEFT, buff=0.18
    )
    labels = VGroup(x_axis_label, y_axis_label)
    curve = axes.plot(identity_fn, x_range=[0, 4], color=NEON_CYAN, stroke_width=6)
    curve_glow = curve.copy().set_stroke(NEON_CYAN, width=16, opacity=0.12)
    paced_play(scene, Create(axes), FadeIn(labels), Create(curve_glow), Create(curve), run_time=1.4)
    narration_wait(scene, 2.67)

    x_tracker = ValueTracker(0.15)
    triangle = always_redraw(lambda: area_region(axes, curve, 0, x_tracker.get_value(), NEON_CYAN, 0.48))
    base_brace = always_redraw(
        lambda: BraceBetweenPoints(axes.c2p(0, 0), axes.c2p(x_tracker.get_value(), 0), direction=DOWN, color=NEON_YELLOW)
    )
    base_label = always_redraw(lambda: eq("x", NEON_YELLOW, cfg.FONT["body"]).next_to(base_brace, DOWN, buff=0.12))
    height_brace = always_redraw(
        lambda: BraceBetweenPoints(
            axes.c2p(x_tracker.get_value(), 0),
            axes.c2p(x_tracker.get_value(), x_tracker.get_value()),
            direction=RIGHT,
            color=NEON_PINK,
        )
    )
    height_label = always_redraw(lambda: eq("x", NEON_PINK, cfg.FONT["body"]).next_to(height_brace, RIGHT, buff=0.12))
    paced_play(scene, FadeIn(triangle), FadeIn(base_brace), FadeIn(base_label), FadeIn(height_brace), FadeIn(height_label), run_time=1.4)
    paced_play(scene, x_tracker.animate.set_value(3.0), run_time=5.36, rate_func=rate_functions.ease_in_out_sine)

    formula = eq(r"A(x)=\tfrac12\,\text{base}\times\text{height}", NEON_YELLOW, cfg.FONT["body"]).move_to([4.15, 1.4, 0])
    paced_play(scene, Write(formula), run_time=2.0)
    narration_wait(scene, 3.28)
    next_formula = eq(r"A(x)=\tfrac12\,x\cdot x", NEON_YELLOW, cfg.FONT["section"]).move_to(formula)
    paced_play(scene, TransformMatchingTex(formula, next_formula), run_time=2.0)
    formula = next_formula
    narration_wait(scene, 3.28)
    next_formula = eq(r"A(x)=\frac{x^2}{2}", NEON_YELLOW, cfg.FONT["title"]).move_to(formula)
    paced_play(scene, TransformMatchingTex(formula, next_formula), run_time=2.0)
    formula = next_formula
    narration_wait(scene, 3.28)

    d_arrow = eq(r"\frac{d}{dx}\left(\frac{x^2}{2}\right)=x", NEON_GREEN, cfg.FONT["title"]).next_to(formula, DOWN, buff=0.72)
    paced_play(scene, Write(d_arrow), run_time=2.3)
    narration_wait(scene, 8.03)

    paced_play(scene, FadeOut(VGroup(base_brace, base_label, height_brace, height_label, formula, d_arrow)), run_time=0.7)

    chain = VGroup(
        eq("x", NEON_CYAN, cfg.FONT["hero"]),
        eq(r"\longrightarrow", NEON_CYAN, cfg.FONT["hero"]),
        eq(r"\frac{x^2}{2}", NEON_YELLOW, cfg.FONT["hero"]),
        eq(r"\longrightarrow", NEON_GREEN, cfg.FONT["hero"]),
        eq("x", NEON_GREEN, cfg.FONT["hero"]),
    ).arrange(RIGHT, buff=0.68).move_to([0, 0.25, 0])
    integrate_label = eq(r"\text{integrate}", NEON_CYAN, cfg.FONT["body"]).next_to(chain[1], UP, buff=0.20)
    differentiate_label = eq(r"\text{differentiate}", NEON_GREEN, cfg.FONT["body"]).next_to(chain[3], UP, buff=0.20)
    paced_play(scene, FadeOut(VGroup(triangle, axes, labels, curve_glow, curve, f_label)), run_time=0.6)
    paced_play(scene, Write(chain), FadeIn(integrate_label), FadeIn(differentiate_label), run_time=2.6)
    narration_wait(scene, 6.69)

    closing = bottom_caption("Impossible to forget: this is the Fundamental Theorem, in miniature.", NEON_YELLOW)
    paced_play(scene, FadeIn(closing), run_time=0.9)
    narration_wait(scene, 8.03)

    end_scene(scene, started, cfg.SCENE_DURATIONS["05"])
