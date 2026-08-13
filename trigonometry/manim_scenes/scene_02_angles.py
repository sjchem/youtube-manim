"""Scene 02: angles are amounts of rotation; radians measure arc in radii."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)
from utils.math_utils import point_on_circle


class Scene02Angles(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "02")
    add_cinematic_background(scene)

    tag = section_tag("02", "Follow the turning ray")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    center = np.array([-3.6, -0.15, 0.0])
    radius = 2.35
    circle = Circle(radius=radius, color=cfg.MUTED, stroke_width=3).move_to(center)
    fixed_ray = Line(center, center + RIGHT * radius, color=cfg.GREEN, stroke_width=6)
    theta = ValueTracker(0.001)
    moving_ray = always_redraw(
        lambda: Line(center, point_on_circle(theta.get_value(), radius, center), color=cfg.GOLD, stroke_width=6)
    )
    point = always_redraw(lambda: glow_dot(point_on_circle(theta.get_value(), radius, center), cfg.GOLD, 0.085))
    arc = always_redraw(
        lambda: Arc(radius=0.72, start_angle=0, angle=theta.get_value(), arc_center=center, color=cfg.GOLD, stroke_width=6)
    )
    degrees = DecimalNumber(
        theta.get_value() * 180 / PI,
        num_decimal_places=0,
        font_size=cfg.FONT["section"],
        color=cfg.GOLD,
    ).move_to([2.9, 0.0, 0])
    degrees.add_updater(lambda mob: mob.set_value(theta.get_value() * 180 / PI))
    degree_symbol = MathTex(r"{}^\circ", font_size=cfg.FONT["body"], color=cfg.GOLD)
    degree_symbol.add_updater(
        lambda mob: mob.next_to(degrees, RIGHT, buff=0.04).align_to(degrees, UP).shift(DOWN * 0.03)
    )

    paced_play(scene, FadeOut(tag), Create(circle), Create(fixed_ray), run_time=1.2)
    scene.add(arc, moving_ray, point, degrees, degree_symbol)
    turn_caption = bottom_caption("The angle records how far the ray has turned")
    paced_play(scene, FadeIn(turn_caption), run_time=0.6)
    for value, seconds in ((PI / 2, 3.2), (PI, 3.2), (3 * PI / 2, 3.2), (TAU, 4.0)):
        paced_play(scene, theta.animate.set_value(value), run_time=seconds, rate_func=smooth)
        narration_wait(scene, 0.8)
    full_turn = eq(r"1\ \mathrm{turn}=360^\circ", cfg.WHITE, cfg.FONT["section"]).move_to([3.1, 1.2, 0])
    paced_play(scene, Write(full_turn), run_time=1.0)

    # Six equal sectors are a visual partition, not an origin story for 360.
    sectors = VGroup()
    for index in range(6):
        a = index * TAU / 6
        b = (index + 1) * TAU / 6
        sectors.add(
            Polygon(
                center,
                point_on_circle(a, radius, center),
                point_on_circle(b, radius, center),
                color=cfg.CYAN,
                stroke_width=2,
                fill_color=cfg.CYAN,
                fill_opacity=0.04 + 0.015 * (index % 2),
            )
        )
    paced_play(scene, LaggedStart(*[FadeIn(s) for s in sectors], lag_ratio=0.12), run_time=1.8)
    sixty = eq(r"6\times60^\circ=360^\circ", cfg.CYAN, cfg.FONT["body"]).next_to(full_turn, DOWN, buff=0.35)
    paced_play(scene, Write(sixty), run_time=0.9)
    narration_wait(scene, 2.0)

    paced_play(scene, FadeOut(VGroup(sectors, full_turn, sixty, degrees, degree_symbol, arc, moving_ray, point, fixed_ray, circle, turn_caption)), run_time=0.9)

    # Radian construction.
    rad_center = np.array([-3.2, -0.2, 0.0])
    rad_radius = 2.05
    rad_circle = Circle(radius=rad_radius, color=cfg.CYAN, stroke_width=5).move_to(rad_center)
    radius_segment = Line(rad_center, rad_center + RIGHT * rad_radius, color=cfg.GOLD, stroke_width=7)
    radius_label = eq("r", cfg.GOLD, cfg.FONT["section"]).next_to(radius_segment, DOWN, buff=0.16)
    one_rad_arc = Arc(radius=rad_radius, start_angle=0, angle=1.0, arc_center=rad_center, color=cfg.GOLD, stroke_width=8)
    arc_label = outlined_text("arc length = r", cfg.FONT["body"], cfg.GOLD, BOLD).next_to(one_rad_arc, RIGHT, buff=0.35)
    radian_label = eq(r"\theta=1\ \mathrm{radian}", cfg.WHITE, cfg.FONT["section"]).move_to([3.2, 1.25, 0])

    paced_play(scene, Create(rad_circle), GrowFromPoint(radius_segment, rad_center), FadeIn(radius_label), run_time=1.5)
    radius_copy = radius_segment.copy()
    scene.add(radius_copy)
    paced_play(scene, ReplacementTransform(radius_copy, one_rad_arc), run_time=1.8)
    paced_play(scene, FadeIn(arc_label), Write(radian_label), run_time=1.0)
    narration_wait(scene, 2.2)

    circumference = eq(r"\text{full arc}=2\pi r", cfg.CYAN, cfg.FONT["section"]).move_to([3.2, -0.2, 0])
    divide = eq(r"\frac{2\pi r}{r}=2\pi\ \mathrm{radians}", cfg.GREEN, cfg.FONT["section"]).next_to(circumference, DOWN, buff=0.45)
    paced_play(scene, Write(circumference), run_time=1.0)
    paced_play(scene, TransformFromCopy(VGroup(circumference, radius_label), divide), run_time=1.2)
    bridge = eq(r"360^\circ=2\pi\ \mathrm{rad}", cfg.GOLD, cfg.FONT["section"]).next_to(divide, DOWN, buff=0.42)
    paced_play(scene, Write(bridge), run_time=1.0)
    narration_wait(scene, 2.0)

    takeaway = bottom_caption("Degrees count slices. Radians measure arc with the radius.", cfg.WHITE)
    paced_play(scene, FadeIn(takeaway, shift=UP * 0.12), run_time=0.7)
    paced_play(scene, Indicate(one_rad_arc, color=cfg.WHITE), Indicate(radius_segment, color=cfg.WHITE), run_time=1.4)
    narration_wait(scene, 2.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["02"])
