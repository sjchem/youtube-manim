"""Chapter 5: individual detections build an interference pattern.

Captions have their own bands above and below the apparatus. Cyan and violet
identify the two wave contributions; bright mint points identify recorded
electron arrivals. The classical alternative alone uses drawn trajectories.
"""
from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import QuantumScene, double_slit_rig, halo, outlined_text
from manim_scenes.double_slit_visuals import (
    BRIGHT_TEXT, CLASSICAL_GOLD, DETECTOR_CORAL, ELECTRON_GLOW,
    LOWER_WAVE, UPPER_WAVE, SlitCloud, classical_stream, detection,
    living_ring, source_activity,
)
from utils.quantum_examples import two_slit_probability

SPAN = 2.45
GRID = np.linspace(-SPAN, SPAN, 401)
STRIP = 1.05
SCATTER = 0.40
HEADER_Y = 3.55
CAPTION_Y = -3.60


def _compact_rig():
    """Reserve the top and bottom of the frame for text, not apparatus."""
    rig = double_slit_rig()
    for panel, lo, hi in (
        (rig.barrier[0], -2.65, rig.barrier[0].get_top()[1]),
        (rig.barrier[2], rig.barrier[2].get_bottom()[1], 2.65),
    ):
        panel.stretch_to_fit_height(hi - lo)
        panel.move_to([rig.slits[0][0], (lo + hi) / 2, 0])
    rig.screen.stretch_to_fit_height(5.45)
    rig.screen[-1].set_stroke(BRIGHT_TEXT, width=2.0, opacity=0.80)
    rig.gun[0].set_stroke(UPPER_WAVE, opacity=0.80)
    rims = VGroup()
    for slit, color in zip(rig.slits, (UPPER_WAVE, LOWER_WAVE)):
        for side in (-1, 1):
            rim = Line(slit + [-0.18, side * 0.31, 0],
                       slit + [0.18, side * 0.31, 0],
                       color=color, stroke_width=3)
            rims.add(rim.copy().set_stroke(width=10, opacity=0.12), rim)
    rig.add(rims)
    return rig


def _draw(rng, weights, count):
    """Sample independent screen arrivals from the established probability."""
    return rng.choice(GRID, size=count, p=weights / weights.sum())


def _band_overlay(weights, screen_x, color=ELECTRON_GLOW):
    """Smooth luminous bands sit behind the distinct recorded points."""
    steps = np.linspace(-SPAN, SPAN, 150)
    bars = VGroup()
    for centre in steps:
        strength = float(np.interp(centre, GRID, weights) / weights.max())
        if strength < 0.02:
            continue
        bars.add(Rectangle(
            width=0.84, height=(steps[1] - steps[0]) * 1.05,
            stroke_width=0, fill_color=color, fill_opacity=0.38 * strength,
        ).move_to([screen_x, centre, 0]))
    return bars


def _probability(scene, coherent):
    """Match A1 and A2 to the two coloured slit contributions."""
    latex = r"P=|A_1+A_2|^2" if coherent else r"P=|A_1|^2+|A_2|^2"
    label = MathTex(latex, font_size=48, color=BRIGHT_TEXT,
                    substrings_to_isolate=[r"A_1", r"A_2"])
    label.set_color_by_tex(r"A_1", UPPER_WAVE)
    label.set_color_by_tex(r"A_2", LOWER_WAVE)
    label.set_stroke(cfg.BG, width=3, opacity=0.9, background=True)
    scene.pin(label.move_to([1.5, HEADER_Y, 0]))
    scene.playq(FadeIn(label), seconds=0.7)
    return label


def _collect(scene, group, seconds):
    """Animate many records, then retain one root for reliable cleanup."""
    scene.playq(LaggedStart(*(FadeIn(mark) for mark in group), lag_ratio=0.015),
                seconds=seconds)
    scene.remove(*group)
    scene.add(group)
    scene.local.append(group)


class Scene05OneAtATime(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("05")
    rng = np.random.default_rng(cfg.SEED + 5)

    # -- Beat 1: an active source, two openings, a receiving screen ----------
    rig = _compact_rig()
    activity = source_activity(rig)
    rig.add(activity)
    scene.morph(rig, seconds=2.2)
    heading = scene.pin(outlined_text("ONE ELECTRON AT A TIME", 38, CLASSICAL_GOLD)
                        .move_to([0, HEADER_Y, 0]))
    scene.playq(FadeIn(heading, shift=DOWN * 0.10), seconds=0.7)
    labels = VGroup(
        outlined_text("source", 30, BRIGHT_TEXT).move_to([-6.0, -0.90, 0]),
        outlined_text("two slits", 30, BRIGHT_TEXT).move_to([-2.5, -2.2, 0]),
        outlined_text("screen", 30, BRIGHT_TEXT).move_to([5.1, -3.15, 0]),
    )
    scene.show(labels, seconds=0.8)
    # Light each component as the narration names it; the source electrons
    # continue moving inside the gun throughout the remaining reading hold.
    for target in (rig.gun[0], rig.barrier, rig.screen[-1]):
        scene.playq(Indicate(target, color=CLASSICAL_GOLD, scale_factor=1.015),
                    seconds=1.1)
    scene.at(14)
    scene.drop(labels, heading, seconds=0.6)

    # -- Beat 2: classical pellets make two arrival distributions -----------
    classical = scene.pin(outlined_text("CLASSICAL PARTICLES", 36, CLASSICAL_GOLD)
                          .move_to([0, HEADER_Y, 0]))
    scene.playq(FadeIn(classical), seconds=0.5)
    for slit in rig.slits:
        pellet = detection(rig.muzzle, CLASSICAL_GOLD, 0.085)
        scene.add(pellet)
        scene.playq(pellet.animate.move_to(slit), seconds=0.55, rate_func=linear)
        landing = np.array([rig.screen_x, np.sign(slit[1]) * STRIP, 0])
        scene.playq(pellet.animate.move_to(landing), seconds=0.55, rate_func=linear)
        scene.playq(Flash(landing, color=CLASSICAL_GOLD, flash_radius=0.22),
                    FadeOut(pellet), seconds=0.35)

    stream = classical_stream(rig)
    scene.show(stream, seconds=0.4)
    lumps = np.where(np.abs(np.abs(GRID) - STRIP) < 0.40, 1.0, 1e-9)
    strips = VGroup(*[
        detection([rig.screen_x + rng.uniform(-SCATTER, SCATTER),
                   float(y) + rng.normal(0, 0.07), 0], CLASSICAL_GOLD, 0.035)
        for y in _draw(rng, lumps, 120)
    ])
    _collect(scene, strips, seconds=6.2)
    two = scene.pin(outlined_text("Two strips", 32, CLASSICAL_GOLD)
                    .move_to([3.0, CAPTION_Y, 0]))
    scene.playq(FadeIn(two), seconds=0.5)
    scene.at(30)
    stream.clear_updaters()
    scene.drop(stream, strips, classical, two, seconds=0.7)

    # -- Beat 3: one spread amplitude, followed by one localized arrival -----
    quantum = scene.pin(outlined_text("ONE ELECTRON · ONE DETECTION", 36, ELECTRON_GLOW)
                        .move_to([0, HEADER_Y, 0]))
    scene.playq(FadeIn(quantum), seconds=0.5)
    weights = two_slit_probability(GRID) + 1e-9
    landed = VGroup()
    for _ in range(6):
        y = float(_draw(rng, weights, 1)[0])
        spot = [rig.screen_x + rng.uniform(-SCATTER, SCATTER), y, 0]
        scene.playq(Flash(rig.muzzle, color=ELECTRON_GLOW, flash_radius=0.22),
                    seconds=0.15)
        progress = ValueTracker(-0.25)
        pulse = SlitCloud(rig, packet=progress.get_value)
        scene.add(pulse)
        scene.playq(progress.animate.set_value(1.40), seconds=0.65, rate_func=linear)
        pulse.clear_updaters()
        scene.remove(pulse)
        mark = detection(spot, radius=0.057)
        scene.playq(FadeIn(mark),
                    Flash(spot, color=ELECTRON_GLOW, flash_radius=0.24),
                    seconds=0.25)
        scene.remove(mark)
        landed.add(mark)
        scene.add(landed)
        scene.hold(0.18)
    scene.local.append(landed)
    scene.cue("One arrival. One point.", BRIGHT_TEXT, hold=1.2,
              position=[0, CAPTION_Y, 0])

    many = VGroup(*[
        detection([rig.screen_x + rng.uniform(-SCATTER, SCATTER), y, 0],
                  radius=0.034)
        for y in _draw(rng, weights, 420)
    ])
    _collect(scene, many, seconds=6.5)
    bright = _band_overlay(weights, rig.screen_x)
    scene.show(bright, seconds=0.7)
    # Keep the white detection cores above the soft accumulated band glow.
    scene.bring_to_front(many, landed)
    scene.at(52)
    scene.drop(landed, quantum, seconds=0.5)

    # -- Beat 4: phase crests move through a fixed interference envelope -----
    addition = _probability(scene, coherent=True)
    cloud = SlitCloud(rig)
    scene.show(cloud, seconds=0.8)
    # The cloud stops before the screen: probabilities and records occupy
    # separate visual regions. It also stays inside the caption-safe aperture.
    scene.cue("Amplitudes reinforce or cancel", CLASSICAL_GOLD, hold=2.2,
              position=[0, CAPTION_Y, 0])
    scene.at(70)
    cloud.clear_updaters()
    scene.drop(cloud, addition, seconds=0.7)

    # -- Beat 5: a fresh run with a record of which opening -----------------
    detector_point = rig.slits[0]
    watcher = VGroup(
        halo(0.24, DETECTOR_CORAL, layers=3, peak_opacity=0.28)
        .move_to(detector_point),
        Circle(radius=0.23, color=DETECTOR_CORAL, stroke_width=3.2)
        .move_to(detector_point),
        outlined_text("path detector", 30, DETECTOR_CORAL)
        .move_to([-3.25, 1.5, 0]),
        Line([-2.10, 1.32, 0], detector_point + [-0.20, 0.15, 0],
             color=DETECTOR_CORAL, stroke_width=2),
    )
    scene.show(watcher, seconds=0.7)
    separate = _probability(scene, coherent=False)
    scene.drop(many, bright, seconds=0.7)
    smooth = SlitCloud(rig, coherent=False)
    scene.show(smooth, seconds=0.6)

    collapsed = two_slit_probability(GRID, coherence=0.0) + 1e-9
    replacement = VGroup(*[
        detection([rig.screen_x + rng.uniform(-SCATTER, SCATTER), y, 0],
                  DETECTOR_CORAL, 0.034)
        for y in _draw(rng, collapsed, 420)
    ])
    _collect(scene, replacement, seconds=3.2)
    lost = _band_overlay(collapsed, rig.screen_x, DETECTOR_CORAL)
    scene.show(lost, seconds=0.6)
    scene.bring_to_front(replacement)
    scene.cue("Path recorded → no interference", DETECTOR_CORAL, hold=1.3,
              position=[0, CAPTION_Y, 0])
    scene.at(84)
    smooth.clear_updaters()
    scene.drop(replacement, lost, watcher, separate, smooth, seconds=0.7)

    # -- Beat 6: a living ring analogy, with nodes fixed in place ------------
    activity.clear_updaters()
    ring = living_ring()
    scene.morph(ring, seconds=2.4)
    scene.finish()
    ring.clear_updaters()
