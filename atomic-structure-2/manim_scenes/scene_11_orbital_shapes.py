"""Chapter 11: the shapes, and the places the electron is never found.

Every surface here is extracted from a real hydrogen wave function rather than
drawn from memory. The chapter keeps saying the two things that are easy to get
wrong: the boundary is a display choice, and a node is a property of the wave,
not a wall.

It also draws the one curve that is most often drawn wrongly. The probability
*density* of 1s is largest at the nucleus; the *radial distribution*
P(r) = r^2 R(r)^2 is zero there, because a shell of no radius has no volume,
and it peaks at exactly one Bohr radius. That is Bohr's number handed back --
as the most probable distance, never as a track.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    equation,
    node_radius,
    node_shell,
    orbital_axes,
    outlined_text,
)
from manim_scenes.radial_probability_visual import radial_probability_demo

PHI, THETA = 68, -50
NODE_PHI = 82
DISPLAY_SCALE = 0.78


def _display_orbital(scene: QuantumScene, *state, **options) -> VGroup:
    """Relight during animation without rerendering identical stationary holds.

    Lighting depends on camera orientation, not elapsed time. A one-argument
    updater still runs on every animated frame, including camera turns, while
    allowing Manim to reuse a still frame when neither state nor camera moves.
    """
    surface = scene.orbital(*state, **options)
    lighting = tuple(surface.get_updaters())
    surface.clear_updaters()

    def relight(mob: VGroup) -> None:
        for update in lighting:
            update(mob)

    surface.add_updater(relight)
    return surface


def _nodal_plane(size: float = 3.2 * DISPLAY_SCALE,
                 colour: str = cfg.GOLD) -> VGroup:
    """A tessellated xy sheet at z=0, depth-sorted with the orbital triangles.

    A single large polygon can only sort as one object. Small coplanar faces
    let the front and back of the sheet occlude correctly between the lobes.
    The nucleus and every plane vertex remain at the same physical origin.
    """
    subdivisions = 14
    coordinates = np.linspace(-size, size, subdivisions + 1)
    plane = VGroup()
    for x0, x1 in zip(coordinates[:-1], coordinates[1:]):
        for y0, y1 in zip(coordinates[:-1], coordinates[1:]):
            a, b = [x0, y0, 0], [x1, y0, 0]
            c, d = [x1, y1, 0], [x0, y1, 0]
            for corners in ((a, b, c), (a, c, d)):
                tile = Polygon(*corners, fill_color=colour, fill_opacity=0.09,
                               stroke_width=0)
                tile.set_shade_in_3d(True)
                plane.add(tile)

    # Segmented perimeter and centre lines share the sheet's depth ordering.
    # The centre lines visibly cross exactly between the positive/negative lobes.
    for a, b in zip(coordinates[:-1], coordinates[1:]):
        for start, stop, width, opacity in (
            ([a, -size, 0], [b, -size, 0], 2.0, 0.65),
            ([a, size, 0], [b, size, 0], 2.0, 0.65),
            ([-size, a, 0], [-size, b, 0], 2.0, 0.65),
            ([size, a, 0], [size, b, 0], 2.0, 0.65),
            ([a, 0, 0], [b, 0, 0], 1.6, 0.55),
            ([0, a, 0], [0, b, 0], 1.6, 0.55),
        ):
            segment = Line(start, stop, color=colour, stroke_width=width,
                           stroke_opacity=opacity)
            segment.set_shade_in_3d(True)
            plane.add(segment)
    plane._needs_depth_sort = True
    plane.is_nodal_plane = True
    return plane


def _show_nodal_plane(scene: QuantumScene, plane: VGroup, seconds: float) -> None:
    """Reveal the sheet from near eye level so its central position is clear."""
    scene.local.append(plane)
    scene.move_camera(
        phi=NODE_PHI * DEGREES,
        added_anims=[FadeIn(plane)],
        run_time=max(1 / config.frame_rate, seconds / cfg.SPEED),
        rate_func=smooth,
    )


def _state_label(scene: QuantumScene, name: str) -> Mobject:
    return scene.formula(name, position=UP * 3.40, size=60)


class Scene11OrbitalShapes(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("11")

    # -- Beat 1: the ground state has no preferred direction ------------------
    scene.dissolve(_display_orbital(scene, 1, 0, 0, size=2.55 * DISPLAY_SCALE), seconds=2.2)
    scene.view3d(phi=PHI, theta=THETA, seconds=2.0)
    axis = orbital_axes(3.6 * DISPLAY_SCALE)
    scene.show(axis, seconds=0.5)
    label = _state_label(scene, "1s")
    scene.turn(seconds=8.5, angle=0.55)
    scene.at(17)

    # -- Beat 2: the surface is a display choice, not the edge of the atom ----
    boundary = scene.pin(outlined_text("surface encloses ≈ 90% of the probability",
                                       cfg.FONT["small"], cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(boundary), seconds=0.7)
    scene.hold(2.0)
    scene.drop(boundary, seconds=0.5)

    scene.morph(_display_orbital(scene, 1, 0, 0, size=3.05 * DISPLAY_SCALE, fraction=0.97), seconds=2.6)
    wider = scene.pin(outlined_text("≈ 97% · same state, different boundary",
                                    cfg.FONT["small"], cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(wider), seconds=0.6)
    scene.hold(1.8)
    scene.at(32)
    scene.drop(wider, label, seconds=0.6)

    # -- Beat 2b: measure spherical probability in a linked flat view --------
    # Clear the depth-sorted surface before returning to the density slice.
    scene.drop(axis, seconds=0.4)
    scene.dissolve(VGroup(), seconds=0.6)
    scene.flat(seconds=0.8)
    radial_probability_demo(scene)
    scene.view3d(phi=PHI, theta=THETA, seconds=1.0)
    axis = orbital_axes(3.6 * DISPLAY_SCALE)
    scene.show(axis, seconds=0.4)
    scene.at(67)

    # -- Beat 3: two s is larger, and it is hollow ----------------------------
    scene.morph(_display_orbital(scene, 2, 0, 0, size=3.15 * DISPLAY_SCALE), seconds=2.6)
    label = _state_label(scene, "2s")
    scene.turn(seconds=7.5, angle=0.5)
    scene.at(84)

    # Turn the surface translucent so the node inside it can be seen at all,
    # then open it. Cutting first only shows a ragged rim: the 90% surface of 2s
    # is a thick shell, and the interesting radius is deep inside it.
    wall = node_shell(node_radius(2, 0, 0, 3.15 * DISPLAY_SCALE))
    scene.morph(_display_orbital(scene, 2, 0, 0, size=3.15 * DISPLAY_SCALE, opacity=0.42), seconds=2.0)
    scene.show(wall, seconds=0.9)
    node_note = scene.pin(outlined_text("a spherical node · ψ = 0, so |ψ|² = 0",
                                        cfg.FONT["small"], cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(node_note), seconds=0.7)
    scene.turn(seconds=5.0, angle=0.40)

    # Kept translucent through the cut as well: the surface is a bag of whole
    # triangles, so an opaque cut edge is a visible staircase rather than a clean
    # section through the shell.
    scene.morph(_display_orbital(scene, 2, 0, 0, size=3.15 * DISPLAY_SCALE, cut=[-0.35, -1.0, 0.0], opacity=0.58), seconds=2.2)
    not_a_shell = scene.pin(VGroup(
        outlined_text("a feature of the wave", 28, cfg.MUTED),
        outlined_text("not a wall", 28, cfg.MUTED),
    ).arrange(DOWN, buff=0.18).move_to([5.15, 0.8, 0]))
    scene.playq(FadeIn(not_a_shell), seconds=0.6)
    scene.turn(seconds=4.0, angle=0.32)
    scene.at(105)
    scene.drop(node_note, not_a_shell, wall, label, seconds=0.7)

    # -- Beat 4: change the angular pattern -----------------------------------
    scene.morph(_display_orbital(scene, 2, 1, 0, size=3.05 * DISPLAY_SCALE), seconds=2.6)
    label = _state_label(scene, "2p")
    plane = _nodal_plane()
    _show_nodal_plane(scene, plane, seconds=0.8)
    plane_note = scene.pin(outlined_text("two lobes, separated by a nodal plane",
                                         cfg.FONT["small"], cfg.CYAN).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(plane_note), seconds=0.6)
    scene.turn(seconds=7.0, angle=0.45)
    scene.drop(plane, plane_note, seconds=0.6)

    # -- Beat 5: the same shape, pointed elsewhere ----------------------------
    for magnetic in (1, -1):
        scene.morph(_display_orbital(scene, 2, 1, magnetic, size=3.05 * DISPLAY_SCALE), seconds=2.4)
        if magnetic == 1:
            # Return from the near-side node view while inspecting the next
            # orientation; the same narration window now carries the tilt.
            scene.move_camera(phi=PHI * DEGREES,
                              run_time=max(1 / config.frame_rate, 4.5 / cfg.SPEED),
                              rate_func=smooth)
        else:
            scene.turn(seconds=4.5, angle=0.35)
    scene.at(136)

    one_state = scene.pin(outlined_text("one state · the lobes are not two electrons",
                                        cfg.FONT["small"], cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(one_state), seconds=0.7)
    scene.hold(2.2)
    scene.drop(one_state, label, seconds=0.6)

    # -- Beat 6: higher angular patterns, all five of them --------------------
    # The names are orientations, and they are worth having: a viewer will meet
    # every one of them again. What the chapter does not do is hand each name a
    # single m_l value -- four of these five are combinations of magnetic
    # states, and only d_z2 is one on its own.
    scene.morph(_display_orbital(scene, 3, 2, -2, size=3.05 * DISPLAY_SCALE), seconds=2.4)
    label = _state_label(scene, "3d")
    shape = scene.pin(outlined_text("d_xy", cfg.FONT["small"], cfg.CYAN).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(shape), seconds=0.5)
    scene.turn(seconds=4.0, angle=0.34)

    for index, (magnetic, name) in enumerate(((1, "d_xz"), (-1, "d_yz"), (2, "d_x²−y²"))):
        scene.morph(_display_orbital(scene, 3, 2, magnetic, size=3.05 * DISPLAY_SCALE), seconds=2.0)
        replacement = outlined_text(name, cfg.FONT["small"], cfg.CYAN).move_to([0, -3.45, 0])
        scene.add_fixed_in_frame_mobjects(replacement)
        scene.remove(replacement)
        scene.playq(FadeTransform(shape, replacement), seconds=0.6)
        scene.remove_fixed_in_frame_mobjects(shape)
        if shape in scene.local:
            scene.local.remove(shape)
        shape = replacement
        scene.local.append(shape)
        scene.turn(seconds=3.4, angle=0.30)

    scene.morph(_display_orbital(scene, 3, 2, 0, size=3.05 * DISPLAY_SCALE), seconds=2.2)
    ring_note = outlined_text("d_z²  ·  two lobes and a ring", cfg.FONT["small"], cfg.CYAN).move_to([0, -3.45, 0])
    scene.add_fixed_in_frame_mobjects(ring_note)
    scene.remove(ring_note)
    scene.playq(FadeTransform(shape, ring_note), seconds=0.6)
    scene.remove_fixed_in_frame_mobjects(shape)
    if shape in scene.local:
        scene.local.remove(shape)
    scene.local.append(ring_note)
    scene.turn(seconds=4.5, angle=0.36)

    counted = scene.pin(VGroup(
        equation(r"2\ell+1 = 5", 44, cfg.GOLD),
        outlined_text("independent states", 28, cfg.GOLD),
    ).arrange(DOWN, buff=0.20).move_to([4.8, 1.25, 0]))
    scene.playq(FadeIn(counted), seconds=0.7)
    scene.hold(2.0)
    scene.at(196)
    scene.drop(ring_note, counted, label, seconds=0.6)

    # -- Beat 7: every node says the same thing -------------------------------
    rule = scene.formula(r"\psi = 0 \quad\Rightarrow\quad |\psi|^2 = 0", position=UP * 3.35, size=54)
    scene.morph(_display_orbital(scene, 2, 1, 0, size=3.05 * DISPLAY_SCALE), seconds=2.6)
    plane = _nodal_plane()
    _show_nodal_plane(scene, plane, seconds=0.7)
    solutions = scene.pin(VGroup(
        equation(r"N_{\rm radial}=n-\ell-1 \qquad N_{\rm angular}=\ell", 34, cfg.GOLD),
        outlined_text("2s: one radial node     ·     2p: one angular node", 28, cfg.CYAN),
    ).arrange(DOWN, buff=0.24).move_to([0, -3.55, 0]))
    scene.playq(FadeIn(solutions), seconds=0.7)
    scene.turn(seconds=6.0, angle=0.4)
    scene.at(217)
    scene.drop(rule, solutions, plane, axis, seconds=0.7)

    scene.finish()
