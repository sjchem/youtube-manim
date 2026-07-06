"""Scene 3: hexagonal order and regular tessellation."""

from __future__ import annotations

import math

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import begin_scene, end_scene, equation, label, paced_play, regular_polygon


class Scene03HexagonOrder(MovingCameraScene):
    """Show why hexagons tile cleanly."""

    def construct(self) -> None:
        play_scene_03(self)


def _hex_at(q: int, r: int, radius: float = 0.66) -> RegularPolygon:
    x = radius * 1.5 * q
    y = radius * math.sqrt(3) * (r + q / 2)
    return regular_polygon(6, radius=radius, color=cfg.GREEN).move_to([x, y, 0])


def play_scene_03(scene: Scene) -> None:
    start = begin_scene(scene)

    heading = label("Geometry gives 6 a physical shape", cfg.GREEN, 38).to_edge(UP, buff=0.48)
    hexagon = regular_polygon(6, radius=1.6, color=cfg.GREEN).shift(LEFT * 3.25)
    center = Dot(hexagon.get_center(), color=cfg.WHITE, radius=0.06)
    radii = VGroup(*[Line(hexagon.get_center(), v, color=cfg.CYAN, stroke_width=3, stroke_opacity=0.75) for v in hexagon.get_vertices()])
    angle = equation(r"120^\circ", cfg.GOLD, 56).move_to(hexagon.get_center() + RIGHT * 0.9 + UP * 0.18)

    paced_play(scene, FadeIn(heading, shift=DOWN * 0.2), run_time=0.6)
    paced_play(scene, Create(hexagon), FadeIn(center), Create(radii), run_time=1.0)
    paced_play(scene, Write(angle), run_time=0.65)

    vertex = np.array([2.2, 0.9, 0])
    tri_hexes = VGroup()
    for rot, color in [(0, cfg.GREEN), (TAU / 3, cfg.CYAN), (2 * TAU / 3, cfg.GOLD)]:
        h = regular_polygon(6, radius=0.9, color=color)
        h.rotate(rot)
        h.move_to(vertex + 0.78 * np.array([math.cos(rot - PI / 6), math.sin(rot - PI / 6), 0]))
        tri_hexes.add(h)
    dot = Dot(vertex, color=cfg.WHITE, radius=0.075)
    meet_eq = equation(r"120^\circ+120^\circ+120^\circ=360^\circ", cfg.WHITE, 38)
    meet_eq.next_to(tri_hexes, DOWN, buff=0.18).shift(RIGHT * 0.15)

    paced_play(scene, LaggedStart(*[Create(h) for h in tri_hexes], lag_ratio=0.18), FadeIn(dot), run_time=1.1)
    paced_play(scene, Write(meet_eq), run_time=0.95)
    scene.play(Indicate(dot, color=cfg.GREEN, scale_factor=1.8), run_time=0.55)

    honeycomb = VGroup()
    for q in range(-2, 3):
        for r in range(-1, 2):
            if abs(q + r) <= 3:
                honeycomb.add(_hex_at(q, r, radius=0.34))
    honeycomb.shift(DOWN * 2.35 + LEFT * 0.55)
    paced_play(scene, LaggedStart(*[FadeIn(h, scale=0.7) for h in honeycomb], lag_ratio=0.025), run_time=1.35)
    tiling = label("no gaps, no overlap", cfg.GREEN, 28).next_to(honeycomb, RIGHT, buff=0.35)
    paced_play(scene, FadeIn(tiling, shift=UP * 0.1), run_time=0.55)
    end_scene(scene, start)
