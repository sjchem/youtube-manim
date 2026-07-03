from manim import *

import config as cfg
from manim_scenes.common import (
    PALETTE,
    cinematic_background,
    dataset_table,
    dot_cloud,
    equation_box,
    info_card,
    labeled_box,
    narration_wait,
    paced_play,
    sample_frame,
    scene_title,
    scene_transition,
)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("The world is bigger", "than the dataset").to_edge(UP)

    clusters = [(-4.7, 1.6, 0), (-1.7, 0.7, 0), (2.2, 1.35, 0), (4.9, -0.8, 0), (-3.8, -1.8, 0), (0.7, -1.55, 0)]
    world = dot_cloud(520, width=13.7, height=7.0, colors=PALETTE, seed=21, radius=0.026, clusters=clusters)
    domain_labels = VGroup(
        Text("customers", font_size=22, color=cfg.GREEN, weight=BOLD).move_to([-5.55, 2.6, 0]),
        Text("patients", font_size=22, color=cfg.RED, weight=BOLD).move_to([-1.85, 1.82, 0]),
        Text("roads", font_size=22, color=cfg.YELLOW, weight=BOLD).move_to([2.15, 2.48, 0]),
        Text("sensors", font_size=22, color=cfg.BLUE, weight=BOLD).move_to([5.25, -1.2, 0]),
        Text("factories", font_size=22, color=cfg.ORANGE, weight=BOLD).move_to([-4.25, -2.35, 0]),
    )
    frame = sample_frame(2.05, 1.25, cfg.YELLOW).move_to([-2.0, 0.65, 0])
    selected = dot_cloud(34, width=1.65, height=0.9, center=frame.get_center(), colors=PALETTE[:4], seed=14, radius=0.034)
    dataset = labeled_box("Training\nDataset", width=2.35, height=1.3, color=cfg.BLUE).to_corner(DR, buff=0.65).shift(UP * 0.55)
    table = dataset_table(4, 6, colors=PALETTE[:4]).scale(0.78).move_to(dataset.get_center() + DOWN * 0.1)
    evidence_card = info_card("Data is evidence", ["measured", "stored", "labeled", "cleaned"], 2.25, cfg.GREEN, 18, 14).to_corner(UL, buff=0.72).shift(DOWN * 1.0)
    missing_card = info_card("What may be missing?", ["rare cases", "future behavior", "sensor failures"], 2.55, cfg.WARNING, 18, 14).next_to(dataset, UP, buff=0.55).shift(UP * 0.25)
    equation = equation_box(r"\mathrm{Dataset}\ll\mathrm{Real\ World}", cfg.YELLOW, 42).to_edge(DOWN)
    chapter = Text("Population vs Sample: The Foundation of ML Data", font_size=30, color=cfg.YELLOW, weight=BOLD).to_edge(DOWN, buff=0.5)

    paced_play(scene, FadeIn(title), FadeIn(world, lag_ratio=0.004), FadeIn(domain_labels, lag_ratio=0.05), run_time=1.25)
    paced_play(scene, world.animate.shift(LEFT * 0.2 + UP * 0.05), Create(frame), run_time=1.1)
    paced_play(scene, FadeIn(evidence_card, shift=RIGHT * 0.15), run_time=0.55)
    paced_play(scene, FadeIn(selected), run_time=0.45)
    paced_play(scene, TransformFromCopy(selected, table), FadeIn(dataset[0]), FadeIn(dataset[1]), run_time=1.15)
    paced_play(scene, FadeIn(missing_card, shift=UP * 0.15), FadeIn(equation, shift=UP * 0.2), run_time=0.75)
    paced_play(scene, ReplacementTransform(equation, chapter), run_time=0.7)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene01WorldDataset(Scene):
    def construct(self) -> None:
        play_scene(self)
