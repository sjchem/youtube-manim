from manim import *

from manim_scenes.common import *


def construct_scene_04(scene: MovingCameraScene) -> None:
    add_oceanic_background(scene)

    eq = math_eq("6 \\div 0 = ?", font_size=76).shift(UP * 2.4)
    reverse = math_eq("? \\times 0 = 6", font_size=64, color=WARNING_ORANGE).next_to(eq, DOWN, buff=0.35)
    scene.play(Write(eq), run_time=0.8)
    scene.play(TransformMatchingTex(eq.copy(), reverse), run_time=0.9)

    attempts = VGroup()
    for value in ["1", "10", "-3", "1000"]:
        row = VGroup(
            math_eq(f"{value} \\times 0 = 0", font_size=46),
            Cross(stroke_color=ERROR_RED, stroke_width=6).scale(0.22),
        ).arrange(RIGHT, buff=0.35)
        attempts.add(row)
    attempts.arrange(DOWN, aligned_edge=LEFT, buff=0.38).shift(DOWN * 0.35)

    six_target = glow(math_eq("6", font_size=70, color=MAIN_WHITE).shift(RIGHT * 4.15 + DOWN * 0.35), VALID_GREEN)
    scene.play(FadeIn(six_target), run_time=0.4)
    for row in attempts:
        row[1].move_to(row[0].get_right() + RIGHT * 0.35)
        zero_result = row[0][-1]
        scene.play(Write(row[0]), run_time=0.45)
        scene.play(Indicate(zero_result, color=ERROR_RED), FadeIn(row[1]), run_time=0.35)

    no_solution = warning_label("No solution", font_size=48).to_edge(DOWN, buff=0.55)
    undefined = glowing_text("Undefined", font_size=42, color=ERROR_RED).next_to(no_solution, UP, buff=0.25)
    scene.play(FadeIn(undefined), FadeIn(no_solution), run_time=0.8)
    scene.wait(1.2)
    clear_scene(scene)


class Scene04NoSolution(MovingCameraScene):
    def construct(self) -> None:
        construct_scene_04(self)
