"""Scene 15: Euler's formula packages circular motion into one expression."""

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


class Scene15Euler(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "15")
    add_cinematic_background(scene)
    tag = section_tag("15", "One symbol for every rotation")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    plane = ComplexPlane(
        x_range=[-1.5, 1.5, 0.5],
        y_range=[-1.5, 1.5, 0.5],
        x_length=6.0,
        y_length=6.0,
        background_line_style={"stroke_color": cfg.GRAY, "stroke_width": 1.5, "stroke_opacity": 0.35},
        axis_config={"stroke_color": cfg.MUTED, "stroke_width": 3},
    ).move_to([-3.25, -0.2, 0])
    real_name = outlined_text("REAL", cfg.FONT["small"], cfg.GREEN, BOLD).next_to(plane.x_axis, DOWN, buff=0.18).to_edge(LEFT, buff=0.55)
    imaginary_name = outlined_text("IMAGINARY AXIS", cfg.FONT["tiny"], cfg.CYAN, BOLD)
    imaginary_name.next_to(plane.y_axis.get_top(), LEFT, buff=0.22)
    unit = Circle(radius=2.0, color=cfg.WHITE, stroke_width=4).move_to(plane.n2p(0))
    paced_play(scene, FadeOut(tag), Create(plane), FadeIn(real_name), FadeIn(imaginary_name), Create(unit), run_time=1.8)

    theta = ValueTracker(0.0)
    point_position = lambda: plane.n2p(np.cos(theta.get_value()) + 1j * np.sin(theta.get_value()))
    vector = always_redraw(lambda: Arrow(plane.n2p(0), point_position(), color=cfg.GOLD, stroke_width=7, buff=0))
    point = always_redraw(lambda: glow_dot(point_position(), cfg.GOLD, 0.1))
    real_projection = always_redraw(
        lambda: Line(plane.n2p(0), plane.n2p(np.cos(theta.get_value())), color=cfg.GREEN, stroke_width=7)
    )
    imag_projection = always_redraw(
        lambda: Line(plane.n2p(np.cos(theta.get_value())), point_position(), color=cfg.CYAN, stroke_width=7)
    )
    arc = always_redraw(lambda: Arc(radius=0.58, start_angle=0, angle=theta.get_value(), arc_center=plane.n2p(0), color=cfg.GOLD, stroke_width=5))
    scene.add(real_projection, imag_projection, vector, arc, point)
    coordinate = VGroup(
        eq(r"\cos\theta", cfg.GREEN, cfg.FONT["section"]),
        eq("+", cfg.WHITE, cfg.FONT["section"]),
        eq(r"i\sin\theta", cfg.CYAN, cfg.FONT["section"]),
    ).arrange(RIGHT, buff=0.25).move_to([3.55, 0.3, 0])
    paced_play(scene, theta.animate.set_value(PI / 3), FadeIn(coordinate), run_time=4.0, rate_func=smooth)
    narration_wait(scene, 1.5)

    # Introduce Euler's formula as soon as the cosine and sine projections are
    # visible, matching the order of the narration.
    exponential = eq(r"e^{i\theta}", cfg.GOLD, cfg.FONT["hero"]).move_to([3.55, 1.65, 0])
    equals = eq("=", cfg.WHITE, cfg.FONT["hero"]).next_to(exponential, DOWN, buff=0.3)
    paced_play(scene, FadeIn(exponential, scale=1.2), FadeIn(equals), run_time=1.1)
    euler = eq(r"e^{i\theta}=\cos\theta+i\sin\theta", cfg.WHITE, cfg.FONT["hero"]).move_to([2.6, -1.4, 0])
    euler.set_color_by_tex(r"e^{i\theta}", cfg.GOLD)
    euler.set_color_by_tex(r"\cos", cfg.GREEN)
    euler.set_color_by_tex(r"\sin", cfg.CYAN)
    paced_play(scene, ReplacementTransform(VGroup(exponential, equals, coordinate), euler), run_time=1.6)
    # Use a fresh, explicit single-line title asset.  The curly apostrophe also
    # prevents Manim from reusing the stale wrapped title from an older render.
    name = outlined_text("EULER’S FORMULA", cfg.FONT["body"], cfg.GOLD, BOLD)
    if name.width > cfg.SAFE_WIDTH - 0.5:
        name.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    name.to_edge(UP, buff=0.42)
    paced_play(scene, FadeIn(name), Indicate(euler, color=cfg.GOLD), run_time=1.1)
    narration_wait(scene, 2.0)

    # Multiplication adds rotations; then a full turn returns to one.
    paced_play(scene, euler.animate.scale(0.72).move_to([3.35, 1.85, 0]), run_time=0.8)
    addition_rule = eq(
        r"e^{i\alpha}e^{i\beta}=e^{i(\alpha+\beta)}",
        cfg.PURPLE,
        cfg.FONT["body"],
    ).move_to([3.35, 0.45, 0])
    addition_words = outlined_text("MULTIPLY → ADD THE ANGLES", cfg.FONT["small"], cfg.WHITE, BOLD)
    addition_words.next_to(addition_rule, DOWN, buff=0.22)
    scene.add(addition_rule, addition_words)
    paced_play(
        scene,
        theta.animate.set_value(5 * PI / 4),
        Indicate(addition_rule, color=cfg.WHITE, scale_factor=1.025),
        run_time=5.0,
        rate_func=linear,
    )

    full_turn = VGroup(
        eq(r"\theta=2\pi", cfg.CYAN, cfg.FONT["body"]),
        eq(r"e^{i2\pi}=1", cfg.GOLD, cfg.FONT["section"]),
    ).arrange(DOWN, buff=0.2).move_to([3.35, 0.35, 0])
    scene.remove(addition_rule, addition_words)
    scene.add(full_turn)
    paced_play(scene, theta.animate.set_value(TAU), Indicate(full_turn[1], color=cfg.WHITE), run_time=5.0, rate_func=linear)

    # At theta=pi the rotating point reaches -1.
    paced_play(scene, theta.animate.set_value(PI), run_time=5.0, rate_func=smooth)
    pi_substitution = eq(r"\theta=\pi", cfg.PURPLE, cfg.FONT["section"]).move_to([3.4, 0.65, 0])
    paced_play(scene, FadeOut(full_turn), FadeIn(pi_substitution), run_time=0.8)
    identity = eq(r"e^{i\pi}+1=0", cfg.GOLD, cfg.FONT["hero"]).move_to([3.35, -0.4, 0])
    paced_play(scene, TransformFromCopy(euler, identity), run_time=1.5)
    paced_play(scene, Indicate(identity, color=cfg.WHITE, scale_factor=1.06), run_time=1.2)
    narration_wait(scene, 1.8)

    paced_play(scene, FadeOut(VGroup(plane, real_name, imaginary_name, unit, real_projection, imag_projection, vector, arc, point, euler, name, pi_substitution, identity)), run_time=0.9)
    closing = VGroup(
        outlined_text("RIGHT TRIANGLE", cfg.FONT["body"], cfg.WHITE, BOLD),
        outlined_text("UNIT CIRCLE", cfg.FONT["body"], cfg.CYAN, BOLD),
        outlined_text("SINE WAVE", cfg.FONT["body"], cfg.GREEN, BOLD),
        outlined_text("COMPLEX EXPONENTIAL", cfg.FONT["body"], cfg.GOLD, BOLD),
    ).arrange(DOWN, buff=0.72).move_to(UP * 0.45)
    arrows = VGroup(*[
        Arrow(
            closing[i].get_bottom(),
            closing[i + 1].get_top(),
            color=cfg.MUTED,
            stroke_width=5,
            buff=0.06,
            max_tip_length_to_length_ratio=0.24,
        )
        for i in range(3)
    ])
    paced_play(scene, LaggedStart(*[FadeIn(item, shift=UP * 0.13) for item in closing], lag_ratio=0.2), run_time=1.8)
    paced_play(scene, LaggedStart(*[GrowArrow(item) for item in arrows], lag_ratio=0.2), run_time=1.3)
    takeaway = outlined_text(
        "FOUR LANGUAGES · ONE ROTATING POINT",
        cfg.FONT["label"],
        cfg.WHITE,
        BOLD,
    )
    if takeaway.width > cfg.SAFE_WIDTH - 0.5:
        takeaway.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    takeaway.to_edge(DOWN, buff=0.28)
    paced_play(scene, FadeIn(takeaway), LaggedStart(*[Indicate(item, color=cfg.WHITE) for item in closing], lag_ratio=0.18), run_time=1.5)
    narration_wait(scene, 2.2)
    end_scene(scene, started, cfg.SCENE_DURATIONS["15"])
