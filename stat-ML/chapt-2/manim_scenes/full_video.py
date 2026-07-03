from manim import *

from manim_scenes.scene_01_world_dataset import play_scene as scene_01
from manim_scenes.scene_02_population import play_scene as scene_02
from manim_scenes.scene_03_sample import play_scene as scene_03
from manim_scenes.scene_04_data_process import play_scene as scene_04
from manim_scenes.scene_05_representative_bias import play_scene as scene_05
from manim_scenes.scene_06_self_driving_shift import play_scene as scene_06
from manim_scenes.scene_07_train_validation_test import play_scene as scene_07
from manim_scenes.scene_08_iid import play_scene as scene_08
from manim_scenes.scene_09_distribution_shift import play_scene as scene_09
from manim_scenes.scene_10_final_question import play_scene as scene_10
from manim_scenes.scene_11_subscribe import play_scene as scene_11


class FullVideo(Scene):
    """Continuous version of all eleven Chapter 2 scenes."""

    def construct(self) -> None:
        for play in (scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08, scene_09, scene_10, scene_11):
            play(self)
