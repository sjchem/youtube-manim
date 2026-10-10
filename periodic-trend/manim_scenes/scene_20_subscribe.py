"""Scene 20: a separate closing subscribe card, in the channel's house style."""

from manim_scenes.common import *


class Scene20Subscribe(Scene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "20")
    card = subscribe_card()
    glow = halo(4.2, cfg.CYAN, layers=6, peak_opacity=0.06).move_to(card)
    atoms = VGroup(Atom(0.95, [-6.4, 0.0, 0], charge=None, core=0.3, count=260, seed=201),
                   Atom(0.6, [6.4, 0.0, 0], charge=None, core=0.18, count=260, seed=202))

    scene.play(FadeIn(glow), FadeIn(card.thank_you, shift=DOWN * 0.15), run_time=0.6)
    scene.play(FadeIn(card.subscribe, scale=1.12), Create(card.rule), FadeIn(atoms, scale=0.6), run_time=0.8)
    scene.play(FadeIn(card.tagline, shift=UP * 0.15), run_time=0.7)
    cue(scene, t, 5.0)
    scene.play(Indicate(card.subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["20"])
