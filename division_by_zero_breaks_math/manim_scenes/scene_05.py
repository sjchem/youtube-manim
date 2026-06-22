from manim import *

from manim_scenes.common import *


def construct_scene_05(scene: MovingCameraScene) -> None:
    add_oceanic_background(scene)

    title = math_eq("y = \\frac{1}{x}", font_size=66).to_edge(UP, buff=0.5)
    axes = graph_axes().shift(DOWN * 0.25)
    left_curve = axes.plot(lambda x: 1 / x, x_range=(-4, -0.14), color=LIMIT_PURPLE, use_smoothing=False)
    right_curve = axes.plot(lambda x: 1 / x, x_range=(0.14, 4), color=LIMIT_PURPLE, use_smoothing=False)
    asymptote = DashedLine(axes.c2p(0, -8), axes.c2p(0, 8), color=WARNING_ORANGE, dash_length=0.12)
    scene.play(Write(title), Create(axes), run_time=1.0)
    scene.play(Create(asymptote), Create(left_curve), Create(right_curve), run_time=1.4)

    dot = Dot(color=CYAN_BRIGHT, radius=0.08).move_to(axes.c2p(1, 1))
    label = MathTex("x=1,\\ y=1", font_size=32, color=MAIN_WHITE).next_to(dot, UR, buff=0.15)
    scene.play(FadeIn(dot), FadeIn(label), run_time=0.5)

    positive_samples = [(0.5, 2), (0.1, 10), (0.01, 100)]
    for x, y in positive_samples:
        display_y = min(y, 7.5)
        next_label = MathTex(f"x={x:g},\\ y={y:g}", font_size=32, color=CYAN_BRIGHT).to_corner(UR, buff=0.55)
        scene.play(dot.animate.move_to(axes.c2p(x, display_y)), Transform(label, next_label), run_time=0.75)
    plus_inf = math_eq("x \\to 0^+\\quad \\frac{1}{x} \\to +\\infty", font_size=48, color=LIMIT_PURPLE).to_edge(RIGHT, buff=0.55).shift(UP * 0.7)
    scene.play(Write(plus_inf), run_time=0.75)

    negative_samples = [(-0.1, -10), (-0.01, -100)]
    for x, y in negative_samples:
        display_y = max(y, -7.5)
        next_label = MathTex(f"x={x:g},\\ y={y:g}", font_size=32, color=CYAN_BRIGHT).to_corner(DR, buff=0.55)
        scene.play(dot.animate.move_to(axes.c2p(x, display_y)), Transform(label, next_label), run_time=0.75)
    minus_inf = math_eq("x \\to 0^-\\quad \\frac{1}{x} \\to -\\infty", font_size=48, color=LIMIT_PURPLE).to_edge(RIGHT, buff=0.55).shift(DOWN * 0.7)
    scene.play(Write(minus_inf), run_time=0.75)

    near = warning_label("Near zero \\neq at zero", font_size=45).to_edge(DOWN, buff=0.45)
    scene.play(FadeIn(near), Flash(asymptote, color=WARNING_ORANGE), run_time=0.85)
    scene.wait(1.4)
    clear_scene(scene)


class Scene05LimitsNotInfinity(MovingCameraScene):
    def construct(self) -> None:
        construct_scene_05(self)
