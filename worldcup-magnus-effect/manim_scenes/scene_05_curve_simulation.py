"""Scene 5: numerical trajectory builds the curved shot."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, goal_top_view, narration_wait, paced_play, path_from_points, pitch_top_view, trionda_image_ball, vector_arrow
from utils.math_utils import rescale_points
from utils.physics_models import FreeKickParams, force_vectors, simulate_free_kick_2d, straight_reference, trajectory_points


class Scene05CurveSimulation(Scene):
    """Build the real trajectory frame by frame."""

    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())
    pitch = pitch_top_view().scale(0.9).shift(DOWN * 0.15)
    goal = goal_top_view(width=2.4, depth=0.85).move_to([5.8, 0.2, 0])
    scene.add(pitch, goal)

    samples = simulate_free_kick_2d(FreeKickParams())
    model_points = trajectory_points(samples)
    straight_points = straight_reference(samples)
    mapped_curve = rescale_points(model_points, (0, 24.5), (-3.2, 2.4), 11.3, 4.5, center=(0, -0.25))
    mapped_straight = rescale_points(straight_points, (0, 24.5), (-3.2, 2.4), 11.3, 4.5, center=(0, -0.25))
    curve = path_from_points(mapped_curve, cfg.GREEN, width=6)
    straight = DashedVMobject(path_from_points(mapped_straight, cfg.RED, width=3.5, opacity=0.75), num_dashes=34, dashed_ratio=0.52)
    ball = trionda_image_ball(width=0.72).move_to(mapped_curve[0])

    paced_play(scene, FadeIn(ball, scale=0.7), Create(straight), run_time=0.85)
    dots = VGroup(*[Dot(point, radius=0.035, color=cfg.GREEN, fill_opacity=0.68) for point in mapped_curve[::4]])
    paced_play(scene, Create(curve), LaggedStart(*[FadeIn(dot, scale=0.7) for dot in dots], lag_ratio=0.035), MoveAlongPath(ball, curve), run_time=2.5)

    sparse_forces = force_vectors(samples, every=10)
    force_group = VGroup()
    for x, y, ax, ay in sparse_forces[:5]:
        p = rescale_points([(x, y)], (0, 24.5), (-3.2, 2.4), 11.3, 4.5, center=(0, -0.25))[0]
        vec = np.array([ax, ay, 0.0])
        norm = np.linalg.norm(vec[:2])
        if norm > 1e-6:
            vec = vec / norm * 0.62
        force_group.add(vector_arrow(p, p + vec, cfg.GREEN))
    equation = MathTex(r"m\vec{a}=\vec{F}_D+\vec{F}_M+\vec{W}", font_size=42, color=cfg.WHITE).to_edge(UP, buff=0.55)
    paced_play(scene, FadeIn(equation), LaggedStart(*[FadeIn(v) for v in force_group], lag_ratio=0.15), run_time=1.1)
    paced_play(scene, Indicate(goal, color=cfg.GREEN, scale_factor=1.02), run_time=0.6)
    narration_wait(scene, 0.9)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["05"])
