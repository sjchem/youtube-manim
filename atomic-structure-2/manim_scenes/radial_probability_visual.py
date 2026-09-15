"""Linked density slice, radial distribution and spherical probability.

The moving circle is a section of a spherical boundary. Shaded area under
the radial curve represents the full three-dimensional enclosed probability.
"""
from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import QuantumScene, density_slice, equation, glow_dot, outlined_text, radial_plot
from utils.physics_models import radial_distribution
from utils.quantum_examples import hydrogen_1s_cumulative, hydrogen_1s_probability_radius


def radial_probability_demo(scene: QuantumScene) -> None:
    """A short worked example in a flat camera, with a clean exit."""
    left = np.array([-3.75, -0.10, 0.0])
    size = 5.6
    radius = ValueTracker(1.0)
    density = density_slice(1, 0, 0, size=size).move_to(left)
    nucleus = glow_dot(left, 0.095, cfg.NUCLEUS_COLOR)
    plot = radial_plot([(1, 0)], span=5, width=5.5, height=2.65,
                       center=[3.45, -0.20, 0])
    axes = plot.axes
    headings = VGroup(
        outlined_text("DENSITY", 32, cfg.CYAN).move_to([-3.75, 3.50, 0]),
        outlined_text("PROBABILITY BY RADIUS", 32, cfg.GOLD).move_to([3.45, 3.50, 0]),
    )
    laws = VGroup(
        equation(r"\rho=|\psi_{1s}|^2", 48, cfg.CYAN).move_to([-3.75, 2.65, 0]),
        equation(r"P(r)=4\pi r^2\rho(r)", 48, cfg.GOLD).move_to([3.45, 2.65, 0]),
    )
    scale = VGroup(*[
        equation(str(n), 25, cfg.MUTED).next_to(axes.c2p(n, 0), DOWN, buff=0.18)
        for n in range(6)
    ])
    scale.add(equation(r"r/a_0", 28, cfg.MUTED).next_to(scale, RIGHT, buff=0.2))
    scene.show(density, seconds=0.7)
    for mob in (nucleus, plot, headings, laws, scale):
        scene.show(mob, seconds=0.35)

    def boundary() -> Circle:
        return Circle(radius=radius.get_value() * size / 8.4, color=cfg.GOLD,
                      stroke_width=3.5).move_to(left)

    def filled_probability() -> VMobject:
        xs = np.linspace(0, radius.get_value(), 90)
        points = [axes.c2p(0, 0)] + [axes.c2p(x, float(radial_distribution(1, 0, x))) for x in xs]
        points.append(axes.c2p(radius.get_value(), 0))
        return Polygon(*points, stroke_width=0, fill_color=cfg.GOLD, fill_opacity=0.28)

    ring = always_redraw(boundary)
    area = always_redraw(filled_probability)
    guide = always_redraw(lambda: DashedLine(
        axes.c2p(radius.get_value(), 0),
        axes.c2p(radius.get_value(), float(radial_distribution(1, 0, radius.get_value()))),
        color=cfg.GOLD, stroke_width=3))
    readout = VGroup(
        equation(r"R/a_0 =", 36, cfg.GOLD),
        DecimalNumber(1, num_decimal_places=2, font_size=36, color=cfg.GOLD),
    ).arrange(RIGHT, buff=0.2).move_to([-3.75, -3.15, 0])
    percent = VGroup(
        DecimalNumber(100 * hydrogen_1s_cumulative(1), num_decimal_places=1,
                      font_size=45, color=cfg.GREEN),
        outlined_text("% inside the sphere", 28, cfg.GREEN),
    ).arrange(RIGHT, buff=0.2).move_to([3.45, -3.15, 0])
    readout[1].add_updater(lambda mob: mob.set_value(radius.get_value()))
    percent[0].add_updater(lambda mob: mob.set_value(100 * hydrogen_1s_cumulative(radius.get_value())))
    for mob in (area, guide, ring, readout, percent):
        scene.show(mob, seconds=0.3)
    peak = scene.pin(outlined_text("most probable radius ≠ a fixed orbit", 30, cfg.WHITE)
                     .move_to([0, -3.85, 0]))
    scene.playq(FadeIn(peak), seconds=0.5)
    scene.hold(6.0)
    scene.playq(radius.animate.set_value(hydrogen_1s_probability_radius()),
                seconds=6.0, rate_func=smooth)
    scene.hold(3.0)
    scene.playq(Indicate(ring, color=cfg.WHITE, scale_factor=1),
                Indicate(percent, color=cfg.WHITE, scale_factor=1.04), seconds=1.0)
    tail_note = outlined_text("10% remains outside this boundary", 30, cfg.WHITE).move_to(peak)
    scene.playq(Transform(peak, tail_note), seconds=0.6)
    scene.hold(6.0)
    for mob in (area, guide, ring, readout, percent):
        mob.clear_updaters(recursive=True)
    scene.drop(density, nucleus, plot, headings, laws, scale, area, guide, ring,
               readout, percent, peak, seconds=0.7)
