"""Continuous full-video scene."""

from __future__ import annotations

from manim import Scene

from manim_scenes.scene_01_hook import play_scene as scene_01
from manim_scenes.scene_02_off_center_kick import play_scene as scene_02
from manim_scenes.scene_03_airflow_spin import play_scene as scene_03
from manim_scenes.scene_04_magnus_force import play_scene as scene_04
from manim_scenes.scene_05_curve_simulation import play_scene as scene_05
from manim_scenes.scene_06_surface_matters import play_scene as scene_06
from manim_scenes.scene_07_trionda_design import play_scene as scene_07
from manim_scenes.scene_08_final_synthesis import play_scene as scene_08
from manim_scenes.scene_09_subscribe import play_scene as scene_09


class FullVideo(Scene):
    """Continuous version of all nine scenes."""

    def construct(self) -> None:
        for play in (scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08, scene_09):
            play(self)
