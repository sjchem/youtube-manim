"""Render the complete film as one deterministic sequence.

Every chapter is a ``play_scene(scene)`` function that themes the scene, lands
on its configured duration, fades out, and restores the flat front camera
(phi = 0, theta = -90 degrees, zoom 1, no fixed-in-frame registrations), so the
3D chapters (03, 11) can sit between flat ones. The faint static bubble layer
is shared and survives every chapter's fade. The only randomness (chapter 11's
Galton board) comes from ``config.SEED``.
"""

from __future__ import annotations

from manim import ThreeDScene

import config as cfg
from manim_scenes.scene_01_mystery import play_scene as scene_01
from manim_scenes.scene_02_start_small import play_scene as scene_02
from manim_scenes.scene_03_cube import play_scene as scene_03
from manim_scenes.scene_04_triangle_builds import play_scene as scene_04
from manim_scenes.scene_05_choice_machines import play_scene as scene_05
from manim_scenes.scene_06_combinations import play_scene as scene_06
from manim_scenes.scene_07_theorem import play_scene as scene_07
from manim_scenes.scene_08_exponents import play_scene as scene_08
from manim_scenes.scene_09_pascal_rule import play_scene as scene_09
from manim_scenes.scene_10_paths import play_scene as scene_10
from manim_scenes.scene_11_coin_flips import play_scene as scene_11
from manim_scenes.scene_12_payoff import play_scene as scene_12
from manim_scenes.scene_13_subscribe import play_scene as scene_13

CHAPTERS = (
    scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07,
    scene_08, scene_09, scene_10, scene_11, scene_12, scene_13,
)


class FullVideo(ThreeDScene):
    """Why Does Pascal's Triangle Know Algebra? — complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
