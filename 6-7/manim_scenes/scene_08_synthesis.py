"""Scene 8: visible order and hidden order meet."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, end_scene, equation, label, paced_play, panel, regular_polygon


class Scene08Synthesis(MovingCameraScene):
    """Close the scientific story before the subscribe card."""

    def construct(self) -> None:
        play_scene_08(self)


def play_scene_08(scene: Scene) -> None:
    start = begin_scene(scene)

    heading = label("6 is visible order. 7 is hidden order.", cfg.WHITE, 38).to_edge(UP, buff=0.48)
    left_panel = panel(5.4, 4.35, cfg.GREEN, 0.14).shift(LEFT * 3.05 + UP * 0.05)
    right_panel = panel(5.4, 4.35, cfg.PURPLE, 0.14).shift(RIGHT * 3.05 + UP * 0.05)

    six = Text("6", font=cfg.TITLE_FONT, font_size=118, color=cfg.GREEN, weight=BOLD).move_to(left_panel.get_top() + DOWN * 0.7)
    seven = Text("7", font=cfg.TITLE_FONT, font_size=118, color=cfg.PURPLE, weight=BOLD).move_to(right_panel.get_top() + DOWN * 0.7)
    for mob in (six, seven):
        mob.set_stroke("#07131A", width=5, opacity=0.85, background=True)

    hexagon = regular_polygon(6, radius=0.85, color=cfg.GREEN).move_to(left_panel.get_center() + UP * 0.05)
    perfect = equation(r"1+2+3=6", cfg.GREEN, 42).next_to(hexagon, DOWN, buff=0.28)

    cycle = VGroup()
    for index, digit in enumerate("142857"):
        dot = Dot(radius=0.085, color=cfg.GOLD)
        angle = PI / 2 - TAU * index / 6
        dot.move_to(right_panel.get_center() + UP * 0.03 + 0.96 * np.array([np.cos(angle), np.sin(angle), 0]))
        num = Text(digit, font_size=34, color=cfg.GOLD, weight=BOLD).move_to(dot.get_center() * 0.96 + right_panel.get_center() * 0.04)
        cycle.add(dot, num)
    cycle_circle = Circle(radius=0.96, color=cfg.PURPLE, stroke_width=3).move_to(right_panel.get_center() + UP * 0.03)
    hidden = equation(r"0.\overline{142857}", cfg.PURPLE, 42).next_to(cycle_circle, DOWN, buff=0.28)

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), Create(left_panel), Create(right_panel), run_time=0.85)
    paced_play(scene, FadeIn(six, scale=0.8), FadeIn(seven, scale=0.8), run_time=0.65)
    paced_play(scene, Create(hexagon), Write(perfect), Create(cycle_circle), FadeIn(cycle), Write(hidden), run_time=1.2)

    bridge = Arrow(left_panel.get_right() + LEFT * 0.2, right_panel.get_left() + RIGHT * 0.2, buff=0.2, color=cfg.CYAN, stroke_width=6)
    bridge_label = equation(r"\gcd(6,7)=1", cfg.CYAN, 46).move_to(bridge.get_center() + DOWN * 0.42)
    paced_play(scene, GrowArrow(bridge), Write(bridge_label), run_time=0.8)

    factorial = equation(r"7!=5040", cfg.GOLD, 42).to_edge(DOWN, buff=0.28).shift(LEFT * 2.35)
    half_week = equation(r"{7\cdot24\cdot60\over2}=5040", cfg.CYAN, 34).to_edge(DOWN, buff=0.18).shift(RIGHT * 2.25)
    paced_play(scene, Write(factorial), Write(half_week), run_time=0.95)

    final = label("Mathematics contains both the pattern you see and the pattern that finds you.", cfg.WHITE, 30).to_edge(DOWN, buff=0.18)
    paced_play(scene, FadeOut(factorial), FadeOut(half_week), FadeIn(final, shift=UP * 0.12), run_time=0.7)
    end_scene(scene, start)
