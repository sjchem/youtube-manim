from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, equation, narration_wait, paced_play, scene_caption, small_label
from utils.physics_models import drag_curve_samples


class Scene06DragCrisis(MovingCameraScene):
    """Introduce drag crisis with a moving football marker."""

    def construct(self) -> None:
        construct_scene_06(self)


def _curve_points(axes: Axes, critical_speed: float) -> list[np.ndarray]:
    return [axes.c2p(sample.speed, sample.cd) for sample in drag_curve_samples(critical_speed)]


def construct_scene_06(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    caption = scene_caption("Drag crisis: when the air changes its mind", color=cfg.ORANGE)
    axes = Axes(
        x_range=[5, 40, 5],
        y_range=[0.15, 0.55, 0.1],
        x_length=9.6,
        y_length=4.4,
        tips=False,
        axis_config={"color": cfg.MUTED, "stroke_width": 2},
    ).move_to(DOWN * 0.25)
    labels = axes.get_axis_labels(
        Text("speed", font_size=26, color=cfg.CYAN),
        MathTex("C_D", font_size=32, color=cfg.WHITE),
    )
    j_curve = VMobject().set_points_smoothly(_curve_points(axes, 23.0)).set_stroke(cfg.ORANGE, width=4)
    t_curve = VMobject().set_points_smoothly(_curve_points(axes, 18.0)).set_stroke(cfg.CYAN, width=5)
    j_label = small_label("transition in play speeds", cfg.ORANGE, 24).move_to(RIGHT * 3.45 + UP * 2.65)
    j_pointer = Arrow(
        j_label.get_bottom() + DOWN * 0.05,
        axes.c2p(24.5, 0.43),
        color=cfg.ORANGE,
        stroke_width=3,
        max_tip_length_to_length_ratio=0.12,
        buff=0.08,
    )
    t_label = small_label("earlier, controlled transition", cfg.CYAN, 24).move_to(axes.c2p(20, 0.25))
    band = Rectangle(width=axes.x_axis.unit_size * 14, height=4.5, color=cfg.PURPLE, fill_color=cfg.PURPLE, fill_opacity=0.08, stroke_opacity=0)
    band.move_to(axes.c2p(23, 0.35))
    band_label = small_label("normal free-kick zone", cfg.PURPLE, 24).next_to(band, UP, buff=0.08)

    marker = Circle(radius=0.12, color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=1).move_to(axes.c2p(8, 0.49))
    trail = TracedPath(marker.get_center, stroke_color=cfg.GOLD, stroke_width=3, dissipating_time=1.2)
    equation_mob = equation(r"F_D=\frac12\rho v^2 C_D A", color=cfg.WHITE, font_size=54).to_corner(DL, buff=0.55)
    nuance = Text("Not minimum drag. Predictable drag.", font_size=36, color=cfg.GREEN, weight=BOLD).to_edge(DOWN, buff=0.38)
    nuance.set_stroke(cfg.BLACKISH, width=3, opacity=0.85, background=True)

    paced_play(scene, FadeIn(caption), FadeIn(axes), FadeIn(labels), FadeIn(band), FadeIn(band_label), run_time=0.85)
    paced_play(scene, Create(j_curve), FadeIn(j_label), GrowArrow(j_pointer), run_time=0.9)
    paced_play(scene, Create(t_curve), FadeIn(t_label), run_time=0.95)
    scene.add(trail)
    paced_play(scene, FadeIn(marker), Write(equation_mob), run_time=0.65)
    paced_play(scene, MoveAlongPath(marker, t_curve), run_time=2.0, rate_func=linear)
    paced_play(scene, FadeIn(nuance, shift=UP * 0.15), run_time=0.6)
    narration_wait(scene, 0.85)
    end_scene(scene, scene_start, "06")
