"""Scene 03 - addition and multiplication rules."""

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
    venn_two_circles,
)


class Scene03RandomVariables(Scene):
    """Use Venn diagrams and a tree to introduce two core probability rules."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "03")
    scene.add(cinematic_background())

    title = scene_title("Two rules describe either/or and together").to_edge(UP, buff=0.34)
    paced_play(scene, FadeIn(title), run_time=0.8)

    venn = venn_two_circles("coffee", "cake", cfg.CYAN, cfg.GOLD, radius=1.25, separation=1.75)
    venn.move_to(LEFT * 3.45 + UP * 0.38)
    overlap = Intersection(venn[0], venn[1], fill_color=cfg.WHITE, fill_opacity=0.45, stroke_width=0)
    at_least_one = Text("at least one", font_size=21, color=cfg.WHITE, weight=BOLD)
    at_least_one.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    at_least_one.next_to(venn, DOWN, buff=0.28)

    addition = equation_box(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)", cfg.CYAN, font_size=31)
    addition.move_to(RIGHT * 2.15 + UP * 1.05)
    add_note = VGroup(
        Text("Union: A or B", font_size=21, color=cfg.CYAN, weight=BOLD),
        Text("Subtract the overlap once.", font_size=20, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    add_note.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    add_note.next_to(addition, DOWN, buff=0.22)

    paced_play(scene, FadeIn(venn), run_time=0.9)
    paced_play(scene, FadeIn(overlap), FadeIn(at_least_one), run_time=0.8)
    paced_play(scene, FadeIn(addition, shift=UP * 0.12), FadeIn(add_note), run_time=1.0)
    narration_wait(scene, 0.8)

    paced_play(scene, FadeOut(venn), FadeOut(overlap), FadeOut(at_least_one), FadeOut(addition), FadeOut(add_note), run_time=0.7)

    start = label_pill("Disease", cfg.RED, font_size=22).move_to(LEFT * 3.75 + UP * 0.9)
    test = label_pill("Positive test", cfg.GOLD, font_size=22).move_to(LEFT * 0.75 + UP * 0.9)
    joint = label_pill("Disease and positive", cfg.GREEN, font_size=20).move_to(RIGHT * 2.85 + UP * 0.9)
    arrow1 = Arrow(start.get_right(), test.get_left(), color=cfg.GOLD, buff=0.14, stroke_width=3.2)
    arrow2 = Arrow(test.get_right(), joint.get_left(), color=cfg.GREEN, buff=0.14, stroke_width=3.2)
    label1 = Text("P(A)", font_size=20, color=cfg.RED, weight=BOLD).next_to(arrow1, UP, buff=0.12)
    label2 = Text("P(B | A)", font_size=20, color=cfg.GOLD, weight=BOLD).next_to(arrow2, UP, buff=0.12)
    tree = VGroup(start, test, joint, arrow1, arrow2, label1, label2)

    multiply = equation_box(r"P(A \cap B) = P(B \mid A)P(A)", cfg.GREEN, font_size=38)
    multiply.move_to(DOWN * 0.95)
    bridge = Text("Together = first event times the next event given the first.", font_size=23, color=cfg.WHITE, weight=BOLD)
    bridge.set_stroke("#02111D", width=4, opacity=0.8, background=True)
    bridge.to_edge(DOWN, buff=0.42)

    paced_play(scene, FadeIn(start), run_time=0.55)
    paced_play(scene, Create(arrow1), FadeIn(test), FadeIn(label1), run_time=0.85)
    paced_play(scene, Create(arrow2), FadeIn(joint), FadeIn(label2), run_time=0.85)
    paced_play(scene, FadeIn(multiply, shift=UP * 0.12), FadeIn(bridge), run_time=1.0)
    narration_wait(scene, 1.0)

    end_scene(scene, scene_start)
