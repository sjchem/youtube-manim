"""Scene 03: Exponent law consistency."""

from __future__ import annotations

from manim import *

from config import ACCENT_BLUE, ACCENT_CYAN, ACCENT_TEAL, ACCENT_YELLOW, TEXT_COLOR
from manim_scenes.common import (
    fit_to_safe_frame,
    highlight_box,
    keep_inside_frame,
    make_block_stack,
    ocean_background,
    reset_camera,
    rule_badge,
    scene_setup,
    section_label,
    soft_arrow,
    with_glow,
)


class ExponentLawScene(MovingCameraScene):
    """Use a^m / a^m to force a^0 = 1."""

    def construct(self) -> None:
        play_scene_03(self)


def play_scene_03(scene: MovingCameraScene) -> None:
    scene_setup(scene)
    scene.add(ocean_background())

    label = section_label("The rule must stay consistent").to_edge(UP).shift(DOWN * 0.12)
    scene.play(FadeIn(label, shift=DOWN * 0.2), run_time=1.0)

    stack_top = make_block_stack(r"a^m", color=ACCENT_BLUE)
    stack_bottom = make_block_stack(r"a^m", color=ACCENT_BLUE)
    stack_pair = VGroup(stack_top, stack_bottom).arrange(DOWN, buff=0.52)
    fraction_bar = Line(LEFT * 1.15, RIGHT * 1.15, color=ACCENT_CYAN, stroke_width=4)
    fraction_bar.move_to(stack_pair.get_center())
    stacks = VGroup(stack_top, fraction_bar, stack_bottom).move_to(LEFT * 3.25)

    fraction = MathTex(r"\frac{a^m}{a^m}", font_size=76, color=TEXT_COLOR).move_to(ORIGIN + UP * 0.6)
    fit_to_safe_frame(VGroup(stacks, fraction), max_width=10.8, max_height=4.2)
    keep_inside_frame(VGroup(stacks, fraction))
    scene.play(FadeIn(stacks, shift=RIGHT * 0.2), run_time=1.3)
    scene.wait(0.7)
    scene.play(TransformFromCopy(stacks, fraction), run_time=1.2)
    scene.wait(0.8)

    left_path = MathTex(r"\frac{a^m}{a^m}=1", font_size=48, color=TEXT_COLOR)
    left_path.move_to(LEFT * 3.05 + DOWN * 1.75)
    left_label = rule_badge("Same thing divided by itself", color=ACCENT_TEAL, font_size=21)
    left_label.next_to(left_path, DOWN, buff=0.2)
    left_arrow = soft_arrow(fraction.get_left() + LEFT * 0.05, left_path.get_top(), color=ACCENT_TEAL)

    right_path = MathTex(r"\frac{a^m}{a^m}=a^{m-m}=a^0", font_size=44, color=TEXT_COLOR)
    right_path.move_to(RIGHT * 3.0 + DOWN * 1.75)
    right_label = rule_badge("Subtract exponents", color=ACCENT_CYAN, font_size=21)
    right_label.next_to(right_path, DOWN, buff=0.2)
    right_arrow = soft_arrow(fraction.get_right() + RIGHT * 0.05, right_path.get_top(), color=ACCENT_CYAN)
    fit_to_safe_frame(VGroup(left_path, left_label, right_path, right_label), max_width=12.2, max_height=2.1)
    keep_inside_frame(VGroup(left_path, left_label, right_path, right_label))

    scene.play(Create(left_arrow), FadeIn(left_path, shift=DOWN * 0.16), FadeIn(left_label), run_time=1.3)
    scene.wait(1.0)
    scene.play(Create(right_arrow), FadeIn(right_path, shift=DOWN * 0.16), FadeIn(right_label), run_time=1.5)
    scene.wait(1.0)

    consistency = rule_badge("Consistency", color=ACCENT_YELLOW, font_size=30)
    consistency.move_to(UP * 2.25)
    scene.play(FadeIn(consistency, scale=0.95), run_time=0.9)

    result = with_glow(MathTex(r"a^0=1", font_size=82, color=TEXT_COLOR), glow_color=ACCENT_YELLOW)
    result.move_to(DOWN * 0.22)
    keep_inside_frame(result)
    merge_left = soft_arrow(left_path.get_top(), result.get_left() + LEFT * 0.05, color=ACCENT_TEAL)
    merge_right = soft_arrow(right_path.get_top(), result.get_right() + RIGHT * 0.05, color=ACCENT_CYAN)
    scene.play(Create(merge_left), Create(merge_right), run_time=1.0)
    scene.play(FadeIn(result, scale=0.92), run_time=1.2)
    scene.wait(1.1)

    condition = MathTex(r"a\ne0", font_size=48, color=ACCENT_YELLOW)
    condition.next_to(result, DOWN, buff=0.38)
    condition_box = highlight_box(condition, color=ACCENT_YELLOW, buff=0.18)
    scene.play(FadeIn(condition), Create(condition_box), run_time=1.0)
    scene.wait(2.1)

    scene.play(
        scene.camera.frame.animate.scale(0.92).move_to(VGroup(result, condition)),
        run_time=2.0,
        rate_func=smooth,
    )
    scene.wait(1.4)
    reset_camera(scene, run_time=1.0)
