from __future__ import annotations

import numpy as np
from manim import *

from utils.equations import diminishing_returns_equation
from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, MUTED_TEXT, RED_GLOW, TEXT_COLOR, glow_text, set_scene_style


class DiminishingReturnsScene(MovingCameraScene):
    """Safe repetition decays while exploration creates variance and spikes."""

    def construct(self) -> None:
        set_scene_style(self)
        title = Text("Diminishing Returns vs Breakthrough Risk", font_size=40, color=TEXT_COLOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(glow_text(title, RED_GLOW, opacity=0.14)), run_time=1.0)

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 8, 1],
            x_length=10.4,
            y_length=4.2,
            tips=False,
            axis_config={"color": MUTED_TEXT, "stroke_width": 1.1},
        ).shift(DOWN * 0.45)
        safe = axes.plot(lambda x: 6.2 * (0.7**x), x_range=[0, 10], color=RED_GLOW, stroke_width=4)
        risk_points = [(0, 1.2), (1, 0.7), (2, 1.6), (3, 0.4), (4, 2.2), (5, 1.1), (6, 1.8), (7, 0.6), (8, 6.9), (9, 2.8), (10, 3.6)]
        risk = VMobject(color=GOLD_GLOW, stroke_width=4)
        risk.set_points_smoothly([axes.c2p(x, y) for x, y in risk_points])
        self.play(Create(axes), run_time=0.8)
        self.play(Create(safe), run_time=1.5)
        self.play(Create(risk), run_time=1.8)

        safe_label = Text("safe formula", font_size=22, color=RED_GLOW).next_to(safe, UP, buff=0.2).shift(LEFT * 1.8)
        risk_label = Text("creative exploration", font_size=22, color=GOLD_GLOW).move_to(axes.c2p(7.4, 7.35))
        self.play(FadeIn(safe_label), FadeIn(risk_label), run_time=0.8)

        decay_notes = VGroup(
            Text("-30%", font_size=22, color=RED_GLOW).move_to(axes.c2p(1.0, 4.4)),
            Text("-30%", font_size=22, color=RED_GLOW).move_to(axes.c2p(2.1, 3.0)),
            Text("-30%", font_size=22, color=RED_GLOW).move_to(axes.c2p(3.2, 2.0)),
        )
        spike = Dot(axes.c2p(8, 6.9), radius=0.11, color=GOLD_GLOW)
        self.play(FadeIn(decay_notes), Flash(spike, color=GOLD_GLOW), FadeIn(spike), run_time=1.0)

        equation = diminishing_returns_equation(40).to_edge(DOWN, buff=0.45)
        lines = VGroup(
            Text("Predictable is not the same as creative.", font_size=24, color=TEXT_COLOR),
            Text("Variance creates possibility.", font_size=24, color=GREEN_GLOW),
        ).arrange(DOWN, buff=0.13).to_edge(RIGHT, buff=0.8).shift(UP * 0.65)
        self.play(FadeIn(glow_text(equation, RED_GLOW, opacity=0.12)), FadeIn(lines), run_time=1.0)
        self.wait(25.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
