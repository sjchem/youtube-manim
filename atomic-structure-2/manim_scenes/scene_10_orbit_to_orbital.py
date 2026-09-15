"""Chapter 10: two extra letters, and a completely different physics.

Orbit and orbital are not synonyms, and this chapter is built so the difference
is impossible to miss: the two ideas are put side by side, then the word itself
is transformed on screen while the object under it changes from a path to a
distribution.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    density_slice,
    orbit,
    outlined_text,
)

from manim_scenes.uncertainty_visuals import OrbitMotion

LEFT_X, RIGHT_X = -3.7, 3.7
COMPARISON_FONT_SIZE = 48
MERGED_FONT_SIZE = 60


def _start_push_in(picture: ImageMobject, target_height: float,
                   seconds: float) -> None:
    """Change only the viewing scale of a fixed density during a narration hold."""
    initial_height = picture.height
    picture.framing_elapsed = 0.0

    def advance(mob: ImageMobject, dt: float) -> None:
        mob.framing_elapsed += dt * cfg.SPEED
        fraction = np.clip(mob.framing_elapsed / seconds, 0.0, 1.0)
        eased = 0.5 - 0.5 * np.cos(PI * fraction)
        mob.height = initial_height + (target_height - initial_height) * eased

    picture.add_updater(advance)



class Scene10OrbitToOrbital(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("10")

    # -- Beat 1: the two ideas, side by side ----------------------------------
    classical = orbit(1.75, nucleus_radius=0.20, electron_radius=0.15).shift(RIGHT * LEFT_X)
    # Keep the classical marker moving through both the explanations and fades.
    rotation = OrbitMotion(classical)
    scene.add(rotation)
    scene.dissolve(classical, seconds=2.0)

    orbit_word = scene.pin(outlined_text("ORBIT", COMPARISON_FONT_SIZE, cfg.MUTED).move_to([LEFT_X, 2.65, 0]))
    orbit_gloss = scene.pin(outlined_text("a path", cfg.FONT["small"], cfg.MUTED).move_to([LEFT_X, -2.85, 0]))
    scene.playq(FadeIn(orbit_word), FadeIn(orbit_gloss), seconds=0.8)

    quantum = density_slice(1, 0, 0, size=3.9).shift(RIGHT * RIGHT_X)
    _start_push_in(quantum, target_height=4.15, seconds=42.0)
    scene.show(quantum, seconds=1.6)
    orbital_word = scene.pin(outlined_text("ORBITAL", COMPARISON_FONT_SIZE, cfg.CYAN).move_to([RIGHT_X, 2.65, 0]))
    orbital_gloss = scene.pin(outlined_text("a one-electron spatial state", cfg.FONT["small"], cfg.CYAN).move_to([RIGHT_X, -2.85, 0]))
    scene.playq(FadeIn(orbital_word), FadeIn(orbital_gloss), seconds=0.8)

    # -- Beat 2: the marker goes round; the distribution simply is ------------
    # The independent driver also runs during this and the longer narrated hold.
    scene.hold(5.0)
    scene.at(26)

    tracker_note = scene.pin(outlined_text("no route between one detection and the next",
                                           cfg.FONT["small"], cfg.GOLD).move_to([0, -3.55, 0]))
    scene.playq(FadeIn(tracker_note), seconds=0.7)
    scene.playq(FadeOut(classical[2], scale=2.4), seconds=1.4)
    rotation.clear_updaters()
    scene.remove(rotation)
    scene.playq(classical[1].animate.set_stroke(opacity=0.20), seconds=1.8)
    scene.at(39)
    scene.drop(tracker_note, orbit_gloss, orbital_gloss, seconds=0.6)

    # -- Beat 3: the word itself changes --------------------------------------
    merged = outlined_text("ORBITAL", MERGED_FONT_SIZE, cfg.CYAN).move_to(UP * 2.5)
    scene.add_fixed_in_frame_mobjects(merged)
    scene.remove(merged)
    # Move one intact word first. Matching two words while both cross the
    # frame superimposes letters; align the ORBIT prefix before adding AL.
    prefix = outlined_text("ORBIT", MERGED_FONT_SIZE, cfg.CYAN)
    prefix.move_to(merged).align_to(merged, LEFT)
    scene.playq(FadeOut(orbital_word), seconds=0.4)
    scene.playq(Transform(orbit_word, prefix), seconds=0.6)
    scene.playq(TransformMatchingShapes(orbit_word, merged), seconds=0.6)
    scene.remove_fixed_in_frame_mobjects(orbit_word, orbital_word)
    for word in (orbit_word, orbital_word):
        if word in scene.local:
            scene.local.remove(word)
    scene.local.append(merged)

    # -- Beat 4: the state takes the whole frame ------------------------------
    scene.local.remove(quantum)
    scene.drop(scene.anchor, seconds=0.6)
    scene.anchor = quantum
    # Pause framing while the composition changes, then resume a restrained
    # push-in. No pixel intensities or probability values are animated.
    quantum.clear_updaters()
    scene.playq(quantum.animate.move_to(DOWN * 0.40).set_height(4.3), seconds=2.4)
    _start_push_in(quantum, target_height=4.55, seconds=32.0)
    scene.at(55)
    scene.drop(merged, seconds=0.6)

    approximate = scene.pin(outlined_text("for many electrons, an approximate building block",
                                          cfg.FONT["tiny"], cfg.MUTED).move_to([0, 3.45, 0]))
    scene.playq(FadeIn(approximate), seconds=0.7)
    scene.at(62)
    scene.drop(approximate, seconds=0.6)

    # The pivot of the whole film: light the station we have just reached.
    scene.spine(3, hold=2.0)

    scene.finish()
    quantum.clear_updaters()
