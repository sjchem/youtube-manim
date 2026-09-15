"""Focused motion review of the worked radial-probability example."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim_scenes.common import QuantumScene
from manim_scenes.radial_probability_visual import radial_probability_demo


class RadialProbabilityReview(QuantumScene):
    def construct(self) -> None:
        self.prepare("11")
        radial_probability_demo(self)
