"""Scene 18: a separate closing subscribe card, in the channel's house style."""

from manim_scenes.common import *


class Scene18Subscribe(Scene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "18")
    card = subscribe_card()
    glow = halo(4.2, cfg.CYAN, layers=6, peak_opacity=0.06).move_to(card)
    gap = 1.5
    molecule = bind_pair(PairCloud(LEFT, RIGHT, 0.9, count=360, seed=181, share=1.0, glow=0.14), lambda: gap, [-5.9, 0.0, 0])
    salt = rock_salt_crystal(1, 0.7, [5.9, 0.0, 0], cation=0.15, anion=0.24, spin=0.3)

    scene.play(FadeIn(glow), FadeIn(card.thank_you, shift=DOWN * 0.15), run_time=0.6)
    scene.add(molecule)
    nuclei = pair_nuclei(molecule, ("+", "+"), radius=0.17)
    scene.play(FadeIn(card.subscribe, scale=1.12), Create(card.rule), FadeIn(molecule), FadeIn(nuclei), FadeIn(salt, scale=0.6),
               run_time=0.8)
    scene.play(FadeIn(card.tagline, shift=UP * 0.15), run_time=0.7)
    cue(scene, t, 5.0)
    scene.play(Indicate(card.subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["18"])
