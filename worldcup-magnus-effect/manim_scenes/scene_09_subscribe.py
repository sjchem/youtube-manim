"""Scene 9: a separate closing subscribe card."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, narration_wait, paced_play


class Scene09Subscribe(Scene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())

    thank_you = Text("THANK YOU FOR WATCHING", font_size=34, color=cfg.CYAN, weight=BOLD)
    subscribe = Text("SUBSCRIBE", font_size=72, color=cfg.GOLD, weight=BOLD)
    subscribe.set_stroke("#351F05", width=3, opacity=0.75, background=True)
    rule = Line(LEFT * 2.8, RIGHT * 2.8, color=cfg.CYAN, stroke_width=6)
    tagline = VGroup(
        Text("Stay curious.", font_size=38, color=cfg.WHITE, weight=BOLD),
        Text("Keep following the physics and mathematics.", font_size=34, color=cfg.WHITE, weight=BOLD),
    ).arrange(DOWN, buff=0.08)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.25).move_to(ORIGIN)
    card.set_stroke("#06131B", width=4, opacity=0.9, background=True)

    paced_play(scene, FadeIn(thank_you, shift=DOWN * 0.15), run_time=0.55)
    paced_play(scene, FadeIn(subscribe, scale=1.12), Create(rule), run_time=0.7)
    paced_play(scene, FadeIn(tagline, shift=UP * 0.15), run_time=0.55)
    narration_wait(scene, 1.0)
    paced_play(scene, Indicate(subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=0.65)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["04"])
