from __future__ import annotations

from manim_scenes.common import *


class OutroScene(TennisScene):
    """Closing summary."""

    def construct(self) -> None:
        court = make_court(width=11, height=5).set_opacity(0.5)
        title = self.title("What the Math Says").to_edge(UP)
        bullets = VGroup(
            Text("Tennis points are Bernoulli trials.", font_size=34, color=LINE_WHITE),
            Text("Games are nonlinear probability machines.", font_size=34, color=LINE_WHITE),
            Text("Deuce creates recursion.", font_size=34, color=LINE_WHITE),
            Text("Small point edges become huge game edges.", font_size=34, color=BALL_YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        end = Text("Sports analytics is probability wearing sneakers.", font_size=38, color=TENNIS_GOLD, weight=BOLD).to_edge(DOWN)

        self.play(FadeIn(court), Write(title))
        self.play(LaggedStart(*[Write(line) for line in bullets], lag_ratio=0.2))
        self.play(Write(end), Circumscribe(end, color=TENNIS_GOLD))
        self.wait(1.2)
