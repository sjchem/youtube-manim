from manim import *

from manim_scenes.common import *


def construct_scene_02(scene: MovingCameraScene) -> None:
    add_oceanic_background(scene)

    eq = math_eq("12 \\div 3 = 4", font_size=68).to_edge(UP, buff=0.55)
    dots = dot_grid(12, cols=6).shift(LEFT * 3.1 + DOWN * 0.25)
    boxes = grouping_boxes(3).shift(RIGHT * 2.4 + DOWN * 0.25)
    scene.play(Write(eq), FadeIn(dots), run_time=1.0)
    scene.play(Create(boxes), run_time=0.7)

    targets = arrange_dots_into_boxes(dots, boxes, per_box=4)
    scene.play(*[dot.animate.move_to(targets[i]) for i, dot in enumerate(dots)], run_time=1.4)
    counts = VGroup(*[math_eq("4", font_size=44, color=VALID_GREEN).next_to(box, DOWN, buff=0.18) for box in boxes])
    scene.play(FadeIn(counts), run_time=0.5)

    reverse = math_eq("4 \\times 3 = 12", font_size=66, color=VALID_GREEN).to_edge(DOWN, buff=0.65)
    prompt = short_label("What number times 3 gives 12?", font_size=32).next_to(reverse, UP, buff=0.35)
    scene.play(TransformMatchingTex(eq.copy(), reverse), FadeIn(prompt), run_time=1.0)
    scene.wait(0.8)

    bad = math_eq("12 \\div 0 = ?", font_size=70).move_to(UP * 1.35)
    reverse_bad = math_eq("? \\times 0 = 12", font_size=64, color=WARNING_ORANGE).next_to(bad, DOWN, buff=0.45)
    scene.play(
        FadeOut(dots),
        FadeOut(boxes),
        FadeOut(counts),
        FadeOut(reverse),
        FadeOut(prompt),
        Transform(eq, bad),
        run_time=0.9,
    )
    scene.play(Write(reverse_bad), run_time=0.8)

    test_dots = dot_grid(12, color=WARNING_ORANGE, cols=6).shift(DOWN * 1.25)
    zero = glow(math_eq("0", font_size=68).move_to(test_dots), CYAN)
    scene.play(FadeIn(test_dots), run_time=0.55)
    scene.play(test_dots.animate.scale(0.05).move_to(zero.get_center()).set_opacity(0), FadeIn(zero), run_time=1.2)
    scene.play(Flash(zero, color=ERROR_RED, flash_radius=1.1), run_time=0.45)
    scene.wait(1.0)
    clear_scene(scene)


class Scene02ReverseMultiplication(MovingCameraScene):
    def construct(self) -> None:
        construct_scene_02(self)
