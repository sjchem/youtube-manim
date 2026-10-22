"""Chapter 22 — a separate closing subscribe card, in the channel's house style."""

from manim_scenes.common import *


class Scene22Subscribe(Scene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "22")
    card = subscribe_card()
    glow = halo(4.2, cfg.CYAN, layers=6, peak_opacity=0.06).move_to(card)
    left, _ = mini_model("CH4", [-5.7, 0.0, 0], zoom=0.62, spin=0.45)
    water = ml.molecule("H2O")
    right = Stage([5.7, 0.2, 0], zoom=0.62, yaw=0.0, pitch=0.2, spin=-0.4)
    MoleculeModel(right, water)
    right.presence = 0.0
    scene.add(left, right)
    scene.play(FadeIn(glow), FadeIn(card.thank_you, shift=DOWN * 0.15), run_time=0.6)
    scene.play(FadeIn(card.subscribe, scale=1.12), Create(card.rule), left.fade(left, 1.0), right.fade(right, 1.0),
               run_time=0.8)
    scene.play(FadeIn(card.tagline, shift=UP * 0.15), run_time=0.7)
    cue(scene, t, 5.0)
    scene.play(Indicate(card.subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["22"])
