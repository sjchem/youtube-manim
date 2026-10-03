"""Scene 16: a separate closing subscribe card, in the channel's house style."""

from manim_scenes.common import *


class Scene16Subscribe(ThreeDScene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: ThreeDScene) -> None:
    t, _ = start(scene, "16")
    card = subscribe_card()
    glow = halo(4.2, cfg.CYAN, layers=6, peak_opacity=0.06).move_to(card)
    shapes = VGroup(*[present_3d(family_orbital(letter, 0.34 if letter != "s" else 0.26, small=True)) for letter in "spdf"])
    shapes.arrange(RIGHT, buff=1.0).next_to(card, DOWN, buff=0.5)
    for shape in shapes:
        spin_forever(shape, 0.5)

    scene.play(FadeIn(glow), FadeIn(card.thank_you, shift=DOWN * 0.15), run_time=0.6)
    scene.play(FadeIn(card.subscribe, scale=1.12), Create(card.rule), run_time=0.8)
    scene.play(FadeIn(card.tagline, shift=UP * 0.15), LaggedStart(*[FadeIn(s, scale=0.5) for s in shapes], lag_ratio=0.2),
               run_time=1.0)
    cue(scene, t, 5.0)
    scene.play(Indicate(card.subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["16"])
