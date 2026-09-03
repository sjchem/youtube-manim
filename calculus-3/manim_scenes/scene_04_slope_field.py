"""Scene 04: fill the plane with directions, then let curves flow through them."""

from __future__ import annotations

import numpy as np
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
    fitted_eq,
    glow_dot,
    narration_wait,
    paced_play,
    slope_field,
    solution_curve,
    top_caption,
)
from utils.math_utils import exponential_solution, self_slope

X_SPAN = (-2.8, 2.8, 0.4)
Y_SPAN = (-2.8, 2.8, 0.4)
Y_CLIP = (-3.0, 3.0)
# Solutions of dy/dx = y climb by a factor of e every unit of x, so a seed of
# any decent size leaves the top of the window almost immediately and every
# curve bunches into the left edge.  These heights are chosen so the family
# fans out and reaches the clip at five different places across the panel.
SEEDS = (
    (-2.7, 0.018, cfg.GREEN),
    (-2.7, 0.075, cfg.GOLD),
    (-2.7, 0.300, cfg.PURPLE),
    (-2.7, -0.045, cfg.ORANGE),
    (-2.7, -0.190, cfg.RED),
)


class Scene04SlopeField(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "04")
    add_cinematic_background(scene)

    equation = fitted_eq(r"\frac{dy}{dx}=y", cfg.WHITE, cfg.FONT["section"], width=3.0)
    equation.to_corner(UL, buff=0.55)
    # The plot sits left of centre so the band annotations have their own
    # column on the right and never reach past the frame edge.
    axes = calc_axes((-3, 3, 1), (-3, 3, 1), 9.4, 5.5).move_to([-0.75, -0.25, 0])
    x_label = eq("x", cfg.WHITE, cfg.FONT["hero"]).next_to(axes.x_axis.get_right(), RIGHT, buff=0.34).shift(DOWN * 0.16)
    y_label = eq("y", cfg.WHITE, cfg.FONT["hero"]).next_to(axes.y_axis.get_top(), UP, buff=0.30)
    axis_labels = VGroup(x_label, y_label)
    paced_play(scene, FadeIn(equation), Create(axes), FadeIn(axis_labels), run_time=1.2)
    narration_wait(scene, 4.8)

    # -- Beat 1: the field appears one horizontal band at a time --------------
    rows = slope_field(axes, self_slope, X_SPAN, Y_SPAN, half_length=0.18)
    field = VGroup(*rows)
    caption = bottom_caption("Every point gets one tiny arrow: the slope allowed there.", cfg.CYAN)
    paced_play(scene, FadeIn(caption), run_time=0.7)
    paced_play(scene, LaggedStart(*(FadeIn(row, shift=UP * 0.06) for row in rows), lag_ratio=0.42), run_time=6.4)
    narration_wait(scene, 6.4)

    flat_band = rows[len(rows) // 2]
    flat_note = eq(r"\text{almost flat}", cfg.CYAN, cfg.FONT["section"])
    flat_note.next_to(axes.c2p(3.0, 0.0), RIGHT, buff=0.42).shift(UP * 0.52)
    paced_play(scene, FadeOut(caption), field.animate.set_stroke(opacity=0.22), run_time=0.8)
    paced_play(scene, flat_band.animate.set_color(cfg.CYAN).set_stroke(opacity=1.0, width=7), FadeIn(flat_note), run_time=1.1)
    narration_wait(scene, 5.4)

    steep_band = rows[-2]
    steep_note = eq(r"\text{steeper up}", cfg.GOLD, cfg.FONT["section"])
    steep_note.next_to(axes.c2p(3.0, 2.4), RIGHT, buff=0.42)
    paced_play(scene, steep_band.animate.set_color(cfg.GOLD).set_stroke(opacity=1.0, width=7), FadeIn(steep_note), run_time=1.1)
    narration_wait(scene, 5.6)

    down_band = rows[1]
    down_note = eq(r"\text{steeper down}", cfg.ORANGE, cfg.FONT["section"])
    down_note.next_to(axes.c2p(3.0, -2.4), RIGHT, buff=0.42)
    paced_play(scene, down_band.animate.set_color(cfg.ORANGE).set_stroke(opacity=1.0, width=7), FadeIn(down_note), run_time=1.1)
    narration_wait(scene, 5.8)

    paced_play(
        scene,
        FadeOut(VGroup(flat_note, steep_note, down_note)),
        field.animate.set_stroke(opacity=0.55, width=3.4),
        run_time=1.0,
    )

    # -- Beat 2: drop one particle and let the field steer it -----------------
    x0, y0, colour = SEEDS[0]
    constant = y0 / np.exp(x0)
    first_curve = solution_curve(axes, lambda x: exponential_solution(x, constant), x0, 2.9, colour, 7, Y_CLIP)
    rider = glow_dot(axes.c2p(x0, y0), colour, 0.10)
    drop_caption = bottom_caption("Drop a point in, and just follow the arrows.", cfg.GOLD)
    paced_play(scene, FadeIn(rider, scale=1.5), FadeIn(drop_caption), run_time=0.9)
    narration_wait(scene, 4.6)
    paced_play(scene, MoveAlongPath(rider, first_curve), Create(first_curve), run_time=6.0, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 5.8)
    paced_play(scene, FadeOut(drop_caption), FadeOut(rider), run_time=0.6)

    # -- Beat 3: many starting points, one family -----------------------------
    family = VGroup(first_curve)
    more_caption = bottom_caption("Start anywhere else, and a whole family appears.", cfg.CYAN)
    paced_play(scene, FadeIn(more_caption), run_time=0.7)
    animations = []
    for start_x, start_y, colour in SEEDS[1:]:
        constant = start_y / np.exp(start_x)
        curve = solution_curve(axes, lambda x, c=constant: exponential_solution(x, c), start_x, 2.9, colour, 6, Y_CLIP)
        family.add(curve)
        animations.append(Create(curve))
    paced_play(scene, LaggedStart(*animations, lag_ratio=0.35), run_time=5.4)
    narration_wait(scene, 6.6)

    equilibrium = Line(axes.c2p(-2.9, 0), axes.c2p(2.9, 0), color=cfg.GREEN, stroke_width=7)
    equilibrium_tag = eq("y=0", cfg.GREEN, cfg.FONT["title"]).next_to(axes.c2p(-2.9, 0), LEFT, buff=0.30)
    paced_play(scene, Create(equilibrium), FadeIn(equilibrium_tag), run_time=1.0)
    narration_wait(scene, 5.8)
    family.add(equilibrium)

    # -- Beat 4: only now, the formula ----------------------------------------
    paced_play(scene, FadeOut(more_caption), run_time=0.5)
    solution = equation_card(r"y=Ce^{x}", cfg.GREEN, cfg.FONT["title"]).to_edge(DOWN, buff=0.34)
    paced_play(scene, FadeIn(solution, scale=1.06), run_time=1.5)
    narration_wait(scene, 6.8)

    metaphor = top_caption("a wind field, telling curves which way to flow", cfg.PURPLE)
    paced_play(scene, FadeOut(equation), FadeIn(metaphor, shift=DOWN * 0.12), run_time=1.0)
    narration_wait(scene, 6.2)

    end_scene(scene, started, cfg.SCENE_DURATIONS["04"])
