"""Standalone opening clip to place before Scene 10 in the two-part edit."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import add_cinematic_background, coordinate_axes, eq, glow_dot, outlined_text


class Scene10Part2Opening(Scene):
    """Recap forward trigonometry, then reverse outputs back to an angle."""

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
        full_wave = axes.plot(np.sin, x_range=[0, TAU], color=cfg.CYAN, stroke_width=6)

        def circle_position() -> np.ndarray:
            angle = theta.get_value()
            return center + radius * np.array([np.cos(angle), np.sin(angle), 0])

        radius_line = always_redraw(
            lambda: Line(center, circle_position(), color=cfg.GOLD, stroke_width=7)
        )
        horizontal = always_redraw(
            lambda: Line(center, [circle_position()[0], center[1], 0], color=cfg.GREEN, stroke_width=7)
        )
        vertical = always_redraw(
            lambda: Line([circle_position()[0], center[1], 0], circle_position(), color=cfg.CYAN, stroke_width=7)
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
        forward_label = outlined_text("FORWARD:  ANGLE  →  COORDINATES  →  WAVE", cfg.FONT["label"], cfg.GOLD, BOLD)
        forward_label.to_edge(UP, buff=0.45)

        self.play(
            LaggedStart(Create(circle), Create(cross), Create(axes), Create(full_wave), FadeIn(forward_label), lag_ratio=0.14),
            run_time=1.4,
        )
        self.add(radius_line, horizontal, vertical, transfer, circle_point, graph_point)
        self.play(theta.animate.set_value(TAU), run_time=3.8, rate_func=linear)
        self.play(theta.animate.set_value(PI / 6), run_time=1.2, rate_func=smooth)
        self.play(Indicate(circle_point, color=cfg.WHITE, scale_factor=1.18), run_time=0.65)

        recap_visual = VGroup(
            circle,
            cross,
            axes,
            full_wave,
            radius_line,
            horizontal,
            vertical,
            transfer,
            circle_point,
            graph_point,
            forward_label,
        )
        self.play(FadeOut(recap_visual), run_time=0.7)

        output_data = (
            ("HEIGHT", r"\frac12", cfg.CYAN),
            ("HORIZONTAL", r"\frac{\sqrt3}{2}", cfg.GREEN),
            ("SLOPE", r"\frac1{\sqrt3}", cfg.ORANGE),
        )
        output_cards = VGroup()
        for label, value, color in output_data:
            box = RoundedRectangle(
                width=3.65,
                height=1.65,
                corner_radius=0.16,
                color=color,
                fill_color=cfg.PANEL,
                fill_opacity=0.9,
            )
            content = VGroup(
                outlined_text(label, cfg.FONT["small"], color, BOLD),
                eq(value, cfg.WHITE, cfg.FONT["section"]),
            ).arrange(DOWN, buff=0.16).move_to(box)
            output_cards.add(VGroup(box, content))
        output_cards.arrange(RIGHT, buff=0.55).move_to(UP * 1.35)

        output_colors = (cfg.CYAN, cfg.GREEN, cfg.ORANGE)
        reverse_arrows = VGroup(
            *[
                Arrow(card.get_bottom(), [0, -0.45, 0], color=color, stroke_width=4, buff=0.13)
                for card, color in zip(output_cards, output_colors, strict=True)
            ]
        )
        reverse_question = outlined_text("WHICH ANGLE PRODUCED THEM?", cfg.FONT["body"], cfg.GOLD, BOLD)
        reverse_question.move_to(DOWN * 0.90)
        theta_question = eq(r"\theta=?", cfg.WHITE, cfg.FONT["hero"]).move_to(DOWN * 2.05)
        theta_answer = eq(r"\theta=30^\circ", cfg.GOLD, cfg.FONT["hero"]).move_to(theta_question)

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.15) for card in output_cards], lag_ratio=0.18), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in reverse_arrows], lag_ratio=0.15), FadeIn(reverse_question), run_time=0.8)
        self.play(FadeIn(theta_question, scale=1.08), run_time=0.6)
        self.play(ReplacementTransform(theta_question, theta_answer), Indicate(theta_answer, color=cfg.WHITE), run_time=0.9)
        self.play(FadeOut(VGroup(output_cards, reverse_arrows, reverse_question, theta_answer)), run_time=0.65)

        part_label = outlined_text("PART 2", cfg.FONT["small"], cfg.PURPLE, BOLD)
        main_title = outlined_text("VISUAL TRIGONOMETRY", cfg.FONT["title"], cfg.WHITE, BOLD)
        subtitle = outlined_text(
            "FROM INVERSE FUNCTIONS TO EULER’S FORMULA",
            cfg.FONT["section"],
            cfg.GOLD,
            BOLD,
        )
        if subtitle.width > cfg.SAFE_WIDTH - 0.7:
            subtitle.scale_to_fit_width(cfg.SAFE_WIDTH - 0.7)
        title_group = VGroup(part_label, main_title, subtitle).arrange(DOWN, buff=0.24).move_to(ORIGIN)
        rule = Line(LEFT * 4.4, RIGHT * 4.4, color=cfg.CYAN, stroke_width=5).next_to(main_title, DOWN, buff=0.2)
        title_group.add(rule)

        self.play(FadeIn(part_label), run_time=0.4)
        self.play(FadeIn(main_title, shift=UP * 0.12), Create(rule), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.12), run_time=0.75)
        self.play(title_group.animate.scale(1.012), run_time=2.2, rate_func=there_and_back)
        self.play(FadeOut(title_group), run_time=0.55)
