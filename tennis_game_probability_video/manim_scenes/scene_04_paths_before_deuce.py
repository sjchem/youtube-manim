from __future__ import annotations

from manim_scenes.common import *
from utils.tennis_scoring import generate_paths


class PathsBeforeDeuceScene(TennisScene):
    """Count the paths that win before deuce."""

    def construct(self) -> None:
        title = self.title("Winning Before Deuce").to_edge(UP)
        terms = VGroup(
            MathTex(r"4-0:\quad p^4", font_size=38, color=BALL_YELLOW),
            MathTex(r"4-1:\quad {4\choose3}p^4(1-p)=4p^4(1-p)", font_size=38, color=SERVER_GREEN),
            MathTex(r"4-2:\quad {5\choose3}p^4(1-p)^2=10p^4(1-p)^2", font_size=38, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT).shift(UP * 0.2)

        counts = [(4, 0, BALL_YELLOW), (4, 1, SERVER_GREEN), (4, 2, BLUE)]
        path_groups = VGroup()
        for row, (s, r, color) in enumerate(counts):
            paths = generate_paths(s, r)
            dots = VGroup()
            for index, path in enumerate(paths):
                mini = VGroup(*[
                    Dot(radius=0.045, color=color if bit else RECEIVER_RED).shift(RIGHT * j * 0.17)
                    for j, bit in enumerate(path)
                ])
                mini.move_to(RIGHT * 3.1 + UP * (1.25 - row * 1.25) + RIGHT * (index % 5) * 0.75 + DOWN * (index // 5) * 0.32)
                dots.add(mini)
            path_groups.add(dots)

        note = Text("The last point is a win; the earlier points create the path count.", font_size=28, color=MUTED).to_edge(DOWN)
        self.play(Write(title))
        for term, group in zip(terms, path_groups):
            self.play(Write(term), LaggedStart(*[FadeIn(dot) for dot in group], lag_ratio=0.05))
            self.play(Circumscribe(term, color=term.get_color()))
        self.play(Write(note))
        self.wait(1.0)
