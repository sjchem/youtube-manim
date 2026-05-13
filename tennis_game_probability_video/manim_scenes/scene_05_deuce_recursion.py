from __future__ import annotations

from manim_scenes.common import *


class DeuceRecursionScene(TennisScene):
    """Show the recursive probability from deuce."""

    def construct(self) -> None:
        title = self.title("Deuce Is a Probability Loop").to_edge(UP)
        deuce = Circle(radius=0.9, color=TENNIS_GOLD).set_fill(TENNIS_GOLD, 0.12)
        deuce_label = Text("Deuce", font_size=36, color=TENNIS_GOLD).move_to(deuce)
        game = Text("Game", font_size=34, color=SERVER_GREEN).move_to(RIGHT * 4 + UP * 1.5)
        lose = Text("Lose Game", font_size=34, color=RECEIVER_RED).move_to(RIGHT * 4 + DOWN * 1.5)
        loop_label = Text("split two points", font_size=26, color=MUTED).move_to(LEFT * 3.5)

        ww = Arrow(deuce.get_right(), game.get_left(), color=SERVER_GREEN, stroke_width=5)
        ll = Arrow(deuce.get_right() + DOWN * 0.2, lose.get_left() + UP * 0.2, color=RECEIVER_RED, stroke_width=5)
        loop = CurvedArrow(deuce.get_left() + UP * 0.2, deuce.get_left() + DOWN * 0.2, angle=TAU * 0.75, color=BALL_YELLOW)
        labels = VGroup(
            MathTex(r"p^2", font_size=30, color=SERVER_GREEN).next_to(ww, UP),
            MathTex(r"(1-p)^2", font_size=30, color=RECEIVER_RED).next_to(ll, DOWN),
            MathTex(r"2p(1-p)", font_size=30, color=BALL_YELLOW).next_to(loop, LEFT),
            loop_label,
        )
        eq1 = MathTex(r"q=p^2+2p(1-p)q", font_size=42, color=LINE_WHITE).to_edge(DOWN).shift(UP * 0.7)
        eq2 = MathTex(r"q={p^2\over 1-2p(1-p)}={p^2\over p^2+(1-p)^2}", font_size=42, color=BALL_YELLOW).to_edge(DOWN)

        self.play(Write(title), FadeIn(deuce), Write(deuce_label))
        self.play(Create(ww), FadeIn(game), Create(ll), FadeIn(lose), Create(loop), FadeIn(labels))
        self.play(Write(eq1))
        self.play(TransformFromCopy(eq1, eq2), Circumscribe(eq2, color=BALL_YELLOW))
        self.wait(1.0)
