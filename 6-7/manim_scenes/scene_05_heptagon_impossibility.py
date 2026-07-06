"""Scene 5: regular heptagon as geometric outsider."""

from __future__ import annotations

import math

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, end_scene, equation, label, paced_play, panel, regular_polygon


class Scene05HeptagonImpossibility(MovingCameraScene):
    """Visualize why seven resists the simple geometric order of six."""

    def construct(self) -> None:
        play_scene_05(self)


def play_scene_05(scene: Scene) -> None:
    start = begin_scene(scene)

    heading = label("Seven does not lock into the plane so easily", cfg.PURPLE, 36).to_edge(UP, buff=0.48)
    heptagon = regular_polygon(7, radius=1.65, color=cfg.PURPLE).shift(LEFT * 3.35 + UP * 0.1)
    construction_circle = Circle(radius=1.65, color=cfg.CYAN, stroke_width=3, stroke_opacity=0.62).move_to(heptagon)
    center = Dot(heptagon.get_center(), color=cfg.WHITE, radius=0.06)
    spokes = VGroup(*[Line(heptagon.get_center(), v, color=cfg.GRAY, stroke_width=2, stroke_opacity=0.55) for v in heptagon.get_vertices()])
    angle = equation(r"{360^\circ\over 7}", cfg.PURPLE, 58).move_to(heptagon.get_center())

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.15), run_time=0.55)
    paced_play(scene, Create(construction_circle), Create(heptagon), FadeIn(center), Create(spokes), run_time=1.05)
    paced_play(scene, Write(angle), run_time=0.7)

    compass_left = Line(RIGHT * 0.1, UP * 1.1, color=cfg.CYAN, stroke_width=5)
    compass_right = Line(LEFT * 0.1, UP * 1.1, color=cfg.CYAN, stroke_width=5)
    hinge = Dot(UP * 1.1, color=cfg.GOLD, radius=0.07)
    compass = VGroup(compass_left, compass_right, hinge).move_to(RIGHT * 2.9 + UP * 0.9)
    straightedge = Rectangle(width=3.2, height=0.16, color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=0.45).rotate(-0.2).shift(RIGHT * 3.0 + DOWN * 0.7)
    tools = VGroup(compass, straightedge)
    note = label("not constructible with these tools", cfg.ORANGE, 25).move_to(RIGHT * 3.05 + DOWN * 0.05)
    paced_play(scene, FadeIn(tools, shift=LEFT * 0.2), run_time=0.7)
    scene.play(Rotate(compass, angle=0.35, about_point=compass.get_top()), rate_func=there_and_back, run_time=0.8)
    paced_play(scene, FadeIn(note, shift=UP * 0.12), run_time=0.6)

    vertex = np.array([0.9, -2.12, 0])
    hepts = VGroup()
    for k in range(3):
        angle_k = k * TAU / 3
        h = regular_polygon(7, radius=0.58, color=[cfg.PURPLE, cfg.CYAN, cfg.GOLD][k])
        h.rotate(angle_k)
        h.move_to(vertex + 0.53 * np.array([math.cos(angle_k), math.sin(angle_k), 0]))
        hepts.add(h)
    mismatch_arc = Arc(radius=0.48, start_angle=-0.36, angle=PI / 7, color=cfg.ORANGE, stroke_width=7)
    mismatch_arc.move_arc_center_to(vertex)
    ray_a = Line(vertex, vertex + 0.56 * np.array([math.cos(-0.36), math.sin(-0.36), 0]), color=cfg.ORANGE, stroke_width=4)
    ray_b = Line(
        vertex,
        vertex + 0.56 * np.array([math.cos(-0.36 + PI / 7), math.sin(-0.36 + PI / 7), 0]),
        color=cfg.ORANGE,
        stroke_width=4,
    )
    gap = VGroup(ray_a, ray_b, mismatch_arc)
    gap_label = equation(r"3\cdot {900^\circ\over7}\neq360^\circ", cfg.ORANGE, 38).next_to(hepts, RIGHT, buff=0.5)
    base_panel = panel(6.8, 1.85, cfg.ORANGE, 0.12).move_to(VGroup(hepts, gap_label)).shift(DOWN * 0.03)

    paced_play(scene, Create(base_panel), LaggedStart(*[Create(h) for h in hepts], lag_ratio=0.15), run_time=0.9)
    paced_play(scene, Create(gap), Write(gap_label), run_time=0.8)
    scene.play(Indicate(gap, color=cfg.ORANGE, scale_factor=1.1), run_time=0.55)
    end_scene(scene, start)
