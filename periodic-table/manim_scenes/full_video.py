"""Render the complete film as one deterministic sequence.

Every chapter is a ``play_scene(scene)`` function that themes the scene, lands
on its configured duration, fades out, and restores the flat front camera
(phi = 0, theta = -90 degrees, zoom 1, no fixed-in-frame registrations), so the
3D chapters (01, 04, 08, 12, 14, 15, 16) can sit between flat ones in any order.
The faint static bubble layer is shared and survives every chapter's fade.
"""

from __future__ import annotations

from manim import ThreeDScene

import config as cfg
from manim_scenes.scene_01_hook import play_scene as scene_01
from manim_scenes.scene_02_atomic_number import play_scene as scene_02
from manim_scenes.scene_03_electrons import play_scene as scene_03
from manim_scenes.scene_04_four_shapes import play_scene as scene_04
from manim_scenes.scene_05_period_one import play_scene as scene_05
from manim_scenes.scene_06_period_two import play_scene as scene_06
from manim_scenes.scene_07_groups import play_scene as scene_07
from manim_scenes.scene_08_group_chemistry import play_scene as scene_08
from manim_scenes.scene_09_period_four import play_scene as scene_09
from manim_scenes.scene_10_filling_order import play_scene as scene_10
from manim_scenes.scene_11_f_block import play_scene as scene_11
from manim_scenes.scene_12_four_blocks import play_scene as scene_12
from manim_scenes.scene_13_periods import play_scene as scene_13
from manim_scenes.scene_14_trends import play_scene as scene_14
from manim_scenes.scene_15_reconstruction import play_scene as scene_15
from manim_scenes.scene_16_subscribe import play_scene as scene_16

CHAPTERS = (
    scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08,
    scene_09, scene_10, scene_11, scene_12, scene_13, scene_14, scene_15, scene_16,
)


class FullVideo(ThreeDScene):
    """Why Does the Periodic Table Have This Shape? — complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
