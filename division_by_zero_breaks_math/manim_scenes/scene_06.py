from manim import *

from manim_scenes.common import *


def construct_scene_06(scene: MovingCameraScene) -> None:
    add_oceanic_background(scene)

    eq = math_eq("0 \\div 0 = ?", font_size=76).shift(UP * 2.45)
    reverse = math_eq("? \\times 0 = 0", font_size=64, color=WARNING_ORANGE).next_to(eq, DOWN, buff=0.35)
    scene.play(Write(eq), run_time=0.8)
    scene.play(TransformMatchingTex(eq.copy(), reverse), run_time=0.85)

    values = ["1", "5", "-10", "\\pi"]
    roads = VGroup()
    zero = glow(math_eq("0", font_size=70).shift(DOWN * 1.15), CYAN)
    for i, value in enumerate(values):
        start = LEFT * 4.0 + UP * (1.15 - i * 0.75)
        token = math_eq(value, font_size=42, color=MAIN_WHITE).move_to(start)
        path = CubicBezier(start, start + RIGHT * 1.6, zero.get_center() + LEFT * 1.4, zero.get_center())
        path.set_color(CYAN).set_stroke(opacity=0.34, width=3)
        roads.add(VGroup(token, path))
    scene.play(FadeIn(zero), *[FadeIn(r[0]) for r in roads], run_time=0.7)
    for road in roads:
        scene.play(Create(road[1]), road[0].animate.move_to(zero.get_center()).set_opacity(0.18), run_time=0.42)

    comparison = VGroup(
        math_eq("6 \\div 0", font_size=44, color=ERROR_RED),
        short_label("No answer", color=ERROR_RED, font_size=30),
        math_eq("0 \\div 0", font_size=44, color=WARNING_ORANGE),
        short_label("Too many answers", color=WARNING_ORANGE, font_size=30),
    ).arrange(DOWN, buff=0.16).to_edge(RIGHT, buff=0.8)
    indeterminate = glowing_text("Indeterminate", font_size=42, color=WARNING_ORANGE).to_edge(DOWN, buff=0.45)
    scene.play(FadeIn(comparison), FadeIn(indeterminate), run_time=0.9)

    limit_examples = VGroup(
        math_eq("\\frac{x}{x} \\to 1", font_size=42, color=VALID_GREEN),
        math_eq("\\frac{x^2}{x} \\to 0", font_size=42, color=VALID_GREEN),
        math_eq("\\frac{\\sin x}{x} \\to 1", font_size=42, color=VALID_GREEN),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=0.75).shift(DOWN * 1.15)
    scene.play(FadeIn(limit_examples, lag_ratio=0.15), run_time=1.0)
    scene.wait(1.4)
    clear_scene(scene)


class Scene06ZeroOverZero(MovingCameraScene):
    def construct(self) -> None:
        construct_scene_06(self)
