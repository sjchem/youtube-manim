"""Scene 13: a separate closing subscribe card, in the channel's house style."""

from manim_scenes.common import *


class Scene13Subscribe(ThreeDScene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: ThreeDScene) -> None:
    t, _ = start(scene, "13")
    card = subscribe_card().shift(UP * 0.45)
    glow = halo(4.2, cfg.CYAN, layers=6, peak_opacity=0.06).move_to(card)
    row = VGroup(*[txt(str(c), cfg.FONT["body"], cfg.GOLD) for c in mu.coefficients(5)]).arrange(RIGHT, buff=0.55)
    row.next_to(card, DOWN, buff=0.55)

    scene.play(FadeIn(glow), FadeIn(card.thank_you, shift=DOWN * 0.15), run_time=0.6)
    scene.play(FadeIn(card.subscribe, scale=1.12), Create(card.rule), run_time=0.8)
    scene.play(FadeIn(card.tagline, shift=UP * 0.15), LaggedStart(*[FadeIn(x, scale=0.6) for x in row], lag_ratio=0.15),
               run_time=1.0)
    cue(scene, t, 5.0)
    scene.play(Indicate(card.subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["13"])
