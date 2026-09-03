"""Scene 04: two synchronized graphs reveal the Fundamental Theorem of Calculus."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    area_region,
    begin_scene,
    bottom_caption,
    dual_axes,
    end_scene,
    eq,
    equation_card,
    glow_dot,
    narration_wait,
    paced_play,
    thin_strip,
)
from utils.math_utils import accumulation_function, accumulation_integrand


NEON_CYAN = "#62F5FF"
NEON_PINK = "#FF5AD9"
NEON_YELLOW = "#FFF45C"
NEON_GREEN = "#72FF98"


class Scene04FundamentalTheorem(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "04")
    add_cinematic_background(scene)

    top_axes, bottom_axes = dual_axes(top_range=(0, 6, 2), bottom_range=(0, 8, 2), x_range=(0, 4, 1))
    top_axes.x_axis.set_stroke(width=3.0)
    top_axes.y_axis.set_stroke(width=3.0)
    bottom_axes.x_axis.set_stroke(width=3.0)
    bottom_axes.y_axis.set_stroke(width=3.0)
    top_label = eq("y=f(x)", NEON_CYAN, cfg.FONT["body"]).next_to(top_axes, UP, buff=0.10).align_to(top_axes, LEFT)
    bottom_label = eq(r"y=A(x)=\int_a^x f(t)\,dt", NEON_PINK, cfg.FONT["body"]).next_to(bottom_axes, UP, buff=0.10).align_to(bottom_axes, LEFT)
    top_curve = top_axes.plot(accumulation_integrand, x_range=[0, 4], color=NEON_CYAN, stroke_width=6)
    top_curve_glow = top_curve.copy().set_stroke(NEON_CYAN, width=16, opacity=0.12)

    paced_play(scene, Create(top_axes), FadeIn(top_label), Create(top_curve_glow), Create(top_curve), run_time=1.3)
    narration_wait(scene, 5.84)
    paced_play(scene, Create(bottom_axes), FadeIn(bottom_label), run_time=1.0)
    narration_wait(scene, 7.29)

    x_tracker = ValueTracker(0.05)

    def current_area() -> VMobject:
        x = max(0.05, x_tracker.get_value())
        return area_region(top_axes, top_curve, 0, x, NEON_CYAN, 0.52)

    def current_bottom_curve() -> VMobject:
        x = max(0.05, x_tracker.get_value())
        return bottom_axes.plot(accumulation_function, x_range=[0, x], color=NEON_PINK, stroke_width=7)

    area_mobj = always_redraw(current_area)
    bottom_curve_mobj = always_redraw(current_bottom_curve)
    cursor = always_redraw(
        lambda: DashedLine(
            top_axes.c2p(x_tracker.get_value(), 0),
            top_axes.c2p(x_tracker.get_value(), accumulation_integrand(x_tracker.get_value())),
            color=NEON_YELLOW,
            stroke_width=3,
            dash_length=0.09,
        )
    )
    top_dot = always_redraw(lambda: glow_dot(top_axes.c2p(x_tracker.get_value(), accumulation_integrand(x_tracker.get_value())), NEON_YELLOW, 0.10))
    bottom_dot = always_redraw(lambda: glow_dot(bottom_axes.c2p(x_tracker.get_value(), accumulation_function(x_tracker.get_value())), NEON_PINK, 0.10))

    scene.add(area_mobj, bottom_curve_mobj, cursor, top_dot, bottom_dot)
    caption = bottom_caption("The area fills in — and a matching point traces the accumulation below.", NEON_CYAN)
    paced_play(scene, FadeIn(caption), run_time=0.8)
    paced_play(scene, x_tracker.animate.set_value(4.0), run_time=12.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.24)
    paced_play(scene, FadeOut(caption), run_time=0.6)

    # -- Zoom: a tiny step dx turns into a thin rectangle -------------------
    x_tracker.set_value(2.3)
    dx_tracker = ValueTracker(0.65)
    strip = always_redraw(lambda: thin_strip(top_axes, accumulation_integrand, 2.3, dx_tracker.get_value(), NEON_YELLOW, 0.92))
    strip_caption = bottom_caption("Move x forward by a tiny dx.", NEON_YELLOW)
    paced_play(scene, FadeIn(strip), FadeIn(strip_caption), run_time=1.5)
    narration_wait(scene, 9.24)

    formula_position = np.array([3.65, -1.15, 0.0])
    da_formula = equation_card(r"dA\approx f(x)\,dx", NEON_YELLOW, cfg.FONT["title"]).move_to(formula_position)
    paced_play(scene, FadeOut(strip_caption), FadeIn(da_formula, shift=RIGHT * 0.15), run_time=1.8)
    paced_play(scene, dx_tracker.animate.set_value(0.07), run_time=8.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 6.00)

    ratio_formula = equation_card(r"\frac{dA}{dx}\approx f(x)", NEON_YELLOW, cfg.FONT["hero"]).move_to(formula_position)
    paced_play(scene, ReplacementTransform(da_formula, ratio_formula), run_time=2.5)
    narration_wait(scene, 10.76)

    ftc_box = equation_card(r"A'(x)=f(x)", NEON_GREEN, cfg.FONT["hero"]).move_to(formula_position)
    paced_play(scene, ReplacementTransform(ratio_formula, ftc_box), run_time=2.3)
    paced_play(scene, Circumscribe(ftc_box, color=NEON_GREEN, fade_out=True), run_time=1.3)
    narration_wait(scene, 13.10)

    final_caption = bottom_caption("One graph's height controls how fast the other's area grows.", NEON_GREEN)
    paced_play(scene, FadeIn(final_caption), run_time=1.1)
    narration_wait(scene, 19.47)

    end_scene(scene, started, cfg.SCENE_DURATIONS["04"])
