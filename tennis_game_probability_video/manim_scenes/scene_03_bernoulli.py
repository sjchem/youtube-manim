from __future__ import annotations

from manim_scenes.common import *


class BernoulliTrialScene(TennisScene):
    """Introduce Bernoulli trials and a running sum."""

    def construct(self) -> None:
        title = self.title("Every Point Becomes a Bernoulli Trial").to_edge(UP)
        equation = formula_box(r"X_i\sim\operatorname{Bernoulli}(p),\quad S_n=X_1+\cdots+X_n").next_to(title, DOWN)
        meaning = Text("1 = server wins point     0 = server loses point", font_size=28, color=MUTED).next_to(equation, DOWN)

        outcomes = ["W", "L", "W", "W", "W"]
        sums = [1, 1, 2, 3, 4]
        row = VGroup()
        for outcome, total in zip(outcomes, sums):
            dot = tennis_ball(0.14)
            label = Text(outcome, font_size=30, color=BACKGROUND, weight=BOLD).move_to(dot)
            s_label = Text(str(total), font_size=30, color=LINE_WHITE).next_to(dot, DOWN)
            row.add(VGroup(dot, label, s_label))
        row.arrange(RIGHT, buff=0.65).shift(DOWN * 0.5)

        win = Text("Four server points, with the scoring margin: game.", font_size=34, color=SERVER_GREEN).to_edge(DOWN)
        self.play(Write(title), Write(equation), FadeIn(meaning))
        for item in row:
            self.play(FadeIn(item[0], scale=0.6), Write(item[1]), Write(item[2]), run_time=0.35)
        self.play(Write(win))
        self.wait(1.0)
