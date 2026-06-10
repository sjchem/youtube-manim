from manim import *

from config import DIM_TEXT_COLOR, PRIMARY_GLOW, SECONDARY_GLOW, TEXT_COLOR
from manim_scenes.common import (
    graph_axes,
    glowing_curve,
    icon_symbol,
    particle_burst,
    set_scene_style,
    soft_background,
)
from utils.math_utils import motivation_decay


def play_scene(scene: Scene):
    set_scene_style(scene)
    scene.add(soft_background())

    title = Text("Motivation is a temporary signal", font_size=34, color=TEXT_COLOR).to_edge(UP, buff=0.6)
    axes = graph_axes(x_range=(0, 8, 1), y_range=(0, 1.2, 0.2), width=8.5, height=4.5).move_to(DOWN * 0.15)
    x_label = Text("Time", font_size=22, color=DIM_TEXT_COLOR).next_to(axes.x_axis, DOWN, buff=0.25)
    y_label = Text("Motivation", font_size=22, color=DIM_TEXT_COLOR).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.25)

    curve = axes.plot(lambda x: motivation_decay(x, m0=1.08, k=0.55), x_range=[0, 8], color=PRIMARY_GLOW)
    curve_group = glowing_curve(curve, PRIMARY_GLOW)

    scene.play(Write(title), Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=2.4)
    scene.play(Create(curve_group), run_time=3.5)

    early = Text("Initial excitement", font_size=22, color=PRIMARY_GLOW).move_to(axes.c2p(1.0, 1.05) + UP * 0.42)
    decay = Text("Decay", font_size=22, color=SECONDARY_GLOW).move_to(axes.c2p(4.25, 0.22) + UP * 0.35)
    scene.play(FadeIn(early), FadeIn(decay), run_time=1.4)

    formula = (
        MathTex("M(t)", "=", "M_0", "e^{-kt}", color=TEXT_COLOR)
        .scale(0.95)
        .to_corner(UR, buff=0.75)
        .shift(DOWN * 0.45)
    )
    scene.play(Write(formula[0]), run_time=0.7)
    scene.play(Write(formula[1:3]), run_time=0.9)
    scene.play(Write(formula[3]), run_time=1.0)

    dots = VGroup()
    for x in [0.4, 1.2, 2.2, 3.4, 5.0, 6.6]:
        y = motivation_decay(x, m0=1.08, k=0.55)
        dot = Dot(axes.c2p(x, y), radius=0.045, color=PRIMARY_GLOW)
        dot.set_opacity(max(0.18, y))
        dots.add(dot)
    scene.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in dots], lag_ratio=0.14), run_time=1.7)
    scene.play(dots.animate.set_opacity(0.26), curve_group[0].animate.set_opacity(0.08), run_time=2.0)

    icons = VGroup(
        icon_symbol("calendar", SECONDARY_GLOW),
        icon_symbol("gym", SECONDARY_GLOW),
        icon_symbol("study", SECONDARY_GLOW),
        icon_symbol("project", SECONDARY_GLOW),
    ).arrange(RIGHT, buff=0.75).scale(0.75).to_edge(DOWN, buff=0.75)
    icon_labels = VGroup(
        Text("goal", font_size=16, color=DIM_TEXT_COLOR),
        Text("gym", font_size=16, color=DIM_TEXT_COLOR),
        Text("study", font_size=16, color=DIM_TEXT_COLOR),
        Text("project", font_size=16, color=DIM_TEXT_COLOR),
    )
    for label, icon in zip(icon_labels, icons):
        label.next_to(icon, DOWN, buff=0.1)
    scene.play(LaggedStart(*[FadeIn(mob, shift=UP * 0.12) for mob in icons], lag_ratio=0.16), run_time=1.8)
    scene.play(FadeIn(icon_labels), run_time=0.8)
    scene.play(icons.animate.set_opacity(0.28), icon_labels.animate.set_opacity(0.35), run_time=2.2)

    note = Text("a simplified metaphor", font_size=19, color=DIM_TEXT_COLOR).next_to(formula, DOWN, buff=0.22)
    scene.play(FadeIn(note), FadeIn(particle_burst(axes.c2p(0.55, 0.8), count=22, radius=0.55)), run_time=1.5)
    scene.wait(4.0)
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=1.0)


class Scene02MotivationDecay(Scene):
    def construct(self):
        play_scene(self)
