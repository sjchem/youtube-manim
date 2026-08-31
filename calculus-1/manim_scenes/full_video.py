"""Render the complete Part 1 film as one deterministic sequence."""

from __future__ import annotations

from manim import Scene

import config as cfg
from manim_scenes.scene_01_moving_car import play_scene as scene_01
from manim_scenes.scene_02_limits import play_scene as scene_02
from manim_scenes.scene_03_hole_in_graph import play_scene as scene_03
from manim_scenes.scene_04_continuity import play_scene as scene_04
from manim_scenes.scene_05_trig_limit import play_scene as scene_05
from manim_scenes.scene_06_secant_to_tangent import play_scene as scene_06
from manim_scenes.scene_07_local_linearity import play_scene as scene_07
from manim_scenes.scene_08_derivative_meaning import play_scene as scene_08
from manim_scenes.scene_09_subscribe import play_scene as scene_09


class FullVideo(Scene):
    """Visual Calculus: From Limits to Derivatives — Part 1, complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in (
            scene_01,
            scene_02,
            scene_03,
            scene_04,
            scene_05,
            scene_06,
            scene_07,
            scene_08,
            scene_09,
        ):
            play(self)
