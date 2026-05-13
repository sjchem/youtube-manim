from __future__ import annotations

from manim_scenes.common import *
from utils.math_utils import game_win_probability


class GraphScene(TennisScene):
    """Plot G(p) against p."""

    def construct(self) -> None:
        title = self.title("The Nonlinear Amplifier").to_edge(UP)
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1, 0.1],
            x_length=9.5,
            y_length=5.4,
            axis_config={"color": LINE_WHITE, "include_numbers": True, "font_size": 22},
        ).shift(DOWN * 0.2)
        labels = axes.get_axis_labels(Text("p", font_size=26), Text("G(p)", font_size=26))
        curve = axes.plot(lambda x: game_win_probability(x), x_range=[0, 1], color=BALL_YELLOW, stroke_width=5)
        ref = axes.plot(lambda x: x, x_range=[0, 1], color=MUTED, stroke_width=3)
        ref.set_stroke(opacity=0.65)

        points = VGroup()
        for p in [0.5, 0.6, 0.70464, 0.8]:
            g = game_win_probability(p)
            dot = Dot(axes.c2p(p, g), color=SERVER_GREEN if abs(p - 0.70464) < 1e-9 else LINE_WHITE)
            label = Text(f"{p:.3g}, {g:.3f}", font_size=20, color=dot.get_color()).next_to(dot, UP, buff=0.08)
            points.add(VGroup(dot, label))
        note = Text("Above the dashed line, point advantages are amplified.", font_size=28, color=MUTED).to_edge(DOWN)

        self.play(Write(title), Create(axes), Write(labels))
        self.play(Create(ref), Create(curve), run_time=1.8)
        self.play(LaggedStart(*[FadeIn(p) for p in points], lag_ratio=0.18))
        self.play(Write(note))
        self.wait(1.0)
