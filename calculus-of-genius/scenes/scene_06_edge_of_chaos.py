from __future__ import annotations

import numpy as np
from manim import *

from utils.particles import RandomWalker, create_edge_of_chaos_particles
from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, MUTED_TEXT, PURPLE_GLOW, RED_GLOW, TEXT_COLOR, glow_text, set_scene_style, soft_panel


class EdgeOfChaosScene(MovingCameraScene):
    """Creativity peaks between rigid order and pure randomness."""

    def construct(self) -> None:
        set_scene_style(self)
        title = Text("The Edge of Chaos", font_size=46, color=TEXT_COLOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(glow_text(title, PURPLE_GLOW, opacity=0.17)), run_time=1.0)

        centers = [LEFT * 4.25 + DOWN * 0.25, DOWN * 0.25, RIGHT * 4.25 + DOWN * 0.25]
        panel_colors = [BLUE_GLOW, RED_GLOW, GREEN_GLOW]
        panels = VGroup(*[soft_panel(3.55, 3.1, panel_colors[i]).move_to(centers[i]) for i in range(3)])
        labels = VGroup(
            Text("too much order", font_size=21, color=BLUE_GLOW).next_to(panels[0], UP, buff=0.16),
            Text("too much chaos", font_size=21, color=PURPLE_GLOW).next_to(panels[1], UP, buff=0.16),
            Text("edge of chaos", font_size=21, color=GREEN_GLOW).next_to(panels[2], UP, buff=0.16),
        )
        self.play(FadeIn(panels), FadeIn(labels), run_time=1.0)

        grid = VGroup()
        for x in np.linspace(-1.25, 1.25, 6):
            for y in np.linspace(-0.95, 0.95, 5):
                grid.add(Dot(centers[0] + np.array([x, y, 0]), radius=0.035, color=BLUE_GLOW, fill_opacity=0.75))
        chaos = RandomWalker(
            count=48,
            bounds=(centers[1][0] - 1.45, centers[1][0] + 1.45, centers[1][1] - 1.1, centers[1][1] + 1.1),
            color=PURPLE_GLOW,
            seed=44,
        )
        edge = create_edge_of_chaos_particles(center=centers[2], count=58, seed=56)
        self.play(FadeIn(grid), FadeIn(chaos), FadeIn(edge), run_time=1.2)
        self.wait(2.0)

        formula = MathTex(r"\mathrm{Creativity}=\mathrm{Structure}\times\mathrm{Variation}", font_size=38, color=TEXT_COLOR)
        formula.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(glow_text(formula, GREEN_GLOW, opacity=0.14)), run_time=1.0)

        slider_line = Line(LEFT * 3.4, RIGHT * 3.4, color=MUTED_TEXT, stroke_width=3).shift(DOWN * 2.7)
        low = Text("low entropy", font_size=17, color=MUTED_TEXT).next_to(slider_line, LEFT, buff=0.18)
        high = Text("high entropy", font_size=17, color=MUTED_TEXT).next_to(slider_line, RIGHT, buff=0.18)
        knob = Dot(slider_line.get_start(), radius=0.11, color=GOLD_GLOW)
        halo = Circle(radius=0.23, color=GOLD_GLOW, fill_color=GOLD_GLOW, fill_opacity=0.1, stroke_opacity=0.35).move_to(knob)
        self.play(Create(slider_line), FadeIn(low), FadeIn(high), FadeIn(halo), FadeIn(knob), run_time=0.9)
        mid = slider_line.point_from_proportion(0.5)
        self.play(knob.animate.move_to(mid), halo.animate.move_to(mid), run_time=1.5)
        balance = Text("balance", font_size=22, color=GOLD_GLOW).next_to(knob, UP, buff=0.18)
        self.play(FadeIn(balance), run_time=0.6)
        self.wait(41.0)
        chaos.clear_updaters()
        edge.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
