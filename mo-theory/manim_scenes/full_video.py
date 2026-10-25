"""Render the complete film as one deterministic sequence.

Every chapter is a ``play_scene(scene)`` function that themes the scene, lands
on its configured duration, and fades out everything except the faint shared
bubble layer. All 3D is drawn by projected stages inside an ordinary Scene,
so there is no camera state to reset between chapters. The only randomness —
the liquid-oxygen and liquid-nitrogen pours and the spins in a field — comes
from ``config.SEED``.
"""

from __future__ import annotations

from manim import Scene

import config as cfg
from manim_scenes.scene_01_oxygen_mystery import play_scene as scene_01
from manim_scenes.scene_02_two_pictures import play_scene as scene_02
from manim_scenes.scene_03_waves import play_scene as scene_03
from manim_scenes.scene_04_lcao import play_scene as scene_04
from manim_scenes.scene_05_bonding_antibonding import play_scene as scene_05
from manim_scenes.scene_06_two_energies import play_scene as scene_06
from manim_scenes.scene_07_h2_plus import play_scene as scene_07
from manim_scenes.scene_08_hydrogen import play_scene as scene_08
from manim_scenes.scene_09_helium import play_scene as scene_09
from manim_scenes.scene_10_sigma_p import play_scene as scene_10
from manim_scenes.scene_11_pi import play_scene as scene_11
from manim_scenes.scene_12_build_diagram import play_scene as scene_12
from manim_scenes.scene_13_orderings import play_scene as scene_13
from manim_scenes.scene_14_fill_nitrogen import play_scene as scene_14
from manim_scenes.scene_15_nitrogen_bond import play_scene as scene_15
from manim_scenes.scene_16_oxygen_reveal import play_scene as scene_16
from manim_scenes.scene_17_mystery_solved import play_scene as scene_17
from manim_scenes.scene_18_remove_electron import play_scene as scene_18
from manim_scenes.scene_19_add_electrons import play_scene as scene_19
from manim_scenes.scene_20_boron_fluorine import play_scene as scene_20
from manim_scenes.scene_21_challenge import play_scene as scene_21
from manim_scenes.scene_22_final import play_scene as scene_22
from manim_scenes.scene_23_subscribe import play_scene as scene_23

CHAPTERS = (
    scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08, scene_09, scene_10, scene_11, scene_12,
    scene_13, scene_14, scene_15, scene_16, scene_17, scene_18, scene_19, scene_20, scene_21, scene_22, scene_23,
)


class FullVideo(Scene):
    """Molecular Orbital Theory, Explained Visually — complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
