"""Scene 2: off-center contact creates speed plus side-spin."""

from __future__ import annotations

from math import cos, sin

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    force_equation_card,
    label_text,
    narration_wait,
    paced_play,
    trionda_image_ball,
    vector_arrow,
)


class Scene02OffCenterKick(Scene):
    """The hidden initial condition: spin axis and angular velocity."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    ball = trionda_image_ball(width=1.9).move_to([0.05, 0.18, 0])
    spin_marks = VGroup()
    for shift in (-0.18, 0.18):
        mark = Arc(radius=1.12, start_angle=PI * 0.08 + shift, angle=PI * 0.78, color=cfg.ORANGE, stroke_width=6)
        end_angle = PI * 0.08 + shift + PI * 0.78
        tip = Triangle(color=cfg.ORANGE, fill_color=cfg.ORANGE, fill_opacity=1).scale(0.105)
        tip.move_to([cos(end_angle) * 1.12, sin(end_angle) * 1.12, 0])
        tip.rotate(end_angle - PI / 2)
        spin_marks.add(mark, tip)
    spin_marks.move_to(ball.get_center())
    ball_visual = Group(ball, spin_marks)
    foot = VGroup(
        RoundedRectangle(corner_radius=0.2, width=2.2, height=0.62, fill_color=cfg.COLORS["panel"], fill_opacity=1, stroke_color=cfg.ORANGE, stroke_width=4),
        Polygon([-1.08, -0.31, 0], [-1.66, -0.52, 0], [-0.72, -0.31, 0], color=cfg.ORANGE, fill_color=cfg.ORANGE, fill_opacity=0.55),
    ).rotate(-12 * DEGREES).move_to([-3.05, -0.52, 0])
    contact = Dot(ball.get_center() + LEFT * 0.8 + DOWN * 0.27, radius=0.085, color=cfg.ORANGE)
    off_center = DashedLine(ball.get_center(), contact.get_center(), color=cfg.ORANGE, stroke_width=4, dash_length=0.09)

    scene.add(ball_visual)
    paced_play(scene, FadeIn(foot, shift=RIGHT * 0.4), Flash(contact, color=cfg.ORANGE, flash_radius=0.45), Create(off_center), run_time=0.85)

    v_arrow = vector_arrow([1.08, 0.18, 0], [4.05, 0.18, 0], cfg.CYAN)
    spin_axis = vector_arrow([0.05, -1.18, 0], [0.05, 1.7, 0], cfg.ORANGE)
    v_label = VGroup(
        MathTex(r"\vec{v}", color=cfg.CYAN, font_size=46),
        Text("velocity", font_size=30, color=cfg.CYAN, weight=BOLD),
    ).arrange(RIGHT, buff=0.16).move_to([2.68, 0.88, 0])
    omega_label = VGroup(
        MathTex(r"\vec{\omega}", color=cfg.ORANGE, font_size=46),
        Text("rotation", font_size=30, color=cfg.ORANGE, weight=BOLD),
    ).arrange(RIGHT, buff=0.2).move_to([1.6, 1.78, 0])
    label = label_text("off-center strike", 31, cfg.ORANGE).move_to([-3.05, -1.42, 0])
    paced_play(scene, GrowArrow(v_arrow[1]), FadeIn(v_arrow[0]), FadeIn(v_label), Create(spin_axis), FadeIn(omega_label), FadeIn(label), run_time=1.15)

    equation = force_equation_card(r"\text{kick} \rightarrow \vec{v}+\vec{\omega}", cfg.WHITE).scale(1.22)
    equation.to_edge(DOWN, buff=0.4)
    paced_play(scene, FadeIn(equation, shift=UP * 0.2), run_time=0.8)
    paced_play(scene, Rotate(ball_visual, angle=TAU * 1.4, about_point=ball.get_center()), run_time=1.4, rate_func=linear)

    small = label_text("the spin is invisible after contact", 42, cfg.WHITE, weight=BOLD)
    small.set_stroke("#06131B", width=5, opacity=0.9, background=True)
    small.to_edge(UP, buff=0.52)
    paced_play(scene, FadeIn(small), run_time=0.45)
    narration_wait(scene, 0.9)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["02"])
