"""Render the complete film as one deterministic sequence.

Chapters 01 and 11 use real 3D geometry and camera movement. Both restore the
default orientation (phi = 0, theta = -90 degrees), zoom and fixed-text
registrations before the next flat chapter.
"""

from __future__ import annotations

from manim import ThreeDScene

import config as cfg
from manim_scenes.scene_01_everyday_machines import play_scene as scene_01
from manim_scenes.scene_02_the_rule import play_scene as scene_02
from manim_scenes.scene_03_one_output import play_scene as scene_03
from manim_scenes.scene_04_domain_range import play_scene as scene_04
from manim_scenes.scene_05_machine_to_graph import play_scene as scene_05
from manim_scenes.scene_06_vertical_line_test import play_scene as scene_06
from manim_scenes.scene_07_transformations import play_scene as scene_07
from manim_scenes.scene_08_composition import play_scene as scene_08
from manim_scenes.scene_09_inverse import play_scene as scene_09
from manim_scenes.scene_10_no_inverse import play_scene as scene_10
from manim_scenes.scene_11_higher_dimensions import play_scene as scene_11
from manim_scenes.scene_12_why_it_matters import play_scene as scene_12
from manim_scenes.scene_13_finale import play_scene as scene_13
from manim_scenes.scene_14_subscribe import play_scene as scene_14

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
)


class FullVideo(ThreeDScene):
    """What Does a Function Actually Do? - complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
