from __future__ import annotations

from manim_scenes.common import *
from config import ZVEREV_ACTUAL_GAME_WIN
from utils.math_utils import game_win_probability, point_win_probability


class ZverevCaseStudyScene(TennisScene):
    """Compare the formula with Zverev's 2024 serving example."""

    def construct(self) -> None:
        title = self.title("Alexander Zverev, 2024 Serving Example").to_edge(UP)
        p = point_win_probability(0.712, 0.768, 1.0, 0.548)
        g = game_win_probability(p)
        stats = VGroup(
            Text("First serve in: 71.2%", font_size=28, color=LINE_WHITE),
            Text("First serve points won: 76.8%", font_size=28, color=LINE_WHITE),
            Text("Second serve points won: 54.8%", font_size=28, color=LINE_WHITE),
            Text(f"Estimated point win probability: {100 * p:.1f}%", font_size=30, color=BALL_YELLOW),
            Text(f"Theoretical service-game win probability: {100 * g:.1f}%", font_size=30, color=SERVER_GREEN),
            Text("Actual service-game win percentage: about 90.2%", font_size=30, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT).shift(RIGHT * 0.6)

        base_y = -2.15
        theory_bar = Rectangle(width=4.5 * g, height=0.45, color=SERVER_GREEN).set_fill(SERVER_GREEN, 0.85)
        actual_bar = Rectangle(width=4.5 * ZVEREV_ACTUAL_GAME_WIN, height=0.45, color=BLUE).set_fill(BLUE, 0.85)
        theory_bar.move_to(RIGHT * 2.7 + UP * (base_y + 0.45))
        actual_bar.move_to(RIGHT * 2.7 + UP * (base_y - 0.35))
        bar_labels = VGroup(
            Text("Theory 90.6%", font_size=24, color=SERVER_GREEN).next_to(theory_bar, LEFT),
            Text("Actual 90.2%", font_size=24, color=BLUE).next_to(actual_bar, LEFT),
        )

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.25) for line in stats], lag_ratio=0.08))
        self.play(FadeIn(bar_labels), GrowFromEdge(theory_bar, LEFT), GrowFromEdge(actual_bar, LEFT))
        self.play(Circumscribe(VGroup(theory_bar, actual_bar), color=BALL_YELLOW))
        self.wait(1.0)
