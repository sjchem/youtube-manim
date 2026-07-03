from manim import *

import config as cfg
from manim_scenes.common import (
    PALETTE,
    arrow_between,
    cinematic_background,
    dataset_table,
    dot_cloud,
    info_card,
    labeled_box,
    narration_wait,
    paced_play,
    sample_frame,
    scene_title,
    scene_transition,
    simple_model,
)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("Does the sample represent reality?").to_edge(UP, buff=0.14)
    ocean = dot_cloud(560, width=14.2, height=5.45, center=DOWN * 0.35, colors=PALETTE, seed=110, radius=0.019, opacity=0.58)
    bucket = sample_frame(1.25, 0.9, cfg.YELLOW).move_to([-3.15, -0.15, 0])
    sample = dataset_table(4, 6, colors=[cfg.BLUE, cfg.BLUE, cfg.GREEN, cfg.YELLOW]).scale(0.78).move_to([-2.35, -2.08, 0])
    sample_label = labeled_box("Dataset", 1.55, 0.66, cfg.YELLOW, 18).next_to(sample, DOWN, buff=0.12)
    model = simple_model("Model").scale(0.88).move_to([0.35, -2.08, 0])
    prediction = Ellipse(width=2.9, height=1.45, stroke_color=cfg.WARNING, stroke_width=4, fill_color=cfg.WARNING, fill_opacity=0.08).move_to([3.15, 0.08, 0])
    reliable_prediction = Ellipse(width=4.7, height=2.0, stroke_color=cfg.GREEN, stroke_width=4, fill_color=cfg.GREEN, fill_opacity=0.08).move_to([2.85, 0.1, 0])
    first_question = Text("How much data do we have?", font_size=32, color=cfg.TEXT, weight=BOLD).move_to([0, 2.38, 0])
    second_question = Text("Does our data represent the world?", font_size=31, color=cfg.YELLOW, weight=BOLD).move_to([0, 2.38, 0])
    final_eq = MathTex(r"\mathrm{Model\ Generalization}\leq\mathrm{Quality\ of\ the\ Training\ Sample}", font_size=27, color=cfg.TEXT).to_edge(DOWN, buff=0.2)
    question_stack = VGroup(
        info_card("Ask about the bucket", ["Who is included?", "Who is missing?", "Will tomorrow match?"], 3.05, cfg.BLUE, 21, 15),
        info_card("Better sample", ["more diverse", "more representative", "less brittle"], 3.05, cfg.GREEN, 21, 15),
    ).arrange(DOWN, buff=0.24).move_to([-5.45, 0.2, 0])
    next_tools = info_card("Next statistical tools", ["mean / median", "variance", "standard deviation"], 3.15, cfg.PURPLE, 20, 15).move_to([5.15, 1.38, 0])

    diverse_sample = dataset_table(4, 6, colors=PALETTE[:6]).scale(0.78).move_to(sample)

    paced_play(scene, FadeIn(title), FadeIn(ocean, lag_ratio=0.002), run_time=1.1)
    paced_play(scene, Create(bucket), FadeIn(first_question), run_time=0.75)
    paced_play(scene, TransformFromCopy(ocean[:24], sample), FadeIn(sample_label), run_time=1.0)
    flow = VGroup(arrow_between(sample, model, cfg.YELLOW), arrow_between(model, prediction, cfg.WARNING))
    paced_play(scene, FadeIn(model), FadeIn(flow), Create(prediction), FadeIn(question_stack[0], shift=RIGHT * 0.12), run_time=1.05)
    paced_play(scene, ReplacementTransform(first_question, second_question), run_time=0.8)
    paced_play(scene, FadeIn(question_stack[1], shift=RIGHT * 0.12), ReplacementTransform(sample, diverse_sample), ReplacementTransform(prediction, reliable_prediction), Write(final_eq), run_time=1.2)
    paced_play(scene, FadeIn(next_tools, shift=LEFT * 0.12), run_time=0.65)
    narration_wait(scene, 1.1)
    scene_transition(scene)


class Scene10FinalQuestion(Scene):
    def construct(self) -> None:
        play_scene(self)
