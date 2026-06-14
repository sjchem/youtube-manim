from manim import *

from manim_scenes.common import *


def construct_scene_03(scene: MovingCameraScene) -> None:
    add_oceanic_background(scene)

    values = ["-5", "-2", "0", "1", "3", "7", "\\pi"]
    tokens = number_tokens(values).shift(UP * 1.1)
    line = NumberLine(x_range=(-6, 8, 1), length=10.5, color=CYAN_BRIGHT).shift(UP * 0.15)
    labels = VGroup(
        short_label("Many inputs", font_size=34).next_to(tokens, UP, buff=0.4),
        math_eq("\\times 0", font_size=62, color=WARNING_ORANGE).shift(DOWN * 1.15),
    )

    scene.play(Create(line), FadeIn(tokens, lag_ratio=0.12), FadeIn(labels[0]), run_time=1.2)
    scene.play(Write(labels[1]), run_time=0.7)

    funnel = VGroup(
        Line(LEFT * 4 + DOWN * 0.15, ORIGIN + DOWN * 2.15, color=CYAN, stroke_opacity=0.35),
        Line(RIGHT * 4 + DOWN * 0.15, ORIGIN + DOWN * 2.15, color=CYAN, stroke_opacity=0.35),
    )
    scene.play(Create(funnel), run_time=0.55)
    collapse_to_zero(scene, tokens, zero_point=DOWN * 2.15, run_time=1.7)

    one_output = short_label("One output", color=VALID_GREEN, font_size=34).next_to(DOWN * 2.15, DOWN, buff=0.55)
    info = short_label("Information collapse", color=WARNING_ORANGE, font_size=36).to_edge(DOWN, buff=0.45)
    scene.play(FadeIn(one_output), FadeIn(info), run_time=0.8)
    scene.wait(1.3)
    clear_scene(scene)


class Scene03ZeroCollapse(MovingCameraScene):
    def construct(self) -> None:
        construct_scene_03(self)
