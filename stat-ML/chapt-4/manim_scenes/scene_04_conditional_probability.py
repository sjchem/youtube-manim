"""Scene 04 - conditional probability from joint probability."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    envelope_icon,
    equation_box,
    label_pill,
    narration_wait,
    paced_play,
    probability_bar,
    scene_title,
    venn_two_circles,
)


class Scene04ConditionalProbability(Scene):
    """Derive conditional probability and connect it to spam evidence."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "04")
    scene.add(cinematic_background())

    title = scene_title("Conditional probability means restricting the world").to_edge(UP, buff=0.34)
    paced_play(scene, FadeIn(title), run_time=0.8)

    venn = venn_two_circles("A", "B", cfg.RED, cfg.GOLD, radius=1.32, separation=1.85)
    venn.move_to(LEFT * 3.35 + UP * 0.35)
    overlap = Intersection(venn[0], venn[1], fill_color=cfg.WHITE, fill_opacity=0.55, stroke_width=0)
    b_region = label_pill("given B", cfg.GOLD, font_size=20).next_to(venn[1], DOWN, buff=0.28)
    overlap_tag = Text("A and B", font_size=19, color=cfg.WHITE, weight=BOLD).move_to(overlap)
    overlap_tag.set_stroke("#02111D", width=4, opacity=0.8, background=True)

    definition = equation_box(r"P(A \mid B) = {P(A \cap B) \over P(B)}", cfg.GOLD, font_size=39)
    definition.move_to(RIGHT * 2.35 + UP * 1.0)
    symbol_notes = VGroup(
        Text("P(B): the world after evidence", font_size=20, color=cfg.GOLD, weight=BOLD),
        Text("P(A ∩ B): the part where both are true", font_size=20, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    symbol_notes.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    symbol_notes.next_to(definition, DOWN, buff=0.28)

    paced_play(scene, FadeIn(venn), run_time=0.9)
    paced_play(scene, FadeIn(overlap), FadeIn(overlap_tag), FadeIn(b_region), run_time=0.9)
    paced_play(scene, FadeIn(definition, shift=UP * 0.12), FadeIn(symbol_notes), run_time=1.0)
    narration_wait(scene, 0.8)

    paced_play(scene, FadeOut(venn), FadeOut(overlap), FadeOut(overlap_tag), FadeOut(b_region), FadeOut(definition), FadeOut(symbol_notes), run_time=0.7)

    envelope = envelope_icon(cfg.CYAN, width=1.35, height=0.9).scale(1.08).move_to(LEFT * 3.6 + UP * 0.95)
    feature_chips = VGroup(
        label_pill('"free"', cfg.GOLD, font_size=21),
        label_pill("many links", cfg.ORANGE, font_size=19),
        label_pill("unknown sender", cfg.PURPLE, font_size=19),
    ).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
    feature_chips.scale_to_fit_width(2.45)
    feature_chips.next_to(envelope, RIGHT, buff=0.22)
    prior_bar = probability_bar(0.30, "P(spam)", color=cfg.MUTED, width=3.9).move_to(RIGHT * 2.55 + UP * 0.72)
    posterior_bar = probability_bar(0.95, "P(spam | features)", color=cfg.RED, width=3.9).move_to(RIGHT * 2.55 + DOWN * 0.72)
    arrow = Arrow(prior_bar.get_bottom(), posterior_bar.get_top(), color=cfg.GOLD, buff=0.18, stroke_width=3.0)
    condition = equation_box(r"P(\text{spam} \mid \text{email features}) = 0.95", cfg.RED, font_size=32)
    condition.to_edge(DOWN, buff=0.42)

    paced_play(scene, FadeIn(envelope), LaggedStart(*[FadeIn(chip, shift=LEFT * 0.1) for chip in feature_chips], lag_ratio=0.15), run_time=1.0)
    paced_play(scene, FadeIn(prior_bar), Create(arrow), FadeIn(posterior_bar), run_time=1.0)
    paced_play(scene, FadeIn(condition, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 0.9)

    end_scene(scene, scene_start)
