"""Scene 11: spin a curve, slice the solid, and integration builds a volume."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    area_region,
    begin_scene,
    bottom_caption,
    calc_axes,
    disk_stack,
    end_scene,
    fitted_eq,
    hide_background,
    labelled_axes,
    move_3d_view,
    narration_wait,
    orbit_hold,
    paced_play,
    pin_to_frame,
    restore_background,
    revolution_surface,
    set_3d_view,
    three_d_axes,
)
from utils.math_utils import disk_sum_volume, sphere_volume
from utils.physics_models import SolidOfRevolution

BALL = SolidOfRevolution(radius=1.0)
AXIS_UNIT = 2.20
DISK_STAGES = (7, 14, 28)


def _closing_sliced_sphere() -> VGroup:
    """A flat, luminous summary of the 3D sphere assembled from disk slices."""
    radius = 1.68
    shadow = Ellipse(
        width=3.35,
        height=0.34,
        fill_color=BLACK,
        fill_opacity=0.34,
        stroke_width=0,
    ).shift(DOWN * 1.84 + RIGHT * 0.12)
    halo = VGroup(
        Circle(radius=radius * 1.10, color=cfg.GREEN, stroke_width=24, stroke_opacity=0.035),
        Circle(radius=radius * 1.04, color=cfg.CYAN, stroke_width=12, stroke_opacity=0.08),
    )
    shell = Circle(
        radius=radius,
        color=cfg.GREEN,
        stroke_width=5,
        fill_color=cfg.BLUE,
        fill_opacity=0.18,
    )
    inner_light = Circle(
        radius=radius * 0.78,
        color=cfg.CYAN,
        stroke_width=0,
        fill_color=cfg.CYAN,
        fill_opacity=0.045,
    ).shift(LEFT * 0.23 + UP * 0.20)
    slices = VGroup()
    for height in np.linspace(-1.35, 1.35, 11):
        half_width = float(np.sqrt(max(radius**2 - height**2, 0.0)))
        slices.add(
            Ellipse(
                width=2 * half_width,
                height=0.10 + 0.08 * half_width / radius,
                color=cfg.GOLD,
                stroke_width=2.5,
                stroke_opacity=0.55,
            ).shift(UP * height)
        )
    equator = Ellipse(width=2 * radius, height=0.26, color=cfg.GOLD, stroke_width=4, stroke_opacity=0.88)
    highlight = Arc(
        radius=radius * 0.88,
        start_angle=112 * DEGREES,
        angle=105 * DEGREES,
        color=cfg.WHITE,
        stroke_width=5,
        stroke_opacity=0.34,
    )
    return VGroup(shadow, halo, shell, inner_light, slices, equator, highlight)


class Scene11AreaToVolume(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "11")
    background = add_cinematic_background(scene)

    # -- Beat 1: an unremarkable curve ----------------------------------------
    flat_axes = calc_axes((-1.6, 1.6, 0.5), (-0.4, 1.6, 0.5), 8.0, 4.4).move_to([0, -0.85, 0])
    flat_labels = labelled_axes(flat_axes, "x", "y", cfg.MUTED, cfg.FONT["small"])
    profile = flat_axes.plot(BALL.profile, x_range=[-1, 1], color=cfg.CYAN, stroke_width=7)
    formula = fitted_eq(r"y=\sqrt{1-x^{2}}", cfg.CYAN, cfg.FONT["title"], width=6.0).to_edge(UP, buff=0.45)
    paced_play(scene, Create(flat_axes), FadeIn(flat_labels), run_time=1.0)
    paced_play(scene, Create(profile), FadeIn(formula, shift=DOWN * 0.12), run_time=1.6)
    narration_wait(scene, 5.0)

    shade = area_region(flat_axes, profile, -1, 1, cfg.BLUE, 0.30)
    paced_play(scene, FadeIn(shade), run_time=1.0)
    narration_wait(scene, 4.4)

    spin_caption = bottom_caption("Now spin it around the x-axis.", cfg.GOLD)
    paced_play(scene, FadeIn(spin_caption), run_time=0.8)
    narration_wait(scene, 4.4)
    paced_play(scene, FadeOut(VGroup(flat_axes, flat_labels, profile, shade, spin_caption, formula)), run_time=0.8)

    # -- Beat 2: the curve sweeps out a solid ----------------------------------
    hide_background(scene)
    # A shorter vertical range keeps the z-axis clear of the pinned equations
    # at the top and bottom of the frame.
    axes = three_d_axes((-1.9, 1.9, 1), (-1.9, 1.9, 1), (-1.5, 1.5, 1), unit=AXIS_UNIT)
    arc = ParametricFunction(
        lambda s: axes.c2p(-np.cos(s), np.sin(s), 0.0),
        t_range=[0, PI],
        color=cfg.CYAN,
        stroke_width=7,
    )
    # theta near -90 deg puts the x-axis across the screen, which is what makes
    # the disk stack read as a stack rather than as concentric rings.
    set_3d_view(scene, phi=66 * DEGREES, theta=-84 * DEGREES)
    paced_play(scene, Create(axes), Create(arc), run_time=1.6)

    sweep_caption = bottom_caption("One curve, one full turn.", cfg.CYAN)
    pin_to_frame(scene, sweep_caption)
    paced_play(scene, FadeIn(sweep_caption), run_time=0.7)
    paced_play(
        scene,
        Rotate(arc, angle=TAU, axis=RIGHT, about_point=axes.c2p(0, 0, 0)),
        run_time=4.6,
        rate_func=rate_functions.ease_in_out_sine,
    )

    sphere = revolution_surface(axes, BALL.profile, -1.0, 1.0, resolution=(22, 40), color=cfg.BLUE, opacity=0.5)
    paced_play(scene, FadeIn(sphere), FadeOut(arc), run_time=1.4)
    orbit_hold(scene, 5.4)
    paced_play(scene, FadeOut(sweep_caption), run_time=0.5)

    # -- Beat 3: slice it into coins --------------------------------------------
    slice_caption = bottom_caption("Slice it into thin disks.", cfg.GOLD)
    pin_to_frame(scene, slice_caption)
    stack = disk_stack(axes, BALL.profile, DISK_STAGES[0], color=cfg.GOLD, opacity=0.72)
    paced_play(scene, FadeIn(slice_caption), FadeOut(sphere), FadeIn(stack), run_time=1.4)
    orbit_hold(scene, 4.6)

    disk_rule = fitted_eq(r"dV=\pi y^{2}\,dx", cfg.GOLD, cfg.FONT["title"], width=6.0).to_edge(UP, buff=0.45)
    pin_to_frame(scene, disk_rule)
    paced_play(scene, FadeIn(disk_rule, shift=DOWN * 0.12), run_time=1.0)
    orbit_hold(scene, 5.4)

    def _tally(count: int) -> MathTex:
        """What the disk stack itself is worth, straight from the midpoint sum."""
        return fitted_eq(
            rf"{count}\ \text{{disks}}:\ V\approx {disk_sum_volume(count):.3f}",
            cfg.WHITE,
            cfg.FONT["small"],
            width=5.6,
        ).to_corner(UL, buff=0.55)

    tally = _tally(DISK_STAGES[0])
    pin_to_frame(scene, tally)
    paced_play(scene, FadeIn(tally), run_time=0.7)
    for count in DISK_STAGES[1:]:
        finer = disk_stack(axes, BALL.profile, count, color=cfg.GOLD, opacity=0.72)
        next_tally = _tally(count)
        pin_to_frame(scene, next_tally)
        paced_play(scene, FadeTransform(stack, finer), FadeTransform(tally, next_tally), run_time=1.5)
        stack, tally = finer, next_tally
    orbit_hold(scene, 5.0)

    # -- Beat 4: the substitution that makes the integral easy --------------------
    substitution = fitted_eq(r"y^{2}=1-x^{2}", cfg.CYAN, cfg.FONT["section"], width=5.0).to_edge(DOWN, buff=0.50)
    pin_to_frame(scene, substitution)
    paced_play(scene, FadeOut(slice_caption), FadeIn(substitution, shift=UP * 0.12), run_time=1.0)
    orbit_hold(scene, 4.6)

    integral = fitted_eq(r"V=\int_{-1}^{1}\pi\,(1-x^{2})\,dx", cfg.WHITE, cfg.FONT["title"], width=8.6).to_edge(UP, buff=0.45)
    pin_to_frame(scene, integral)
    paced_play(scene, FadeOut(disk_rule), FadeIn(integral, shift=DOWN * 0.12), run_time=1.2)
    orbit_hold(scene, 5.4)

    # -- Beat 5: the value, and the solid put back together ----------------------
    answer = fitted_eq(
        rf"V=\frac{{4\pi}}{{3}}\approx {sphere_volume():.3f}",
        cfg.GREEN,
        cfg.FONT["title"],
        width=7.0,
    ).to_edge(DOWN, buff=0.45)
    pin_to_frame(scene, answer)
    paced_play(scene, FadeOut(substitution), FadeOut(tally), FadeIn(answer, shift=UP * 0.12), run_time=1.2)
    orbit_hold(scene, 4.6)

    rebuilt = revolution_surface(axes, BALL.profile, -1.0, 1.0, resolution=(22, 40), color=cfg.GREEN, opacity=0.5)
    paced_play(scene, FadeTransform(stack, rebuilt), run_time=2.0)
    move_3d_view(scene, phi=58 * DEGREES, theta=-140 * DEGREES, run_time=5.0)
    narration_wait(scene, 4.0)

    paced_play(scene, FadeOut(VGroup(axes, rebuilt, integral, answer)), run_time=0.8)
    restore_background(scene, background)

    summary_sphere = _closing_sliced_sphere().move_to([-3.75, 0.35, 0])
    summary_integral = fitted_eq(
        r"V=\int_{-1}^{1}\pi(1-x^2)\,dx",
        cfg.WHITE,
        cfg.FONT["section"],
        width=6.2,
    )
    summary_arrow = fitted_eq(r"\Downarrow", cfg.GOLD, cfg.FONT["title"], width=1.0)
    summary_answer = fitted_eq(r"V=\frac{4\pi}{3}", cfg.GREEN, cfg.FONT["hero"], width=4.8)
    summary_math = VGroup(summary_integral, summary_arrow, summary_answer).arrange(DOWN, buff=0.34).move_to([3.45, 0.42, 0])
    answer_plate = SurroundingRectangle(
        summary_answer,
        color=cfg.GREEN,
        buff=0.26,
        corner_radius=0.15,
        stroke_width=3,
        fill_color=cfg.PANEL,
        fill_opacity=0.38,
    )
    verdict = bottom_caption("Tiny pieces, understood one at a time, then added back up.", cfg.GOLD)
    paced_play(
        scene,
        FadeIn(summary_sphere, scale=1.04),
        FadeIn(summary_math, shift=UP * 0.10),
        FadeIn(answer_plate),
        FadeIn(verdict),
        run_time=0.9,
    )
    narration_wait(scene, 5.0)

    end_scene(scene, started, cfg.SCENE_DURATIONS["11"])
