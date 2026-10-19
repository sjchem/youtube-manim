"""Render the complete film as one deterministic sequence.

Every chapter is a ``play_scene(scene)`` function that themes the scene, lands
on its configured duration, fades out, and restores the flat front camera
(phi = 0, theta = -90 degrees, zoom 1, no fixed-in-frame registrations), so the
3D chapters (04, 08, 09, 17) can sit between flat ones. The faint static bubble
layer is shared and survives every chapter's fade. The only randomness — the
electron-cloud and electron-sea samples — comes from ``config.SEED``.
"""

from __future__ import annotations

from manim import ThreeDScene

import config as cfg
from manim_scenes.scene_01_invisible_force import play_scene as scene_01
from manim_scenes.scene_02_promise import play_scene as scene_02
from manim_scenes.scene_03_pushes_and_pulls import play_scene as scene_03
from manim_scenes.scene_04_energy_landscape import play_scene as scene_04
from manim_scenes.scene_05_stable_bond import play_scene as scene_05
from manim_scenes.scene_06_valence_lewis import play_scene as scene_06
from manim_scenes.scene_07_covalent import play_scene as scene_07
from manim_scenes.scene_08_sigma_overlap import play_scene as scene_08
from manim_scenes.scene_09_pi_bonds import play_scene as scene_09
from manim_scenes.scene_10_electron_transfer import play_scene as scene_10
from manim_scenes.scene_11_ionic_lattice import play_scene as scene_11
from manim_scenes.scene_12_polarity import play_scene as scene_12
from manim_scenes.scene_13_metallic import play_scene as scene_13
from manim_scenes.scene_14_length_strength import play_scene as scene_14
from manim_scenes.scene_15_octet_limits import play_scene as scene_15
from manim_scenes.scene_16_big_picture import play_scene as scene_16
from manim_scenes.scene_17_geometry_teaser import play_scene as scene_17
from manim_scenes.scene_18_subscribe import play_scene as scene_18

CHAPTERS = (
    scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08, scene_09,
    scene_10, scene_11, scene_12, scene_13, scene_14, scene_15, scene_16, scene_17, scene_18,
)


class FullVideo(ThreeDScene):
    """Chemical Bonding, Explained Visually — complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
