from __future__ import annotations

import numpy as np
from manim import *

from utils.helpers import add_particle_drift, create_particle_field
from utils.style import BLUE_GLOW, GOLD_GLOW, MUTED_TEXT, TEXT_COLOR, glow_text, set_scene_style


class TitleScene(MovingCameraScene):
    """Cold open: particles organize into the thesis."""

    def construct(self) -> None:
        set_scene_style(self)
        particles = create_particle_field(120, color=BLUE_GLOW, seed=10)
        add_particle_drift(particles)
        self.add(particles)
        self.wait(1.5)

        grid_points = []
        for x in np.linspace(-5.5, 5.5, 12):
            for y in np.linspace(-2.3, 2.3, 5):
                grid_points.append(np.array([x, y, 0]))
        targets = [grid_points[i % len(grid_points)] for i in range(len(particles))]

        self.play(
            *[dot.animate.move_to(targets[i]).set_opacity(0.32) for i, dot in enumerate(particles)],
            run_time=3.0,
            rate_func=smooth,
        )

        title = Text("The Mathematics of Creativity", font_size=56, color=TEXT_COLOR, weight=BOLD)
        subtitle = Text("Why genius follows a formula", font_size=29, color=MUTED_TEXT)
        equation = MathTex(
            r"\mathrm{Creativity}\approx \mathrm{Attempts}\times\mathrm{Combinations}\times\mathrm{Time}\times\mathrm{Chaos}",
            font_size=28,
            color=GOLD_GLOW,
        )
        group = VGroup(glow_text(title, BLUE_GLOW, opacity=0.18), subtitle, equation).arrange(DOWN, buff=0.35)

        self.play(FadeIn(group[0], shift=UP * 0.15), run_time=1.4)
        self.play(FadeIn(subtitle), Write(equation), run_time=1.8)
        self.wait(6.5)
        self.play(FadeOut(group), particles.animate.set_opacity(0.08), run_time=1.0)
        particles.clear_updaters()
        self.play(FadeOut(particles), run_time=0.8)
