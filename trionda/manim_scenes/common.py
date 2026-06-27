"""Shared Manim helpers for the Trionda animation project."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np
from manim import *

import config as cfg


def begin_scene(scene: Scene) -> float:
    """Apply theme and return the current scene time."""

    cfg.apply_manim_config()
    cfg.apply_oceanic_next_theme(scene)
    if hasattr(scene.camera, "frame"):
        scene.camera.frame.move_to(ORIGIN)
        scene.camera.frame.set(width=cfg.FRAME_WIDTH)
    return scene.time


def cinematic_background() -> VGroup:
    """Create a deep Oceanic background with subtle grid and bubbles."""

    base = Rectangle(width=16.2, height=9.2, fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    grid = VGroup()
    for x in np.arange(-8, 8.1, 0.8):
        grid.add(Line([x, -4.5, 0], [x, 4.5, 0], color=cfg.GRID, stroke_width=1, stroke_opacity=0.16))
    for y in np.arange(-4, 4.1, 0.8):
        grid.add(Line([-8, y, 0], [8, y, 0], color=cfg.GRID, stroke_width=1, stroke_opacity=0.13))
    bubbles = cfg.oceanic_bubbles()
    bubbles.set_z_index(-7)
    stars = VGroup(
        *[
            Dot(
                [-7.5 + (i * 1.57) % 15.0, -4.1 + (i * 2.33) % 8.2, 0],
                radius=0.01 + 0.004 * (i % 3),
                color=cfg.MUTED,
                fill_opacity=0.22,
            )
            for i in range(70)
        ]
    )
    return VGroup(base, grid, bubbles, stars).set_z_index(-10)


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    """Play animations with a shared pacing scale."""

    kwargs["run_time"] = kwargs.get("run_time", 1.0) * cfg.TIMING["pace_scale"]
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, duration: float = 1.0) -> None:
    scene.wait(duration * cfg.TIMING["pace_scale"])


def end_scene(scene: Scene, _scene_start: float, duration_key: str | None = None) -> None:
    """Leave a short breathing beat and fade all scene objects."""

    if duration_key is not None:
        target = cfg.SCENE_DURATIONS.get(duration_key, 0)
        remaining = target - scene.time
        if 0 < remaining < 3:
            scene.wait(remaining)
    if scene.mobjects:
        paced_play(scene, FadeOut(*scene.mobjects), run_time=0.55)


def glow(mobject: Mobject, color: str = cfg.CYAN, width: float = 10, layers: int = 3) -> VGroup:
    halos = VGroup()
    for layer in range(layers, 0, -1):
        halo = mobject.copy()
        halo.set_color(color)
        if hasattr(halo, "set_stroke"):
            halo.set_stroke(color=color, width=width * layer, opacity=0.07 / layer)
        if hasattr(halo, "set_fill"):
            halo.set_fill(opacity=0)
        halos.add(halo)
    return VGroup(halos, mobject)


def scene_caption(text: str, color: str = cfg.WHITE, y: float = 3.75) -> VGroup:
    label = Text(text, font_size=cfg.FONT_SIZES["caption"], color=color, weight=BOLD)
    label.set_stroke(cfg.BLACKISH, width=4, opacity=0.85, background=True)
    label.move_to([0, y, 0])
    return glow(label, color=color, width=5, layers=2)


def small_label(text: str, color: str = cfg.CYAN, font_size: int = 28) -> Text:
    label = Text(text, font_size=font_size, color=color, weight=MEDIUM)
    label.set_stroke(cfg.BLACKISH, width=3, opacity=0.85, background=True)
    return label


def equation(tex: str, color: str = cfg.WHITE, font_size: int = 58) -> MathTex:
    eq = MathTex(tex, color=color, font_size=font_size)
    eq.set_stroke(cfg.BLACKISH, width=2, opacity=0.8, background=True)
    return eq


def wavy_path(start: np.ndarray, end: np.ndarray, amp: float = 0.35, waves: int = 2) -> VMobject:
    points = []
    for i in range(50):
        t = i / 49
        p = start * (1 - t) + end * t
        p[1] += amp * math.sin(t * TAU * waves)
        points.append(p)
    mob = VMobject()
    mob.set_points_smoothly(points)
    return mob


def _stylized_trionda_fallback(radius: float = 1.45, include_texture: bool = True) -> VGroup:
    """Fallback if the local TRIONDA PNG is unavailable."""

    shell = Circle(radius=radius, fill_color=cfg.WHITE, fill_opacity=0.98, stroke_color=cfg.CYAN, stroke_width=3)
    shell.set_sheen_direction(UL)
    seams = VGroup()
    colors = [cfg.RED, cfg.GREEN, cfg.BLUE, cfg.GOLD]
    for i, angle in enumerate([0, PI / 2, PI, 3 * PI / 2]):
        curve = wavy_path(
            np.array([-radius * 0.92, 0, 0]),
            np.array([radius * 0.92, 0, 0]),
            amp=0.28 * radius,
            waves=1,
        )
        curve.rotate(angle)
        curve.set_stroke(colors[i], width=6, opacity=0.88)
        seams.add(curve)
    texture = VGroup()
    if include_texture:
        for angle in np.linspace(0, TAU, 28, endpoint=False):
            start = np.array([math.cos(angle), math.sin(angle), 0]) * radius * 0.72
            end = np.array([math.cos(angle + 0.08), math.sin(angle + 0.08), 0]) * radius * 0.9
            texture.add(Line(start, end, color=cfg.GRAY, stroke_opacity=0.28, stroke_width=2))
    return VGroup(shell, seams, texture)


def trionda_ball(radius: float = 1.45, include_texture: bool = True) -> Group:
    """Create the TRIONDA ball from the local PNG asset."""

    if not cfg.TRIONDA_IMAGE.exists():
        return _stylized_trionda_fallback(radius=radius, include_texture=include_texture)

    image = ImageMobject(str(cfg.TRIONDA_IMAGE))
    image.set_height(radius * 2)
    outline = Circle(radius=radius * 1.005, color=cfg.CYAN, stroke_width=2, stroke_opacity=0.55)
    aura = Circle(radius=radius * 1.025, color=cfg.CYAN, stroke_width=14, stroke_opacity=0.08)
    specular = Arc(radius=radius * 0.78, start_angle=PI * 0.18, angle=PI * 0.34, color=cfg.WHITE, stroke_width=3, stroke_opacity=0.24)
    specular.shift(UP * radius * 0.33 + LEFT * radius * 0.14)
    texture_marks = VGroup()
    if include_texture:
        for angle in np.linspace(-PI * 0.1, PI * 0.55, 9):
            start = np.array([math.cos(angle), math.sin(angle), 0]) * radius * 0.72
            end = np.array([math.cos(angle + 0.045), math.sin(angle + 0.045), 0]) * radius * 0.9
            texture_marks.add(Line(start, end, color=cfg.CYAN, stroke_opacity=0.18, stroke_width=2))
    return Group(aura, image, outline, specular, texture_marks)


def cutaway_layers(radius: float = 1.55) -> VGroup:
    """Layered cross-section: cover, foam/backing, bladder, sensor layer."""

    outer = AnnularSector(inner_radius=radius * 0.86, outer_radius=radius, angle=TAU * 0.78, start_angle=-PI * 0.68)
    outer.set_style(fill_color=cfg.WHITE, fill_opacity=0.95, stroke_color=cfg.CYAN, stroke_width=2)
    backing = AnnularSector(inner_radius=radius * 0.66, outer_radius=radius * 0.85, angle=TAU * 0.78, start_angle=-PI * 0.68)
    backing.set_style(fill_color=cfg.BLUE, fill_opacity=0.35, stroke_color=cfg.BLUE, stroke_width=2)
    bladder = AnnularSector(inner_radius=0.0, outer_radius=radius * 0.63, angle=TAU * 0.78, start_angle=-PI * 0.68)
    bladder.set_style(fill_color=cfg.PURPLE, fill_opacity=0.18, stroke_color=cfg.PURPLE, stroke_width=2)
    missing = Sector(radius=radius * 1.02, angle=TAU * 0.18, start_angle=PI * 0.29)
    missing.set_style(fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    sensor = RoundedRectangle(width=0.54, height=0.32, corner_radius=0.05, color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=0.9)
    sensor.move_to([0.78, 0.88, 0])
    return VGroup(outer, backing, bladder, missing, sensor)


def layer_stack(labels: Iterable[tuple[str, str]]) -> VGroup:
    rows = VGroup()
    for i, (text, color) in enumerate(labels):
        rect = RoundedRectangle(width=4.2, height=0.44, corner_radius=0.08, stroke_color=color, fill_color=color, fill_opacity=0.22)
        label = small_label(text, color=cfg.WHITE, font_size=24).move_to(rect)
        rows.add(VGroup(rect, label))
    rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    return rows


def old_stitched_ball(radius: float = 1.1) -> VGroup:
    ball = Circle(radius=radius, color=cfg.MUTED, fill_color="#DDE7EE", fill_opacity=0.94, stroke_width=2)
    seams = VGroup()
    for angle in np.linspace(0, TAU, 10, endpoint=False):
        chord = Line(LEFT * radius * 0.86, RIGHT * radius * 0.86, color=cfg.GRAY, stroke_width=2, stroke_opacity=0.7)
        chord.rotate(angle)
        seams.add(DashedVMobject(chord, num_dashes=14))
    stitches = VGroup()
    for x in np.linspace(-0.75, 0.75, 9):
        stitches.add(Line([x, -0.08, 0], [x + 0.1, 0.08, 0], color=cfg.RED, stroke_width=2))
    stitches.move_to([0, 0.28, 0])
    return VGroup(ball, seams, stitches)


def four_panel_map(radius: float = 1.1) -> Group:
    ball = trionda_ball(radius=radius)
    label = small_label("4 controlled panels", color=cfg.GREEN, font_size=28).next_to(ball, DOWN, buff=0.28)
    return Group(ball, label)


def twenty_panel_map(radius: float = 1.1) -> VGroup:
    ball = Circle(radius=radius, color=cfg.MUTED, fill_color="#DCE6EE", fill_opacity=0.92)
    lines = VGroup()
    for angle in np.linspace(0, TAU, 10, endpoint=False):
        lines.add(Line(LEFT * radius * 0.86, RIGHT * radius * 0.86, color=cfg.GRAY, stroke_width=2).rotate(angle))
    for y in [-0.55, 0, 0.55]:
        lines.add(DashedVMobject(Line(LEFT * radius * 0.9, RIGHT * radius * 0.9, color=cfg.GRAY, stroke_width=2).shift(UP * y)))
    label = small_label("older many-panel map", color=cfg.MUTED, font_size=28).next_to(ball, DOWN, buff=0.28)
    return VGroup(ball, lines, label)


def flow_lines(center: np.ndarray, radius: float, rough: bool) -> VGroup:
    from utils.physics_models import airflow_streamlines

    lines = VGroup()
    for points in airflow_streamlines(center[0], center[1], radius, rough=rough):
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in points])
        path.set_stroke(cfg.CYAN if rough else cfg.MUTED, width=3, opacity=0.9)
        lines.add(path)
    return lines


def wake_cloud(center: np.ndarray, rough: bool) -> VGroup:
    cloud = VGroup()
    spread = 1.1 if rough else 1.85
    color = cfg.BLUE if rough else cfg.ORANGE
    for i in range(18 if rough else 28):
        x = center[0] + 1.3 + (i % 7) * 0.28
        y = center[1] + ((i * 1.7) % 2 - 1) * spread * (0.18 + 0.03 * (i % 3))
        cloud.add(Circle(radius=0.07 + 0.02 * (i % 3), color=color, stroke_opacity=0, fill_opacity=0.16).move_to([x, y, 0]))
    return cloud


def sensor_chip() -> VGroup:
    body = RoundedRectangle(width=0.72, height=0.44, corner_radius=0.06, color=cfg.GOLD, fill_color=cfg.GOLD, fill_opacity=0.95)
    core = Rectangle(width=0.34, height=0.2, color=cfg.BLACKISH, fill_color=cfg.BLACKISH, fill_opacity=0.9).move_to(body)
    pins = VGroup()
    for side in [-1, 1]:
        for y in [-0.14, 0, 0.14]:
            pins.add(Line([side * 0.36, y, 0], [side * 0.5, y, 0], color=cfg.GOLD, stroke_width=2))
    return VGroup(body, core, pins)


def data_pulses(count: int = 10, color: str = cfg.CYAN) -> VGroup:
    pulses = VGroup()
    for i in range(count):
        dot = Dot(radius=0.055, color=color)
        dot.shift(RIGHT * i * 0.24)
        pulses.add(dot)
    pulses.center()
    return pulses


def make_player(color: str, label: str) -> VGroup:
    head = Circle(radius=0.12, color=color, fill_color=color, fill_opacity=1)
    body = Line(DOWN * 0.1, DOWN * 0.55, color=color, stroke_width=6)
    legs = VGroup(Line(DOWN * 0.55, DOWN * 0.86 + LEFT * 0.18, color=color, stroke_width=4), Line(DOWN * 0.55, DOWN * 0.86 + RIGHT * 0.18, color=color, stroke_width=4))
    text = small_label(label, color=color, font_size=20).next_to(legs, DOWN, buff=0.08)
    return VGroup(head, body, legs, text)
