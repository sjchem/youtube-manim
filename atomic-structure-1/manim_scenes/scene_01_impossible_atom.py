"""Scene 01: the familiar atom, and the reason it should not survive a nanosecond."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    end_scene,
    fit_width,
    glowing_sphere,
    glow_dot,
    narration_wait,
    orbit_circle_3d,
    orbit_hold,
    outlined_text,
    paced_play,
    reset_flat_camera,
    set_3d_view,
    spiral_3d,
)
from utils.physics_models import ClassicalCollapse

COLLAPSE = ClassicalCollapse(display_radius=2.65, turns=5.0)


def _radiation_burst(center: np.ndarray, color: str = cfg.ORANGE) -> VGroup:
    """Three expanding rings: the energy an accelerating charge throws away."""
    rings = VGroup()
    for index in range(3):
        rings.add(
            Circle(
                radius=0.16 + 0.07 * index,
                color=color,
                stroke_width=5 - index,
                stroke_opacity=0.9,
                fill_opacity=0,
            ).move_to(center)
        )
    return rings


def _question_symbol(center: np.ndarray) -> VGroup:
    """A drawn question mark for the narration-led mystery."""
    hook = VMobject(color=cfg.GOLD, stroke_width=8)
    hook.start_new_path([-0.46, 0.45, 0])
    hook.add_cubic_bezier_curve_to([-0.46, 1.14, 0], [0.54, 1.14, 0], [0.54, 0.48, 0])
    hook.add_cubic_bezier_curve_to([0.54, 0.08, 0], [0.0, 0.16, 0], [0.0, -0.34, 0])
    dot = Dot([0.0, -0.72, 0], radius=0.075, color=cfg.GOLD)
    return VGroup(hook, dot).shift(center).set_z_index(5)


def _inspection_corners(center: np.ndarray) -> VGroup:
    """An incomplete viewing frame, not an assumed atomic boundary."""
    corners = VGroup()
    for xsign, ysign in ((-1, 1), (1, 1), (1, -1), (-1, -1)):
        corner = center + np.array([1.85 * xsign, 1.85 * ysign, 0])
        bracket = VMobject(color=cfg.CYAN, stroke_width=3, stroke_opacity=0.65)
        bracket.set_points_as_corners([
            corner - np.array([0.46 * xsign, 0, 0]),
            corner,
            corner - np.array([0, 0.46 * ysign, 0]),
        ])
        corners.add(bracket)
    return corners.set_z_index(4)


def _probe_path(height: float, exit_height: float) -> VMobject:
    """Illustrative input/output clue; the hidden interaction is not revealed."""
    path = VMobject(color=cfg.CYAN, stroke_width=2.4, stroke_opacity=0.42)
    path.start_new_path([-6.35, height, 0])
    path.add_line_to(np.array([-0.45, height, 0]))
    path.add_cubic_bezier_curve_to([0.1, height, 0], [2.0, exit_height, 0], [2.75, exit_height, 0])
    path.add_line_to(np.array([5.85, exit_height, 0]))
    return path.set_z_index(1)


class Scene01ImpossibleAtom(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "01")
    set_3d_view(scene, phi=64 * DEGREES, theta=-62 * DEGREES)

    # -- Beat 1: the picture everybody already has ---------------------------
    core = glowing_sphere(0.42, cfg.NUCLEUS_COLOR, resolution=(20, 40), shells=2)
    ring = orbit_circle_3d(COLLAPSE.display_radius, cfg.MUTED, stroke_width=3.2)
    bead = glowing_sphere(0.17, cfg.ELECTRON_COLOR, resolution=(16, 32), shells=2)
    bead.move_to([COLLAPSE.display_radius, 0, 0])

    paced_play(scene, FadeIn(core, scale=1.3), run_time=1.0)
    paced_play(scene, Create(ring), FadeIn(bead, scale=1.4), run_time=1.2)
    paced_play(scene, Rotating(bead, angle=TAU * 0.9, about_point=ORIGIN, axis=OUT), run_time=5.5, rate_func=linear)

    # -- Beat 2: an orbiting charge is an accelerating charge, so it radiates --
    bursts = VGroup()
    for index in range(3):
        angle = TAU * (0.9 + 0.26 * index)
        point = COLLAPSE.display_radius * np.array([np.cos(angle), np.sin(angle), 0.0])
        bursts.add(_radiation_burst(point))
    scene.add(bursts)

    emissions = [
        burst.animate(run_time=1.9, rate_func=rate_functions.ease_out_sine)
        .scale(6.5)
        .set_stroke(opacity=0.0)
        for burst in bursts
    ]
    paced_play(
        scene,
        Rotating(bead, angle=TAU * 1.15, about_point=ORIGIN, axis=OUT),
        LaggedStart(*emissions, lag_ratio=0.45),
        run_time=6.5,
        rate_func=linear,
    )
    scene.remove(bursts)

    # -- Beat 3: energy leaves, so the orbit cannot hold its radius ------------
    spiral_points = COLLAPSE.spiral(620)
    spiral = spiral_3d(spiral_points, cfg.ORANGE, stroke_width=4.0)
    bead.move_to([spiral_points[0][0], spiral_points[0][1], 0.0])
    trail = spiral.copy().set_stroke(cfg.ORANGE, width=16, opacity=0.10)

    paced_play(scene, FadeOut(ring), run_time=0.5)
    paced_play(
        scene,
        Create(trail),
        Create(spiral),
        MoveAlongPath(bead, spiral),
        run_time=11.4,
        rate_func=rate_functions.ease_in_quad,
    )

    # -- Beat 4: it hits the nucleus ------------------------------------------
    flash = Circle(radius=0.3, color=cfg.WHITE, stroke_width=8, fill_color=cfg.WHITE, fill_opacity=0.55)
    scene.add(flash)
    paced_play(
        scene,
        flash.animate.scale(9.0).set_stroke(opacity=0).set_fill(opacity=0),
        FadeOut(bead, scale=0.2),
        run_time=0.9,
    )
    scene.remove(flash)
    orbit_hold(scene, 1.9)
    paced_play(scene, FadeOut(spiral, trail, core), run_time=0.8)

    # -- Beat 5: the atom remains a visual question, not a text card -----------
    reset_flat_camera(scene)
    add_cinematic_background(scene)
    target_center = np.array([1.15, 0.0, 0.0])
    # This opaque mask conceals the interaction. No nucleus, model sequence,
    # or quantum orbital is revealed before the story earns those pictures.
    hidden = Circle(radius=1.58, stroke_width=0, fill_color="#061522", fill_opacity=1)
    hidden.move_to(target_center).set_z_index(3)
    corners = _inspection_corners(target_center)
    question = _question_symbol(target_center)
    paced_play(scene, FadeIn(hidden), Create(corners), run_time=1.4)
    paced_play(scene, Create(question), run_time=1.0)
    narration_wait(scene, 2.0)

    # -- Beat 6: the promise is spoken while measurements begin ---------------
    emitter = RoundedRectangle(width=0.30, height=3.15, corner_radius=0.10,
                               color=cfg.CYAN, stroke_width=2, fill_color=cfg.PANEL, fill_opacity=0.7)
    emitter.move_to([-6.5, 0, 0])
    detector = Line([5.85, -2.25, 0], [5.85, 2.5, 0], color=cfg.MUTED, stroke_width=4)
    paced_play(scene, FadeIn(emitter, shift=RIGHT * 0.15), run_time=1.0)
    paced_play(scene, Create(detector), run_time=1.2)

    tracks = VGroup()
    detections = VGroup()
    for height, exit_height in ((-1.0, -1.15), (0.0, 0.45), (1.0, 1.9)):
        path = _probe_path(height, exit_height)
        probe = Dot(path.get_start(), radius=0.075, color=cfg.CYAN).set_z_index(2)
        tracks.add(path)
        scene.add(probe)
        paced_play(scene, Create(path), MoveAlongPath(probe, path), run_time=2.2, rate_func=linear)
        scene.remove(probe)
        hit = glow_dot(path.get_end(), cfg.GREEN, 0.07).set_z_index(4)
        detections.add(hit)
        paced_play(scene, FadeIn(hit, scale=1.7), run_time=0.45)
        narration_wait(scene, 1.2)

    # -- Beat 7: seeing effects still leaves the inside an open question -------
    scan = Line(target_center + [-1.45, -1.5, 0], target_center + [1.45, -1.5, 0],
                color=cfg.CYAN, stroke_width=2, stroke_opacity=0.35).set_z_index(4)
    paced_play(scene, FadeIn(scan), run_time=0.5)
    paced_play(scene, scan.animate.shift(UP * 3.0), run_time=3.0,
               rate_func=rate_functions.ease_in_out_sine)
    paced_play(scene, FadeOut(scan), run_time=0.5)
    paced_play(scene, LaggedStart(*[Indicate(hit, color=cfg.WHITE, scale_factor=1.3)
                                   for hit in detections], lag_ratio=0.5), run_time=2.4)
    narration_wait(scene, 2.0)

    # -- Beat 8: resolve the opening into the film's title --------------------
    # Use the existing closing window so the narration timing stays intact.
    paced_play(scene, Indicate(question, color=cfg.WHITE, scale_factor=1.12), run_time=0.8)
    paced_play(scene, FadeOut(hidden, corners, question, tracks, detections, emitter, detector),
               run_time=0.7)
    title = VGroup(
        outlined_text("How We Discovered", cfg.FONT["section"], cfg.WHITE),
        outlined_text("What an Atom Looks Like", cfg.FONT["title"], cfg.GOLD),
    ).arrange(DOWN, buff=0.35)
    fit_width(title, 13.4)
    rule = Line(LEFT * 2.4, RIGHT * 2.4, color=cfg.CYAN, stroke_width=3)
    VGroup(title, rule).arrange(DOWN, buff=0.55).move_to(ORIGIN)
    paced_play(scene, FadeIn(title, shift=UP * 0.18), Create(rule), run_time=1.1)
    narration_wait(scene, 4.0)
    end_scene(scene, started, cfg.SCENE_DURATIONS["01"])
