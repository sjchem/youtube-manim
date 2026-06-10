from manim import *

from manim_scenes.scene_01_hook import play_scene as scene_01
from manim_scenes.scene_02_motivation_decay import play_scene as scene_02
from manim_scenes.scene_03_inertia import play_scene as scene_03
from manim_scenes.scene_04_friction import play_scene as scene_04
from manim_scenes.scene_05_energy_barrier import play_scene as scene_05
from manim_scenes.scene_06_momentum import play_scene as scene_06
from manim_scenes.scene_07_feedback_loop import play_scene as scene_07
from manim_scenes.scene_08_final_synthesis import play_scene as scene_08


class FullVideo(Scene):
    """Complete continuous animation."""

    def construct(self):
        scene_01(self)
        scene_02(self)
        scene_03(self)
        scene_04(self)
        scene_05(self)
        scene_06(self)
        scene_07(self)
        scene_08(self)

