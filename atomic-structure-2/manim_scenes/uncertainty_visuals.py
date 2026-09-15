"""Live chapter-seven diagrams; animation time and plot axes are schematic.

The packet is a family of Gaussian states, not a free packet evolving in time.
A global phase animates Re(psi) while leaving its envelope and |psi|² intact.
Changing sigma compares prepared states; sigma_p = 1 / (2 sigma_x).
"""
from __future__ import annotations

import numpy as np
from manim import *
import config as cfg
from manim_scenes.common import equation
from utils.physics_models import sigma_p

CYAN = "#A3F1FF"
GOLD = "#FFE69A"
MINT = "#9DFFCB"
VIOLET = "#D6B3FF"
CORAL = "#FFA3B4"


def bright_math(latex, size=48, color=CYAN):
    """Reinforce thin mathematical strokes at preview resolution."""
    result = equation(latex, size, color)
    result.set_stroke(color, width=0.35, opacity=1)
    return result


class OrbitMotion(VMobject):
    """Drive the bead and its radial/tangent vectors even through a fade."""

    def __init__(self, atom):
        super().__init__()
        self.atom = atom
        self.phase = 0.0
        self.vectors = None
        self.labels = None
        self.marker = None
        atom[2].add(Dot(atom[2].get_center(), radius=0.045, color=WHITE))
        self.add_updater(self.advance)

    def advance(self, _, dt):
        self.phase += dt * cfg.SPEED * TAU / 7.5
        ring, bead = self.atom[1], self.atom[2]
        centre = ring.get_center()
        radial = np.array([np.cos(self.phase), np.sin(self.phase), 0])
        tangent = np.array([-radial[1], radial[0], 0])
        point = centre + ring.width / 2 * radial
        bead.move_to(point)
        if self.vectors is not None:
            self.vectors[0].put_start_and_end_on(centre + radial * 0.32,
                                                point - radial * 0.18)
            self.vectors[1].put_start_and_end_on(point + tangent * 0.19,
                                                point + tangent * 1.35)
        if self.labels is not None:
            self.labels[0].move_to(centre + radial * 1.15 - tangent * 0.36)
            self.labels[1].move_to(point + tangent * 0.83 + radial * 0.44)
        if self.marker is not None:
            self.marker[0].move_to(point)
            self.marker[1].put_start_and_end_on(point + tangent * 0.20,
                                               point + tangent * 1.45)


class GaussianPanels(VGroup):
    """Animate only global wave phase; preserve reciprocal distribution widths."""

    def __init__(self, width, scale=1.0, center=ORIGIN):
        super().__init__()
        self.width_tracker = width
        self.phase = 0.0
        self.plot_scale = scale
        self.offset = np.array(center, dtype=float)
        self.x = np.linspace(-5.8, 5.8, 465)
        self.amplitude = VMobject(stroke_color=CYAN, stroke_width=3.8)
        self.bloom = VMobject(stroke_color=CYAN, stroke_width=12, stroke_opacity=0.12)
        self.envelope = VMobject(stroke_color=MINT, stroke_width=2, stroke_opacity=0.62)
        self.momentum = VMobject(stroke_color=VIOLET, stroke_width=4)
        self.momentum_glow = VMobject(stroke_color=VIOLET, stroke_width=13, stroke_opacity=0.12)
        self.fill = VMobject(stroke_width=0, fill_color=VIOLET, fill_opacity=0.09)
        self.axes = VGroup(*[
            Line(self.map_point([-5.8, y, 0]), self.map_point([5.8, y, 0]),
                 stroke_color=color, stroke_width=1.2, stroke_opacity=0.27)
            for y, color in ((1.7, CYAN), (-1.45, VIOLET))
        ])
        self.add(self.axes, self.fill, self.bloom, self.envelope,
                 self.amplitude, self.momentum_glow, self.momentum)
        self.advance(self, 0)
        self.add_updater(self.advance)

    def map_point(self, points):
        return np.asarray(points) * self.plot_scale + self.offset

    def advance(self, _, dt):
        self.phase += dt * cfg.SPEED * 2.8
        sigma = self.width_tracker.get_value()
        envelope = np.exp(-self.x**2 / (4 * sigma**2))
        # A global phase changes the real part, never the probability density.
        y = 1.7 + 0.75 * envelope * np.cos(7 * self.x - self.phase)
        points = self.map_point(np.column_stack((self.x, y, np.zeros_like(y))))
        for curve in (self.amplitude, self.bloom):
            curve.set_points_as_corners(points)
        upper = self.map_point(np.column_stack(
            (self.x, 1.7 + 0.75 * envelope, np.zeros_like(y))))
        self.envelope.set_points_as_corners(upper)
        spread = float(sigma_p(sigma))
        momentum_y = -1.45 + 1.25 * np.exp(-self.x**2 / (2 * spread**2))
        points_p = self.map_point(np.column_stack((self.x, momentum_y, np.zeros_like(y))))
        for curve in (self.momentum, self.momentum_glow):
            curve.set_points_as_corners(points_p)
        self.fill.set_points_as_corners(np.vstack((
            self.map_point([-5.8, -1.45, 0]), points_p,
            self.map_point([5.8, -1.45, 0]), self.map_point([-5.8, -1.45, 0]),
        )))
