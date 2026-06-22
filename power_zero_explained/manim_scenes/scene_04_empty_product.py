"""Scene 04: Empty product intuition."""

from __future__ import annotations

from manim import *

from config import ACCENT_CYAN, ACCENT_TEAL, ACCENT_YELLOW, PANEL_COLOR, TEXT_COLOR, WORD_COLOR, WORD_FONT
from manim_scenes.common import (
    factor_expression,
    fit_to_safe_frame,
    glow_dot,
    keep_inside_frame,
    make_factor_chips,
    ocean_background,
    reset_camera,
    rule_badge,
    scene_setup,
    section_label,
    with_glow,
)


class EmptyProductScene(MovingCameraScene):
    """Explain zero factors through the multiplicative identity."""

    def construct(self) -> None:
        play_scene_04(self)


def play_scene_04(scene: MovingCameraScene) -> None:
    scene_setup(scene)
    scene.add(ocean_background())

    label = section_label("Multiplying nothing").to_edge(UP).shift(DOWN * 0.12)
    scene.play(FadeIn(label, shift=DOWN * 0.2), run_time=1.0)

    rows = VGroup()
    for exponent, count in [(3, 3), (2, 2), (1, 1), (0, 0)]:
        left = MathTex(rf"a^{exponent}", "=", font_size=48, color=TEXT_COLOR)
        right = factor_expression("a", count, font_size=46)
        row = VGroup(left, right).arrange(RIGHT, buff=0.25)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36)
    rows.move_to(LEFT * 3.55 + UP * 0.25)
    fit_to_safe_frame(rows, max_width=5.4, max_height=4.6)
    keep_inside_frame(rows)

    scene.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.16) for row in rows], lag_ratio=0.14), run_time=2.0)
    scene.wait(0.8)

    chips = make_factor_chips("a", 3, color=ACCENT_TEAL)
    chips.move_to(RIGHT * 2.85 + UP * 1.55)
    basket = RoundedRectangle(
        corner_radius=0.14,
        width=3.3,
        height=1.55,
        fill_color=PANEL_COLOR,
        fill_opacity=0.6,
        stroke_color=ACCENT_CYAN,
        stroke_width=1.8,
    )
    basket.move_to(RIGHT * 2.85 + DOWN * 0.35)
    start_value = with_glow(MathTex("1", font_size=72, color=TEXT_COLOR), glow_color=ACCENT_YELLOW)
    start_value.move_to(basket)
    start_label = Text("start", font=WORD_FONT, font_size=24, color=WORD_COLOR).next_to(basket, UP, buff=0.2)
    fit_to_safe_frame(VGroup(chips, basket, start_value, start_label), max_width=4.9, max_height=4.2)
    keep_inside_frame(VGroup(chips, basket, start_value, start_label))

    scene.play(FadeIn(chips, shift=DOWN * 0.2), Create(basket), FadeIn(start_value), FadeIn(start_label), run_time=1.4)
    scene.wait(0.8)

    for index, power_tex in enumerate([r"a", r"a^2", r"a^3"]):
        chip = chips[index]
        target = chip.copy()
        scene.add(target)
        scene.play(target.animate.move_to(basket.get_center()), run_time=0.8)
        new_value = with_glow(MathTex(power_tex, font_size=72, color=TEXT_COLOR), glow_color=ACCENT_TEAL)
        new_value.move_to(basket)
        scene.play(Transform(start_value, new_value), FadeOut(target), run_time=0.75)
        scene.wait(0.25)

    scene.wait(0.7)
    scene.play(
        FadeOut(chips),
        Transform(start_value, with_glow(MathTex("1", font_size=80, color=TEXT_COLOR), glow_color=ACCENT_YELLOW).move_to(basket)),
        run_time=1.0,
    )
    no_factors = Text("zero factors", font=WORD_FONT, font_size=30, color=WORD_COLOR)
    no_factors.next_to(basket, DOWN, buff=0.24)
    scene.play(FadeIn(no_factors, shift=UP * 0.15), run_time=0.8)
    scene.wait(0.9)

    identity = rule_badge("1 is the identity of multiplication", color=ACCENT_YELLOW, font_size=25)
    identity.to_edge(DOWN, buff=0.38)
    keep_inside_frame(identity)
    scene.play(FadeIn(identity, shift=UP * 0.2), run_time=1.0)

    zero_row_highlight = SurroundingRectangle(rows[-1], buff=0.12, color=ACCENT_YELLOW, stroke_width=3)
    scene.play(Create(zero_row_highlight), run_time=0.8)
    dot = glow_dot(rows[-1].get_right() + RIGHT * 0.28, color=ACCENT_YELLOW, radius=0.045)
    keep_inside_frame(dot)
    scene.play(FadeIn(dot), run_time=0.5)
    scene.wait(2.0)

    result = with_glow(MathTex(r"a^0=1", font_size=64, color=TEXT_COLOR), glow_color=ACCENT_YELLOW)
    result.next_to(no_factors, DOWN, buff=0.28)
    keep_inside_frame(result)
    scene.play(FadeIn(result, shift=UP * 0.18), run_time=1.0)
    scene.wait(1.9)
    reset_camera(scene, run_time=1.0)
