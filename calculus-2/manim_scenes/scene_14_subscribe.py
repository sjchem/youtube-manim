"""Scene 14: a separate closing subscribe card."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    end_scene,
    narration_wait,
    outlined_text,
    paced_play,
)


class Scene14Subscribe(Scene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "14")
    add_cinematic_background(scene)

    thank_you = outlined_text("THANK YOU FOR WATCHING", cfg.FONT["body"], cfg.CYAN, BOLD)
    subscribe = outlined_text("SUBSCRIBE", cfg.FONT["hero"], cfg.GOLD, BOLD)
    rule = Line(LEFT * 2.8, RIGHT * 2.8, color=cfg.CYAN, stroke_width=6)
    tagline = VGroup(
        outlined_text("Stay curious.", cfg.FONT["body"], cfg.WHITE, BOLD),
        outlined_text("Two sides of the same idea.", cfg.FONT["small"], cfg.WHITE, BOLD),
    ).arrange(DOWN, buff=0.12)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.28).move_to(ORIGIN)

    paced_play(scene, FadeIn(thank_you, shift=DOWN * 0.15), run_time=0.55)
    paced_play(scene, FadeIn(subscribe, scale=1.12), Create(rule), run_time=0.75)
    paced_play(scene, FadeIn(tagline, shift=UP * 0.15), run_time=0.55)
    narration_wait(scene, 11.0)
    paced_play(scene, Indicate(subscribe, color=cfg.WHITE, scale_factor=1.05), run_time=0.7)

    end_scene(scene, started, cfg.SCENE_DURATIONS["14"])
