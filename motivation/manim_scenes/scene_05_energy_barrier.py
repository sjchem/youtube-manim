import numpy as np
from manim import *

from config import DIM_TEXT_COLOR, PRIMARY_GLOW, SECONDARY_GLOW, SUCCESS_COLOR, TEXT_COLOR, WARNING_COLOR
from manim_scenes.common import graph_axes, glowing_curve, rolling_ball, set_scene_style, soft_background
from utils.math_utils import lower_barrier, potential_energy_barrier


def play_scene(scene: Scene):
    set_scene_style(scene)
    scene.add(soft_background())

    title = Text("Procrastination can behave like an energy barrier", font_size=33, color=TEXT_COLOR)
    title.to_edge(UP, buff=0.6)
    axes = graph_axes(x_range=(-3.2, 3.2, 1), y_range=(-0.4, 4.6, 1), width=9.2, height=4.6)
    axes.move_to(DOWN * 0.15)

    def base_y(x):
        return potential_energy_barrier(x, barrier_height=1.15, width=0.7)

    def lowered_y(x):
        return base_y(x) - lower_barrier(x, amount=0.9)

    curve = axes.plot(base_y, x_range=[-3.05, 3.05], color=PRIMARY_GLOW)
    lowered_curve = axes.plot(lowered_y, x_range=[-3.05, 3.05], color=SUCCESS_COLOR)
    curve_group = glowing_curve(curve, PRIMARY_GLOW)

    scene.play(Write(title), Create(axes), run_time=2.0)
    scene.play(Create(curve_group), run_time=2.4)

    labels = VGroup(
        Text("Procrastination", font_size=21, color=DIM_TEXT_COLOR).move_to(axes.c2p(-2.0, 0.65)),
        Text("Starting", font_size=21, color=WARNING_COLOR).move_to(axes.c2p(0.0, 4.35)),
        Text("Flow", font_size=21, color=SUCCESS_COLOR).move_to(axes.c2p(2.05, 0.25)),
    )
    barrier = Text("Activation energy", font_size=22, color=WARNING_COLOR).move_to(axes.c2p(0.62, 3.25))
    scene.play(FadeIn(labels), FadeIn(barrier), run_time=1.4)

    ball_x = ValueTracker(-2.1)
    barrier_drop = ValueTracker(0.0)

    ball = always_redraw(
        lambda: rolling_ball(radius=0.22, color=PRIMARY_GLOW).move_to(
            axes.c2p(
                ball_x.get_value(),
                base_y(ball_x.get_value())
                - barrier_drop.get_value() * np.exp(-(ball_x.get_value() ** 2) / 1.8)
                + 0.16,
            )
        )
    )
    scene.play(FadeIn(ball), run_time=0.8)
    scene.wait(0.8)

    not_enough = Text("push is not enough", font_size=22, color=DIM_TEXT_COLOR).move_to(axes.c2p(-0.9, 2.15))
    scene.play(ball_x.animate.set_value(-0.55), FadeIn(not_enough), run_time=1.5)
    scene.play(ball_x.animate.set_value(-2.05), run_time=1.2)
    scene.play(ball_x.animate.set_value(-0.35), run_time=1.4)
    scene.play(ball_x.animate.set_value(-2.0), FadeOut(not_enough), run_time=1.1)

    discipline = Text("Discipline lowers the effective barrier.", font_size=28, color=SUCCESS_COLOR)
    discipline.to_edge(DOWN, buff=0.7)
    scene.play(Write(discipline), run_time=1.3)
    scene.play(Transform(curve_group, glowing_curve(lowered_curve, SUCCESS_COLOR)), barrier_drop.animate.set_value(0.9), run_time=2.0)
    scene.play(ball_x.animate.set_value(2.12), run_time=3.0)

    compassion = Text("Not laziness. A system stuck behind a barrier.", font_size=24, color=DIM_TEXT_COLOR)
    compassion.next_to(discipline, UP, buff=0.25)
    scene.play(FadeIn(compassion), run_time=1.2)
    scene.wait(4.0)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)


class Scene05EnergyBarrier(Scene):
    def construct(self):
        play_scene(self)

