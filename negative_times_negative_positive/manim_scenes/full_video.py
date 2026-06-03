from manim import *

from manim_scenes.scene_01 import play_scene as scene_01
from manim_scenes.scene_02 import play_scene as scene_02
from manim_scenes.scene_03 import play_scene as scene_03
from manim_scenes.scene_04 import play_scene as scene_04
from manim_scenes.scene_05 import play_scene as scene_05
from manim_scenes.scene_06 import play_scene as scene_06
from manim_scenes.scene_07 import play_scene as scene_07
from manim_scenes.scene_08 import play_scene as scene_08


class FullVideo(Scene):
    """Continuous version of all eight scenes."""

    def construct(self) -> None:
        for play in (scene_01, scene_02, scene_03, scene_04, scene_05, scene_06, scene_07, scene_08):
            play(self)
