from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    four_panel_map,
    narration_wait,
    old_stitched_ball,
    paced_play,
    scene_caption,
    small_label,
)


class Scene03ThermalBonding(MovingCameraScene):
    """Compare stitched assembly with thermal bonding."""

    def construct(self) -> None:
        construct_scene_03(self)


def construct_scene_03(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    caption = scene_caption("Thermal bonding controls seam geometry", color=cfg.GOLD)
    old_ball = old_stitched_ball(radius=1.25).shift(LEFT * 4.1 + UP * 0.4)
    new_ball = four_panel_map(radius=1.25).shift(RIGHT * 4.1 + UP * 0.4)
    old_title = small_label("stitched seams", cfg.MUTED, 34).next_to(old_ball, UP, buff=0.28)
    new_title = small_label("thermally bonded seams", cfg.GREEN, 34).next_to(new_ball, UP, buff=0.28)

    seam_left = VGroup(
        Rectangle(width=2.2, height=0.22, color=cfg.MUTED, fill_color=cfg.MUTED, fill_opacity=0.25).shift(LEFT * 1.1),
        Rectangle(width=2.2, height=0.22, color=cfg.MUTED, fill_color=cfg.MUTED, fill_opacity=0.25).shift(RIGHT * 1.1),
        VGroup(*[Line([x, -0.35, 0], [x + 0.16, 0.35, 0], color=cfg.RED, stroke_width=3) for x in np.linspace(-0.7, 0.7, 7)]),
    ).move_to(LEFT * 4.1 + DOWN * 2.0)
    seam_right = VGroup(
        Rectangle(width=2.1, height=0.24, color=cfg.CYAN, fill_color=cfg.BLUE, fill_opacity=0.3).shift(LEFT * 1.02),
        Rectangle(width=2.1, height=0.24, color=cfg.CYAN, fill_color=cfg.BLUE, fill_opacity=0.3).shift(RIGHT * 1.02),
        Line(UP * 0.24, DOWN * 0.24, color=cfg.GOLD, stroke_width=8),
    ).move_to(RIGHT * 4.1 + DOWN * 2.0)
    heat = VGroup(*[Arc(radius=0.22 + i * 0.13, angle=PI, color=cfg.ORANGE, stroke_width=3, stroke_opacity=0.75 / (i + 1)) for i in range(5)])
    heat.rotate(PI / 2).move_to(seam_right[2].get_center() + UP * 0.42)

    points = VGroup(
        small_label("seam depth", cfg.CYAN),
        small_label("water resistance", cfg.BLUE),
        small_label("repeatability", cfg.GREEN),
    ).arrange(RIGHT, buff=0.55).move_to(DOWN * 3.35)

    paced_play(scene, FadeIn(caption), FadeIn(old_title), FadeIn(new_title), run_time=0.75)
    paced_play(scene, FadeIn(old_ball, shift=RIGHT * 0.2), FadeIn(new_ball, shift=LEFT * 0.2), run_time=0.9)
    paced_play(scene, FadeIn(seam_left), FadeIn(seam_right), run_time=0.65)
    paced_play(scene, Create(heat), seam_right[0].animate.shift(RIGHT * 0.1), seam_right[1].animate.shift(LEFT * 0.1), run_time=0.95)
    paced_play(scene, seam_right[2].animate.set_stroke(width=14, opacity=0.95), rate_func=there_and_back, run_time=0.7)
    paced_play(scene, FadeIn(points, shift=UP * 0.1), run_time=0.7)
    for point in points:
        paced_play(scene, Indicate(point, color=cfg.GOLD, scale_factor=1.03), run_time=0.28)
    narration_wait(scene, 0.7)
    end_scene(scene, scene_start, "03")
