"""Chapter 2: evidence is made on screen, then carried past the rejected orbit.

Scattering, dispersed hydrogen light and discrete energy changes become three
surviving exhibits. The light cue at the end is literally a spectral line
opening into the wave that starts chapter 3. Photons come from the discharge
source or an energy change, never from the bare nucleus.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.atomic_visuals import nucleon_cluster
from manim_scenes.common import (
    QuantumScene, check_mark, glow_curve, glow_dot, glow_line, halo,
    electron, outlined_text, wave,
)

# The four Balmer lines, in increasing wavelength order. This is a qualitative
# dispersion view: no numerical wavelength scale is drawn. The upper-state
# indices link each colour to the same hydrogen energy-gap ordering.
LIGHT_LINES = ((6, cfg.PURPLE), (5, "#857AFF"), (4, cfg.CYAN), (3, cfg.RED))
SCREEN_Y = (-1.35, -0.72, 0.06, 1.35)


def _scattering_paths() -> VGroup:
    """Three illustrative repulsive paths; the close approach turns back."""
    paths = VGroup()
    for points in (
        ([-6, 1.8, 0], [-2, 1.8, 0], [1, 2.0, 0], [5.7, 2.45, 0]),
        ([-6, -1.9, 0], [-2, -1.9, 0], [1, -2.1, 0], [5.7, -2.65, 0]),
    ):
        path = VMobject(color=cfg.GOLD, stroke_width=2.2, stroke_opacity=0.35)
        path.set_points_smoothly(points)
        paths.add(path)
    # Explicit controls keep the turnaround outside the drawn nucleus;
    # unconstrained spline smoothing can overshoot into its surface.
    close = VMobject(color=cfg.GOLD, stroke_width=2.2, stroke_opacity=0.35)
    close.start_new_path([-6, -0.30, 0])
    close.add_cubic_bezier_curve_to([-3, -0.30, 0], [-1, -0.30, 0], [-1, -0.70, 0])
    close.add_cubic_bezier_curve_to([-1, -1.10, 0], [-2.2, -1.8, 0], [-4, -2.8, 0])
    paths.add(close)
    return paths


def _discharge_source() -> VGroup:
    """A glass hydrogen tube with electrodes and a visible excited-gas glow."""
    tube = RoundedRectangle(width=1.8, height=0.65, corner_radius=0.25,
                            stroke_color=cfg.CYAN, stroke_width=2.2,
                            fill_color=cfg.PURPLE, fill_opacity=0.22)
    glow = VGroup(*[
        tube.copy().scale(1 + 0.12 * i).set_stroke(width=0).set_fill(cfg.PURPLE, opacity=0.05)
        for i in (3, 2, 1)
    ])
    electrodes = VGroup(*[
        RoundedRectangle(width=0.14, height=0.48, corner_radius=0.03,
                         fill_color=cfg.MUTED, fill_opacity=1, stroke_width=0).shift(RIGHT * x)
        for x in (-0.76, 0.76)
    ])
    gas = VGroup(*[glow_dot([x, 0.10 * np.sin(i * 2.2), 0], radius=0.045, color=cfg.PURPLE)
                  for i, x in enumerate(np.linspace(-0.58, 0.58, 7))])
    return VGroup(glow, tube, gas, electrodes).move_to([-4.8, -0.45, 0])


def _prism() -> VGroup:
    """A lightly filled glass prism; colour is supplied by the dispersed rays."""
    front = Polygon([-0.35, 0.80, 0], [-1.10, -1.0, 0], [0.55, -1.0, 0],
                    fill_color=cfg.CYAN, fill_opacity=0.13,
                    stroke_color=cfg.CYAN, stroke_width=2.2)
    back = front.copy().shift(UP * 0.20 + RIGHT * 0.25).set_opacity(0.22)
    joins = VGroup(*[Line(a, b, color=cfg.CYAN, stroke_width=1.4, stroke_opacity=0.3)
                    for a, b in zip(front.get_vertices(), back.get_vertices())])
    return VGroup(back, joins, front)


def _spectrum() -> tuple[VGroup, VGroup, VGroup]:
    """A vertical detector, rotated into the familiar barcode after dispersion."""
    plate = RoundedRectangle(width=1.05, height=3.45, corner_radius=0.12,
                             stroke_color=cfg.MUTED, stroke_width=1.8, stroke_opacity=0.5,
                             fill_color="#03101B", fill_opacity=0.92).move_to([5.0, 0, 0])
    bands = VGroup(*[
        glow_line([4.65, y, 0], [5.35, y, 0], colour, 5)
        for (_, colour), y in zip(LIGHT_LINES, SCREEN_Y)
    ])
    return VGroup(plate), plate, bands


def _energy_levels() -> tuple[VGroup, dict[int, float]]:
    """Hydrogen n=2…6 spacings, without spending this recap on level labels."""
    energies = {n: -1 / n**2 for n in range(2, 7)}
    y = {n: -1.3 + 2.6 * (energy - energies[2]) / (energies[6] - energies[2])
         for n, energy in energies.items()}
    shelves = VGroup(*[glow_line([-1.55, y[n], 0], [1.55, y[n], 0], cfg.CYAN, 2.6)
                      for n in range(2, 7)])
    return shelves, y


def _packet(colour: str, cycles: float = 2.0) -> VGroup:
    """A finite light packet with a smooth envelope, not a persistent ray."""
    curve = ParametricFunction(
        lambda x: [x, 0.18 * np.cos(PI * x / 1.4)**2 * np.sin(TAU * cycles * x / 1.4), 0],
        t_range=[-0.7, 0.7, 0.025], color=colour, stroke_width=3.5)
    return glow_curve(curve, colour, opacity=0.10)


def _show_energy_change(scene: QuantumScene, levels: VGroup, y: dict[int, float],
                        bands: VGroup, index: int) -> None:
    """Match one discrete drop to its coloured spectral line, then clear it."""
    upper, colour = LIGHT_LINES[index]
    bead = glow_dot([-0.9, y[upper], 0], radius=0.11, color=cfg.CYAN)
    drop = Arrow([-0.9, y[upper], 0], [-0.9, y[2], 0], color=colour,
                 buff=0.10, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
    scene.show(VGroup(bead, drop), seconds=0.3)
    owned = scene.local[-1]
    scene.playq(bead.animate.move_to([-0.9, y[2], 0]), seconds=0.7)
    packet = _packet(colour, cycles=1.4 + 0.55 * (3 - index)).move_to([1.8, y[2], 0])
    scene.show(packet, seconds=0.2)
    scene.playq(packet.animate.move_to(bands[index].get_center()), seconds=1.0, rate_func=linear)
    scene.playq(Indicate(bands[index], color=colour, scale_factor=1.12),
                FadeOut(packet), FadeOut(owned), seconds=0.45)
    scene.local.remove(packet)
    scene.local.remove(owned)
    scene.remove(bead, drop)


class Scene02WhatSurvives(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("02")

    # -- Beat 1: recreate the scattering clue around a lit, dimensional core --
    scene.lower_ground(seconds=0.35)
    # Reuse chapter 1's exact clustered nucleus, including its warm lighting.
    core = nucleon_cluster(scene)
    glow = halo(0.62, cfg.ORANGE, layers=6, peak_opacity=0.14)
    scene.camera.add_fixed_orientation_mobjects(glow)
    nuclear = VGroup(glow, core)
    evidence = VGroup(nuclear)
    evidence._needs_depth_sort = True
    scene.move_camera(phi=52 * DEGREES, theta=-75 * DEGREES,
                      added_anims=[FadeOut(scene.anchor), FadeIn(evidence)], run_time=1.1 / cfg.SPEED)
    scene.anchor = evidence
    # Each nucleon owns a lighting updater. Keep those callbacks for the next
    # camera move, then freeze them so the stationary evidence stays inexpensive.
    relighters = [(nucleon, tuple(nucleon.updaters)) for nucleon in core]
    core.clear_updaters(recursive=True)
    question = scene.pin(outlined_text("WHAT SURVIVES?", cfg.FONT["label"], cfg.GOLD).move_to(UP * 3.5))
    scene.playq(FadeIn(question), seconds=0.4)
    paths = _scattering_paths()
    particles = VGroup(*[glow_dot(path.get_start(), radius=0.10, color=cfg.GOLD) for path in paths])
    scene.show(VGroup(paths, particles), seconds=0.4)
    scatter = scene.local[-1]
    scene.playq(LaggedStart(*[MoveAlongPath(particle, path, rate_func=linear)
                              for particle, path in zip(particles, paths)], lag_ratio=0.12), seconds=3.2)
    scene.drop(scatter, question, seconds=0.4)
    nucleus_label = scene.pin(outlined_text("Nucleus", 30, cfg.GREEN).move_to([-5.0, 1.5, 0]))
    for nucleon, callbacks in relighters:
        for callback in callbacks:
            nucleon.add_updater(callback)
    scene.move_camera(phi=0, theta=-90 * DEGREES,
                      added_anims=[nuclear.animate.scale(0.68).move_to([-5, 2.4, 0]), FadeIn(nucleus_label)],
                      run_time=0.9 / cfg.SPEED)
    core.clear_updaters(recursive=True)
    scene.camera.remove_fixed_orientation_mobjects(glow)

    # -- Beat 2: hydrogen light really arrives at the spectroscope -----------
    source, prism = _discharge_source(), _prism()
    spectrum, plate, bands = _spectrum()
    source_label = scene.pin(outlined_text("HYDROGEN", 30, cfg.PURPLE).move_to([-4.8, -1.55, 0]))
    spectrum_label = scene.pin(outlined_text("Spectrum", 30, cfg.GREEN).move_to([5.0, -2.2, 0]))
    scene.playq(FadeIn(source), FadeIn(prism), FadeIn(spectrum),
                FadeIn(source_label), FadeIn(spectrum_label), seconds=0.65)
    scene.local += [source, prism, spectrum]
    incoming = glow_dot([-3.85, -0.45, 0], radius=0.10, color=cfg.WHITE)
    scene.add(incoming)
    scene.playq(incoming.animate.move_to([-0.25, -0.30, 0]),
                Indicate(source[2], color=cfg.WHITE, scale_factor=1.12), seconds=1.0)
    exits = [np.array([5.0, y, 0]) for y in SCREEN_Y]
    start = np.array([0.35, -0.40, 0])
    rays = VGroup(*[Line(start, end, color=colour, stroke_width=2, stroke_opacity=0.24)
                   for (_, colour), end in zip(LIGHT_LINES, exits)])
    packets = VGroup(*[
        _packet(colour, cycles=3.0 - index * 0.45)
        .rotate(np.arctan2((end - start)[1], (end - start)[0])).move_to(start)
        for index, ((_, colour), end) in enumerate(zip(LIGHT_LINES, exits))
    ])
    scene.playq(FadeOut(incoming), Create(rays), FadeIn(packets), seconds=0.35)
    scene.local += [rays, packets]
    scene.playq(*[packet.animate.move_to(end) for packet, end in zip(packets, exits)], seconds=2.0, rate_func=linear)
    scene.playq(FadeOut(packets), FadeIn(bands),
                *[Flash(end, color=colour, flash_radius=0.17, line_length=0.08)
                  for (_, colour), end in zip(LIGHT_LINES, exits)], seconds=0.55)
    scene.local.remove(packets)
    scene.remove(bands)
    spectrum.add(bands)
    scene.add(spectrum)
    scene.at(12)

    # -- Beat 3: gather the clues and connect a drop to its light -------------
    scene.drop(source, prism, rays, source_label, seconds=0.55)
    levels, y = _energy_levels()
    scene.playq(nuclear.animate.move_to([-5, 0.1, 0]),
                nucleus_label.animate.move_to([-5, -2.1, 0]),
                spectrum.animate.rotate(-PI / 2).move_to([4.8, 0.1, 0]),
                spectrum_label.animate.move_to([4.8, -2.1, 0]), FadeIn(levels), seconds=1.2)
    scene.local.remove(spectrum)
    scene.adopt(spectrum, levels)
    energy_label = scene.pin(outlined_text("Allowed energies", 30, cfg.GREEN).move_to([0, -2.1, 0]))
    scene.playq(FadeIn(energy_label), seconds=0.5)
    for index in (3, 0, 2):
        _show_energy_change(scene, levels, y, bands, index)
    scene.at(24)

    # -- Beat 4: keep each result in turn; the exhibits respond to the voice --
    ticks = []
    for x, item in ((-5, nuclear), (0, levels), (4.8, spectrum)):
        tick = check_mark(0.20).move_to([x, 2.2, 0])
        scene.show(tick, seconds=0.4)
        # Confirm the nucleus with its halo; retain the red/gold nucleon colours.
        highlight = glow if item is nuclear else item
        scene.playq(Indicate(highlight, color=cfg.GREEN, scale_factor=1.035), seconds=1.1)
        ticks.append(tick)
    scene.playq(LaggedStart(*[Indicate(band, color=colour, scale_factor=1.08)
                              for (_, colour), band in zip(LIGHT_LINES, bands)], lag_ratio=0.3), seconds=2.4)
    scene.at(32)

    # -- Beat 5: the evidence stays as the circular route becomes a question -
    # Carry the SAME nucleus into the orbit drawing instead of creating a
    # different centre with the generic orbit helper. Only its path and electron
    # are new; preserve the familiar (core, ring, electron) indexing below.
    atom_center = np.array([-3.6, 0.0, 0.0])
    ring = Circle(radius=2.0, color=cfg.MUTED, stroke_width=2.4,
                  stroke_opacity=0.62).move_to(atom_center)
    bead = electron(0.17).move_to(atom_center + RIGHT * 2.0)
    orbit_parts = VGroup(ring, bead)
    scene.playq(nuclear.animate.move_to(atom_center), FadeIn(orbit_parts),
                levels.animate.scale(0.64).move_to([3.5, 1.1, 0]),
                spectrum.animate.scale(0.82).move_to([3.5, -1.35, 0]),
                nucleus_label.animate.move_to([-3.6, -2.75, 0]),
                energy_label.animate.move_to([3.5, 2.35, 0]),
                spectrum_label.animate.move_to([3.5, -2.55, 0]),
                ticks[0].animate.move_to([-3.6 - nucleus_label.width / 2 - 0.45, -2.75, 0]),
                ticks[1].animate.move_to([3.5 - energy_label.width / 2 - 0.45, 2.35, 0]),
                ticks[2].animate.move_to([3.5 - spectrum_label.width / 2 - 0.45, -2.55, 0]), seconds=1.4)
    scene.anchor.remove(nuclear)
    scene.remove(nuclear, orbit_parts, ring, bead)
    doubted = VGroup(nuclear, ring, bead)
    doubted._needs_depth_sort = True
    scene.adopt(doubted)
    # A flat background would cover the depth-sorted nucleons. Restore it only
    # once the entire atom leaves at the start of the final light beat.
    scene.anchor._needs_depth_sort = True
    route_question = scene.pin(outlined_text("?", 66, cfg.GOLD).move_to([-3.6, 2.75, 0]))
    scene.playq(FadeIn(route_question, scale=0.7), seconds=0.45)
    scene.playq(Rotate(doubted[2], angle=TAU * 0.70, about_point=[-3.6, 0, 0]),
                doubted[1].animate.set_stroke(cfg.RED, opacity=0.85), seconds=4.3, rate_func=linear)
    old_track = doubted[1]
    broken = DashedVMobject(old_track.copy(), num_dashes=36, dashed_ratio=0.45)
    # Crossfade the two tracks: morphing a circle into many dash subpaths
    # produces temporary coils rather than a clean loss of certainty.
    scene.playq(FadeOut(old_track), FadeIn(broken), seconds=0.8)
    doubted.remove(old_track)
    scene.remove(broken)
    doubted.add(broken)
    scene.at(41)

    # -- Beat 6: the next clue comes from the surviving LIGHT, not the track --
    scene.drop(nucleus_label, energy_label, spectrum_label, route_question, *ticks, seconds=0.5)
    scene.playq(FadeOut(doubted), FadeOut(levels), spectrum.animate.scale(2.6).move_to(ORIGIN), seconds=1.3)
    scene.remove(scene.anchor)
    scene.anchor = VGroup(spectrum)
    scene.add(scene.anchor)
    scene.raise_ground(seconds=0.6)
    selected = bands[2]
    scene.playq(Indicate(selected, color=cfg.WHITE, scale_factor=1.10), seconds=0.8)
    radiation = wave(k=4)
    scene.playq(ReplacementTransform(selected, radiation), FadeOut(plate),
                *[FadeOut(band) for index, band in enumerate(bands) if index != 2], seconds=1.4)
    scene.remove(scene.anchor, spectrum)
    scene.anchor = radiation
    scene.add(radiation)
    scene.at(46)
    light = scene.pin(outlined_text("LIGHT", cfg.FONT["label"], cfg.GOLD).move_to(UP * 3.35))
    phase = ValueTracker(0)
    radiation.add_updater(lambda mob: mob.become(wave(k=4, phase=phase.get_value())))
    scene.playq(FadeIn(light), phase.animate.set_value(TAU * 0.2), seconds=0.5, rate_func=linear)
    scene.playq(phase.animate.set_value(TAU * 1.6), seconds=2.0, rate_func=linear)
    scene.playq(FadeOut(light), phase.animate.set_value(TAU * 2), seconds=0.6, rate_func=linear)
    scene.remove_fixed_in_frame_mobjects(light)
    scene.local.remove(light)
    radiation.clear_updaters()
    radiation.become(wave(k=4))
    scene.finish()
