"""Scene 7: Trionda as a modern design case study."""

from __future__ import annotations

from math import cos, sin

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, label_text, narration_wait, paced_play, speed_graph, trionda_image_ball


class Scene07TriondaDesign(Scene):
    """Use Trionda's four-panel design to connect geometry and flight."""

    def construct(self) -> None:
        play_scene(self)


def rotation_arrows(radius: float = 1.18) -> VGroup:
    """Create bold spin arrows for the final Trionda rotation."""
    arrows = VGroup()
    for shift in (-0.17, 0.18):
        arc = Arc(radius=radius, start_angle=0.12 * PI + shift, angle=0.76 * PI, color=cfg.ORANGE, stroke_width=9)
        end_angle = 0.12 * PI + shift + 0.76 * PI
        tip = Triangle(color=cfg.ORANGE, fill_color=cfg.ORANGE, fill_opacity=1).scale(0.12)
        tip.move_to([cos(end_angle) * radius, sin(end_angle) * radius, 0])
        tip.rotate(end_angle - PI / 2)
        arrows.add(arc, tip)
    return arrows


def four_panel_ball(radius: float = 1.05) -> VGroup:
    """Create a clear four-panel construction graphic inside a ball shell."""
    halo = Circle(radius=radius * 1.07, stroke_color=cfg.CYAN, stroke_width=10, stroke_opacity=0.12)
    shell = Circle(
        radius=radius,
        fill_color=cfg.WHITE,
        fill_opacity=0.12,
        stroke_color=cfg.CYAN,
        stroke_width=4,
    )
    panels = VGroup()
    for index, color in enumerate((cfg.RED, cfg.GREEN, cfg.BLUE, cfg.GOLD)):
        panel = AnnularSector(
            inner_radius=radius * 0.12,
            outer_radius=radius * 0.88,
            angle=PI / 2 - 0.08,
            start_angle=index * PI / 2 + 0.04,
            fill_color=color,
            fill_opacity=0.86,
            stroke_color=cfg.WHITE,
            stroke_width=2.2,
        )
        panels.add(panel)
    center = Dot(radius=radius * 0.1, color=cfg.WHITE)
    return VGroup(halo, shell, panels, center)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())
    title = label_text("Trionda is a geometry problem in the air", cfg.FONT_SIZES["subtitle"], cfg.WHITE, weight=BOLD).to_edge(UP, buff=0.55)
    paced_play(scene, FadeIn(title), run_time=0.55)

    ball_center = [-1.3, 0.15, 0]
    panel_graphic = four_panel_ball(radius=1.05).move_to(ball_center)
    real_ball = trionda_image_ball(width=2.0).move_to(ball_center)
    panels = Text("4 panels", font_size=36, color=cfg.GOLD, weight=BOLD).next_to(panel_graphic, DOWN, buff=0.35)
    graph = speed_graph(width=5.4, height=2.5).move_to([3.7, 0.15, 0])

    paced_play(scene, FadeIn(panel_graphic, scale=0.78), FadeIn(panels, shift=UP * 0.12), run_time=1.1)
    paced_play(scene, FadeIn(graph, shift=LEFT * 0.25), run_time=1.0)

    notes = VGroup(
        label_text("roughness moves transition", cfg.FONT_SIZES["small"], cfg.CYAN),
        label_text("wake controls force", cfg.FONT_SIZES["small"], cfg.GREEN),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.75, -2.15, 0])
    paced_play(scene, FadeIn(notes), run_time=0.8)

    factors = VGroup(
        label_text("Speed", 31, cfg.CYAN, weight=BOLD),
        label_text("Spin", 31, cfg.ORANGE, weight=BOLD),
        label_text("Altitude", 31, cfg.PURPLE, weight=BOLD),
        label_text("Humidity", 31, cfg.BLUE, weight=BOLD),
        label_text("Strike", 31, cfg.GOLD, weight=BOLD),
    ).arrange(RIGHT, buff=0.5).move_to([0, -3.15, 0])
    paced_play(
        scene,
        LaggedStart(*[FadeIn(item, shift=UP * 0.14) for item in factors], lag_ratio=0.24),
        run_time=2.2,
    )

    spin_marks = rotation_arrows().move_to(real_ball.get_center())
    paced_play(
        scene,
        FadeOut(panel_graphic, scale=0.9),
        FadeIn(real_ball, scale=0.9),
        run_time=0.8,
    )
    paced_play(
        scene,
        FadeIn(spin_marks, scale=1.08),
        Rotate(real_ball, angle=TAU * 1.5, about_point=real_ball.get_center(), rate_func=linear),
        run_time=4.2,
    )
    narration_wait(scene, 1.0)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["07"])
