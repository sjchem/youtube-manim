"""Combined render scene for the full 4-5 minute video."""

from __future__ import annotations

from manim import *

from config import apply_oceanic_next_theme
from manim_scenes.scene_01_hook import play_scene_01
from manim_scenes.scene_02_power_ladder import play_scene_02
from manim_scenes.scene_03_exponent_law import play_scene_03
from manim_scenes.scene_04_empty_product import play_scene_04
from manim_scenes.scene_05_graph_view import play_scene_05
from manim_scenes.scene_06_final_summary import play_scene_06


class FullVideo(MovingCameraScene):
    """Render every section as one continuous Manim scene."""

    def construct(self) -> None:
        apply_oceanic_next_theme(self)
        for index, scene_player in enumerate(
            [
                play_scene_01,
                play_scene_02,
                play_scene_03,
                play_scene_04,
                play_scene_05,
                play_scene_06,
            ]
        ):
            scene_player(self)
            if index < 5:
                self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
                self.wait(0.2)
