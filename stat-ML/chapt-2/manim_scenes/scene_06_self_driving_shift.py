from manim import *

import config as cfg
from manim_scenes.common import arrow_between, cinematic_background, info_card, narration_wait, paced_play, road_scene, scene_title, scene_transition, simple_model


def _thumbnail_grid(labels: list[str], weather: list[str], x: float, title: str, color: str) -> VGroup:
    heading = Text(title, font_size=29, color=color, weight=BOLD).move_to([x, 2.32, 0])
    group = VGroup(heading)
    for index, item in enumerate(weather):
        thumb = road_scene(item, color).scale(0.68)
        row = index // 2
        col = index % 2
        thumb.move_to([x + (col - 0.5) * 1.92, 1.3 - row * 1.28, 0])
        label = Text(labels[index], font_size=16, color=cfg.TEXT).next_to(thumb, DOWN, buff=0.04)
        group.add(VGroup(thumb, label))
    return group


def _confidence_bar(value: float) -> VGroup:
    frame = RoundedRectangle(corner_radius=0.08, width=2.2, height=0.28, stroke_color=cfg.MUTED, fill_opacity=0)
    fill = Rectangle(width=2.2 * value, height=0.2, fill_color=cfg.GREEN if value > 0.55 else cfg.WARNING, fill_opacity=0.9, stroke_width=0)
    fill.align_to(frame, LEFT)
    fill.move_to(frame.get_left() + RIGHT * fill.width / 2)
    text = Text("confidence", font_size=16, color=cfg.MUTED).next_to(frame, UP, buff=0.1)
    return VGroup(text, frame, fill)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = scene_title("Self-driving car").to_edge(UP, buff=0.16)
    training = _thumbnail_grid(["sunlight", "clear sky", "dry road", "daytime"], ["sun", "sun", "sun", "sun"], -3.95, "Training World", cfg.GREEN)
    deployment = _thumbnail_grid(["rain", "fog", "night", "snow", "glare"], ["rain", "fog", "night", "snow", "glare"], 3.95, "Deployment World", cfg.WARNING)
    model = simple_model("Learner").scale(0.9).move_to([0, -1.18, 0])
    train_arrow = arrow_between(training.get_right() + RIGHT * 0.1, model.get_left(), cfg.GREEN)
    deploy_arrow = arrow_between(model.get_right(), deployment.get_left() + LEFT * 0.1, cfg.WARNING)
    bar_high = _confidence_bar(0.86).scale(0.92).move_to([0, -2.45, 0])
    bar_low = _confidence_bar(0.28).scale(0.92).move_to([0, -2.45, 0])
    equation = MathTex(r"\mathrm{Training\ World}\neq\mathrm{Deployment\ World}", font_size=32, color=cfg.TEXT).to_edge(DOWN, buff=0.1)
    training_card = info_card("Model practiced", ["clear lane marks", "dry road texture", "daylight pixels"], 3.1, cfg.GREEN, 21, 16).move_to([-4.25, -2.65, 0])
    deployment_card = info_card("Reality adds", ["low visibility", "glare", "snow and fog"], 3.05, cfg.WARNING, 21, 16).move_to([4.85, -2.72, 0])
    eval_warning = info_card("Test accuracy can mislead", ["test data can look too familiar"], 3.45, cfg.YELLOW, 19, 15).move_to([0, 2.18, 0])

    paced_play(scene, FadeIn(title), FadeIn(training, lag_ratio=0.05), run_time=1.0)
    paced_play(scene, FadeIn(model), FadeIn(train_arrow), FadeIn(bar_high), FadeIn(training_card, shift=UP * 0.1), run_time=0.85)
    paced_play(scene, FadeIn(deployment, lag_ratio=0.05), FadeIn(deploy_arrow), run_time=1.0)
    paced_play(scene, FadeIn(deployment_card, shift=UP * 0.1), ReplacementTransform(bar_high, bar_low), Write(equation), run_time=0.85)
    paced_play(scene, FadeIn(eval_warning, shift=DOWN * 0.12), run_time=0.55)
    narration_wait(scene, 0.9)
    scene_transition(scene)


class Scene06SelfDrivingShift(Scene):
    def construct(self) -> None:
        play_scene(self)
