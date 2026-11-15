"""Scene 30 — the channel's closing card: thank you, subscribe, stay curious."""

from manim_scenes.common import *


class Scene30Subscribe(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "30")
    card = subscribe_card()
    scene.play(FadeIn(card.thank_you, shift=DOWN * 0.2), run_time=0.8)
    scene.play(FadeIn(card.subscribe, scale=1.12), Create(card.rule), run_time=1.0)
    scene.play(FadeIn(card.tagline, shift=UP * 0.2), run_time=0.8)
    scene.play(Indicate(card.subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=1.0)
    finish(scene, t, fill=lambda s: [card.rule.animate.set_stroke(opacity=0.5)])
