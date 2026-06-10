from manim import *

from config import DIM_TEXT_COLOR, PRIMARY_GLOW, SECONDARY_GLOW, SUCCESS_COLOR, TEXT_COLOR, WARNING_COLOR
from manim_scenes.common import force_arrow, motion_trail, rolling_ball, set_scene_style, soft_background, surface_line


def play_scene(scene: Scene):
    set_scene_style(scene)
    scene.add(soft_background())

    title = Text("Momentum is built by small repeated actions", font_size=34, color=TEXT_COLOR).to_edge(UP, buff=0.6)
    surface = surface_line(width=9.0, y=-1.35)
    path = DashedLine(surface.get_left(), surface.get_right(), color="#384052", dash_length=0.18)
    ball = rolling_ball(radius=0.24, color=PRIMARY_GLOW).move_to(surface.get_left() + RIGHT * 0.7 + UP * 0.27)

    scene.play(Write(title), Create(surface), FadeIn(path), FadeIn(ball), run_time=2.0)

    calendar_dots = VGroup()
    for i in range(14):
        dot = Dot(radius=0.055, color=DIM_TEXT_COLOR).set_opacity(0.35)
        dot.move_to(LEFT * 4.2 + RIGHT * i * 0.32 + UP * 2.35)
        calendar_dots.add(dot)
    scene.play(FadeIn(calendar_dots), run_time=0.8)

    trail_points = [ball.get_center()]
    for i in range(8):
        pulse = force_arrow(ball.get_right(), ball.get_right() + RIGHT * (0.55 + i * 0.08), color=SUCCESS_COLOR, label=None).scale(0.75)
        scene.play(FadeIn(pulse), calendar_dots[i].animate.set_color(SUCCESS_COLOR).set_opacity(0.95), run_time=0.25)
        shift = RIGHT * (0.28 + i * 0.08)
        trail_points.append(ball.get_center() + shift)
        scene.play(ball.animate.shift(shift), FadeOut(pulse), run_time=0.45)

    trail = motion_trail(trail_points, color=PRIMARY_GLOW, max_width=7)
    scene.play(FadeIn(trail), run_time=0.8)

    friction = VGroup()
    for offset in [0.0, 0.55, 1.1]:
        friction.add(force_arrow(ball.get_left() + LEFT * offset, ball.get_left() + LEFT * (offset + 0.5), color=WARNING_COLOR))
    friction.scale(0.7)
    scene.play(FadeIn(friction), run_time=0.8)
    scene.play(friction.animate.set_opacity(0.32).scale(0.78), run_time=1.0)

    equation = MathTex(
        r"\text{Action}",
        "=",
        r"\text{Motivation}",
        "-",
        r"\text{Friction}",
        "+",
        r"\text{Momentum}",
        color=TEXT_COLOR,
    ).scale(0.72)
    equation.move_to(DOWN * 2.85)
    equation[2].set_color(PRIMARY_GLOW)
    equation[4].set_color(WARNING_COLOR)
    equation[6].set_color(SUCCESS_COLOR)
    scene.play(Write(equation), run_time=1.8)

    p_eq = MathTex("p", "=", "m", "v", color=TEXT_COLOR).scale(0.95).next_to(equation, UP, buff=0.38)
    p_eq[0].set_color(SUCCESS_COLOR)
    p_eq[2].set_color(SECONDARY_GLOW)
    p_eq[3].set_color(PRIMARY_GLOW)
    scene.play(Write(p_eq), run_time=1.2)

    metaphor = VGroup(
        Text("mass = consistency", font_size=20, color=SECONDARY_GLOW),
        Text("velocity = repeated action", font_size=20, color=PRIMARY_GLOW),
        Text("momentum = habit strength", font_size=20, color=SUCCESS_COLOR),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
    metaphor.to_edge(RIGHT, buff=0.85).shift(UP * 2.05)
    scene.play(FadeIn(metaphor, shift=LEFT * 0.2), run_time=1.3)

    final_dots = VGroup(*[calendar_dots[i] for i in range(8, 12)])
    scene.play(ball.animate.shift(RIGHT * 1.2), final_dots.animate.set_color(SUCCESS_COLOR).set_opacity(0.95), run_time=1.5)
    scene.wait(4.0)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)


class Scene06Momentum(Scene):
    def construct(self):
        play_scene(self)
