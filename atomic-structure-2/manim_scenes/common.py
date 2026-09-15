"""Shared visual language for the quantum sequel.

Every recurring object on screen is built here exactly once: the nucleus, the
electron, the classical orbit, the matter wave, the standing wave on a ring,
the wave packet, the calculated orbital surfaces, the orbital-box diagram, the
energy shelves and the periodic table. A chapter composes these; it does not
redraw them.

The film is one continuous ``QuantumScene``. Each chapter hands the next one a
living anchor -- the diagram currently carrying the argument -- so the whole
24-minute film reads as a single transformation rather than sixteen separate
title cards:

    ORBIT -> WAVE -> PROBABILITY -> ORBITAL -> ATOM -> CHEMISTRY
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from manim import *

import config as cfg
from utils.physics_models import (
    grid_extent,
    occupancy,
    orbital_geometry,
    psi,
    sample_positions,
    wave_packet,
)


# ---------------------------------------------------------------------------
# Typography
#
# Every glyph the viewer must read carries a background stroke in the ground
# colour. On a busy frame -- a cloud of detections, a lit orbital -- unstroked
# text dissolves into whatever happens to be behind it.
# ---------------------------------------------------------------------------


def outlined_text(
    body: str,
    font_size: int | None = None,
    color: str = cfg.WHITE,
    weight=BOLD,
    limit: float = 14.0,
) -> Text:
    """The film's standard on-screen words: bold, legible, separated from the art."""
    label = Text(body, font="DejaVu Sans", font_size=font_size or cfg.FONT["label"], color=color, weight=weight)
    label.set_stroke(cfg.BG, width=4, opacity=0.95, background=True)
    if label.width > limit:
        label.scale_to_fit_width(limit)
    return label


def text(body: str, size: int | None = None, color: str = cfg.WHITE) -> Text:
    """Short alias used throughout the chapters."""
    return outlined_text(body, size, color)


def eq(
    latex: str,
    color: str = cfg.WHITE,
    font_size: int | None = None,
    *,
    limit: float = 13.5,
    substrings_to_isolate: Sequence[str] | None = None,
) -> MathTex:
    formula = MathTex(
        latex,
        color=color,
        font_size=font_size or cfg.FONT["section"],
        substrings_to_isolate=list(substrings_to_isolate or ()),
    )
    formula.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    if formula.width > limit:
        formula.scale_to_fit_width(limit)
    return formula


def equation(latex: str, size: int | None = None, color: str = cfg.WHITE) -> MathTex:
    """Short alias used throughout the chapters."""
    return eq(latex, color, size)


def equation_card(latex: str, color: str = cfg.WHITE, font_size: int | None = None) -> VGroup:
    """A formula on its own lit plate, for the handful of equations that matter.

    Part 1 reserved this treatment for the two equations the whole film turned
    on. Part 2 uses it for lambda = h/p, the uncertainty relation, and the
    stationary Schroedinger equation, and for nothing else.
    """
    formula = eq(latex, color, font_size or cfg.FONT["title"])
    plate = RoundedRectangle(
        width=formula.width + 1.0,
        height=formula.height + 0.62,
        corner_radius=0.18,
        stroke_color=color,
        stroke_opacity=0.6,
        fill_color=cfg.PANEL,
        fill_opacity=0.90,
    )
    glow = plate.copy().set_stroke(color, width=14, opacity=0.08)
    return VGroup(glow, plate, formula)


def chip(body: str, color: str = cfg.CYAN, font_size: int | None = None) -> VGroup:
    """A small labelled plate, used for the film's concept chains."""
    label = outlined_text(body, font_size or cfg.FONT["tiny"], color, BOLD)
    frame = RoundedRectangle(
        width=label.width + 0.50,
        height=label.height + 0.44,
        corner_radius=0.14,
        color=color,
        stroke_width=2.8,
        fill_color=cfg.PANEL,
        fill_opacity=0.80,
    )
    return VGroup(frame, label)


def title_card(title: str, subtitle: str | None = None, color: str = cfg.GOLD) -> VGroup:
    """The film's hero title: a glowing shadow under a rule-and-subtitle stack."""
    heading = outlined_text(title, cfg.FONT["title"], color, BOLD, limit=cfg.SAFE_WIDTH)
    shadow = heading.copy().set_color(color).set_opacity(0.18).set_stroke(width=0, background=True)
    shadow.shift(DOWN * 0.06 + RIGHT * 0.06).scale(1.02)
    # A drop shadow belongs under its own glyphs, so the layout audit is told to
    # skip it rather than reporting the deliberate overlap as a collision.
    for glyph in shadow.get_family():
        glyph._is_decorative = True
    stacked = VGroup(shadow, heading)
    rule = Line(
        LEFT * min(heading.width * 0.48, 5.7),
        RIGHT * min(heading.width * 0.48, 5.7),
        color=cfg.CYAN,
        stroke_width=4,
    )
    card = VGroup(stacked, rule).arrange(DOWN, buff=0.22)
    if subtitle:
        card.add(outlined_text(subtitle, cfg.FONT["body"], cfg.WHITE, BOLD, limit=cfg.SAFE_WIDTH - 0.5))
        card.arrange(DOWN, buff=0.24)
    return card


def check_mark(size: float = 0.30, color: str = cfg.GREEN) -> VMobject:
    stroke = VMobject(color=color, stroke_width=max(5.0, size * 22))
    stroke.set_points_as_corners(
        [LEFT * size, LEFT * size * 0.15 + DOWN * size * 0.72, RIGHT * size * 1.05 + UP * size * 0.78]
    )
    return stroke


def cross_mark(size: float = 0.28, color: str = cfg.RED) -> VGroup:
    width = max(5.0, size * 22)
    return VGroup(
        Line(LEFT * size + DOWN * size, RIGHT * size + UP * size, color=color, stroke_width=width),
        Line(LEFT * size + UP * size, RIGHT * size + DOWN * size, color=color, stroke_width=width),
    )


# ---------------------------------------------------------------------------
# Glow primitives
# ---------------------------------------------------------------------------


def halo(radius: float, color: str, layers: int = 4, peak_opacity: float = 0.18) -> VGroup:
    """Concentric soft discs, the film's standard way of making something glow."""
    group = VGroup()
    for index in range(layers):
        fraction = (index + 1) / layers
        group.add(
            Circle(
                radius=radius * (1.0 + 0.85 * fraction),
                color=color,
                stroke_width=0,
                fill_color=color,
                fill_opacity=peak_opacity * (1.0 - fraction) ** 2,
            )
        )
    return group


def glow_dot(point=ORIGIN, radius: float = 0.13, color: str = cfg.CYAN) -> VGroup:
    """A bead with its own light around it."""
    group = halo(radius, color, layers=3, peak_opacity=0.26)
    group.add(Dot(ORIGIN, radius=radius, color=color).set_stroke(cfg.WHITE, width=1.4, opacity=0.55))
    return group.move_to(point)


def glow_curve(curve: VMobject, color: str | None = None, spread: float = 3.4, opacity: float = 0.13) -> VGroup:
    """Lay a wide faint copy under a curve so it reads as light, not as wire.

    A one-pixel sine on a dark ground looks like a technical drawing. The same
    sine over its own bloom looks like something luminous, which is what the
    matter-wave chapters are actually about.
    """
    tone = color or curve.get_color()
    bloom = curve.copy().set_stroke(tone, width=curve.get_stroke_width() * spread, opacity=opacity)
    return VGroup(bloom, curve)


def glow_line(start, end, color: str, width: float = 5) -> VGroup:
    return VGroup(
        Line(start, end, color=color, stroke_width=width * 3.2, stroke_opacity=0.12),
        Line(start, end, color=color, stroke_width=width),
    )


def dashed_connector(start, end, color: str = cfg.MUTED, dashes: int = 12, stroke_width: float = 2.6) -> VGroup:
    """A dashed guide assembled from separate segments, safe to fade out."""
    first = np.array(start, dtype=float)
    last = np.array(end, dtype=float)
    group = VGroup()
    for index in range(dashes):
        a, b = index / dashes, (index + 0.55) / dashes
        group.add(Line(first + (last - first) * a, first + (last - first) * b, color=color, stroke_width=stroke_width))
    return group


# ---------------------------------------------------------------------------
# Background
#
# Two layers with different jobs. The flat ground carries the 2D chapters; it
# is a rectangle in the z = 0 plane, so it has to leave before the camera tilts
# or it renders as a skewed slab across the frame. The mote field is genuinely
# three-dimensional and stays: while the camera turns around an orbital, those
# points drift past at different rates and give the shot its only depth cue.
# ---------------------------------------------------------------------------


def deep_field() -> VGroup:
    """The Oceanic ground: a faint grid under a slow vertical drift of bubbles."""
    base = Rectangle(width=16.4, height=9.3, fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    grid = VGroup()
    for x in np.linspace(-8, 8, 17):
        grid.add(Line([x, -4.65, 0], [x, 4.65, 0], color="#173653", stroke_width=0.65, stroke_opacity=0.16))
    for y in np.linspace(-4.5, 4.5, 10):
        grid.add(Line([-8.2, y, 0], [8.2, y, 0], color="#173653", stroke_width=0.65, stroke_opacity=0.11))

    rng = np.random.default_rng(cfg.SEED)
    bubbles = VGroup()
    for index in range(14):
        radius = float(rng.uniform(0.05, 0.42))
        centre = [float(rng.uniform(-7.2, 7.2)), float(rng.uniform(-4.2, 4.2)), 0.0]
        opacity = float(rng.uniform(0.012, 0.030))
        body = Circle(
            radius=radius,
            color=cfg.CYAN,
            stroke_width=max(0.7, radius * 5.0),
            stroke_opacity=min(opacity * 2.4, 0.12),
            fill_color=cfg.CYAN,
            fill_opacity=opacity,
        ).move_to(centre)
        shine = Circle(radius=radius * 0.18, color="#E8FAFF", stroke_width=0, fill_opacity=min(opacity * 2.1, 0.085))
        shine.move_to(centre).shift(LEFT * radius * 0.34 + UP * radius * 0.34)
        speed = 0.018 + 0.003 * (index % 5)

        def drift(mob: Mobject, dt: float, velocity: float = speed) -> None:
            mob.shift(UP * velocity * dt)
            if mob.get_bottom()[1] > 4.65:
                mob.shift(DOWN * 9.3)

        bubble = VGroup(body, shine)
        bubble.add_updater(drift)
        bubbles.add(bubble)

    layers = VGroup(base, grid, bubbles)
    layers._is_project_background = True
    return layers


def mote_field(count: int = 90, radius: float = 9.0) -> VGroup:
    """A sparse shell of dim points, for parallax while the 3D camera turns."""
    rng = np.random.default_rng(cfg.SEED + 7)
    motes = VGroup()
    for _ in range(count):
        direction = rng.normal(size=3)
        direction /= np.linalg.norm(direction)
        point = direction * radius * float(rng.uniform(0.75, 1.0))
        mote = Dot(point, radius=float(rng.uniform(0.012, 0.030)), color=cfg.CYAN)
        mote.set_opacity(float(rng.uniform(0.10, 0.34)))
        motes.add(mote)
    motes._is_project_background = True
    return motes


# ---------------------------------------------------------------------------
# The cast: nucleus, electron, the classical orbit
# ---------------------------------------------------------------------------


def nucleus(radius: float = 0.22, color: str = cfg.NUCLEUS_COLOR, nucleons: bool = True) -> VGroup:
    """A dense, hot core: a glow, a shell, and a suggestion of packed nucleons."""
    group = halo(radius, color, layers=4, peak_opacity=0.22)
    group.add(Circle(radius=radius, color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.94))
    if nucleons and radius >= 0.18:
        packing = VGroup()
        for index, angle in enumerate(np.linspace(0, TAU, 7, endpoint=False)):
            offset = radius * 0.44 * np.array([np.cos(angle), np.sin(angle), 0.0])
            tone = cfg.PROTON_COLOR if index % 2 == 0 else "#FFB4A2"
            packing.add(Dot(offset, radius=radius * 0.26, color=tone).set_opacity(0.85))
        packing.add(Dot(ORIGIN, radius=radius * 0.26, color=cfg.PROTON_COLOR).set_opacity(0.9))
        group.add(packing)
    group.add(
        Arc(radius=radius * 0.72, start_angle=40 * DEGREES, angle=95 * DEGREES,
            color=cfg.WHITE, stroke_width=2.6, stroke_opacity=0.42)
    )
    return group


def electron(radius: float = 0.15, color: str = cfg.ELECTRON_COLOR, sign: bool = True) -> VGroup:
    """The film's electron: a cool glowing bead carrying a minus sign."""
    group = glow_dot(ORIGIN, radius, color)
    if sign and radius >= 0.12:
        group.add(Line(LEFT * radius * 0.48, RIGHT * radius * 0.48, color=cfg.BG, stroke_width=max(2.0, radius * 11)))
    return group


def orbit(radius: float = 2.3, nucleus_radius: float = 0.22, electron_radius: float = 0.15) -> VGroup:
    """The familiar textbook atom: a core, a track, and a bead riding the track.

    Returned as ``VGroup(core, ring, bead)`` in that order, because the whole
    film depends on being able to destroy the ring while the core stays put.
    """
    ring = Circle(radius=radius, color=cfg.MUTED, stroke_width=2.4, stroke_opacity=0.62)
    group = VGroup(nucleus(nucleus_radius), ring, electron(electron_radius).move_to([radius, 0, 0]))
    group.visual_kind = "orbit"
    return group


def spine_strip(active: int | None = None, font_size: int | None = None) -> VGroup:
    """The film's argument as six stations, with the current one lit.

    Part 2 is a single long transformation, and a viewer who loses the thread
    loses the film. This strip is shown for a few seconds at the joins, never
    parked permanently on the frame.
    """
    plates = VGroup()
    for index, station in enumerate(cfg.SPINE):
        lit = active is not None and index <= active
        current = active is not None and index == active
        colour = cfg.GOLD if current else (cfg.CYAN if lit else cfg.GRAY)
        plate = chip(station, colour, font_size or cfg.FONT["tiny"] - 4)
        if not lit:
            plate.set_opacity(0.42)
        plates.add(plate)
    plates.arrange(RIGHT, buff=0.62)

    arrows = VGroup()
    for index in range(len(plates) - 1):
        start = plates[index].get_right()
        end = plates[index + 1].get_left()
        arrows.add(Arrow(start + RIGHT * 0.06, end + LEFT * 0.06, buff=0,
                         color=cfg.MUTED, stroke_width=2.4, max_tip_length_to_length_ratio=0.42).set_opacity(0.6))
    strip = VGroup(plates, arrows)
    if strip.width > cfg.SAFE_WIDTH:
        strip.scale_to_fit_width(cfg.SAFE_WIDTH)
    strip.plates = plates
    return strip


# ---------------------------------------------------------------------------
# Waves
# ---------------------------------------------------------------------------


def wave(width: float = 10, k: float = 4, color: str = cfg.CYAN, amplitude: float = 0.65,
         center=ORIGIN, phase: float = 0, glow: bool = True) -> VMobject:
    """A travelling matter-wave amplitude, drawn as light rather than as wire."""
    curve = ParametricFunction(
        lambda x: np.array([x, amplitude * np.sin(k * x - phase), 0]) + center,
        t_range=[-width / 2, width / 2, 0.035],
        color=color,
        stroke_width=4,
    )
    return glow_curve(curve, color) if glow else curve


def ring_wave(k: float = 5, radius: float = 2.3, amplitude: float = 0.26,
              color: str = cfg.CYAN, glow: bool = True) -> VMobject:
    """A wave wrapped around the old circular track: whole lobes, or a mismatch."""
    curve = ParametricFunction(
        lambda t: (radius + amplitude * np.sin(k * t)) * np.array([np.cos(t), np.sin(t), 0]),
        t_range=[0, TAU, 0.02],
        color=color,
        stroke_width=4,
    )
    return glow_curve(curve, color) if glow else curve


def string_mode(mode: int, phase: float = 0, span: float = 4.0, amplitude: float = 1.1,
                color: str = cfg.CYAN) -> VMobject:
    """One normal mode of a string clamped at both ends."""
    curve = ParametricFunction(
        lambda x: np.array([x, amplitude * np.sin(mode * PI * (x + span) / (2 * span)) * np.cos(phase), 0]),
        t_range=[-span, span, 0.02],
        color=color,
        stroke_width=4,
    )
    return glow_curve(curve, color)


def packet_plot(sigma: float, carrier: float = 7.0) -> VGroup:
    """The uncertainty chapter's paired panels: a packet above, its momenta below.

    The momentum peak is rescaled for readability. Compare the horizontal
    widths of the two curves, never their plotted areas.
    """
    from utils.physics_models import sigma_p

    amplitude = ParametricFunction(
        lambda x: np.array([x, 1.55 + wave_packet(x, sigma, k=carrier), 0]),
        t_range=[-5.8, 5.8, 0.02], color=cfg.CYAN, stroke_width=3.5,
    )
    envelope = ParametricFunction(
        lambda x: np.array([x, 1.55 + np.exp(-x * x / (4 * sigma * sigma)), 0]),
        t_range=[-5.8, 5.8, 0.03], color=cfg.MUTED, stroke_width=1.6,
    ).set_stroke(opacity=0.7)
    spread = float(sigma_p(sigma))
    momentum = ParametricFunction(
        lambda p: np.array([p, -1.5 + 1.5 * np.exp(-p * p / (2 * spread * spread)), 0]),
        t_range=[-5.8, 5.8, 0.02], color=cfg.PURPLE, stroke_width=4,
    )
    return VGroup(glow_curve(amplitude, cfg.CYAN), envelope, glow_curve(momentum, cfg.PURPLE))


# ---------------------------------------------------------------------------
# Calculated orbitals
#
# The surface is extracted from a real hydrogen state with marching cubes, then
# shaded by hand. Manim's own 3D shading is switched off for the whole film
# (see cfg.apply_project_theme): it recolours a face from that face's own
# corner normals, which is fine for a Sphere and wrong for a triangle soup.
#
# The lighting is recomputed every frame from the live camera angle, and it is
# two-sided. Culling the faces that turn away would halve the work, but a d
# state has a narrow neck between its lobes, and culling opens that neck into a
# hole you can see the background through. Shading a turned-away face from its
# flipped normal costs one extra pass over an array and keeps the atom solid
# from every angle.
# ---------------------------------------------------------------------------


def _orbital_resolution(preview: int = 29, production: int = 41) -> int:
    return preview if config.pixel_height <= 480 else production


def orbital(
    scene: Scene | None,
    n: int = 1,
    l: int = 0,
    m: int = 0,
    size: float = 2.8,
    fraction: float = 0.90,
    ambient: float | None = None,
    opacity: float = 1.0,
    cut: Sequence[float] | None = None,
    cut_beyond: float | None = None,
) -> VGroup:
    """A lit isodensity surface for one hydrogen state, in display units.

    ``size`` is the radius the furthest point of the surface is scaled to, so a
    chapter can hold two different states at a comparable screen size. That is
    a display choice: these are not calibrated atomic radii.

    Pass the scene so the surface can light itself from wherever the camera is.
    Passing ``None`` lights it from the film's nominal three-quarter view, which
    is what the still-frame audits and the storyboard want.

    ``cut`` is an outward plane normal. Faces on its positive side are dropped,
    which opens the surface so a viewer can see inside it. ``cut_beyond`` spares
    everything closer to the nucleus than that display radius. That is how the
    film shows the spherical node of 2s: the outer shell is cut away and the
    inner region is simply there, with empty space between them.
    """
    triangles, normals, signs, enclosed = orbital_geometry(
        n, l, m, fraction=fraction, resolution=_orbital_resolution()
    )
    factor = size / float(np.linalg.norm(triangles.reshape(-1, 3), axis=1).max())
    triangles = triangles * factor

    if cut is not None:
        plane = np.array(cut, dtype=float)
        plane /= np.linalg.norm(plane)
        centroids = triangles.mean(axis=1)
        keep = centroids @ plane <= 0.0
        if cut_beyond is not None:
            # Open the outer shell but leave everything inside it whole. That is
            # what makes the 2s reveal work: the inner region stays a closed
            # object, with empty space between it and the shell around it.
            keep |= np.linalg.norm(centroids, axis=1) < cut_beyond
        triangles, normals, signs = triangles[keep], normals[keep], signs[keep]

    positive = np.array(ManimColor(cfg.PHASE_POS).to_rgb())
    negative = np.array(ManimColor(cfg.PHASE_NEG).to_rgb())
    base = np.where((signs >= 0)[:, None], positive, negative)
    shadow = np.array(ManimColor(cfg.SURFACE_SHADOW).to_rgb())
    highlight = np.array(ManimColor(cfg.WHITE).to_rgb())
    floor = cfg.SURFACE_AMBIENT if ambient is None else ambient

    surface = VGroup(*[Polygon(*triangle, fill_opacity=opacity, stroke_width=0) for triangle in triangles])
    for face in surface.submobjects:
        # shade_in_3d is what puts a face into the camera's depth sort. The
        # camera's own recolouring stays off; the lighting below replaces it.
        face.set_shade_in_3d(True)
    rgbas = np.stack([face.fill_rgbas[0] for face in surface.submobjects])

    def relight(mob: Mobject, dt: float = 0.0) -> None:
        if scene is not None and hasattr(scene.camera, "get_phi"):
            phi, theta = float(scene.camera.get_phi()), float(scene.camera.get_theta())
        else:
            phi, theta = 68 * DEGREES, -50 * DEGREES
        eye = np.array([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])
        up = np.array([0.0, 0.0, 1.0]) - eye * eye[2]
        up = up / np.linalg.norm(up) if np.linalg.norm(up) > 1e-6 else np.array([0.0, 1.0, 0.0])
        light = eye * 0.62 + up * 0.60 + np.cross(up, eye) * 0.50
        light /= np.linalg.norm(light)
        half = light + eye
        half /= np.linalg.norm(half)

        away = (normals @ eye) < 0
        facing = np.where(away[:, None], -normals, normals)
        # Wrap lighting: nothing falls to black, so a grazing underside reads as
        # shadow rather than as a bite taken out of the lobe.
        lambert = np.clip(0.5 + 0.5 * (facing @ light), 0, 1)
        specular = np.clip(facing @ half, 0, 1) ** 24
        rim = np.clip(1.0 - np.abs(facing @ eye), 0, 1) ** 3
        tone = floor + (1 - floor) * lambert**1.25 + 0.28 * rim
        tone = np.where(away, tone * 0.72, tone)

        colour = shadow + (base - shadow) * np.clip(tone, 0, 1.15)[:, None]
        colour += (highlight - colour) * np.where(away, 0.0, np.minimum(0.60, specular))[:, None]
        rgbas[:, :3] = colour
        for face, row in zip(mob.submobjects, rgbas):
            # Lighting owns RGB only. Fade animations update alpha on both
            # the visible mesh and their hidden start/target copies; restoring
            # the construction-time alpha here turns every dissolve into a cut.
            face.fill_rgbas[0, :3] = row[:3]

    relight(surface)
    surface.add_updater(relight)
    surface.enclosed_probability = enclosed
    surface.quantum_state = (n, l, m)
    # The flat ground is not depth-sorted, so it paints over anything that is.
    # QuantumScene reads this flag and lowers the ground before the surface lands.
    surface._needs_depth_sort = True
    return surface


def orbital_axes(size: float = 3.4, color: str = cfg.MUTED) -> VGroup:
    """A faint z axis through the nucleus: the reference m_l is measured against."""
    axis = Line([0, 0, -size], [0, 0, size], color=color, stroke_width=2, stroke_opacity=0.35)
    group = VGroup(axis)
    group._needs_depth_sort = True
    return group


def node_shell(radius: float, color: str = cfg.GOLD) -> VGroup:
    """Three orthogonal rings marking a radius at which the amplitude vanishes.

    The 90% surface of 2s is genuinely hollow -- its inner wall sits almost
    exactly on the spherical node -- so once the display is cut open there is a
    real cavity to point at, and this marks where its wall is.
    """
    rings = VGroup()
    for axis in (RIGHT, UP):
        ring = Circle(radius=radius, color=color, stroke_width=2.6, stroke_opacity=0.85)
        ring.rotate(PI / 2, axis=axis)
        rings.add(ring)
    rings.add(Circle(radius=radius, color=color, stroke_width=2.6, stroke_opacity=0.85))
    for ring in rings:
        ring.set_shade_in_3d(True)
    rings._needs_depth_sort = True
    return rings


def node_radius(n: int, l: int, m: int, size: float, fraction: float = 0.90) -> float:
    """The display radius of the innermost point of an isodensity surface."""
    triangles, *_ = orbital_geometry(n, l, m, fraction=fraction, resolution=_orbital_resolution())
    distances = np.linalg.norm(triangles.mean(axis=1), axis=1)
    return size * float(distances.min()) / float(np.linalg.norm(triangles.reshape(-1, 3), axis=1).max())


def cloud(n: int = 1, l: int = 0, m: int = 0, count: int = 600, scale: float = 1.0,
          center=ORIGIN, color: str | None = None) -> VGroup:
    """Independent detections drawn as small flat discs at three-dimensional points.

    Flat discs rather than Dot3D spheres: a few hundred sphere meshes bring the
    Cairo renderer to a crawl, and under any camera these read as a haze, which
    is all this is meant to be.
    """
    samples = sample_positions(n, l, m, count)
    # One common physical-to-display scale per principal shell, not per frame.
    samples = samples * (scale / (n * n))
    group = VGroup()
    for index, point in enumerate(samples):
        if np.linalg.norm(point) > 3.65 * scale:
            continue
        if color is None:
            colour = interpolate_color(ManimColor(cfg.CYAN), ManimColor(cfg.PURPLE), (index % 11) / 10)
        else:
            colour = ManimColor(color)
        group.add(Dot(point + center, radius=0.036, color=colour, fill_opacity=0.75 + 0.25 * (index % 7) / 6))
    return group


def density_slice(n: int = 1, l: int = 0, m: int = 0, size: float = 5.6, phase: bool = False) -> ImageMobject:
    """A labelled x-z slice through a 3D state.

    Brightness is normalized per image for visibility, so brightness must not be
    compared between two of these. A slice is a slice: it is not an integrated
    projection of what a detector would record.

    The sampling box is cropped to where the state actually lives -- the full
    grid used for the isosurfaces leaves a hydrogen 2p as a small smudge in a
    mostly empty square -- and the alpha is faded to nothing at the border so
    the image does not announce itself as a rectangle sitting on the frame.
    """
    samples = 256
    # Where the radial density has essentially run out, in Bohr radii.
    extent = {1: 4.2, 2: 11.0, 3: 21.0, 4: 34.0}.get(n, 2.2 * n * n)
    axis = np.linspace(-extent, extent, samples)
    xx, zz = np.meshgrid(axis, axis[::-1])
    points = np.stack([xx, np.zeros_like(xx), zz], axis=-1)
    amplitude = psi(n, l, m, points)
    density = np.abs(amplitude) if phase else amplitude**2
    opacity = np.clip(density / (density.max() + 1e-20), 0, 1) ** (0.55 if phase else 0.32)

    # A soft circular vignette, so the slice reads as a glow rather than a tile.
    radius = np.sqrt(xx**2 + zz**2) / extent
    opacity *= np.clip(1.0 - (np.clip(radius, 0.0, 1.0) - 0.72) / 0.28, 0.0, 1.0)

    rgba = np.zeros((samples, samples, 4), dtype=np.uint8)
    positive = np.array(ManimColor(cfg.PHASE_POS).to_rgb()) * 255
    negative = np.array(ManimColor(cfg.PHASE_NEG).to_rgb()) * 255
    rgba[..., :3] = np.where((amplitude >= 0)[..., None], positive, negative) if phase else positive
    rgba[..., 3] = (opacity * 250).astype(np.uint8)
    return ImageMobject(rgba).set_height(size)


# ---------------------------------------------------------------------------
# Diagram furniture: boxes, shelves, the table
# ---------------------------------------------------------------------------


def boxes(z: int = 0, center=ORIGIN, scale: float = 1.0) -> VGroup:
    """The orbital-box diagram for a neutral atom, H through Ar.

    A box counts occupancy of one spatial orbital. It is never a room, and the
    arrows are never trajectories; the narration says so out loud at carbon.
    """
    group = VGroup()
    labels: dict[str, Mobject] = {}
    slots: dict[tuple[str, int], Mobject] = {}
    arrows: dict[tuple[str, int, int], Mobject] = {}
    for row, (label, states) in enumerate(occupancy(z)[:4]):
        y = -2.0 + 1.35 * row
        tag = equation(label, 38).move_to([-2.5, y, 0])
        group.add(tag)
        labels[label] = tag
        for column, spins in enumerate(states):
            x = -0.9 + column * 1.25
            slot = RoundedRectangle(
                width=1.08, height=0.86, corner_radius=0.10,
                color=cfg.MUTED, stroke_width=2,
                fill_color=cfg.PANEL, fill_opacity=0.55,
            ).move_to([x, y, 0])
            group.add(slot)
            slots[(label, column)] = slot
            for index, spin in enumerate(spins):
                tip = x + (-0.22 if index == 0 else 0.22)
                arrow = Arrow(
                    [tip, y - 0.27 * spin, 0], [tip, y + 0.27 * spin, 0], buff=0,
                    color=cfg.CYAN if spin == 1 else cfg.PURPLE,
                    stroke_width=4, max_tip_length_to_length_ratio=0.3,
                )
                group.add(arrow)
                arrows[(label, column, index)] = arrow
    group.scale(scale).move_to(center)
    group.slots, group.arrows, group.labels = slots, arrows, labels
    return group


def energy_shelves(split: bool = True) -> VGroup:
    """Orbital energies: degenerate for hydrogen, separated once electrons repel.

    The spacing is schematic. In particular the 4s / 3d order shown here is a
    common filling guide for neutral atoms, not a ladder carved into space.
    """
    levels = (("1s", -2.8), ("2s", -1.55), ("2p", -0.5 if split else -1.55),
              ("3s", 0.5), ("3p", 1.35), ("4s", 2.1), ("3d", 2.85))
    group = VGroup()
    group.shelves = {}
    for name, y in levels:
        if not split and name not in ("1s", "2s", "2p"):
            continue
        x = 0 if (split or name == "1s") else (-2.2 if name == "2s" else 2.2)
        width = 7.5 if (split or name == "1s") else 3.0
        shelf = glow_line([x - width / 2, y, 0], [x + width / 2, y, 0], cfg.CYAN, 3)
        tag = equation(name, 34).move_to([x - width / 2 - 0.65, y, 0])
        group.add(shelf, tag)
        group.shelves[name] = shelf
    # The level values are physical ordering, not screen coordinates: centre the
    # finished ladder so it does not sit in the bottom half of the frame.
    group.shift(-group.get_center() + UP * 0.10)
    return group


def periodic_table() -> VGroup:
    """The first four periods, as positions rather than as a data table."""
    elements = [
        ("H", 1, 1), ("He", 1, 18),
        ("Li", 2, 1), ("Be", 2, 2), ("B", 2, 13), ("C", 2, 14), ("N", 2, 15),
        ("O", 2, 16), ("F", 2, 17), ("Ne", 2, 18),
        ("Na", 3, 1), ("Mg", 3, 2), ("Al", 3, 13), ("Si", 3, 14), ("P", 3, 15),
        ("S", 3, 16), ("Cl", 3, 17), ("Ar", 3, 18),
        ("K", 4, 1), ("Ca", 4, 2), ("Sc", 4, 3), ("Ti", 4, 4), ("V", 4, 5),
        ("Cr", 4, 6), ("Mn", 4, 7), ("Fe", 4, 8), ("Co", 4, 9), ("Ni", 4, 10),
        ("Cu", 4, 11), ("Zn", 4, 12), ("Ga", 4, 13), ("Ge", 4, 14), ("As", 4, 15),
        ("Se", 4, 16), ("Br", 4, 17), ("Kr", 4, 18),
    ]
    table = VGroup()
    table.tiles = {}
    for symbol, row, column in elements:
        colour = cfg.GOLD if column == 1 else cfg.GREEN if column == 18 else cfg.CYAN
        centre = np.array([(column - 9.5) * 0.73, (2.5 - row) * 0.85, 0])
        tile = VGroup(
            RoundedRectangle(width=0.66, height=0.73, corner_radius=0.06, color=colour,
                             fill_color=cfg.PANEL, fill_opacity=1, stroke_width=1.5),
            outlined_text(symbol, 22, colour),
        ).move_to(centre)
        table.add(tile)
        table.tiles[symbol] = tile
    return table


# ---------------------------------------------------------------------------
# Chapters 3 and 16: the shell picture the viewer already owns
#
# Every student arrives knowing the ring diagram and the string "2, 8, 1".
# The film uses it twice and for opposite purposes: chapter 3 builds it and
# lets it make its promise, chapter 16 lays it beside the subshell notation so
# the two can be read as the same statement.
# ---------------------------------------------------------------------------


def bohr_shell_atom(
    shells: Sequence[int],
    radii: Sequence[float] | None = None,
    center=ORIGIN,
    nucleus_radius: float = 0.30,
    electron_radius: float = 0.10,
    ring_color: str = cfg.MUTED,
) -> VGroup:
    """A lit nucleus inside glowing shells, with the electrons spaced on them.

    ``shells`` is the occupancy per shell, so ``(2, 8, 1)`` is sodium. The
    radii default to an even spacing rather than to n^2: the real ratios put
    n = 3 nine times further out than n = 1, which is true and unreadable.
    That rescaling is a drawing choice and the chapter says so out loud.
    """
    spacing = list(radii) if radii is not None else [1.15 + 0.92 * index for index in range(len(shells))]
    group = VGroup(nucleus(nucleus_radius))
    group.rings, group.electrons = {}, {}
    for index, (count, radius) in enumerate(zip(shells, spacing)):
        ring = Circle(radius=radius, color=ring_color, stroke_width=2.2, stroke_opacity=0.50)
        bloom = ring.copy().set_stroke(cfg.CYAN, width=9, opacity=0.055)
        group.add(bloom, ring)
        group.rings[index + 1] = ring
        beads = VGroup()
        # Start each shell at a different phase so beads do not line up into
        # spokes, which would read as a structure the model does not claim.
        offset = 0.35 * index
        for slot in range(count):
            angle = offset + TAU * slot / max(count, 1)
            beads.add(glow_dot(
                [radius * np.cos(angle), radius * np.sin(angle), 0],
                electron_radius, cfg.ELECTRON_COLOR,
            ))
        group.add(beads)
        group.electrons[index + 1] = beads
    return group.move_to(center)


def scale_ruler(
    marks: Sequence[tuple[str, float, str]],
    low: float = -40.0,
    high: float = -8.0,
    width: float = 12.0,
    center=ORIGIN,
) -> VGroup:
    """A logarithmic length axis, for putting two wavelengths in the same view.

    A cricket ball's de Broglie wavelength and an electron's differ by twenty
    powers of ten. Drawn to scale on a linear axis one of them is the whole
    frame and the other is not a pixel; the only honest way to show both at
    once is to say out loud that the axis is logarithmic, and label the decades.
    """
    axis = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=cfg.MUTED, stroke_width=3)
    group = VGroup(axis.copy().set_stroke(width=10, opacity=0.07), axis)
    group.pins = {}

    for power in range(int(low), int(high) + 1, 4):
        x = -width / 2 + width * (power - low) / (high - low)
        group.add(Line([x, -0.13, 0], [x, 0.13, 0], color=cfg.MUTED, stroke_width=2))
        group.add(eq(rf"10^{{{power}}}", cfg.MUTED, 26).move_to([x, -0.46, 0]))

    for index, (label, metres, colour) in enumerate(marks):
        power = float(np.log10(metres))
        x = -width / 2 + width * (power - low) / (high - low)
        stem = 0.70 + 0.50 * (index % 3)
        pin = VGroup(
            Line([x, 0.10, 0], [x, stem, 0], color=colour, stroke_width=2.6),
            Dot([x, 0.10, 0], radius=0.075, color=colour),
            outlined_text(label, cfg.FONT["tiny"] - 6, colour, limit=3.4).move_to([x, stem + 0.26, 0]),
        )
        group.add(pin)
        group.pins[label] = pin

    unit = outlined_text("metres  ·  logarithmic", cfg.FONT["tiny"] - 8, cfg.MUTED)
    unit.move_to([width / 2 - 1.5, -1.02, 0])
    group.add(unit)
    return group.move_to(center)


# ---------------------------------------------------------------------------
# Chapter 5: the double slit
# ---------------------------------------------------------------------------


def double_slit_rig(
    gun_x: float = -6.0,
    barrier_x: float = -1.1,
    screen_x: float = 5.1,
    gap: float = 0.62,
    separation: float = 1.05,
) -> VGroup:
    """Source, a barrier with two openings, and a detecting screen.

    Returned with named parts because the chapter has to close one slit, put a
    detector beside it, and light up individual arrivals on the screen.
    """
    barrel = VGroup(
        RoundedRectangle(width=1.15, height=0.66, corner_radius=0.12,
                         color=cfg.MUTED, stroke_width=2.4,
                         fill_color=cfg.PANEL_2, fill_opacity=0.95).move_to([gun_x, 0, 0]),
        Rectangle(width=0.34, height=0.22, color=cfg.MUTED, stroke_width=2,
                  fill_color=cfg.PANEL, fill_opacity=1).move_to([gun_x + 0.70, 0, 0]),
    )
    barrel.add(halo(0.30, cfg.CYAN, layers=3, peak_opacity=0.16).move_to([gun_x + 0.86, 0, 0]))

    top, bottom = separation / 2 + gap / 2, separation / 2 - gap / 2
    panels = VGroup()
    for low, high in ((-3.6, -top), (-bottom, bottom), (top, 3.6)):
        slab = Rectangle(width=0.26, height=high - low, color=cfg.GRAY, stroke_width=2,
                         fill_color=cfg.PANEL_2, fill_opacity=1)
        slab.move_to([barrier_x, (low + high) / 2, 0])
        panels.add(slab)

    # A detecting strip rather than a bare line: arrivals accumulate across its
    # width, and a pattern piled onto a single pixel column cannot be read.
    # 6.6 rather than 7.0: the taller panel reached into the band the chapter's
    # captions occupy, and a text/shape overlap is not something the layout
    # audit can see -- it only compares text against text.
    panel = Rectangle(width=1.02, height=6.6, color=cfg.MUTED, stroke_width=2.4,
                      fill_color=cfg.PANEL, fill_opacity=0.32).move_to([screen_x, 0, 0])
    screen = VGroup(panel.copy().set_stroke(cfg.CYAN, width=12, opacity=0.06), panel)

    rig = VGroup(barrel, panels, screen)
    rig.gun, rig.barrier, rig.screen = barrel, panels, screen
    rig.muzzle = np.array([gun_x + 0.86, 0.0, 0.0])
    rig.slits = (np.array([barrier_x, separation / 2, 0.0]), np.array([barrier_x, -separation / 2, 0.0]))
    rig.screen_x = screen_x
    return rig


def fringe_profile(y, wavenumber: float = 3.2, envelope: float = 1.75) -> np.ndarray:
    """A two-slit intensity curve: cos^2 interference under a broad envelope.

    Illustrative, not a calculation from the drawn geometry -- ``wavenumber`` is
    chosen to put six or seven readable bands across the screen rather than to
    follow from the slit spacing, which at any honest scale would give fringes
    far too fine to see. What the chapter claims is only the alternation of
    bright and dark, and that the dark gaps sit where single-slit arrivals
    would have been common.
    """
    y = np.asarray(y, dtype=float)
    return np.cos(wavenumber * y) ** 2 * np.exp(-(y**2) / (2 * envelope**2))


# ---------------------------------------------------------------------------
# Chapters 11 and 13: how far out, rather than how dense
# ---------------------------------------------------------------------------


def radial_plot(
    states: Sequence[tuple[int, int]],
    span: float = 16.0,
    width: float = 7.6,
    height: float = 3.0,
    colors: Sequence[str] | None = None,
    center=ORIGIN,
) -> VGroup:
    """Radial distribution curves P(r) = r^2 R^2, with axes in Bohr radii.

    Deliberately not the probability density. |psi_1s|^2 is *largest* at the
    nucleus; this function is zero there, because the thin shell at r = 0 has
    no volume. Its peak for 1s is exactly one Bohr radius, which is how the
    film hands Bohr's number back after taking his orbit away.
    """
    from utils.physics_models import radial_distribution

    palette = list(colors) if colors else [cfg.CYAN, cfg.GOLD, cfg.PURPLE, cfg.GREEN]
    peak = max(float(radial_distribution(n, l, np.linspace(1e-6, span, 4000)).max())
               for n, l in states)
    axes = Axes(
        x_range=[0, span, span / 4],
        y_range=[0, peak * 1.18, peak],
        x_length=width,
        y_length=height,
        tips=False,
        axis_config=dict(color=cfg.MUTED, stroke_width=2.4,
                         include_ticks=True, include_numbers=False),
    )
    group = VGroup(axes)
    group.axes = axes
    group.curves, group.peaks = {}, {}
    for index, (n, l) in enumerate(states):
        tone = palette[index % len(palette)]
        curve = axes.plot(lambda r, n=n, l=l: float(radial_distribution(n, l, r)),
                          x_range=[1e-4, span, span / 900], color=tone, stroke_width=4)
        group.add(glow_curve(curve, tone, spread=3.0, opacity=0.12))
        group.curves[(n, l)] = curve
        grid = np.linspace(1e-6, span, 6000)
        best = float(grid[int(np.argmax(radial_distribution(n, l, grid)))])
        group.peaks[(n, l)] = best
    group.move_to(center)
    return group


# ---------------------------------------------------------------------------
# Chapter 12: the address, drawn as a building
#
# The chapter is called "an address for a quantum state" and for a long time it
# only said so. A house number, a floor and a room are the three spatial labels;
# the two beds in a room are the fourth. The analogy is labelled on screen,
# because a shell is not a container and a floor is not a place.
# ---------------------------------------------------------------------------


def house(n: int, width: float = 2.05, floor_height: float = 0.62, center=ORIGIN) -> VGroup:
    """Shell n as a building: n floors, and 2l+1 rooms on floor l.

    ``.floors[l]`` is the band for subshell l and ``.rooms[(l, index)]`` is one
    room, so a chapter can light a single orbital inside a single subshell.
    """
    letters = "spdf"
    body = VGroup()
    rooms: dict[tuple[int, int], Mobject] = {}
    floors: dict[int, Mobject] = {}
    labels: dict[int, Mobject] = {}
    for l in range(n):
        slots = 2 * l + 1
        y = -((n - 1) / 2) * floor_height + l * floor_height
        band = Rectangle(width=width, height=floor_height, color=cfg.MUTED,
                         stroke_width=1.8, fill_color=cfg.PANEL, fill_opacity=0.75)
        band.move_to([0, y, 0])
        body.add(band)
        floors[l] = band
        inner = width - 0.16
        for index in range(slots):
            room = Rectangle(
                width=inner / slots - 0.055, height=floor_height - 0.17,
                color=cfg.CYAN, stroke_width=1.5, stroke_opacity=0.55,
                fill_color=cfg.PANEL_2, fill_opacity=0.9,
            )
            room.move_to([-inner / 2 + inner * (index + 0.5) / slots, y, 0])
            body.add(room)
            rooms[(l, index)] = room
        tag = outlined_text(f"{n}{letters[l]}", cfg.FONT["tiny"] - 6, cfg.CYAN)
        tag.next_to(band, LEFT, buff=0.16)
        body.add(tag)
        labels[l] = tag

    # The floors are stacked symmetrically about the origin, so the body's top
    # edge is at n * floor_height / 2. The roof sits ON that edge; putting its
    # base half a floor lower drops it through the top storey.
    eaves = n * floor_height / 2
    roof = Polygon(
        [-width / 2 - 0.20, eaves, 0],
        [width / 2 + 0.20, eaves, 0],
        [0, eaves + 0.46, 0],
        color=cfg.GOLD, stroke_width=2.2, fill_color=cfg.PANEL_2, fill_opacity=0.85,
    )
    number = outlined_text(f"n = {n}", cfg.FONT["tiny"] - 4, cfg.GOLD)
    number.next_to(roof, UP, buff=0.10)
    group = VGroup(body, roof, number)
    group.rooms, group.floors, group.labels, group.roof = rooms, floors, labels, roof
    return group.move_to(center)


def street(shells: Sequence[int] = (1, 2, 3), buff: float = 0.95, center=ORIGIN) -> VGroup:
    """Several houses side by side, aligned on a common ground line."""
    row = VGroup(*[house(n) for n in shells])
    row.arrange(RIGHT, buff=buff, aligned_edge=DOWN)
    # Along the foot of the bodies, not through the middle of the bounding box.
    base = row.get_bottom()[1] - 0.10
    ground = Line([row.get_left()[0] - 0.4, base, 0], [row.get_right()[0] + 0.4, base, 0],
                  color=cfg.MUTED, stroke_width=2.4, stroke_opacity=0.45)
    group = VGroup(row, ground)
    group.houses = {n: row[index] for index, n in enumerate(shells)}
    return group.move_to(center)


# ---------------------------------------------------------------------------
# Chapter 17: the arithmetic behind the filling order
# ---------------------------------------------------------------------------


def madelung_rows(count: int = 7, scale: float = 1.0, center=ORIGIN) -> VGroup:
    """A table of n, l and n + l for the first few subshells, in filling order.

    The chapter previously asserted the order 1s, 2s, 2p, 3s, 3p, 4s, 3d. This
    shows the arithmetic that produces it, including the tie that (n + l) alone
    does not settle: 2p and 3s both give three, and the lower n goes first.
    """
    from utils.physics_models import madelung_order

    header = VGroup(*[
        outlined_text(word, cfg.FONT["tiny"] - 4, cfg.GOLD)
        for word in ("orbital", "n", "l", "n + l")
    ])
    columns = (-2.15, -0.55, 0.55, 2.0)
    for tag, x in zip(header, columns):
        tag.move_to([x, 0, 0])

    table = VGroup(header)
    table.rows = {}
    for index, (label, n, l, total) in enumerate(madelung_order(count)):
        y = -0.58 * (index + 1)
        cells = VGroup(
            outlined_text(label, cfg.FONT["tiny"] - 2, cfg.CYAN).move_to([columns[0], y, 0]),
            equation(str(n), 32, cfg.WHITE).move_to([columns[1], y, 0]),
            equation(str(l), 32, cfg.WHITE).move_to([columns[2], y, 0]),
            equation(str(total), 34, cfg.GOLD).move_to([columns[3], y, 0]),
        )
        table.add(cells)
        table.rows[label] = cells
    rule = Line(table.get_left() + LEFT * 0.1, table.get_right() + RIGHT * 0.1,
                color=cfg.MUTED, stroke_width=2, stroke_opacity=0.5)
    rule.next_to(header, DOWN, buff=0.16).set_x(table.get_x())
    table.add(rule)
    return table.scale(scale).move_to(center)


def diagonal_chart(rows: int = 5, spacing: float = 1.12, center=ORIGIN) -> VGroup:
    """The subshell grid with the diagonal sweeps drawn across it.

    Each arrow runs along one constant value of n + l, which is exactly what
    Madelung's rule says: follow the diagonals, and inside a diagonal take the
    smaller n first.
    """
    letters = "spdf"
    tiles: dict[str, Mobject] = {}
    # Boxes and labels are kept apart so the arrows can be layered between them:
    # a diagonal necessarily runs over the very tiles it connects, so the shaft
    # has to pass above the boxes and below the text to stay readable.
    boxes_layer = VGroup()
    labels_layer = VGroup()
    for n in range(1, rows + 1):
        for l in range(min(n, len(letters))):
            label = f"{n}{letters[l]}"
            centre = [l * spacing, -n * 0.86, 0]
            box = RoundedRectangle(width=0.92, height=0.62, corner_radius=0.09,
                                   color=cfg.MUTED, stroke_width=1.8,
                                   fill_color=cfg.PANEL, fill_opacity=0.85).move_to(centre)
            text_mob = outlined_text(label, cfg.FONT["tiny"] - 6, cfg.CYAN).move_to(centre)
            boxes_layer.add(box)
            labels_layer.add(text_mob)
            tiles[label] = VGroup(box, text_mob)

    arrows = VGroup()
    for total in range(1, rows + len(letters)):
        diagonal = [(n, total - n) for n in range(1, rows + 1)
                    if 0 <= total - n < min(n, len(letters))]
        if len(diagonal) < 2:
            continue
        # `diagonal` is built in increasing n, and within one value of n + l the
        # rule takes the SMALLER n first -- 2p before 3s. So the arrow runs from
        # diagonal[0] to diagonal[-1], which on the grid is the familiar sweep
        # down and to the left. Reversing these two reverses the filling order.
        first, last = diagonal[0], diagonal[-1]
        start = tiles[f"{first[0]}{letters[first[1]]}"].get_center()
        end = tiles[f"{last[0]}{letters[last[1]]}"].get_center()
        direction = (end - start) / np.linalg.norm(end - start)
        arrows.add(Arrow(start - direction * 0.40, end + direction * 0.46, buff=0,
                         color=cfg.GOLD, stroke_width=3.4,
                         max_tip_length_to_length_ratio=0.11).set_opacity(0.85))

    chart = VGroup(boxes_layer, arrows, labels_layer)
    chart.tiles, chart.arrows = tiles, arrows
    return chart.move_to(center)


# ---------------------------------------------------------------------------
# The continuous scene
#
# One class runs the whole film. `anchor` is the diagram currently carrying the
# argument; a chapter transforms it rather than opening on a blank frame, and
# `finish()` refuses to end a chapter that has left anything visible outside it.
# ---------------------------------------------------------------------------


class QuantumScene(ThreeDScene):
    """All chapters share one anchor; FullVideo never resets between them."""

    # -- Chapter lifecycle ---------------------------------------------------

    def prepare(self, key: str) -> None:
        """Open a chapter: start its clock, and build the ground exactly once."""
        self.key = key
        self.chapter_start = self.time
        self.chapter_target = cfg.DURATIONS[key] / cfg.SPEED
        if not hasattr(self, "anchor"):
            cfg.apply_project_theme(self)
            self.set_camera_orientation(phi=0, theta=-PI / 2)
            self.ground = deep_field()
            self.motes = mote_field()
            self.add(self.motes, self.ground)
            self.anchor = VGroup()
            self.add(self.anchor)
        self.local: list[Mobject] = []
        self.caption: Mobject | None = None

    def finish(self) -> None:
        """Clear the chapter's temporary material and hold the planned window."""
        self.clear_local()
        self.at(cfg.DURATIONS[self.key])
        if getattr(self.renderer, "check_lifetimes", False):
            family = set(self.anchor.get_family())
            leftovers = [
                type(mob).__name__
                for mob in self.mobjects
                if mob not in family
                and not getattr(mob, "_is_project_background", False)
                and any(isinstance(part, (VMobject, ImageMobject)) and part.has_points()
                        for part in mob.get_family())
            ]
            if leftovers:
                raise AssertionError(f"Scene {self.key} left visible roots outside anchor: {leftovers}")

    # -- Time ----------------------------------------------------------------

    def playq(self, *animations: Animation, seconds: float = 1, **kwargs) -> None:
        self.play(*animations, run_time=max(1 / config.frame_rate, seconds / cfg.SPEED), **kwargs)

    def hold(self, seconds: float) -> None:
        """Leave the diagram still while the viewer listens and reads."""
        self.wait(max(1 / config.frame_rate, seconds / cfg.SPEED))

    def at(self, seconds: float) -> None:
        """Hold to an explicit narration beat; fail if the choreography overruns."""
        remaining = seconds / cfg.SPEED - (self.time - self.chapter_start)
        if remaining < -2 / config.frame_rate and cfg.SPEED == 1:
            raise RuntimeError(f"Scene {self.key} overran beat {seconds}s by {-remaining:.2f}s")
        if remaining > 1 / config.frame_rate:
            self.wait(remaining)

    # -- Overlays pinned to the screen ---------------------------------------

    def pin(self, mob: Mobject) -> Mobject:
        """Keep a caption or formula facing the viewer while the camera moves."""
        self.add_fixed_in_frame_mobjects(mob)
        self.remove(mob)
        self.local.append(mob)
        return mob

    def show(self, mob: Mobject, seconds: float = 0.8) -> Mobject:
        """Fade in temporary material that belongs to this chapter only."""
        self._make_room_for(mob)
        self.local.append(mob)
        self.playq(FadeIn(mob), seconds=seconds)
        return mob

    def drop(self, *mobs: Mobject, seconds: float = 0.7) -> None:
        """Fade material out, and only then release its screen attachment.

        Releasing first would tilt the text into the 3D world for the length of
        the fade, which looks like a mistake rather than like a transition.
        """
        present = [mob for mob in mobs if mob is not None]
        if not present:
            return
        self.playq(*(FadeOut(mob) for mob in present), seconds=seconds)
        self.remove_fixed_in_frame_mobjects(*present)
        for mob in present:
            if mob in self.local:
                self.local.remove(mob)
            if mob is self.caption:
                self.caption = None

    def clear_local(self) -> None:
        visible = [
            mob for mob in self.local
            if mob in self.mobjects or any(part in self.mobjects for part in mob.get_family())
        ]
        if visible:
            self.drop(*visible)
        self.local = []

    def cue(self, label: str, color: str = cfg.GOLD, hold: float = 2.5, position=UP * 3.5) -> None:
        """A short caption: one line, held for a beat, then gone.

        The film has no permanent chapter strip and no narration duplicated as
        whole sentences on screen. A cue names the idea and leaves.
        """
        if self.caption is not None:
            self.drop(self.caption)
        mob = self.pin(outlined_text(label, cfg.FONT["label"], color).move_to(position))
        self.caption = mob
        self.playq(FadeIn(mob, shift=DOWN * 0.10), seconds=0.6)
        self.hold(hold)
        self.drop(mob, seconds=0.6)

    def formula(self, latex: str, position=UP * 3.3, size: int = 62, color: str = cfg.WHITE) -> Mobject:
        """Pin an equation to the screen and leave it for the chapter to drop."""
        mob = self.pin(equation(latex, size, color).move_to(position))
        self.playq(FadeIn(mob), seconds=0.8)
        return mob

    def headline(self, latex: str, position=ORIGIN, color: str = cfg.WHITE) -> Mobject:
        """The plated treatment, reserved for the film's three central equations."""
        card = self.pin(equation_card(latex, color).move_to(position))
        self.playq(FadeIn(card, scale=1.06), seconds=0.9)
        return card

    def spine(self, active: int, hold: float = 2.4, position=DOWN * 3.45) -> None:
        """Show where we are on ORBIT -> WAVE -> ... -> CHEMISTRY, then move on."""
        strip = self.pin(spine_strip(active).scale(0.94).move_to(position))
        self.playq(FadeIn(strip, shift=UP * 0.12), seconds=0.7)
        self.hold(hold)
        self.drop(strip, seconds=0.6)

    # -- The anchor ----------------------------------------------------------

    def _make_room_for(self, target: Mobject) -> None:
        """Lower the flat ground before anything depth-sorted arrives.

        Manim's 3D camera sorts depth-sorted mobjects by distance and then puts
        everything else in front of them. A flat background is everything else,
        so leaving it up would hide the orbital completely.
        """
        if getattr(target, "_needs_depth_sort", False):
            self.lower_ground(seconds=0.5)

    def morph(self, target: Mobject, seconds: float = 1.8) -> Mobject:
        """Carry the current diagram into the next one."""
        self._make_room_for(target)
        old = self.anchor
        if not old.submobjects and not old.has_points():
            self.playq(FadeIn(target), seconds=seconds)
        elif getattr(old, "visual_kind", None) == "orbit" and isinstance(target, VMobject):
            # Unwrap the actual track while the classical particle markers fade.
            self.playq(ReplacementTransform(old[1], target), FadeOut(old[0]), FadeOut(old[2]), seconds=seconds)
            self.remove(old)
        elif (isinstance(old, VMobject) and isinstance(target, VMobject)
              and not old.submobjects and not target.submobjects):
            self.playq(ReplacementTransform(old, target), seconds=seconds)
        else:
            # Aligning heterogeneous recursive groups multiplies hidden geometry
            # over a full-length render. A registered crossfade holds the visual
            # anchor without that growth.
            self.playq(FadeOut(old), FadeIn(target), seconds=seconds)
        self.anchor = target
        return target

    def dissolve(self, target: Mobject, seconds: float = 1.8) -> Mobject:
        """Crossfade when the two representations have nothing in common."""
        self._make_room_for(target)
        self.playq(FadeOut(self.anchor), FadeIn(target), seconds=seconds)
        self.anchor = target
        return target

    def adopt(self, *mobs: Mobject) -> None:
        """Move animated children under the anchor without leaving duplicate roots."""
        self.remove(*mobs)
        self.anchor.add(*mobs)
        self.add(self.anchor)

    # -- Camera --------------------------------------------------------------

    def view3d(self, phi: float = 68, theta: float = -50, seconds: float = 2) -> None:
        """Open the camera. The flat ground leaves first; the motes stay for depth."""
        self.lower_ground(seconds=min(seconds, 0.8))
        self.move_camera(phi=phi * DEGREES, theta=theta * DEGREES,
                         run_time=max(1 / config.frame_rate, seconds / cfg.SPEED))

    def flat(self, seconds: float = 1.5) -> None:
        """Return to the head-on view the 2D chapters assume, and restore the ground."""
        self.move_camera(phi=0, theta=-90 * DEGREES,
                         run_time=max(1 / config.frame_rate, seconds / cfg.SPEED))
        self.raise_ground(seconds=0.6)

    def turn(self, seconds: float = 8, angle: float = 0.6) -> None:
        """Hold a 3D beat by drifting the camera rather than by nudging the object.

        Scaling a mesh to keep a shot alive is expensive and it distorts the very
        thing being explained. The drift supplies the motion instead, and it
        alternates direction so a long chapter never walks all the way around.
        """
        sign = getattr(self, "_drift_sign", 1.0)
        self._drift_sign = -sign
        self.move_camera(
            theta=self.camera.get_theta() + angle * sign,
            run_time=max(1 / config.frame_rate, seconds / cfg.SPEED),
            rate_func=rate_functions.ease_in_out_sine,
        )

    def lower_ground(self, seconds: float = 0.8) -> None:
        """Detach the flat background: a z = 0 rectangle skews under a tilted camera."""
        ground = getattr(self, "ground", None)
        if ground is None or ground not in self.mobjects:
            return
        self.playq(FadeOut(ground), seconds=seconds)
        ground.suspend_updating()
        self.remove(ground)

    def raise_ground(self, seconds: float = 0.6) -> None:
        """Put the flat ground back, unless something depth-sorted still needs it down."""
        ground = getattr(self, "ground", None)
        if ground is None or ground in self.mobjects:
            return
        if any(getattr(mob, "_needs_depth_sort", False) for mob in self.mobjects):
            return
        ground.resume_updating()
        self.add(ground)
        self.bring_to_back(ground)
        # FadeIn restores each layer's own authored opacity; set_opacity(1)
        # would flatten the grid and the bubbles into a solid slab.
        self.playq(FadeIn(ground), seconds=seconds)

    # -- Convenience ---------------------------------------------------------

    def orbital(self, n: int = 1, l: int = 0, m: int = 0, **kwargs) -> VGroup:
        """A lit orbital surface that follows this scene's camera."""
        return orbital(self, n, l, m, **kwargs)
