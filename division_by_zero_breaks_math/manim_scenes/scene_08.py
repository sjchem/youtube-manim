from manim import *

from manim_scenes.common import *


def construct_scene_08(scene: MovingCameraScene) -> None:
    add_oceanic_background(scene)

    logic = VGroup(
        math_eq("a \\div b = c", font_size=62),
        short_label("means", font_size=28),
        math_eq("c \\times b = a", font_size=62, color=CYAN_BRIGHT),
    ).arrange(DOWN, buff=0.22).shift(UP * 2.0)
    scene.play(FadeIn(logic, lag_ratio=0.2), run_time=1.2)

    impossible = VGroup(
        math_eq("6 \\div 0 = ?", font_size=52),
        math_eq("? \\times 0 = 6", font_size=48, color=ERROR_RED),
        short_label("Impossible", color=ERROR_RED, font_size=32),
    ).arrange(DOWN, buff=0.18).shift(LEFT * 3.35 + DOWN * 0.5)
    not_unique = VGroup(
        math_eq("0 \\div 0 = ?", font_size=52),
        math_eq("? \\times 0 = 0", font_size=48, color=WARNING_ORANGE),
        short_label("Not unique", color=WARNING_ORANGE, font_size=32),
    ).arrange(DOWN, buff=0.18).shift(RIGHT * 3.35 + DOWN * 0.5)
    scene.play(FadeIn(impossible, shift=RIGHT * 0.2), FadeIn(not_unique, shift=LEFT * 0.2), run_time=1.1)

    final = VGroup(
        glowing_text("Division by zero is not forbidden.", font_size=40, color=MAIN_WHITE),
        glowing_text("It is undefined.", font_size=52, color=WARNING_ORANGE),
    ).arrange(DOWN, buff=0.24).to_edge(DOWN, buff=0.55)
    scene.play(FadeIn(final), run_time=1.0)
    scene.wait(1.2)

    scene.play(FadeOut(logic), FadeOut(impossible), FadeOut(not_unique), FadeOut(final), run_time=0.8)
    zero = glow(math_eq("0", font_size=132, color=MAIN_WHITE), CYAN, layers=4, stroke_width=12)
    closing = short_label("Zero does not mean simple. Zero means the rules change.", color=CYAN_BRIGHT, font_size=34)
    closing.next_to(zero, DOWN, buff=0.55)
    button_bg = RoundedRectangle(
        width=3.8,
        height=0.72,
        corner_radius=0.18,
        stroke_color=MAIN_WHITE,
        stroke_width=2,
        fill_color=ERROR_RED,
        fill_opacity=0.95,
    )
    play_icon = Triangle(color=MAIN_WHITE, fill_color=MAIN_WHITE, fill_opacity=1).scale(0.16).rotate(-PI / 2)
    button_text = Text("SUBSCRIBE", font_size=30, color=MAIN_WHITE, weight=BOLD)
    button_content = VGroup(play_icon, button_text).arrange(RIGHT, buff=0.18)
    subscribe_button = VGroup(button_bg, button_content)
    button_content.move_to(button_bg)
    subscribe_button.next_to(closing, DOWN, buff=0.42)

    scene.play(FadeIn(zero, scale=1.2), run_time=1.0)
    scene.play(FadeIn(closing), run_time=0.8)
    scene.play(FadeIn(subscribe_button, scale=0.82), run_time=0.55)
    scene.play(subscribe_button.animate.scale(1.08), run_time=0.18)
    scene.play(subscribe_button.animate.scale(1 / 1.08), run_time=0.18)
    scene.wait(1.5)
    clear_scene(scene)


class Scene08FinalSummary(MovingCameraScene):
    def construct(self) -> None:
        construct_scene_08(self)
