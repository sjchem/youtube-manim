"""Scene 08: Rutherford's atom is beautiful, and by the physics of its own day, impossible."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    cross_mark,
    electron,
    end_scene,
    eq,
    fit_width,
    halo,
    narration_wait,
    orbit_ring,
    outlined_text,
    paced_play,
    planetary_atom,
    polyline,
    top_caption,
)
from utils.physics_models import ClassicalCollapse

COLLAPSE = ClassicalCollapse(display_radius=2.30, turns=5.0)
ORBIT_CENTER = np.array([0.0, 0.25, 0.0])
VELOCITY_COLOR = "#B8F3FF"
ACCELERATION_COLOR = "#FFE69B"
RADIATION_COLOR = "#FFB5BD"


def _sun_and_planet(radius: float = 1.45) -> tuple[VGroup, VGroup]:
    sun = VGroup(halo(0.42, cfg.GOLD, 4, 0.20), Dot(ORIGIN, radius=0.42, color=cfg.GOLD))
    path = orbit_ring(radius, cfg.MUTED, stroke_width=2.2, opacity=0.45)
    planet = VGroup(halo(0.15, cfg.BLUE, 3, 0.18), Dot(ORIGIN, radius=0.15, color=cfg.BLUE))
    planet.move_to([radius, 0, 0])
    return VGroup(sun, path, planet), planet


class Scene08UnstableAtom(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "08")
    add_cinematic_background(scene)

    # -- Beat 1: it looks exactly like a solar system --------------------------
    heading = top_caption("A MINIATURE SOLAR SYSTEM?", cfg.GOLD)
    paced_play(scene, FadeIn(heading), run_time=0.8)

    solar, planet = _sun_and_planet(1.45)
    solar.move_to([-3.9, 0.20, 0])
    atom, core, ring, bead = planetary_atom(orbit_radius=1.45, nucleus_radius=0.30, electron_radius=0.17)
    atom.move_to([3.9, 0.20, 0])

    paced_play(scene, FadeIn(solar, scale=1.1), run_time=1.0)
    paced_play(scene, FadeIn(atom, scale=1.1), run_time=1.0)
    paced_play(
        scene,
        Rotating(planet, angle=TAU * 0.7, about_point=solar[0].get_center(), axis=OUT),
        Rotating(bead, angle=TAU * 0.7, about_point=core.get_center(), axis=OUT),
        run_time=4.4,
        rate_func=linear,
    )
    narration_wait(scene, 7.0)

    difference = bottom_caption("gravity holds planets; electric forces bind electrons", cfg.ORANGE)
    paced_play(scene, FadeIn(difference), run_time=0.8)
    narration_wait(scene, 6.2)
    paced_play(scene, FadeOut(solar, difference, heading), run_time=0.7)
    paced_play(scene, atom.animate.scale(1.35, about_point=core.get_center()).shift(ORBIT_CENTER-core.get_center()), run_time=1.1)

    # -- Beat 2: going round a circle is accelerating -------------------------
    orbit_radius = 1.45 * 1.35
    offset = bead.get_center() - ORBIT_CENTER
    initial_angle = float(np.arctan2(offset[1], offset[0]))
    angle = ValueTracker(initial_angle)

    def position() -> np.ndarray:
        theta = angle.get_value()
        return ORBIT_CENTER + orbit_radius * np.array([np.cos(theta), np.sin(theta), 0.0])

    scene.remove(bead)
    live_bead = always_redraw(lambda: electron(0.17).move_to(position()))
    velocity = always_redraw(
        lambda: Arrow(
            position(),
            position() + 1.05 * np.array([-np.sin(angle.get_value()), np.cos(angle.get_value()), 0.0]),
            color=VELOCITY_COLOR, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.28,
        )
    )
    acceleration = always_redraw(
        lambda: Arrow(
            position(),
            position() + 0.85 * (ORBIT_CENTER - position()) / orbit_radius,
            color=ACCELERATION_COLOR, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.30,
        )
    )
    scene.add(live_bead, velocity)
    v_label = eq(r"\vec{v}", VELOCITY_COLOR, 78).move_to([-4.6, 2.35, 0])
    a_label = eq(r"\vec{a}", ACCELERATION_COLOR, 78).move_to([-4.6, 1.05, 0])
    paced_play(scene, FadeIn(v_label), run_time=0.6)
    paced_play(scene, angle.animate.set_value(initial_angle + TAU * 0.55), run_time=3.4, rate_func=linear)
    scene.add(acceleration)
    paced_play(scene, FadeIn(a_label), run_time=0.6)
    turning = bottom_caption("the direction keeps changing, so it is accelerating", cfg.CYAN)
    paced_play(scene, FadeIn(turning), run_time=0.8)
    paced_play(scene, angle.animate.set_value(initial_angle + TAU * 1.35), run_time=4.6, rate_func=linear)
    narration_wait(scene, 5.6)

    # -- Beat 3: an accelerating charge radiates -------------------------------
    paced_play(scene, FadeOut(turning), run_time=0.5)
    law = VGroup(
        outlined_text("Accelerating charge", 40, RADIATION_COLOR),
        eq(r"\Rightarrow", cfg.WHITE, 54),
        outlined_text("Radiates energy", 40, RADIATION_COLOR),
    ).arrange(RIGHT, buff=0.28)
    fit_width(law, cfg.SAFE_WIDTH - 0.6)
    law.move_to([0, -3.05, 0])
    paced_play(scene, FadeIn(law, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 5.8)

    chain = VGroup(
        eq(r"E \downarrow", ACCELERATION_COLOR, 72),
        eq(r"r \downarrow", RADIATION_COLOR, 72),
    ).arrange(RIGHT, buff=1.30).move_to([4.55, 2.35, 0])
    link = Arrow(chain[0].get_right(), chain[1].get_left(), color=cfg.WHITE,
                 buff=0.22, stroke_width=4, max_tip_length_to_length_ratio=0.28)
    paced_play(scene, FadeIn(chain[0], scale=1.15), run_time=0.8)
    paced_play(scene, GrowArrow(link), FadeIn(chain[1], scale=1.15), run_time=0.9)
    narration_wait(scene, 5.4)

    # -- Beat 4: so it falls in ------------------------------------------------
    for mob in (live_bead, velocity, acceleration):
        mob.clear_updaters()
    paced_play(scene, FadeOut(velocity, acceleration, v_label, a_label, law), run_time=0.6)
    scene.remove(live_bead, ring)

    # Match the current orbit's radius and phase, so the electron never jumps
    # outward and the spiral stays clear of the corner labels.
    spiral_points = COLLAPSE.spiral(560) * (orbit_radius / COLLAPSE.display_radius)
    start_phase = float(np.arctan2(spiral_points[0, 1], spiral_points[0, 0]))
    phase = angle.get_value() - start_phase
    rotation = np.array([[np.cos(phase), -np.sin(phase)],
                         [np.sin(phase), np.cos(phase)]])
    spiral_points = spiral_points @ rotation.T
    spiral_points[:, 0] += ORBIT_CENTER[0]
    spiral_points[:, 1] += ORBIT_CENTER[1]
    spiral = polyline(spiral_points, cfg.ORANGE, stroke_width=4.0)
    falling = electron(0.17).move_to([spiral_points[0][0], spiral_points[0][1], 0.0])
    scene.add(falling)
    paced_play(
        scene,
        Create(spiral),
        MoveAlongPath(falling, spiral),
        run_time=7.0,
        rate_func=rate_functions.ease_in_quad,
    )
    burst = Circle(radius=0.25, color=cfg.WHITE, stroke_width=8, fill_color=cfg.WHITE, fill_opacity=0.5)
    burst.move_to(ORBIT_CENTER)
    scene.add(burst)
    paced_play(
        scene,
        burst.animate.scale(8.0).set_stroke(opacity=0).set_fill(opacity=0),
        FadeOut(falling, scale=0.2),
        FadeOut(spiral, core, chain, link),
        run_time=0.9,
    )
    scene.remove(burst)

    lifetime = eq(
        rf"t \approx {COLLAPSE.lifetime_picoseconds:.0f}\times 10^{{-12}}\ \text{{s}}",
        RADIATION_COLOR,
        60,
    ).move_to([0, 0.85, 0])
    paced_play(scene, FadeIn(lifetime, scale=1.1), run_time=0.9)
    fail = VGroup(
        cross_mark(0.23, RADIATION_COLOR),
        outlined_text("the atom cannot last", 48, RADIATION_COLOR),
    ).arrange(RIGHT, buff=0.34).move_to([0, -0.65, 0])
    paced_play(scene, FadeIn(fail, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 6.4)

    # -- Beat 5: leave the question standing ----------------------------------
    paced_play(scene, FadeOut(lifetime, fail), run_time=0.8)
    question = outlined_text("so what is holding the atom up?", cfg.FONT["title"], cfg.GOLD)
    fit_width(question)
    paced_play(scene, FadeIn(question, scale=1.08), run_time=1.0)
    narration_wait(scene, 6.4)

    end_scene(scene, started, cfg.SCENE_DURATIONS["08"])
