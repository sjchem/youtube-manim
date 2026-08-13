"""Standalone closing clip to place after Scene 09 in the two-part edit."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import add_cinematic_background, coordinate_axes, glow_dot, outlined_text


class Scene09Part1Ending(Scene):
    """Close Part 1 without changing the already-rendered Scene 09."""

    def construct(self) -> None:
        cfg.apply_project_theme(self, bubbles=False)
        add_cinematic_background(self)

        center = np.array([-4.45, 0.35, 0.0])
        radius = 1.75
        theta = ValueTracker(0.001)
        circle = Circle(radius=radius, color=cfg.WHITE, stroke_width=5).move_to(center)
        cross = VGroup(
            Line(center + LEFT * 2.05, center + RIGHT * 2.05, color=cfg.GRAY, stroke_width=2),
            Line(center + DOWN * 2.05, center + UP * 2.05, color=cfg.GRAY, stroke_width=2),
        )
        axes = coordinate_axes(x_length=6.4, y_length=3.5).move_to([3.1, 0.35, 0])

        def circle_position() -> np.ndarray:
            angle = theta.get_value()
            return center + radius * np.array([np.cos(angle), np.sin(angle), 0])

        radius_line = always_redraw(
            lambda: Line(center, circle_position(), color=cfg.GOLD, stroke_width=7)
        )
        circle_point = always_redraw(lambda: glow_dot(circle_position(), cfg.GOLD, 0.09))
        graph_point = always_redraw(
            lambda: glow_dot(axes.c2p(theta.get_value(), np.sin(theta.get_value())), cfg.GOLD, 0.07)
        )
        transfer = always_redraw(
            lambda: DashedLine(
                circle_position(),
                axes.c2p(theta.get_value(), np.sin(theta.get_value())),
                color=cfg.CYAN,
                stroke_width=2.5,
                dash_length=0.12,
            )
        )
        live_wave = always_redraw(
            lambda: axes.plot(
                np.sin,
                x_range=[0, max(theta.get_value(), 0.001)],
                color=cfg.CYAN,
                stroke_width=7,
            )
        )

        recap = outlined_text("AN ANGLE BECAME A WAVE", cfg.FONT["body"], cfg.GOLD, BOLD)
        recap.to_edge(UP, buff=0.45)
        self.play(
            LaggedStart(Create(circle), Create(cross), Create(axes), FadeIn(recap), lag_ratio=0.16),
            run_time=1.4,
        )
        self.add(radius_line, live_wave, transfer, circle_point, graph_point)
        self.play(theta.animate.set_value(TAU), run_time=4.6, rate_func=linear)
        self.play(Indicate(graph_point, color=cfg.WHITE, scale_factor=1.2), run_time=0.7)

        visual_group = VGroup(
            circle,
            cross,
            axes,
            radius_line,
            circle_point,
            graph_point,
            transfer,
            live_wave,
            recap,
        )
        self.play(FadeOut(visual_group), run_time=0.75)

        part_label = outlined_text("PART 1 COMPLETE", cfg.FONT["small"], cfg.CYAN, BOLD)
        main_title = outlined_text("VISUAL TRIGONOMETRY", cfg.FONT["title"], cfg.WHITE, BOLD)
        subtitle = outlined_text("FROM TRIANGLES TO WAVES", cfg.FONT["section"], cfg.GOLD, BOLD)
        part_one = VGroup(part_label, main_title, subtitle).arrange(DOWN, buff=0.22).move_to(UP * 1.05)

        question = outlined_text("Can we run the wave backward?", cfg.FONT["body"], cfg.WHITE, BOLD)
        arrow = Arrow(UP * 0.35, DOWN * 0.35, color=cfg.PURPLE, stroke_width=5, buff=0)
        continue_label = outlined_text("CONTINUE TO PART 2", cfg.FONT["small"], cfg.PURPLE, BOLD)
        next_title = outlined_text(
            "From Inverse Functions to Euler’s Formula",
            cfg.FONT["label"],
            cfg.WHITE,
            BOLD,
        )
        if next_title.width > cfg.SAFE_WIDTH - 0.7:
            next_title.scale_to_fit_width(cfg.SAFE_WIDTH - 0.7)
        invitation = VGroup(question, arrow, continue_label, next_title).arrange(DOWN, buff=0.18).move_to(DOWN * 1.75)

        self.play(FadeIn(part_label), run_time=0.45)
        self.play(FadeIn(main_title, shift=UP * 0.12), FadeIn(subtitle, shift=UP * 0.12), run_time=0.9)
        self.play(FadeIn(question), GrowArrow(arrow), run_time=0.75)
        self.play(FadeIn(continue_label), FadeIn(next_title, shift=UP * 0.1), run_time=0.75)
        self.play(VGroup(part_one, invitation).animate.scale(1.012), run_time=1.5, rate_func=there_and_back)
        self.play(FadeOut(VGroup(part_one, invitation)), run_time=0.55)
