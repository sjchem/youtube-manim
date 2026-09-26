"""Render the complete film as one deterministic sequence.

Chapters 01, 03, 08 and 10 use real 3D geometry and camera movement. Each one
restores the default orientation (phi = 0, theta = -90 degrees), the zoom, the
background colour and its fixed-in-frame registrations before the next flat
chapter begins, so the sequence is order-independent.
"""

from __future__ import annotations

from manim import ThreeDScene

import config as cfg
from manim_scenes.scene_01_hook import play_scene as scene_01
from manim_scenes.scene_02_what_is_a_set import play_scene as scene_02
from manim_scenes.scene_03_subsets import play_scene as scene_03
from manim_scenes.scene_04_empty_set import play_scene as scene_04
from manim_scenes.scene_05_venn import play_scene as scene_05
from manim_scenes.scene_06_union_intersection import play_scene as scene_06
from manim_scenes.scene_07_numbers_challenge import play_scene as scene_07
from manim_scenes.scene_08_complement import play_scene as scene_08
from manim_scenes.scene_09_pizza_challenge import play_scene as scene_09
from manim_scenes.scene_10_de_morgan_one import play_scene as scene_10
from manim_scenes.scene_11_de_morgan_two import play_scene as scene_11
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
    """Set Theory: From Sets to De Morgan's Laws - complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
