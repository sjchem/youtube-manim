from manim import *

from config import DIM_TEXT_COLOR, PRIMARY_GLOW, SECONDARY_GLOW, SUCCESS_COLOR, TEXT_COLOR, WARNING_COLOR
from manim_scenes.common import (
    curved_loop_arrow,
    force_arrow,
    graph_axes,
    glowing_curve,
    rolling_ball,
    set_scene_style,
    soft_background,
    subtle_end_card,
    surface_line,
)
from utils.math_utils import motivation_decay


def play_scene(scene: Scene):
    set_scene_style(scene)
    scene.add(soft_background())

    title = Text("Discipline is physics-inspired system design", font_size=34, color=TEXT_COLOR)
    title.to_edge(UP, buff=0.6)
    scene.play(Write(title), run_time=1.4)

    axes = graph_axes(x_range=(0, 5, 1), y_range=(0, 1.1, 0.5), width=3.2, height=1.8)
    axes.move_to(LEFT * 4.75 + UP * 1.35)
    decay_curve = glowing_curve(axes.plot(lambda x: motivation_decay(x, 1.0, 0.65), x_range=[0, 5]), PRIMARY_GLOW)
    decay_label = Text("decay", font_size=18, color=DIM_TEXT_COLOR).next_to(axes, DOWN, buff=0.12)

    inert_surface = surface_line(width=2.6, y=0).move_to(LEFT * 1.65 + UP * 1.35)
    inert_ball = rolling_ball(radius=0.16, color=PRIMARY_GLOW).move_to(inert_surface.get_left() + RIGHT * 0.55 + UP * 0.18)
    inert_label = Text("inertia", font_size=18, color=DIM_TEXT_COLOR).next_to(inert_surface, DOWN, buff=0.2)

    friction = VGroup(
        force_arrow(RIGHT * 0.3 + UP * 1.55, LEFT * 0.25 + UP * 1.55, WARNING_COLOR),
        force_arrow(RIGHT * 0.95 + UP * 1.25, RIGHT * 0.35 + UP * 1.25, WARNING_COLOR),
        Text("friction", font_size=18, color=DIM_TEXT_COLOR).move_to(RIGHT * 0.45 + UP * 0.75),
    )

    barrier = VGroup(
        ArcBetweenPoints(RIGHT * 2.25 + UP * 1.05, RIGHT * 3.45 + UP * 1.05, angle=-PI, color=SECONDARY_GLOW),
        Text("barrier", font_size=18, color=DIM_TEXT_COLOR).move_to(RIGHT * 2.85 + UP * 0.75),
    )

    loop = VGroup(
        curved_loop_arrow(RIGHT * 4.45 + UP * 1.5, RIGHT * 5.2 + UP * 0.95, SUCCESS_COLOR),
        curved_loop_arrow(RIGHT * 5.2 + UP * 0.95, RIGHT * 4.45 + UP * 1.5, SUCCESS_COLOR),
        Text("feedback", font_size=18, color=DIM_TEXT_COLOR).move_to(RIGHT * 4.85 + UP * 0.72),
    )

    miniatures = VGroup(axes, decay_curve, decay_label, inert_surface, inert_ball, inert_label, friction, barrier, loop)
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in miniatures], lag_ratio=0.08), run_time=3.0)

    equation = MathTex(
        r"\text{Action}",
        "=",
        r"\text{Motivation}",
        "-",
        r"\text{Friction}",
        "+",
        r"\text{Momentum}",
        color=TEXT_COLOR,
    ).scale(0.82)
    equation.move_to(DOWN * 0.65)
    equation[2].set_color(PRIMARY_GLOW)
    equation[4].set_color(WARNING_COLOR)
    equation[6].set_color(SUCCESS_COLOR)
    scene.play(Write(equation), run_time=1.8)

    discipline = MathTex(
        r"\text{Discipline}",
        "=",
        r"\text{Lower friction}",
        "+",
        r"\text{Repeatable motion}",
        "+",
        r"\text{Feedback}",
        color=TEXT_COLOR,
    ).scale(0.68)
    discipline.move_to(DOWN * 1.55)
    discipline[2].set_color(WARNING_COLOR)
    discipline[4].set_color(PRIMARY_GLOW)
    discipline[6].set_color(SUCCESS_COLOR)
    scene.play(TransformFromCopy(equation, discipline), run_time=2.0)
    scene.wait(1.0)

    scene.play(FadeOut(VGroup(miniatures, equation, discipline, title)), run_time=1.3)

    final_surface = surface_line(width=9.2, y=-1.15)
    final_ball = rolling_ball(radius=0.28, color=SUCCESS_COLOR).move_to(final_surface.get_left() + RIGHT * 0.5 + UP * 0.31)
    glow_path = Line(final_surface.get_left(), final_surface.get_right(), color=SUCCESS_COLOR, stroke_width=9).set_opacity(0.22)
    final_text = VGroup(
        Text("Motivation starts motion.", font_size=34, color=PRIMARY_GLOW),
        Text("Discipline keeps it moving.", font_size=34, color=SUCCESS_COLOR),
    ).arrange(DOWN, buff=0.25).move_to(UP * 1.25)

    scene.play(Create(final_surface), FadeIn(glow_path), FadeIn(final_ball), run_time=1.5)
    scene.play(final_ball.animate.shift(RIGHT * 7.9), run_time=4.2)
    scene.play(FadeIn(final_text, shift=UP * 0.2), run_time=1.6)
    end_card = subtle_end_card().to_edge(DOWN, buff=0.55)
    scene.play(FadeIn(end_card), run_time=1.2)
    scene.wait(4.0)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)


class Scene08FinalSynthesis(Scene):
    def construct(self):
        play_scene(self)

