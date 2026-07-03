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
    simple_model,
    scene_title,
    scene_transition,
)


def _jar() -> VGroup:
    body = RoundedRectangle(corner_radius=0.24, width=4.25, height=5.15, stroke_color=cfg.BLUE, stroke_width=3, fill_color=cfg.COLORS["panel"], fill_opacity=0.18)
    lip = Ellipse(width=3.55, height=0.46, stroke_color=cfg.BLUE, stroke_width=3).move_to(body.get_top() + DOWN * 0.08)
    balls = dot_cloud(330, width=3.65, height=4.2, center=DOWN * 0.25, colors=PALETTE[:5], seed=32, radius=0.035)
    return VGroup(body, lip, balls)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("Sample", "a small window into reality").to_edge(UP)
    jar = _jar().scale(0.82).shift(LEFT * 3.35 + DOWN * 0.35)
    scoop = Arc(radius=0.5, start_angle=PI, angle=PI, color=cfg.YELLOW, stroke_width=5).move_to([-1.55, 0.2, 0]).rotate(-0.25)
    sample_balls = dot_cloud(24, width=1.05, height=0.48, center=scoop.get_center() + UP * 0.05, colors=PALETTE[:5], seed=7, radius=0.045)
    table = dataset_table(4, 6, colors=PALETTE[:5]).scale(1.02).move_to([1.35, 0.85, 0])
    table_label = Text("dataset grid", font_size=20, color=cfg.MUTED).next_to(table, DOWN, buff=0.12)
    equation = equation_box(r"\mathrm{Sample}\subset\mathrm{Population}", cfg.YELLOW, 42).to_edge(DOWN)
    risk_card = info_card("Sampling risk", ["miss rare groups", "over-sample easy cases", "hide future conditions"], 2.8, cfg.WARNING, 18, 14).move_to([3.95, 1.75, 0])
    jump_card = info_card("Generalization jump", ["sample patterns", "population predictions"], 2.75, cfg.GREEN, 18, 14).move_to([4.0, -0.15, 0])

    sample = labeled_box("Sample", 1.55, 0.8, cfg.GREEN).move_to([-0.75, -2.32, 0])
    model = simple_model().move_to([1.15, -2.32, 0])
    pred = labeled_box("Prediction", 1.9, 0.8, cfg.YELLOW).move_to([3.3, -2.32, 0])
    sample_to_model = Arrow(sample[0].get_right(), model[0].get_left(), buff=0.12, stroke_width=cfg.VISUAL["arrow_stroke"], color=cfg.GREEN, max_tip_length_to_length_ratio=0.18)
    model_to_pred = Arrow(model[0].get_right(), pred[0].get_left(), buff=0.12, stroke_width=cfg.VISUAL["arrow_stroke"], color=cfg.YELLOW, max_tip_length_to_length_ratio=0.18)
    pipeline = VGroup(sample, sample_to_model, model, model_to_pred, pred)

    paced_play(scene, FadeIn(title), FadeIn(jar), run_time=0.9)
    paced_play(scene, Create(scoop), TransformFromCopy(jar[2][:24], sample_balls), run_time=0.9)
    paced_play(scene, TransformFromCopy(sample_balls, table), FadeIn(table_label), FadeIn(risk_card, shift=LEFT * 0.15), run_time=1.0)
    paced_play(scene, FadeIn(equation), run_time=0.65)
    paced_play(scene, FadeOut(equation, shift=DOWN * 0.15), run_time=0.35)
    paced_play(scene, FadeIn(pipeline, lag_ratio=0.18), FadeIn(jump_card, shift=UP * 0.1), run_time=1.1)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene03Sample(Scene):
    def construct(self) -> None:
        play_scene(self)
