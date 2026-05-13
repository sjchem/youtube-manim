from __future__ import annotations

from manim_scenes.common import *
from utils.math_utils import point_win_probability


class ServicePointProbabilityScene(TennisScene):
    """Calculate the point win probability from serve components."""

    def construct(self) -> None:
        title = self.title("One Service Point").to_edge(UP)
        formula = formula_box(r"P(W)=P(S_1)P(W|S_1)+(1-P(S_1))P(S_2)P(W|S_2)").next_to(title, DOWN)
        if formula.width > config.frame_width - 1.0:
            formula.scale((config.frame_width - 1.0) / formula.width)

        root = Dot(LEFT * 5.0 + UP * 0.2, color=BALL_YELLOW)
        s1 = Text("First serve in", font_size=24, color=LINE_WHITE).move_to(LEFT * 2.65 + UP * 1.15)
        miss = Text("First serve missed", font_size=24, color=LINE_WHITE).move_to(LEFT * 2.65 + DOWN * 0.95)
        win1 = Text("Win point", font_size=24, color=SERVER_GREEN).move_to(RIGHT * 1.35 + UP * 1.15)
        s2 = Text("Second serve in", font_size=24, color=LINE_WHITE).move_to(RIGHT * 1.05 + DOWN * 0.95)
        win2 = Text("Win point", font_size=24, color=SERVER_GREEN).move_to(RIGHT * 4.45 + DOWN * 0.95)
        branches = VGroup(
            branch(root, s1, "0.712", BALL_YELLOW),
            branch(root, miss, "0.288", MUTED),
            branch(s1, win1, "0.768", SERVER_GREEN),
            branch(miss, s2, "1.000", BALL_YELLOW),
            branch(s2, win2, "0.548", SERVER_GREEN),
        )

        term1 = MathTex(r"0.712\times0.768=0.5468", font_size=34, color=LINE_WHITE)
        term2 = MathTex(r"0.288\times1.0\times0.548=0.1578", font_size=34, color=LINE_WHITE)
        total = point_win_probability(0.712, 0.768, 1.0, 0.548)
        total_tex = MathTex(fr"P(W)=0.7046\approx {100 * total:.1f}\%", font_size=42, color=BALL_YELLOW)
        calc = VGroup(term1, term2, total_tex).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN).shift(UP * 0.15)

        self.play(Write(title), Write(formula))
        self.play(FadeIn(root), FadeIn(VGroup(s1, miss, win1, s2, win2)))
        self.play(LaggedStart(*[Create(item) for item in branches], lag_ratio=0.18))
        self.play(Write(term1), Write(term2))
        self.play(Write(total_tex), Circumscribe(total_tex, color=BALL_YELLOW))
        self.wait(1.0)
