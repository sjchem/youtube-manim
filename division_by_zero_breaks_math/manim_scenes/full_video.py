from manim import MovingCameraScene

from config import apply_oceanic_next_theme
from manim_scenes.scene_01 import construct_scene_01
from manim_scenes.scene_02 import construct_scene_02
from manim_scenes.scene_03 import construct_scene_03
from manim_scenes.scene_04 import construct_scene_04
from manim_scenes.scene_05 import construct_scene_05
from manim_scenes.scene_06 import construct_scene_06
from manim_scenes.scene_07 import construct_scene_07
from manim_scenes.scene_08 import construct_scene_08


class FullVideo(MovingCameraScene):
    """Render all eight chapters as one continuous Manim video."""

    def construct(self) -> None:
        apply_oceanic_next_theme()
        construct_scene_01(self)
        construct_scene_02(self)
        construct_scene_03(self)
        construct_scene_04(self)
        construct_scene_05(self)
        construct_scene_06(self)
        construct_scene_07(self)
        construct_scene_08(self)
