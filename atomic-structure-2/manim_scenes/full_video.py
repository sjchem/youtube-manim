"""The complete nineteen-chapter film; the CLI registry is the source of order.

Every chapter runs on one scene and inherits the outgoing anchor, so the joins
between chapters are transformations rather than cuts to black.
"""

from __future__ import annotations

from importlib import import_module

from main import SCENE_MAP
from manim_scenes.common import QuantumScene

CHAPTERS = tuple(import_module(module).play_scene for module, _, _ in SCENE_MAP.values())


class FullVideo(QuantumScene):
    def construct(self) -> None:
        for play in CHAPTERS:
            play(self)
            if getattr(self.renderer, "check_lifetimes", False):
                print(f"{self.key}: continuous chapter complete at {self.time:.2f}s", flush=True)
