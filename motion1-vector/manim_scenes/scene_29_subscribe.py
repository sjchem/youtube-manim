"""Scene 29 — the channel's closing card."""

from manim_scenes.common import *


class Scene29Subscribe(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "29")
    card = subscribe_card()
    scene.play(FadeIn(card.thank_you, shift=DOWN * 0.2), run_time=0.8)
    scene.play(FadeIn(card.subscribe, scale=0.9), Create(card.rule), run_time=1.2)
    scene.play(FadeIn(card.tagline, shift=UP * 0.2), run_time=1.0)
    scene.play(Indicate(card.subscribe, color=cfg.GOLD, scale_factor=1.06), run_time=1.4)
    scene.wait(1.6)
    end_scene(scene, t, cfg.SCENE_DURATIONS["29"])
