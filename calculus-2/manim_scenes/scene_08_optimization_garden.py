"""Scene 08: a fenced garden beside a river — where does the area stop improving?"""

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
    river_garden_diagram,
    tangent_line,
)
from utils.math_utils import d_garden_area, garden_area, garden_optimal_width


class Scene08OptimizationGarden(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "08")
    add_cinematic_background(scene)

    fence_caption = eq(r"100\text{ m of fencing} \;+\; \text{one river edge}", cfg.WHITE, cfg.FONT["small"]).to_edge(UP, buff=0.5)
    paced_play(scene, FadeIn(fence_caption), run_time=0.9)
    narration_wait(scene, 6.40)

    w_t = ValueTracker(6.0)
    diagram = always_redraw(lambda: river_garden_diagram(w_t.get_value(), 100.0, 0.045).move_to([-3.6, -0.3, 0]))
    scene.add(diagram)
    paced_play(scene, FadeIn(diagram), run_time=0.9)

    setup_group = VGroup(
        eq(r"2x+y=100", cfg.CYAN, cfg.FONT["small"]),
        eq(r"y=100-2x", cfg.CYAN, cfg.FONT["small"]),
        eq(r"A(x)=x(100-2x)", cfg.GOLD, cfg.FONT["section"]),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.4, 1.2, 0])
    for line in setup_group:
        paced_play(scene, Write(line), run_time=0.9)
        narration_wait(scene, 3.84)

    narrow_caption = bottom_caption("Very narrow: small area.", cfg.RED)
    paced_play(scene, FadeIn(narrow_caption), run_time=0.6)
    paced_play(scene, w_t.animate.set_value(4.0), run_time=4.6, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.12)

    wide_caption = bottom_caption("Very wide: also small area.", cfg.RED)
    paced_play(scene, ReplacementTransform(narrow_caption, wide_caption), run_time=0.6)
    paced_play(scene, w_t.animate.set_value(46.0), run_time=6.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 1.52)

    between_caption = bottom_caption("Somewhere in between, the area peaks.", cfg.GOLD)
    paced_play(scene, ReplacementTransform(wide_caption, between_caption), run_time=0.6)
    paced_play(scene, w_t.animate.set_value(25.0), run_time=5.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 2.32)
    paced_play(scene, FadeOut(between_caption), run_time=0.5)

    paced_play(scene, FadeOut(VGroup(diagram, setup_group, fence_caption)), run_time=0.8)

    axes = calc_axes(x_range=(0, 50, 10), y_range=(0, 1300, 300), x_length=9.4, y_length=4.6).move_to([0, -0.4, 0])
    labels = calc_axis_labels(axes, "x", "A(x)")
    curve = axes.plot(garden_area, x_range=[0, 50], color=cfg.WHITE, stroke_width=6)
    paced_play(scene, Create(axes), FadeIn(labels), Create(curve), run_time=1.5)
    scan_x = ValueTracker(2.0)
    scan_dot = always_redraw(lambda: glow_dot(axes.c2p(scan_x.get_value(), garden_area(scan_x.get_value())), cfg.CYAN, 0.09))
    scan_tangent = always_redraw(lambda: tangent_line(axes, garden_area, d_garden_area, scan_x.get_value(), cfg.CYAN, half_length=2.0))
    scene.add(scan_tangent, scan_dot)
    paced_play(scene, FadeIn(scan_tangent), FadeIn(scan_dot), run_time=0.6)
    paced_play(scene, scan_x.animate.set_value(25.0), run_time=8.7, rate_func=rate_functions.ease_in_out_sine)

    x_opt = garden_optimal_width(100.0)
    peak_area = garden_area(x_opt, 100.0)
    flat_tangent = tangent_line(axes, garden_area, d_garden_area, x_opt, cfg.GOLD, half_length=6.0)
    peak_dot = glow_dot(axes.c2p(x_opt, peak_area), cfg.GOLD, 0.11)
    paced_play(scene, FadeOut(scan_dot), FadeOut(scan_tangent), FadeIn(peak_dot), FadeIn(flat_tangent), run_time=1.0)
    narration_wait(scene, 0.98)

    derivative_formula = eq(r"A'(x)=100-4x", cfg.CYAN, cfg.FONT["section"]).next_to(axes, UP, buff=0.2)
    paced_play(scene, Write(derivative_formula), run_time=1.1)
    narration_wait(scene, 8.00)

    solve = eq(rf"A'(x)=0 \;\Rightarrow\; x={x_opt:.0f}", cfg.GOLD, cfg.FONT["title"]).move_to(derivative_formula)
    paced_play(scene, ReplacementTransform(derivative_formula, solve), run_time=1.1)
    box = SurroundingRectangle(solve, color=cfg.GOLD, buff=0.26, corner_radius=0.12)
    paced_play(scene, Create(box), run_time=0.7)
    narration_wait(scene, 9.60)

    closing = bottom_caption("The point where improvement stops and decline begins.", cfg.WHITE)
    paced_play(scene, FadeIn(closing), run_time=0.9)
    narration_wait(scene, 11.21)

    end_scene(scene, started, cfg.SCENE_DURATIONS["08"])
