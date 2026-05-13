from __future__ import annotations

from manim_scenes.common import *
from utils.math_utils import game_win_probability, point_win_probability


class FullFormulaScene(TennisScene):
    """Assemble the complete service-game probability."""

    def construct(self) -> None:
        title = self.title("The Whole Game Probability").to_edge(UP)
        lines = VGroup(
            MathTex(r"G(p)=p^4", font_size=38, color=BALL_YELLOW),
            MathTex(r"\quad +4p^4(1-p)", font_size=38, color=SERVER_GREEN),
            MathTex(r"\quad +10p^4(1-p)^2", font_size=38, color=BLUE),
            MathTex(r"\quad +20p^3(1-p)^3\cdot {p^2\over p^2+(1-p)^2}", font_size=38, color=TENNIS_GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).shift(UP * 0.15)
        p = point_win_probability(0.712, 0.768, 1.0, 0.548)
        value = game_win_probability(p)
        substitution = MathTex(fr"G(0.7046)\approx {value:.3f}=90.6\%", font_size=48, color=BALL_YELLOW).to_edge(DOWN).shift(UP * 0.6)
        sentence = Text("A 70.4% point edge compounds into a 90.6% game edge.", font_size=32, color=LINE_WHITE).to_edge(DOWN)

        self.play(Write(title))
        for line in lines:
            self.play(Write(line), run_time=0.65)
        self.play(Write(substitution), Circumscribe(substitution, color=BALL_YELLOW))
        self.play(Write(sentence))
        self.wait(1.0)
