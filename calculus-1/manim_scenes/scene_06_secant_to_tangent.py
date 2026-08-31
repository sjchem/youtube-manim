"""Scene 06: build the derivative of x^2 by hand, geometry and algebra together."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    calc_axis_labels,
    calc_axes,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    paced_play,
    secant_line,
    tangent_line,
)
from utils.math_utils import d_square, square


class Scene06SecantToTangent(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "06")
    add_cinematic_background(scene)

    f_label = eq("f(x)=x^2", cfg.WHITE, cfg.FONT["section"]).to_edge(UP, buff=0.4)
    paced_play(scene, Write(f_label), run_time=1.1)
    narration_wait(scene, 11.61)

    axes = calc_axes(x_range=(-2.2, 2.2, 1), y_range=(-0.5, 4.5, 1), x_length=6.6, y_length=5.3).move_to([-4.0, -0.6, 0])
    axis_labels = calc_axis_labels(axes)
    curve = axes.plot(square, x_range=[-2.15, 2.15], color=cfg.WHITE, stroke_width=6)
    paced_play(scene, Create(axes), FadeIn(axis_labels), run_time=1.6)
    paced_play(scene, Create(curve), run_time=3.4, rate_func=rate_functions.ease_in_out_sine)

    x0 = 1.25
    h_tracker = ValueTracker(1.0)
    p_point = glow_dot(axes.c2p(x0, square(x0)), cfg.WHITE, 0.12)
    p_label = eq("P=(x,x^2)", cfg.WHITE, cfg.FONT["small"])
    p_label.next_to(p_point, RIGHT, buff=0.28).shift(DOWN * 0.5)
    paced_play(scene, FadeIn(p_point), FadeIn(p_label), run_time=1.0)

    q_point = always_redraw(lambda: glow_dot(axes.c2p(x0 + h_tracker.get_value(), square(x0 + h_tracker.get_value())), cfg.GOLD, 0.115))
    q_label = eq("Q=(x{+}h,(x{+}h)^2)", cfg.GOLD, cfg.FONT["small"])

    def place_q_label(mob: Mobject) -> None:
        # Stay to the right of Q throughout. As Q approaches P, glide the
        # label from below Q to above Q so the two labels remain separated.
        h = h_tracker.get_value()
        blend = max(0.0, min(1.0, (0.45 - h) / 0.35))
        vertical_offset = -0.45 * (1.0 - blend) + 0.55 * blend
        horizontal_offset = 1.55 * (1.0 - blend) + 2.05 * blend
        mob.move_to(q_point.get_center() + RIGHT * horizontal_offset + UP * vertical_offset)

    q_label.add_updater(place_q_label)
    secant = always_redraw(lambda: secant_line(axes, square, x0, h_tracker.get_value(), cfg.CYAN))
    scene.add(secant, q_point, q_label)
    paced_play(scene, FadeIn(q_point), FadeIn(q_label), run_time=1.0)
    narration_wait(scene, 3.0)

    # -- Algebra, stacked on the right --
    slope_expr = eq(r"\frac{(x+h)^2-x^2}{h}", cfg.CYAN, cfg.FONT["body"]).move_to([4.0, 2.3, 0])
    paced_play(scene, Write(slope_expr), run_time=1.2)
    narration_wait(scene, 19.01)

    expand_expr = eq(r"=\frac{2xh+h^2}{h}", cfg.CYAN, cfg.FONT["body"]).next_to(slope_expr, DOWN, buff=0.35, aligned_edge=LEFT)
    paced_play(scene, Write(expand_expr), run_time=1.2)
    narration_wait(scene, 11.4)

    cancel_expr = eq(r"=2x+h", cfg.GOLD, cfg.FONT["title"]).next_to(expand_expr, DOWN, buff=0.4, aligned_edge=LEFT)
    paced_play(scene, Write(cancel_expr), run_time=1.1)
    narration_wait(scene, 11.4)

    live_readout = always_redraw(
        lambda: eq(rf"2x+h={2 * x0 + h_tracker.get_value():.3f}", cfg.GOLD, cfg.FONT["body"]).next_to(cancel_expr, DOWN, buff=0.4, aligned_edge=LEFT)
    )
    scene.add(live_readout)
    both_caption = bottom_caption("Watch both sides shrink h toward zero, together.", cfg.WHITE)
    paced_play(scene, FadeIn(both_caption), FadeIn(live_readout), run_time=0.8)

    for target_h in (0.5, 0.2, 0.08, 0.03, 0.01, 0.002):
        paced_play(scene, h_tracker.animate.set_value(target_h), run_time=3.1, rate_func=rate_functions.ease_in_out_sine)
        narration_wait(scene, 0.76)

    tangent = tangent_line(axes, square, d_square, x0, cfg.GREEN, half_length=1.7)
    paced_play(scene, FadeOut(VGroup(q_label)), FadeIn(tangent, scale=1.02), run_time=1.0)
    narration_wait(scene, 7.6)

    derivative = eq(r"\frac{d}{dx}x^2=2x", cfg.GREEN, cfg.FONT["hero"])
    derivative.move_to([4.0, -1.3, 0])
    paced_play(
        scene,
        FadeOut(both_caption),
        FadeOut(VGroup(slope_expr, expand_expr, cancel_expr, live_readout)),
        run_time=1.0,
    )
    paced_play(scene, Write(derivative), run_time=3.2)
    narration_wait(scene, 20.11)

    end_scene(scene, started, cfg.SCENE_DURATIONS["06"])
