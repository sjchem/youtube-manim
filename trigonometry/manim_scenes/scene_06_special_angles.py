"""Scene 06: derive exact 30, 45, 60, and 90 degree values visually."""

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


class Scene06SpecialAngles(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "06")
    add_cinematic_background(scene)
    tag = section_tag("06", "Build the special angles")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    # A square cut diagonally creates a 45-45-90 triangle.
    square = Square(side_length=4.0, color=cfg.GREEN, stroke_width=6, fill_color=cfg.GREEN, fill_opacity=0.08).move_to([-3.1, -0.1, 0])
    diagonal = Line(square.get_corner(DL), square.get_corner(UR), color=cfg.GOLD, stroke_width=7)
    side_labels = VGroup(
        eq("1", cfg.GREEN, cfg.FONT["section"]).next_to(square, DOWN, buff=0.15),
        eq("1", cfg.CYAN, cfg.FONT["section"]).next_to(square, LEFT, buff=0.15),
    )
    paced_play(scene, FadeOut(tag), Create(square), FadeIn(side_labels), run_time=1.4)
    paced_play(scene, Create(diagonal), run_time=1.3)
    angle_marks = VGroup(
        eq(r"45^\circ", cfg.GOLD, cfg.FONT["body"]).move_to(square.get_corner(DL) + np.array([0.78, 0.34, 0])),
        eq(r"45^\circ", cfg.GOLD, cfg.FONT["body"]).move_to(square.get_corner(UR) + np.array([-0.34, -0.78, 0])),
    )
    angle_marks.set_stroke(cfg.BG, width=5, opacity=0.95, background=True)
    paced_play(scene, FadeIn(angle_marks), run_time=0.9)
    pythag = eq(r"1^2+1^2=c^2", cfg.WHITE, cfg.FONT["section"]).move_to([3.45, 1.55, 0])
    result = eq(r"c=\sqrt2", cfg.GOLD, cfg.FONT["hero"]).next_to(pythag, DOWN, buff=0.32)
    paced_play(scene, Write(pythag), run_time=1.2)
    paced_play(scene, TransformFromCopy(VGroup(diagonal, pythag), result), run_time=1.3)
    values45 = VGroup(
        eq(r"\sin45^\circ=\frac1{\sqrt2}=\frac{\sqrt2}{2}", cfg.CYAN, cfg.FONT["body"]),
        eq(r"\cos45^\circ=\frac1{\sqrt2}=\frac{\sqrt2}{2}", cfg.GREEN, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.38).move_to([3.4, -1.45, 0])
    paced_play(scene, LaggedStart(*[Write(item) for item in values45], lag_ratio=0.28), run_time=1.8)
    narration_wait(scene, 1.8)

    paced_play(scene, FadeOut(VGroup(square, diagonal, side_labels, angle_marks, pythag, result, values45)), run_time=0.9)

    # Split an equilateral triangle and let every narrated fact appear on it.
    left = np.array([-6.0, -2.05, 0.0])
    right = np.array([-1.8, -2.05, 0.0])
    foot = np.array([-3.9, -2.05, 0.0])
    top = np.array([-3.9, 1.59, 0.0])
    equilateral = Polygon(
        left,
        right,
        top,
        color=cfg.WHITE,
        stroke_width=7,
        fill_color=cfg.PANEL,
        fill_opacity=0.4,
    )
    base_two = eq("2", cfg.WHITE, cfg.FONT["section"]).next_to(Line(left, right), DOWN, buff=0.15)
    side_twos = VGroup(
        eq("2", cfg.WHITE, cfg.FONT["section"]).move_to((left + top) / 2 + UL * 0.22),
        eq("2", cfg.WHITE, cfg.FONT["section"]).move_to((right + top) / 2 + UR * 0.22),
    )
    sixty_left = eq(r"60^\circ", cfg.GOLD, cfg.FONT["label"]).move_to(left + np.array([0.73, 0.34, 0]))
    sixty_right = eq(r"60^\circ", cfg.GOLD, cfg.FONT["label"]).move_to(right + np.array([-0.73, 0.34, 0]))
    sixty_top = eq(r"60^\circ", cfg.GOLD, cfg.FONT["label"]).move_to(top + DOWN * 0.55)
    initial_angles = VGroup(sixty_left, sixty_right, sixty_top)
    initial_angles.set_stroke(cfg.BG, width=5, opacity=0.95, background=True)
    paced_play(
        scene,
        Create(equilateral),
        FadeIn(base_two),
        FadeIn(side_twos),
        LaggedStart(*[FadeIn(angle) for angle in initial_angles], lag_ratio=0.18),
        run_time=1.6,
    )

    altitude = DashedLine(top, foot, color=cfg.CYAN, stroke_width=6, dash_length=0.16)
    right_angle = Polygon(
        foot,
        foot + LEFT * 0.28,
        foot + LEFT * 0.28 + UP * 0.28,
        foot + UP * 0.28,
        color=cfg.GOLD,
        stroke_width=3,
        fill_opacity=0,
    )
    one_left = eq("1", cfg.GREEN, cfg.FONT["section"]).move_to([-4.95, -2.43, 0])
    one_right = eq("1", cfg.GREEN, cfg.FONT["section"]).move_to([-2.85, -2.43, 0])
    paced_play(
        scene,
        Create(altitude),
        FadeIn(right_angle),
        ReplacementTransform(base_two, VGroup(one_left, one_right)),
        run_time=1.2,
    )

    thirty_left = eq(r"30^\circ", cfg.GOLD, cfg.FONT["label"]).move_to(top + np.array([-0.57, -0.72, 0]))
    thirty_right = eq(r"30^\circ", cfg.GOLD, cfg.FONT["label"]).move_to(top + np.array([0.57, -0.72, 0]))
    ninety = eq(r"90^\circ", cfg.GOLD, cfg.FONT["label"]).move_to(foot + np.array([-0.53, 0.38, 0]))
    thirty_angles = VGroup(thirty_left, thirty_right, ninety)
    thirty_angles.set_stroke(cfg.BG, width=5, opacity=0.95, background=True)
    chosen_triangle = Polygon(
        left,
        foot,
        top,
        color=cfg.CYAN,
        stroke_width=4,
        fill_color=cfg.CYAN,
        fill_opacity=0.12,
    )
    paced_play(
        scene,
        ReplacementTransform(sixty_top, thirty_left),
        FadeIn(thirty_right),
        FadeIn(ninety),
        FadeIn(chosen_triangle),
        run_time=1.3,
    )

    height_equation = eq(r"h^2+1^2=2^2", cfg.WHITE, cfg.FONT["section"]).move_to([3.25, 1.25, 0])
    pythagoras_label = outlined_text("PYTHAGORAS", cfg.FONT["small"], cfg.CYAN, BOLD).next_to(
        height_equation, UP, buff=0.22
    )
    paced_play(scene, FadeIn(pythagoras_label), Write(height_equation), run_time=1.2)

    height = eq(r"h=\sqrt{2^2-1^2}=\sqrt3", cfg.CYAN, cfg.FONT["section"]).next_to(
        height_equation, DOWN, buff=0.42
    )
    altitude_value = eq(r"\sqrt3", cfg.CYAN, cfg.FONT["section"]).next_to(altitude, RIGHT, buff=0.14)
    paced_play(
        scene,
        TransformFromCopy(VGroup(altitude, height_equation), height),
        FadeIn(altitude_value),
        run_time=1.2,
    )

    side_pattern = eq(r"1:\sqrt3:2", cfg.GOLD, cfg.FONT["hero"]).move_to([3.2, 0.75, 0])
    pattern_label = outlined_text(
        "OPPOSITE 30°  :  OPPOSITE 60°  :  OPPOSITE 90°",
        cfg.FONT["tiny"],
        cfg.WHITE,
        BOLD,
    ).next_to(side_pattern, UP, buff=0.25)
    paced_play(
        scene,
        FadeOut(VGroup(pythagoras_label, height_equation, height)),
        FadeIn(VGroup(pattern_label, side_pattern), shift=UP * 0.12),
        run_time=1.0,
    )

    thirty_values = VGroup(
        outlined_text("FOR 30°", cfg.FONT["small"], cfg.GOLD, BOLD),
        eq(r"\sin30^\circ=\frac{1}{2}", cfg.CYAN, cfg.FONT["body"]),
        eq(r"\cos30^\circ=\frac{\sqrt3}{2}", cfg.GREEN, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.20)
    sixty_values = VGroup(
        outlined_text("FOR 60°", cfg.FONT["small"], cfg.GOLD, BOLD),
        eq(r"\sin60^\circ=\frac{\sqrt3}{2}", cfg.CYAN, cfg.FONT["body"]),
        eq(r"\cos60^\circ=\frac{1}{2}", cfg.GREEN, cfg.FONT["body"]),
    ).arrange(DOWN, buff=0.20)
    value_panel = VGroup(thirty_values, sixty_values).arrange(RIGHT, buff=0.70).move_to([3.2, -1.35, 0])
    paced_play(
        scene,
        LaggedStart(
            FadeIn(thirty_values, shift=RIGHT * 0.12),
            FadeIn(sixty_values, shift=RIGHT * 0.12),
            lag_ratio=0.35,
        ),
        run_time=2.0,
    )

    construction = VGroup(
        equilateral,
        altitude,
        right_angle,
        side_twos,
        one_left,
        one_right,
        sixty_left,
        sixty_right,
        thirty_angles,
        chosen_triangle,
        altitude_value,
        pattern_label,
        side_pattern,
        value_panel,
    )
    paced_play(scene, FadeOut(construction), run_time=0.9)

    # Exact values emerge from the two triangles, not from memorization.
    headers = VGroup(*[
        outlined_text(text, cfg.FONT["body"], color, BOLD)
        for text, color in (("θ", cfg.GOLD), ("sin θ", cfg.CYAN), ("cos θ", cfg.GREEN), ("tan θ", cfg.ORANGE))
    ]).arrange(RIGHT, buff=1.15).to_edge(UP, buff=0.7)
    rows = (
        (r"0^\circ", "0", "1", "0"),
        (r"30^\circ", r"\frac12", r"\frac{\sqrt3}{2}", r"\frac1{\sqrt3}"),
        (r"45^\circ", r"\frac{\sqrt2}{2}", r"\frac{\sqrt2}{2}", "1"),
        (r"60^\circ", r"\frac{\sqrt3}{2}", r"\frac12", r"\sqrt3"),
        (r"90^\circ", "1", "0", r"\text{undefined}"),
    )
    table_rows = VGroup()
    colors = (cfg.GOLD, cfg.CYAN, cfg.GREEN, cfg.ORANGE)
    for row in rows:
        items = VGroup(*[eq(value, colors[i], cfg.FONT["body"]) for i, value in enumerate(row)])
        items.arrange(RIGHT, buff=1.22)
        for item, header in zip(items, headers, strict=True):
            item.set_x(header.get_x())
        table_rows.add(items)
    table_rows.arrange(DOWN, buff=0.36).next_to(headers, DOWN, buff=0.42)
    paced_play(scene, LaggedStart(*[FadeIn(header, shift=DOWN * 0.12) for header in headers], lag_ratio=0.18), run_time=1.2)
    paced_play(scene, LaggedStart(*[FadeIn(row, shift=RIGHT * 0.18) for row in table_rows], lag_ratio=0.18), run_time=2.4)
    paced_play(scene, LaggedStart(*[Indicate(row, color=cfg.WHITE, scale_factor=1.02) for row in table_rows], lag_ratio=0.2), run_time=2.0)
    memory = bottom_caption("Derive the table from the two triangles.", cfg.WHITE)
    paced_play(scene, FadeIn(memory), run_time=0.8)
    narration_wait(scene, 2.4)

    paced_play(scene, FadeOut(VGroup(headers, table_rows, memory)), run_time=0.8)
    circle = Circle(radius=2.65, color=cfg.WHITE, stroke_width=5)
    rays = VGroup()
    points = VGroup()
    point_labels = VGroup()
    for angle, label in ((0, "0°"), (PI / 6, "30°"), (PI / 4, "45°"), (PI / 3, "60°"), (PI / 2, "90°")):
        end = 2.65 * np.array([np.cos(angle), np.sin(angle), 0])
        rays.add(Line(ORIGIN, end, color=cfg.MUTED, stroke_width=3))
        points.add(glow_dot(end, cfg.GOLD, 0.08))
        point_labels.add(outlined_text(label, cfg.FONT["tiny"], cfg.GOLD, BOLD).move_to(end * 1.18))
    first_quadrant = VGroup(circle, rays, points, point_labels).move_to(DOWN * 0.15)
    paced_play(scene, Create(circle), run_time=1.1)
    paced_play(scene, LaggedStart(*[Create(ray) for ray in rays], lag_ratio=0.16), LaggedStart(*[FadeIn(point) for point in points], lag_ratio=0.16), run_time=2.0)
    paced_play(scene, LaggedStart(*[FadeIn(label) for label in point_labels], lag_ratio=0.15), run_time=1.2)
    bridge = bottom_caption("These exact points extend around the unit circle.", cfg.GOLD)
    paced_play(scene, FadeIn(bridge), run_time=0.7)
    narration_wait(scene, 2.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["06"])
