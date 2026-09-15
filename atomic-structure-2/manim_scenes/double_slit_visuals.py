"""Scene 5's luminous sources, detection marks and two-route wave display.

The cloud interpolates Gaussian amplitudes towards the existing far-field
screen model. It is a schematic amplitude display, not a measured trajectory
or a numerical solution of propagation through the drawn apparatus.
"""
from __future__ import annotations

import numpy as np
from manim import *
import config as cfg

UPPER_WAVE = "#63ECFF"
LOWER_WAVE = "#C4A0FF"
ELECTRON_GLOW = "#80FFE8"
BRIGHT_TEXT = "#F4FCFF"
CLASSICAL_GOLD = "#FFE699"
DETECTOR_CORAL = "#FFACBB"


def detection(point, color=ELECTRON_GLOW, radius=0.042):
    """A recorded point has a small white centre and a soft coloured halo."""
    return VGroup(
        Dot(point, radius=radius * 2.4, color=color).set_opacity(0.075),
        Dot(point, radius=radius * 1.5, color=color).set_opacity(0.20),
        Dot(point, radius=radius, color=color),
        Dot(point, radius=radius * 0.43, color=BRIGHT_TEXT),
    )


def source_activity(rig):
    """Confined source electrons keep the apparatus live during reading holds.

    These stay inside the source; they do not imply additional emissions
    between the explicitly animated single-electron shots.
    """
    centre = rig.gun[0].get_center()
    group = VGroup(*[detection(centre, radius=0.040) for _ in range(3)])
    group.phase = 0.0

    def advance(mob, dt):
        mob.phase += dt * cfg.SPEED * 1.25
        for index, bead in enumerate(mob):
            angle = mob.phase + index * TAU / 3
            bead.move_to(centre + [0.32 * np.cos(angle), 0.16 * np.sin(angle), 0])

    advance(group, 0)
    group.add_updater(advance)
    return group


def classical_stream(rig):
    """Moving gold pellets illustrate the explicitly classical alternative."""
    group = VGroup(*[detection(rig.muzzle, CLASSICAL_GOLD, 0.044) for _ in range(8)])
    group.phase = 0.0

    def advance(mob, dt):
        mob.phase = (mob.phase + dt * cfg.SPEED / 3.8) % 1
        for index, bead in enumerate(mob):
            f = (mob.phase + index / len(mob)) % 1
            slit = rig.slits[index % 2]
            landing = np.array([rig.screen_x, np.sign(slit[1]) * 1.05, 0])
            if f < 0.42:
                point = interpolate(rig.muzzle, slit, f / 0.42)
            else:
                point = interpolate(slit, landing, (f - 0.42) / 0.58)
            bead.move_to(point)

    advance(group, 0)
    group.add_updater(advance)
    return group


class SlitCloud(ImageMobject):
    """A glowing amplitude envelope with moving phase crests.

    At the screen:
        A1 = sqrt(g/2) exp(+i k y), A2 = sqrt(g/2) exp(-i k y).
    Coherent intensity is |A1+A2|². With a path record it is |A1|²+|A2|².
    Thus the screen edge uses exactly the probabilities sampled by the scene.
    Near the openings, the envelope is smoothly narrowed for explanation.

    Cyan and violet identify contributions from the two openings, not charge.
    Moving crest highlights show phase; the underlying intensity stays fixed.
    """

    def __init__(self, rig, coherent=True, packet=None):
        self.phase = 0.0
        self.packet = packet
        x = np.linspace(rig.slits[0][0] + 0.15, rig.screen_x - 0.55, 320)
        y = np.linspace(2.45, -2.45, 260)
        xx, yy = np.meshgrid(x, y)
        # The screen-edge coordinate is the abstract far-field screen plane;
        # the narrow unpainted gap keeps the map separate from recorded hits.
        t = (xx - x[0]) / (x[-1] - x[0])
        width = 0.18 + (1.75 - 0.18) * t
        centres = [slit[1] * (1 - t) for slit in rig.slits]
        a = [np.exp(-(yy - c) ** 2 / (4 * width ** 2)) / np.sqrt(2)
             for c in centres]
        phase = 3.2 * yy * t
        intensity = a[0] ** 2 + a[1] ** 2
        if coherent:
            intensity += 2 * a[0] * a[1] * np.cos(2 * phase)
        strength = np.sqrt(np.maximum(intensity, 0) / 2)
        edge = np.clip((2.45 - np.abs(yy)) / 0.15, 0, 1)
        edge *= np.clip(t / 0.06, 0, 1)
        alpha = 195 * strength * edge

        upper = np.array([99, 236, 255])
        lower = np.array([196, 160, 255])
        mixture = (a[0][..., None] * upper + a[1][..., None] * lower)
        mixture /= (a[0] + a[1])[..., None] + 1e-12
        rgba = np.zeros((*xx.shape, 4), dtype=np.uint8)
        rgba[:, :, 3] = alpha.astype(np.uint8)
        self._alpha = alpha
        self._mixture = mixture
        self._carrier = 12 * (xx - x[0])
        self._fraction = t

        super().__init__(rgba)
        self.stretch_to_fit_width(x[-1] - x[0])
        self.stretch_to_fit_height(4.9)
        self.move_to([(x[-1] + x[0]) / 2, 0, 0])
        self._advance(self, 0)
        self.add_updater(self._advance)

    def _advance(self, mob, dt):
        mob.phase += 4.8 * dt * cfg.SPEED
        crest = (0.5 + 0.5 * np.cos(mob._carrier - mob.phase)) ** 3
        rgb = mob._mixture * (0.40 + 0.60 * crest[..., None])
        mob.pixel_array[:, :, :3] = rgb.astype(np.uint8)
        if mob.packet is not None:
            gate = np.exp(-0.5 * ((mob._fraction - mob.packet()) / 0.18) ** 2)
            mob.pixel_array[:, :, 3] = (mob._alpha * gate).astype(np.uint8)


def living_ring():
    """An outgoing standing-wave analogy: the nodes remain fixed."""
    angle = np.linspace(0, TAU, 481)
    group = VGroup(
        VMobject(stroke_color=LOWER_WAVE, stroke_width=14, stroke_opacity=0.13),
        VMobject(stroke_color=UPPER_WAVE, stroke_width=3.4),
    )
    group.phase = 0.0

    def advance(mob, dt):
        mob.phase += 2.3 * dt * cfg.SPEED
        radius = 2.3 + 0.26 * np.sin(5 * angle) * np.cos(mob.phase)
        points = np.column_stack((radius * np.cos(angle), radius * np.sin(angle),
                                  np.zeros_like(angle)))
        for curve in mob:
            curve.set_points_as_corners(points)

    advance(group, 0)
    group.add_updater(advance)
    return group
