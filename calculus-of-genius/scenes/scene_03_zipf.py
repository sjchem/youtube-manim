from __future__ import annotations

import numpy as np
from manim import *

from utils.equations import zipf_law_equation
from utils.style import BLUE_GLOW, GOLD_GLOW, MUTED_TEXT, TEXT_COLOR, glow_text, set_scene_style


class ZipfScene(MovingCameraScene):
    """Power-law impact: most ideas vanish, a few dominate."""

    def construct(self) -> None:
        set_scene_style(self)
        title = Text("Creativity Is Not Evenly Distributed", font_size=42, color=TEXT_COLOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(glow_text(title, GOLD_GLOW, opacity=0.15)), run_time=1.0)

        ranks = np.arange(1, 31)
        s = 1.08
        values = 1 / (ranks**s)
        values = values / values.max()
        bars = VGroup()
        width = 0.23
        for i, value in enumerate(values):
            color = GOLD_GLOW if i < 2 else BLUE_GLOW
            opacity = 0.95 if i < 2 else max(0.16, 0.72 - i * 0.018)
            bar = Rectangle(width=width, height=3.7 * value, fill_color=color, fill_opacity=opacity, stroke_width=0)
            bar.move_to(LEFT * 4.7 + RIGHT * i * (width + 0.08) + DOWN * 1.25 + UP * bar.height / 2)
            bars.add(bar)

        shuffled = bars.copy()
        for bar in shuffled:
            bar.shift(UP * np.random.default_rng(8).uniform(-1.0, 1.0))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars], lag_ratio=0.025), run_time=1.7)

        long_tail = BraceBetweenPoints(bars[7].get_bottom(), bars[-1].get_bottom(), DOWN, color=MUTED_TEXT)
        long_tail_label = Text("long tail of ordinary ideas", font_size=20, color=MUTED_TEXT).next_to(long_tail, DOWN, buff=0.12)
        signal = Text("signal", font_size=23, color=GOLD_GLOW).next_to(bars[0], UP, buff=0.2)
        noise = Text("noise", font_size=22, color=MUTED_TEXT).next_to(bars[18], UP, buff=0.2)
        self.play(FadeIn(signal), FadeIn(noise), GrowFromCenter(long_tail), FadeIn(long_tail_label), run_time=1.1)

        equation = zipf_law_equation(46).to_edge(RIGHT, buff=0.8).shift(UP * 0.4)
        notes = VGroup(
            Text("A few outcomes", font_size=25, color=GOLD_GLOW),
            Text("carry most of the impact.", font_size=25, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(equation, DOWN, buff=0.55)
        self.play(FadeIn(glow_text(equation, BLUE_GLOW, opacity=0.13), shift=LEFT * 0.15), run_time=1.0)
        self.play(FadeIn(notes, shift=UP * 0.15), run_time=0.8)
        self.wait(29.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
