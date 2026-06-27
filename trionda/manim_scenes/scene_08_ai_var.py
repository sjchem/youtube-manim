from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, make_player, narration_wait, paced_play, scene_caption, small_label
from utils.physics_models import offside_tracking_points


class Scene08AIVAR(MovingCameraScene):
    """Combine ball data, player tracking, and AI into an offside decision."""

    def construct(self) -> None:
        construct_scene_08(self)


def construct_scene_08(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    caption = scene_caption("Motion data becomes a referee tool", color=cfg.CYAN)
    pitch = Rectangle(width=9.4, height=4.4, color=cfg.GREEN, stroke_width=3, fill_color="#0A3A2A", fill_opacity=0.3)
    pitch.move_to(LEFT * 2.0 + DOWN * 0.1)
    mid = Line(pitch.get_top() + DOWN * 4.4 / 2, pitch.get_bottom() + UP * 4.4 / 2, color=cfg.GREEN, stroke_opacity=0.55)
    pts = offside_tracking_points()
    passer = make_player(cfg.BLUE, "passer").move_to(pitch.get_center() + np.array(pts["passer"]))
    attacker = make_player(cfg.GOLD, "attacker").move_to(pitch.get_center() + np.array(pts["attacker"]))
    defender = make_player(cfg.RED, "defender").move_to(pitch.get_center() + np.array(pts["defender"]))
    ball = Dot(pitch.get_center() + np.array(pts["ball"]), radius=0.1, color=cfg.WHITE)
    offside_line = DashedLine(
        pitch.get_center() + np.array(pts["offside_line_top"]),
        pitch.get_center() + np.array(pts["offside_line_bottom"]),
        color=cfg.ORANGE,
        stroke_width=5,
        dash_length=0.18,
    )
    ball_signal = VGroup(*[Circle(radius=0.2 + i * 0.18, color=cfg.CYAN, stroke_width=2, stroke_opacity=0.55 / (i + 1)).move_to(ball) for i in range(4)])

    tracking_dots = VGroup()
    for mob, color in [(passer, cfg.BLUE), (attacker, cfg.GOLD), (defender, cfg.RED)]:
        tracking_dots.add(Dot(mob.get_center() + UP * 0.55, radius=0.055, color=color))

    data_panel = RoundedRectangle(width=4.4, height=4.7, corner_radius=0.12, color=cfg.CYAN, fill_color=cfg.PANEL, fill_opacity=0.72)
    data_panel.to_edge(RIGHT, buff=0.55).shift(DOWN * 0.05)
    rows = VGroup(
        small_label("ball touch time", cfg.CYAN, 28),
        small_label("player positions", cfg.BLUE, 28),
        small_label("AI alignment", cfg.PURPLE, 28),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(data_panel).shift(UP * 0.8 + LEFT * 0.1)
    row_colors = [cfg.CYAN, cfg.BLUE, cfg.PURPLE]
    arrows = VGroup(
        *[
            Arrow(
                row.get_right() + RIGHT * 0.1,
                data_panel.get_right() + LEFT * 0.7 + UP * (0.95 - i * 0.45),
                color=row_colors[i],
                stroke_width=3,
            )
            for i, row in enumerate(rows)
        ]
    )
    decision = VGroup(
        RoundedRectangle(width=4.0, height=0.85, corner_radius=0.1, color=cfg.GREEN, fill_color=cfg.GREEN, fill_opacity=0.18),
        Text("CHECK COMPLETE", font_size=24, color=cfg.GREEN, weight=BOLD),
    ).move_to(data_panel.get_bottom() + UP * 0.75)

    final_line = Text("materials + seams + air + data = Trionda", font_size=38, color=cfg.WHITE, weight=BOLD)
    final_line.to_edge(DOWN, buff=0.32)
    final_line.set_stroke(cfg.BLACKISH, width=4, opacity=0.85, background=True)

    paced_play(scene, FadeIn(caption), FadeIn(pitch), Create(mid), run_time=0.75)
    paced_play(scene, FadeIn(passer), FadeIn(attacker), FadeIn(defender), FadeIn(ball), run_time=0.75)
    paced_play(scene, Create(offside_line), FadeIn(tracking_dots), Create(ball_signal), run_time=0.8)
    paced_play(scene, FadeIn(data_panel, shift=LEFT * 0.2), FadeIn(rows), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=1.0)
    paced_play(scene, ReplacementTransform(ball_signal.copy(), decision), run_time=0.8)
    paced_play(scene, FadeIn(final_line, shift=UP * 0.15), run_time=0.75)
    narration_wait(scene, 1.0)
    end_scene(scene, scene_start, "08")
