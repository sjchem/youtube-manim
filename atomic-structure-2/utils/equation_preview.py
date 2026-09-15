"""Continuous review of matter waves, uncertainty and allowed atomic states.

    ATOM_REVIEW_SPEED=3 python -m manim -ql --fps 12 \
        --media_dir output/equation_motion utils/equation_preview.py EquationPreview

The review uses the real chapters 04–08, including their visual joins. With the
environment setting above it runs at three times the production pace and has
no audio. Omit that setting to retain the actual narration windows.
"""

from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import SCENE_MAP
from manim_scenes.common import QuantumScene


class EquationPreview(QuantumScene):
    def setup(self) -> None:
        super().setup()
        # Retain this multi-chapter review's partials for quick visual fixes.
        from manim import config
        config.max_files_cached = max(config.max_files_cached, 1000)

    def construct(self) -> None:
        for key in ("04", "05", "06", "07", "08"):
            module, _, _ = SCENE_MAP[key]
            import_module(module).play_scene(self)


class UncertaintyReview(QuantumScene):
    """Refresh chapter 07 from chapter 06's exact outgoing wave."""

    def construct(self) -> None:
        from manim_scenes.common import wave
        from manim_scenes.scene_07_uncertainty import play_scene

        self.prepare("07")
        self.remove(self.anchor)
        self.anchor = wave(width=12, k=5, amplitude=0.6)
        self.add(self.anchor)
        play_scene(self)
