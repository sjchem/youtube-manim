from __future__ import annotations

from math import comb

import numpy as np
from manim import *

from utils.equations import combinations_equation
from utils.helpers import mini_icon
from utils.particles import create_idea_collision_animation, optional_charge_field
from utils.style import BLUE_GLOW, GOLD_GLOW, GREEN_GLOW, MUTED_TEXT, PURPLE_GLOW, TEXT_COLOR, glow_text, set_scene_style


class CombinatorialScene(MovingCameraScene):
    """Ideas as recombinations of existing ingredients."""

    def construct(self) -> None:
        set_scene_style(self)
        title = Text("Innovation Is Remix", font_size=46, color=TEXT_COLOR, weight=BOLD).to_edge(UP)
        self.play(FadeIn(glow_text(title, PURPLE_GLOW, opacity=0.16)), run_time=1.0)

        labels = ["MUSIC", "MATH", "IMAGE", "ATOM", "CODE", "STORY"]
        colors = [BLUE_GLOW, GOLD_GLOW, PURPLE_GLOW, GREEN_GLOW, BLUE_GLOW, GOLD_GLOW]
        blocks = VGroup(*[mini_icon(label, colors[i]) for i, label in enumerate(labels)]).arrange(RIGHT, buff=0.24)
        blocks.move_to(UP * 1.65)
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in blocks], lag_ratio=0.12), run_time=1.4)

        chosen = VGroup(blocks[1].copy(), blocks[3].copy(), blocks[5].copy()).arrange(RIGHT, buff=0.18).move_to(LEFT * 3.4 + DOWN * 0.65)
        arrow = Arrow(LEFT * 1.6 + DOWN * 0.65, RIGHT * 0.2 + DOWN * 0.65, color=MUTED_TEXT, buff=0.1)
        new_idea = VGroup(
            Circle(radius=0.52, color=GOLD_GLOW, fill_color=GOLD_GLOW, fill_opacity=0.08),
            Text("NEW", font_size=24, color=TEXT_COLOR, weight=BOLD),
        ).move_to(RIGHT * 1.35 + DOWN * 0.65)
        self.play(TransformFromCopy(VGroup(blocks[1], blocks[3], blocks[5]), chosen), GrowArrow(arrow), FadeIn(new_idea), run_time=1.4)

        equation = combinations_equation(44).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(glow_text(equation, BLUE_GLOW, opacity=0.13)), run_time=1.0)

        counts = VGroup()
        for n in [5, 10, 20]:
            counts.add(Text(f"n = {n} -> {comb(n, 2)} pairs", font_size=25, color=TEXT_COLOR))
        counts.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.85).shift(UP * 0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in counts], lag_ratio=0.22), run_time=1.3)

        network = VGroup()
        node_points = [np.array([np.cos(TAU * i / 9), np.sin(TAU * i / 9), 0]) * 1.15 for i in range(9)]
        node_group = VGroup(*[Dot(p, radius=0.055, color=BLUE_GLOW) for p in node_points])
        for i, p in enumerate(node_points):
            for j in range(i + 1, len(node_points)):
                if (i + j) % 4 == 0:
                    network.add(Line(p, node_points[j], color=PURPLE_GLOW, stroke_width=1.2, stroke_opacity=0.45))
        network.add(node_group)
        network.move_to(LEFT * 4.5 + DOWN * 1.15)
        self.play(Create(network), run_time=1.4)

        physics_field = optional_charge_field().scale(0.75).move_to(RIGHT * 4.2 + DOWN * 1.2)
        if len(physics_field) > 0:
            note = Text("manim-physics field", font_size=16, color=MUTED_TEXT).next_to(physics_field, DOWN, buff=0.1)
            self.play(FadeIn(physics_field), FadeIn(note), run_time=1.0)

        particles = VGroup(*[Dot(blocks[i].get_center(), radius=0.055, color=colors[i]) for i in range(4)])
        self.add(particles)
        molecule = create_idea_collision_animation(self, particles, center=RIGHT * 4.0 + UP * 1.0)
        label = Text("old ingredients, new arrangement", font_size=23, color=MUTED_TEXT).next_to(molecule, DOWN, buff=0.15)
        self.play(FadeIn(label), run_time=0.7)
        self.wait(38.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
