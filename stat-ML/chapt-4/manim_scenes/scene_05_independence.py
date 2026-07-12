"""Scene 05 - Bayes' theorem derived from conditional probability."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    bayes_flow,
    begin_scene,
    cinematic_background,
    end_scene,
    equation_box,
    narration_wait,
    paced_play,
    scene_title,
)


class Scene05Independence(Scene):
    """Derive Bayes' theorem in three short steps."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "05")
    scene.add(cinematic_background())

    title = scene_title("Bayes is conditional probability turned around").to_edge(UP, buff=0.34)
    paced_play(scene, FadeIn(title), run_time=0.8)

    flow = bayes_flow("2% risk", "positive test", "updated risk").scale(0.78).move_to(UP * 1.18)
    paced_play(scene, FadeIn(flow[0][0]), run_time=0.55)
    paced_play(scene, Create(flow[1]), FadeIn(flow[0][1]), run_time=0.65)
    paced_play(scene, Create(flow[2]), FadeIn(flow[0][2]), run_time=0.65)
    narration_wait(scene, 0.35)
    paced_play(scene, FadeOut(flow, shift=UP * 0.12), run_time=0.55)

    step1 = equation_box(r"P(H \mid E) = {P(H \cap E) \over P(E)}", cfg.CYAN, font_size=34)
    step2 = equation_box(r"P(H \cap E) = P(E \mid H)P(H)", cfg.GOLD, font_size=34)
    step3 = equation_box(r"P(H \mid E) = {P(E \mid H)P(H) \over P(E)}", cfg.GREEN, font_size=34)
    steps = VGroup(step1, step2, step3).arrange(DOWN, buff=0.28).move_to(RIGHT * 2.05 + DOWN * 0.56)

    labels = VGroup(
        Text("1. Conditional probability", font_size=25, color=cfg.CYAN, weight=BOLD),
        Text("2. Rewrite joint probability", font_size=25, color=cfg.GOLD, weight=BOLD),
        Text("3. Substitute the joint term", font_size=25, color=cfg.GREEN, weight=BOLD),
    )
    label_left = -6.35
    for label, step in zip(labels, steps):
        label.set_stroke("#02111D", width=4, opacity=0.8, background=True)
        label.move_to([label_left + label.width / 2, step.get_y(), 0])

    paced_play(scene, FadeIn(labels[0]), FadeIn(step1, shift=UP * 0.08), run_time=0.85)
    narration_wait(scene, 0.25)
    paced_play(scene, FadeIn(labels[1]), FadeIn(step2, shift=UP * 0.08), run_time=0.85)
    narration_wait(scene, 0.25)
    paced_play(scene, FadeIn(labels[2]), FadeIn(step3, shift=UP * 0.08), run_time=0.85)
    paced_play(scene, Indicate(step3, color=cfg.WHITE, scale_factor=1.04), run_time=0.65)

    legend = VGroup(
        Text("H = hypothesis, like disease", font_size=23, color=cfg.MUTED),
        Text("E = evidence, like a positive test", font_size=23, color=cfg.MUTED),
    ).arrange(RIGHT, buff=0.55)
    legend.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    legend.to_edge(DOWN, buff=0.35)
    paced_play(scene, FadeIn(legend), run_time=0.8)
    narration_wait(scene, 0.9)

    end_scene(scene, scene_start)
