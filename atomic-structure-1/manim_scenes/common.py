"""Shared visual language for the atomic-structure film.

Every recurring object on screen is built here exactly once: the nucleus, the
electron, the alpha particle, the cathode-ray tube, the gold-foil apparatus, the
prism, the spectrum, the energy ladder, and the MODEL / PREDICTION / EXPERIMENT
banner that carries the whole argument. A chapter composes these; it does not
redraw them.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable, Sequence

import numpy as np
from manim import *

import config as cfg
from utils.math_utils import wavelength_to_hex
from utils.render_helpers import fit_to_safe_frame, fit_to_width


# ---------------------------------------------------------------------------
# Chapter scaffolding
# ---------------------------------------------------------------------------


def begin_scene(scene: Scene, scene_key: str) -> float:
    """Apply the theme and remember when this chapter started."""
    cfg.apply_project_theme(scene, bubbles=False)
    scene._project_scene_key = scene_key
    return float(scene.time)


def paced_play(scene: Scene, *animations: Animation, **kwargs) -> None:
    kwargs["run_time"] = kwargs.get("run_time", 1.0)
    scene.play(*animations, **kwargs)


def narration_wait(scene: Scene, seconds: float = 1.0) -> None:
    """Leave diagrams and captions still while the viewer listens and reads."""
    if seconds > 0:
        scene.wait(seconds)


def end_scene(
    scene: Scene,
    started_at: float,
    target_seconds: float,
    *,
    fade_background: bool = False,
) -> None:
    """Clear the chapter, padding or warning so the narration window is honoured."""
    reset_flat_camera(scene)
    transition = cfg.TIMING["transition"]
    elapsed = float(scene.time) - started_at
    remaining = target_seconds - elapsed - transition
    key = getattr(scene, "_project_scene_key", "unknown")
    if remaining >= 1.0 / scene.camera.frame_rate:
        narration_wait(scene, remaining)
    elif remaining < -0.1:
        warnings.warn(f"Scene {key} overruns its narration target by {-remaining:.2f}s.", stacklevel=2)
    visible = [
        mob
        for mob in scene.mobjects
        if fade_background or not getattr(mob, "_is_project_background", False)
    ]
    if visible:
        scene.play(FadeOut(*visible), run_time=transition)
        scene.remove(*visible)


# ---------------------------------------------------------------------------
# 3D camera helpers
#
# The complete film renders as one ThreeDScene so the dimensional chapters can
# open the camera mid-story. Every helper degrades to a no-op under a flat
# camera, which keeps the individual 2D scene classes and the audits working.
# ---------------------------------------------------------------------------


def has_3d_camera(scene: Scene) -> bool:
    return isinstance(getattr(scene, "camera", None), ThreeDCamera)


def set_3d_view(scene: Scene, phi: float, theta: float, zoom: float = 1.0) -> None:
    if has_3d_camera(scene):
        scene.set_camera_orientation(phi=phi, theta=theta, zoom=zoom)


def move_3d_view(scene: Scene, phi: float, theta: float, run_time: float = 2.0, **kwargs) -> None:
    """Glide to a viewpoint, or simply hold the beat under a flat camera."""
    if has_3d_camera(scene):
        scene.move_camera(phi=phi, theta=theta, run_time=run_time, **kwargs)
    else:
        scene.wait(run_time)


def reset_flat_camera(scene: Scene) -> None:
    """Return to the head-on orientation the 2D chapters assume."""
    if has_3d_camera(scene):
        scene.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        scene.stop_ambient_camera_rotation()


def orbit_hold(scene: Scene, seconds: float, rate: float = 0.045) -> None:
    """Hold a 3D beat by drifting the camera instead of nudging the geometry.

    Scaling a Sphere or a Surface to keep a frame alive is expensive and it
    distorts the very object being explained. The drift supplies the motion
    instead, and it alternates direction so a long chapter never walks the
    camera all the way around its subject.
    """
    if not has_3d_camera(scene):
        narration_wait(scene, seconds)
        return
    sign = getattr(scene, "_orbit_drift_sign", 1.0)
    scene._orbit_drift_sign = -sign
    scene.move_camera(
        theta=scene.camera.get_theta() + rate * seconds * sign,
        run_time=seconds,
        rate_func=rate_functions.ease_in_out_sine,
    )


def pin_to_frame(scene: Scene, *mobjects: Mobject) -> None:
    """Keep captions and formulas facing the viewer while the 3D camera moves."""
    if has_3d_camera(scene):
        scene.add_fixed_in_frame_mobjects(*mobjects)
    else:
        scene.add(*mobjects)


def unpin_from_frame(scene: Scene, *mobjects: Mobject) -> None:
    """Release frame-pinned overlays so they can be faded out normally."""
    if has_3d_camera(scene):
        for mobject in mobjects:
            if mobject in scene.camera.fixed_in_frame_mobjects:
                scene.remove_fixed_in_frame_mobjects(mobject)


# ---------------------------------------------------------------------------
# Background and typography
# ---------------------------------------------------------------------------


def oceanic_bubbles_layer() -> VGroup:
    from themes.oceanic_next import oceanic_bubbles

    return oceanic_bubbles()


def cinematic_background(show_bubbles: bool = True) -> VGroup:
    """The Oceanic ground: a faint grid under an extremely slow bubble drift."""
    base = Rectangle(width=16.4, height=9.3, fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    grid = VGroup()
    for x in np.linspace(-8, 8, 17):
        grid.add(Line([x, -4.65, 0], [x, 4.65, 0], color="#173653", stroke_width=0.65, stroke_opacity=0.16))
    for y in np.linspace(-4.5, 4.5, 10):
        grid.add(Line([-8.2, y, 0], [8.2, y, 0], color="#173653", stroke_width=0.65, stroke_opacity=0.11))
    layers = VGroup(base, grid)
    if show_bubbles:
        bubbles = oceanic_bubbles_layer()
        for index, bubble in enumerate(bubbles):
            speed = 0.018 + 0.003 * (index % 5)

            def drift(mob: Mobject, dt: float, velocity: float = speed) -> None:
                mob.shift(UP * velocity * dt)
                if mob.get_bottom()[1] > 4.65:
                    mob.shift(DOWN * 9.3)

            bubble.add_updater(drift)
        layers.add(bubbles)
    layers._is_project_background = True
    return layers


def add_cinematic_background(scene: Scene, show_bubbles: bool = True) -> VGroup:
    """Reuse one living background when many chapters share a single Scene."""
    for mob in scene.mobjects:
        if getattr(mob, "_is_project_background", False):
            return mob
    background = cinematic_background(show_bubbles)
    scene.add(background)
    return background


def dark_room_background() -> VGroup:
    """A near-black ground for the chapters about not being able to see."""
    base = Rectangle(width=16.4, height=9.3, fill_color="#01080F", fill_opacity=1, stroke_width=0)
    vignette = VGroup()
    for index, (radius, opacity) in enumerate(((7.6, 0.05), (6.2, 0.05), (5.0, 0.05))):
        vignette.add(Circle(radius=radius, color="#000000", stroke_width=0, fill_color="#000000", fill_opacity=opacity))
    layers = VGroup(base, vignette)
    layers._is_project_background = True
    return layers


def hide_background(scene: Scene) -> VGroup | None:
    """Detach the flat background before a 3D beat, returning it for later reuse."""
    for mob in list(scene.mobjects):
        if getattr(mob, "_is_project_background", False):
            mob.suspend_updating()
            scene.remove(mob)
            return mob
    return None


def restore_background(scene: Scene, background: VGroup | None) -> None:
    """Return to the flat viewpoint, then put the shared background back.

    The background is a flat rectangle in the z = 0 plane, so adding it while
    the camera is still tilted renders it skewed across the frame. Resetting
    the camera here keeps the two steps from ever being separated.
    """
    reset_flat_camera(scene)
    if background is None:
        return
    background.resume_updating()
    scene.add(background)


def fit_width(mobject: Mobject, limit: float | None = None) -> Mobject:
    """Hold a mobject to the safe frame's width, or to a tighter limit."""
    return fit_to_width(mobject, cfg.SAFE_WIDTH if limit is None else limit)


def fit_safe(mobject: Mobject, padding: float = 0.25) -> Mobject:
    """Hold a mobject inside the safe frame in both directions."""
    return fit_to_safe_frame(mobject, padding)


def outlined_text(text: str, font_size: int, color: str = cfg.WHITE, weight=BOLD) -> Text:
    result = Text(text, font_size=font_size, color=color, weight=weight)
    result.set_stroke(cfg.BG, width=4, opacity=0.95, background=True)
    return result


def title_card(title: str, subtitle: str | None = None, color: str = cfg.GOLD) -> VGroup:
    """The film's hero title: a glowing shadow under a rule-and-subtitle stack."""
    heading = fit_width(outlined_text(title, cfg.FONT["title"], color, BOLD))
    shadow = heading.copy().set_color(color).set_opacity(0.18).set_stroke(width=0, background=True)
    shadow.shift(DOWN * 0.06 + RIGHT * 0.06).scale(1.02)
    # A drop shadow belongs under its own glyphs, so the layout audit skips it
    # rather than reporting the deliberate overlap as a collision.
    for glyph in shadow.get_family():
        glyph._is_decorative_shadow = True
    stacked = VGroup(shadow, heading)
    rule = Line(
        LEFT * min(heading.width * 0.48, 5.7),
        RIGHT * min(heading.width * 0.48, 5.7),
        color=cfg.CYAN,
        stroke_width=4,
    )
    group = VGroup(stacked, rule).arrange(DOWN, buff=0.22)
    if subtitle:
        sub = fit_width(outlined_text(subtitle, cfg.FONT["body"], cfg.WHITE), cfg.SAFE_WIDTH - 0.5)
        group.add(sub)
        group.arrange(DOWN, buff=0.22)
    return group


def eq(
    latex: str,
    color: str = cfg.WHITE,
    font_size: int | None = None,
    *,
    substrings_to_isolate: Sequence[str] | None = None,
) -> MathTex:
    result = MathTex(
        latex,
        color=color,
        font_size=font_size or cfg.FONT["section"],
        substrings_to_isolate=list(substrings_to_isolate or ()),
    )
    result.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    return result


def equation_card(latex: str, color: str = cfg.WHITE, font_size: int | None = None) -> VGroup:
    """A large formula on its own lit plate, for the two equations that matter."""
    formula = eq(latex, color, font_size or cfg.FONT["title"])
    box = RoundedRectangle(
        width=formula.width + 1.0,
        height=formula.height + 0.62,
        corner_radius=0.18,
        stroke_color=color,
        stroke_opacity=0.6,
        fill_color=cfg.PANEL,
        fill_opacity=0.9,
    )
    halo = box.copy().set_stroke(color, width=14, opacity=0.08)
    return VGroup(halo, box, formula)


def live_readout(
    label: str,
    value: Callable[[], float],
    color: str = cfg.WHITE,
    font_size: int | None = None,
    decimal_places: int = 1,
    suffix: str | None = None,
) -> VGroup:
    """A static LaTeX label beside a number that updates every frame.

    Rebuilding a MathTex from an f-string inside `always_redraw` forces a fresh
    LaTeX compile for every distinct value it displays, which quietly dominates
    render time for a counter that sweeps a range. A DecimalNumber reuses cached
    digit glyphs, so only the label is ever compiled. The number re-anchors to
    the label each frame, so the readout stays put as its digit count changes.
    """
    size = font_size or cfg.FONT["small"]
    tag = eq(label, color, size)
    number = DecimalNumber(value(), num_decimal_places=decimal_places, color=color, font_size=size)
    number.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    tail = eq(suffix, color, size) if suffix else None

    parts = [tag, number] + ([tail] if tail else [])
    group = VGroup(*parts).arrange(RIGHT, buff=0.18)

    def refresh(mob: Mobject) -> None:
        mob.set_value(value())
        mob.next_to(tag, RIGHT, buff=0.18)
        if tail is not None:
            tail.next_to(mob, RIGHT, buff=0.12)

    number.add_updater(refresh)
    return group


def bottom_caption(text: str, color: str = cfg.GOLD) -> Text:
    caption = fit_width(outlined_text(text, cfg.FONT["body"], color, BOLD), cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(DOWN, buff=0.30)


def top_caption(text: str, color: str = cfg.CYAN) -> Text:
    caption = fit_width(outlined_text(text, cfg.FONT["body"], color, BOLD), cfg.SAFE_WIDTH - 0.5)
    return caption.to_edge(UP, buff=0.32)


def chip(text: str, color: str = cfg.CYAN, font_size: int | None = None) -> VGroup:
    """A small labelled plate, used for the film's concept chains."""
    label = outlined_text(text, font_size or cfg.FONT["tiny"], color, BOLD)
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


# ---------------------------------------------------------------------------
# Glow primitives
# ---------------------------------------------------------------------------


def glow_dot(point: Sequence[float], color: str = cfg.GOLD, radius: float = 0.09) -> VGroup:
    layers = VGroup()
    for size, opacity in ((0.26, 0.05), (0.19, 0.09), (0.14, 0.15)):
        layers.add(Circle(radius=size, color=color, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(point))
    layers.add(Dot(point, radius=radius, color=color))
    return layers


def glow_line(start: Sequence[float], end: Sequence[float], color: str, width: float = 5) -> VGroup:
    return VGroup(
        Line(start, end, color=color, stroke_width=width * 3.2, stroke_opacity=0.1),
        Line(start, end, color=color, stroke_width=width),
    )


def halo(radius: float, color: str, layers: int = 4, peak_opacity: float = 0.16) -> VGroup:
    """Concentric soft rings, the film's standard way of making something glow."""
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


def dashed_connector(
    start: Sequence[float],
    end: Sequence[float],
    color: str = cfg.MUTED,
    dashes: int = 12,
    stroke_width: float = 2.6,
) -> VGroup:
    """A dashed guide assembled from separate segments, safe to fade out."""
    start_point = np.array(start, dtype=float)
    end_point = np.array(end, dtype=float)
    group = VGroup()
    for index in range(dashes):
        a = index / dashes
        b = (index + 0.55) / dashes
        group.add(
            Line(
                start_point + (end_point - start_point) * a,
                start_point + (end_point - start_point) * b,
                color=color,
                stroke_width=stroke_width,
            )
        )
    return group


def polyline(points: np.ndarray, color: str, stroke_width: float = 4.0, smooth: bool = True) -> VMobject:
    """Turn an (N, 2) array of model output into a drawable curve."""
    path = VMobject(color=color, stroke_width=stroke_width)
    coordinates = [np.array([float(x), float(y), 0.0]) for x, y in points]
    if len(coordinates) < 2:
        coordinates = coordinates * 2
    if smooth:
        path.set_points_smoothly(coordinates)
    else:
        path.set_points_as_corners(coordinates)
    return path


# ---------------------------------------------------------------------------
# The cast: nucleus, electron, alpha particle
# ---------------------------------------------------------------------------


def _minus_glyph(size: float, color: str = cfg.BG) -> Line:
    return Line(LEFT * size, RIGHT * size, color=color, stroke_width=max(2.0, size * 22))


def _plus_glyph(size: float, color: str = cfg.BG) -> VGroup:
    width = max(2.0, size * 22)
    return VGroup(
        Line(LEFT * size, RIGHT * size, color=color, stroke_width=width),
        Line(DOWN * size, UP * size, color=color, stroke_width=width),
    )


def electron(radius: float = 0.16, color: str = cfg.ELECTRON_COLOR, sign: bool = True) -> VGroup:
    """The film's electron: a cool glowing bead carrying a minus sign."""
    body = Dot(ORIGIN, radius=radius, color=color)
    body.set_stroke(cfg.WHITE, width=1.6, opacity=0.65)
    group = VGroup(halo(radius, color, layers=3, peak_opacity=0.22), body)
    if sign and radius >= 0.12:
        group.add(_minus_glyph(radius * 0.48))
    return group


def nucleus(radius: float = 0.34, color: str = cfg.NUCLEUS_COLOR, nucleons: bool = True) -> VGroup:
    """A dense, hot core: a glow, a shell, and a suggestion of packed nucleons."""
    group = VGroup(halo(radius, color, layers=4, peak_opacity=0.20))
    shell = Circle(
        radius=radius,
        color=color,
        stroke_width=3.0,
        fill_color=color,
        fill_opacity=0.92,
    )
    group.add(shell)
    if nucleons and radius >= 0.22:
        packing = VGroup()
        angles = np.linspace(0, TAU, 7, endpoint=False)
        for index, angle in enumerate(angles):
            offset = radius * 0.44 * np.array([np.cos(angle), np.sin(angle), 0.0])
            tone = cfg.PROTON_COLOR if index % 2 == 0 else "#FFB4A2"
            packing.add(Dot(offset, radius=radius * 0.26, color=tone).set_opacity(0.85))
        packing.add(Dot(ORIGIN, radius=radius * 0.26, color=cfg.PROTON_COLOR).set_opacity(0.9))
        group.add(packing)
    highlight = Arc(
        radius=radius * 0.72,
        start_angle=40 * DEGREES,
        angle=95 * DEGREES,
        color=cfg.WHITE,
        stroke_width=3,
        stroke_opacity=0.42,
    )
    group.add(highlight)
    return group


def alpha_particle(radius: float = 0.13, color: str = cfg.ALPHA_COLOR) -> VGroup:
    """A helium nucleus as a projectile: gold, fast, doubly positive."""
    body = Dot(ORIGIN, radius=radius, color=color)
    body.set_stroke(cfg.WHITE, width=1.4, opacity=0.6)
    return VGroup(halo(radius, color, layers=3, peak_opacity=0.18), body)


def orbit_ring(radius: float, color: str = cfg.MUTED, stroke_width: float = 2.6, opacity: float = 0.55) -> Circle:
    return Circle(radius=radius, color=color, stroke_width=stroke_width, stroke_opacity=opacity, fill_opacity=0)


def planetary_atom(
    orbit_radius: float = 2.3,
    nucleus_radius: float = 0.36,
    electron_radius: float = 0.17,
    start_angle: float = 0.0,
) -> tuple[VGroup, VGroup, Circle, VGroup]:
    """The familiar textbook atom, returned in pieces so a chapter can break it.

    Handing back the core, the ring, and the electron separately is what lets
    the opening chapter shrink the orbit while the nucleus holds still.
    """
    core = nucleus(nucleus_radius)
    ring = orbit_ring(orbit_radius, cfg.MUTED)
    bead = electron(electron_radius)
    bead.move_to(orbit_radius * np.array([np.cos(start_angle), np.sin(start_angle), 0.0]))
    return VGroup(core, ring, bead), core, ring, bead


def dalton_sphere(radius: float = 1.5, color: str = cfg.CYAN) -> VGroup:
    """One indivisible ball: featureless on purpose, because that was the claim."""
    body = Circle(radius=radius, color=color, stroke_width=5, fill_color=color, fill_opacity=0.35)
    shade = Circle(radius=radius * 0.92, color=cfg.BG, stroke_width=0, fill_color="#062B45", fill_opacity=0.35)
    shade.shift(RIGHT * radius * 0.14 + DOWN * radius * 0.14)
    gloss = Arc(
        radius=radius * 0.7,
        start_angle=55 * DEGREES,
        angle=80 * DEGREES,
        color=cfg.WHITE,
        stroke_width=6,
        stroke_opacity=0.30,
    )
    return VGroup(halo(radius, color, layers=3, peak_opacity=0.08), body, shade, gloss)


def thomson_atom(
    radius: float = 1.7,
    electron_count: int = 7,
    seed: int = cfg.SEED,
    electron_radius: float = 0.14,
) -> tuple[VGroup, VGroup]:
    """A diffuse positive cloud with negative beads embedded in it.

    The film calls this a positive cloud rather than a pudding, because the
    point is that the positive charge is *spread out* -- which is precisely the
    property the gold-foil experiment goes on to destroy.
    """
    rng = np.random.default_rng(seed)
    cloud = VGroup()
    for index in range(6):
        fraction = index / 6
        cloud.add(
            Circle(
                radius=radius * (1.0 - 0.14 * index),
                color=cfg.POSITIVE_CLOUD,
                stroke_width=0,
                fill_color=cfg.POSITIVE_CLOUD,
                fill_opacity=0.055 + 0.03 * fraction,
            )
        )
    rim = Circle(radius=radius, color=cfg.POSITIVE_CLOUD, stroke_width=3.2, stroke_opacity=0.75, fill_opacity=0)
    cloud.add(rim)

    beads = VGroup()
    for _ in range(electron_count):
        # Uniform over the disc: sqrt keeps the beads from clumping at the centre.
        r = radius * 0.78 * float(np.sqrt(rng.uniform(0.02, 1.0)))
        angle = float(rng.uniform(0, TAU))
        beads.add(electron(electron_radius).move_to([r * np.cos(angle), r * np.sin(angle), 0.0]))
    return VGroup(cloud, beads), beads


def rutherford_atom(
    atom_radius: float = 2.4,
    nucleus_radius: float = 0.20,
    electron_count: int = 5,
    seed: int = cfg.SEED,
) -> tuple[VGroup, VGroup, VGroup]:
    """A pin-prick of positive charge, an empty interior, electrons far outside."""
    rng = np.random.default_rng(seed)
    boundary = DashedVMobject(
        Circle(radius=atom_radius, color=cfg.MUTED, stroke_width=2.4, stroke_opacity=0.45),
        num_dashes=54,
    )
    core = nucleus(nucleus_radius, cfg.NUCLEUS_COLOR, nucleons=False)
    beads = VGroup()
    for index in range(electron_count):
        angle = TAU * index / electron_count + float(rng.uniform(-0.25, 0.25))
        r = atom_radius * float(rng.uniform(0.62, 0.93))
        beads.add(electron(0.13).move_to([r * np.cos(angle), r * np.sin(angle), 0.0]))
    return VGroup(boundary, core, beads), core, beads


# ---------------------------------------------------------------------------
# Apparatus
# ---------------------------------------------------------------------------


def cathode_ray_tube(
    width: float = 9.4,
    height: float = 3.0,
    center: Sequence[float] | None = None,
) -> dict[str, VGroup]:
    """The discharge tube, built as named parts so a chapter can assemble it.

    Returned as a dictionary rather than one group because the chapter's whole
    method is to add the tube, then the electrodes, then the voltage, then the
    screen, one narrated step at a time.

    Some parts appear under two keys -- `cathode_plate` is also inside `cathode`
    -- so a caller must never reposition this by iterating the values: the shared
    mobjects would move once per key they appear under. Pass `center` instead and
    the whole apparatus is built where it belongs.
    """
    glass = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.55,
        color=cfg.CYAN,
        stroke_width=4,
        stroke_opacity=0.75,
        fill_color="#062033",
        fill_opacity=0.55,
    )
    inner_sheen = RoundedRectangle(
        width=width - 0.28,
        height=height - 0.28,
        corner_radius=0.45,
        color=cfg.WHITE,
        stroke_width=1.6,
        stroke_opacity=0.16,
        fill_opacity=0,
    )
    # Tucked into the top-left of the tube: the middle of the ceiling is where
    # the anode's lead-out wire and, later, the deflecting plates both live.
    vacuum_label = outlined_text("NEARLY EMPTY", cfg.FONT["tiny"], cfg.MUTED)
    vacuum_label.move_to(glass.get_top() + DOWN * 0.44 + LEFT * width * 0.255)

    cathode_plate = RoundedRectangle(
        width=0.30,
        height=1.25,
        corner_radius=0.07,
        color=cfg.BLUE,
        stroke_width=3,
        fill_color=cfg.BLUE,
        fill_opacity=0.75,
    ).move_to(glass.get_left() + RIGHT * 0.86)
    cathode_stem = Line(cathode_plate.get_left(), glass.get_left() + LEFT * 0.55, color=cfg.GRAY, stroke_width=6)
    cathode = VGroup(cathode_stem, cathode_plate)

    anode_plate = RoundedRectangle(
        width=0.30,
        height=1.25,
        corner_radius=0.07,
        color=cfg.ORANGE,
        stroke_width=3,
        fill_color=cfg.ORANGE,
        fill_opacity=0.75,
    ).move_to(glass.get_left() + RIGHT * 3.05)
    anode_slit = Rectangle(width=0.34, height=0.24, color=cfg.BG, fill_color=cfg.BG, fill_opacity=1, stroke_width=0)
    anode_slit.move_to(anode_plate.get_center())
    anode_stem = Line(anode_plate.get_top(), anode_plate.get_top() + UP * 0.9, color=cfg.GRAY, stroke_width=6)
    anode = VGroup(anode_stem, anode_plate, anode_slit)

    screen = Rectangle(
        width=0.22,
        height=height - 0.55,
        color=cfg.GREEN,
        stroke_width=3,
        fill_color=cfg.GREEN,
        fill_opacity=0.16,
    ).move_to(glass.get_right() + LEFT * 0.42)

    # The two electrode names are wider than the gap between the electrodes, so
    # the anode's label rides above the tube beside its own lead-out wire.
    cathode_label = outlined_text("CATHODE  –", cfg.FONT["tiny"], cfg.BLUE).next_to(cathode_plate, DOWN, buff=0.34)
    anode_label = outlined_text("ANODE  +", cfg.FONT["tiny"], cfg.ORANGE).next_to(anode_stem, UP, buff=0.18)
    screen_label = outlined_text("SCREEN", cfg.FONT["tiny"], cfg.GREEN).next_to(screen, DOWN, buff=0.30)

    if center is not None:
        offset = np.array(center, dtype=float)
        # Shift each distinct piece exactly once, whatever the dictionary shares.
        for piece in (
            glass, inner_sheen, vacuum_label,
            cathode_stem, cathode_plate, anode_stem, anode_plate, anode_slit,
            screen, cathode_label, anode_label, screen_label,
        ):
            piece.shift(offset)

    return {
        "glass": VGroup(glass, inner_sheen),
        "vacuum_label": vacuum_label,
        "cathode": cathode,
        "cathode_plate": cathode_plate,
        "anode": anode,
        "anode_plate": anode_plate,
        "screen": screen,
        "cathode_label": cathode_label,
        "anode_label": anode_label,
        "screen_label": screen_label,
    }


def deflecting_plates(
    center_x: float,
    gap: float = 1.9,
    length: float = 2.4,
    top_color: str = cfg.ORANGE,
    bottom_color: str = cfg.BLUE,
) -> tuple[VGroup, VGroup, VGroup]:
    """A parallel-plate pair with signs, for bending the beam."""
    top = RoundedRectangle(
        width=length, height=0.22, corner_radius=0.07, color=top_color,
        stroke_width=3, fill_color=top_color, fill_opacity=0.8,
    ).move_to([center_x, gap / 2, 0])
    bottom = RoundedRectangle(
        width=length, height=0.22, corner_radius=0.07, color=bottom_color,
        stroke_width=3, fill_color=bottom_color, fill_opacity=0.8,
    ).move_to([center_x, -gap / 2, 0])
    plus = _plus_glyph(0.17, top_color).next_to(top, UP, buff=0.16)
    minus = _minus_glyph(0.17, bottom_color).next_to(bottom, DOWN, buff=0.16)
    field = VGroup()
    for offset in np.linspace(-length * 0.36, length * 0.36, 5):
        field.add(
            Arrow(
                [center_x + offset, gap / 2 - 0.22, 0],
                [center_x + offset, -gap / 2 + 0.22, 0],
                color=cfg.MUTED,
                stroke_width=2.6,
                buff=0,
                max_tip_length_to_length_ratio=0.10,
            ).set_opacity(0.45)
        )
    return VGroup(top, bottom), VGroup(plus, minus), field


def gold_foil_apparatus(detector_radius: float = 3.35) -> dict[str, VGroup]:
    """Source, collimator, foil, and the fluorescent ring that surrounds them."""
    housing = VGroup(
        RoundedRectangle(width=1.25, height=1.05, corner_radius=0.14, color=cfg.GRAY,
                         stroke_width=3.4, fill_color="#0B1D2B", fill_opacity=1),
        Dot(ORIGIN, radius=0.14, color=cfg.RED),
    )
    housing.move_to([-6.1, 0, 0])
    housing.add(halo(0.30, cfg.RED, layers=3, peak_opacity=0.14).move_to(housing[1].get_center()))

    # The aperture has to be wider than the spread of lanes the chapter fires
    # through it, or the beam appears to come from inside solid lead.
    collimator = VGroup(
        Rectangle(width=0.30, height=1.55, color=cfg.GRAY, stroke_width=2.6,
                  fill_color=cfg.GRAY, fill_opacity=0.85).move_to([-4.85, 3.32, 0]),
        Rectangle(width=0.30, height=1.55, color=cfg.GRAY, stroke_width=2.6,
                  fill_color=cfg.GRAY, fill_opacity=0.85).move_to([-4.85, -3.32, 0]),
    )

    foil = VGroup(
        Rectangle(width=0.16, height=4.5, color=cfg.GOLD, stroke_width=2.6,
                  fill_color=cfg.GOLD, fill_opacity=0.42),
        Rectangle(width=0.05, height=4.5, color=cfg.WHITE, stroke_width=0,
                  fill_color=cfg.WHITE, fill_opacity=0.18),
    )

    detector = VGroup(
        Circle(radius=detector_radius, color=cfg.GREEN, stroke_width=6, stroke_opacity=0.30, fill_opacity=0),
        DashedVMobject(
            Circle(radius=detector_radius, color=cfg.GREEN, stroke_width=3.2, stroke_opacity=0.60),
            num_dashes=88,
        ),
    )

    source_label = outlined_text("ALPHA SOURCE", cfg.FONT["tiny"], cfg.RED).next_to(housing, DOWN, buff=0.34)
    # Above the detector ring, not above the foil: the space above the foil is
    # where the scintillations land, and a flash on top of a caption reads badly.
    foil_label = outlined_text("GOLD FOIL", cfg.FONT["tiny"], cfg.GOLD)
    foil_label.move_to([0, detector_radius + 0.55, 0])
    detector_label = outlined_text("FLUORESCENT SCREEN", cfg.FONT["tiny"], cfg.GREEN)
    detector_label.move_to([0, -detector_radius - 0.52, 0])

    return {
        "source": housing,
        "collimator": collimator,
        "foil": foil,
        "detector": detector,
        "source_label": source_label,
        "foil_label": foil_label,
        "detector_label": detector_label,
    }


def prism(size: float = 1.9, color: str = cfg.CYAN) -> VGroup:
    """A glass triangle with an inner glint, for the chapters about light."""
    height = size * np.sqrt(3) / 2
    body = Polygon(
        [0, height * 2 / 3, 0],
        [-size / 2, -height / 3, 0],
        [size / 2, -height / 3, 0],
        color=color,
        stroke_width=4,
        fill_color="#0B3A57",
        fill_opacity=0.6,
    )
    glint = Line(
        [-size * 0.20, -height * 0.16, 0],
        [size * 0.04, height * 0.40, 0],
        color=cfg.WHITE,
        stroke_width=4,
        stroke_opacity=0.35,
    )
    return VGroup(halo(size * 0.6, color, layers=3, peak_opacity=0.06), body, glint)


def discharge_tube(width: float = 3.4, height: float = 0.85, glow_color: str = cfg.PURPLE) -> VGroup:
    """A narrow gas tube, glowing the way an excited element actually does."""
    body = RoundedRectangle(
        width=width, height=height, corner_radius=height / 2,
        color=cfg.CYAN, stroke_width=3.4, stroke_opacity=0.8,
        fill_color=glow_color, fill_opacity=0.55,
    )
    inner = RoundedRectangle(
        width=width - 0.26, height=height - 0.26, corner_radius=(height - 0.26) / 2,
        color=cfg.WHITE, stroke_width=0, fill_color=cfg.WHITE, fill_opacity=0.16,
    )
    caps = VGroup(
        Rectangle(width=0.18, height=height * 0.72, color=cfg.GRAY, stroke_width=2,
                  fill_color=cfg.GRAY, fill_opacity=0.9).move_to(body.get_left() + RIGHT * 0.16),
        Rectangle(width=0.18, height=height * 0.72, color=cfg.GRAY, stroke_width=2,
                  fill_color=cfg.GRAY, fill_opacity=0.9).move_to(body.get_right() + LEFT * 0.16),
    )
    glow = VGroup()
    for scale, opacity in ((1.5, 0.05), (1.28, 0.08), (1.12, 0.12)):
        glow.add(
            RoundedRectangle(
                width=width * scale, height=height * scale, corner_radius=height * scale / 2,
                color=glow_color, stroke_width=0, fill_color=glow_color, fill_opacity=opacity,
            )
        )
    return VGroup(glow, body, inner, caps)


# ---------------------------------------------------------------------------
# Light: waves, spectra, and the barcode
# ---------------------------------------------------------------------------


def sine_wave(
    start: Sequence[float],
    end: Sequence[float],
    wavelength: float = 0.9,
    amplitude: float = 0.34,
    color: str = cfg.CYAN,
    stroke_width: float = 4.5,
    samples: int = 400,
) -> VMobject:
    """A travelling wave drawn between two points, at a stated wavelength."""
    start_point = np.array(start, dtype=float)
    end_point = np.array(end, dtype=float)
    axis = end_point - start_point
    length = float(np.linalg.norm(axis))
    if length < 1e-6:
        return VMobject(color=color, stroke_width=stroke_width)
    unit = axis / length
    normal = np.array([-unit[1], unit[0], 0.0])
    points = []
    for t in np.linspace(0.0, length, samples):
        phase = TAU * t / max(wavelength, 1e-3)
        points.append(start_point + unit * t + normal * amplitude * np.sin(phase))
    wave = VMobject(color=color, stroke_width=stroke_width)
    wave.set_points_smoothly(points)
    return wave


def photon(
    start: Sequence[float],
    end: Sequence[float],
    wavelength: float = 0.55,
    color: str = cfg.PHOTON_COLOR,
    amplitude: float = 0.24,
) -> VGroup:
    """A short wave packet: the film's picture of one quantum of light."""
    wave = sine_wave(start, end, wavelength, amplitude, color, stroke_width=5.0, samples=260)
    return VGroup(wave.copy().set_stroke(color, width=16, opacity=0.12), wave)


def wavelength_marks(wave_start: Sequence[float], wavelength: float, color: str = cfg.GOLD) -> VGroup:
    """A labelled bracket spanning exactly one wavelength."""
    start = np.array(wave_start, dtype=float)
    end = start + RIGHT * wavelength
    bracket = VGroup(
        Line(start + UP * 0.06, start + UP * 0.52, color=color, stroke_width=3),
        Line(end + UP * 0.06, end + UP * 0.52, color=color, stroke_width=3),
        DoubleArrow(start + UP * 0.40, end + UP * 0.40, color=color, stroke_width=3,
                    buff=0, max_tip_length_to_length_ratio=0.13),
    )
    label = eq(r"\lambda", color, cfg.FONT["body"]).next_to(bracket, UP, buff=0.12)
    return VGroup(bracket, label)


def continuous_spectrum(
    width: float = 10.4,
    height: float = 1.25,
    low_nm: float = 380.0,
    high_nm: float = 720.0,
    slices: int = 260,
) -> VGroup:
    """An unbroken rainbow: every colour present, which is what a hot solid gives."""
    band = VGroup()
    slice_width = width / slices
    for index in range(slices):
        fraction = (index + 0.5) / slices
        nm = low_nm + (high_nm - low_nm) * fraction
        band.add(
            Rectangle(
                width=slice_width * 1.04,
                height=height,
                stroke_width=0,
                fill_color=wavelength_to_hex(nm),
                fill_opacity=1,
            ).move_to([(fraction - 0.5) * width, 0, 0])
        )
    frame = Rectangle(width=width, height=height, color=cfg.WHITE, stroke_width=2.4, stroke_opacity=0.55, fill_opacity=0)
    return VGroup(band, frame)


def spectrum_frame(width: float = 10.4, height: float = 1.25, fill: str = "#03101B") -> VGroup:
    """The dark plate a line spectrum is drawn on."""
    plate = Rectangle(width=width, height=height, color=cfg.WHITE, stroke_width=2.4,
                      stroke_opacity=0.55, fill_color=fill, fill_opacity=1)
    return VGroup(plate)


def spectral_line(
    wavelength_nm: float,
    width: float = 10.4,
    height: float = 1.25,
    low_nm: float = 380.0,
    high_nm: float = 720.0,
    thickness: float = 0.10,
) -> VGroup:
    """One sharp emission line, placed and coloured by its own wavelength."""
    fraction = (wavelength_nm - low_nm) / (high_nm - low_nm)
    x = (fraction - 0.5) * width
    color = wavelength_to_hex(wavelength_nm)
    core = Rectangle(width=thickness, height=height * 0.92, stroke_width=0, fill_color=color, fill_opacity=1)
    bloom = Rectangle(width=thickness * 4.2, height=height * 0.92, stroke_width=0, fill_color=color, fill_opacity=0.22)
    line = VGroup(bloom, core).move_to([x, 0, 0])
    line._spectral_x = x
    line._spectral_color = color
    return line


def line_spectrum(
    wavelengths: Sequence[float],
    width: float = 10.4,
    height: float = 1.25,
    low_nm: float = 380.0,
    high_nm: float = 720.0,
) -> tuple[VGroup, VGroup]:
    """A dark plate plus its handful of bright lines, returned separately."""
    plate = spectrum_frame(width, height)
    lines = VGroup(*[spectral_line(w, width, height, low_nm, high_nm) for w in wavelengths])
    return plate, lines


def wavelength_axis(
    width: float = 10.4,
    low_nm: float = 380.0,
    high_nm: float = 720.0,
    ticks: Sequence[float] = (400, 500, 600, 700),
    color: str = cfg.MUTED,
    center: Sequence[float] | None = None,
) -> VGroup:
    """A nanometre scale under a spectrum, so a line can be read off it.

    Pass `center` to place it. The trailing "nm" hangs off the right-hand end, so
    the group is wider than the scale itself and `next_to` would centre the unit
    label rather than the scale -- which silently slides every tick away from the
    wavelength it is supposed to mark.
    """
    axis = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=2.6)
    marks = VGroup()
    for value in ticks:
        fraction = (value - low_nm) / (high_nm - low_nm)
        x = (fraction - 0.5) * width
        marks.add(Line([x, 0.0, 0], [x, -0.16, 0], color=color, stroke_width=2.6))
        marks.add(outlined_text(f"{int(value)}", cfg.FONT["tiny"], color).scale(0.8).move_to([x, -0.46, 0]))
    unit = outlined_text("nm", cfg.FONT["tiny"], color).scale(0.8).next_to(axis, RIGHT, buff=0.24)
    group = VGroup(axis, marks, unit)
    if center is not None:
        group.shift(np.array(center, dtype=float) - axis.get_center())
    return group


# ---------------------------------------------------------------------------
# Energy: the ramp, the staircase, and the ladder
# ---------------------------------------------------------------------------


def energy_ramp(width: float = 4.0, height: float = 3.0, color: str = cfg.MUTED) -> VGroup:
    """A smooth slope: any energy at all is available."""
    ramp = Line([-width / 2, -height / 2, 0], [width / 2, height / 2, 0], color=color, stroke_width=6)
    ground = Line([-width / 2, -height / 2, 0], [width / 2, -height / 2, 0], color=color,
                  stroke_width=3, stroke_opacity=0.5)
    return VGroup(ramp, ground)


def energy_staircase(width: float = 4.0, height: float = 3.0, steps: int = 4, color: str = cfg.CYAN) -> tuple[VGroup, list[np.ndarray]]:
    """A staircase, and the point at the middle of each tread to stand on."""
    stair = VGroup()
    treads: list[np.ndarray] = []
    step_width = width / steps
    step_height = height / steps
    x = -width / 2
    y = -height / 2
    for index in range(steps):
        tread = Line([x, y, 0], [x + step_width, y, 0], color=color, stroke_width=6)
        riser = Line([x + step_width, y, 0], [x + step_width, y + step_height, 0], color=color,
                     stroke_width=6, stroke_opacity=0.75)
        stair.add(tread, riser)
        treads.append(np.array([x + step_width / 2, y, 0.0]))
        x += step_width
        y += step_height
    return stair, treads


def energy_ladder(
    levels: Sequence[int],
    heights: Sequence[float],
    line_width: float = 5.6,
    color: str = cfg.CYAN,
    label_color: str = cfg.MUTED,
    font_size: int | None = None,
) -> tuple[VGroup, dict[int, Line]]:
    """Hydrogen's allowed energies as horizontal rails, keyed by quantum number.

    The heights come from the model, not from taste: they are proportional to
    1 - 1/n^2, so the rails crowd together at the top exactly as the real
    energies do. That crowding is what the spectrum's crowded violet end shows.
    """
    size = font_size or cfg.FONT["small"]
    group = VGroup()
    rails: dict[int, Line] = {}
    for n, height in zip(levels, heights):
        rail = Line([-line_width / 2, height, 0], [line_width / 2, height, 0], color=color, stroke_width=5)
        rail.set_stroke(opacity=0.95 if n <= 3 else 0.75)
        label = eq(f"n={n}", label_color, size).next_to(rail, LEFT, buff=0.34)
        group.add(rail, label)
        rails[n] = rail
    return group, rails


def ionisation_line(height: float, line_width: float = 5.6, color: str = cfg.PURPLE) -> VGroup:
    """The n -> infinity limit: the rail the electron never quite reaches."""
    rail = DashedVMobject(
        Line([-line_width / 2, height, 0], [line_width / 2, height, 0], color=color, stroke_width=4),
        num_dashes=34,
    )
    label = eq(r"n\to\infty", color, cfg.FONT["small"]).next_to(rail, LEFT, buff=0.34)
    return VGroup(rail, label)


def transition_arrow(
    start_rail: Line,
    end_rail: Line,
    color: str,
    x_offset: float = 0.0,
    stroke_width: float = 5.0,
) -> Arrow:
    """The electron's fall from one rail to another, drawn where it happens."""
    start = np.array([start_rail.get_center()[0] + x_offset, start_rail.get_center()[1], 0.0])
    end = np.array([end_rail.get_center()[0] + x_offset, end_rail.get_center()[1], 0.0])
    return Arrow(start, end, color=color, buff=0.05, stroke_width=stroke_width,
                 max_tip_length_to_length_ratio=0.14)


# ---------------------------------------------------------------------------
# The recurring narrative device
# ---------------------------------------------------------------------------

STAGE_COLORS: dict[str, str] = {
    "MODEL": cfg.CYAN,
    "PREDICTION": cfg.BLUE,
    "EXPERIMENT": cfg.GOLD,
    "RESULT": cfg.WHITE,
    "SURPRISE": cfg.ORANGE,
}


def stage_banner(stage: str, detail: str | None = None, color: str | None = None) -> VGroup:
    """The MODEL / PREDICTION / EXPERIMENT / RESULT label that structures the film."""
    tone = color or STAGE_COLORS.get(stage.upper(), cfg.CYAN)
    label = outlined_text(stage.upper(), cfg.FONT["label"], tone, BOLD)
    rule = Line(LEFT * (label.width / 2 + 0.28), RIGHT * (label.width / 2 + 0.28), color=tone,
                stroke_width=4, stroke_opacity=0.85)
    group = VGroup(label, rule).arrange(DOWN, buff=0.14)
    if detail:
        note = fit_width(outlined_text(detail, cfg.FONT["small"], cfg.MUTED, BOLD), cfg.SAFE_WIDTH - 1.0)
        group.add(note)
        group.arrange(DOWN, buff=0.16)
    return group


def check_mark(size: float = 0.30, color: str = cfg.GREEN) -> VMobject:
    mark = VMobject(color=color, stroke_width=size * 26)
    mark.set_points_as_corners([
        np.array([-size, 0.05 * size, 0.0]),
        np.array([-0.25 * size, -0.75 * size, 0.0]),
        np.array([size, 0.85 * size, 0.0]),
    ])
    return mark


def cross_mark(size: float = 0.28, color: str = cfg.RED) -> VGroup:
    width = size * 24
    return VGroup(
        Line([-size, -size, 0], [size, size, 0], color=color, stroke_width=width),
        Line([-size, size, 0], [size, -size, 0], color=color, stroke_width=width),
    )


def verdict_stamp(text: str, color: str = cfg.RED) -> VGroup:
    """MODEL FAILS, stamped across the frame when a prediction breaks."""
    label = outlined_text(text.upper(), cfg.FONT["title"], color, BOLD)
    frame = RoundedRectangle(
        width=label.width + 0.90,
        height=label.height + 0.62,
        corner_radius=0.16,
        color=color,
        stroke_width=6,
        fill_color=cfg.BG,
        fill_opacity=0.55,
    )
    return VGroup(frame, label).rotate(-8 * DEGREES)


def timeline_strip(
    entries: Sequence[tuple[str, str]],
    width: float = 12.4,
    y: float = 0.0,
) -> tuple[VGroup, list[VGroup]]:
    """The film's one and only timeline: names as stops on a lit rail."""
    rail = Line([-width / 2, y, 0], [width / 2, y, 0], color=cfg.MUTED, stroke_width=3, stroke_opacity=0.5)
    stops: list[VGroup] = []
    positions = np.linspace(-width / 2 + 0.7, width / 2 - 0.7, len(entries))
    slot = width / max(len(entries), 1)
    for index, ((label, color), x) in enumerate(zip(entries, positions)):
        node = glow_dot([x, y, 0], color, 0.10)
        # Names alternate above and below the rail. Set on one side, a long name
        # such as RUTHERFORD simply cannot clear its neighbours at a readable size.
        above = index % 2 == 0
        text = fit_to_width(outlined_text(label, cfg.FONT["small"], color, BOLD), slot * 1.45)
        text.move_to([x, y + (0.80 if above else -0.86), 0])
        stem = Line(
            [x, y + (0.13 if above else -0.13), 0],
            [x, y + (0.52 if above else -0.55), 0],
            color=color,
            stroke_width=2.4,
            stroke_opacity=0.6,
        )
        stops.append(VGroup(node, stem, text))
    return VGroup(rail), stops


# ---------------------------------------------------------------------------
# 3D constructions
# ---------------------------------------------------------------------------


def glowing_sphere(
    radius: float,
    color: str,
    resolution: tuple[int, int] = (24, 48),
    opacity: float = 1.0,
    shells: int = 2,
) -> VGroup:
    """A solid sphere wrapped in translucent shells, so it reads as a light source."""
    # Preview tessellation only; full-HD retains the authored sphere resolution.
    preview = config.pixel_height <= 480
    if preview:
        resolution = (min(resolution[0], 8), min(resolution[1], 16))
        shells = min(shells, 1)
    group = VGroup()
    core = Sphere(radius=radius, resolution=resolution, fill_opacity=opacity, stroke_width=0)
    core.set_color(color)
    group.add(core)
    for index in range(shells):
        scale = 1.35 + 0.55 * index
        shell = Sphere(radius=radius * scale, resolution=(6, 12) if preview else (12, 24), stroke_width=0)
        shell.set_color(color)
        shell.set_opacity(0.10 / (index + 1))
        group.add(shell)
    return group


def orbit_circle_3d(radius: float, color: str = cfg.MUTED, stroke_width: float = 3.0) -> ParametricFunction:
    """A ring in the z = 0 plane that survives being viewed from any angle."""
    return ParametricFunction(
        lambda t: np.array([radius * np.cos(t), radius * np.sin(t), 0.0]),
        t_range=[0, TAU],
        color=color,
        stroke_width=stroke_width,
    ).set_stroke(opacity=0.6)


def spiral_3d(points: np.ndarray, color: str = cfg.CYAN, stroke_width: float = 4.0) -> VMobject:
    """A model-generated in-spiral, drawn in the z = 0 plane."""
    return polyline(points, color, stroke_width, smooth=True)


def foil_lattice_3d(
    rows: int = 5,
    columns: int = 7,
    spacing: float = 0.62,
    radius: float = 0.13,
    color: str = cfg.GOLD,
) -> VGroup:
    """A slab of gold atoms standing in the y-z plane, for the beam to cross."""
    lattice = VGroup()
    for row in range(rows):
        for column in range(columns):
            y = (column - (columns - 1) / 2) * spacing
            z = (row - (rows - 1) / 2) * spacing
            atom = Sphere(radius=radius, resolution=(8, 16), stroke_width=0)
            atom.set_color(color)
            atom.set_opacity(0.55)
            atom.move_to([0.0, y, z])
            lattice.add(atom)
    return lattice


def probability_cloud(
    count: int = 900,
    radius: float = 2.0,
    color: str = cfg.PURPLE,
    seed: int = cfg.SEED,
    dot_radius: float = 0.022,
) -> VGroup:
    """A fuzzy shell of points: a hint of where the electron might be found.

    The radial density follows the hydrogen ground state, r^2 e^(-2r/a), so the
    haze is thickest at one Bohr radius. The film stops here on purpose, before
    the shape becomes an answer.

    The points are flat discs placed at 3D positions rather than `Dot3D`, which
    is a full Sphere mesh: a few hundred of those bring the Cairo renderer to a
    crawl. Under a tilted camera these read as a haze, which is all this is.
    """
    rng = np.random.default_rng(seed)
    cloud = VGroup()
    scale = radius / 1.0
    drawn = 0
    while drawn < count:
        r = float(rng.exponential(0.75))
        if r > 3.2:
            continue
        # Rejection-sample the radial probability so the shell peaks correctly.
        if rng.uniform() > (r * r * np.exp(-2.0 * r)) / 0.0555:
            continue
        theta = float(np.arccos(rng.uniform(-1.0, 1.0)))
        phi = float(rng.uniform(0.0, TAU))
        point = scale * r * np.array([
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta),
        ])
        dot = Dot(point, radius=dot_radius, color=color)
        dot.set_opacity(float(rng.uniform(0.25, 0.75)))
        cloud.add(dot)
        drawn += 1
    return cloud



def method_cycle(
    radius_x: float = 3.45,
    radius_y: float = 2.10,
    stages: Sequence[tuple[str, str]] | None = None,
    font_size: int | None = None,
) -> tuple[VGroup, list[VGroup], VGroup]:
    """The film's method, drawn as a loop rather than a list.

    A cycle is the honest shape for this story: the last stage is a new model,
    which is where the first stage started. Returned in pieces so a chapter can
    light one stage at a time.

    The ring is an ellipse, wider than it is tall, because the stage names are
    wide and the frame is 16 by 9. On a circle the two lower plates collide.
    """
    ring = stages or (
        ("MODEL", cfg.CYAN),
        ("PREDICTION", cfg.BLUE),
        ("EXPERIMENT", cfg.GOLD),
        ("SURPRISE", cfg.ORANGE),
        ("NEW MODEL", cfg.GREEN),
    )
    size = font_size or cfg.FONT["tiny"]
    plates: list[VGroup] = []
    centers: list[np.ndarray] = []
    for index, (text, color) in enumerate(ring):
        angle = PI / 2 - TAU * index / len(ring)
        center = np.array([radius_x * np.cos(angle), radius_y * np.sin(angle), 0.0])
        plate = chip(text, color, size).move_to(center)
        plates.append(plate)
        centers.append(center)

    arrows = VGroup()
    for index in range(len(ring)):
        start = centers[index]
        end = centers[(index + 1) % len(ring)]
        direction = end - start
        span = float(np.linalg.norm(direction))
        unit = direction / span
        # Start and end the arc clear of the plates it joins, not inside them.
        arrows.add(
            CurvedArrow(
                start + unit * (span * 0.40),
                end - unit * (span * 0.40),
                angle=-0.55,
                color=cfg.MUTED,
                stroke_width=3.4,
                tip_length=0.20,
            ).set_opacity(0.75)
        )
    return VGroup(*plates), plates, arrows
