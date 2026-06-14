from manim import *

from manim_scenes.common import *


def construct_scene_01(scene: MovingCameraScene) -> None:
    add_oceanic_background(scene)

    title = short_label("Division by zero", font_size=32).to_edge(UP, buff=1.05)
    panel = calculator_panel()
    equation = math_eq("1 \\div 0 = ?", font_size=78).move_to(panel)
    machine = VGroup(panel, equation)

    gears = VGroup(
        *[
            RegularPolygon(n=8, radius=0.28, color=CYAN, fill_opacity=0.05)
            .rotate(i * PI / 8)
            .next_to(panel, direction, buff=0.35)
            for i, direction in enumerate([LEFT, RIGHT])
        ]
    )

    scene.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(panel), run_time=0.9)
    reveal_equation(scene, equation, run_time=0.9)
    scene.play(Rotate(gears[0], angle=PI), Rotate(gears[1], angle=-PI), FadeIn(gears), run_time=1.0)
    error_glitch_effect(scene, machine, flashes=7)

    warning = VGroup(
        warning_label("ERROR", font_size=62),
        glowing_text("UNDEFINED", font_size=44, color=ERROR_RED),
    ).arrange(DOWN, buff=0.22)
    warning.move_to(ORIGIN).shift(DOWN * 1.65)
    scene.play(Flash(equation, color=WARNING_ORANGE, flash_radius=1.2), FadeIn(warning), run_time=0.7)
    camera_zoom(scene, equation, scale=0.82, run_time=0.9)
    why = short_label("Why?", color=MAIN_WHITE, font_size=40).next_to(warning, DOWN, buff=0.45)
    scene.play(FadeIn(why, shift=UP * 0.2), run_time=0.65)
    scene.wait(1.2)

    scene.play(
        FadeOut(title),
        FadeOut(machine),
        FadeOut(gears),
        FadeOut(warning),
        FadeOut(why),
        run_time=0.55,
    )
    reset_camera(scene)
    final_title = glowing_text("Why Can't We Divide by Zero?", font_size=48, color=MAIN_WHITE)
    final_title.scale_to_fit_width(config.frame_width - 1.25)
    subscribe_line = short_label(
        "Subscribe for math mysteries cracked open.",
        color=CYAN,
        font_size=28,
    )
    title_card = VGroup(final_title, subscribe_line).arrange(DOWN, buff=0.35).move_to(ORIGIN)
    scene.play(FadeIn(title_card, shift=UP * 0.25), run_time=0.8)
    scene.wait(1.4)
    clear_scene(scene)


class Scene01Hook(MovingCameraScene):
    def construct(self) -> None:
        construct_scene_01(self)
