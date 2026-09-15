"""Animated wave amplitude and a coherent finite-lattice diffraction model.

The lattice is a kinematic, far-field illustration, not a material-specific
electron-diffraction simulation. Drawing distances and playback times are
schematic. Detector samples and the angular field share one complex amplitude.
"""
from __future__ import annotations

from collections.abc import Callable
import numpy as np
from manim import *
import config as cfg

BRIGHT_CYAN = "#C6F3FF"
BRIGHT_GOLD = "#FFE895"


class TravellingWave(VGroup):
    """A live real-amplitude graph; the curve is never a particle trajectory."""

    def __init__(self, width=10.0, k=4.0, amplitude=0.62, center=ORIGIN,
                 color=BRIGHT_CYAN, packet: Callable[[], float] | None = None):
        super().__init__()
        self.wave_number = k
        self.amplitude = amplitude
        self.wave_center = np.asarray(center, dtype=float)
        self.x = np.linspace(-width / 2, width / 2, max(120, int(width / 0.025)))
        self.phase = 0.0
        self.packet = packet
        self.fill = VMobject(stroke_width=0, fill_color=color, fill_opacity=0.075)
        self.bloom = VMobject(stroke_color=color, stroke_width=13, stroke_opacity=0.12)
        self.crest = VMobject(stroke_color=color, stroke_width=3.5)
        self.add(self.fill, self.bloom, self.crest)
        self._advance(self, 0)
        self.add_updater(self._advance)

    def _advance(self, _wave, dt):
        k = self.wave_number() if callable(self.wave_number) else self.wave_number
        # omega proportional to k² supplies the free-particle dispersion in the
        # speed example. Absolute time is slowed for viewing.
        self.phase += min(9.0, 2.0 * (k / 4.0) ** 2) * dt * cfg.SPEED
        # Dense unresolved waves use a capped display frequency to avoid
        # temporal aliasing at 15 fps. The quantitative k=4 -> 8 example
        # retains omega proportional to k² throughout.
        if self.packet is not None:
            # The opening light packet has its carrier and envelope travel
            # together; there is no free-particle dispersion for this pulse.
            self.phase = k * (self.packet() - self.wave_center[0])
        envelope = 1.0
        if self.packet is not None:
            envelope = np.exp(-0.5 * ((self.x + self.wave_center[0] - self.packet()) / 0.7) ** 2)
        y = self.amplitude * envelope * np.sin(k * self.x - self.phase)
        points = np.column_stack((self.x, y, np.zeros_like(self.x))) + self.wave_center
        if self.packet is not None:
            # No straight gold line outside the pulse: draw just its luminous
            # envelope, so the light never resembles a bead on a rail.
            visible = np.abs(self.x + self.wave_center[0] - self.packet()) < 2.1
            points = points[visible]
        for curve in (self.bloom, self.crest):
            curve.set_points_as_corners(points)
        self.fill.set_points_as_corners(np.vstack([
            [points[0, 0], self.wave_center[1], 0], points,
            [points[-1, 0], self.wave_center[1], 0],
            [points[0, 0], self.wave_center[1], 0],
        ]))


class CrystalDiffraction:
    """Coherent elastic scattering from a small periodic 2D array.

    A(theta) = sum exp[i k ((1-cos(theta)) x_j - sin(theta) y_j)] / N.
    This is the incident/outgoing phase difference at every scattering site.
    A smooth atomic envelope reduces high-angle intensity. The screen samples
    |A|², rather than a hand-authored set of Gaussian peaks.
    """

    spacing = 0.66
    wavelength = 0.25
    screen_x = 5.05
    screen_y = np.linspace(-2.65, 2.65, 1401)

    def __init__(self):
        self.sites = np.array([[x, y, 0] for x in (-0.45, 0.0, 0.45)
                               for y in np.arange(-3, 4) * self.spacing])
        self.profile = self.intensity(self.screen_y)
        peaks = np.flatnonzero((self.profile[1:-1] > self.profile[:-2])
                              & (self.profile[1:-1] > self.profile[2:])) + 1
        strong = peaks[np.argsort(self.profile[peaks])[-3:]]
        self.maxima = np.sort(self.screen_y[strong])

    def amplitude(self, theta):
        theta = np.asarray(theta)
        phase = TAU / self.wavelength * (
            (1 - np.cos(theta))[..., None] * self.sites[:, 0]
            - np.sin(theta)[..., None] * self.sites[:, 1]
        )
        atomic_envelope = np.exp(-0.5 * (np.sin(theta) / 0.65) ** 2)
        return np.exp(1j * phase).mean(axis=-1) * atomic_envelope

    def intensity(self, y):
        return np.abs(self.amplitude(np.arctan2(y, self.screen_x))) ** 2

    def sample(self, rng, count):
        return rng.choice(self.screen_y, size=count, p=self.profile / self.profile.sum())

    def field(self):
        """Moving crests in the far-field angular pattern, stretched for viewing.

        Crest brightness displays phase evolution. The fixed angular envelope
        comes from |A|; it must not be mistaken for a changing detection rate.
        Alpha stays fixed so Manim can fade the image cleanly.
        """
        x = np.linspace(0.70, self.screen_x - 0.23, 340)
        y = np.linspace(2.65, -2.65, 360)
        xx, yy = np.meshgrid(x, y)
        theta = np.arctan2(yy, xx)
        amplitude = self.amplitude(theta)
        envelope = np.abs(amplitude)
        edge = np.clip((xx - 0.70) / 0.45, 0, 1)
        edge *= np.clip((2.65 - np.abs(yy)) / 0.22, 0, 1)
        rgba = np.zeros((*xx.shape, 4), dtype=np.uint8)
        rgba[:, :, 3] = (210 * envelope ** 0.65 * edge).astype(np.uint8)
        # The displayed crests are magnified; physical spacing is not to scale.
        carrier = 11.0 * np.hypot(xx, yy) + np.angle(amplitude)
        visual = ImageMobject(rgba).stretch_to_fit_width(x[-1] - x[0])
        visual.stretch_to_fit_height(5.3).move_to([(x[0] + x[-1]) / 2, 0, 0])
        visual.phase = 0.0

        def advance(mob, dt):
            mob.phase += 4.2 * dt * cfg.SPEED
            crest = (0.5 + 0.5 * np.cos(carrier - mob.phase)) ** 3
            rgb = np.array([100, 222, 255])[None, None, :] * (0.24 + 0.76 * crest[..., None])
            mob.pixel_array[:, :, :3] = rgb.astype(np.uint8)

        advance(visual, 0)
        visual.add_updater(advance)
        return visual

    def incoming(self):
        """Parallel incident wavefronts advance into the periodic lattice."""
        crests = VGroup(*[
            Line(UP * 2.1, DOWN * 2.1, color=BRIGHT_CYAN, stroke_width=2.4)
            for _ in range(9)
        ])
        crests.phase = 0.0

        def advance(mob, dt):
            mob.phase = (mob.phase + 0.32 * dt * cfg.SPEED) % 1
            for index, line in enumerate(mob):
                f = (mob.phase + index / len(mob)) % 1
                line.move_to([-5.9 + f * 4.95, 0, 0])
                line.set_stroke(opacity=0.50 * np.sin(PI * f) ** 0.5)

        advance(crests, 0)
        crests.add_updater(advance)
        return crests
