"""Energy gaps, moving photons and spectral lines, with one clear equation."""
from __future__ import annotations

import numpy as np
from manim import *
import config as cfg
from manim_scenes.common import (
    add_cinematic_background, begin_scene, electron, end_scene, eq,
    equation_card, line_spectrum, narration_wait, paced_play, photon,
    spectral_line, wavelength_axis,
)
from utils.physics_models import HydrogenAtom
from utils.render_helpers import spectrum_positions

HYDROGEN = HydrogenAtom()
LEVELS = (2, 3, 4, 5, 6)
RAIL_LEFT, RAIL_RIGHT = -5.7, -.95
BAR_WIDTH, BAR_Y = 10.0, -2.6
LOW_NM, HIGH_NM = 380.0, 720.0


def level_y(n):
    return -1.2 + 1.04*(HYDROGEN.energy_ev(n)-HYDROGEN.energy_ev(2))


def spectrum_x(wavelength_nm):
    return spectrum_positions([wavelength_nm], LOW_NM, HIGH_NM, BAR_WIDTH)[0]


def _colour(n):
    return interpolate_color(ManimColor(HYDROGEN.color(n, 2)), ManimColor(cfg.WHITE), .25)


def _drop(n, x, color):
    return Arrow([x, level_y(n), 0], [x, level_y(2), 0], buff=.07,
                 color=color, stroke_width=4.5, max_tip_length_to_length_ratio=.12)


def _gap(n):
    bracket = DoubleArrow([-.35, level_y(2), 0], [-.35, level_y(n), 0], buff=0,
                          color=cfg.GOLD, stroke_width=2.4, max_tip_length_to_length_ratio=.09)
    label = eq(r'\Delta E', cfg.GOLD, 48).move_to([.27, (level_y(2)+level_y(n))/2, 0])
    return VGroup(bracket, label)


def _wave(n, y):
    spacing = .9*HYDROGEN.wavelength_nm(n, 2)/HYDROGEN.wavelength_nm(3, 2)
    return photon([1.05, y, 0], [4.65, y, 0], wavelength=spacing,
                  amplitude=.20, color=_colour(n))


def _state_change(scene, n, x, arrow, duration=1.2):
    upper = electron(.18).move_to([x, level_y(n), 0])
    lower = electron(.18).move_to([x, level_y(2), 0])
    scene.add(upper)
    paced_play(scene, GrowArrow(arrow),
               Succession(FadeOut(upper, run_time=duration/2), FadeIn(lower, run_time=duration/2)),
               run_time=duration)
    return lower


class Scene11PhotonLadder(Scene):
    def construct(self):
        play_scene(self)


def play_scene(scene):
    started = begin_scene(scene, '11')
    add_cinematic_background(scene)

    # No permanent headline. Only the main level labels need to stay beside rails.
    rails = {n: Line([RAIL_LEFT, level_y(n), 0], [RAIL_RIGHT, level_y(n), 0],
                     color=cfg.CYAN, stroke_width=3, stroke_opacity=.85 if n <= 4 else .4)
             for n in LEVELS}
    labels = {n: eq(rf'n={n}', '#BEDFED', 34).next_to(rails[n], LEFT, buff=.23) for n in (2, 3, 4)}
    ladder = VGroup(*rails.values(), *labels.values())
    paced_play(scene, LaggedStart(*[FadeIn(rail) for rail in rails.values()], lag_ratio=.2),
               *[FadeIn(label) for label in labels.values()], run_time=2)
    active = eq(r'n=3\rightarrow n=2', cfg.CYAN, 42).move_to([-3.15, 2.75, 0])
    paced_play(scene, FadeIn(active), run_time=.6)
    narration_wait(scene, 1.4)
    red_drop = _drop(3, -2.9, _colour(3))
    resident = _state_change(scene, 3, -2.9, red_drop, duration=1.4)
    red = _wave(3, -.65)
    paced_play(scene, Create(red), run_time=1.4)
    paced_play(scene, red.animate.shift(RIGHT*1.25), run_time=4, rate_func=linear)
    narration_wait(scene, 2)
    paced_play(scene, FadeOut(active), run_time=.6)
    paced_play(scene, Indicate(red_drop, color=cfg.GOLD, scale_factor=1.0), run_time=1.2)
    narration_wait(scene, 7.6)

    # The energy gap and equation occupy their own clear areas.
    gap = _gap(3)
    card = equation_card(r'\Delta E = h\,\nu', cfg.WHITE, 78).move_to([3.65, 2.45, 0])
    paced_play(scene, FadeIn(gap), run_time=.8)
    paced_play(scene, FadeIn(card), run_time=1)
    narration_wait(scene, 11)

    # Compare two Balmer transitions. Both photons are visible light (a 4->3
    # transition would be infrared, so it must not be presented as a red line).
    paced_play(scene, FadeOut(red, resident, red_drop, gap), run_time=.6)
    smaller = _drop(3, -4.1, _colour(3))
    larger = _drop(6, -2.2, _colour(6))
    small_wave, large_wave = _wave(3, .6), _wave(6, -.8)
    paced_play(scene, GrowArrow(smaller), Create(small_wave), run_time=1.4)
    narration_wait(scene, 2.2)
    bigger_gap = _gap(6)
    active = eq(r'n=6\rightarrow n=2', '#C8B0FF', 42).move_to([-3.15, 2.75, 0])
    paced_play(scene, GrowArrow(larger), Create(large_wave), FadeIn(bigger_gap, active), run_time=1.4)
    narration_wait(scene, 2.2)
    # Equal displacements in equal times make the common propagation speed clear.
    paced_play(scene, small_wave.animate.shift(RIGHT*1.25), large_wave.animate.shift(RIGHT*1.25),
               run_time=5, rate_func=linear)
    narration_wait(scene, 2)
    paced_play(scene, FadeOut(smaller, larger, small_wave, large_wave, bigger_gap, active), run_time=.8)

    # Each transition writes one line. Its arrow and photon clear before the next.
    plate, _ = line_spectrum([], width=BAR_WIDTH, height=.72, low_nm=LOW_NM, high_nm=HIGH_NM)
    plate.move_to([0, BAR_Y, 0])
    axis = wavelength_axis(width=BAR_WIDTH, low_nm=LOW_NM, high_nm=HIGH_NM,
                           center=[0, -3.24, 0])
    paced_play(scene, FadeIn(plate, axis), run_time=.8)
    spectral_lines = VGroup()
    for n, wavelength, _ in HYDROGEN.balmer_series(6):
        active = eq(rf'n={n}\rightarrow n=2', cfg.WHITE, 42).move_to([-3.15, 2.75, 0])
        paced_play(scene, FadeIn(active), Indicate(rails[n], color=_colour(n), scale_factor=1.0), run_time=.6)
        drop = _drop(n, -2.9, _colour(n))
        resident = _state_change(scene, n, -2.9, drop, duration=.9)
        start = np.array([-2.65, level_y(2)-.22, 0])
        target = np.array([spectrum_x(wavelength), BAR_Y+.37, 0])
        direction = target-start
        unit = direction/np.linalg.norm(direction)
        packet = photon(start, start+unit*.6, wavelength=.24, amplitude=.075, color=_colour(n))
        paced_play(scene, FadeIn(packet), run_time=.2)
        paced_play(scene, packet.animate.shift(direction-unit*.3), run_time=1.1, rate_func=linear)
        line = spectral_line(wavelength, width=BAR_WIDTH, height=.72, low_nm=LOW_NM, high_nm=HIGH_NM)
        line.move_to([spectrum_x(wavelength), BAR_Y, 0])
        spectral_lines.add(line)
        paced_play(scene, FadeOut(packet, drop, resident, active), FadeIn(line), run_time=.5)
        narration_wait(scene, 1.5)
    narration_wait(scene, 3)

    # Clear the ladder before the numerical example. Keep the important equation.
    paced_play(scene, FadeOut(ladder), card.animate.move_to([0, 2.6, 0]), run_time=1)
    spectrum = VGroup(plate, spectral_lines, axis)
    paced_play(scene, spectrum.animate.shift(UP*.6), run_time=.8)
    wavelength = HYDROGEN.wavelength_nm(5, 2)
    energy = HYDROGEN.transition_energy_ev(5, 2)
    transition = eq(r'n=5\rightarrow n=2', '#C4DCFF', 46).move_to([-3.6, .75, 0])
    energy_value = eq(rf'\Delta E = {energy:.2f}\,\mathrm{{eV}}', cfg.GOLD, 50).move_to([3, .75, 0])
    wavelength_value = eq(rf'\lambda\approx {wavelength:.0f}\,\mathrm{{nm}}', '#C7AEFF', 50).move_to([3, -.25, 0])
    paced_play(scene, FadeIn(transition), run_time=.7)
    paced_play(scene, FadeIn(energy_value), run_time=.7)
    paced_play(scene, FadeIn(wavelength_value), run_time=.7)
    marker_x = spectrum_x(wavelength)
    pointer = Arrow([marker_x, -.1, 0], [marker_x, BAR_Y+.6+.46, 0],
                    buff=.1, color='#C7AEFF', stroke_width=3, max_tip_length_to_length_ratio=.14)
    paced_play(scene, GrowArrow(pointer), Indicate(spectral_lines[2], color='#C7AEFF', scale_factor=1.05), run_time=.9)
    narration_wait(scene, 5.4)

    # Finish on the equation and the barcode, with every transition arrow gone.
    paced_play(scene, FadeOut(transition, energy_value, wavelength_value, pointer), run_time=.7)
    paced_play(scene, spectrum.animate.shift(UP*.55), run_time=1)
    paced_play(scene, LaggedStart(*[Indicate(line, color=_colour(n), scale_factor=1.03)
        for n, line in zip((3, 4, 5, 6), spectral_lines)], lag_ratio=.5), run_time=3.5)
    narration_wait(scene, 4)
    end_scene(scene, started, cfg.SCENE_DURATIONS['11'])
