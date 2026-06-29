"""Full video — all scenes played sequentially in one Manim Scene.

Render at YouTube quality:
    python main.py render
Or directly:
    manim -qqh manim_scenes/full_video.py FullVideo --fps 30
"""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene
from themes.oceanic_next import apply_oceanic_next_theme

# Import each scene's play_scene function
from manim_scenes.scene_01_opening         import play_scene as s01
from manim_scenes.scene_02_uncertain_world import play_scene as s02
from manim_scenes.scene_03_signal_noise    import play_scene as s03
from manim_scenes.scene_04_population_sample import play_scene as s04
from manim_scenes.scene_05_patterns_prediction import play_scene as s05
from manim_scenes.scene_06_overfitting     import play_scene as s06
from manim_scenes.scene_07_bias_variance   import play_scene as s07
from manim_scenes.scene_08_statistics_layer import play_scene as s08
from manim_scenes.scene_09_subscribe       import play_scene as s09


class FullVideo(Scene):
    """Renders the complete Chapter 1 video in a single pass."""

    def construct(self) -> None:
        try:
            apply_oceanic_next_theme(self)
        except Exception:
            self.camera.background_color = cfg.BG

        for play in (s01, s02, s03, s04, s05, s06, s07, s08, s09):
            play(self)
