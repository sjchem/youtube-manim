"""Reusable visual primitives for the Magnus effect animation."""

from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path

import numpy as np
from manim import *

import config as cfg
from utils.math_utils import cubic_bezier, rescale_points


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    """Play with a project-wide pacing scale."""
    kwargs["run_time"] = kwargs.get("run_time", 1.0) * cfg.TIMING["pace_scale"]
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, duration: float = 1.0) -> None:
    """Wait with project pacing."""
    scene.wait(duration * cfg.TIMING["pace_scale"])


def scene_transition(scene: Scene, run_time: float = 0.5) -> None:
    """Fade out all objects in a scene."""
    if scene.mobjects:
        paced_play(scene, FadeOut(*scene.mobjects), run_time=run_time)
    narration_wait(scene, 0.1)


def begin_scene(scene: Scene) -> float:
    """Return the current Manim scene clock in seconds."""
    return float(getattr(scene, "time", 0.0))


def end_scene(scene: Scene, start_time: float, target_seconds: float, transition_run_time: float = 0.5) -> None:
    """Pad a scene so its total duration matches the narration window."""
    elapsed = float(getattr(scene, "time", 0.0)) - start_time
    transition_seconds = (transition_run_time + 0.1) * cfg.TIMING["pace_scale"]
    remaining = target_seconds - elapsed - transition_seconds
    if remaining > 0:
        scene.wait(remaining)
    scene_transition(scene, run_time=transition_run_time)


def cinematic_background(show_bubbles: bool = True) -> VGroup:
    """Create an Oceanic scientific background."""
    base = Rectangle(
        width=16.4,
        height=9.3,
        fill_color=cfg.BG,
        fill_opacity=1,
        stroke_width=0,
    )
    grid = VGroup()
    for x in np.linspace(-8, 8, 21):
        grid.add(Line([x, -4.5, 0], [x, 4.5, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.22, stroke_width=1))
    for y in np.linspace(-4.4, 4.4, 12):
        grid.add(Line([-8, y, 0], [8, y, 0], stroke_color=cfg.COLORS["line"], stroke_opacity=0.16, stroke_width=1))
    bubbles = cfg.oceanic_bubbles(count=42, opacity=0.10) if show_bubbles else VGroup()
    return VGroup(base, grid, bubbles)


def glow(mobject: Mobject, color: str = cfg.CYAN, scale_steps: int = 4, opacity: float = 0.16) -> VGroup:
    """Duplicate a mobject with soft glowing strokes."""
    layers = VGroup()
    for index in range(scale_steps, 0, -1):
        layer = mobject.copy()
        if hasattr(layer, "set_stroke"):
            layer.set_stroke(color, width=cfg.VISUAL["stroke_width"] + index * 3, opacity=opacity / index)
        layer.set_opacity(opacity / max(index, 1))
        layers.add(layer)
    return VGroup(layers, mobject)


def label_text(text: str, font_size: int | None = None, color: str = cfg.WHITE, weight: str = NORMAL) -> Text:
    """Create a compact readable text label."""
    return Text(text, font_size=font_size or cfg.FONT_SIZES["label"], color=color, weight=weight)


def title_stack(title: str, subtitle: str | None = None) -> VGroup:
    """Create a clean title stack."""
    title_mob = Text(title, font_size=cfg.FONT_SIZES["title"], color=cfg.WHITE, weight=BOLD)
    underline = Line(LEFT * min(title_mob.width, 7) / 2, RIGHT * min(title_mob.width, 7) / 2, color=cfg.CYAN, stroke_width=4)
    underline.next_to(title_mob, DOWN, buff=0.18)
    group = VGroup(title_mob, underline)
    if subtitle:
        sub = Text(subtitle, font_size=cfg.FONT_SIZES["subtitle"], color=cfg.MUTED)
        sub.next_to(underline, DOWN, buff=0.24)
        group.add(sub)
    return group


def football(radius: float = 0.36, trionda: bool = False, spin_marks: bool = False) -> VGroup:
    """Create a stylized football with optional Trionda-like colored panels."""
    shell = Circle(radius=radius, fill_color=cfg.WHITE, fill_opacity=1, stroke_color=cfg.CYAN, stroke_width=2.6)
    shadow = Circle(radius=radius * 1.05, stroke_color=cfg.CYAN, stroke_opacity=0.18, stroke_width=9)
    panels = VGroup()
    if trionda:
        colors = [cfg.RED, cfg.GREEN, cfg.BLUE, cfg.GOLD]
        for i, color in enumerate(colors):
            arc = Arc(radius=radius * (0.58 + 0.06 * (i % 2)), start_angle=i * TAU / 4 + 0.18, angle=TAU / 3.2, color=color, stroke_width=5)
            panels.add(arc)
        for i in range(12):
            angle = i * TAU / 12
            dot = Dot([cos(angle) * radius * 0.62, sin(angle) * radius * 0.62, 0], radius=radius * 0.025, color=cfg.COLORS["line_soft"])
            panels.add(dot)
    else:
        pent = RegularPolygon(n=5, radius=radius * 0.26, color=cfg.COLORS["line_soft"], fill_color=cfg.COLORS["line_soft"], fill_opacity=0.18)
        panels.add(pent)
        for i in range(5):
            angle = i * TAU / 5 + PI / 2
            panels.add(Line(ORIGIN, [cos(angle) * radius * 0.78, sin(angle) * radius * 0.78, 0], color=cfg.COLORS["line_soft"], stroke_width=1.6))
    group = VGroup(shadow, shell, panels)
    if spin_marks:
        arcs = VGroup()
        for shift, color in [(-0.18, cfg.ORANGE), (0.18, cfg.ORANGE)]:
            mark = Arc(radius=radius * 1.23, start_angle=PI * 0.1 + shift, angle=PI * 0.72, color=color, stroke_width=4)
            tip = Triangle(color=color, fill_color=color, fill_opacity=1).scale(radius * 0.08)
            end_angle = PI * 0.1 + shift + PI * 0.72
            tip.move_to([cos(end_angle) * radius * 1.23, sin(end_angle) * radius * 1.23, 0])
            tip.rotate(end_angle - PI / 2)
            arcs.add(mark, tip)
        group.add(arcs)
    return group


def trionda_image_ball(width: float = 0.52) -> Mobject:
    """Create a moving ball from the local Trionda PNG, with vector fallback."""
    path = Path(cfg.TRIONDA_IMAGE)
    if not path.exists():
        return football(radius=width / 2, trionda=True)
    try:
        image = ImageMobject(str(path))
    except Exception:
        return football(radius=width / 2, trionda=True)
    image.set_width(width)
    shadow = Circle(
        radius=width * 0.52,
        fill_color="#031E17",
        fill_opacity=0.42,
        stroke_color=cfg.CYAN,
        stroke_opacity=0.22,
        stroke_width=6,
    )
    return Group(shadow, image)


def goal_top_view(width: float = 2.6, depth: float = 1.0) -> VGroup:
    """Create a top-view goal mouth."""
    post_l = Line([0, -width / 2, 0], [0, width / 2, 0], color=cfg.WHITE, stroke_width=7)
    net_back = Line([depth, -width / 2, 0], [depth, width / 2, 0], color=cfg.COLORS["line_soft"], stroke_width=2)
    side_a = Line([0, -width / 2, 0], [depth, -width / 2, 0], color=cfg.COLORS["line_soft"], stroke_width=2)
    side_b = Line([0, width / 2, 0], [depth, width / 2, 0], color=cfg.COLORS["line_soft"], stroke_width=2)
    net = VGroup()
    for i in range(6):
        alpha = i / 5
        y = -width / 2 + alpha * width
        net.add(Line([0, y, 0], [depth, y, 0], color=cfg.COLORS["line_soft"], stroke_width=1, stroke_opacity=0.6))
    return VGroup(side_a, side_b, net_back, net, post_l)


def pitch_top_view() -> VGroup:
    """Create a simplified top-view free-kick pitch."""
    grass = Rectangle(width=14.2, height=6.8, fill_color=cfg.COLORS["grass"], fill_opacity=0.72, stroke_color=cfg.COLORS["line_soft"], stroke_width=2)
    bands = VGroup()
    for i in range(7):
        band = Rectangle(width=14.2 / 7, height=6.8, fill_color=cfg.COLORS["grass_2"], fill_opacity=0.16 if i % 2 == 0 else 0.05, stroke_width=0)
        band.move_to([-7.1 + (i + 0.5) * 14.2 / 7, 0, 0])
        bands.add(band)
    center_line = Line([0, -3.4, 0], [0, 3.4, 0], color=cfg.COLORS["line_soft"], stroke_opacity=0.42, stroke_width=2)
    box = Rectangle(width=2.0, height=4.3, color=cfg.COLORS["line_soft"], stroke_opacity=0.55, stroke_width=2).move_to([5.9, 0, 0])
    return VGroup(grass, bands, center_line, box)


def path_from_points(points: list[np.ndarray], color: str = cfg.GREEN, width: float = 5, opacity: float = 1.0) -> VMobject:
    """Create a smooth path from coordinate points."""
    path = VMobject()
    path.set_points_smoothly(points)
    path.set_stroke(color=color, width=width, opacity=opacity)
    return path


def path_arrow_tip(path: Mobject, color: str, scale: float = 0.16) -> Triangle:
    """Create an arrow tip aligned with the end of a path."""
    path_source = path
    if hasattr(path, "has_no_points") and path.has_no_points():
        path_pieces = path.family_members_with_points()
        if path_pieces:
            path_source = path_pieces[-1]
    end = np.array(path_source.point_from_proportion(1.0))
    before = np.array(path_source.point_from_proportion(0.04 if path_source is not path else 0.96))
    direction = end - before
    angle = np.arctan2(direction[1], direction[0])
    tip = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_color=cfg.WHITE, stroke_width=1.2)
    tip.scale(scale)
    tip.move_to(end)
    tip.rotate(angle - PI / 2)
    return tip


def expected_and_curved_paths() -> tuple[VMobject, VMobject]:
    """Return the hook-scene straight and curved paths in screen coordinates."""
    start = (-5.7, -1.65)
    end_x = 5.85
    miss_end_y = -2.16
    straight = [
        np.array([x, start[1] + (miss_end_y - start[1]) * (x - start[0]) / (end_x - start[0]), 0])
        for x in np.linspace(start[0], end_x, 28)
    ]
    curved_raw = cubic_bezier(start, (-2.55, -2.16), (2.25, -1.48), (5.82, -0.34), samples=56)
    curved = [np.array([x, y, 0]) for x, y in curved_raw]
    miss_path = DashedVMobject(path_from_points(straight, cfg.RED, width=7, opacity=0.94), num_dashes=30, dashed_ratio=0.62)
    curve_path = path_from_points(curved, cfg.GREEN, width=7.5, opacity=1)
    return miss_path, curve_path


def airflow_lines(spinning: bool = False, count: int = 9, color: str = cfg.BLUE) -> VGroup:
    """Create airflow lines around a central ball."""
    lines = VGroup()
    ys = np.linspace(-1.55, 1.55, count)
    for i, y in enumerate(ys):
        phase = (i - count / 2) * 0.08
        if spinning:
            points = [
                np.array([-5.0, y, 0]),
                np.array([-2.1, y + 0.12 * sin(i), 0]),
                np.array([-0.65, y + 0.42 * np.exp(-abs(y)) + phase, 0]),
                np.array([0.85, y - 0.45 * np.exp(-abs(y)) + phase, 0]),
                np.array([3.4, y - 0.65 + phase, 0]),
            ]
        else:
            points = [
                np.array([-5.0, y, 0]),
                np.array([-2.0, y, 0]),
                np.array([-0.8, y + 0.18 * np.sign(y) * np.exp(-abs(y)), 0]),
                np.array([0.8, y + 0.18 * np.sign(y) * np.exp(-abs(y)), 0]),
                np.array([3.4, y, 0]),
            ]
        line = path_from_points(points, color=color, width=2.2, opacity=0.65)
        lines.add(line)
    return lines


def wake_ribbon(color: str = cfg.ORANGE) -> VGroup:
    """Create a tilted wake ribbon behind a spinning ball."""
    ribbons = VGroup()
    for offset, opacity in [(-0.25, 0.45), (0.0, 0.7), (0.25, 0.42)]:
        pts = [
            np.array([0.45, offset, 0]),
            np.array([1.3, offset - 0.24, 0]),
            np.array([2.2, offset - 0.55, 0]),
            np.array([3.55, offset - 0.9, 0]),
        ]
        ribbons.add(path_from_points(pts, color=color, width=5, opacity=opacity))
    return ribbons


def vector_arrow(start: np.ndarray | list[float], end: np.ndarray | list[float], color: str, label: str | None = None) -> VGroup:
    """Create a glowing vector arrow with optional MathTex label."""
    arrow = Arrow(start, end, buff=0, color=color, stroke_width=cfg.VISUAL["arrow_stroke"], max_tip_length_to_length_ratio=0.18)
    glow_arrow = arrow.copy().set_stroke(color, width=15, opacity=0.12)
    group = VGroup(glow_arrow, arrow)
    if label:
        lab = MathTex(label, color=color, font_size=cfg.FONT_SIZES["label"])
        lab.next_to(arrow, UP, buff=0.18)
        group.add(lab)
    return group


def equation(text: str, color: str = cfg.WHITE, font_size: int | None = None) -> MathTex:
    """Create a readable MathTex equation."""
    return MathTex(text, color=color, font_size=font_size or cfg.FONT_SIZES["equation"])


def force_equation_card(text: str, color: str = cfg.WHITE) -> VGroup:
    """Create an equation with a restrained technical frame."""
    eq = equation(text, color=color, font_size=44)
    box = RoundedRectangle(corner_radius=0.12, width=eq.width + 0.7, height=eq.height + 0.45, stroke_color=color, stroke_opacity=0.68, fill_color=cfg.COLORS["panel"], fill_opacity=0.72)
    halo = box.copy().set_stroke(color, width=9, opacity=0.10)
    return VGroup(halo, box, eq)


def load_reference_image(max_width: float = 8.4) -> Mobject | None:
    """Try to load a reference image, returning None on failure."""
    for candidate in cfg.REFERENCE_IMAGE_CANDIDATES:
        path = Path(candidate)
        if not path.exists():
            continue
        try:
            image = ImageMobject(str(path))
        except Exception:
            continue
        image.set_width(max_width)
        return image
    return None


def ball_history_montage() -> VGroup:
    """Create a vector montage from early balls to Trionda."""
    from utils.physics_models import world_cup_ball_milestones

    items = VGroup()
    for index, item in enumerate(world_cup_ball_milestones()):
        is_trionda = item["year"] == 2026
        ball = football(radius=0.28, trionda=is_trionda)
        year = Text(str(item["year"]), font_size=18, color=cfg.GOLD if is_trionda else cfg.MUTED)
        note = Text(str(item["note"]), font_size=15, color=cfg.CYAN if is_trionda else cfg.MUTED)
        stack = VGroup(ball, year, note).arrange(DOWN, buff=0.12)
        stack.move_to([-5.5 + index * 2.18, 0, 0])
        items.add(stack)
    line = Line(items[0].get_center() + DOWN * 0.85, items[-1].get_center() + DOWN * 0.85, color=cfg.COLORS["line_soft"], stroke_width=2)
    return VGroup(line, items)


def speed_graph(width: float = 5.8, height: float = 2.7) -> VGroup:
    """Create a schematic drag crisis graph with a Trionda marker."""
    from utils.physics_models import drag_crisis_profile

    axes = Axes(
        x_range=[20, 100, 20],
        y_range=[0.18, 0.5, 0.1],
        x_length=width,
        y_length=height,
        axis_config={"color": cfg.MUTED, "stroke_width": 2, "include_tip": False},
        tips=False,
    )
    points = [axes.c2p(x, y) for x, y in drag_crisis_profile()]
    curve = path_from_points(points, cfg.CYAN, width=4)
    marker_x = 43
    marker = DashedLine(axes.c2p(marker_x, 0.18), axes.c2p(marker_x, 0.49), color=cfg.GOLD, stroke_width=3, dash_length=0.08)
    label = Text("~43 km/h", font_size=18, color=cfg.GOLD).next_to(marker, UP, buff=0.08)
    xlab = Text("speed", font_size=18, color=cfg.MUTED).next_to(axes.x_axis, DOWN, buff=0.18)
    ylab = Text("drag", font_size=18, color=cfg.MUTED).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.15)
    return VGroup(axes, curve, marker, label, xlab, ylab)
