"""Scene 03: Cartesian coordinates and Pythagoras prepare the triangle language."""

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


class Scene03CoordinatesPythagoras(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "03")
    add_cinematic_background(scene)
    tag = section_tag("03", "Give every point an address")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    axes = Axes(
        x_range=[-5, 5, 1],
        y_range=[-3, 3, 1],
        x_length=10.8,
        y_length=6.0,
        tips=True,
        axis_config={"color": cfg.MUTED, "stroke_width": 3},
    ).move_to(DOWN * 0.15)
    x_name = outlined_text("x  ·  horizontal", cfg.FONT["small"], cfg.GREEN, BOLD).next_to(axes.x_axis, DOWN, buff=0.2).to_edge(RIGHT, buff=0.6)
    y_name = outlined_text("y  ·  vertical", cfg.FONT["small"], cfg.CYAN, BOLD).next_to(axes.y_axis, LEFT, buff=0.2).to_edge(UP, buff=0.55)
    paced_play(scene, FadeOut(tag), Create(axes), FadeIn(x_name), FadeIn(y_name), run_time=1.6)

    x = ValueTracker(3.0)
    y = ValueTracker(2.0)
    point = always_redraw(lambda: glow_dot(axes.c2p(x.get_value(), y.get_value()), cfg.GOLD, 0.1))
    horizontal = always_redraw(
        lambda: Line(axes.c2p(0, y.get_value()), axes.c2p(x.get_value(), y.get_value()), color=cfg.GREEN, stroke_width=7)
    )
    vertical = always_redraw(
        lambda: Line(axes.c2p(x.get_value(), 0), axes.c2p(x.get_value(), y.get_value()), color=cfg.CYAN, stroke_width=7)
    )
    coordinate = always_redraw(
        lambda: eq(
            rf"({x.get_value():.0f},\,{y.get_value():.0f})",
            cfg.GOLD,
            cfg.FONT["section"],
        ).next_to(axes.c2p(x.get_value(), y.get_value()), UR, buff=0.18)
    )
    scene.add(horizontal, vertical, point, coordinate)
    quadrant_label = outlined_text("QUADRANT I", cfg.FONT["body"], cfg.WHITE, BOLD).to_corner(UR, buff=0.45)
    paced_play(scene, FadeIn(quadrant_label), run_time=0.7)

    positions = (
        (-3.0, 2.0, "QUADRANT II"),
        (-3.0, -2.0, "QUADRANT III"),
        (3.0, -2.0, "QUADRANT IV"),
        (3.0, 2.0, "QUADRANT I"),
    )
    for next_x, next_y, name in positions:
        next_label = outlined_text(name, cfg.FONT["body"], cfg.WHITE, BOLD).move_to(quadrant_label)
        paced_play(
            scene,
            x.animate.set_value(next_x),
            y.animate.set_value(next_y),
            ReplacementTransform(quadrant_label, next_label),
            run_time=3.2,
            rate_func=smooth,
        )
        quadrant_label = next_label
        narration_wait(scene, 0.55)

    signs = VGroup(
        outlined_text("I   (+,+)", cfg.FONT["small"], cfg.GOLD, BOLD),
        outlined_text("II  (−,+)", cfg.FONT["small"], cfg.CYAN, BOLD),
        outlined_text("III (−,−)", cfg.FONT["small"], cfg.PURPLE, BOLD),
        outlined_text("IV  (+,−)", cfg.FONT["small"], cfg.GREEN, BOLD),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(UR, buff=0.42)
    paced_play(scene, ReplacementTransform(quadrant_label, signs), run_time=1.0)
    narration_wait(scene, 1.5)

    paced_play(scene, FadeOut(VGroup(axes, x_name, y_name, horizontal, vertical, point, coordinate, signs)), run_time=0.9)

    # A 3-4-5 triangle and three area squares make Pythagoras visible.
    a = 3.0
    b = 4.0
    scale = 0.78
    p0 = np.array([-3.8, -2.2, 0.0])
    p1 = p0 + RIGHT * b * scale
    p2 = p1 + UP * a * scale
    triangle = Polygon(p0, p1, p2, color=cfg.WHITE, stroke_width=7, fill_color=cfg.PANEL, fill_opacity=0.35)
    right = Square(side_length=0.25, color=cfg.GOLD, stroke_width=3).move_to(p1 + LEFT * 0.125 + UP * 0.125)
    base_label = eq("4", cfg.GREEN, cfg.FONT["section"]).next_to(Line(p0, p1), DOWN, buff=0.15)
    side_label = eq("3", cfg.CYAN, cfg.FONT["section"]).next_to(Line(p1, p2), RIGHT, buff=0.15)
    hyp_label = eq("5", cfg.WHITE, cfg.FONT["section"]).move_to((p0 + p2) / 2 + UL * 0.35)
    paced_play(scene, Create(triangle), FadeIn(right), FadeIn(base_label), FadeIn(side_label), FadeIn(hyp_label), run_time=1.8)

    squares = VGroup(
        Square(side_length=1.45, color=cfg.CYAN, fill_color=cfg.CYAN, fill_opacity=0.12).move_to([-4.9, 0.5, 0]),
        Square(side_length=1.9, color=cfg.GREEN, fill_color=cfg.GREEN, fill_opacity=0.12).move_to([-2.75, 1.0, 0]),
        Square(side_length=2.35, color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=0.1).move_to([3.2, 0.1, 0]),
    )
    areas = VGroup(
        eq("9", cfg.CYAN, cfg.FONT["hero"]).move_to(squares[0]),
        eq("16", cfg.GREEN, cfg.FONT["hero"]).move_to(squares[1]),
        eq("25", cfg.GOLD, cfg.FONT["hero"]).move_to(squares[2]),
    )
    paced_play(scene, LaggedStart(*[GrowFromCenter(square) for square in squares], lag_ratio=0.2), run_time=2.2)
    paced_play(scene, LaggedStart(*[FadeIn(area, scale=1.2) for area in areas], lag_ratio=0.25), run_time=1.4)
    plus = eq("9+16=25", cfg.WHITE, cfg.FONT["hero"]).to_edge(UP, buff=0.45)
    paced_play(scene, TransformFromCopy(areas, plus), run_time=1.4)
    narration_wait(scene, 1.6)

    theorem_name = outlined_text("PYTHAGOREAN THEOREM", cfg.FONT["body"], cfg.GOLD, BOLD).to_edge(UP, buff=0.35)
    general = eq(r"a^2+b^2=c^2", cfg.WHITE, cfg.FONT["hero"]).next_to(theorem_name, DOWN, buff=0.18)
    general.set_color_by_tex("a", cfg.CYAN)
    general.set_color_by_tex("b", cfg.GREEN)
    general.set_color_by_tex("c", cfg.GOLD)
    paced_play(
        scene,
        ReplacementTransform(plus, general),
        FadeIn(theorem_name, shift=DOWN * 0.1),
        run_time=1.2,
    )
    takeaway = bottom_caption("Coordinates create lengths. The Pythagorean theorem connects them.", cfg.WHITE)
    paced_play(scene, FadeIn(takeaway), Indicate(general, color=cfg.GOLD), run_time=1.2)
    narration_wait(scene, 2.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["03"])
