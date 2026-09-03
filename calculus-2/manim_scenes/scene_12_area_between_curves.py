"""Scene 12: complicated shapes become simple when sliced into tiny vertical strips."""

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
    narration_wait,
    paced_play,
    riemann_group,
)
from utils.math_utils import lower_curve, upper_curve


NEON_CYAN = "#62F5FF"
NEON_PINK = "#FF5AD9"
NEON_YELLOW = "#FFF45C"


class Scene12AreaBetweenCurves(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "12")
    add_cinematic_background(scene)

    axes = calc_axes(x_range=(-2, 2, 1), y_range=(-1.5, 4, 1), x_length=9.4, y_length=4.8).move_to([0, -0.3, 0])
    axes.x_axis.set_stroke(width=3.1)
    axes.y_axis.set_stroke(width=3.1)
    x_label = eq("x", NEON_CYAN, cfg.FONT["section"]).next_to(
        axes.x_axis.get_right(), RIGHT, buff=0.22
    ).shift(DOWN * 0.16)
    y_label = eq("y", NEON_CYAN, cfg.FONT["section"]).next_to(
        axes.y_axis.get_top(), RIGHT, buff=0.18
    )
    labels = VGroup(x_label, y_label)
    f_curve = axes.plot(upper_curve, x_range=[-2, 2], color=NEON_PINK, stroke_width=7).set_z_index(3)
    g_curve = axes.plot(lower_curve, x_range=[-2, 2], color=NEON_CYAN, stroke_width=7).set_z_index(3)
    f_glow = f_curve.copy().set_stroke(NEON_PINK, width=17, opacity=0.13).set_z_index(2)
    g_glow = g_curve.copy().set_stroke(NEON_CYAN, width=17, opacity=0.13).set_z_index(2)
    f_tag = eq("f(x)", NEON_PINK, cfg.FONT["body"]).next_to(axes.c2p(-1.9, upper_curve(-1.9)), UP, buff=0.12).set_z_index(4)
    g_tag = eq("g(x)", NEON_CYAN, cfg.FONT["body"]).next_to(axes.c2p(-1.9, lower_curve(-1.9)), DOWN, buff=0.12).set_z_index(4)
    paced_play(scene, Create(axes), FadeIn(labels), run_time=1.0)
    paced_play(scene, Create(f_glow), Create(f_curve), FadeIn(f_tag), run_time=1.0)
    paced_play(scene, Create(g_glow), Create(g_curve), FadeIn(g_tag), run_time=1.0)
    narration_wait(scene, 5.27)

    x0 = -0.6
    gap_line = Line(axes.c2p(x0, lower_curve(x0)), axes.c2p(x0, upper_curve(x0)), color=NEON_YELLOW, stroke_width=6)
    gap_brace = BraceBetweenPoints(axes.c2p(x0, lower_curve(x0)), axes.c2p(x0, upper_curve(x0)), direction=LEFT, color=NEON_YELLOW)
    gap_label = eq("f(x)-g(x)", NEON_YELLOW, cfg.FONT["small"]).next_to(gap_brace, LEFT, buff=0.15)
    paced_play(scene, Create(gap_line), GrowFromCenter(gap_brace), FadeIn(gap_label), run_time=1.1)
    narration_wait(scene, 6.58)
    paced_play(scene, FadeOut(VGroup(gap_line, gap_brace, gap_label)), run_time=0.6)

    strip_formula = eq(r"[f(x)-g(x)]\,dx", cfg.GOLD, cfg.FONT["section"]).to_edge(UP, buff=0.5)
    coarse_strips = riemann_group(axes, f_curve, upper_curve, -1.9, 1.9, 8, cfg.ORANGE, 0.62, bounded_graph=g_curve)
    paced_play(scene, Write(strip_formula), run_time=1.5)
    paced_play(
        scene,
        LaggedStart(*(GrowFromEdge(rect, DOWN) for rect in coarse_strips), lag_ratio=0.12),
        run_time=3.0,
    )
    narration_wait(scene, 1.87)

    strips = riemann_group(axes, f_curve, upper_curve, -1.9, 1.9, 55, cfg.GOLD, 0.55, bounded_graph=g_curve)
    paced_play(scene, FadeOut(strip_formula), ReplacementTransform(coarse_strips, strips), run_time=5.5, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.98)

    caption = bottom_caption("Hundreds of tiny strips fill the region between the curves.", cfg.WHITE)
    paced_play(scene, FadeIn(caption), run_time=0.8)
    narration_wait(scene, 7.89)
    paced_play(scene, FadeOut(caption), run_time=0.5)

    integral = eq(r"A=\int_a^b [f(x)-g(x)]\,dx", cfg.GREEN, cfg.FONT["title"]).to_edge(UP, buff=0.5)
    paced_play(scene, Write(integral), run_time=1.3)
    narration_wait(scene, 7.89)

    closing = bottom_caption("Complicated shapes become simple when sliced thin enough.", cfg.GOLD)
    paced_play(scene, FadeIn(closing), run_time=0.9)
    narration_wait(scene, 6.58)

    end_scene(scene, started, cfg.SCENE_DURATIONS["12"])
