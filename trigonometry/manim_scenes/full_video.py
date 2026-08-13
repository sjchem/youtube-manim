"""Render the complete visual trigonometry course as one deterministic film."""

from __future__ import annotations

from manim import Scene

import config as cfg
from manim_scenes.scene_01_hook import play_scene as scene_01
from manim_scenes.scene_02_angles import play_scene as scene_02
from manim_scenes.scene_03_coordinates_pythagoras import play_scene as scene_03
from manim_scenes.scene_04_ratios import play_scene as scene_04
from manim_scenes.scene_05_six_functions import play_scene as scene_05
from manim_scenes.scene_06_special_angles import play_scene as scene_06
from manim_scenes.scene_07_unit_circle import play_scene as scene_07
from manim_scenes.scene_08_unrolling import play_scene as scene_08
from manim_scenes.scene_09_wave_controls import play_scene as scene_09
from manim_scenes.scene_10_inverse_trig import play_scene as scene_10
from manim_scenes.scene_11_identities import play_scene as scene_11
from manim_scenes.scene_12_non_right_triangles import play_scene as scene_12
from manim_scenes.scene_13_real_sound import play_scene as scene_13
from manim_scenes.scene_14_fourier import play_scene as scene_14
from manim_scenes.scene_15_euler import play_scene as scene_15
from manim_scenes.scene_16_synthesis import play_scene as scene_16
from manim_scenes.scene_17_subscribe import play_scene as scene_17


class FullVideo(Scene):
    """The complete 14-minute visualized trigonometry video."""

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
            scene_15,
            scene_16,
            scene_17,
        ):
            play(self)
