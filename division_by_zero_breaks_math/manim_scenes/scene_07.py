from manim import *

from manim_scenes.common import *


def construct_scene_07(scene: MovingCameraScene) -> None:
    add_oceanic_background(scene)

    lines = [
        (">>> 1 / 0", MAIN_WHITE),
        ("ZeroDivisionError", ERROR_RED),
        (">>> 1.0 / 0.0", MAIN_WHITE),
        ("Infinity", LIMIT_PURPLE),
        (">>> 0.0 / 0.0", MAIN_WHITE),
        ("NaN  |  Not a Number", WARNING_ORANGE),
    ]
    panel = terminal_panel(lines)
    header = short_label("Computers need rules", font_size=36).next_to(panel, UP, buff=0.45)
    scene.play(FadeIn(header), FadeIn(panel[0]), run_time=0.8)
    for line in panel[1]:
        scene.play(FadeIn(line, shift=RIGHT * 0.15), run_time=0.28)
        if "Error" in line.text or "NaN" in line.text:
            scene.play(Flash(line, color=WARNING_ORANGE, flash_radius=0.7), run_time=0.25)

    pixels = VGroup(
        *[
            Square(side_length=0.08, fill_color=ERROR_RED if i % 3 == 0 else CYAN, fill_opacity=0.8, stroke_width=0)
            .move_to(panel.get_center() + RIGHT * ((i % 18) - 9) * 0.12 + DOWN * ((i // 18) - 3) * 0.12)
            for i in range(126)
        ]
    )
    scene.play(FadeIn(pixels, lag_ratio=0.01), run_time=0.55)
    scene.play(pixels.animate.set_opacity(0.15).scale(1.8), run_time=0.7)
    note = short_label("Integer error, floating-point infinity, or NaN", color=MAIN_WHITE, font_size=30).to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(note), run_time=0.55)
    scene.wait(1.2)
    clear_scene(scene)


class Scene07Computers(MovingCameraScene):
    def construct(self) -> None:
        construct_scene_07(self)
