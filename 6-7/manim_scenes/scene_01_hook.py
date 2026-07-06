"""Scene 1: cultural hook into the mathematical question."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, end_scene, equation, label, paced_play, title_block


class Scene01Hook(MovingCameraScene):
    """Open with the 6-7 trend and pivot to the core question."""

    def construct(self) -> None:
        play_scene_01(self)


def play_scene_01(scene: Scene) -> None:
    start = begin_scene(scene)

    trend = label("The 6-7 trend has no fixed meaning.", cfg.CYAN, 34).to_edge(UP, buff=0.55)
    six = Text("6", font=cfg.TITLE_FONT, font_size=156, color=cfg.GREEN, weight=BOLD).shift(LEFT * 2.0 + UP * 0.95)
    seven = Text("7", font=cfg.TITLE_FONT, font_size=156, color=cfg.PURPLE, weight=BOLD).shift(RIGHT * 2.0 + UP * 0.95)
    dash = Text("-", font_size=92, color=cfg.WHITE, weight=BOLD)
    for mob in (six, seven, dash):
        mob.set_stroke("#07131A", width=6, opacity=0.85, background=True)
    pair = VGroup(six, dash, seven)
    dash.move_to((six.get_center() + seven.get_center()) / 2)

    question = title_block("Why 6 Is Perfect", "and 7 is mysterious", cfg.GOLD)
    question.scale(0.86).move_to(DOWN * 2.03)

    order = equation(r"6:\;1+2+3=6", cfg.GREEN, 44).next_to(six, DOWN, buff=0.22)
    mystery = equation(r"7:\;1/7=0.\overline{142857}", cfg.PURPLE, 44).next_to(seven, DOWN, buff=0.22)

    paced_play(scene, FadeIn(trend, shift=DOWN * 0.2), run_time=0.7)
    paced_play(scene, GrowFromCenter(six), GrowFromCenter(seven), FadeIn(dash), run_time=0.85)
    scene.play(six.animate.shift(UP * 0.12), seven.animate.shift(DOWN * 0.12), rate_func=there_and_back, run_time=0.55)
    paced_play(scene, FadeIn(question, shift=UP * 0.25), run_time=0.9)
    paced_play(scene, Write(order), Write(mystery), run_time=1.1)
    scene.play(pair.animate.scale(1.04), rate_func=there_and_back, run_time=0.8)

    bridge = label("Two neighbors. Two kinds of order.", cfg.WHITE, 30).to_edge(DOWN, buff=0.15)
    paced_play(scene, FadeIn(bridge, shift=UP * 0.2), run_time=0.7)
    end_scene(scene, start)
