from __future__ import annotations

from manim_scenes.common import *


class HookScene(TennisScene):
    """Open with the point-to-game probability jump."""

    def construct(self) -> None:
        court = make_court().scale(0.95)
        ball = tennis_ball(0.18).move_to(LEFT * 4 + UP * 1.4)
        title = self.title("Winning a point is not the same as winning a game.").to_edge(UP)
        point = percent_label("Point win chance", 0.704).shift(LEFT * 2.8 + DOWN * 2.2)
        game = percent_label("Game win chance", 0.906).shift(RIGHT * 2.8 + DOWN * 2.2)
        arrow = CurvedArrow(point.get_right(), game.get_left(), angle=-TAU / 6, color=BALL_YELLOW)
        question = Text("Where does the extra probability come from?", font_size=34, color=LINE_WHITE).to_edge(DOWN)

        self.play(FadeIn(court), Write(title))
        self.play(FadeIn(ball), ball.animate.move_to(RIGHT * 2.8 + DOWN * 0.7), run_time=1.2)
        self.play(FadeIn(point), Create(arrow), TransformFromCopy(point, game))
        self.play(Write(question))
        self.wait(1.0)
