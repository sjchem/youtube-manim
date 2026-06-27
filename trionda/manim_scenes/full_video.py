from __future__ import annotations

from manim import MovingCameraScene

import config as cfg
from manim_scenes.scene_01_cutaway import construct_scene_01
from manim_scenes.scene_02_material_layers import construct_scene_02
from manim_scenes.scene_03_thermal_bonding import construct_scene_03
from manim_scenes.scene_04_panel_geometry import construct_scene_04
from manim_scenes.scene_05_boundary_layer import construct_scene_05
from manim_scenes.scene_06_drag_crisis import construct_scene_06
from manim_scenes.scene_07_sensor_inside import construct_scene_07
from manim_scenes.scene_08_ai_var import construct_scene_08
from manim_scenes.scene_09_subscribe import construct_scene_09


class FullVideo(MovingCameraScene):
    """Render all chapters as one continuous video."""

    def construct(self) -> None:
        cfg.apply_manim_config()
        construct_scene_01(self)
        construct_scene_02(self)
        construct_scene_03(self)
        construct_scene_04(self)
        construct_scene_05(self)
        construct_scene_06(self)
        construct_scene_07(self)
        construct_scene_08(self)
        construct_scene_09(self)
