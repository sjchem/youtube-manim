"""Render the complete Part 3 film as one deterministic sequence.

The scene is a ThreeDScene so the dimensional chapters (10, 11, 13) can open
the camera mid-film; every chapter returns the camera to the flat orientation
before it hands over, so the 2D chapters are unaffected.
"""

from __future__ import annotations

from manim import ThreeDScene

import config as cfg
from manim_scenes.scene_01_reverse_problem import play_scene as scene_01
from manim_scenes.scene_02_missing_constant import play_scene as scene_02
from manim_scenes.scene_03_equation_of_change import play_scene as scene_03
from manim_scenes.scene_04_slope_field import play_scene as scene_04
from manim_scenes.scene_05_exponential_growth import play_scene as scene_05
from manim_scenes.scene_06_exponential_decay import play_scene as scene_06
from manim_scenes.scene_07_newton_cooling import play_scene as scene_07
from manim_scenes.scene_08_separation_of_variables import play_scene as scene_08
from manim_scenes.scene_09_initial_conditions import play_scene as scene_09
from manim_scenes.scene_10_spring_oscillation import play_scene as scene_10
from manim_scenes.scene_11_area_to_volume import play_scene as scene_11
from manim_scenes.scene_12_one_idea import play_scene as scene_12
from manim_scenes.scene_13_equation_to_future import play_scene as scene_13
from manim_scenes.scene_14_modern_science import play_scene as scene_14
from manim_scenes.scene_15_synthesis import play_scene as scene_15
from manim_scenes.scene_16_subscribe import play_scene as scene_16

CHAPTERS = (
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
    scene_15,
    scene_16,
)


class FullVideo(ThreeDScene):
    """Visual Calculus: From Integrals to Differential Equations — Part 3, complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
