"""Scene 21 — a separate closing subscribe card, in the channel's house style.

Two small turning glasses of the reference solution keep moving beside the
card: one outlined in purple (per litre of solution), one with its solvent
lit (per kilogram of solvent).
"""

from manim_scenes.common import *


class Scene21Subscribe(Scene):
    """Close with a concise channel call to action."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "21")
    card = subscribe_card()
    glow = halo(4.2, cfg.CYAN, layers=6, peak_opacity=0.06).move_to(card)
    left, lglass, lswarm = solution_stage([-6.0, -1.6, 0], zoom=0.62, solvent=220, solute=3, seed=21, spin=0.3)
    right, rglass, rswarm = solution_stage([6.0, -1.6, 0], zoom=0.62, solvent=220, solute=3, seed=22, spin=-0.3)
    lglass.glow = 1.0
    rswarm.solvent_glow = 1.0
    for st in (left, right):
        st.presence = 0.0
        scene.add(st)
    scene.play(FadeIn(glow), FadeIn(card.thank_you, shift=DOWN * 0.15), run_time=0.6)
    scene.play(FadeIn(card.subscribe, scale=1.12), Create(card.rule), left.fade(left, 1.0), right.fade(right, 1.0),
               run_time=0.8)
    scene.play(FadeIn(card.tagline, shift=UP * 0.15), run_time=0.7)
    cue(scene, t, 5.0)
    scene.play(Indicate(card.subscribe, color=cfg.WHITE, scale_factor=1.04), run_time=0.8)
    end_scene(scene, t, cfg.SCENE_DURATIONS["21"])
