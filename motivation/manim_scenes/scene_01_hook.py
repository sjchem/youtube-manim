from manim import *

from config import DIM_TEXT_COLOR, PRIMARY_GLOW, SECONDARY_GLOW, TEXT_COLOR
from manim_scenes.common import (
    cinematic_title_card,
    force_arrow,
    rolling_ball,
    set_scene_style,
    simple_clock,
    soft_background,
    spark,
    surface_line,
)


def play_scene(scene: Scene):
    set_scene_style(scene)
    bg = soft_background()
    scene.add(bg)

    night_label = Text("Tomorrow I change everything.", font_size=30, color=TEXT_COLOR)
    night_label.to_edge(UP, buff=0.75)

    motivation = spark(radius=0.16, color=PRIMARY_GLOW).move_to(LEFT * 3.2 + UP * 0.85)
    clock = simple_clock(radius=0.58).move_to(RIGHT * 3.25 + UP * 0.85)

    track = surface_line(width=6.6, y=-2.15)
    ball = rolling_ball(radius=0.26, color=PRIMARY_GLOW).move_to(track.get_left() + UP * 0.28)

    scene.play(FadeIn(motivation, scale=0.6), Write(night_label), Create(clock), run_time=2.4)
    scene.play(motivation.animate.scale(1.45), Rotate(clock[1], angle=-PI / 3), Rotate(clock[2], angle=TAU * 1.8), run_time=2.5)
    scene.play(Create(track), FadeIn(ball, shift=UP * 0.2), run_time=1.4)
    scene.wait(2.0)

    morning = Text("Morning", font_size=26, color=DIM_TEXT_COLOR).move_to(clock.get_center() + DOWN * 0.95)
    weak_spark = motivation.copy().scale(0.45).set_opacity(0.45)
    scene.play(
        Transform(motivation, weak_spark),
        FadeOut(night_label, shift=UP * 0.15),
        FadeIn(morning),
        Rotate(clock[2], angle=TAU * 2.2),
        run_time=2.6,
    )

    push = force_arrow(ball.get_right() + LEFT * 0.05, ball.get_right() + RIGHT * 1.0, PRIMARY_GLOW, "motivation")
    scene.play(FadeIn(push, shift=RIGHT * 0.1), run_time=1.0)
    scene.play(ball.animate.shift(RIGHT * 0.25), run_time=1.0)
    scene.play(ball.animate.shift(LEFT * 0.25), FadeOut(push), run_time=1.2)

    question = Text("Motivation feels powerful.", font_size=32, color=TEXT_COLOR)
    question2 = Text("But why does it fade?", font_size=32, color=SECONDARY_GLOW)
    VGroup(question, question2).arrange(DOWN, buff=0.22).move_to(ORIGIN + DOWN * 0.1)
    scene.play(FadeIn(question, shift=UP * 0.2), run_time=1.4)
    scene.wait(1.0)
    scene.play(FadeIn(question2, shift=UP * 0.2), run_time=1.4)
    scene.wait(1.5)

    title = cinematic_title_card("Why Motivation Fades", "The Physics Behind Discipline")
    scene.play(
        FadeOut(VGroup(motivation, clock, morning, track, ball, question, question2)),
        FadeIn(title, scale=0.95),
        run_time=2.2,
    )
    scene.wait(4.0)
    scene.play(FadeOut(title), run_time=1.0)


class Scene01Hook(Scene):
    def construct(self):
        play_scene(self)

