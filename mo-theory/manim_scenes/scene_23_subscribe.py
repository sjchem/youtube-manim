"""Chapter 23 — a separate closing subscribe card, in the channel's house style.

Two computed orbitals keep turning beside the card: the sigma bond that holds
molecules together and the pi* orbital that makes oxygen magnetic.
"""

from manim_scenes.common import *


class Scene23Subscribe(Scene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "23")
    card = subscribe_card()
    glow = halo(4.2, cfg.CYAN, layers=6, peak_opacity=0.06).move_to(card)
    left = Stage([-5.9, 0.0, 0], zoom=0.55, yaw=0.4, pitch=0.3, spin=0.45)
    MOCloud(left, om.MOSpec("s", 1.0, om.R_S))
    right = Stage([5.9, 0.0, 0], zoom=0.26, yaw=0.4, pitch=0.35, spin=-0.4)
    MOCloud(right, om.MOSpec("py", -1.0, om.R_P))
    for st in (left, right):
        st.presence = 0.0
        scene.add(st)
    scene.play(FadeIn(glow), FadeIn(card.thank_you, shift=DOWN * 0.15), run_time=0.6)
    scene.play(FadeIn(card.subscribe, scale=1.12), Create(card.rule), left.fade(left, 1.0), right.fade(right, 1.0),
               run_time=0.8)
    scene.play(FadeIn(card.tagline, shift=UP * 0.15), run_time=0.7)
    cue(scene, t, 5.0)
    scene.play(Indicate(card.subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["23"])
