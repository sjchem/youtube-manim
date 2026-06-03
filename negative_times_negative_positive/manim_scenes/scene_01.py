from manim import *

import config as cfg
from manim_scenes.common import cinematic_background, create_glow_text, narration_wait, paced_play, scene_transition


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())

    eq = MathTex(r"(-3)\times(-4)=+12", font_size=72)
    eq.set_color_by_tex("-", cfg.NEGATIVE)
    eq.set_color_by_tex("+", cfg.GOLD)
    eq.set_color_by_tex("12", cfg.GOLD)
    paced_play(scene, Write(eq), run_time=1.6)
    paced_play(scene, eq.animate.scale(1.04), rate_func=there_and_back, run_time=0.35)
    paced_play(scene, Flash(eq, color=cfg.NEGATIVE, flash_radius=3.0), run_time=0.8)

    question = create_glow_text("Why?", font_size=72, color=cfg.GOLD)
    question.next_to(eq, DOWN, buff=0.7)
    paced_play(scene, FadeIn(question, shift=UP * 0.2), run_time=0.7)
    narration_wait(scene, 0.35)

    rule = Text("minus times minus is plus", font_size=34, color=cfg.MUTED)
    rule.move_to(DOWN * 1.8)
    strike = Line(rule.get_left() + LEFT * 0.1, rule.get_right() + RIGHT * 0.1, color=cfg.NEGATIVE, stroke_width=8)
    paced_play(scene, FadeOut(question), FadeIn(rule, shift=UP * 0.15), run_time=0.5)
    paced_play(scene, Create(strike), run_time=0.35)
    narration_wait(scene, 0.25)

    answer = create_glow_text("Not a trick. A structure.", font_size=42, color=cfg.POSITIVE)
    answer.move_to(DOWN * 1.65)
    paced_play(scene, FadeOut(rule), FadeOut(strike), FadeIn(answer, shift=UP * 0.2), run_time=0.75)
    narration_wait(scene, 0.9)

    title_top = create_glow_text("Negative x Negative Is Positive", font_size=48, color=cfg.GOLD)
    title_bottom = create_glow_text("— But Why?", font_size=52, color=cfg.POSITIVE)
    title_card = VGroup(title_top, title_bottom).arrange(DOWN, buff=0.18).move_to(ORIGIN)
    underline = Line(LEFT * 2.6, RIGHT * 2.6, color=cfg.NEGATIVE, stroke_width=5)
    underline.next_to(title_card, DOWN, buff=0.32)
    underline_glow = underline.copy().set_stroke(cfg.NEGATIVE, width=16, opacity=0.16)
    title_group = VGroup(title_card, underline_glow, underline)
    paced_play(scene, FadeOut(eq), FadeOut(answer), FadeIn(title_group, shift=UP * 0.18), run_time=1.15)
    paced_play(scene, Flash(title_group, color=cfg.GOLD, flash_radius=4.2), run_time=0.9)
    narration_wait(scene, 1.25)
    scene_transition(scene)


class Scene01ColdOpen(Scene):
    def construct(self) -> None:
        play_scene(self)
