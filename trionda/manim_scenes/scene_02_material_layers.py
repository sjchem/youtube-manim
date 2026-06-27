from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    layer_stack,
    narration_wait,
    paced_play,
    scene_caption,
    small_label,
    trionda_ball,
)


class Scene02MaterialLayers(MovingCameraScene):
    """Explain the outer material system without fake formula precision."""

    def construct(self) -> None:
        construct_scene_02(self)


def construct_scene_02(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    caption = scene_caption("The outer skin is where air and boot meet", color=cfg.CYAN)
    ball = trionda_ball(radius=1.45).shift(LEFT * 3.6)
    stack = layer_stack(
        [
            ("textured polymer cover", cfg.WHITE),
            ("layered graphics + icons", cfg.GOLD),
            ("support / backing layers", cfg.BLUE),
            ("sealed air bladder", cfg.PURPLE),
        ]
    ).shift(RIGHT * 2.0 + UP * 0.7)
    note = VGroup(
        Text("Exact formula? Not public.", font_size=27, color=cfg.MUTED),
        Text("Engineering effect? Visible.", font_size=27, color=cfg.MUTED),
    ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
    note.move_to(LEFT * 3.05 + DOWN * 2.75)
    note.set_stroke(cfg.BLACKISH, width=3, opacity=0.8, background=True)

    boot = Polygon(
        [-0.9, -0.25, 0],
        [0.45, -0.25, 0],
        [0.85, 0.03, 0],
        [0.2, 0.28, 0],
        [-0.95, 0.18, 0],
        color=cfg.ORANGE,
        fill_color=cfg.ORANGE,
        fill_opacity=0.75,
    ).scale(0.85).move_to(RIGHT * 4.9 + DOWN * 1.35)
    contact = VGroup(*[Arc(radius=0.38 + i * 0.18, angle=PI / 1.7, color=cfg.GOLD, stroke_width=3, stroke_opacity=0.5 / (i + 1)) for i in range(4)])
    contact.rotate(PI / 9).move_to(RIGHT * 3.5 + DOWN * 1.0)
    airflow = VGroup(*[Arrow(LEFT * 0.6, RIGHT * 0.55, color=cfg.CYAN, stroke_width=3, max_tip_length_to_length_ratio=0.18).shift(UP * y) for y in [-0.55, -0.2, 0.15, 0.5]])
    airflow.move_to(LEFT * 0.15 + DOWN * 1.55)
    air_label = small_label("air feels texture", cfg.CYAN, 26).next_to(airflow, UP, buff=0.18)
    boot_label = small_label("boot feels grip", cfg.GOLD, 26).next_to(boot, DOWN, buff=0.18)

    paced_play(scene, FadeIn(caption, shift=DOWN * 0.2), FadeIn(ball, scale=0.95), run_time=0.8)
    paced_play(scene, ball.animate.shift(RIGHT * 0.5), FadeIn(stack, shift=LEFT * 0.2), run_time=0.9)
    for row in stack:
        paced_play(scene, Indicate(row[0], color=row[0].get_stroke_color(), scale_factor=1.02), run_time=0.28)
    paced_play(scene, FadeIn(note, shift=UP * 0.1), run_time=0.45)
    paced_play(scene, GrowArrow(airflow[0]), GrowArrow(airflow[1]), GrowArrow(airflow[2]), GrowArrow(airflow[3]), FadeIn(air_label), run_time=0.8)
    paced_play(scene, FadeIn(boot, shift=LEFT * 0.4), FadeIn(boot_label), Create(contact), run_time=0.85)
    paced_play(scene, contact.animate.scale(1.12).set_opacity(0.55), rate_func=there_and_back, run_time=0.8)
    narration_wait(scene, 0.9)
    end_scene(scene, scene_start, "02")
