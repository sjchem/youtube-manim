"""Scene 07: setting the hypotenuse to one builds the unit-circle bridge."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    color_formula_parts,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)
from utils.math_utils import point_on_circle


class Scene07UnitCircle(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "07")
    add_cinematic_background(scene)
    tag = section_tag("07", "Make the hypotenuse one")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    center = np.array([-2.7, -0.3, 0.0])
    radius = 2.6
    theta = ValueTracker(np.arctan2(3, 4))
    endpoint = point_on_circle(theta.get_value(), radius, center)
    triangle = VGroup(
        Line(center, [endpoint[0], center[1], 0], color=cfg.GREEN, stroke_width=7),
        Line([endpoint[0], center[1], 0], endpoint, color=cfg.CYAN, stroke_width=7),
        Line(center, endpoint, color=cfg.WHITE, stroke_width=7),
    )
    labels = VGroup(
        eq(r"\frac45", cfg.GREEN, cfg.FONT["section"]).next_to(triangle[0], DOWN, buff=0.16),
        eq(r"\frac35", cfg.CYAN, cfg.FONT["section"]).next_to(triangle[1], RIGHT, buff=0.16),
        eq("1", cfg.WHITE, cfg.FONT["section"]).next_to(triangle[2], LEFT, buff=0.18),
    )
    paced_play(
        scene,
        FadeOut(tag),
        Create(triangle),
        LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.2),
        run_time=1.8,
    )
    one = outlined_text("hypotenuse = 1", cfg.FONT["body"], cfg.GOLD, BOLD).move_to([3.25, 1.5, 0])
    paced_play(scene, FadeIn(one), run_time=0.8)
    narration_wait(scene, 1.7)

    circle = Circle(radius=radius, color=cfg.CYAN, stroke_width=5).move_to(center)
    point = glow_dot(endpoint, cfg.GOLD, 0.1)
    paced_play(scene, Create(circle), FadeIn(point), run_time=1.8)
    unit_name = outlined_text("UNIT CIRCLE", cfg.FONT["section"], cfg.CYAN, BOLD).move_to([3.25, 0.6, 0])
    paced_play(scene, Write(unit_name), run_time=0.9)

    mapping = VGroup(
        color_formula_parts(eq(r"x=\cos\theta", cfg.WHITE, cfg.FONT["section"])),
        color_formula_parts(eq(r"y=\sin\theta", cfg.WHITE, cfg.FONT["section"])),
    ).arrange(DOWN, buff=0.38).move_to([3.25, -0.75, 0])
    paced_play(scene, ReplacementTransform(labels[0].copy(), mapping[0]), ReplacementTransform(labels[1].copy(), mapping[1]), run_time=1.5)
    narration_wait(scene, 2.0)

    paced_play(scene, FadeOut(VGroup(one, unit_name, labels, point, triangle, mapping)), run_time=0.8)

    # Dynamic coordinates across all four quadrants.
    axes = Axes(
        x_range=[-1.25, 1.25, 1],
        y_range=[-1.25, 1.25, 1],
        x_length=5.2,
        y_length=5.2,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2.5},
    ).move_to(center)
    unit_circle = Circle(radius=2.08, color=cfg.WHITE, stroke_width=4).move_to(axes.c2p(0, 0))
    theta.set_value(PI / 4)
    moving_point = always_redraw(lambda: glow_dot(axes.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())), cfg.GOLD, 0.09))
    radius_line = always_redraw(lambda: Line(axes.c2p(0, 0), axes.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())), color=cfg.WHITE, stroke_width=6))
    x_projection = always_redraw(lambda: Line(axes.c2p(0, 0), axes.c2p(np.cos(theta.get_value()), 0), color=cfg.GREEN, stroke_width=8))
    y_projection = always_redraw(lambda: Line(axes.c2p(np.cos(theta.get_value()), 0), axes.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())), color=cfg.CYAN, stroke_width=8))
    angle_arc = always_redraw(lambda: Arc(radius=0.55, start_angle=0, angle=theta.get_value(), arc_center=axes.c2p(0, 0), color=cfg.GOLD, stroke_width=5))
    x_number = DecimalNumber(np.cos(theta.get_value()), num_decimal_places=2, font_size=cfg.FONT["section"], color=cfg.GREEN)
    y_number = DecimalNumber(np.sin(theta.get_value()), num_decimal_places=2, font_size=cfg.FONT["section"], color=cfg.CYAN)
    x_number.add_updater(lambda mob: mob.set_value(np.cos(theta.get_value())))
    y_number.add_updater(lambda mob: mob.set_value(np.sin(theta.get_value())))
    coordinate_panel = VGroup(
        outlined_text("cos θ =", cfg.FONT["body"], cfg.GREEN, BOLD), x_number,
        outlined_text("sin θ =", cfg.FONT["body"], cfg.CYAN, BOLD), y_number,
    ).arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.38)).move_to([3.25, 0.8, 0])
    scene.add(axes, unit_circle, radius_line, x_projection, y_projection, angle_arc, moving_point)
    paced_play(scene, FadeIn(coordinate_panel), run_time=0.8)
    for value in (3 * PI / 4, 5 * PI / 4, 7 * PI / 4, 9 * PI / 4):
        paced_play(scene, theta.animate.set_value(value), run_time=5.0, rate_func=linear)
        narration_wait(scene, 0.8)

    all_angles = bottom_caption("The circle keeps sine and cosine meaningful for every angle.", cfg.GOLD)
    paced_play(scene, FadeIn(all_angles), run_time=0.7)
    narration_wait(scene, 2.0)

    paced_play(scene, FadeOut(VGroup(coordinate_panel, all_angles)), run_time=0.6)
    theta.set_value(np.arctan2(3, 4))
    identity = color_formula_parts(eq(r"\cos^2\theta+\sin^2\theta=1", cfg.WHITE, cfg.FONT["hero"]))
    identity.move_to([3.65, 0.6, 0])
    pythagoras = eq(r"x^2+y^2=1", cfg.MUTED, cfg.FONT["section"]).next_to(identity, DOWN, buff=0.55)
    paced_play(scene, Write(pythagoras), run_time=1.0)
    paced_play(scene, TransformFromCopy(pythagoras, identity), run_time=1.4)
    areas = VGroup(
        eq(r"\left(\frac45\right)^2", cfg.GREEN, cfg.FONT["body"]),
        eq("+", cfg.WHITE, cfg.FONT["body"]),
        eq(r"\left(\frac35\right)^2", cfg.CYAN, cfg.FONT["body"]),
        eq("=1", cfg.GOLD, cfg.FONT["body"]),
    ).arrange(RIGHT, buff=0.2).next_to(pythagoras, DOWN, buff=0.5)
    paced_play(scene, LaggedStart(*[FadeIn(item, shift=UP * 0.1) for item in areas], lag_ratio=0.2), run_time=1.3)
    conclusion = bottom_caption("The famous identity is simply Pythagoras on a circle of radius one.", cfg.WHITE)
    paced_play(scene, FadeIn(conclusion), run_time=0.8)
    paced_play(scene, Indicate(identity, color=cfg.GOLD, scale_factor=1.04), run_time=1.4)
    narration_wait(scene, 2.5)
    end_scene(scene, started, cfg.SCENE_DURATIONS["07"])
