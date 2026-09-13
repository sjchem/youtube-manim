"""Scene 13: Bohr's atom works beautifully, and it is still not a picture of an atom."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    cross_mark,
    end_scene,
    fit_width,
    narration_wait,
    outlined_text,
    paced_play,
    planetary_atom,
    top_caption,
)

LIMITS = (
    "spectra of bigger atoms",
    "fine detail inside each line",
    "lines that split in a field",
    "why atoms bond at all",
)
ORBIT_RADIUS = 2.30
WAVE_NUMBER = 4


def _standing_wave(radius: float, amplitude: float, lobes: int = WAVE_NUMBER, color: str = cfg.PURPLE) -> ParametricFunction:
    """The orbit with a wave wrapped around it: a whole number of lobes, or nothing."""
    return ParametricFunction(
        lambda t: (radius + amplitude * np.sin(lobes * t)) * np.array([np.cos(t), np.sin(t), 0.0]),
        t_range=[0, TAU],
        color=color,
        stroke_width=5,
    )


class Scene13NotAnOrbit(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "13")
    add_cinematic_background(scene)

    # -- Beat 1: look very closely at the track ---------------------------------
    atom, core, ring, bead = planetary_atom(
        orbit_radius=ORBIT_RADIUS, nucleus_radius=0.30, electron_radius=0.19
    )
    paced_play(scene, FadeIn(atom, scale=1.1), run_time=1.1)
    paced_play(scene, Rotating(bead, angle=TAU * 0.6, about_point=ORIGIN, axis=OUT), run_time=3.4, rate_func=linear)

    question = top_caption("IS THIS REALLY WHAT AN ATOM LOOKS LIKE?", cfg.GOLD)
    paced_play(scene, FadeIn(question), run_time=0.9)
    narration_wait(scene, 3.0)
    paced_play(scene, FadeOut(question), run_time=0.6)
    narration_wait(scene, 5.8)

    zoom = Circle(radius=0.62, color=cfg.WHITE, stroke_width=3, stroke_opacity=0.7).move_to(bead.get_center())
    paced_play(scene, Create(zoom), run_time=0.8)
    paced_play(scene, VGroup(atom, zoom).animate.scale(1.55).shift(-bead.get_center() * 0.55), run_time=2.2)
    narration_wait(scene, 3.6)

    # -- Beat 2: the honest answer ---------------------------------------------
    no = outlined_text("no.", cfg.FONT["hero"], cfg.RED).move_to([0, -1.9, 0])
    paced_play(scene, FadeOut(zoom), run_time=0.4)
    paced_play(scene, atom.animate.scale(0.45).move_to([0, 0.7, 0]).fade(0.65), run_time=1.0)
    paced_play(scene, FadeIn(no, scale=1.3), run_time=0.9)
    narration_wait(scene, 4.0)
    paced_play(scene, FadeOut(no), run_time=0.6)

    # -- Beat 3: where the model runs out --------------------------------------
    paced_play(scene, FadeOut(atom), run_time=0.6)
    listing = top_caption("WHERE BOHR'S ATOM RUNS OUT", cfg.ORANGE)
    paced_play(scene, FadeIn(listing), run_time=0.7)

    rows = VGroup()
    for text in LIMITS:
        mark = cross_mark(0.17, cfg.RED)
        label = outlined_text(text, 34, "#EBD9B4", BOLD)
        rows.add(VGroup(mark, label).arrange(RIGHT, buff=0.42))
    rows.arrange(DOWN, buff=0.62, aligned_edge=LEFT).move_to([0, 0.15, 0])
    fit_width(rows, cfg.SAFE_WIDTH - 0.6)

    for row in rows:
        paced_play(scene, FadeIn(row, shift=RIGHT * 0.18), run_time=0.8)
        narration_wait(scene, 3.0)

    works = bottom_caption("works best for hydrogen and other one-electron systems", cfg.GOLD)
    paced_play(scene, FadeIn(works), run_time=0.8)
    narration_wait(scene, 9.6)
    paced_play(scene, FadeOut(rows, works, listing), run_time=0.7)

    # -- Beat 4: the deeper trouble --------------------------------------------
    deeper_2 = outlined_text("the electron also shows", cfg.FONT["title"], cfg.PURPLE)
    deeper_3 = outlined_text("wave-like behaviour", cfg.FONT["title"], cfg.PURPLE)
    stack = VGroup(deeper_2, deeper_3).arrange(DOWN, buff=0.44).move_to([0, 0.35, 0])
    for line in stack:
        fit_width(line, cfg.SAFE_WIDTH - 0.4)
    paced_play(scene, FadeIn(deeper_2, scale=1.06), run_time=0.9)
    narration_wait(scene, 2.6)
    paced_play(scene, FadeIn(deeper_3, scale=1.06), run_time=0.9)
    narration_wait(scene, 5.1)
    paced_play(scene, FadeOut(stack), run_time=0.7)

    # -- Beat 5: the bead stretches into a wave --------------------------------
    _atom_2, core_2, ring_2, bead_2 = planetary_atom(
        orbit_radius=ORBIT_RADIUS, nucleus_radius=0.26, electron_radius=0.19
    )
    paced_play(scene, FadeIn(core_2), FadeIn(ring_2), FadeIn(bead_2, scale=1.3), run_time=1.0)

    amplitude = ValueTracker(0.0)
    wave = always_redraw(lambda: _standing_wave(ORBIT_RADIUS, amplitude.get_value()))
    scene.add(wave)
    paced_play(scene, FadeOut(bead_2, scale=2.6), run_time=1.0)
    paced_play(scene, amplitude.animate.set_value(0.46), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
    smear = bottom_caption("wave analogy: not an electron trajectory", cfg.PURPLE)
    paced_play(scene, FadeIn(smear), run_time=0.8)
    paced_play(scene, ring_2.animate.set_stroke(opacity=0.12), run_time=1.6)
    narration_wait(scene, 4.4)

    wave.clear_updaters()
    end_scene(scene, started, cfg.SCENE_DURATIONS["13"])
