"""Scene 02 - probability as a function, plus the complement rule."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    equation_box,
    label_pill,
    narration_wait,
    paced_play,
    probability_bar,
    scene_title,
)


class Scene02ProbabilityScale(Scene):
    """Introduce P(A), the 0-to-1 range, sample space, and complements."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "02")
    scene.add(cinematic_background())

    title = scene_title("Probability assigns a number to an event").to_edge(UP, buff=0.34)
    paced_play(scene, FadeIn(title), run_time=0.8)

    p_of_a = equation_box(r"P(A)", cfg.CYAN, font_size=52).move_to(LEFT * 3.75 + UP * 1.35)
    event_note = VGroup(
        Text("A = event", font_size=23, color=cfg.WHITE, weight=BOLD),
        Text("P(A) = probability", font_size=23, color=cfg.CYAN, weight=BOLD),
    ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    event_note.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    event_note.next_to(p_of_a, RIGHT, buff=0.55)

    paced_play(scene, FadeIn(p_of_a, shift=UP * 0.12), FadeIn(event_note), run_time=1.0)
    narration_wait(scene, 0.4)

    range_rule = equation_box(r"0 \leq P(A) \leq 1", cfg.GOLD, font_size=40)
    sample_space = equation_box(r"P(\Omega) = 1", cfg.GREEN, font_size=40)
    rules = VGroup(range_rule, sample_space).arrange(RIGHT, buff=0.55).move_to(UP * 0.08)
    paced_play(scene, FadeIn(rules, shift=UP * 0.12), run_time=1.0)

    rain_line = NumberLine(x_range=[0, 1, 0.25], length=6.3, include_numbers=True, font_size=20, color=cfg.MUTED, tick_size=0.08)
    rain_line.move_to(DOWN * 1.35)
    rain_dot = Dot(rain_line.n2p(0.3), radius=0.11, color=cfg.BLUE)
    rain_label = label_pill("P(Rain) = 0.30", cfg.BLUE, font_size=21).next_to(rain_dot, DOWN, buff=0.38)
    rain_caption = Text("30% chance of rain", font_size=22, color=cfg.WHITE, weight=BOLD)
    rain_caption.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    rain_caption.next_to(rain_label, DOWN, buff=0.28)
    rain_group = VGroup(rain_line, rain_dot, rain_label, rain_caption)

    paced_play(scene, Create(rain_line), FadeIn(rain_dot), FadeIn(rain_label), FadeIn(rain_caption), run_time=1.2)
    narration_wait(scene, 0.5)

    complement_rule = equation_box(r"P(A^c) = 1 - P(A)", cfg.RED, font_size=40)
    complement_rule.move_to(UP * 1.05)
    spam_bar = probability_bar(0.95, "P(spam)", color=cfg.RED, width=3.65).move_to(LEFT * 2.5 + DOWN * 0.95)
    not_spam_bar = probability_bar(0.05, "P(not spam)", color=cfg.GREEN, width=3.65).move_to(RIGHT * 2.5 + DOWN * 0.95)
    binary_note = Text("If spam is 0.95, not spam is 0.05.", font_size=23, color=cfg.WHITE, weight=BOLD)
    binary_note.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    binary_note.to_edge(DOWN, buff=0.38)

    paced_play(scene, FadeOut(p_of_a), FadeOut(event_note), FadeOut(rules), FadeOut(rain_group), run_time=0.65)
    paced_play(scene, FadeIn(complement_rule, shift=UP * 0.12), run_time=0.8)
    paced_play(scene, FadeIn(spam_bar), FadeIn(not_spam_bar), FadeIn(binary_note), run_time=1.0)
    narration_wait(scene, 0.9)

    end_scene(scene, scene_start)
