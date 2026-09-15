"""A short motion review of the film's visual spine, without the narration holds.

This is the fastest way to see whether the transformations still read:

    python -m manim -ql --fps 15 utils/visual_preview.py VisualPreview

It is a sample, not the film. Nothing here is synchronised to narration, and
the storyboard audit remains the check that the real chapters still fit their
windows.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from manim_scenes.common import *  # noqa: F403
from manim_scenes.common import packet_plot

BUILD_UP = ((1, "H"), (2, "He"), (3, "Li"), (6, "C"), (10, "Ne"), (11, "Na"))


class VisualPreview(QuantumScene):  # noqa: F405
    def construct(self) -> None:
        self.prepare("01")

        # ORBIT -> WAVE
        self.morph(orbit(2.6), seconds=1.0)  # noqa: F405
        self.cue("WHERE IS THE ELECTRON?", hold=1.2)
        self.playq(Rotate(self.anchor[2], TAU, about_point=ORIGIN), seconds=2, rate_func=linear)  # noqa: F405
        self.morph(wave(k=5), seconds=2)  # noqa: F405
        law = self.formula(r"\lambda=\frac{h}{p}", size=70)
        self.morph(wave(k=9), seconds=1.5)  # noqa: F405
        self.morph(wave(k=3), seconds=1.5)  # noqa: F405
        self.drop(law)

        # The uncertainty trade
        sigma = ValueTracker(1.8)  # noqa: F405
        panels = always_redraw(lambda: packet_plot(sigma.get_value()))  # noqa: F405
        self.dissolve(panels)
        law = self.formula(r"\Delta x\,\Delta p\geq\frac{\hbar}{2}", size=62)
        self.playq(sigma.animate.set_value(0.38), seconds=3)
        self.playq(sigma.animate.set_value(1.5), seconds=3)
        panels.clear_updaters()
        self.drop(law)

        # WAVE -> PROBABILITY
        self.dissolve(density_slice(2, 1, 0, phase=True), seconds=1.5)  # noqa: F405
        law = self.formula(r"\psi\ \longrightarrow\ |\psi|^2", size=66)
        self.dissolve(density_slice(2, 1, 0), seconds=2)  # noqa: F405
        self.hold(1)
        self.drop(law)
        self.dissolve(VGroup(nucleus()), seconds=1)  # noqa: F405
        detections = cloud(count=500, scale=1.05)  # noqa: F405
        self.playq(LaggedStart(*(FadeIn(dot) for dot in detections), lag_ratio=0.012), seconds=4)  # noqa: F405
        self.adopt(*detections)

        # PROBABILITY -> ORBITAL
        self.dissolve(self.orbital(1, 0, 0, size=2.5), seconds=2)
        self.view3d(seconds=1.5)
        self.turn(seconds=2)
        self.morph(self.orbital(2, 1, 0, size=2.9), seconds=2)
        self.turn(seconds=3)
        state = self.formula(r"n=2,\quad \ell=1,\quad m_\ell=0", size=52)
        self.hold(2)
        self.drop(state)
        self.morph(self.orbital(3, 2, -2, size=2.9), seconds=2)
        self.turn(seconds=3)

        # ORBITAL -> ATOM -> CHEMISTRY
        self.dissolve(VGroup(), seconds=0.8)  # noqa: F405
        self.flat(seconds=1)
        self.morph(boxes(1), seconds=1.2)  # noqa: F405
        for z, symbol in BUILD_UP:
            name = self.pin(text(symbol, 40, cfg.GOLD).move_to([-4.8, 1, 0]))  # noqa: F405
            self.playq(FadeIn(name), seconds=0.35)  # noqa: F405
            self.morph(boxes(z), seconds=0.8)  # noqa: F405
            self.hold(0.5)
            self.drop(name, seconds=0.3)
        self.morph(periodic_table(), seconds=2)  # noqa: F405
        self.spine(len(cfg.SPINE) - 1, hold=2.0)  # noqa: F405
        self.hold(1.5)
        self.playq(FadeOut(self.anchor), seconds=1)  # noqa: F405
