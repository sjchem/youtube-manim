from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    cutaway_layers,
    end_scene,
    glow,
    narration_wait,
    paced_play,
    scene_caption,
    small_label,
    trionda_ball,
)


class Scene01CutawayHook(MovingCameraScene):
    """Cold open: cut the ball open and reveal the engineered interior."""

    def construct(self) -> None:
        construct_scene_01(self)


def construct_scene_01(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    title = scene_caption("Cut open the 2026 World Cup ball", color=cfg.GOLD)
    ball = trionda_ball(radius=1.85).move_to(ORIGIN)
    shadow = Circle(radius=1.88, color=cfg.CYAN).set_stroke(width=16, opacity=0.10)
    shadow.move_to(ball)
    blade = Line(UP * 2.3, DOWN * 2.3, color=cfg.ORANGE, stroke_width=8).shift(LEFT * 3.2)
    spark = Star(outer_radius=0.18, inner_radius=0.07, color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=0.9)
    spark.move_to(blade.get_top())

    paced_play(scene, FadeIn(title, shift=DOWN * 0.2), FadeIn(shadow), FadeIn(ball, scale=0.92), run_time=1.0)
    paced_play(scene, Create(blade), FadeIn(spark), run_time=0.45)
    paced_play(scene, blade.animate.shift(RIGHT * 6.4), spark.animate.shift(RIGHT * 6.4 + DOWN * 4.2), run_time=1.15)
    paced_play(scene, FadeOut(blade), FadeOut(spark), ball.animate.shift(LEFT * 2.35).scale(0.86), run_time=0.75)

    layers = cutaway_layers(radius=1.72).move_to(RIGHT * 2.05)
    labels = VGroup(
        small_label("engineered cover", cfg.WHITE, 25),
        small_label("support layers", cfg.BLUE, 25),
        small_label("air bladder", cfg.PURPLE, 25),
        small_label("side-mounted IMU", cfg.GOLD, 25),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(layers, RIGHT, buff=0.22)
    arrows = VGroup()
    for label, target in zip(labels, [layers[0], layers[1], layers[2], layers[4]]):
        arrows.add(Arrow(label.get_left() + LEFT * 0.1, target.get_center(), buff=0.08, color=label.color, stroke_width=3))

    question = Text("Not just fewer panels.", font_size=38, color=cfg.WHITE, weight=BOLD)
    answer = Text("A precision aerodynamic instrument.", font_size=42, color=cfg.CYAN, weight=BOLD)
    stack = VGroup(question, answer).arrange(DOWN, buff=0.16).move_to(DOWN * 3.15)
    stack.set_stroke(cfg.BLACKISH, width=4, opacity=0.85, background=True)

    paced_play(scene, FadeOut(ball, scale=0.92), FadeIn(layers, scale=1.02), run_time=1.2)
    paced_play(scene, FadeIn(labels, shift=LEFT * 0.15), Create(arrows), run_time=0.85)
    paced_play(scene, FadeIn(glow(stack, color=cfg.CYAN, width=6, layers=2)), run_time=0.7)
    if hasattr(scene.camera, "frame"):
        focus = VGroup(layers, labels, arrows)
        paced_play(scene, scene.camera.frame.animate.move_to(focus).set(width=9.0), run_time=1.0)
        narration_wait(scene, 0.35)
        paced_play(scene, scene.camera.frame.animate.move_to(ORIGIN).set(width=16), run_time=0.8)
    video_title = VGroup(
        Text("The Secret Material Inside", font_size=45, color=cfg.WHITE, weight=BOLD),
        Text("the 2026 World Cup Ball", font_size=55, color=cfg.GOLD, weight=BOLD),
    ).arrange(DOWN, buff=0.08).move_to(ORIGIN)
    video_title.set_stroke(cfg.BLACKISH, width=5, opacity=0.9, background=True)
    underline = Line(LEFT * 3.1, RIGHT * 3.1, color=cfg.CYAN, stroke_width=5).next_to(video_title, DOWN, buff=0.22)
    title_card = glow(VGroup(video_title, underline), color=cfg.GOLD, width=7, layers=2)
    paced_play(scene, FadeOut(stack), FadeOut(labels), FadeOut(arrows), FadeOut(layers), FadeOut(title), run_time=0.55)
    paced_play(scene, FadeIn(title_card, scale=1.05), run_time=0.75)
    narration_wait(scene, 0.9)
    end_scene(scene, scene_start, "01")
