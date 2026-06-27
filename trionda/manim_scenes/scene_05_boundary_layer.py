from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    flow_lines,
    narration_wait,
    paced_play,
    scene_caption,
    small_label,
    trionda_ball,
    wake_cloud,
)


class Scene05BoundaryLayer(MovingCameraScene):
    """Airflow comparison: smooth sphere versus engineered roughness."""

    def construct(self) -> None:
        construct_scene_05(self)


def construct_scene_05(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    caption = scene_caption("The goal is predictable drag", color=cfg.GREEN)
    left_center = LEFT * 3.65 + UP * 0.2
    right_center = RIGHT * 3.65 + UP * 0.2
    smooth = Circle(radius=1.05, color=cfg.WHITE, fill_color=cfg.WHITE, fill_opacity=0.93).move_to(left_center)
    textured = trionda_ball(radius=1.05).move_to(right_center)
    smooth_title = small_label("too smooth", cfg.ORANGE, 34).move_to(left_center + UP * 1.7 + LEFT * 0.15)
    rough_title = small_label("precisely rough", cfg.GREEN, 34).move_to(right_center + UP * 1.7 + LEFT * 0.1)

    left_flow = flow_lines(left_center, 1.05, rough=False)
    right_flow = flow_lines(right_center, 1.05, rough=True)
    for line in left_flow:
        line.set_stroke(cfg.MUTED, width=5.2, opacity=0.55)
    for line in right_flow:
        line.set_stroke(cfg.CYAN, width=5.2, opacity=0.62)
    left_wake = wake_cloud(left_center, rough=False)
    right_wake = wake_cloud(right_center, rough=True)
    sep_left = Dot(left_center + RIGHT * 0.55 + UP * 0.86, color=cfg.ORANGE, radius=0.08)
    sep_right = Dot(right_center + RIGHT * 0.88 + UP * 0.58, color=cfg.GREEN, radius=0.08)
    sep_labels = VGroup(
        small_label("early separation", cfg.ORANGE, 24).move_to(left_center + RIGHT * 1.55 + UP * 1.15),
        small_label("delayed separation", cfg.GREEN, 24).move_to(right_center + RIGHT * 1.75 + UP * 0.95),
    )
    sep_labels.set_z_index(5)
    smooth_title.set_z_index(5)
    rough_title.set_z_index(5)

    boundary = VGroup(
        small_label("boundary layer", cfg.CYAN, 34),
        Text("a thin skin of air that decides the wake", font_size=29, color=cfg.WHITE),
    ).arrange(DOWN, buff=0.08).move_to(DOWN * 3.2)
    boundary.set_stroke(cfg.BLACKISH, width=3, opacity=0.85, background=True)

    paced_play(scene, FadeIn(caption), FadeIn(smooth), FadeIn(textured), FadeIn(smooth_title), FadeIn(rough_title), run_time=0.85)
    paced_play(scene, LaggedStart(*[Create(line) for line in left_flow], lag_ratio=0.08), run_time=1.2)
    paced_play(scene, FadeIn(left_wake), FadeIn(sep_left), FadeIn(sep_labels[0]), run_time=0.65)
    paced_play(scene, LaggedStart(*[Create(line) for line in right_flow], lag_ratio=0.08), run_time=1.2)
    paced_play(scene, FadeIn(right_wake), FadeIn(sep_right), FadeIn(sep_labels[1]), run_time=0.65)
    paced_play(scene, FadeIn(boundary, shift=UP * 0.12), run_time=0.7)
    paced_play(scene, right_wake.animate.scale(0.94).set_opacity(0.88), rate_func=there_and_back, run_time=0.8)
    narration_wait(scene, 0.9)
    end_scene(scene, scene_start, "05")
