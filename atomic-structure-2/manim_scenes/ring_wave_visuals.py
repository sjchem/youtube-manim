"""A live travelling wave on a ring for chapter 6's boundary-condition analogy.

The bright curve is one real-amplitude pattern. Faint phase-delayed echoes
are motion trails of that same pattern, not additional electron orbits.
An integer mode closes in both value and slope for every phase.
"""
from __future__ import annotations

import numpy as np
from manim import *
import config as cfg
from manim_scenes.common import glow_dot, outlined_text

WAVE_CYAN = "#74EEFF"
TRAIL_VIOLET = "#BCA3FF"
BRIGHT_GOLD = "#FFE693"
BRIGHT_WHITE = "#F3FCFF"
BRIGHT_GREEN = "#A0FFCA"
BRIGHT_CORAL = "#FF96A5"


def ring_points(mode, phase, radius=2.6, amplitude=0.36, center=ORIGIN, count=481):
    """Sample the amplitude radially, keeping both ends of the interval."""
    theta = np.linspace(0, TAU, count)
    r = radius + amplitude * np.sin(mode * theta - phase)
    return np.column_stack((r * np.cos(theta), r * np.sin(theta),
                            np.zeros_like(theta))) + np.asarray(center)


class WrappedWave(VGroup):
    """One continuously moving pattern around a fixed reference circumference."""

    def __init__(self, mode, radius=2.6, color=WAVE_CYAN):
        super().__init__()
        self.mode = mode
        self.phase = 0.0
        self.relative_amplitude = 0.36 / radius
        self.guide = Circle(radius=radius, stroke_color=WAVE_CYAN,
                            stroke_width=2, stroke_opacity=0.24)
        core = glow_dot(ORIGIN, radius=0.34, color="#FF496D")
        symbol = outlined_text("H", 28, BRIGHT_WHITE).move_to(ORIGIN)
        self.core = VGroup(core, symbol)
        self.echoes = VGroup(
            VMobject(stroke_color=TRAIL_VIOLET, stroke_width=2.1, stroke_opacity=0.13),
            VMobject(stroke_color=WAVE_CYAN, stroke_width=2.1, stroke_opacity=0.22),
        )
        self.bloom = VMobject(stroke_color=color, stroke_width=14, stroke_opacity=0.14)
        self.crest = VMobject(stroke_color=color, stroke_width=4.0)
        self.measure = VMobject(stroke_color=BRIGHT_GOLD, stroke_width=6,
                                stroke_opacity=0)
        self.add(self.guide, self.echoes, self.bloom, self.crest, self.measure, self.core)
        self._advance(self, 0)
        self.add_updater(self._advance)

    def _advance(self, _wave, dt):
        self.phase += dt * cfg.SPEED * 1.85
        radius = self.guide.width / 2
        centre = self.guide.get_center()
        mode = self.mode.get_value()
        amplitude = radius * self.relative_amplitude * (
            1 + 0.5 * min(max((mode - 1) / 3, 0), 1))
        # Higher modes get a larger illustrative displacement so their lobes
        # remain clear at preview resolution; the guide's radius never changes.
        # Sampling in the live guide's coordinates survives animated shifts
        # and scale changes without dragging the diagram back to the origin.
        for curve, lag in zip(self.echoes, (0.78, 0.38)):
            curve.set_points_as_corners(ring_points(
                mode, self.phase - lag, radius, amplitude, centre))
        points = ring_points(mode, self.phase, radius, amplitude, centre)
        self.bloom.set_points_as_corners(points)
        self.crest.set_points_as_corners(points)
        theta = np.linspace(self.phase * 0.6, self.phase * 0.6 + PI / 3, 65)
        arc = np.column_stack((radius * np.cos(theta), radius * np.sin(theta),
                               np.zeros_like(theta))) + centre
        self.measure.set_points_as_corners(arc)


def join_marker(wrapped, color):
    """Highlight the two ends, including their mismatch during phase motion."""
    halo = Circle(radius=0.50, color=color, stroke_width=2.4)
    halo.move_to(wrapped.guide.get_right())
    dots = VGroup(Dot(radius=0.05, color=BRIGHT_WHITE),
                  Dot(radius=0.05, color=color))
    bridge = VMobject(stroke_color=color, stroke_width=4)
    group = VGroup(halo.copy().set_stroke(width=12, opacity=0.10), halo, bridge, dots)

    def advance(_group, dt):
        first, last = wrapped.crest.get_start(), wrapped.crest.get_end()
        dots[0].move_to(first)
        dots[1].move_to(last)
        bridge.set_points_as_corners([first, last])

    advance(group, 0)
    group.add_updater(advance)
    return group
