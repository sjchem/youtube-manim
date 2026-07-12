"""Scene 08 - supervised ML as estimating P(y | x)."""

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
    scene_title,
    tiny_model,
)


class Scene08MLConnections(Scene):
    """Connect probability basics to the supervised prediction formula."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "08")
    scene.add(cinematic_background())

    title = scene_title("Machine learning often estimates P(y | x)").to_edge(UP, buff=0.34)
    paced_play(scene, FadeIn(title), run_time=0.8)

    x_card = label_pill("x = features", cfg.CYAN, font_size=24).move_to(LEFT * 4.3 + UP * 0.95)
    model = tiny_model("ML model").scale(1.05).move_to(LEFT * 0.9 + UP * 0.95)
    y_card = equation_box(r"P(y \mid x)", cfg.GOLD, font_size=52).move_to(RIGHT * 3.2 + UP * 0.95)
    arrow1 = Arrow(x_card.get_right(), model.get_left(), color=cfg.MUTED, buff=0.18, stroke_width=3.5)
    arrow2 = Arrow(model.get_right(), y_card.get_left(), color=cfg.MUTED, buff=0.18, stroke_width=3.5)

    explanation = VGroup(
        Text("x: evidence the model observes", font_size=21, color=cfg.CYAN, weight=BOLD),
        Text("y: prediction the model returns", font_size=21, color=cfg.GOLD, weight=BOLD),
    ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    explanation.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    explanation.move_to(LEFT * 0.9 + DOWN * 0.45)

    paced_play(scene, FadeIn(x_card), Create(arrow1), FadeIn(model), run_time=0.95)
    paced_play(scene, Create(arrow2), FadeIn(y_card, shift=LEFT * 0.12), FadeIn(explanation), run_time=0.95)
    narration_wait(scene, 0.5)

    examples = VGroup(
        label_pill("P(Spam | Email)", cfg.RED, font_size=21),
        label_pill("P(Cat | Pixels)", cfg.CYAN, font_size=21),
        label_pill("P(Fraud | Transaction)", cfg.ORANGE, font_size=20),
        label_pill("P(Disease | Symptoms)", cfg.GREEN, font_size=20),
    ).arrange_in_grid(rows=2, cols=2, buff=(0.34, 0.52))
    examples.move_to(DOWN * 1.75)
    conclusion = Text("Supervised ML turns evidence into conditional probabilities.", font_size=22, color=cfg.WHITE, weight=BOLD)
    conclusion.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    conclusion.to_edge(DOWN, buff=0.25)

    paced_play(scene, LaggedStart(*[FadeIn(example, scale=0.85) for example in examples], lag_ratio=0.14), run_time=1.2)
    paced_play(scene, FadeIn(conclusion, shift=UP * 0.12), run_time=0.9)
    narration_wait(scene, 1.0)

    end_scene(scene, scene_start)
