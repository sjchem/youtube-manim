"""Scene 3: spinning surface redirects the surrounding air."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, cinematic_background, end_scene, label_text, narration_wait, paced_play, path_from_points, trionda_image_ball


class Scene03AirflowSpin(Scene):
    """Reveal the air around the ball before and after spin."""

    def construct(self) -> None:
        play_scene(self)


def air_streams(spinning: bool = False, count: int = 13, color: str = cfg.CYAN) -> VGroup:
    """Soft airflow wisps with small particles so the air feels continuous."""
    streams = VGroup()
    ys = np.linspace(-1.85, 1.85, count)
    for index, y in enumerate(ys):
        phase = (index - count / 2) * 0.075
        if spinning:
            points = [
                np.array([-5.55, y, 0]),
                np.array([-2.7, y + 0.12 * np.sin(index), 0]),
                np.array([-1.05, y + 0.48 * np.exp(-abs(y)) + phase, 0]),
                np.array([0.75, y - 0.42 * np.exp(-abs(y)) + phase, 0]),
                np.array([4.45, y - 0.7 + phase, 0]),
            ]
        else:
            points = [
                np.array([-5.55, y, 0]),
                np.array([-2.6, y, 0]),
                np.array([-1.05, y + 0.18 * np.sign(y) * np.exp(-abs(y)), 0]),
                np.array([0.95, y + 0.18 * np.sign(y) * np.exp(-abs(y)), 0]),
                np.array([4.45, y, 0]),
            ]
        core = path_from_points(points, color, width=5.2, opacity=0.5)
        haze = core.copy().set_stroke(color, width=17, opacity=0.1)
        particles = VGroup()
        for alpha in np.linspace(0.12, 0.92, 5):
            dot = Dot(core.point_from_proportion(alpha), radius=0.035, color=color)
            dot.set_opacity(0.58 - 0.2 * abs(y) / 1.85)
            particles.add(dot)
        arrow = VGroup()
        if index in (2, 5, 8, 11):
            end = core.point_from_proportion(0.9)
            before = core.point_from_proportion(0.84)
            direction = end - before
            angle = np.arctan2(direction[1], direction[0])
            tip = Triangle(color=color, fill_color=color, fill_opacity=0.9, stroke_width=0).scale(0.1)
            tip.move_to(end)
            tip.rotate(angle - PI / 2)
            arrow.add(tip)
        streams.add(VGroup(haze, core, particles, arrow))
    return streams


def spin_arrows(radius: float = 1.05, stroke_width: float = 9) -> VGroup:
    """Create thicker rotation arrows around the ball."""
    arrows = VGroup()
    for shift in (-0.14, 0.2):
        arc = Arc(radius=radius, start_angle=0.15 * PI + shift, angle=0.78 * PI, color=cfg.ORANGE, stroke_width=stroke_width)
        end_angle = 0.15 * PI + shift + 0.78 * PI
        tip = Triangle(color=cfg.ORANGE, fill_color=cfg.ORANGE, fill_opacity=1).scale(0.13)
        tip.move_to([np.cos(end_angle) * radius, np.sin(end_angle) * radius, 0])
        tip.rotate(end_angle - PI / 2)
        arrows.add(arc, tip)
    return arrows


def wake_cloud() -> VGroup:
    """A tilted low-pressure wake shown as diffuse orange air."""
    cloud = VGroup()
    for offset, opacity, width in [(-0.28, 0.18, 16), (0.0, 0.28, 11), (0.28, 0.16, 14)]:
        pts = [
            np.array([0.65, offset, 0]),
            np.array([1.6, offset - 0.24, 0]),
            np.array([2.6, offset - 0.55, 0]),
            np.array([4.1, offset - 0.92, 0]),
        ]
        cloud.add(path_from_points(pts, cfg.ORANGE, width=width, opacity=opacity))
    for i in range(22):
        x = 0.95 + 3.0 * (i / 21)
        y = -0.1 - 0.72 * (i / 21) + 0.18 * np.sin(i * 1.7)
        dot = Dot([x, y, 0], radius=0.035 + 0.012 * (i % 3), color=cfg.ORANGE)
        dot.set_opacity(0.22)
        cloud.add(dot)
    return cloud


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background())
    caption = label_text("air is the hidden player", cfg.FONT_SIZES["subtitle"], cfg.WHITE, weight=BOLD).to_edge(UP, buff=0.55)
    ball = trionda_image_ball(width=1.5).move_to(ORIGIN)
    still_air = air_streams(spinning=False, count=13, color=cfg.BLUE)
    flow_label = label_text("air flow", 34, cfg.CYAN, weight=BOLD).move_to([-4.75, 2.45, 0])
    scene.add(ball)
    paced_play(scene, FadeIn(caption), FadeIn(flow_label), LaggedStart(*[FadeIn(stream, shift=RIGHT * 0.12) for stream in still_air], lag_ratio=0.05), run_time=1.5)

    symmetric = label_text("no spin: symmetric wake", cfg.FONT_SIZES["small"], cfg.MUTED).move_to([0, -2.9, 0])
    paced_play(scene, FadeIn(symmetric), run_time=0.45)
    narration_wait(scene, 0.55)

    rotation = spin_arrows(radius=1.03, stroke_width=10).move_to(ball.get_center())
    spinning_ball = Group(ball, rotation)
    spun_air = air_streams(spinning=True, count=13, color=cfg.CYAN)
    wake = wake_cloud()
    spin_label = label_text("spin bends the wake", cfg.FONT_SIZES["small"], cfg.ORANGE).move_to([1.8, -2.75, 0])
    paced_play(
        scene,
        ReplacementTransform(still_air, spun_air),
        FadeIn(rotation, scale=1.08),
        FadeOut(symmetric),
        run_time=1.2,
    )
    paced_play(scene, FadeIn(wake, shift=RIGHT * 0.2), FadeIn(spin_label), Rotate(spinning_ball, angle=TAU, rate_func=linear), run_time=1.6)
    narration_wait(scene, 1.0)
    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["03"])
