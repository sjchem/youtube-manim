"""Chapter 14: hydrogen, helium, lithium -- and the rules named only after use.

Helium is where exclusion is derived rather than announced. Both of its
electrons want the lowest state, and that state's three spatial labels are
(1, 0, 0) for each of them. Put the two addresses side by side and they are
identical, which is the contradiction: if no two electrons may share every
label, and three of the four already match, the fourth has to be the one that
differs. Spin is not introduced here as a new fact, it is the only place left
for the difference to live.

Aufbau is the search for the lowest-energy arrangement, so the chapter performs
the search first and names it afterwards. Pauli arrives the same way: the film
draws the arrangement that is not allowed, marks it, and only then says why.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    boxes,
    cross_mark,
    density_slice,
    equation,
    outlined_text,
)

from manim_scenes.filling_motion import (
    ReadingTrace as _ReadingTrace,
    fill_electrons as _fill_next,
    portrait_push_in as _portrait_push_in,
)


DIAGRAM_CENTRE = RIGHT * 2.4
PORTRAIT_CENTRE = [-4.15, -0.25, 0]


def _element_card(symbol: str, z: int) -> VGroup:
    """The atom currently under construction, named at the top of its column."""
    name = outlined_text(symbol, cfg.FONT["title"], cfg.GOLD)
    number = outlined_text(f"Z = {z}", cfg.FONT["small"], cfg.MUTED)
    return VGroup(name, number).arrange(DOWN, buff=0.20).move_to([-4.15, 2.65, 0])


class Scene14BuildingAtoms(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("14")

    # -- Beat 1: hydrogen. One electron, lowest available state ---------------
    scene.morph(boxes(0, center=DIAGRAM_CENTRE), seconds=2.0)
    portrait = density_slice(1, 0, 0, size=3.0).move_to(PORTRAIT_CENTRE)
    scene.show(portrait, seconds=0.8)
    card = scene.pin(_element_card("H", 1))
    scene.playq(FadeIn(card), seconds=0.7)

    _fill_next(scene, 1)
    _portrait_push_in(portrait)
    focus = _ReadingTrace()
    focus.focus([scene.anchor.slots[("1s", 0)]], cfg.GOLD)
    scene.add(focus)
    written = scene.formula(r"1s^1", position=[-4.15, -2.85, 0], size=56)
    scene.at(8)
    aufbau = scene.pin(outlined_text("AUFBAU · lowest energy first",
                                     cfg.FONT["small"], cfg.GOLD).move_to([0, 3.65, 0]))
    scene.playq(FadeIn(aufbau), seconds=0.7)
    scene.hold(2.0)
    scene.drop(aufbau, seconds=0.6)
    scene.at(14)
    scene.drop(card, written, seconds=0.6)

    # -- Beat 2: helium. The arrangement that is not allowed, drawn first -----
    card = scene.pin(_element_card("He", 2))
    scene.playq(FadeIn(card), seconds=0.7)
    slot = scene.anchor.slots[("1s", 0)].get_center()
    same_spin = Arrow(slot + np.array([0.22, -0.27, 0]), slot + np.array([0.22, 0.27, 0]),
                      buff=0, color=cfg.RED, stroke_width=4, max_tip_length_to_length_ratio=0.3)
    rejected = VGroup(cross_mark(0.20, cfg.RED),
                      outlined_text("same spin state", cfg.FONT["tiny"], cfg.RED))
    rejected.arrange(RIGHT, buff=0.28).next_to(scene.anchor, DOWN, buff=0.55)
    scene.show(VGroup(same_spin, rejected), seconds=0.8)
    scene.playq(Indicate(same_spin, color=cfg.RED), seconds=1.2)
    focus.focus([scene.anchor.slots[("1s", 0)]], cfg.RED)
    scene.bring_to_front(focus)
    scene.at(23)
    scene.drop(same_spin, rejected, seconds=0.6)

    # -- Beat 2b: put the two addresses side by side and read the collision ---
    addresses = scene.pin(VGroup(
        VGroup(
            outlined_text("electron 1", cfg.FONT["tiny"] - 4, cfg.CYAN),
            equation(r"n=1,\ \ell=0,\ m_\ell=0", 34, cfg.CYAN),
        ).arrange(DOWN, buff=0.18),
        VGroup(
            outlined_text("electron 2", cfg.FONT["tiny"] - 4, cfg.CYAN),
            equation(r"n=1,\ \ell=0,\ m_\ell=0", 34, cfg.CYAN),
        ).arrange(DOWN, buff=0.18),
    ).arrange(DOWN, buff=0.70).move_to([-4.05, 0.55, 0]))
    portrait.clear_updaters()
    scene.playq(LaggedStart(*(FadeIn(entry, shift=RIGHT * 0.14) for entry in addresses),
                            lag_ratio=0.6), FadeOut(portrait), seconds=2.0)
    clash = scene.pin(VGroup(
        cross_mark(0.22, cfg.RED),
        outlined_text("three labels, all identical", cfg.FONT["tiny"], cfg.RED, limit=5.0),
    ).arrange(RIGHT, buff=0.30).move_to([-4.05, -1.05, 0]))
    scene.playq(FadeIn(clash), Indicate(addresses, color=cfg.RED, scale_factor=1.05), seconds=1.8)
    focus.focus([entry[1] for entry in addresses], cfg.CYAN)
    scene.bring_to_front(focus)
    scene.hold(1.4)

    fourth = scene.pin(equation(r"m_s=+\tfrac12,\; -\tfrac12", 42, cfg.GOLD).move_to([-4.05, -2.30, 0]))
    scene.playq(FadeIn(fourth, shift=UP * 0.12), seconds=0.9)
    only = scene.pin(outlined_text("the only label left to differ",
                                   cfg.FONT["tiny"], cfg.GREEN, limit=5.4).move_to([-4.05, -3.25, 0]))
    scene.playq(FadeIn(only), seconds=0.7)
    focus.focus([fourth], cfg.GOLD)
    scene.bring_to_front(focus)
    scene.hold(1.8)
    scene.at(40)
    focus.focus([scene.anchor.slots[("1s", 0)]], cfg.GREEN)
    scene.bring_to_front(focus)
    scene.drop(addresses, clash, fourth, only, seconds=0.7)

    _fill_next(scene, 2)
    scene.bring_to_front(focus)
    scene.playq(FadeIn(portrait), seconds=0.6)
    _portrait_push_in(portrait)
    written = scene.formula(r"1s^2", position=[-4.15, -2.85, 0], size=56)
    pauli = scene.pin(outlined_text("PAULI · opposite spins here",
                                    cfg.FONT["small"], cfg.GOLD).move_to([0, 3.65, 0]))
    scene.playq(FadeIn(pauli), seconds=0.7)
    scene.hold(2.2)
    scene.drop(pauli, seconds=0.6)
    scene.at(54)

    fermion = scene.pin(outlined_text("fermion exclusion",
                                      cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.70, 0]))
    scene.playq(FadeIn(fermion), Indicate(scene.anchor.slots[("1s", 0)], color=cfg.GREEN), seconds=1.8)
    scene.at(63)
    portrait.clear_updaters()
    scene.drop(card, written, fermion, seconds=0.6)

    # -- Beat 3: lithium. The inner state is full, so the next one opens ------
    card = scene.pin(_element_card("Li", 3))
    scene.playq(FadeIn(card), seconds=0.7)
    focus.focus([scene.anchor.slots[("2s", 0)]], cfg.CYAN)
    _fill_next(scene, 3)
    scene.bring_to_front(focus)
    outer = density_slice(2, 0, 0, size=4.2).move_to(PORTRAIT_CENTRE)
    scene.playq(FadeOut(portrait), FadeIn(outer), seconds=1.8)
    scene.local.remove(portrait)
    scene.local.append(outer)
    written = scene.formula(r"1s^2\,2s^1", position=[-4.15, -2.85, 0], size=50)
    pattern = scene.pin(outlined_text("a new outer electron",
                                      cfg.FONT["small"], cfg.CYAN).move_to([0, 3.60, 0]))
    scene.playq(FadeIn(pattern), seconds=0.7)
    scene.at(76)
    scene.drop(pattern, seconds=0.6)
    focus.clear_updaters()
    scene.playq(FadeOut(focus), seconds=0.4)

    scene.finish()
