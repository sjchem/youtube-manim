"""Chapter 6: a closing wave selects discrete patterns.

This is a ring analogy, not a hydrogen orbital or the orbital-angular-momentum
rule. Continuous phase motion makes its boundary condition visible. The
numerical comparison and algebra occupy a separate column beside the ring.
"""
from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import QuantumScene, check_mark, cross_mark, outlined_text, equation
from manim_scenes.matter_wave_visuals import TravellingWave
from manim_scenes.ring_wave_visuals import (
    BRIGHT_CORAL, BRIGHT_GOLD, BRIGHT_GREEN, BRIGHT_WHITE, WAVE_CYAN,
    WrappedWave, join_marker,
)
from utils.quantum_examples import bohr_radius, bohr_speed, de_broglie_wavelength

RING_RADIUS = 2.60
NUMBER_CENTRE = np.array([3.45, 0.0, 0.0])
ELECTRON_LAMBDA = de_broglie_wavelength(9.1093837015e-31, bohr_speed(1))
CIRCUMFERENCE = 2 * np.pi * bohr_radius(1)


def _number(latex, size=48, color=BRIGHT_WHITE):
    """Bright, lightly reinforced maths with a fixed right-column width."""
    label = equation(latex, size, color)
    label.set_stroke(color, width=0.35, opacity=1)
    if label.width > 5.4:
        label.scale_to_fit_width(5.4)
    return label


def _closed_transition(scene, previous, count, shift=ORIGIN):
    """Crossfade closed modes rather than label an intermediate fraction."""
    replacement = WrappedWave(ValueTracker(count), radius=RING_RADIUS)
    replacement.phase = previous.phase
    displacement = previous.guide.get_center() + np.asarray(shift)
    replacement.shift(displacement)
    replacement.update(0)
    scene.playq(
        FadeOut(previous, shift=shift, suspend_mobject_updating=False),
        FadeIn(replacement, shift=shift, suspend_mobject_updating=False),
        seconds=2.2,
    )
    previous.clear_updaters()
    scene.remove(previous.mode)
    scene.anchor = replacement
    return replacement


class Scene06WavesThatFit(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("06")
    mode = ValueTracker(4.4)
    wrapped = WrappedWave(mode, radius=RING_RADIUS, color=BRIGHT_CORAL)

    # -- Beat 1: the ends must agree through the whole phase cycle -----------
    scene.morph(wrapped, seconds=1.8)
    marker = join_marker(wrapped, BRIGHT_CORAL)
    verdict = VGroup(
        cross_mark(0.23, BRIGHT_CORAL),
        outlined_text("The join disagrees", 36, BRIGHT_CORAL),
    ).arrange(RIGHT, buff=0.30).move_to([0, -3.70, 0])
    scene.show(marker, seconds=0.8)
    scene.show(verdict, seconds=1.0)
    scene.at(12)
    marker.clear_updaters()
    scene.drop(marker, verdict, seconds=0.6)

    # -- Beat 2: tune the wavelength until the pattern closes ---------------
    scene.playq(mode.animate.set_value(4),
                wrapped.crest.animate.set_color(WAVE_CYAN),
                wrapped.bloom.animate.set_color(WAVE_CYAN),
                seconds=3.0)
    agreed = VGroup(
        check_mark(0.22, BRIGHT_GREEN),
        outlined_text("A whole number fits", 36, BRIGHT_GREEN),
    ).arrange(RIGHT, buff=0.30).move_to([0, -3.70, 0])
    agreed_marker = join_marker(wrapped, BRIGHT_GREEN)
    scene.show(agreed_marker, seconds=0.5)
    scene.show(agreed, seconds=0.5)
    scene.hold(1.6)
    agreed_marker.clear_updaters()
    scene.drop(agreed_marker, agreed, seconds=0.5)

    # -- Beat 3: distinct closed patterns, with the phase always advancing ---
    count = scene.pin(outlined_text("4 wavelengths", 38, WAVE_CYAN)
                      .move_to([0, -3.70, 0]))
    scene.playq(FadeIn(count), seconds=0.5)
    for lobes in (5, 6, 4):
        scene.playq(FadeOut(count), seconds=0.2)
        wrapped = _closed_transition(scene, wrapped, lobes)
        replacement = outlined_text(f"{lobes} wavelengths", 38, WAVE_CYAN)
        replacement.move_to([0, -3.70, 0])
        scene.add_fixed_in_frame_mobjects(replacement)
        scene.remove(replacement)
        scene.playq(FadeIn(replacement), seconds=0.3)
        scene.remove_fixed_in_frame_mobjects(count)
        scene.local.remove(count)
        count = replacement
        scene.local.append(count)
        scene.hold(1.4)
    scene.at(38)
    scene.drop(count, seconds=0.5)

    # -- Beat 4: give the drawing and calculation their own columns ----------
    # The wave follows its live reference circle, so it keeps moving while the
    # whole diagram shifts left. The gold arc highlights the circumference;
    # it is a moving measurement highlight, not a particle.
    wrapped = _closed_transition(scene, wrapped, 1, shift=LEFT * 3.2)
    scene.playq(
        wrapped.guide.animate.set_stroke(BRIGHT_GOLD, width=3.2, opacity=0.75),
        wrapped.measure.animate.set_stroke(opacity=1),
        seconds=1.4,
    )
    pair = scene.pin(VGroup(
        _number(rf"\lambda={ELECTRON_LAMBDA * 1e10:.4f}\ \text{{\AA}}", 48, WAVE_CYAN),
        _number(rf"2\pi r_1={CIRCUMFERENCE * 1e10:.4f}\ \text{{\AA}}", 48, BRIGHT_GOLD),
    ).arrange(DOWN, buff=0.48).move_to(NUMBER_CENTRE + UP * 1.30))
    scene.playq(LaggedStart(*(FadeIn(line, shift=LEFT * 0.12) for line in pair),
                           lag_ratio=0.7), seconds=2.2)
    scene.playq(Indicate(pair, color=BRIGHT_WHITE, scale_factor=1.04), seconds=1.4)
    same = scene.pin(outlined_text("The same number", 36, BRIGHT_GREEN, limit=5.4)
                     .move_to(NUMBER_CENTRE + DOWN * 0.20))
    scene.playq(FadeIn(same), seconds=0.6)
    scene.at(54)
    scene.drop(pair, same, seconds=0.6)

    # -- Beat 5: the boundary condition returns Bohr's ring-model rule -------
    steps = scene.pin(VGroup(
        _number(r"2\pi r=n\lambda", 48, WAVE_CYAN),
        _number(r"\lambda=\frac{h}{mv}", 46, BRIGHT_WHITE),
        _number(r"mvr=\frac{nh}{2\pi}", 50, BRIGHT_GOLD),
    ).arrange(DOWN, buff=0.38).move_to(NUMBER_CENTRE + UP * 0.65))
    for line in steps:
        scene.playq(FadeIn(line, shift=UP * 0.12), seconds=1.0)
        scene.hold(0.7)
    stamp = scene.pin(VGroup(
        outlined_text("Bohr assumed this.", 32, BRIGHT_WHITE, limit=5.4),
        outlined_text("A closed wave gives it.", 32, BRIGHT_GREEN, limit=5.4),
    ).arrange(DOWN, buff=0.20).move_to(NUMBER_CENTRE + DOWN * 2.45))
    scene.playq(FadeIn(stamp),
                Indicate(steps[2], color=BRIGHT_WHITE, scale_factor=1.06),
                seconds=1.4)
    scene.at(66)
    scene.drop(steps, stamp, seconds=0.7)

    # -- Beat 6: leave the analogy with a travelling amplitude --------------
    caveat = scene.pin(outlined_text(
        "Ring analogy · real states are three-dimensional",
        30, BRIGHT_WHITE,
    ).move_to([0, -3.65, 0]))
    scene.playq(FadeIn(caveat), seconds=0.6)
    wrapped.clear_updaters()
    outgoing = TravellingWave(width=12, k=5, amplitude=0.60, color=WAVE_CYAN)
    scene.morph(outgoing, seconds=2.6)
    scene.at(72)
    scene.drop(caveat, seconds=0.6)
    scene.finish()
    outgoing.clear_updaters()
    scene.remove(mode)
