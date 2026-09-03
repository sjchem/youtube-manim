"""Render the complete Part 2 film as one deterministic sequence."""

from __future__ import annotations

from manim import Scene

import config as cfg
from manim_scenes.scene_01_velocity_to_distance import play_scene as scene_01
from manim_scenes.scene_02_riemann_sums import play_scene as scene_02
from manim_scenes.scene_03_what_is_dx import play_scene as scene_03
from manim_scenes.scene_04_fundamental_theorem import play_scene as scene_04
from manim_scenes.scene_05_beautiful_example import play_scene as scene_05
from manim_scenes.scene_06_derivative_new_function import play_scene as scene_06
from manim_scenes.scene_07_maxima_minima import play_scene as scene_07
from manim_scenes.scene_08_optimization_garden import play_scene as scene_08
from manim_scenes.scene_09_reverse_problem import play_scene as scene_09
from manim_scenes.scene_10_substitution import play_scene as scene_10
from manim_scenes.scene_11_integration_by_parts import play_scene as scene_11
from manim_scenes.scene_12_area_between_curves import play_scene as scene_12
from manim_scenes.scene_13_synthesis import play_scene as scene_13
from manim_scenes.scene_14_subscribe import play_scene as scene_14


class FullVideo(Scene):
    """Visual Calculus: From Derivatives to Integrals — Part 2, complete."""

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
            scene_10,
            scene_11,
            scene_12,
            scene_13,
            scene_14,
        ):
            play(self)
