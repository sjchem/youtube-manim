"""Render the complete film as one deterministic sequence.

Every scene is a ``play_scene(scene)`` function that themes the scene, lands
on its configured duration, and fades out everything except the faint shared
bubble layer. All 3D is drawn by projected stages inside an ordinary Scene,
so there is no camera state to reset between scenes. Every gas, simulation
and sampled orientation is seeded, so two renders are frame-for-frame equal.
"""

from __future__ import annotations

import importlib

from manim import Scene

import config as cfg
from main import SCENE_MAP

CHAPTERS = tuple(importlib.import_module(module).play_scene for module, _, _ in SCENE_MAP.values())


class FullVideo(Scene):
    """The Molecular Dance — complete."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        for play in CHAPTERS:
            play(self)
