"""Scene 12: right-triangle ideas extend to every triangle."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)


class Scene12NonRightTriangles(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "12")
    add_cinematic_background(scene)
    tag = section_tag("12", "What if the triangle is not right?")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    # Keep the base high enough to reserve a clean band for the projection braces.
    a = np.array([-5.1, -1.15, 0.0])
    b = np.array([4.7, -1.15, 0.0])
    c = np.array([1.05, 2.55, 0.0])
    triangle = Polygon(a, b, c, color=cfg.WHITE, stroke_width=7, fill_color=cfg.PANEL, fill_opacity=0.38)
    vertices = VGroup(
        outlined_text("A", cfg.FONT["body"], cfg.GOLD, BOLD).next_to(a, DL, buff=0.12),
        outlined_text("B", cfg.FONT["body"], cfg.GOLD, BOLD).next_to(b, DR, buff=0.12),
        outlined_text("C", cfg.FONT["body"], cfg.GOLD, BOLD).next_to(c, UP, buff=0.12),
    )
    side_names = VGroup(
        outlined_text("a", cfg.FONT["body"], cfg.CYAN, BOLD).move_to((b + c) / 2 + UR * 0.2),
        outlined_text("b", cfg.FONT["body"], cfg.GREEN, BOLD).move_to((a + c) / 2 + UL * 0.2),
        outlined_text("c", cfg.FONT["body"], cfg.WHITE, BOLD).next_to(Line(a, b), DOWN, buff=0.15),
    )
    paced_play(scene, FadeOut(tag), Create(triangle), FadeIn(vertices), FadeIn(side_names), run_time=1.7)
    not_right = outlined_text(
        "No right angle is visible—but we can create one.",
        cfg.FONT["label"],
        cfg.GOLD,
        BOLD,
    )
    if not_right.width > cfg.SAFE_WIDTH - 0.5:
        not_right.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    not_right.to_edge(DOWN, buff=0.28)
    paced_play(scene, FadeIn(not_right), run_time=0.7)
    narration_wait(scene, 1.3)

    foot = np.array([1.05, -1.15, 0.0])
    altitude = DashedLine(c, foot, color=cfg.CYAN, stroke_width=6, dash_length=0.16)
    right_mark = Square(side_length=0.28, color=cfg.GOLD, stroke_width=3).move_to(foot + LEFT * 0.14 + UP * 0.14)
    altitude_caption = outlined_text("DROP AN ALTITUDE", cfg.FONT["label"], cfg.CYAN, BOLD).to_edge(DOWN, buff=0.25)
    paced_play(scene, ReplacementTransform(not_right, altitude_caption), Create(altitude), FadeIn(right_mark), run_time=1.4)
    braces = VGroup(
        Brace(Line(a, foot), DOWN, color=cfg.GREEN),
        Brace(Line(foot, b), DOWN, color=cfg.ORANGE),
    )
    projections = VGroup(
        eq(r"b\cos A", cfg.GREEN, cfg.FONT["body"]).next_to(braces[0], DOWN, buff=0.12),
        eq(r"a\cos B", cfg.ORANGE, cfg.FONT["body"]).next_to(braces[1], DOWN, buff=0.12),
    )
    paced_play(scene, GrowFromCenter(braces), FadeIn(projections), run_time=1.4)
    narration_wait(scene, 1.5)

    paced_play(
        scene,
        FadeOut(altitude_caption),
        VGroup(triangle, vertices, side_names, altitude, right_mark, braces, projections).animate.scale(0.7).to_edge(LEFT, buff=0.45),
        run_time=1.0,
    )
    area_a = eq(r"h=b\sin A", cfg.CYAN, cfg.FONT["section"]).move_to([3.8, 1.5, 0])
    area_b = eq(r"h=a\sin B", cfg.CYAN, cfg.FONT["section"]).next_to(area_a, DOWN, buff=0.55)
    paced_play(scene, Write(area_a), run_time=1.1)
    paced_play(scene, Write(area_b), run_time=1.1)
    equal_height = eq(r"b\sin A=a\sin B", cfg.WHITE, cfg.FONT["section"]).next_to(area_b, DOWN, buff=0.55)
    paced_play(scene, TransformFromCopy(VGroup(area_a, area_b), equal_height), run_time=1.3)
    sine_law = eq(
        r"\frac{a}{\sin A}=\frac{b}{\sin B}=\frac{c}{\sin C}",
        cfg.GOLD,
        cfg.FONT["section"],
    ).move_to([3.8, -1.7, 0])
    paced_play(scene, TransformFromCopy(equal_height, sine_law), run_time=1.5)
    narration_wait(scene, 2.0)

    law_name = outlined_text("LAW OF SINES", cfg.FONT["label"], cfg.GOLD, BOLD).to_edge(UP, buff=0.4)
    paced_play(scene, FadeIn(law_name), Indicate(sine_law, color=cfg.WHITE), run_time=1.0)
    narration_wait(scene, 1.4)

    paced_play(scene, FadeOut(VGroup(area_a, area_b, equal_height, sine_law, law_name)), run_time=0.8)
    diagram = VGroup(triangle, vertices, side_names, altitude, right_mark, braces, projections)
    paced_play(scene, diagram.animate.scale(0.9).move_to([-4.0, -0.05, 0]), run_time=1.0)
    cosine_steps = VGroup(
        eq(r"a^2=h^2+(c-b\cos A)^2", cfg.WHITE, cfg.FONT["body"]),
        eq(r"h^2=b^2-b^2\cos^2 A", cfg.CYAN, cfg.FONT["body"]),
        eq(r"a^2=b^2+c^2-2bc\cos A", cfg.GOLD, cfg.FONT["section"]),
    ).arrange(DOWN, buff=0.45).move_to([3.2, 0.25, 0])
    for step in cosine_steps:
        paced_play(scene, FadeIn(step, shift=LEFT * 0.15), run_time=1.1)
        narration_wait(scene, 0.75)
    cosine_name = outlined_text("LAW OF COSINES", cfg.FONT["label"], cfg.GOLD, BOLD).to_edge(UP, buff=0.4)
    paced_play(scene, FadeIn(cosine_name), Indicate(cosine_steps[-1], color=cfg.WHITE), run_time=1.0)
    narration_wait(scene, 1.7)

    paced_play(scene, FadeOut(VGroup(diagram, cosine_steps, cosine_name)), run_time=0.9)
    chooser = VGroup()
    choices = (
        ("RIGHT TRIANGLE", "SOH–CAH–TOA", cfg.CYAN),
        ("SIDE–OPPOSITE PAIR", "LAW OF SINES", cfg.GREEN),
        ("THREE SIDES OR SAS", "LAW OF COSINES", cfg.GOLD),
    )
    for condition, tool, color in choices:
        box = RoundedRectangle(width=4.35, height=2.75, corner_radius=0.18, color=color, fill_color=cfg.PANEL, fill_opacity=0.9)
        content = VGroup(
            outlined_text(condition, cfg.FONT["tiny"], cfg.WHITE, BOLD),
            Arrow(UP * 0.4, DOWN * 0.4, color=color, stroke_width=4, buff=0),
            outlined_text(tool, cfg.FONT["small"], color, BOLD),
        ).arrange(DOWN, buff=0.18).move_to(box)
        chooser.add(VGroup(box, content))
    chooser.arrange(RIGHT, buff=0.25).move_to(UP * 0.35)
    paced_play(scene, LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in chooser], lag_ratio=0.24), run_time=1.8)
    area = eq(r"\text{Area}=\frac12 ab\sin C", cfg.PURPLE, cfg.FONT["section"]).move_to(DOWN * 2.25)
    paced_play(scene, FadeIn(area), run_time=1.0)
    paced_play(scene, LaggedStart(*[Indicate(card, color=cfg.WHITE, scale_factor=1.02) for card in chooser], lag_ratio=0.22), run_time=1.6)
    # Keep this final takeaway as one explicit line.  Besides preserving the
    # phrase "Every non-right", the shorter wording matches the narration and
    # avoids stale wrapped-text cache artifacts from earlier renders.
    takeaway = outlined_text(
        "Every non-right triangle hides right triangles inside it.",
        cfg.FONT["body"],
        cfg.WHITE,
        BOLD,
    )
    if takeaway.width > cfg.SAFE_WIDTH - 0.5:
        takeaway.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    takeaway.to_edge(DOWN, buff=0.28)
    paced_play(scene, FadeOut(area), FadeIn(takeaway), run_time=0.8)
    narration_wait(scene, 2.2)
    end_scene(scene, started, cfg.SCENE_DURATIONS["12"])
