from manim import *

import config as cfg
from manim_scenes.common import cinematic_background, create_vector_arrow, narration_wait, paced_play, scene_transition


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = Text("Negative means reversal", font_size=42, color=cfg.ZERO).to_edge(UP)
    paced_play(scene, FadeIn(title, shift=DOWN * 0.2))

    guide = Circle(radius=1.65, color=cfg.MUTED, stroke_opacity=0.28).move_to(ORIGIN)
    arrow_pos = create_vector_arrow(LEFT * 1.7, RIGHT * 1.7, cfg.POSITIVE, "+4")
    arrow_neg = create_vector_arrow(RIGHT * 1.7, LEFT * 1.7, cfg.NEGATIVE, "-4")
    paced_play(scene, Create(guide), GrowArrow(arrow_pos[1]), FadeIn(arrow_pos[0]), FadeIn(arrow_pos[2]), run_time=1.0)

    op1 = MathTex(r"\times(-1)", font_size=42)
    op1.set_color_by_tex("-", cfg.NEGATIVE)
    op1.next_to(guide, DOWN, buff=0.6)
    paced_play(scene, FadeIn(op1, shift=UP * 0.2), run_time=0.4)
    paced_play(scene, Rotate(arrow_pos, angle=PI, about_point=ORIGIN), run_time=1.05)
    paced_play(scene, Transform(arrow_pos, arrow_neg), run_time=0.35)
    label1 = Text("One reversal flips.", font_size=30, color=cfg.NEGATIVE).to_edge(DOWN)
    paced_play(scene, FadeIn(label1), run_time=0.45)
    narration_wait(scene, 0.25)

    op2 = MathTex(r"\times(-1)\ \text{again}", font_size=42)
    op2.set_color_by_tex("-", cfg.NEGATIVE)
    op2.next_to(guide, DOWN, buff=0.6)
    paced_play(scene, ReplacementTransform(op1, op2), FadeOut(label1), run_time=0.5)
    paced_play(scene, Rotate(arrow_pos, angle=PI, about_point=ORIGIN), run_time=1.05)
    paced_play(scene, Transform(arrow_pos, create_vector_arrow(LEFT * 1.7, RIGHT * 1.7, cfg.POSITIVE, "+4")), run_time=0.35)

    equation = MathTex(r"(-1)\times(-1)\times4=4", font_size=48)
    equation.set_color_by_tex("-", cfg.NEGATIVE)
    equation.set_color_by_tex("4", cfg.GOLD)
    equation.to_edge(DOWN)
    paced_play(scene, ReplacementTransform(op2, equation), run_time=0.75)
    label2 = Text("Two reversals restore.", font_size=30, color=cfg.GOLD).next_to(equation, UP, buff=0.35)
    paced_play(scene, FadeIn(label2), Flash(arrow_pos, color=cfg.GOLD), run_time=0.7)
    narration_wait(scene, 0.8)
    scene_transition(scene)


class Scene03NegativeAsReversal(Scene):
    def construct(self) -> None:
        play_scene(self)
