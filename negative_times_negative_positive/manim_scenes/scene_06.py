from manim import *

import config as cfg
from manim_scenes.common import cinematic_background, create_balance_scale, create_math_machine, narration_wait, paced_play, scene_transition


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = Text("The distributive law machine", font_size=40, color=cfg.ZERO).to_edge(UP)
    paced_play(scene, FadeIn(title))

    expression = MathTex(r"-3(5+(-5))", font_size=54)
    expression.set_color_by_tex("-", cfg.NEGATIVE)
    expression.move_to(UP * 1.8)
    zero_step = MathTex(r"5+(-5)=0", font_size=44, color=cfg.ZERO).next_to(expression, DOWN, buff=0.45)
    zero_step.set_color_by_tex("-", cfg.NEGATIVE)
    total = MathTex(r"-3\times0=0", font_size=44, color=cfg.GOLD).next_to(zero_step, DOWN, buff=0.25)
    total.set_color_by_tex("-", cfg.NEGATIVE)
    paced_play(scene, Write(expression), run_time=0.8)
    paced_play(scene, FadeIn(zero_step, shift=DOWN * 0.15), run_time=0.6)
    paced_play(scene, FadeIn(total, shift=DOWN * 0.15), run_time=0.6)
    narration_wait(scene, 0.35)

    machine = create_math_machine("distribute").move_to(ORIGIN)
    input_expr = expression.copy().scale(0.72).move_to(LEFT * 4.5)
    output_expr = MathTex(r"(-3)(5)+(-3)(-5)", font_size=34)
    output_expr.set_color_by_tex("-", cfg.NEGATIVE)
    output_expr.move_to(RIGHT * 3.65)
    paced_play(scene, FadeOut(zero_step), FadeOut(total), expression.animate.scale(0.72).move_to(LEFT * 4.5), FadeIn(machine), run_time=0.85)
    paced_play(scene, expression.animate.move_to(machine.get_left() + LEFT * 0.4), run_time=0.45)
    paced_play(scene, Rotate(machine[-2], TAU), Rotate(machine[-1], -TAU), run_time=0.75)
    paced_play(scene, ReplacementTransform(input_expr, output_expr), expression.animate.set_opacity(0), run_time=0.8)
    narration_wait(scene, 0.25)

    known = MathTex(r"(-3)(5)=-15", font_size=42)
    known.set_color_by_tex("-", cfg.NEGATIVE)
    known.next_to(output_expr, DOWN, buff=0.55)
    line = MathTex(r"-15+(-3)(-5)=0", font_size=44)
    line.set_color_by_tex("-", cfg.NEGATIVE)
    line.next_to(known, DOWN, buff=0.25)
    paced_play(scene, Write(known), run_time=0.65)
    paced_play(scene, Write(line), run_time=0.75)

    balance = create_balance_scale("-15", "?").scale(0.95).to_edge(DOWN, buff=0.45)
    paced_play(scene, FadeIn(balance, shift=UP * 0.2), run_time=0.75)
    reveal = MathTex(r"+15", font_size=34, color=cfg.GOLD).move_to(balance[-1])
    paced_play(scene, Flash(balance[-1], color=cfg.GOLD), Transform(balance[-1], reveal), run_time=0.8)

    final = MathTex(r"(-3)(-5)=+15", font_size=58)
    final.set_color_by_tex("-", cfg.NEGATIVE)
    final.set_color_by_tex("+", cfg.GOLD)
    final.to_edge(DOWN, buff=0.35)
    paced_play(scene, FadeOut(balance), ReplacementTransform(line.copy(), final), run_time=0.9)
    paced_play(scene, Flash(final, color=cfg.GOLD), run_time=0.6)
    narration_wait(scene, 0.8)
    scene_transition(scene)


class Scene06DistributiveLawMachine(Scene):
    def construct(self) -> None:
        play_scene(self)
