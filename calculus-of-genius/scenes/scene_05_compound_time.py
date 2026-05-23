from __future__ import annotations

from manim import *

from utils.equations import compound_growth_equation
from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, MUTED_TEXT, TEXT_COLOR, glow_text, set_scene_style


class CompoundTimeScene(MovingCameraScene):
    """Skill as compounding growth through repeated practice."""

    def construct(self) -> None:
        set_scene_style(self)
        title = Text("Skill Compounds in Time", font_size=44, color=TEXT_COLOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(glow_text(title, GREEN_GLOW, opacity=0.15)), run_time=1.0)

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 8, 1],
            x_length=9.3,
            y_length=4.3,
            tips=False,
            axis_config={"color": MUTED_TEXT, "stroke_width": 1.2},
        ).shift(DOWN * 0.55)
        curve = axes.plot(lambda x: 0.55 * (1.28**x), x_range=[0, 10], color=GOLD_GLOW, stroke_width=5)
        flat = axes.plot(lambda x: 0.35 + 0.17 * x, x_range=[0, 5], color=BLUE_GLOW, stroke_width=3, stroke_opacity=0.65)
        self.play(Create(axes), Create(flat), run_time=1.2)
        self.play(Transform(flat, curve), run_time=2.0)

        equation = compound_growth_equation(42).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(glow_text(equation, GOLD_GLOW, opacity=0.14)), run_time=1.0)

        t = ValueTracker(0)
        moving_dot = always_redraw(lambda: Dot(axes.c2p(t.get_value(), 0.55 * (1.28 ** t.get_value())), radius=0.08, color=GOLD_GLOW))
        trace = TracedPath(moving_dot.get_center, stroke_color=GOLD_GLOW, stroke_width=4, dissipating_time=0.25)
        self.add(trace, moving_dot)
        self.play(t.animate.set_value(10), run_time=4.0, rate_func=smooth)

        labels = VGroup(
            Text("invisible phase", font_size=20, color=MUTED_TEXT).move_to(axes.c2p(2.0, 1.25)),
            Text("acceleration", font_size=20, color=GREEN_GLOW).move_to(axes.c2p(6.7, 3.0)),
            Text("breakthrough", font_size=22, color=GOLD_GLOW).move_to(axes.c2p(9.15, 6.6)),
        )
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in labels], lag_ratio=0.18), run_time=1.2)

        blocks = VGroup()
        for i in range(20):
            block = Square(side_length=0.16, color=BLUE_GLOW, fill_color=BLUE_GLOW, fill_opacity=0.35, stroke_width=0.5)
            block.move_to(LEFT * 5.45 + DOWN * 2.5 + RIGHT * (i % 10) * 0.22 + UP * (i // 10) * 0.22)
            blocks.add(block)
        practice = Text("little and often", font_size=20, color=MUTED_TEXT).next_to(blocks, UP, buff=0.15)
        self.play(FadeIn(practice), LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.035), run_time=1.4)
        self.wait(35.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
