"""Scene 09 — Subscribe card.

A separate closing card with channel call-to-action.
Narration cue: ~12 seconds
"""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, cinematic_background, end_scene, narration_wait, paced_play,
)


class Scene09Subscribe(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=True))

    thank_you = Text(
        "THANK YOU FOR WATCHING",
        font_size=36, color=cfg.CYAN, weight=BOLD,
    )

    subscribe = Text(
        "SUBSCRIBE",
        font_size=82, color=cfg.GOLD, weight=BOLD,
    )
    subscribe.set_stroke(cfg.COLORS["panel"], width=4, opacity=0.80, background=True)

    rule = Line(LEFT * 3.2, RIGHT * 3.2, color=cfg.CYAN, stroke_width=6)

    tagline = VGroup(
        Text("Stay curious.", font_size=40, color=cfg.WHITE, weight=BOLD),
        Text("Follow the maths. Follow the data.", font_size=34, color=cfg.WHITE),
    ).arrange(DOWN, buff=0.10)

    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.28)
    card.move_to(ORIGIN)

    for mob in card:
        if hasattr(mob, "set_stroke"):
            mob.set_stroke(cfg.BG, width=3, background=True)

    paced_play(scene, FadeIn(thank_you, shift=DOWN * 0.15), run_time=0.55)
    paced_play(scene, FadeIn(subscribe, scale=1.10), Create(rule), run_time=0.70)
    paced_play(scene, FadeIn(tagline, shift=UP * 0.15), run_time=0.55)
    narration_wait(scene, 0.9)
    paced_play(
        scene,
        Indicate(subscribe, color=cfg.WHITE, scale_factor=1.05),
        run_time=0.65,
    )
    narration_wait(scene, 1.0)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["09"])
