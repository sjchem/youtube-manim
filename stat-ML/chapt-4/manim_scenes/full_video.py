"""Combined Chapter 4 video."""

from __future__ import annotations

from manim import *

from manim_scenes.scene_01_uncertainty import play_scene as play_scene_01
from manim_scenes.scene_02_probability_scale import play_scene as play_scene_02
from manim_scenes.scene_03_random_variables import play_scene as play_scene_03
from manim_scenes.scene_04_conditional_probability import play_scene as play_scene_04
from manim_scenes.scene_05_independence import play_scene as play_scene_05
from manim_scenes.scene_06_joint_marginal import play_scene as play_scene_06
from manim_scenes.scene_07_bayes_theorem import play_scene as play_scene_07
from manim_scenes.scene_08_ml_connections import play_scene as play_scene_08
from manim_scenes.scene_09_synthesis import play_scene as play_scene_09
from manim_scenes.scene_10_subscribe import play_scene as play_scene_10


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
        ):
            play(self)
            self.clear()
