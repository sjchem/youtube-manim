"""Scene 01: Hook - The Strange Rule."""

from __future__ import annotations

from manim import *

from config import ACCENT_CYAN, ACCENT_YELLOW, MUTED_TEXT, QUESTION_COLOR, TEXT_COLOR, WORD_COLOR, WORD_FONT
from manim_scenes.common import (
    fit_to_safe_frame,
    glow_dot,
    keep_inside_frame,
    ocean_background,
    reset_camera,
    rule_badge,
    scene_setup,
    section_label,
    with_glow,
)


class HookStrangeRule(MovingCameraScene):
    """Open with the strange-looking zero-power rule."""

    def construct(self) -> None:
        play_scene_01(self)


def play_scene_01(scene: MovingCameraScene) -> None:
    scene_setup(scene)
    scene.add(ocean_background())

    label = section_label("The strange rule").to_edge(UP).shift(DOWN * 0.15)
    scene.play(FadeIn(label, shift=DOWN * 0.25), run_time=1.2)

    equations = [
        MathTex(r"2^3=8", font_size=68, color=TEXT_COLOR),
        MathTex(r"2^2=4", font_size=68, color=TEXT_COLOR),
        MathTex(r"2^1=2", font_size=68, color=TEXT_COLOR),
        MathTex(r"2^0", "=", "?", font_size=78, color=TEXT_COLOR),
    ]
    equations[-1][2].set_color(QUESTION_COLOR)
    equation_groups = VGroup(
        with_glow(equations[0], ACCENT_CYAN),
        with_glow(equations[1], ACCENT_CYAN),
        with_glow(equations[2], ACCENT_CYAN),
        with_glow(equations[3], ACCENT_YELLOW),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
    equation_groups.move_to(LEFT * 1.2)

    factors = VGroup(
        MathTex(r"2 \cdot 2 \cdot 2", font_size=38, color=MUTED_TEXT),
        MathTex(r"2 \cdot 2", font_size=38, color=MUTED_TEXT),
        MathTex(r"2", font_size=38, color=MUTED_TEXT),
        Text("zero factors?", font=WORD_FONT, font_size=32, color=QUESTION_COLOR),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.61)
    factors.next_to(equation_groups, RIGHT, buff=1.15)
    fit_to_safe_frame(VGroup(equation_groups, factors), max_width=11.4, max_height=5.5)
    keep_inside_frame(VGroup(equation_groups, factors))

    for eq_group, factor in zip(equation_groups, factors):
        scene.play(FadeIn(eq_group, shift=RIGHT * 0.2), FadeIn(factor, shift=LEFT * 0.2), run_time=1.25)
        scene.wait(0.45)

    question_glow = glow_dot(equation_groups[-1].get_right() + RIGHT * 0.33, color=ACCENT_YELLOW, radius=0.06)
    scene.play(FadeIn(question_glow, scale=0.6), run_time=0.8)
    scene.play(
        scene.camera.frame.animate.scale(0.9).move_to(equation_groups[-1]),
        run_time=3.0,
        rate_func=smooth,
    )
    scene.wait(1.4)

    badge = rule_badge("Not a trick. Forced by structure.", color=ACCENT_CYAN, font_size=28)
    badge.next_to(equation_groups, DOWN, buff=0.58)
    keep_inside_frame(badge)
    scene.play(FadeIn(badge, shift=UP * 0.18), run_time=1.2)
    scene.wait(2.2)

    why_one = with_glow(Text("Why one?", font=WORD_FONT, font_size=58, color=QUESTION_COLOR), glow_color=QUESTION_COLOR)
    why_one.move_to(equation_groups[-1])
    scene.play(Transform(equation_groups[-1], why_one), FadeOut(question_glow), run_time=1.4)
    scene.wait(2.0)

    reset_camera(scene, run_time=1.3)
    title_line = Text(
        "The Zero Power Paradox:",
        font=WORD_FONT,
        font_size=42,
        color=WORD_COLOR,
        weight=BOLD,
    )
    question_line = Text(
        "Why Is the Answer One?",
        font=WORD_FONT,
        font_size=52,
        color=QUESTION_COLOR,
        weight=BOLD,
    )
    hook_title = VGroup(title_line, question_line).arrange(DOWN, buff=0.18).move_to(ORIGIN)
    fit_to_safe_frame(hook_title, max_width=11.6, max_height=2.1)

    scene.play(
        FadeOut(label),
        FadeOut(equation_groups),
        FadeOut(factors),
        FadeOut(badge),
        run_time=0.75,
    )
    scene.play(FadeIn(with_glow(hook_title, glow_color=QUESTION_COLOR), scale=0.96), run_time=1.2)
    scene.wait(1.6)
