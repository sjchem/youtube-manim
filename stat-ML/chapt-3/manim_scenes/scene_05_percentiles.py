"""Scene 05 - percentiles and rank."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, deterministic_values, end_scene, equation_box, label_pill, narration_wait, number_line_with_dots, paced_play, scene_title, vertical_marker


class Scene05Percentiles(Scene):
    """Show percentiles as position in a sorted population."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "05")
    scene.add(cinematic_background())

    values = deterministic_values() + [6.9, 7.1, 7.4]
    line, dots = number_line_with_dots(values, x_min=0, x_max=8)
    VGroup(line, dots).move_to(DOWN * 1.0)
    title = scene_title("Percentiles Are Rank, Not Just Size", "where one value stands among the rest").to_edge(UP, buff=0.42)

    paced_play(scene, FadeIn(title), Create(line), LaggedStart(*[FadeIn(dot, scale=0.3) for dot in dots], lag_ratio=0.04), run_time=1.35)

    sorted_positions = VGroup()
    for index, dot in enumerate(dots):
        target = line.n2p(values[index]) + UP * (0.23 + 0.055 * index)
        sorted_positions.add(Dot(target, radius=0.07, color=dot.get_color()))
    paced_play(scene, Transform(dots, sorted_positions), run_time=1.0)

    p90_value = sorted(values)[int(0.9 * (len(values) - 1))]
    marker = vertical_marker(line, p90_value, "90th percentile", cfg.PURPLE)
    marker[0].put_start_and_end_on(line.n2p(p90_value) + DOWN * 0.34, line.n2p(p90_value) + UP * 1.28)
    marker[1].next_to(marker[0], UP, buff=0.22)
    left_band = Rectangle(
        width=line.n2p(p90_value)[0] - line.n2p(0)[0],
        height=0.28,
        fill_color=cfg.PURPLE,
        fill_opacity=0.2,
        stroke_width=0,
    ).move_to((line.n2p(p90_value) + line.n2p(0)) / 2 + DOWN * 0.58)
    right_note = label_pill("top tail", cfg.ORANGE).next_to(marker, RIGHT, buff=0.2)
    equation = equation_box(r"P_{90}: 90\%\ \text{at or below}", cfg.PURPLE, font_size=44).move_to(LEFT * 2.45 + UP * 1.05)

    paced_play(scene, FadeIn(left_band), FadeIn(marker), run_time=0.8)
    paced_play(scene, FadeIn(equation, shift=DOWN * 0.12), FadeIn(right_note), run_time=0.8)
    paced_play(scene, Indicate(marker, color=cfg.WHITE), run_time=0.7)

    caption = Text("For ML, percentiles turn raw magnitudes into context.", font_size=31, color=cfg.WHITE, weight=BOLD)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.42)
    paced_play(scene, FadeIn(caption, shift=UP * 0.12), run_time=0.75)
    narration_wait(scene, 0.5)
    end_scene(scene, scene_start)
