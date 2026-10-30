"""Render the complete film as one deterministic sequence.

Every scene is a ``play_scene(scene)`` function that themes the scene, lands
on its configured duration, and fades out everything except the faint shared
bubble layer. All 3D is drawn by projected stages inside an ordinary Scene,
so there is no camera state to reset between scenes. The only randomness —
particle homes and the mole-fraction picks — comes from ``config.SEED``.
"""

from __future__ import annotations

import importlib

from manim import Scene

import config as cfg
from main import SCENE_MAP

CHAPTERS = tuple(importlib.import_module(module).play_scene for module, _, _ in SCENE_MAP.values())


class FullVideo(Scene):
    """Concentration, Explained Visually — complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
