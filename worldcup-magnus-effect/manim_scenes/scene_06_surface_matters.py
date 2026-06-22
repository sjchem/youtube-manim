"""Scene 6: seams, panels, texture, and speed change the airflow."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    ball_history_montage,
    begin_scene,
    cinematic_background,
    end_scene,
    football,
    label_text,
    load_reference_image,
    narration_wait,
    paced_play,
    path_from_points,
)


class Scene06SurfaceMatters(Scene):
    """World Cup ball evolution as a bridge to aerodynamics."""

    def construct(self) -> None:
        play_scene(self)


def flow_path(points: list[list[float] | np.ndarray], color: str, width: float = 3.2, opacity: float = 0.78) -> VMobject:
    """Create one smooth airflow path."""
    return path_from_points([np.array(point, dtype=float) for point in points], color=color, width=width, opacity=opacity)


def callout(text: str, point: np.ndarray, target: np.ndarray, color: str) -> VGroup:
    """Create a compact surface-detail callout."""
    label = label_text(text, cfg.FONT_SIZES["label"], color, weight=BOLD)
    label.move_to(point)
    line = Line(label.get_left() + LEFT * 0.1, target, color=color, stroke_width=3, stroke_opacity=0.78)
    dot = Dot(target, radius=0.045, color=color)
    return VGroup(line, dot, label)


def surface_texture(center: np.ndarray, color: str = cfg.ORANGE) -> VGroup:
    """Create tiny deterministic surface texture dots."""
    dots = VGroup()
    for row, yoff in enumerate([-0.34, -0.18, -0.02, 0.14, 0.30]):
        for col in range(9):
            xoff = (col - 4) * 0.13 + (0.035 if row % 2 else 0)
            if xoff * xoff + yoff * yoff < 0.52:
                dots.add(Dot(center + np.array([xoff, yoff, 0]), radius=0.015, color=color))
    return dots


def boundary_layer_lines() -> VGroup:
    """Airflow that clings near the ball and then separates into a wake."""
    upper = flow_path(
        [[-6.3, 0.65, 0], [-4.9, 0.65, 0], [-4.1, 1.02, 0], [-3.1, 0.78, 0], [-1.4, 0.28, 0], [1.0, -0.02, 0]],
        cfg.CYAN,
        width=3.0,
    )
    middle = flow_path([[-6.3, 0.06, 0], [-5.1, 0.06, 0], [-3.0, 0.0, 0], [-1.1, -0.15, 0], [1.0, -0.42, 0]], cfg.BLUE, width=2.5)
    lower = flow_path(
        [[-6.3, -0.55, 0], [-4.95, -0.55, 0], [-4.1, -0.96, 0], [-3.1, -0.74, 0], [-1.3, -0.62, 0], [1.0, -0.86, 0]],
        cfg.CYAN,
        width=3.0,
    )
    wake = VGroup(
        flow_path([[-1.1, 0.30, 0], [0.2, 0.18, 0], [1.25, -0.06, 0], [2.1, -0.35, 0]], cfg.ORANGE, width=4.5, opacity=0.55),
        flow_path([[-1.1, -0.20, 0], [0.2, -0.36, 0], [1.2, -0.62, 0], [2.1, -0.94, 0]], cfg.ORANGE, width=4.5, opacity=0.48),
    )
    return VGroup(upper, middle, lower, wake)


def mini_ball(label: str, x: float, rough: bool = False, seam_angle: float = 0.0) -> VGroup:
    """Create a small comparison ball with its own shifted wake."""
    ball = football(radius=0.38, trionda=False).move_to([x, -1.15, 0])
    if rough:
        dots = surface_texture(ball.get_center(), cfg.ORANGE).scale(0.55, about_point=ball.get_center())
    else:
        dots = VGroup()
    seam = Arc(radius=0.31, start_angle=seam_angle, angle=PI * 1.1, color=cfg.CYAN if seam_angle else cfg.MUTED, stroke_width=3).move_to(ball.get_center())
    word = label_text(label, cfg.FONT_SIZES["small"], cfg.WHITE).next_to(ball, DOWN, buff=0.22)
    return VGroup(ball, seam, dots, word)


def comparison_wake(x: float, lift: float, color: str) -> VGroup:
    """Create a wake and side-force arrow for a comparison ball."""
    wake = VGroup(
        flow_path([[x + 0.35, -1.02, 0], [x + 0.9, -0.96 + lift * 0.25, 0], [x + 1.45, -0.88 + lift * 0.55, 0]], color, width=3.5, opacity=0.7),
        flow_path([[x + 0.35, -1.28, 0], [x + 0.95, -1.31 + lift * 0.18, 0], [x + 1.55, -1.36 + lift * 0.48, 0]], color, width=3.5, opacity=0.55),
    )
    force = Arrow([x, -0.64, 0], [x, -0.64 + lift * 0.72, 0], color=cfg.GREEN, stroke_width=4, buff=0)
    return VGroup(wake, force)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())
    title = label_text("the surface changes the flight", cfg.FONT_SIZES["subtitle"], cfg.WHITE, weight=BOLD).to_edge(UP, buff=0.55)
    paced_play(scene, FadeIn(title), run_time=0.5)

    ref = load_reference_image(max_width=9.2)
    history_caption = label_text("1930 to 2026", cfg.FONT_SIZES["small"], cfg.MUTED).to_edge(DOWN, buff=0.58)
    if ref is not None:
        ref.move_to([0, 0.34, 0])
        history_group = Group(ref, history_caption)
        paced_play(scene, FadeIn(ref, scale=0.96), FadeIn(history_caption, shift=UP * 0.12), run_time=1.0)
    else:
        fallback = ball_history_montage().move_to([0, 0.05, 0])
        history_group = VGroup(fallback, history_caption)
        paced_play(scene, FadeIn(fallback), FadeIn(history_caption, shift=UP * 0.12), run_time=1.0)

    narration_wait(scene, 1.0)
    paced_play(scene, FadeOut(history_group), run_time=0.75)

    surface_ball = football(radius=1.08, trionda=True).move_to([-3.85, -0.05, 0])
    texture = surface_texture(surface_ball.get_center(), cfg.ORANGE)
    engineered = VGroup(
        *[
            Arc(radius=0.58 + index * 0.08, start_angle=PI * 0.12 + index * 0.2, angle=PI * 0.54, color=cfg.GOLD, stroke_width=2.3, stroke_opacity=0.65)
            for index in range(3)
        ]
    ).move_to(surface_ball.get_center())
    seam_call = callout("seams", np.array([2.55, 0.62, 0]), surface_ball.get_center() + np.array([0.68, 0.35, 0]), cfg.CYAN)
    panel_call = callout("panels", np.array([2.55, -0.08, 0]), surface_ball.get_center() + np.array([-0.12, 0.68, 0]), cfg.BLUE)
    texture_call = callout("texture + patterns", np.array([3.05, -0.88, 0]), surface_ball.get_center() + np.array([0.12, -0.28, 0]), cfg.ORANGE)

    paced_play(scene, FadeIn(surface_ball, scale=0.88), run_time=1.0)
    paced_play(scene, Create(seam_call), run_time=0.9)
    paced_play(scene, Create(panel_call), run_time=0.9)
    paced_play(scene, FadeIn(texture), Create(texture_call), run_time=1.0)
    paced_play(scene, FadeIn(engineered), run_time=0.75)
    narration_wait(scene, 0.75)

    detail_group = VGroup(surface_ball, texture, engineered, seam_call, panel_call, texture_call)
    paced_play(scene, detail_group.animate.scale(0.72).move_to([-4.25, 0.0, 0]), run_time=1.1)
    paced_play(scene, FadeOut(seam_call, panel_call, texture_call), run_time=0.45)

    flow = boundary_layer_lines()
    layer_label = MathTex(r"\text{boundary layer}", font_size=38, color=cfg.CYAN).move_to([0.9, 1.35, 0])
    cling = label_text("clings", cfg.FONT_SIZES["small"], cfg.CYAN).move_to([-1.55, 0.88, 0])
    separate = label_text("separates", cfg.FONT_SIZES["small"], cfg.ORANGE).move_to([1.75, -0.72, 0])
    wake_label = label_text("wake forms", cfg.FONT_SIZES["small"], cfg.ORANGE).move_to([2.65, -1.2, 0])
    paced_play(scene, FadeIn(layer_label), LaggedStart(*[Create(line) for line in flow[:3]], lag_ratio=0.12), run_time=1.8)
    paced_play(scene, FadeIn(cling, shift=UP * 0.12), run_time=0.5)
    paced_play(scene, LaggedStart(*[Create(line) for line in flow[3]], lag_ratio=0.18), FadeIn(separate), FadeIn(wake_label), run_time=1.5)
    narration_wait(scene, 0.95)

    boundary_group = VGroup(surface_ball, texture, engineered, flow, layer_label, cling, separate, wake_label)
    paced_play(scene, FadeOut(boundary_group), run_time=0.9)

    compare_title = label_text("same kick, different air", cfg.FONT_SIZES["label"], cfg.WHITE, weight=BOLD).move_to([0, 1.55, 0])
    smooth = mini_ball("smoother", -4.6, rough=False, seam_angle=0.0)
    rougher = mini_ball("rougher", -0.4, rough=True, seam_angle=0.25)
    seamed = mini_ball("new seam layout", 3.9, rough=False, seam_angle=1.0)
    wakes = VGroup(
        comparison_wake(-4.6, 0.45, cfg.MUTED),
        comparison_wake(-0.4, 0.86, cfg.CYAN),
        comparison_wake(3.9, 0.64, cfg.ORANGE),
    )
    shift_note = label_text("a shifted wake changes the sideways force", cfg.FONT_SIZES["small"], cfg.GREEN).move_to([0, -3.18, 0])
    paced_play(scene, FadeIn(compare_title), LaggedStart(FadeIn(smooth), FadeIn(rougher), FadeIn(seamed), lag_ratio=0.16), run_time=1.2)
    paced_play(scene, LaggedStart(*[FadeIn(wake) for wake in wakes], lag_ratio=0.22), run_time=1.5)
    paced_play(scene, FadeIn(shift_note, shift=UP * 0.1), run_time=0.55)
    narration_wait(scene, 1.0)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["06"])
