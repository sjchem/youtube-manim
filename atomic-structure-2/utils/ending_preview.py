"""Render the revised closing sequence with its actual narration windows.

    python -m manim -ql --fps 12 utils/ending_preview.py EndingPreview

The chapters share one anchor, as in FullVideo. The first twenty minutes are
omitted, making it practical to inspect the filling-to-chemistry transitions,
the recap and the separate subscribe card together. No voiceover is attached.
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


class EndingPreview(QuantumScene):
    def construct(self) -> None:
        for key, (module, _, _) in SCENE_MAP.items():
            if int(key) >= 14:
                import_module(module).play_scene(self)
