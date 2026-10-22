"""Render the complete film as one deterministic sequence.

Every chapter is a ``play_scene(scene)`` function that themes the scene, lands
on its configured duration, and fades out everything except the faint shared
bubble layer. All 3D is drawn by projected stages inside an ordinary Scene,
so there is no camera state to reset between chapters. The only randomness —
the scrambled start of the repulsion demo (chapter 03) and the oxygen
droplets (chapter 21) — comes from ``config.SEED``.
"""

from __future__ import annotations

from manim import Scene

import config as cfg
from manim_scenes.scene_01_shape_mystery import play_scene as scene_01
from manim_scenes.scene_02_lewis_is_flat import play_scene as scene_02
from manim_scenes.scene_03_regions_repel import play_scene as scene_03
from manim_scenes.scene_04_counting_regions import play_scene as scene_04
from manim_scenes.scene_05_linear_planar import play_scene as scene_05
from manim_scenes.scene_06_tetrahedron import play_scene as scene_06
from manim_scenes.scene_07_ammonia import play_scene as scene_07
from manim_scenes.scene_08_water import play_scene as scene_08
from manim_scenes.scene_09_five_regions import play_scene as scene_09
from manim_scenes.scene_10_tbp_family import play_scene as scene_10
from manim_scenes.scene_11_six_regions import play_scene as scene_11
from manim_scenes.scene_12_flat_from_six import play_scene as scene_12
from manim_scenes.scene_13_mixing_orbitals import play_scene as scene_13
from manim_scenes.scene_14_sp2_sp3 import play_scene as scene_14
from manim_scenes.scene_15_methane_ethene import play_scene as scene_15
from manim_scenes.scene_16_two_models import play_scene as scene_16
from manim_scenes.scene_17_bond_dipoles import play_scene as scene_17
from manim_scenes.scene_18_symmetry_polarity import play_scene as scene_18
from manim_scenes.scene_19_predict import play_scene as scene_19
from manim_scenes.scene_20_big_picture import play_scene as scene_20
from manim_scenes.scene_21_oxygen_magnet import play_scene as scene_21
from manim_scenes.scene_22_subscribe import play_scene as scene_22

CHAPTERS = (
    scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08, scene_09, scene_10, scene_11,
    scene_12, scene_13, scene_14, scene_15, scene_16, scene_17, scene_18, scene_19, scene_20, scene_21, scene_22,
)


class FullVideo(Scene):
    """Molecular Geometry, Explained Visually — complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
