"""Scene 01 - the real world is noisy, so ML speaks in probabilities."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    dot_cloud,
    end_scene,
    envelope_icon,
    narration_wait,
    paced_play,
    probability_bar,
    tiny_model,
)


class Scene01Uncertainty(Scene):
    """Open on the core question: how does ML predict under uncertainty?"""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "01")
    scene.add(cinematic_background())

    question = Text(
        "How does a model predict when the world is noisy?",
        font_size=30, color=cfg.WHITE, weight=BOLD,
    ).set_stroke("#02111D", width=4, opacity=0.8, background=True)
    question.to_edge(UP, buff=0.72)
    paced_play(scene, FadeIn(question, shift=UP * 0.1), run_time=0.9)
    narration_wait(scene, 0.6)

    noise = dot_cloud(count=58, width=4.4, height=2.0, center=LEFT * 4.4 + DOWN * 0.55, seed=21)
    noise_label = Text("messy evidence", font_size=22, color=cfg.MUTED, weight=BOLD)
    noise_label.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    noise_label.next_to(noise, DOWN, buff=0.24)
    paced_play(scene, FadeOut(question), FadeIn(noise), FadeIn(noise_label), run_time=0.9)
    narration_wait(scene, 0.35)

    envelope = envelope_icon(cfg.CYAN, width=1.6, height=1.05).scale(1.4).move_to(LEFT * 4.4 + DOWN * 0.6)
    model = tiny_model("ML model").scale(1.3).move_to(DOWN * 0.6)
    arrow_in = Arrow(envelope.get_right(), model.get_left(), color=cfg.MUTED, buff=0.2, stroke_width=4)

    paced_play(scene, FadeOut(noise), FadeOut(noise_label), FadeIn(envelope, shift=RIGHT * 0.2), run_time=0.8)
    paced_play(scene, Create(arrow_in), FadeIn(model, shift=LEFT * 0.2), run_time=0.9)

    bar = probability_bar(0.95, "P(spam)", color=cfg.RED, width=4.6).move_to(RIGHT * 3.6 + DOWN * 0.6)
    arrow_out = Arrow(model.get_right(), bar.get_left(), color=cfg.MUTED, buff=0.25, stroke_width=4)

    paced_play(scene, Create(arrow_out), run_time=0.6)
    fill = bar[1]
    fill.stretch_to_fit_width(0.01, about_edge=LEFT)
    paced_play(scene, FadeIn(bar[0]), FadeIn(bar[2]), FadeIn(bar[3]), FadeIn(bar[5]), run_time=0.5)
    target_fill = probability_bar(0.95, "P(spam)", color=cfg.RED, width=4.6).move_to(bar.get_center())[1]
    paced_play(scene, Transform(fill, target_fill), FadeIn(bar[4]), run_time=1.2)
    paced_play(scene, Indicate(bar[4], color=cfg.WHITE, scale_factor=1.15), run_time=0.6)

    caption = Text(
        "Not certainty. Confidence, expressed as a number.",
        font_size=28, color=cfg.GOLD, weight=BOLD,
    ).set_stroke("#02111D", width=4, opacity=0.8, background=True)
    caption.to_edge(DOWN, buff=0.5)
    paced_play(scene, FadeIn(caption, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 0.65)

    visual_group = VGroup(envelope, arrow_in, model, arrow_out, bar, caption)
    title_top = Text("Probability Basics", font_size=52, color=cfg.CYAN, weight=BOLD)
    title_bottom = Text("Every ML Learner Must Know", font_size=44, color=cfg.CYAN, weight=BOLD)
    subtitle = Text("the language of uncertainty", font_size=31, color=cfg.WHITE)
    rule = Line(LEFT, RIGHT, color=cfg.GOLD, stroke_width=5)
    rule.width = 7.3
    final_title = VGroup(title_top, title_bottom, rule, subtitle).arrange(DOWN, buff=0.14)
    final_title.set_stroke("#02111D", width=5, opacity=0.85, background=True)
    if final_title.width > cfg.SAFE_FRAME_WIDTH:
        final_title.scale_to_fit_width(cfg.SAFE_FRAME_WIDTH)
    final_title.move_to(ORIGIN)

    paced_play(scene, FadeOut(visual_group, shift=DOWN * 0.12), run_time=0.75)
    paced_play(scene, FadeIn(final_title, shift=UP * 0.18), run_time=0.9)
    narration_wait(scene, 0.9)

    end_scene(scene, scene_start)
