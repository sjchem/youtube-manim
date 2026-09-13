"""The complete fifteen-scene film; the CLI registry is the source of order."""
from importlib import import_module
from manim import ThreeDScene
from main import SCENE_MAP
import config as cfg

CHAPTERS = tuple(import_module(module).play_scene for module, _, _ in SCENE_MAP.values())

class FullVideo(ThreeDScene):
    def construct(self):
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
