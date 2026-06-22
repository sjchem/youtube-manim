"""Scene 1: the visual illusion of the curling free kick."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene,
    cinematic_background,
    end_scene,
    expected_and_curved_paths,
    goal_top_view,
    narration_wait,
    path_arrow_tip,
    paced_play,
    pitch_top_view,
    title_stack,
    trionda_image_ball,
)


class Scene01Hook(Scene):
    """Cold open: the straight path misses, the real path bends inside."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())
    title = title_stack("The ball is already gone.", "So how does it turn?")
    title.to_edge(UP, buff=0.18)
    title[2].set_color(cfg.CYAN).set_opacity(0.9)
    paced_play(scene, FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

    pitch = pitch_top_view().scale(0.86).shift(DOWN * 0.62)
    pitch[0].set_fill("#1F8F58", opacity=0.92).set_stroke("#8DE6A3", opacity=0.42, width=2.5)
    for index, band in enumerate(pitch[1]):
        band.set_fill("#32B36F" if index % 2 == 0 else "#167A4D", opacity=0.18)
    goal_center = np.array([5.8, -0.62, 0])
    goal = goal_top_view(width=2.4, depth=0.85).move_to(goal_center)
    ball = trionda_image_ball(width=0.52).move_to([-5.7, -1.65, 0])
    lower_post = goal_center + DOWN * 1.2
    post_flash = Circle(radius=0.09, color=cfg.WHITE, fill_color=cfg.WHITE, fill_opacity=0.9).move_to(lower_post)
    miss_path, curve_path = expected_and_curved_paths()
    miss_tip = path_arrow_tip(miss_path, cfg.RED, scale=0.22)
    curve_tip = path_arrow_tip(curve_path, cfg.GREEN, scale=0.22)

    scene.add(pitch)
    scene.bring_to_front(title)
    paced_play(scene, Create(goal), FadeIn(ball, scale=0.8), run_time=0.7)

    expected_main = Text("expected", font_size=38, color=cfg.RED, weight=BOLD)
    expected_main.set_stroke("#2B0808", width=4, opacity=0.95, background=True)
    expected_shadow = expected_main.copy().set_color("#060A0D").set_opacity(0.78).shift(RIGHT * 0.07 + DOWN * 0.07)
    expected_glow = expected_main.copy().set_color(cfg.ORANGE).set_opacity(0.20).scale(1.12)
    miss_label = VGroup(expected_shadow, expected_glow, expected_main).next_to(miss_path, DOWN, buff=0.18)
    paced_play(scene, Create(miss_path), FadeIn(miss_tip), FadeIn(miss_label), run_time=1.2)
    paced_play(scene, Flash(post_flash, color=cfg.RED, flash_radius=0.42), run_time=0.5)
    narration_wait(scene, 0.45)

    actual_main = Text("actual", font_size=46, color=cfg.GOLD, weight=BOLD)
    actual_main.set_stroke("#06251D", width=5, opacity=0.95, background=True)
    actual_shadow = actual_main.copy().set_color("#031C14").set_opacity(0.96).shift(RIGHT * 0.09 + DOWN * 0.09)
    actual_glow = actual_main.copy().set_color(cfg.WHITE).set_opacity(0.20).scale(1.14)
    curve_label = VGroup(actual_shadow, actual_glow, actual_main).move_to([3.22, 0.58, 0])
    paced_play(
        scene,
        Create(curve_path),
        FadeIn(curve_tip),
        MoveAlongPath(ball, curve_path),
        FadeOut(miss_label),
        FadeIn(curve_label),
        run_time=2.4,
    )
    paced_play(scene, Indicate(goal, color=cfg.GREEN, scale_factor=1.02), run_time=0.55)

    core = Text("Spin turns air into steering.", font_size=36, color=cfg.WHITE, weight=BOLD)
    core.to_edge(DOWN, buff=0.42)
    paced_play(scene, FadeIn(core, shift=UP * 0.15), run_time=0.7)

    end_card_title = Text("Why the World Cup Ball Curves in Mid-Air ?", font_size=43, color=cfg.WHITE, weight=BOLD)
    end_card_subtitle = Text("The Magnus Effect", font_size=38, color=cfg.CYAN, weight=BOLD)
    end_rule = Line(LEFT * 5.3, RIGHT * 5.3, color=cfg.CYAN, stroke_width=4)
    end_card = VGroup(end_card_title, end_rule, end_card_subtitle).arrange(DOWN, buff=0.24).move_to(ORIGIN)
    end_shadow = end_card.copy().set_color("#031C28").set_opacity(0.72).shift(RIGHT * 0.08 + DOWN * 0.08)
    final_title = VGroup(end_shadow, end_card)

    paced_play(
        scene,
        FadeOut(title, pitch, goal, ball, miss_path, miss_tip, curve_path, curve_tip, curve_label, core),
        run_time=0.75,
    )
    paced_play(scene, FadeIn(final_title, shift=UP * 0.2), run_time=0.8)
    narration_wait(scene, 1.0)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["01"])
