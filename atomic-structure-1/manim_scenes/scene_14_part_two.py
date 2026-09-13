"""Scene 14: the orbit dissolves, something else begins to form, and we cut away."""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    end_scene,
    fit_width,
    glowing_sphere,
    hide_background,
    narration_wait,
    orbit_circle_3d,
    orbit_hold,
    outlined_text,
    paced_play,
    pin_to_frame,
    probability_cloud,
    reset_flat_camera,
    restore_background,
    set_3d_view,
    title_card,
    unpin_from_frame,
)

ORBIT_RADIUS = 2.85


class Scene14PartTwo(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "14")
    add_cinematic_background(scene)

    background = hide_background(scene)
    set_3d_view(scene, phi=66 * DEGREES, theta=-58 * DEGREES)

    # -- Beat 1: the last picture of a particle on a track ---------------------
    core = glowing_sphere(0.34, cfg.NUCLEUS_COLOR, resolution=(16, 32), shells=1)
    ring = orbit_circle_3d(ORBIT_RADIUS, cfg.MUTED, stroke_width=3.0)
    bead = glowing_sphere(0.18, cfg.ELECTRON_COLOR, resolution=(12, 24), shells=1)
    bead.move_to([ORBIT_RADIUS, 0, 0])
    paced_play(scene, FadeIn(core), Create(ring), FadeIn(bead, scale=1.4), run_time=1.4)

    question = outlined_text("what replaces the circular path?", cfg.FONT["body"], cfg.WHITE)
    question.to_edge(UP, buff=0.42)
    pin_to_frame(scene, question)
    scene.remove(question)
    paced_play(scene, FadeIn(question, shift=DOWN * 0.12), run_time=0.8)
    orbit_hold(scene, 3.0, rate=0.045)
    # Finish the screen-space fade before releasing the camera attachment.
    paced_play(scene, FadeOut(question), run_time=0.6)
    unpin_from_frame(scene, question)
    orbit_hold(scene, 14.2, rate=0.045)

    # -- Beat 2: it dissolves --------------------------------------------------
    paced_play(scene, FadeOut(bead, scale=3.2), run_time=1.2)
    paced_play(scene, ring.animate.set_stroke(opacity=0.06), run_time=1.8)

    cloud = probability_cloud(count=420, radius=1.85, color=cfg.PURPLE, dot_radius=0.040)
    # Fit the full spatial sample into the frame without shrinking the dots.
    extent = max(np.linalg.norm(dot.get_center()) for dot in cloud)
    for i, dot in enumerate(cloud):
        dot.move_to(dot.get_center() * 3.65 / extent)
        dot.set_color(interpolate_color(ManimColor(cfg.PURPLE), ManimColor(cfg.CYAN), (i % 7) / 6))
        dot.set_fill(opacity=0.72 + 0.28 * (i % 5) / 4)
        dot.set_shade_in_3d(True)
    # Camera-facing discs retain their readable size during the gentle orbit.
    # Register each point separately so its 3D centre still projects correctly.
    scene.add_fixed_orientation_mobjects(*cloud, use_static_center_func=True)
    scene.remove(*cloud)
    paced_play(scene, FadeIn(cloud), run_time=2.6)
    meaning = outlined_text("One electron", cfg.FONT["small"], cfg.CYAN)
    meaning.to_edge(DOWN, buff=0.4)
    pin_to_frame(scene, meaning)
    scene.remove(meaning)
    paced_play(scene, FadeIn(meaning), run_time=0.8)
    orbit_hold(scene, 3.0, rate=0.055)
    paced_play(scene, FadeOut(meaning), run_time=0.6)
    unpin_from_frame(scene, meaning)
    orbit_hold(scene, 13.0, rate=0.055)

    # -- Beat 3: fade fully before resetting the 3D camera ---------------------
    paced_play(scene, FadeOut(cloud, core, ring), run_time=1.0)
    scene.remove_fixed_orientation_mobjects(*cloud)
    reset_flat_camera(scene)
    restore_background(scene, background)

    card = title_card("NEXT VIDEO", "Why Electrons Don't Orbit the Nucleus", cfg.PURPLE)
    paced_play(scene, FadeIn(card, scale=1.1), run_time=1.2)
    tail = outlined_text("The next mystery: a stable quantum atom", cfg.FONT["body"], cfg.GOLD)
    fit_width(tail, cfg.SAFE_WIDTH - 0.6)
    tail.move_to([0, -2.55, 0])
    paced_play(scene, FadeIn(tail, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 11.7)

    end_scene(scene, started, cfg.SCENE_DURATIONS["14"])
