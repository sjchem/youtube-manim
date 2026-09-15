"""Chapter 1: a dimensional classical atom loses its apparently obvious answers.

Three populated classical shells establish the familiar picture. The camera
then isolates one electron and its track before that track opens into a wave. A fixed
sample of possible detections gives the closing cloud depth without suggesting
that hundreds of electrons are moving inside the atom. Camera motion supplies
parallax; it does not animate the sampled positions as particle trajectories.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import QuantumScene, cloud, glow_curve, halo, outlined_text, title_card, wave

from manim_scenes.atomic_visuals import nucleon_cluster

ORBIT_RADIUS = 3.15
START_ANGLE = 0.35
# A schematic 2,8,2 classical picture, not quantum orbital surfaces.
SHELLS = ((1.35, 2, 1.55), (2.25, 8, 1.20), (ORBIT_RADIUS, 2, 1.0))


def _bright_electron(radius: float = 0.07) -> VGroup:
    """Small camera-facing cyan core, white glint and a broad soft bloom."""
    return VGroup(
        halo(radius * 1.7, cfg.BLUE, layers=5, peak_opacity=0.16),
        Dot(radius=radius, color=cfg.BLUE),
        Dot(radius=radius * 0.48, color=cfg.WHITE),
    )


def _shell_point(radius: float, angle: float) -> np.ndarray:
    return radius * np.array([np.cos(angle), np.sin(angle), 0.0])



def _trail(angle: float) -> VGroup:
    """A short graded arc behind the classical bead, never a second orbit."""
    parts = VGroup()
    for index in range(14):
        strength = (index + 1) / 14
        segment = Arc(radius=ORBIT_RADIUS, start_angle=angle - 0.95 + index * 0.95 / 14,
                      angle=0.95 / 14, color=cfg.CYAN,
                      stroke_width=2.0 + 3.0 * strength, stroke_opacity=0.10 + 0.8 * strength)
        parts.add(glow_curve(segment, opacity=0.09 * strength))
    return parts


def _crosshair(point) -> VGroup:
    """A camera-facing location marker attached to the paused model electron."""
    size = 0.39
    arms = VGroup(Line(LEFT * size, RIGHT * size), Line(DOWN * size, UP * size))
    arms.set_stroke(cfg.GOLD, width=3)
    ring = Circle(radius=size * 0.7, color=cfg.GOLD, stroke_width=2.4)
    return VGroup(arms, ring).move_to(point)


def _detection_cloud() -> VGroup:
    """Bright, static 1s samples; small halos distinguish depth from background."""
    points = cloud(count=900, scale=0.76, center=DOWN * 0.45, color=cfg.CYAN)
    for index, dot in enumerate(points):
        dot.scale(1.10 if index % 5 else 1.45)
        dot.set_opacity(0.72 + 0.28 * (index % 9) / 8)
        if index % 5 == 0:
            bloom = dot.copy().scale(2.4).set_opacity(0.09)
            dot.add(bloom)
    return points


class Scene01WhereIsIt(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("01")

    # -- Beat 1: inspect a luminous, dimensional version of the familiar atom -
    scene.lower_ground(seconds=0.35)
    scene.set_camera_orientation(phi=46 * DEGREES, theta=-85 * DEGREES, zoom=1.25)
    phase = ValueTracker(START_ANGLE)
    core = nucleon_cluster(scene)
    core_glow = halo(0.62, cfg.ORANGE, layers=6, peak_opacity=0.14)
    scene.camera.add_fixed_orientation_mobjects(core_glow)

    # Keep the selected outer track as a named object: it is the one that
    # unwraps later. The other two rings and eleven electrons leave together.
    ring = Circle(radius=ORBIT_RADIUS, color=cfg.CYAN, stroke_width=1.8, stroke_opacity=0.48)
    ring_glow = ring.copy().set_stroke(width=8, opacity=0.05)
    satellite_tracks = VGroup()
    satellites = VGroup()
    bead = None
    for radius, population, angular_rate in SHELLS:
        if radius != ORBIT_RADIUS:
            track = Circle(radius=radius, color=cfg.CYAN, stroke_width=1.6, stroke_opacity=0.42)
            satellite_tracks.add(track.copy().set_stroke(width=8, opacity=0.04), track)
        for index in range(population):
            selected = radius == ORBIT_RADIUS and index == 0
            offset = TAU * index / population + (0.25 if radius != ORBIT_RADIUS else 0.0)
            marker = _bright_electron(0.09 if selected else 0.07)
            marker.move_to(_shell_point(radius, START_ANGLE + offset))

            def follow(mob, radius=radius, offset=offset, angular_rate=angular_rate):
                angle = START_ANGLE + offset + angular_rate * (phase.get_value() - START_ANGLE)
                mob.move_to(_shell_point(radius, angle))

            marker.add_updater(follow)
            scene.camera.add_fixed_orientation_mobjects(marker)
            if selected:
                bead = marker
            else:
                satellites.add(marker)

    assert bead is not None
    trail = _trail(START_ANGLE)
    atom = VGroup(core_glow, satellite_tracks, ring_glow, ring, trail, core, satellites, bead)
    atom._needs_depth_sort = True
    scene.morph(atom, seconds=1.2)
    trail.add_updater(lambda mob: mob.become(_trail(phase.get_value())))
    scene.move_camera(phi=42 * DEGREES, theta=-65 * DEGREES,
                      added_anims=[phase.animate.set_value(START_ANGLE + TAU)],
                      run_time=5.0 / cfg.SPEED, rate_func=linear)

    # Pause the model to ask about one definite electron. This also makes the
    # subsequent single-electron probability cloud an unambiguous change of view.
    core.clear_updaters(recursive=True)
    bead.clear_updaters()
    for marker in satellites:
        marker.clear_updaters()
    trail.clear_updaters()
    scene.playq(FadeOut(satellite_tracks), FadeOut(satellites), seconds=0.7)
    scene.camera.remove_fixed_orientation_mobjects(*satellites)
    scene.remove(atom)
    atom.remove(satellite_tracks, satellites)
    scene.add(atom)

    # -- Beat 2: locate it, then show the tangent velocity of this exact orbit -
    mark = _crosshair(bead.get_center())
    scene.camera.add_fixed_orientation_mobjects(mark)
    where = scene.pin(outlined_text("WHERE?", cfg.FONT["label"], cfg.GOLD).move_to(UP * 3.5))
    scene.playq(Create(mark), FadeIn(where, shift=DOWN * 0.1), seconds=0.8)
    scene.local.append(mark)
    scene.hold(1.2)
    scene.drop(where, seconds=0.35)
    tangent = np.array([-np.sin(phase.get_value()), np.cos(phase.get_value()), 0.])
    velocity = Arrow(bead.get_center(), bead.get_center() + 1.65 * tangent,
                     color=cfg.GOLD, buff=0.16, stroke_width=6, max_tip_length_to_length_ratio=0.18)
    speed = scene.pin(outlined_text("HOW FAST?", cfg.FONT["label"], cfg.GOLD).move_to(UP * 3.5))
    scene.playq(GrowArrow(velocity), FadeIn(speed, shift=DOWN * 0.1), seconds=0.8)
    scene.local.append(velocity)
    scene.at(15)

    # -- Beat 3: the apparent certainty fails before the track does -----------
    scene.drop(speed, seconds=0.4)
    for _ in range(3):
        scene.playq(mark.animate.set_opacity(0.18), velocity.animate.set_opacity(0.18), seconds=0.18)
        scene.playq(mark.animate.set_opacity(1.0), velocity.animate.set_opacity(1.0), seconds=0.18)
    scene.playq(Indicate(mark, color=cfg.RED, scale_factor=1.25),
                Indicate(velocity, color=cfg.RED, scale_factor=1.1), seconds=1.1)
    scene.drop(mark, velocity, seconds=0.6)
    scene.camera.remove_fixed_orientation_mobjects(mark)
    scene.playq(ring.animate.set_stroke(color=cfg.RED, opacity=0.85), seconds=0.6)

    # -- Beat 4: unwrap the actual track while returning to the diagram view --
    core.clear_updaters()
    bead.clear_updaters()
    ripple = wave(width=8.8, k=4, amplitude=0.12)
    scene.move_camera(phi=0, theta=-90 * DEGREES, zoom=1,
                      added_anims=[ReplacementTransform(ring, ripple), FadeOut(ring_glow),
                                   FadeOut(trail), FadeOut(core), FadeOut(bead),
                                   FadeOut(core_glow)],
                      run_time=2.1 / cfg.SPEED)
    scene.camera.remove_fixed_orientation_mobjects(core_glow, bead)
    scene.remove(atom)
    scene.anchor = ripple
    scene.add(ripple)
    scene.raise_ground(seconds=0.6)
    scene.morph(wave(width=8.8, k=4, amplitude=0.72), seconds=1.6)
    scene.at(26)

    # -- Beat 5: the same wave gives way to a cloud with real spatial depth ---
    detections = _detection_cloud()
    # Face discs toward the camera so the side view never makes them vanish.
    scene.camera.add_fixed_orientation_mobjects(*detections)
    scene.lower_ground(seconds=0.4)
    scene.move_camera(phi=52 * DEGREES, theta=-75 * DEGREES,
                      added_anims=[FadeOut(scene.anchor), FadeIn(detections)],
                      run_time=2.0 / cfg.SPEED)
    scene.anchor = detections

    # -- Beat 6: a brief title above the cloud, leaving the centre unobscured --
    card = scene.pin(title_card(cfg.PROJECT_TITLE).scale(0.92).move_to(UP * 3.3))
    scene.playq(FadeIn(card, shift=DOWN * 0.12), seconds=0.7)
    scene.turn(seconds=3.5, angle=0.30)
    scene.at(34)
    scene.drop(card, seconds=0.6)
    scene.flat(seconds=1.7)
    scene.camera.remove_fixed_orientation_mobjects(*detections)
    scene.finish()
