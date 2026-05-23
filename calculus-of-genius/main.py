from __future__ import annotations

from manim import *

from scenes.scene_00_title import TitleScene
from scenes.scene_01_hook import HookScene
from scenes.scene_02_probability import ProbabilityScene
from scenes.scene_03_zipf import ZipfScene
from scenes.scene_04_combinatorial import CombinatorialScene
from scenes.scene_05_compound_time import CompoundTimeScene
from scenes.scene_06_edge_of_chaos import EdgeOfChaosScene
from scenes.scene_07_diminishing_returns import DiminishingReturnsScene
from scenes.scene_08_final_formula import FinalFormulaScene
from utils.style import set_scene_style


class CombinedScene(MovingCameraScene):
    """Full 5-6 minute program assembled from all modular scenes."""

    def construct(self) -> None:
        set_scene_style(self)
        for scene_cls in [
            TitleScene,
            HookScene,
            ProbabilityScene,
            ZipfScene,
            CombinatorialScene,
            CompoundTimeScene,
            EdgeOfChaosScene,
            DiminishingReturnsScene,
            FinalFormulaScene,
        ]:
            scene_cls.construct(self)


__all__ = [
    "TitleScene",
    "HookScene",
    "ProbabilityScene",
    "ZipfScene",
    "CombinatorialScene",
    "CompoundTimeScene",
    "EdgeOfChaosScene",
    "DiminishingReturnsScene",
    "FinalFormulaScene",
    "CombinedScene",
]

