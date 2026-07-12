"""Scene 09 - synthesis and next-chapter bridge."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    label_pill,
    narration_wait,
    paced_play,
    scene_title,
)


class Scene09Synthesis(Scene):
    """Close the probability chain and point to distributions."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "09")
    scene.add(cinematic_background())

    title = scene_title("The probability chain now leads into machine learning").to_edge(UP, buff=0.34)
    paced_play(scene, FadeIn(title), run_time=0.8)

    chain_labels = [
        ("P(A)", cfg.CYAN),
        ("Complement", cfg.GREEN),
        ("Addition", cfg.GOLD),
        ("Multiplication", cfg.ORANGE),
        ("Conditional", cfg.PURPLE),
        ("Bayes", cfg.RED),
        ("Random variable", cfg.CYAN),
        ("Distribution", cfg.GOLD),
        ("Joint / Marginal", cfg.BLUE),
        ("Independence", cfg.GREEN),
        ("P(y | x)", cfg.RED),
        ("ML prediction", cfg.CYAN),
    ]
    nodes = VGroup(*[label_pill(text, color, font_size=18) for text, color in chain_labels])
    row1 = VGroup(*nodes[:4]).arrange(RIGHT, buff=0.42).move_to(UP * 1.18)
    row2 = VGroup(nodes[7], nodes[6], nodes[5], nodes[4]).arrange(RIGHT, buff=0.42).move_to(UP * 0.06)
    row3 = VGroup(*nodes[8:12]).arrange(RIGHT, buff=0.42).move_to(DOWN * 1.06)

    arrows = VGroup()
    for i in range(3):
        arrows.add(Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=cfg.MUTED, buff=0.11, stroke_width=2.2, max_tip_length_to_length_ratio=0.18))
    for i in range(4, 7):
        arrows.add(Arrow(nodes[i].get_left(), nodes[i + 1].get_right(), color=cfg.MUTED, buff=0.11, stroke_width=2.2, max_tip_length_to_length_ratio=0.18))
    for i in range(8, 11):
        arrows.add(Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=cfg.MUTED, buff=0.11, stroke_width=2.2, max_tip_length_to_length_ratio=0.18))
    arrows.add(Arrow(nodes[3].get_bottom(), nodes[4].get_top(), color=cfg.MUTED, buff=0.12, stroke_width=2.2, max_tip_length_to_length_ratio=0.18))
    arrows.add(Arrow(nodes[7].get_bottom(), nodes[8].get_top(), color=cfg.MUTED, buff=0.12, stroke_width=2.2, max_tip_length_to_length_ratio=0.18))

    paced_play(scene, LaggedStart(*[FadeIn(node, scale=0.82) for node in nodes], lag_ratio=0.06), run_time=1.7)
    paced_play(scene, LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.04), run_time=1.1)
    narration_wait(scene, 0.6)

    takeaway = Text("Useful prediction under uncertainty.", font_size=29, color=cfg.WHITE, weight=BOLD)
    takeaway.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    takeaway.to_edge(DOWN, buff=0.45)
    paced_play(scene, FadeIn(takeaway, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 0.8)

    paced_play(scene, FadeOut(nodes), FadeOut(arrows), FadeOut(takeaway), run_time=0.75)

    question = Text("Next question: what shapes can a distribution take?", font_size=27, color=cfg.WHITE, weight=BOLD)
    question.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    question.move_to(UP * 1.05)

    baseline = Line(LEFT * 2.25, RIGHT * 2.25, color=cfg.MUTED, stroke_width=2)
    bell_curve = ParametricFunction(
        lambda t: np.array([t, 1.45 * np.exp(-(t**2) / 0.92), 0]),
        t_range=[-2.2, 2.2],
        color=cfg.CYAN,
        stroke_width=5,
    )
    skew_curve = ParametricFunction(
        lambda t: np.array([t, 1.32 * (t + 2.05) * np.exp(-1.35 * (t + 2.05)), 0]),
        t_range=[-2.0, 3.0],
        color=cfg.GOLD,
        stroke_width=5,
    )
    bell_shape = VGroup(baseline.copy(), bell_curve).scale(0.78)
    skew_shape = VGroup(baseline.copy(), skew_curve).scale(0.78)
    distribution_shapes = VGroup(bell_shape, skew_shape).arrange(RIGHT, buff=0.75)
    distribution_shapes.move_to(DOWN * 0.15)

    next_title = Text("Next: Probability Distributions", font_size=31, color=cfg.GOLD, weight=BOLD)
    next_subtitle = Text("The Patterns Behind Data", font_size=25, color=cfg.CYAN, weight=BOLD)
    next_card = VGroup(next_title, next_subtitle).arrange(DOWN, buff=0.1)
    next_card.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    next_card.to_edge(DOWN, buff=0.82)

    paced_play(scene, FadeIn(question, shift=UP * 0.12), run_time=0.8)
    paced_play(scene, LaggedStart(Create(bell_shape), Create(skew_shape), lag_ratio=0.35), run_time=1.4)
    paced_play(scene, FadeIn(next_card, shift=UP * 0.14), run_time=0.8)
    narration_wait(scene, 0.8)

    end_scene(scene, scene_start)
