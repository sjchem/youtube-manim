"""Scene 05: Graph view of exponential curves."""

from __future__ import annotations

from fractions import Fraction

from manim import *

from config import ACCENT_CYAN, ACCENT_TEAL, ACCENT_YELLOW, TEXT_COLOR, WORD_COLOR, WORD_FONT
from manim_scenes.common import (
    fit_to_safe_frame,
    glow_dot,
    keep_inside_frame,
    make_exponential_axes,
    ocean_background,
    readable_label,
    reset_camera,
    scene_setup,
    section_label,
    with_glow,
)
from utils.math_utils import exponential_points, latex_fraction


class GraphViewScene(MovingCameraScene):
    """Show y = a^x crossing the y-axis at 1."""

    def construct(self) -> None:
        play_scene_05(self)


def _point_label(base: int, x: int, value: int | Fraction) -> MathTex:
    value_tex = latex_fraction(value)
    return MathTex(rf"{base}^{{{x}}}={value_tex}", font_size=38, color=TEXT_COLOR)


def play_scene_05(scene: MovingCameraScene) -> None:
    scene_setup(scene)
    scene.add(ocean_background())

    label = section_label("The curve passes through one").to_edge(UP).shift(DOWN * 0.12)
    scene.play(FadeIn(label, shift=DOWN * 0.2), run_time=1.0)

    axes, curve, curve_label = make_exponential_axes(2, color=ACCENT_CYAN)
    curve_label.next_to(curve.point_from_proportion(0.72), UP, buff=0.18)
    graph_group = VGroup(axes, curve, curve_label)
    graph_group.move_to(LEFT * 0.35 + DOWN * 0.35)
    fit_to_safe_frame(graph_group, max_width=10.4, max_height=5.55)
    keep_inside_frame(graph_group)
    scene.play(Create(axes), run_time=1.3)
    scene.play(Create(curve), FadeIn(curve_label), run_time=1.8)
    scene.wait(0.7)

    points = exponential_points(2, [3, 2, 1, 0, -1])
    moving_dot = None
    value_label = None
    for x, value in points:
        y = float(value)
        point = axes.coords_to_point(x, y)
        new_dot = glow_dot(point, color=ACCENT_YELLOW if x == 0 else ACCENT_CYAN, radius=0.05)
        new_label = readable_label(_point_label(2, x, value), fill_opacity=0.84, buff=0.16)
        new_label.to_corner(UR, buff=0.68)
        keep_inside_frame(new_label)

        if moving_dot is None:
            moving_dot = new_dot
            value_label = new_label
            scene.play(FadeIn(moving_dot, scale=0.8), FadeIn(value_label, shift=LEFT * 0.2), run_time=0.9)
        else:
            scene.play(Transform(moving_dot, new_dot), Transform(value_label, new_label), run_time=1.05)
        scene.wait(0.45)

    intercept = axes.coords_to_point(0, 1)
    v_line = DashedLine(axes.coords_to_point(0, 0), intercept, color=ACCENT_YELLOW, stroke_width=2.5)
    h_line = DashedLine(axes.coords_to_point(-1.15, 1), intercept, color=ACCENT_YELLOW, stroke_width=2.5)
    intercept_label = with_glow(MathTex(r"(0,1)", font_size=46, color=TEXT_COLOR), glow_color=ACCENT_YELLOW)
    intercept_label.next_to(intercept, LEFT + UP, buff=0.16)
    scene.play(Create(v_line), Create(h_line), FadeIn(intercept_label), run_time=1.1)
    scene.play(scene.camera.frame.animate.scale(0.92).move_to(intercept), run_time=2.0, rate_func=smooth)
    scene.wait(1.0)
    reset_camera(scene, run_time=1.2)

    curve_3 = axes.plot(lambda x: 3**x, x_range=[-1.25, 2.05], color=ACCENT_TEAL, stroke_width=5)
    label_3 = MathTex(r"y=3^x", font_size=38, color=ACCENT_TEAL)
    label_3.next_to(curve_3.point_from_proportion(0.72), UP, buff=0.18)
    same_intercept = glow_dot(axes.coords_to_point(0, 1), color=ACCENT_YELLOW, radius=0.055)

    scene.play(
        Transform(curve, curve_3),
        Transform(curve_label, label_3),
        Transform(moving_dot, same_intercept),
        FadeOut(value_label),
        FadeOut(v_line),
        FadeOut(h_line),
        run_time=1.5,
    )
    same_label = VGroup(
        Text("same", font=WORD_FONT, font_size=28, color=WORD_COLOR),
        MathTex("(0,1)", font_size=40, color=ACCENT_YELLOW),
    ).arrange(RIGHT, buff=0.14)
    same_label.next_to(same_intercept, RIGHT, buff=0.2)
    keep_inside_frame(same_label)
    scene.play(FadeIn(same_label, shift=LEFT * 0.1), run_time=0.8)
    scene.wait(1.6)

    conclusion = with_glow(
        VGroup(
            MathTex(r"y=a^x", font_size=44, color=TEXT_COLOR),
            Text("passes through", font=WORD_FONT, font_size=28, color=WORD_COLOR),
            MathTex(r"(0,1)", font_size=44, color=ACCENT_YELLOW),
        ).arrange(RIGHT, buff=0.18),
        glow_color=ACCENT_YELLOW,
    )
    conclusion.to_edge(DOWN, buff=0.45)
    fit_to_safe_frame(conclusion, max_width=11.7, max_height=0.95)
    keep_inside_frame(conclusion)
    scene.play(FadeIn(conclusion, shift=UP * 0.2), run_time=1.1)
    scene.wait(2.0)
    reset_camera(scene, run_time=0.8)
