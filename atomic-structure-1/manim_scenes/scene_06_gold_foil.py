"""Scene 06: the gold foil. Fire the beam, count the flashes, and wait for the one that comes back."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    alpha_particle,
    begin_scene,
    end_scene,
    eq,
    fit_safe,
    fit_width,
    glow_dot,
    glowing_sphere,
    gold_foil_apparatus,
    hide_background,
    move_3d_view,
    narration_wait,
    orbit_hold,
    outlined_text,
    paced_play,
    pin_to_frame,
    polyline,
    restore_background,
    set_3d_view,
    stage_banner,
    unpin_from_frame,
    verdict_stamp,
)
from utils.physics_models import RutherfordScattering

# A gentler coupling than a bare nucleus, chosen so a shot from the far edge of
# the beam bends by a couple of degrees. The angles are still the exact Coulomb
# result; only the length scale is picked to fit a 16-by-9 frame.
SCATTER = RutherfordScattering(strength=0.05, speed=1.0, entry_x=-6.05)
DETECTOR_RADIUS = 3.30

# Lanes are separate shots at different impact parameters, all inside the
# detector ring so every one of them ends on the screen. At this coupling the
# far lanes turn by two to five degrees, the near ones by twenty or thirty, and
# a shot that comes in almost exactly on axis is thrown back the way it came.
MOSTLY_STRAIGHT = (
    2.40, -2.10, 1.75, -2.30, 1.30, -1.55, 2.00, -1.15,
    2.25, -1.85, 1.50, -2.25, 1.90, -1.35,
)
NOTICEABLE = (0.35, -0.25, 0.18)
THE_ONE = 0.008


def _gold_sheet() -> VGroup:
    """A thin, gently uneven metallic sheet with warm reflected highlights."""
    sheet = Surface(
        lambda y, z: np.array([0.035 + 0.006*np.sin(2.5*y + z)*np.cos(3*z), y, z]),
        u_range=(-1.75, 1.75), v_range=(-1.2, 1.2),
        resolution=(24, 18) if config.pixel_height <= 480 else (40, 30),
        checkerboard_colors=False, fill_opacity=1, stroke_width=0,
    )
    for patch in sheet:
        _, y, z = patch.get_center()
        shine = 0.5 + 0.5*np.sin(1.5*y + 0.9*z + 0.7)
        tone = interpolate_color(ManimColor("#9C580D"), ManimColor("#FFE69B"),
                                 0.18 + 0.76*shine)
        patch.set_fill(tone, opacity=1)
        # Matching edge coverage closes subpixel seams between surface patches.
        patch.set_stroke(tone, width=0.75, opacity=1)
    rim = Polygon([0.04,-1.75,-1.2], [0.04,1.75,-1.2],
                  [0.04,1.75,1.2], [0.04,-1.75,1.2],
                  color="#FFE5A0", stroke_width=1.6, fill_opacity=0).set_shade_in_3d(True)
    bloom = VGroup()
    for scale, opacity in ((1.06,0.035), (1.13,0.023), (1.22,0.012)):
        glow = rim.copy().scale(scale).shift(LEFT*0.08)
        glow.set_stroke(width=0).set_fill(cfg.GOLD, opacity=opacity)
        bloom.add(glow)
    return VGroup(bloom, sheet, rim)


def _flat_gold_sheet() -> VGroup:
    # Cover the full selected beam: its outermost lane is 2.4 units off axis.
    height = 5.2
    glow = VGroup(*[
        Rectangle(width=0.16+0.08*i, height=height+0.06*i, stroke_width=0,
                  fill_color=cfg.GOLD, fill_opacity=0.025)
        for i in range(4,0,-1)
    ])
    strips = VGroup(*[
        Rectangle(width=0.035, height=height, stroke_width=0, fill_color=tone, fill_opacity=1)
        .shift(RIGHT*((i-2)*0.035))
        for i,tone in enumerate(("#A96512", "#D9982D", "#FFEBA5", "#F5C65D", "#BB7B1D"))
    ])
    return VGroup(glow, strips)


def _track_points(impact_parameter: float) -> np.ndarray:
    return SCATTER.screen_trajectory(impact_parameter, DETECTOR_RADIUS)


def _fire(
    scene: Scene,
    impact_parameter: float,
    run_time: float,
    color: str = cfg.ALPHA_COLOR,
    trail_opacity: float = 0.45,
    bead_radius: float = 0.10,
    previous_tracks: VGroup | None = None,
) -> VGroup:
    """Send one alpha particle in, leave its track, and light up where it lands."""
    points = _track_points(impact_parameter)
    track = polyline(points, color, stroke_width=2.5).set_stroke(opacity=trail_opacity)
    bead = alpha_particle(bead_radius, color)
    bead.move_to([points[0][0], points[0][1], 0.0])
    scene.add(bead)
    soften = [old[0].animate.set_stroke(opacity=0.09) for old in previous_tracks] if previous_tracks else []
    scene.play(MoveAlongPath(bead, track), Create(track), *soften, run_time=run_time, rate_func=linear)
    scene.remove(bead)
    # The flash goes where the particle actually stopped, so the picture and the
    # trajectory can never disagree.
    spark = glow_dot([points[-1][0], points[-1][1], 0.0], cfg.GREEN, 0.06)
    scene.play(FadeIn(spark, scale=1.8), run_time=0.22)
    return VGroup(track, spark)


class Scene06GoldFoil(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "06")
    add_cinematic_background(scene)

    # -- Beat 1: the real apparatus, seen from outside ------------------------
    background = hide_background(scene)
    set_3d_view(scene, phi=70 * DEGREES, theta=-64 * DEGREES)

    housing = Cylinder(radius=0.34, height=1.0, direction=RIGHT, resolution=(2, 20))
    housing.set_color(cfg.GRAY)
    housing.set_opacity(0.9)
    housing.move_to([-4.6, 0, 0])
    hot = Sphere(radius=0.15, resolution=(12, 24), stroke_width=0)
    hot.set_color(cfg.RED)
    hot.move_to([-4.25, 0, 0])

    foil = _gold_sheet()
    ring = Torus(major_radius=DETECTOR_RADIUS, minor_radius=0.045, resolution=(6, 40))
    ring.set_color("#779B8D")
    ring.set_opacity(0.85)

    label = stage_banner("EXPERIMENT")
    label.to_edge(UP, buff=0.32)
    pin_to_frame(scene, label)

    paced_play(scene, FadeIn(label, shift=DOWN * 0.15), run_time=0.9)
    paced_play(scene, FadeIn(housing), FadeIn(hot, scale=1.5), run_time=1.2)
    paced_play(scene, FadeIn(foil, scale=1.15), run_time=1.4)
    paced_play(scene, Create(ring), run_time=1.8)
    # Fade overlays while they are still fixed to the screen: releasing them
    # first makes the text jump into the tilted world camera during its exit.
    paced_play(scene, FadeOut(label), run_time=0.6)
    unpin_from_frame(scene, label)
    packet = glowing_sphere(0.09, cfg.GOLD, resolution=(6,12), shells=1).move_to([-4.25,0,0])
    flash = glowing_sphere(0.12, cfg.GREEN, resolution=(6,12), shells=1).move_to([DETECTOR_RADIUS,0,0])
    travel = Line([-4.25,0,0], [DETECTOR_RADIUS,0,0])
    scene.move_camera(theta=scene.camera.get_theta()+0.84, run_time=8.4, rate_func=smooth,
        added_anims=[Succession(
            Wait(1.0), FadeIn(packet, run_time=0.3),
            MoveAlongPath(packet, travel, run_time=3.0, rate_func=linear),
            FadeOut(packet, run_time=0.3), FadeIn(flash, run_time=0.25),
            FadeOut(flash, run_time=0.75), Wait(2.8),
        )])
    move_3d_view(scene, phi=58 * DEGREES, theta=-30 * DEGREES, run_time=3.6)
    orbit_hold(scene, 8.0, rate=0.08)

    # The apparatus turns smoothly into the viewing direction of the next shot.
    move_3d_view(scene, phi=0, theta=-90*DEGREES, run_time=7.0)
    paced_play(scene, FadeOut(housing, hot, foil, ring), run_time=0.9)
    restore_background(scene, background)

    # -- Beat 2: the same scene, head on --------------------------------------
    parts = gold_foil_apparatus(DETECTOR_RADIUS)
    flat_ring = parts["detector"]
    flat_ring[0].set_stroke("#577C75", width=3, opacity=0.35)
    flat_ring[1].set_stroke("#99B9A9", width=1.5, opacity=0.60)
    flat_foil = _flat_gold_sheet()
    paced_play(scene, FadeIn(flat_ring), FadeIn(flat_foil), run_time=1.2)
    paced_play(scene, FadeIn(parts["source"]), FadeIn(parts["collimator"]), run_time=0.9)
    paced_play(scene, FadeIn(parts["foil_label"]), FadeIn(parts["detector_label"]), run_time=0.7)
    narration_wait(scene, 5.6)

    # -- Beat 3: almost everything sails through ------------------------------
    paced_play(
        scene,
        FadeOut(parts["foil_label"], parts["detector_label"]),
        run_time=0.7,
    )

    tracks = VGroup()
    for index, parameter in enumerate(MOSTLY_STRAIGHT):
        tracks.add(_fire(scene, parameter, run_time=1.55 - 0.09 * index, previous_tracks=tracks))
    narration_wait(scene, 6.4)

    # -- Beat 4: a few refuse to behave ---------------------------------------
    narration_wait(scene, 1.2)
    for parameter in NOTICEABLE:
        tracks.add(_fire(scene, parameter, run_time=1.75, color=cfg.ORANGE,
                         trail_opacity=0.7, bead_radius=0.12, previous_tracks=tracks))
        narration_wait(scene, 2.2)
    narration_wait(scene, 5.4)
    narration_wait(scene, 0.5)

    # -- Beat 5: the one that came back ---------------------------------------
    paced_play(scene, *[old[0].animate.set_stroke(opacity=0.06) for old in tracks],
               *[old[1].animate.fade(0.65) for old in tracks], run_time=0.9)
    narration_wait(scene, 0.8)
    narration_wait(scene, 4.2)

    points = _track_points(THE_ONE)
    rebound = polyline(points, cfg.RED, stroke_width=5.0)
    bead = alpha_particle(0.15, cfg.RED).move_to([points[0][0], points[0][1], 0.0])
    scene.add(bead)
    paced_play(scene, MoveAlongPath(bead, rebound), Create(rebound), run_time=5.4, rate_func=linear)

    impact_spark = glow_dot([points[-1][0], points[-1][1], 0.0], cfg.RED, 0.13)
    paced_play(scene, FadeIn(impact_spark, scale=2.0), FadeOut(bead), run_time=0.5)
    ring_flash = Circle(radius=0.2, color=cfg.RED, stroke_width=8, fill_opacity=0)
    ring_flash.move_to(impact_spark.get_center())
    scene.add(ring_flash)
    paced_play(scene, ring_flash.animate.scale(4.5).set_stroke(opacity=0), run_time=1.1)
    scene.remove(ring_flash)

    narration_wait(scene, 0.4)
    paced_play(scene, ShowPassingFlash(rebound.copy().set_stroke(cfg.WHITE, width=6), time_width=0.18), run_time=1.0)
    narration_wait(scene, 5.0)

    # -- Beat 6: how rare is "once in a while"? -------------------------------
    paced_play(scene, FadeOut(impact_spark, tracks, rebound, flat_ring, flat_foil,
                             parts["source"], parts["collimator"]), run_time=0.6)
    one_in = round(1.0 / SCATTER.backscatter_fraction)
    rate = eq(
        rf"\approx 1 \text{{ in }} {one_in:,}".replace(",", "{,}"),
        cfg.GOLD,
        cfg.FONT["hero"],
    ).move_to([0, 0.40, 0])
    paced_play(scene, FadeIn(rate, scale=1.1), run_time=0.9)
    sample_note = outlined_text("Textbook example", cfg.FONT["tiny"], cfg.MUTED)
    fit_width(sample_note)
    sample_note.next_to(rate, DOWN, buff=0.55)
    paced_play(scene, FadeIn(sample_note), run_time=0.8)
    narration_wait(scene, 6.2)
    paced_play(scene, FadeOut(sample_note), run_time=0.5)

    # -- Beat 7: the prediction is dead ---------------------------------------
    paced_play(
        scene,
        FadeOut(rate),
        run_time=0.9,
    )
    stamp = verdict_stamp("THOMSON'S MODEL FAILS", cfg.RED).move_to([0, 0.9, 0])
    fit_safe(stamp, padding=0.4)
    paced_play(scene, FadeIn(stamp, scale=1.25), run_time=1.0)
    reason = outlined_text("diffuse charge cannot explain the observed large deflections", cfg.FONT["body"], cfg.MUTED)
    fit_width(reason, cfg.SAFE_WIDTH - 0.6)
    reason.move_to([0, -1.55, 0])
    paced_play(scene, FadeIn(reason, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 5.6)

    end_scene(scene, started, cfg.SCENE_DURATIONS["06"])
