"""Chapter 19: a separate, staged channel call to action.

Adapt the supplied card to QuantumScene's clock and background lifecycle. In a
continuous render the recap leaves first; the thank-you, subscribe word, rule
and tagline then arrive in order, with one gentle emphasis on subscribe.
"""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import QuantumScene, outlined_text


class Scene19Subscribe(QuantumScene):
    """Close with thanks and the physics, chemistry and mathematics tagline."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("19")

    # -- Beat 1: clear the recap while keeping the cinematic background ------
    scene.dissolve(VGroup(), seconds=0.55)
    thank_you = outlined_text("THANK YOU FOR WATCHING", 34, cfg.CYAN)
    subscribe = outlined_text("SUBSCRIBE", 72, cfg.GOLD)
    subscribe.set_stroke("#351F05", width=3, opacity=0.75, background=True)
    rule = Line(LEFT * 2.8, RIGHT * 2.8, color=cfg.CYAN, stroke_width=6)
    tagline = VGroup(
        outlined_text("Stay curious.", 38, cfg.WHITE),
        outlined_text("Keep following the physics, chemistry and mathematics.", 34, cfg.WHITE),
    ).arrange(DOWN, buff=0.18)
    if tagline.width > cfg.SAFE_WIDTH:
        tagline.scale_to_fit_width(cfg.SAFE_WIDTH)
    card = VGroup(thank_you, subscribe, rule, tagline).arrange(DOWN, buff=0.30).move_to(ORIGIN)

    scene.playq(FadeIn(thank_you, shift=DOWN * 0.15), seconds=0.55)
    scene.playq(FadeIn(subscribe, scale=1.12), Create(rule), seconds=0.7)
    scene.at(5)

    # -- Beat 2: the channel promise, then one restrained invitation ---------
    scene.playq(FadeIn(tagline, shift=UP * 0.15), seconds=0.55)
    scene.adopt(thank_you, subscribe, rule, tagline)
    scene.hold(1.0)
    scene.playq(Indicate(subscribe, color=cfg.WHITE, scale_factor=1.04), seconds=0.65)
    scene.at(13.5)
    scene.dissolve(VGroup(), seconds=0.8)
    scene.finish()
