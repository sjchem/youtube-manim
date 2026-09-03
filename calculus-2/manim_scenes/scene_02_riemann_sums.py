"""Scene 02: rectangles multiply and thin until the sum becomes the integral."""

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
)
from utils.math_utils import distance_traveled, left_riemann_sum, velocity_curve


NEON_CYAN = "#62F5FF"
NEON_PINK = "#FF5AD9"
NEON_YELLOW = "#FFF45C"
NEON_GREEN = "#72FF98"


class Scene02RiemannSums(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "02")
    add_cinematic_background(scene)

    axes = calc_axes(x_range=(0, 6, 1), y_range=(0, 30, 10), x_length=10.4, y_length=4.4).move_to([0, 0.18, 0])
    axes.x_axis.set_stroke(width=3.2)
    axes.y_axis.set_stroke(width=3.2)
    t_label = eq("t", NEON_CYAN, cfg.FONT["section"]).next_to(axes.x_axis.get_right(), RIGHT, buff=0.22).shift(DOWN * 0.10)
    v_label = eq("v(t)", NEON_CYAN, cfg.FONT["section"]).next_to(axes.y_axis.get_top(), LEFT, buff=0.22)
    labels = VGroup(t_label, v_label)
    curve = axes.plot(velocity_curve, x_range=[0, 6], color=NEON_CYAN, stroke_width=6)
    curve_glow = curve.copy().set_stroke(NEON_CYAN, width=18, opacity=0.16)
    paced_play(scene, Create(axes), FadeIn(labels), FadeIn(curve_glow), Create(curve), run_time=1.4)
    narration_wait(scene, 3.87)

    n_label = eq("n=4", NEON_YELLOW, cfg.FONT["hero"]).to_edge(UP, buff=0.38)
    rects = riemann_group(axes, curve, velocity_curve, 0, 6, 4, NEON_PINK, 0.62)
    paced_play(scene, FadeIn(n_label), FadeIn(rects), run_time=2.5, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.37)

    sum_formula = equation_card(
        r"\text{distance}\approx v_1\Delta t+v_2\Delta t+v_3\Delta t+v_4\Delta t",
        NEON_YELLOW,
        cfg.FONT["body"],
    )
    if sum_formula.width > 13.2:
        sum_formula.scale_to_fit_width(13.2)
    sum_formula.next_to(axes, DOWN, buff=0.28)
    paced_play(scene, FadeIn(sum_formula, shift=UP * 0.10), run_time=2.6)
    narration_wait(scene, 7.85)

    rough = bottom_caption("Only four rectangles — visibly rough.", cfg.WHITE)
    paced_play(scene, FadeOut(sum_formula), FadeIn(rough), run_time=0.8)
    narration_wait(scene, 6.47)
    paced_play(scene, FadeOut(rough), run_time=0.5)

    counts = (10, 50, 200)
    colors = (NEON_YELLOW, NEON_CYAN, NEON_GREEN)
    current_rects = rects
    for count, color in zip(counts, colors):
        new_n_label = eq(f"n={count}", color, cfg.FONT["hero"]).to_edge(UP, buff=0.38)
        new_rects = riemann_group(axes, curve, velocity_curve, 0, 6, count, color, 0.6 if count < 200 else 0.5)
        paced_play(
            scene,
            ReplacementTransform(current_rects, new_rects),
            ReplacementTransform(n_label, new_n_label),
            run_time=3.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        n_label = new_n_label
        current_rects = new_rects
        narration_wait(scene, 1.24)

    thin_caption = bottom_caption("Each rectangle thins. The gaps disappear.", NEON_GREEN)
    paced_play(scene, FadeIn(thin_caption), run_time=0.8)
    narration_wait(scene, 7.76)
    paced_play(scene, FadeOut(thin_caption), run_time=0.6)

    approx = left_riemann_sum(velocity_curve, 0.0, 6.0, 200)
    exact = distance_traveled(0.0, 6.0)
    readout = equation_card(
        rf"n=200:\; {approx:.2f}\text{{ m}} \qquad \text{{exact}}:\; {exact:.2f}\text{{ m}}",
        NEON_GREEN,
        cfg.FONT["body"],
    ).next_to(axes, DOWN, buff=0.28)
    paced_play(scene, FadeIn(readout, shift=UP * 0.10), run_time=1.0)
    narration_wait(scene, 4.13)

    paced_play(scene, FadeOut(VGroup(current_rects, n_label, readout, curve_glow, curve, axes, labels)), run_time=0.9)

    integral_notation = eq(r"\int_a^b f(x)\,dx", NEON_CYAN, cfg.FONT["hero"])
    paced_play(scene, Write(integral_notation), run_time=3.2)
    narration_wait(scene, 7.45)

    paced_play(scene, integral_notation.animate.shift(UP * 0.5), run_time=0.6)
    box_text = eq(
        r"\text{Integral} = \text{sum of infinitely many tiny pieces}",
        NEON_YELLOW,
        cfg.FONT["body"],
    ).next_to(integral_notation, DOWN, buff=0.55)
    box = SurroundingRectangle(box_text, color=NEON_YELLOW, buff=0.28, corner_radius=0.12)
    paced_play(scene, FadeIn(box_text), Create(box), run_time=1.1)
    narration_wait(scene, 11.63)

    end_scene(scene, started, cfg.SCENE_DURATIONS["02"])
