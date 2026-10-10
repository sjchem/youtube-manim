"""Render the complete film as one deterministic sequence.

Every chapter is a ``play_scene(scene)`` function that themes the scene, lands
on its configured duration, fades out, and restores the flat front camera
(phi = 0, theta = -90 degrees, zoom 1, no fixed-in-frame registrations), so the
3D chapters (06, 10, 15, 18) can sit between flat ones. The faint static bubble
layer is shared and survives every chapter's fade. The only randomness — the
electron-cloud samples — comes from ``config.SEED``.
"""

from __future__ import annotations

from manim import ThreeDScene

import config as cfg
from manim_scenes.scene_01_hook import play_scene as scene_01
from manim_scenes.scene_02_from_shape import play_scene as scene_02
from manim_scenes.scene_03_nuclear_pull import play_scene as scene_03
from manim_scenes.scene_04_shielding import play_scene as scene_04
from manim_scenes.scene_05_radius_across import play_scene as scene_05
from manim_scenes.scene_06_radius_down import play_scene as scene_06
from manim_scenes.scene_07_ions import play_scene as scene_07
from manim_scenes.scene_08_isoelectronic import play_scene as scene_08
from manim_scenes.scene_09_ionization import play_scene as scene_09
from manim_scenes.scene_10_ionization_landscape import play_scene as scene_10
from manim_scenes.scene_11_exceptions import play_scene as scene_11
from manim_scenes.scene_12_electron_gain import play_scene as scene_12
from manim_scenes.scene_13_fluorine_chlorine import play_scene as scene_13
from manim_scenes.scene_14_electronegativity import play_scene as scene_14
from manim_scenes.scene_15_bond_landscape import play_scene as scene_15
from manim_scenes.scene_16_sodium_chloride import play_scene as scene_16
from manim_scenes.scene_17_behaviour_map import play_scene as scene_17
from manim_scenes.scene_18_heat_maps import play_scene as scene_18
from manim_scenes.scene_19_ending import play_scene as scene_19
from manim_scenes.scene_20_subscribe import play_scene as scene_20

CHAPTERS = (
    scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08, scene_09, scene_10,
    scene_11, scene_12, scene_13, scene_14, scene_15, scene_16, scene_17, scene_18, scene_19, scene_20,
)


class FullVideo(ThreeDScene):
    """Periodic Trends, Explained Visually — complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
