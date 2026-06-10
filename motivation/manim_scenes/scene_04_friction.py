from manim import *

from config import DIM_TEXT_COLOR, PRIMARY_GLOW, SECONDARY_GLOW, TEXT_COLOR, WARNING_COLOR
from manim_scenes.common import (
    force_arrow,
    friction_arrow,
    rolling_ball,
    set_scene_style,
    soft_background,
    surface_line,
)


def play_scene(scene: Scene):
    set_scene_style(scene)
    scene.add(soft_background())

    title = Text("Friction is invisible until motion slows", font_size=34, color=TEXT_COLOR).to_edge(UP, buff=0.6)
    surface = surface_line(width=8.4, y=-1.8, rough=False)
    rough_surface = surface_line(width=8.4, y=-1.8, rough=True)
    ball = rolling_ball(radius=0.26, color=PRIMARY_GLOW).move_to(surface.get_left() + RIGHT * 0.7 + UP * 0.29)

    scene.play(Write(title), Create(surface), FadeIn(ball), run_time=2.0)
    push = force_arrow(ball.get_right(), ball.get_right() + RIGHT * 1.35, color=PRIMARY_GLOW, label="motivation")
    scene.play(FadeIn(push), run_time=0.8)
    scene.play(ball.animate.shift(RIGHT * 2.1), FadeOut(push), run_time=1.7)

    scene.play(Transform(surface, rough_surface), run_time=1.2)
    label_positions = [
        ("phone", -3.55, -0.95),
        ("fatigue", -2.35, -0.25),
        ("noise", -1.1, -0.95),
        ("fear", 0.2, -0.25),
        ("unclear goal", 1.65, -0.95),
        ("bad environment", 3.3, 0.45),
    ]
    arrows = VGroup()
    for label, x, y in label_positions:
        arrow = friction_arrow(
            [x + 0.45, y, 0],
            [x - 0.45, y, 0],
            label=label,
            label_font_size=24,
        )
        arrow[-1].shift(UP * 0.08)
        arrows.add(arrow)
    scene.play(LaggedStart(*[FadeIn(a, shift=LEFT * 0.08) for a in arrows], lag_ratio=0.12), run_time=2.4)
    scene.play(ball.animate.shift(RIGHT * 0.65), run_time=1.4)
    scene.play(ball.animate.shift(RIGHT * 0.22), run_time=1.4)

    equation = MathTex(r"\text{Action}", "=", r"\text{Motivation}", "-", r"\text{Friction}", color=TEXT_COLOR)
    equation.scale(0.92).move_to(UP * 2.45)
    equation[2].set_color(PRIMARY_GLOW)
    equation[4].set_color(WARNING_COLOR)
    scene.play(Write(equation), run_time=1.8)

    vector_line = NumberLine(x_range=[-3, 3, 1], length=4.5, color=DIM_TEXT_COLOR).next_to(equation, DOWN, buff=0.45)
    forward = force_arrow(vector_line.n2p(0), vector_line.n2p(2.4), color=PRIMARY_GLOW)
    backward = friction_arrow(vector_line.n2p(2.4), vector_line.n2p(0.45))
    result = force_arrow(vector_line.n2p(0), vector_line.n2p(0.45), color=SECONDARY_GLOW, label="result")
    scene.play(Create(vector_line), FadeIn(forward), FadeIn(backward), run_time=1.5)
    scene.play(FadeIn(result), run_time=0.8)

    warning = Text("When motivation decays, friction dominates.", font_size=25, color=DIM_TEXT_COLOR)
    warning.next_to(vector_line, DOWN, buff=0.35)
    scene.play(FadeIn(warning), run_time=1.2)
    scene.wait(4.0)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)


class Scene04Friction(Scene):
    def construct(self):
        play_scene(self)
