"""Chapter 8: from a clamped string to Schroedinger's stationary equation.

The string is the bridge and the film says so on screen: an atom has no string
and no rigid outer wall. What survives the analogy is the only thing the
chapter needs -- a condition on a wave picks out a discrete set of patterns,
each one arriving with its own energy.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    density_slice,
    glow_dot,
    orbital_axes,
    outlined_text,
    string_mode,
)

from manim_scenes.scientist_portraits import scientist_portrait
from utils.quantum_examples import hydrogen_energy

SPAN = 4.0
# A z offset projects down consistently while the camera circles the atom.
# These are presentation sizes, not a shared physical radius scale.
ORBITAL_CENTRE = np.array([0.0, 0.0, -0.55])
ORBITAL_SIZES = {"1s": 2.0, "2p": 2.15}
CAMERA_TURN_RATE = 0.085
MODE_LABELS = {1: "fundamental", 2: "one node", 3: "two nodes"}


def _clamps() -> VGroup:
    """The two fixed ends. The wave has to vanish at both, and that is the rule."""
    posts = VGroup()
    for x in (-SPAN, SPAN):
        posts.add(Line([x, -1.6, 0], [x, 1.6, 0], color=cfg.GOLD, stroke_width=6))
        posts.add(glow_dot([x, 0, 0], radius=0.11, color=cfg.GOLD))
    return posts


def _node_dots(mode: int) -> VGroup:
    """The interior points that stay still, marked so the count is visible."""
    dots = VGroup()
    for index in range(1, mode):
        x = -SPAN + 2 * SPAN * index / mode
        dots.add(Dot([x, 0, 0], radius=0.085, color=cfg.GOLD).set_stroke(cfg.BG, width=2))
    return dots


class Scene08AllowedStates(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("08")

    # -- Beat 1: a string that is only allowed certain shapes -----------------
    scene.morph(string_mode(1), seconds=2.0)
    posts = _clamps()
    scene.show(posts, seconds=0.8)

    caption = None
    for mode in (1, 2, 3):
        swing = ValueTracker(0.0)
        moving = always_redraw(lambda mode=mode: string_mode(mode, swing.get_value()))
        scene.morph(moving, seconds=1.4)
        nodes = _node_dots(mode)
        label = outlined_text(MODE_LABELS[mode], cfg.FONT["small"], cfg.CYAN).move_to([0, -2.55, 0])
        scene.add_fixed_in_frame_mobjects(label)
        scene.remove(label)
        if caption is None:
            scene.playq(FadeIn(label), FadeIn(nodes), seconds=0.5)
        else:
            scene.playq(FadeTransform(caption, label), FadeIn(nodes), seconds=0.5)
            scene.remove_fixed_in_frame_mobjects(caption)
            scene.local.remove(caption)
        caption = label
        scene.local += [caption, nodes]
        scene.playq(swing.animate.set_value(4 * PI), seconds=4.4, rate_func=linear)
        moving.clear_updaters()
        scene.hold(1.6)
        scene.drop(nodes, seconds=0.4)

    bridge = scene.pin(outlined_text("an analogy · an atom has no string and no wall",
                                     cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.55, 0]))
    scene.playq(FadeIn(bridge), seconds=0.6)
    scene.at(40)
    scene.drop(caption, bridge, posts, seconds=0.7)

    # -- Beat 2: Schrödinger supplies the equation for the allowed states -----
    scene.morph(string_mode(1).scale(0.50).shift(RIGHT * 2.3 + DOWN * 1.7), seconds=0.8)
    portrait = scene.pin(scientist_portrait("schrodinger.jpg", "Erwin Schrödinger"))
    scene.playq(FadeIn(portrait), seconds=0.7)
    law = scene.headline(r"\hat H\,\psi=E\,\psi", position=[2.3, 0.7, 0])
    scene.hold(2.2)
    scene.drop(portrait, seconds=0.6)
    scene.playq(law.animate.move_to(UP * 3.10), seconds=0.7)
    scene.at(47)
    scene.drop(law, seconds=0.5)

    # The expanded operator says what the compact H actually does. Keep its
    # two contributions visually separate from the cloud behind them.
    expanded = scene.formula(r"\left[-\frac{\hbar^2}{2m_e}\nabla^2+V(\mathbf r)\right]\psi=E\psi",
                             position=[-0.65, 3.1, 0], size=52)
    terms = scene.pin(VGroup(
        outlined_text("kinetic", 30, cfg.CYAN).move_to([-5.0, 1.8, 0]),
        outlined_text("potential", 30, cfg.GOLD).move_to([5.0, 1.8, 0]),
    ))
    scene.playq(FadeIn(terms), seconds=0.6)
    scene.view3d(phi=68, theta=-50, seconds=1.6)
    # Inspect a stationary state from a continuously moving viewpoint. Keeping
    # the surface itself fixed preserves its geometry and live lighting normals.
    scene.begin_ambient_camera_rotation(rate=CAMERA_TURN_RATE * cfg.SPEED)
    scene.morph(
        scene.orbital(1, 0, 0, size=ORBITAL_SIZES["1s"]).shift(ORBITAL_CENTRE),
        seconds=2.0,
    )
    axis = orbital_axes(2.65).shift(ORBITAL_CENTRE)
    scene.show(axis, seconds=0.5)
    kinetic = scene.formula(r"K=\frac{p^2}{2m_e}", position=[-5.0, 0.65, 0], size=44, color=cfg.CYAN)
    potential = scene.formula(r"V(r)=-\frac{e^2}{4\pi\varepsilon_0 r}", position=[5.0, 0.65, 0], size=42, color=cfg.GOLD)
    scene.hold(4.0)
    scene.at(66)
    scene.drop(expanded, terms, kinetic, potential, seconds=0.7)
    law = scene.headline(r"\hat H\,\psi=E\,\psi", position=[-4.85, 2.8, 0])

    # -- Beat 3: hydrogen's ground state is a shape AND an energy -------------
    state = scene.formula(r"\psi_{1s}", position=[4.85, 1.35, 0], size=60, color=cfg.CYAN)
    energy = scene.formula(rf"E_1\approx {hydrogen_energy(1):.1f}\ \mathrm{{eV}}",
                           position=[4.85, 0.15, 0], size=48, color=cfg.GOLD)
    spectrum = scene.formula(r"E_n\approx-\frac{13.6\ \mathrm{eV}}{n^2}",
                             position=[-4.85, -1.35, 0], size=48, color=cfg.GOLD)
    scene.hold(5.0)
    scene.at(86)
    scene.drop(state, energy, seconds=0.6)

    # -- Beat 4: a different solution, with the changed energy alongside ------
    scene.morph(
        scene.orbital(2, 1, 0, size=ORBITAL_SIZES["2p"]).shift(ORBITAL_CENTRE),
        seconds=2.6,
    )
    state = scene.formula(r"\psi_{2p}", position=[4.85, 1.35, 0], size=60, color=cfg.CYAN)
    energy = scene.formula(rf"E_2\approx {hydrogen_energy(2):.2f}\ \mathrm{{eV}}",
                           position=[4.85, 0.15, 0], size=48, color=cfg.GOLD)
    scene.hold(6.0)
    scene.at(105)
    scene.drop(state, energy, spectrum, law, seconds=0.7)
    stationary = scene.pin(outlined_text("stationary density", cfg.FONT["small"], cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(stationary), seconds=0.7)
    scene.hold(6.0)
    scene.at(116)
    scene.drop(stationary, seconds=0.6)
    connection = scene.formula(r"p=\hbar k\quad\longrightarrow\quad-\frac{\hbar^2}{2m_e}\nabla^2",
                               position=[-3.65, 2.7, 0], size=44, color=cfg.CYAN)
    scene.at(126)
    scene.drop(connection, axis, seconds=0.7)

    # -- Beat 5: flatten out, holding the state, and ask what psi means -------
    scene.dissolve(VGroup(), seconds=1.2)
    scene.stop_ambient_camera_rotation()
    scene.flat(seconds=1.4)
    scene.dissolve(density_slice(2, 1, 0, phase=True), seconds=1.8)

    scene.finish()
