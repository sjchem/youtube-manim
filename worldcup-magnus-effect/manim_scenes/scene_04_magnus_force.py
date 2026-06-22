"""Scene 4: wake deflection becomes a sideways force."""

from __future__ import annotations

from math import cos, sin

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, force_equation_card, narration_wait, paced_play, trionda_image_ball, vector_arrow, wake_ribbon


class Scene04MagnusForce(Scene):
    """Newton's third law view of the Magnus force."""

    def construct(self) -> None:
        play_scene(self)


def rotation_arrows(radius: float = 0.92, stroke_width: float = 9) -> VGroup:
    """Create bold rotation arrows around the real ball image."""
    arrows = VGroup()
    for shift in (-0.18, 0.18):
        arc = Arc(radius=radius, start_angle=0.12 * PI + shift, angle=0.76 * PI, color=cfg.ORANGE, stroke_width=stroke_width)
        end_angle = 0.12 * PI + shift + 0.76 * PI
        tip = Triangle(color=cfg.ORANGE, fill_color=cfg.ORANGE, fill_opacity=1).scale(0.11)
        tip.move_to([cos(end_angle) * radius, sin(end_angle) * radius, 0])
        tip.rotate(end_angle - PI / 2)
        arrows.add(arc, tip)
    return arrows


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())
    ball = trionda_image_ball(width=1.5).shift(LEFT * 1.2)
    spin = rotation_arrows(radius=0.96, stroke_width=10).move_to(ball.get_center())
    ball_visual = Group(ball, spin)
    wake = wake_ribbon(cfg.ORANGE).shift(LEFT * 1.2)
    velocity = vector_arrow([-3.45, 1.15, 0], [-1.75, 1.15, 0], cfg.CYAN)
    air_push = vector_arrow([1.0, -0.15, 0], [3.05, -1.25, 0], cfg.ORANGE)
    ball_push = vector_arrow([-1.2, 0.55, 0], [-1.2, 2.5, 0], cfg.GREEN)

    velocity_label = VGroup(
        MathTex(r"\vec{v}", color=cfg.CYAN, font_size=50),
        Text("velocity", font_size=32, color=cfg.CYAN, weight=BOLD),
    ).arrange(RIGHT, buff=0.16).move_to([-2.55, 1.72, 0])
    air_label = Text("air pushed down", font_size=35, color=cfg.ORANGE, weight=BOLD).move_to([2.15, -0.18, 0])
    force_label = VGroup(
        MathTex(r"\vec{F}_M", color=cfg.GREEN, font_size=52),
        Text("Magnus force", font_size=34, color=cfg.GREEN, weight=BOLD),
    ).arrange(RIGHT, buff=0.16).move_to([0.35, 2.28, 0])

    paced_play(scene, FadeIn(ball_visual, scale=0.8), GrowArrow(velocity[1]), FadeIn(velocity[0]), FadeIn(velocity_label), run_time=2.1)
    paced_play(scene, FadeIn(wake), GrowArrow(air_push[1]), FadeIn(air_push[0]), FadeIn(air_label), run_time=2.5)
    paced_play(scene, GrowArrow(ball_push[1]), FadeIn(ball_push[0]), FadeIn(force_label), run_time=2.3)

    equation = force_equation_card(r"\vec{F}_M \propto \vec{\omega}\times\vec{v}", cfg.WHITE).scale(1.35)
    equation.to_edge(DOWN, buff=0.42)
    side_note = Text("sideways force keeps acting", font_size=40, color=cfg.WHITE, weight=BOLD).to_edge(UP, buff=0.48)
    side_note.set_stroke("#06131B", width=5, opacity=0.9, background=True)
    paced_play(scene, FadeIn(equation, shift=UP * 0.2), FadeIn(side_note), run_time=2.2)
    paced_play(scene, Indicate(ball_push, color=cfg.GREEN, scale_factor=1.05), Rotate(ball_visual, angle=TAU * 0.8, rate_func=linear), run_time=4.0)
    narration_wait(scene, 2.4)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["04"])
