"""Scene 01: distance is the area under a velocity graph — and a curved velocity asks a new question."""

from __future__ import annotations

import numpy as np
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
    outlined_text,
    paced_play,
    title_card,
)
from utils.math_utils import velocity_curve


def _perspective_road_hook() -> tuple[VGroup, VGroup]:
    """Build a cinematic 2.5D road and a rear-view car for the opening hook."""
    vanish = np.array([0.0, 1.15, 0.0])

    ground_left = Polygon(
        [-8.2, -4.7, 0],
        [-6.9, -3.25, 0],
        vanish,
        [-8.2, 1.5, 0],
        fill_color="#06223A",
        fill_opacity=0.95,
        stroke_width=0,
    )
    ground_right = ground_left.copy().flip(RIGHT)
    road = Polygon(
        [-6.9, -3.25, 0],
        [6.9, -3.25, 0],
        [0.78, 1.15, 0],
        [-0.78, 1.15, 0],
        fill_color="#09131E",
        fill_opacity=1,
        stroke_width=0,
    )
    left_edge = Line([-6.9, -3.25, 0], [-0.78, 1.15, 0], color=cfg.CYAN, stroke_width=5)
    right_edge = Line([6.9, -3.25, 0], [0.78, 1.15, 0], color=cfg.CYAN, stroke_width=5)

    lane_marks = VGroup(
        Polygon([-0.30, -2.95, 0], [0.30, -2.95, 0], [0.18, -1.95, 0], [-0.18, -1.95, 0], fill_color=cfg.GOLD, fill_opacity=0.9, stroke_width=0),
        Polygon([-0.14, -1.36, 0], [0.14, -1.36, 0], [0.09, -0.74, 0], [-0.09, -0.74, 0], fill_color=cfg.GOLD, fill_opacity=0.8, stroke_width=0),
        Polygon([-0.07, -0.28, 0], [0.07, -0.28, 0], [0.04, 0.10, 0], [-0.04, 0.10, 0], fill_color=cfg.GOLD, fill_opacity=0.68, stroke_width=0),
        Polygon([-0.032, 0.48, 0], [0.032, 0.48, 0], [0.018, 0.70, 0], [-0.018, 0.70, 0], fill_color=cfg.GOLD, fill_opacity=0.55, stroke_width=0),
    )

    skyline = VGroup()
    for x, width, height in ((-4.8, 0.7, 0.75), (-3.9, 0.5, 1.05), (-3.1, 0.8, 0.62), (3.2, 0.65, 0.82), (4.1, 0.52, 1.12), (5.0, 0.78, 0.7)):
        skyline.add(
            Rectangle(width=width, height=height, fill_color=cfg.PANEL_2, fill_opacity=0.85, stroke_width=0).move_to([x, 1.15 + height / 2, 0])
        )
    horizon_glow = Circle(radius=1.25, color=cfg.CYAN, stroke_width=0, fill_color=cfg.CYAN, fill_opacity=0.055).move_to(vanish)
    horizon = Line([-7.4, 1.15, 0], [7.4, 1.15, 0], color=cfg.BLUE, stroke_width=2, stroke_opacity=0.35)
    road_group = VGroup(horizon_glow, skyline, horizon, ground_left, ground_right, road, lane_marks, left_edge, right_edge)

    shadow = Ellipse(width=1.75, height=0.28, fill_color=BLACK, fill_opacity=0.52, stroke_width=0).shift(DOWN * 0.36)
    body = RoundedRectangle(width=1.7, height=0.72, corner_radius=0.16, color=cfg.CYAN, fill_color=cfg.BLUE, fill_opacity=0.92, stroke_width=3)
    rear_window = Polygon(
        [-0.58, 0.26, 0],
        [0.58, 0.26, 0],
        [0.40, 0.66, 0],
        [-0.40, 0.66, 0],
        color=cfg.CYAN,
        fill_color=cfg.PANEL,
        fill_opacity=0.96,
        stroke_width=2,
    )
    left_light = RoundedRectangle(width=0.34, height=0.16, corner_radius=0.04, color=cfg.RED, fill_color=cfg.RED, fill_opacity=0.95, stroke_width=0).shift(LEFT * 0.52 + DOWN * 0.13)
    right_light = left_light.copy().shift(RIGHT * 1.04)
    bumper = Line([-0.62, -0.29, 0], [0.62, -0.29, 0], color=cfg.WHITE, stroke_width=3)
    car = VGroup(shadow, body, rear_window, left_light, right_light, bumper).move_to([0, -2.45, 0])
    return road_group, car


class Scene01VelocityToDistance(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "01")
    add_cinematic_background(scene)

    # -- Beat 1: a car recedes into a perspective road ----------------------
    road, car = _perspective_road_hook()
    question = outlined_text("HOW FAR DID IT GO?", cfg.FONT["title"], cfg.GOLD, BOLD).to_edge(UP, buff=0.48)
    paced_play(scene, FadeIn(road, shift=UP * 0.08), FadeIn(car, shift=UP * 0.12), run_time=1.0)
    paced_play(
        scene,
        car.animate.move_to([0, 0.72, 0]).scale(0.20),
        run_time=5.0,
        rate_func=rate_functions.ease_out_sine,
    )
    paced_play(scene, FadeIn(question, shift=DOWN * 0.2), run_time=0.9)
    narration_wait(scene, 8.51)
    paced_play(scene, FadeOut(VGroup(road, car, question)), run_time=0.8)

    # -- Beat 2: constant velocity, a rectangle of area ----------------------
    axes = calc_axes(x_range=(0, 6, 1), y_range=(0, 30, 10), x_length=10.8, y_length=5.0).move_to([0, -0.35, 0])
    axes.x_axis.set_stroke(width=3.2)
    axes.y_axis.set_stroke(width=3.2)
    # Keep the labels outside the fillable plot region.  In particular, the
    # changing-velocity area reaches t=6, so an inset t would lose contrast.
    t_label = eq("t", cfg.CYAN, cfg.FONT["section"]).next_to(axes.x_axis.get_right(), RIGHT, buff=0.22).shift(DOWN * 0.10)
    v_label = eq("v(t)", cfg.CYAN, cfg.FONT["section"]).next_to(axes.y_axis.get_top(), LEFT, buff=0.22).shift(UP * 0.02)
    labels = VGroup(t_label, v_label)
    paced_play(scene, Create(axes), FadeIn(labels), run_time=1.2)

    flat_curve = axes.plot(lambda t: 20.0, x_range=[0, 5], color=cfg.WHITE, stroke_width=6)
    flat_label = eq("v=20\\text{ m/s}", cfg.WHITE, cfg.FONT["body"]).move_to(axes.c2p(1.25, 23.6))
    paced_play(scene, Create(flat_curve), FadeIn(flat_label), run_time=1.1)
    narration_wait(scene, 6.17)

    rectangle = area_region(axes, flat_curve, 0, 5, cfg.CYAN, 0.5)
    paced_play(scene, FadeIn(rectangle), run_time=2.8, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 1.90)

    product = eq("20\\times5=100", cfg.GOLD, cfg.FONT["section"]).next_to(axes, DOWN, buff=0.35)
    paced_play(scene, Write(product), run_time=1.2)
    narration_wait(scene, 4.94)

    reveal = bottom_caption("Distance = area under the velocity graph.", cfg.GOLD)
    paced_play(scene, FadeOut(product), FadeIn(reveal), run_time=0.9)
    narration_wait(scene, 8.64)
    paced_play(scene, FadeOut(reveal), run_time=0.6)

    # -- Beat 3: let the speed change continuously ---------------------------
    curved_curve = axes.plot(velocity_curve, x_range=[0, 6], color=cfg.CYAN, stroke_width=6)
    curved_area = area_region(axes, curved_curve, 0, 6, cfg.CYAN, 0.35)
    paced_play(
        scene,
        FadeOut(rectangle),
        ReplacementTransform(flat_curve, curved_curve),
        FadeOut(flat_label),
        run_time=3.5,
        rate_func=rate_functions.ease_in_out_sine,
    )
    paced_play(scene, FadeIn(curved_area), run_time=2.5, rate_func=rate_functions.ease_in_out_sine)
    narration_wait(scene, 1.44)

    question2 = bottom_caption("If speed changes every instant, what is the distance now?", cfg.WHITE)
    paced_play(scene, FadeIn(question2), run_time=0.9)
    narration_wait(scene, 11.11)

    lead_in = eq(r"\text{distance} = \int_0^6 v(t)\,dt \; ?", cfg.PURPLE, cfg.FONT["title"])
    lead_in.next_to(axes, UP, buff=0.35)
    paced_play(scene, FadeOut(question2), FadeIn(lead_in, shift=UP * 0.1), run_time=2.0)
    narration_wait(scene, 7.74)

    # The title is the payoff to the hook, not an interruption inside it.
    paced_play(scene, FadeOut(VGroup(axes, labels, curved_curve, curved_area, lead_in)), run_time=0.7)
    heading = title_card("VISUAL CALCULUS", "Part Two — From Derivatives to Integrals", cfg.GOLD)
    paced_play(scene, FadeIn(heading, shift=UP * 0.15), run_time=1.5)
    narration_wait(scene, 8.14)

    end_scene(scene, started, cfg.SCENE_DURATIONS["01"])
