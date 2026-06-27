from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    four_panel_map,
    narration_wait,
    paced_play,
    scene_caption,
    small_label,
    twenty_panel_map,
    wavy_path,
)


class Scene04PanelGeometry(MovingCameraScene):
    """Show why fewer panels alone is not the whole story."""

    def construct(self) -> None:
        construct_scene_04(self)


def construct_scene_04(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    caption = scene_caption("Fewer panels is not the whole trick", color=cfg.WHITE)
    many = twenty_panel_map(radius=1.25).shift(LEFT * 4.1 + UP * 0.3)
    four = four_panel_map(radius=1.25).shift(RIGHT * 4.1 + UP * 0.3)
    arrow = Arrow(LEFT * 1.6, RIGHT * 1.6, color=cfg.CYAN, stroke_width=6, max_tip_length_to_length_ratio=0.14)
    arrow_label = small_label("topology changes", cfg.CYAN, 28).next_to(arrow, UP, buff=0.2)

    tetra = VGroup(
        Polygon([0, 1.0, 0], [-1.0, -0.7, 0], [1.0, -0.7, 0], color=cfg.PURPLE, fill_color=cfg.PURPLE, fill_opacity=0.08),
        Line([0, 1.0, 0], [0, -0.15, 0], color=cfg.PURPLE, stroke_opacity=0.55),
        Line([-1.0, -0.7, 0], [0, -0.15, 0], color=cfg.PURPLE, stroke_opacity=0.55),
        Line([1.0, -0.7, 0], [0, -0.15, 0], color=cfg.PURPLE, stroke_opacity=0.55),
    ).scale(0.88).move_to(DOWN * 2.55 + LEFT * 2.65)
    tetra_label = small_label("tetrahedron idea", cfg.PURPLE, 28).next_to(tetra, DOWN, buff=0.18)

    seam_sample = VGroup()
    base = Line(LEFT * 1.7, RIGHT * 1.7, color=cfg.MUTED, stroke_width=6)
    groove = wavy_path(LEFT * 1.7, RIGHT * 1.7, amp=0.18, waves=2)
    groove.set_stroke(cfg.GOLD, width=8, opacity=0.95)
    dots = VGroup(*[Dot([x, 0.18 * ((i % 2) * 2 - 1), 0], radius=0.045, color=cfg.CYAN) for i, x in enumerate([-1.25, -0.75, -0.25, 0.25, 0.75, 1.25])])
    seam_sample.add(base, groove, dots).scale(0.9).move_to(DOWN * 2.55 + RIGHT * 2.85)
    seam_label = small_label("deep seams + debossed texture", cfg.GOLD, 28).next_to(seam_sample, DOWN, buff=0.18)

    warning = Text("A smooth four-panel ball would be a different machine.", font_size=24, color=cfg.ORANGE, weight=BOLD)
    warning.move_to(DOWN * 4.1)
    warning.set_stroke(cfg.BLACKISH, width=3, opacity=0.86, background=True)

    paced_play(scene, FadeIn(caption), FadeIn(many, shift=RIGHT * 0.1), run_time=0.75)
    paced_play(scene, GrowArrow(arrow), FadeIn(arrow_label), FadeIn(four, shift=LEFT * 0.1), run_time=0.9)
    paced_play(scene, FadeIn(tetra, shift=UP * 0.15), FadeIn(tetra_label), run_time=0.7)
    paced_play(scene, FadeIn(seam_sample, shift=UP * 0.15), FadeIn(seam_label), run_time=0.75)
    paced_play(scene, Indicate(groove, color=cfg.ORANGE, scale_factor=1.04), run_time=0.65)
    paced_play(scene, FadeIn(warning, shift=UP * 0.15), run_time=0.55)
    narration_wait(scene, 0.8)
    end_scene(scene, scene_start, "04")
