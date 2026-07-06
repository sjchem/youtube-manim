"""Combined render scene for the full 6-7 video."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import clear_scene
from manim_scenes.scene_01_hook import play_scene_01
from manim_scenes.scene_02_perfect_six import play_scene_02
from manim_scenes.scene_03_hexagon_order import play_scene_03
from manim_scenes.scene_04_prime_outsider import play_scene_04
from manim_scenes.scene_05_heptagon_impossibility import play_scene_05
from manim_scenes.scene_06_decimal_cycle import play_scene_06
from manim_scenes.scene_07_cyclic_number import play_scene_07
from manim_scenes.scene_08_synthesis import play_scene_08
from manim_scenes.scene_09_subscribe import play_scene_09


class FullVideo(MovingCameraScene):
    """Render every section as one continuous Manim scene."""

    def construct(self) -> None:
        cfg.apply_oceanic_next_theme(self)
        players = [
            play_scene_01,
            play_scene_02,
            play_scene_03,
            play_scene_04,
            play_scene_05,
            play_scene_06,
            play_scene_07,
            play_scene_08,
            play_scene_09,
        ]
        for index, player in enumerate(players):
            player(self)
            if index < len(players) - 1:
                clear_scene(self)
