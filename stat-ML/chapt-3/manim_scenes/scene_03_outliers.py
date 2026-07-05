"""Scene 03 - outliers and robust center."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, label_pill, narration_wait, number_line_with_dots, paced_play, scene_title


class Scene03Outliers(Scene):
    """Show why mean and median respond differently to extremes."""

    def construct(self) -> None:
        play_scene(self)


def center_callout(line: NumberLine, value: float, label: str, detail: str, color: str, position: np.ndarray) -> VGroup:
    """Create a separated marker label for close mean/median positions."""
    base = line.n2p(value)
    marker = Line(base + DOWN * 0.35, base + UP * 0.68, color=color, stroke_width=5)
    name = label_pill(label, color, font_size=23)
    desc = Text(detail, font_size=19, color=cfg.WHITE, weight=BOLD)
    desc.set_stroke("#02111D", width=3, opacity=0.75, background=True)
    card = VGroup(name, desc).arrange(DOWN, buff=0.08).move_to(position)
    connector = Line(card.get_bottom() + DOWN * 0.04, marker.get_top(), color=color, stroke_width=2.4, stroke_opacity=0.68)
    return VGroup(marker, connector, card)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene, "03")
    scene.add(cinematic_background())

    values = [2.0, 2.1, 2.2, 2.4, 2.6, 2.7, 2.8, 3.0, 3.1, 3.3, 3.4]
    line, dots = number_line_with_dots(values, x_min=0, x_max=11, length=9.5)
    VGroup(line, dots).move_to(DOWN * 0.25)
    title = scene_title("An Outlier Pulls the Average", "The median barely moves").to_edge(UP, buff=0.42)
    mean_marker = center_callout(line, np.mean(values), "mean", "balance shifts", cfg.CYAN, RIGHT * 2.05 + UP * 1.25)
    median_marker = center_callout(line, np.median(values), "median", "order stays steady", cfg.GREEN, LEFT * 2.05 + UP * 1.25)

    paced_play(scene, FadeIn(title), Create(line), LaggedStart(*[FadeIn(dot, scale=0.3) for dot in dots], lag_ratio=0.04), run_time=1.65)
    paced_play(scene, FadeIn(mean_marker), FadeIn(median_marker), run_time=1.05)

    outlier_value = 9.8
    outlier = Dot(line.n2p(outlier_value) + UP * 0.28, radius=0.1, color=cfg.ORANGE)
    warning = label_pill("new extreme value", cfg.ORANGE).next_to(outlier, UP, buff=0.18)
    pulled_mean = center_callout(line, np.mean(values + [outlier_value]), "mean", "pulled right", cfg.ORANGE, RIGHT * 2.25 + UP * 1.25)
    stable_median = center_callout(line, np.median(values + [outlier_value]), "median", "barely moves", cfg.GREEN, LEFT * 2.05 + UP * 1.25)
    tug = Arrow(mean_marker[0].get_center() + UP * 0.25, pulled_mean[0].get_center() + UP * 0.25, color=cfg.ORANGE, stroke_width=7, buff=0.08)

    paced_play(scene, FadeIn(outlier, scale=1.5), FadeIn(warning), run_time=1.0)
    paced_play(scene, GrowArrow(tug), Transform(mean_marker, pulled_mean), Transform(median_marker, stable_median), run_time=1.55)
    paced_play(scene, Indicate(mean_marker, color=cfg.ORANGE), Indicate(median_marker, color=cfg.WHITE), run_time=1.0)

    inspect = VGroup(
        label_pill("data error?", cfg.RED, font_size=21),
        label_pill("rare real case?", cfg.GOLD, font_size=21),
        label_pill("future risk?", cfg.PURPLE, font_size=21),
    ).arrange(RIGHT, buff=0.28).move_to(DOWN * 2.05)
    inspect_title = Text("inspect before training", font_size=27, color=cfg.ORANGE, weight=BOLD).next_to(inspect, UP, buff=0.16)
    inspect_title.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    paced_play(scene, FadeIn(inspect_title, shift=UP * 0.1), LaggedStart(*[FadeIn(item, scale=0.95) for item in inspect], lag_ratio=0.16), run_time=1.15)

    caption = VGroup(
        Text("Outliers are not mistakes by default.", font_size=29, color=cfg.WHITE, weight=BOLD),
        Text("They are signals to inspect.", font_size=29, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.08)
    caption.set_stroke("#02111D", width=4, opacity=0.85, background=True)
    caption.to_edge(DOWN, buff=0.36)
    paced_play(scene, FadeIn(caption, shift=UP * 0.16), run_time=0.95)
    narration_wait(scene, 0.8)
    end_scene(scene, scene_start)
