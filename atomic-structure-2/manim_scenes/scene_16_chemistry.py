"""Chapter 16: the Ne-to-Na bridge from filling to chemistry.

It opens by settling a debt to the viewer. Most people meet sodium at school as
"2, 8, 1", and the film has spent twenty minutes building a different notation
without ever saying the two are the same statement. So the ring diagram from
chapter 3 comes back one last time and each of its shell counts splits into the
subshells inside it: 2 becomes 1s^2, 8 becomes 2s^2 2p^6, 1 becomes 3s^1. The
quantum model does not overturn the counting rule from school; it explains it.

The completed p set becomes an atom with one new outer electron. Schematic
density views then make the ionization contrast visible. The periodic table
itself waits for the next-video question in the recap.
"""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    bohr_shell_atom,
    boxes,
    equation,
    glow_dot,
    outlined_text,
)

from manim_scenes.filling_motion import ReadingTrace, fill_electrons
from manim_scenes.chemistry_motion import (
    ShellRotation, DensityViewMotion, neon_density, sodium_density,
    OUTER_CYAN, OUTER_GOLD,
)

NEON_CENTRE = LEFT * 3.4
SODIUM_CENTRE = RIGHT * 3.4


def _neon() -> VGroup:
    return neon_density(NEON_CENTRE)


def _sodium() -> VGroup:
    return sodium_density(SODIUM_CENTRE)


class Scene16Chemistry(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("16")

    # -- Beat 1: inherit neon's completed set; sodium opens 3s ---------------
    scene.morph(boxes(10, center=RIGHT * 2.4), seconds=1.0)
    name = scene.pin(outlined_text("Ne", cfg.FONT["title"], OUTER_CYAN).move_to([-4.15, 1.0, 0]))
    scene.playq(FadeIn(name), seconds=0.5)
    focus = ReadingTrace()
    focus.focus([scene.anchor.slots[("2p", index)] for index in range(3)], OUTER_CYAN)
    scene.add(focus)
    scene.at(3)
    scene.drop(name, seconds=0.5)
    name = scene.pin(outlined_text("Na", cfg.FONT["title"], OUTER_GOLD).move_to([-4.15, 1.0, 0]))
    scene.playq(FadeIn(name), seconds=0.5)
    fill_electrons(scene, 11)
    focus.focus([scene.anchor.slots[("3s", 0)]], OUTER_GOLD)
    scene.bring_to_front(focus)
    written = scene.formula(r"[\mathrm{Ne}]\,3s^1", position=[-4.15, -0.65, 0], size=50)
    scene.playq(Indicate(scene.anchor.slots[("3s", 0)], color=cfg.GOLD), seconds=1.1)
    scene.bring_to_front(focus)
    scene.at(12)
    scene.drop(name, written, seconds=0.6)

    # -- Beat 1b: the notation from school, and the notation we built --------
    shells = bohr_shell_atom((2, 8, 1), nucleus_radius=0.30, electron_radius=0.095)
    shells.scale(0.62).move_to([-3.95, 0.30, 0])
    focus.clear_updaters()
    scene.remove(focus)
    rotation = ShellRotation(shells)
    # Put the driver before the diagram so Cairo redraws every moving bead.
    scene.add(rotation)
    scene.morph(shells, seconds=2.2)
    school = scene.pin(VGroup(
        outlined_text("what school taught", cfg.FONT["tiny"], cfg.MUTED),
        equation(r"2,\ 8,\ 1", 56, cfg.GOLD),
    ).arrange(DOWN, buff=0.24).move_to([-3.95, -3.05, 0]))
    scene.playq(FadeIn(school), seconds=0.8)

    rows = (
        (1, r"2 \;\rightarrow\; 1s^2", OUTER_CYAN),
        (2, r"8 \;\rightarrow\; 2s^2\,2p^6", OUTER_CYAN),
        (3, r"1 \;\rightarrow\; 3s^1", OUTER_GOLD),
    )
    mapped = VGroup()
    for shell, latex, colour in rows:
        line = equation(latex, 46, colour)
        mapped.add(line)
    mapped.arrange(DOWN, buff=0.62, aligned_edge=LEFT).move_to([3.30, 0.30, 0])
    for (shell, _, colour), line in zip(rows, mapped):
        scene.add_fixed_in_frame_mobjects(line)
        scene.remove(line)
        scene.playq(
            Indicate(scene.anchor.rings[shell], color=cfg.WHITE, scale_factor=1.04),
            *[Indicate(bead, color=cfg.WHITE, scale_factor=1.15)
              for bead in scene.anchor.electrons[shell]],
            FadeIn(line, shift=LEFT * 0.16),
            seconds=1.9,
        )
    scene.local.append(mapped)
    reading = ReadingTrace()
    reading.focus(mapped, OUTER_GOLD)
    scene.add(reading)

    same = scene.pin(outlined_text("the same atom, counted twice", cfg.FONT["small"], cfg.GREEN, limit=7.0)
                     .move_to([3.30, -3.05, 0]))
    scene.playq(FadeIn(same), seconds=0.7)
    scene.hold(2.0)
    scene.at(42)
    reading.clear_updaters()
    scene.playq(FadeOut(reading), FadeOut(school), FadeOut(mapped), FadeOut(same), seconds=0.7)
    for label in (school, mapped, same):
        scene.remove_fixed_in_frame_mobjects(label)
        scene.local.remove(label)

    # -- Beat 2: the occupancy picture becomes a spatial comparison ---------
    neon, sodium = _neon(), _sodium()
    scene.morph(VGroup(neon, sodium), seconds=2.2)
    rotation.clear_updaters()
    scene.remove(rotation)
    turning = DensityViewMotion((neon, sodium))
    scene.add(turning)
    scene.remove(scene.anchor)
    scene.add(scene.anchor)
    names = scene.show(VGroup(
        outlined_text("Ne", cfg.FONT["title"], OUTER_CYAN).move_to([-3.4, 2.9, 0]),
        outlined_text("Na", cfg.FONT["title"], OUTER_GOLD).move_to([3.4, 2.9, 0]),
    ), seconds=0.7)
    labels = scene.pin(VGroup(
        outlined_text("closed outer shell", cfg.FONT["small"], OUTER_CYAN).move_to([-3.4, -3.25, 0]),
        outlined_text("one outer electron", cfg.FONT["small"], OUTER_GOLD).move_to([3.4, -3.25, 0]),
    ))
    view_note = scene.pin(outlined_text("schematic density · turning view", 25, cfg.MUTED)
                          .move_to([0, 3.95, 0]))
    scene.playq(FadeIn(labels), FadeIn(view_note), seconds=0.6)
    scene.at(55)
    scene.drop(labels, seconds=0.6)

    # -- Beat 3: the gold density leaves with the ionized electron ------------
    # A detection marker illustrates the outcome, not a pre-existing orbit.
    escaping = glow_dot([4.9, 0.2, 0], radius=0.14, color=OUTER_GOLD)
    escaping.add(Dot(escaping.get_center(), radius=0.042, color=cfg.WHITE))
    scene.show(escaping, seconds=0.5)
    scene.playq(
        escaping.animate.move_to([6.9, 1.5, 0]).set_opacity(0.85),
        sodium[2].animate.set_opacity(0),
        seconds=2.6,
    )
    scene.drop(escaping, seconds=0.4)
    ion = MathTex(r"\mathrm{Na}^{+}", font_size=60, color=OUTER_GOLD).move_to(names[1])
    scene.playq(Transform(names[1], ion), seconds=0.7)
    scene.cue("energies → chemistry", hold=2.4)
    scene.at(71)
    scene.drop(names, view_note, seconds=0.7)
    turning.clear_updaters()
    scene.remove(turning)
    scene.finish()
