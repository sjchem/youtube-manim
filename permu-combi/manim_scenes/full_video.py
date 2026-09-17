"""Render the complete film as one deterministic sequence.

Chapters 01, 04 and 11 use real 3D geometry and camera movement. Each one
restores the default orientation (phi = 0, theta = -90 degrees), the zoom, the
background colour and its fixed-in-frame registrations before the next flat
chapter begins, so the sequence is order-independent.
"""

from __future__ import annotations

from manim import ThreeDScene

import config as cfg
from manim_scenes.scene_01_lock_paradox import play_scene as scene_01
from manim_scenes.scene_02_choices_multiply import play_scene as scene_02
from manim_scenes.scene_03_factorial import play_scene as scene_03
from manim_scenes.scene_04_permutations import play_scene as scene_04
from manim_scenes.scene_05_order_matters import play_scene as scene_05
from manim_scenes.scene_06_block_gap import play_scene as scene_06
from manim_scenes.scene_07_combinations import play_scene as scene_07
from manim_scenes.scene_08_quiz import play_scene as scene_08
from manim_scenes.scene_09_alike_geometry import play_scene as scene_09
from manim_scenes.scene_10_symmetry import play_scene as scene_10
from manim_scenes.scene_11_poker import play_scene as scene_11
from manim_scenes.scene_12_zero_factorial import play_scene as scene_12
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
    """Permutations & Combinations Explained Visually - complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
