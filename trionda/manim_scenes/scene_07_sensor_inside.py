from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    cutaway_layers,
    data_pulses,
    end_scene,
    narration_wait,
    paced_play,
    scene_caption,
    sensor_chip,
    small_label,
)
from utils.math_utils import hz_to_period_ms


class Scene07SensorInside(MovingCameraScene):
    """Show connected ball technology inside one panel."""

    def construct(self) -> None:
        construct_scene_07(self)


def construct_scene_07(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    caption = scene_caption("The sensor is in one panel, not floating at center", color=cfg.GOLD)
    cutaway = cutaway_layers(radius=1.85).shift(LEFT * 3.3 + UP * 0.2)
    chip = sensor_chip().scale(0.72).move_to(cutaway[4])
    panel_label = small_label("500 Hz IMU layer", cfg.GOLD, 32).next_to(chip, UP + RIGHT, buff=0.25)
    panel_arrow = Arrow(panel_label.get_left(), chip.get_center(), color=cfg.GOLD, stroke_width=4, buff=0.08)

    weights = VGroup()
    for point in [RIGHT * 2.7 + UP * 1.1, RIGHT * 3.75 + DOWN * 0.15, RIGHT * 2.35 + DOWN * 1.45]:
        weights.add(Circle(radius=0.22, color=cfg.GREEN, fill_color=cfg.GREEN, fill_opacity=0.35).move_to(point))
    weight_label = VGroup(
        small_label("counter-balances", cfg.GREEN, 25),
        small_label("preserve rotation", cfg.GREEN, 25),
    ).arrange(DOWN, buff=0.04).next_to(weights, DOWN, buff=0.28)

    pulses = data_pulses(18, color=cfg.CYAN).scale(1.15).move_to(RIGHT * 2.7 + UP * 2.35)
    pulse_label = VGroup(
        Text("500 samples each second", font_size=36, color=cfg.CYAN, weight=BOLD),
        Text(f"one sample every {hz_to_period_ms(500):.1f} ms", font_size=28, color=cfg.WHITE),
    ).arrange(DOWN, buff=0.06).next_to(pulses, UP, buff=0.22)
    pulse_label.set_stroke(cfg.BLACKISH, width=3, opacity=0.86, background=True)

    signal = Arrow(chip.get_right(), pulses.get_left(), color=cfg.CYAN, stroke_width=4, max_tip_length_to_length_ratio=0.08)
    var_box = RoundedRectangle(width=2.25, height=0.9, corner_radius=0.1, color=cfg.CYAN, fill_color=cfg.PANEL, fill_opacity=0.75)
    var_text = Text("VAR data", font_size=34, color=cfg.WHITE, weight=BOLD).move_to(var_box)
    var_group = VGroup(var_box, var_text).move_to(RIGHT * 6.35 + DOWN * 2.35)
    signal2 = Arrow(pulses.get_bottom(), var_group.get_top(), color=cfg.CYAN, stroke_width=4, max_tip_length_to_length_ratio=0.08)

    paced_play(scene, FadeIn(caption), FadeIn(cutaway), run_time=0.85)
    paced_play(scene, ReplacementTransform(cutaway[4].copy(), chip), FadeIn(panel_label), GrowArrow(panel_arrow), run_time=0.8)
    paced_play(scene, FadeIn(weights, scale=0.9), FadeIn(weight_label, shift=DOWN * 0.12), run_time=0.75)
    paced_play(scene, LaggedStart(*[FadeIn(dot, scale=1.6) for dot in pulses], lag_ratio=0.045), FadeIn(pulse_label), GrowArrow(signal), run_time=1.05)
    paced_play(scene, pulses.animate.shift(RIGHT * 0.18), rate_func=there_and_back, run_time=0.65)
    paced_play(scene, FadeIn(var_group, shift=UP * 0.15), GrowArrow(signal2), run_time=0.75)
    narration_wait(scene, 0.8)
    end_scene(scene, scene_start, "07")
