"""Scene 8: final synthesis of the layered explanation."""

from __future__ import annotations

from math import cos, sin

from manim import *

import config as cfg
from manim_scenes.common import (
    airflow_lines,
    begin_scene,
    cinematic_background,
    end_scene,
    expected_and_curved_paths,
    force_equation_card,
    goal_top_view,
    label_text,
    narration_wait,
    paced_play,
    pitch_top_view,
    trionda_image_ball,
    vector_arrow,
    wake_ribbon,
)


class Scene08FinalSynthesis(Scene):
    """End by layering spin, air, force, and curve."""

    def construct(self) -> None:
        play_scene(self)


def rotation_arrows(radius: float = 0.43) -> VGroup:
    """Bold spin arrows sized for the moving Trionda image."""
    arrows = VGroup()
    for shift in (-0.16, 0.18):
        arc = Arc(radius=radius, start_angle=0.12 * PI + shift, angle=0.74 * PI, color=cfg.ORANGE, stroke_width=6)
        end_angle = 0.12 * PI + shift + 0.74 * PI
        tip = Triangle(color=cfg.ORANGE, fill_color=cfg.ORANGE, fill_opacity=1).scale(0.055)
        tip.move_to([cos(end_angle) * radius, sin(end_angle) * radius, 0])
        tip.rotate(end_angle - PI / 2)
        arrows.add(arc, tip)
    return arrows


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())
    pitch = pitch_top_view().scale(0.82).shift(DOWN * 0.85)
    pitch[0].set_fill("#197A54", opacity=0.94).set_stroke("#A5E7C5", opacity=0.55, width=2.5)
    for index, band in enumerate(pitch[1]):
        band.set_fill("#2BAE72" if index % 2 == 0 else "#0F5E45", opacity=0.2)
    goal = goal_top_view(width=2.1, depth=0.72).move_to([5.35, -0.65, 0])
    _, curve = expected_and_curved_paths()
    curve.scale(0.86).shift(DOWN * 0.65)
    ball = trionda_image_ball(width=0.7).move_to(curve.get_start())
    spin = rotation_arrows().move_to(ball.get_center())
    ball_visual = Group(ball, spin)
    scene.add(pitch, goal, ball_visual)

    layers = VGroup(
        label_text("off-center kick", 34, cfg.ORANGE, weight=BOLD),
        label_text("spin", 34, cfg.ORANGE, weight=BOLD),
        label_text("tilted wake", 34, cfg.CYAN, weight=BOLD),
        label_text("side force", 34, cfg.GREEN, weight=BOLD),
    ).arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.55)
    paced_play(scene, LaggedStart(*[FadeIn(item, shift=DOWN * 0.12) for item in layers], lag_ratio=0.18), run_time=1.0)

    air = airflow_lines(spinning=True, count=7, color=cfg.CYAN).scale(0.48).move_to([-1.0, 1.35, 0])
    wake = wake_ribbon(cfg.ORANGE).scale(0.45).move_to([0.55, 1.25, 0])
    force = vector_arrow([0.0, 0.25, 0], [0.0, 1.25, 0], cfg.GREEN, r"\vec{F}_M").move_to([2.4, 1.15, 0])
    force[2].scale(1.4).next_to(force[1], RIGHT, buff=0.2)
    equation = force_equation_card(r"\vec{F}_M \perp \vec{v}", cfg.WHITE).scale(1.0).move_to([-3.8, 1.25, 0])
    paced_play(scene, FadeIn(equation), FadeIn(air), FadeIn(wake), FadeIn(force), run_time=1.1)
    paced_play(scene, Create(curve), MoveAlongPath(ball_visual, curve), run_time=2.2)

    final = VGroup(
        Text("A free kick curves because spin turns air", font_size=42, color=cfg.WHITE, weight=BOLD),
        Text("into an invisible steering force.", font_size=42, color=cfg.CYAN, weight=BOLD),
    ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.28)
    final.set_stroke("#06251D", width=5, opacity=0.92, background=True)
    paced_play(scene, FadeIn(final, shift=UP * 0.2), Indicate(goal, color=cfg.GREEN, scale_factor=1.03), run_time=1.0)
    narration_wait(scene, 1.4)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["08"])
