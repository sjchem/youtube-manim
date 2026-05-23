from __future__ import annotations

import numpy as np
from manim import *

from utils.equations import probability_success_equation
from utils.helpers import probability_of_success, value_label
from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, MUTED_TEXT, TEXT_COLOR, glow_text, set_scene_style


class ProbabilityScene(MovingCameraScene):
    """Law of large numbers: attempts create outliers."""

    def construct(self) -> None:
        set_scene_style(self)
        rng = np.random.default_rng(33)

        title = Text("Attempts Create Outliers", font_size=42, color=TEXT_COLOR, weight=BOLD).to_edge(UP)
        subtitle = Text("Most attempts are ordinary. Volume changes the odds.", font_size=22, color=MUTED_TEXT)
        subtitle.next_to(title, DOWN, buff=0.16)
        self.play(FadeIn(glow_text(title, BLUE_GLOW, opacity=0.14)), FadeIn(subtitle), run_time=1.0)

        axes = Axes(
            x_range=[0, 1000, 200],
            y_range=[0, 1, 0.2],
            x_length=5.7,
            y_length=3.0,
            tips=False,
            axis_config={"color": MUTED_TEXT, "stroke_width": 1.2},
        ).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.3)
        p = 0.006
        curve = axes.plot(lambda x: probability_of_success(p, x), x_range=[0, 1000], color=GREEN_GLOW, stroke_width=4)
        curve_label = MathTex(r"1-(1-p)^n", font_size=30, color=GREEN_GLOW).next_to(axes, UP, buff=0.2)
        self.play(Create(axes), FadeIn(curve_label), Create(curve), run_time=1.6)

        cloud_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=5.4,
            y_length=3.2,
            tips=False,
            axis_config={"color": MUTED_TEXT, "stroke_width": 1},
        ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.35)
        threshold = DashedLine(cloud_axes.c2p(0, 4.55), cloud_axes.c2p(10, 4.55), color=GOLD_GLOW, stroke_width=2)
        threshold_label = Text("breakthrough threshold", font_size=17, color=GOLD_GLOW).next_to(threshold, UP, buff=0.08)
        self.play(Create(cloud_axes), Create(threshold), FadeIn(threshold_label), run_time=1.0)

        samples = rng.lognormal(mean=0.5, sigma=0.78, size=120)
        samples = np.clip(samples, 0.15, 5.5)
        dots = VGroup()
        for i, y in enumerate(samples):
            x = rng.uniform(0.25, 9.75)
            color = GOLD_GLOW if y > 4.55 else BLUE_GLOW
            radius = 0.052 if y > 4.55 else 0.032
            opacity = 0.95 if y > 4.55 else 0.42
            dots.add(Dot(cloud_axes.c2p(x, y), radius=radius, color=color, fill_opacity=opacity))

        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.015), run_time=3.0)

        n_tracker = ValueTracker(10)
        moving_dot = always_redraw(lambda: Dot(axes.c2p(n_tracker.get_value(), probability_of_success(p, n_tracker.get_value())), color=GOLD_GLOW, radius=0.08))
        n_label = value_label("n = ", n_tracker, decimals=0).next_to(axes, DOWN, buff=0.28)
        prob_number = DecimalNumber(probability_of_success(p, 10), num_decimal_places=2, color=GREEN_GLOW, font_size=30)
        prob_number.add_updater(lambda m: m.set_value(probability_of_success(p, n_tracker.get_value())))
        prob_label = VGroup(Text("P = ", font_size=26, color=MUTED_TEXT), prob_number).arrange(RIGHT, buff=0.07).next_to(n_label, DOWN, buff=0.12)
        self.play(FadeIn(moving_dot), FadeIn(n_label), FadeIn(prob_label), run_time=0.8)
        self.play(n_tracker.animate.set_value(100), run_time=1.4)
        self.play(n_tracker.animate.set_value(1000), run_time=2.0)

        equation = probability_success_equation(34).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(glow_text(equation, BLUE_GLOW, opacity=0.13)), run_time=1.0)
        takeaway = Text("Volume does not guarantee genius. It changes the odds.", font_size=25, color=TEXT_COLOR)
        takeaway.next_to(equation, UP, buff=0.22)
        self.play(FadeIn(takeaway), run_time=0.8)
        self.wait(31.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
