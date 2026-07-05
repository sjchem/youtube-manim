"""Combined Chapter 3 video."""

from __future__ import annotations

from manim import *

from manim_scenes.scene_01_data_first_look import play_scene as play_scene_01
from manim_scenes.scene_02_center import play_scene as play_scene_02
from manim_scenes.scene_03_outliers import play_scene as play_scene_03
from manim_scenes.scene_04_spread import play_scene as play_scene_04
from manim_scenes.scene_05_percentiles import play_scene as play_scene_05
from manim_scenes.scene_06_scaling import play_scene as play_scene_06
from manim_scenes.scene_07_covariance_correlation import play_scene as play_scene_07
from manim_scenes.scene_08_worked_mean_variance import play_scene as play_scene_08
from manim_scenes.scene_09_distribution_shape import play_scene as play_scene_09
from manim_scenes.scene_10_correlation_example import play_scene as play_scene_10
from manim_scenes.scene_11_ml_checklist import play_scene as play_scene_11
from manim_scenes.scene_12_subscribe import play_scene as play_scene_12


class FullVideo(Scene):
    """Render every scene in sequence as one Manim scene."""

    def construct(self) -> None:
        for play in (
            play_scene_01,
            play_scene_02,
            play_scene_03,
            play_scene_04,
            play_scene_05,
            play_scene_06,
            play_scene_07,
            play_scene_08,
            play_scene_09,
            play_scene_10,
            play_scene_11,
            play_scene_12,
        ):
            play(self)
            self.clear()
