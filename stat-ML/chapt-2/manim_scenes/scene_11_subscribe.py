"""Scene 11: Subscribe card."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import cinematic_background


class Scene11Subscribe(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background(show_bubbles=True))

    thank_you = Text(
        "THANK YOU FOR WATCHING",
        font_size=36,
        color=cfg.CYAN,
        weight=BOLD,
    )

    subscribe = Text(
        "SUBSCRIBE",
        font_size=82,
        color=cfg.GOLD,
        weight=BOLD,
    )
    subscribe.set_stroke(cfg.COLORS["panel"], width=4, opacity=0.8, background=True)

    rule = Line(LEFT * 3.2, RIGHT * 3.2, color=cfg.CYAN, stroke_width=6)

    tagline = VGroup(
        Text("Stay curious.", font_size=40, color=cfg.WHITE, weight=BOLD),
        Text("Follow the math. Follow the data.", font_size=34, color=cfg.WHITE),
    ).arrange(DOWN, buff=0.1)

    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.34)
    card.move_to(ORIGIN)

    for mob in card:
        if hasattr(mob, "set_stroke"):
            mob.set_stroke(cfg.BG, width=3, background=True)

    scene.play(FadeIn(thank_you, shift=DOWN * 0.15), run_time=0.55)
    scene.play(FadeIn(subscribe, scale=1.1), Create(rule), run_time=0.7)
    scene.play(FadeIn(tagline, shift=UP * 0.15), run_time=0.55)
    scene.wait(3.5)
    scene.play(
        Indicate(subscribe, color=cfg.WHITE, scale_factor=1.05),
        run_time=0.65,
    )
    scene.wait(9.0)
    scene.play(FadeOut(card), run_time=1.25)
    scene.wait(0.25)
