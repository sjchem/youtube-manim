"""Scene 04: similar right triangles reveal sine, cosine, and tangent."""

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
    equation_card,
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)


def triangle_group(scale: float, origin: np.ndarray) -> VGroup:
    adjacent = 4.0 * scale
    opposite = 3.0 * scale
    p0 = origin
    p1 = origin + RIGHT * adjacent
    p2 = p1 + UP * opposite
    base = Line(p0, p1, color=cfg.GREEN, stroke_width=6)
    vertical = Line(p1, p2, color=cfg.CYAN, stroke_width=6)
    hypotenuse = Line(p2, p0, color=cfg.WHITE, stroke_width=6)
    marker = Square(side_length=0.22 * max(scale, 0.5), color=cfg.MUTED, stroke_width=3).move_to(p1 + LEFT * 0.11 * max(scale, 0.5) + UP * 0.11 * max(scale, 0.5))
    return VGroup(base, vertical, hypotenuse, marker)


class Scene04Ratios(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "04")
    add_cinematic_background(scene)
    tag = section_tag("04", "Freeze the ray into a triangle")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    origin = np.array([-5.9, -2.45, 0.0])
    tri = triangle_group(1.0, origin)
    hypotenuse_angle = np.arctan2(3, 4)
    angle = Angle(tri[0], tri[2].copy().reverse_direction(), radius=0.65, color=cfg.GOLD, stroke_width=5)
    theta_label = eq(r"\theta", cfg.GOLD, cfg.FONT["body"]).move_to(origin + np.array([0.78, 0.32, 0]))
    side_labels = VGroup(
        outlined_text("adjacent = 4", cfg.FONT["label"], cfg.GREEN).next_to(tri[0], DOWN, buff=0.17),
        outlined_text("opposite = 3", cfg.FONT["label"], cfg.CYAN).next_to(tri[1], RIGHT, buff=0.17),
        outlined_text("hypotenuse = 5", cfg.FONT["label"], cfg.WHITE)
        .rotate(hypotenuse_angle)
        .move_to(tri[2].get_center() + np.array([-0.38, 0.52, 0])),
    )
    paced_play(
        scene,
        FadeOut(tag),
        LaggedStart(Create(tri), Create(angle), FadeIn(theta_label), lag_ratio=0.2),
        run_time=1.8,
    )
    paced_play(scene, LaggedStart(*[FadeIn(label) for label in side_labels], lag_ratio=0.2), run_time=1.2)
    narration_wait(scene, 1.8)

    ratio_column = VGroup(
        equation_card(r"\frac{\mathrm{opposite}}{\mathrm{hypotenuse}}=\frac35", cfg.CYAN, cfg.FONT["body"]),
        equation_card(r"\frac{\mathrm{adjacent}}{\mathrm{hypotenuse}}=\frac45", cfg.GREEN, cfg.FONT["body"]),
        equation_card(r"\frac{\mathrm{opposite}}{\mathrm{adjacent}}=\frac34", cfg.ORANGE, cfg.FONT["body"]),
    )
    card_width = max(card[1].width for card in ratio_column)
    for card in ratio_column:
        card[0].stretch_to_fit_width(card_width)
        card[1].stretch_to_fit_width(card_width)
    ratio_column.arrange(DOWN, buff=0.28).move_to([3.75, -0.25, 0])
    paced_play(scene, LaggedStart(*[FadeIn(card, shift=LEFT * 0.18) for card in ratio_column], lag_ratio=0.3), run_time=2.0)
    narration_wait(scene, 2.0)

    # Double every side while keeping the angle fixed.
    big_origin = np.array([-6.25, -2.45, 0.0])
    big_tri = triangle_group(1.35, big_origin)
    big_angle = Angle(big_tri[0], big_tri[2].copy().reverse_direction(), radius=0.72, color=cfg.GOLD, stroke_width=5)
    big_theta_label = eq(r"\theta", cfg.GOLD, cfg.FONT["body"]).move_to(big_origin + np.array([0.86, 0.36, 0]))
    big_labels = VGroup(
        outlined_text("5.4", cfg.FONT["label"], cfg.GREEN).next_to(big_tri[0], DOWN, buff=0.16),
        outlined_text("4.05", cfg.FONT["label"], cfg.CYAN).next_to(big_tri[1], RIGHT, buff=0.16),
        outlined_text("6.75", cfg.FONT["label"], cfg.WHITE)
        .rotate(hypotenuse_angle)
        .move_to(big_tri[2].get_center() + np.array([-0.28, 0.38, 0])),
    )
    scale_word = outlined_text("Scale every side", cfg.FONT["body"], cfg.GOLD, BOLD).move_to([-3.0, 2.35, 0])
    paced_play(
        scene,
        FadeIn(scale_word),
        Transform(tri, big_tri),
        Transform(angle, big_angle),
        Transform(theta_label, big_theta_label),
        FadeOut(side_labels),
        run_time=2.2,
    )
    paced_play(scene, FadeIn(big_labels), run_time=0.8)
    paced_play(scene, LaggedStart(*[Indicate(card, color=cfg.WHITE) for card in ratio_column], lag_ratio=0.25), run_time=2.0)
    narration_wait(scene, 1.8)

    unchanged = bottom_caption("The lengths changed. The ratios did not.", cfg.GOLD)
    paced_play(scene, FadeIn(unchanged), run_time=0.7)
    narration_wait(scene, 2.3)

    paced_play(scene, FadeOut(VGroup(tri, angle, theta_label, big_labels, scale_word, unchanged)), ratio_column.animate.arrange(RIGHT, buff=0.28).scale(0.9).move_to([0, 1.1, 0]), run_time=1.1)

    formula_origin = np.array([-6.0, -1.65, 0.0])
    formula_triangle_lines = triangle_group(0.82, formula_origin)
    formula_angle = Angle(
        formula_triangle_lines[0],
        formula_triangle_lines[2].copy().reverse_direction(),
        radius=0.55,
        color=cfg.GOLD,
        stroke_width=4,
    )
    formula_theta = eq(r"\theta", cfg.GOLD, cfg.FONT["small"]).move_to(formula_origin + np.array([0.68, 0.28, 0]))
    formula_labels = VGroup(
        outlined_text("adjacent", cfg.FONT["small"], cfg.GREEN).next_to(formula_triangle_lines[0], DOWN, buff=0.14),
        outlined_text("opposite", cfg.FONT["small"], cfg.CYAN).next_to(formula_triangle_lines[1], RIGHT, buff=0.14),
        outlined_text("hypotenuse", cfg.FONT["small"], cfg.WHITE)
        .rotate(hypotenuse_angle)
        .move_to(formula_triangle_lines[2].get_center() + np.array([-0.3, 0.42, 0])),
    )
    formula_triangle = VGroup(formula_triangle_lines, formula_angle, formula_theta, formula_labels)

    names = VGroup(
        color_formula_parts(eq(r"\sin\theta=\frac{\mathrm{opposite}}{\mathrm{hypotenuse}}", cfg.WHITE, cfg.FONT["section"])),
        color_formula_parts(eq(r"\cos\theta=\frac{\mathrm{adjacent}}{\mathrm{hypotenuse}}", cfg.WHITE, cfg.FONT["section"])),
        color_formula_parts(eq(r"\tan\theta=\frac{\mathrm{opposite}}{\mathrm{adjacent}}", cfg.WHITE, cfg.FONT["section"])),
    ).arrange(DOWN, buff=0.38).move_to([2.35, 0.55, 0])
    paced_play(scene, FadeOut(ratio_column), FadeIn(formula_triangle, shift=RIGHT * 0.12), run_time=0.5)
    for formula in names:
        paced_play(scene, Write(formula), run_time=1.1)
        narration_wait(scene, 1.0)

    tan_bridge = color_formula_parts(eq(r"\tan\theta=\frac{\sin\theta}{\cos\theta}", cfg.WHITE, cfg.FONT["section"]))
    tan_bridge.next_to(names, DOWN, buff=0.34)
    paced_play(scene, TransformFromCopy(VGroup(names[0], names[1], names[2]), tan_bridge), run_time=1.4)
    narration_wait(scene, 2.0)

    paced_play(scene, FadeOut(VGroup(names, tan_bridge, formula_triangle)), run_time=0.7)

    # Let the triangle breathe as theta changes; values update live.
    theta = ValueTracker(np.arctan2(3, 4))
    pivot = np.array([-3.25, -1.4, 0.0])
    hyp = 3.7
    dynamic_triangle = always_redraw(
        lambda: VGroup(
            Line(pivot, pivot + RIGHT * hyp * np.cos(theta.get_value()), color=cfg.GREEN, stroke_width=7),
            Line(
                pivot + RIGHT * hyp * np.cos(theta.get_value()),
                pivot + np.array([hyp * np.cos(theta.get_value()), hyp * np.sin(theta.get_value()), 0]),
                color=cfg.CYAN,
                stroke_width=7,
            ),
            Line(
                pivot,
                pivot + np.array([hyp * np.cos(theta.get_value()), hyp * np.sin(theta.get_value()), 0]),
                color=cfg.WHITE,
                stroke_width=7,
            ),
            Arc(radius=0.72, start_angle=0, angle=theta.get_value(), arc_center=pivot, color=cfg.GOLD, stroke_width=5),
        )
    )
    values = VGroup(
        outlined_text("sin", cfg.FONT["section"], cfg.CYAN, BOLD),
        DecimalNumber(np.sin(theta.get_value()), num_decimal_places=2, font_size=cfg.FONT["section"], color=cfg.CYAN),
        outlined_text("cos", cfg.FONT["section"], cfg.GREEN, BOLD),
        DecimalNumber(np.cos(theta.get_value()), num_decimal_places=2, font_size=cfg.FONT["section"], color=cfg.GREEN),
        outlined_text("tan", cfg.FONT["section"], cfg.ORANGE, BOLD),
        DecimalNumber(np.tan(theta.get_value()), num_decimal_places=2, font_size=cfg.FONT["section"], color=cfg.ORANGE),
    ).arrange_in_grid(rows=3, cols=2, buff=(0.45, 0.28)).move_to([3.45, -0.1, 0])
    values[1].add_updater(lambda mob: mob.set_value(np.sin(theta.get_value())))
    values[3].add_updater(lambda mob: mob.set_value(np.cos(theta.get_value())))
    values[5].add_updater(lambda mob: mob.set_value(np.tan(theta.get_value())))
    heading = outlined_text("Same size. Change only the angle.", cfg.FONT["body"], cfg.WHITE, BOLD).to_edge(UP, buff=0.42)
    scene.add(dynamic_triangle)
    paced_play(scene, FadeIn(values), FadeIn(heading), run_time=1.0)
    paced_play(scene, theta.animate.set_value(PI / 6), run_time=4.0, rate_func=smooth)
    paced_play(scene, theta.animate.set_value(PI / 3), run_time=5.0, rate_func=smooth)
    paced_play(scene, theta.animate.set_value(PI / 4), run_time=4.0, rate_func=smooth)
    final_caption = bottom_caption("A trigonometric ratio belongs to the angle—not the triangle's size.", cfg.GOLD)
    paced_play(scene, FadeIn(final_caption), run_time=0.8)
    narration_wait(scene, 2.5)
    end_scene(scene, started, cfg.SCENE_DURATIONS["04"])
