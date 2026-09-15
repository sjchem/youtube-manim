"""Chapter 15: carbon poses the question, and Hund's rule is the answer.

The chapter starts at carbon, draws both candidate arrangements, and lets the
viewer choose before naming the rule. Then it jumps to neon, where the
capacity of a p subshell turns out to be something the labels already implied
rather than a number to be memorised.

Oxygen sits between them, and it is the other half of Hund's rule. Carbon shows
the preference for separate orbitals while there is still a choice; oxygen is
the first atom with no choice left, where the fourth p electron has to pair.
Seeing both is what stops the rule being remembered as "never pair".
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    boxes,
    check_mark,
    density_slice,
    outlined_text,
)

from manim_scenes.filling_motion import ReadingTrace, fill_electrons, portrait_push_in

DIAGRAM_CENTRE = RIGHT * 2.4
PORTRAIT_CENTRE = [-4.15, -0.35, 0]


def _element_card(symbol: str, z: int) -> VGroup:
    name = outlined_text(symbol, cfg.FONT["title"], cfg.GOLD)
    number = outlined_text(f"Z = {z}", cfg.FONT["small"], cfg.MUTED)
    return VGroup(name, number).arrange(DOWN, buff=0.20).move_to([-4.15, 2.65, 0])


def _candidate(scene: QuantumScene, paired: bool) -> VGroup:
    """One of the two ways to put carbon's second p electron into the diagram."""
    if paired:
        slot = scene.anchor.slots[("2p", 0)].get_center()
        arrow = Arrow(slot + np.array([0.22, 0.27, 0]), slot + np.array([0.22, -0.27, 0]),
                      buff=0, color=cfg.PURPLE, stroke_width=4, max_tip_length_to_length_ratio=0.3)
    else:
        slot = scene.anchor.slots[("2p", 1)].get_center()
        arrow = Arrow(slot + np.array([-0.22, -0.27, 0]), slot + np.array([-0.22, 0.27, 0]),
                      buff=0, color=cfg.CYAN, stroke_width=4, max_tip_length_to_length_ratio=0.3)
    return arrow


class Scene15FillingP(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("15")

    # -- Beat 1: jump straight to carbon's two p electrons -------------------
    # Five arrows are the partial carbon diagram, not a separate boron lesson.
    scene.morph(boxes(5, center=DIAGRAM_CENTRE), seconds=1.5)
    portrait = density_slice(2, 1, 0, size=3.7).move_to(PORTRAIT_CENTRE)
    scene.show(portrait, seconds=0.7)
    card = scene.pin(_element_card("C", 6))
    scene.playq(FadeIn(card), seconds=0.6)
    portrait_push_in(portrait)
    focus = ReadingTrace()
    focus.focus([scene.anchor.slots[("2p", 0)]], cfg.GOLD)
    scene.add(focus)
    scene.at(8)

    # -- Beat 2: compare the two allowed candidate arrangements -------------
    question = scene.pin(outlined_text("pair them, or keep them apart?",
                                       cfg.FONT["small"], cfg.GOLD).move_to([0, 3.60, 0]))
    scene.playq(FadeIn(question), seconds=0.6)

    paired = _candidate(scene, paired=True)
    scene.local.append(paired)
    scene.playq(GrowArrow(paired), seconds=0.6)
    focus.focus([scene.anchor.slots[("2p", 0)]], cfg.GOLD)
    scene.bring_to_front(focus)
    scene.hold(2.2)
    scene.playq(FadeOut(paired), seconds=0.5)
    scene.local.remove(paired)

    separate = _candidate(scene, paired=False)
    scene.local.append(separate)
    scene.playq(GrowArrow(separate), seconds=0.6)
    focus.focus([scene.anchor.slots[("2p", index)] for index in (0, 1)], cfg.CYAN)
    scene.bring_to_front(focus)
    scene.hold(2.0)
    scene.at(20)
    scene.drop(separate, question, seconds=0.6)

    # -- Beat 3: the lower-energy choice, and only now its name ---------------
    fill_electrons(scene, 6)
    focus.focus([scene.anchor.slots[("2p", index)] for index in (0, 1)], cfg.GREEN)
    scene.bring_to_front(focus)
    verdict = VGroup(check_mark(0.20, cfg.GREEN),
                     outlined_text("separate orbitals, parallel spins", cfg.FONT["small"], cfg.GREEN))
    verdict.arrange(RIGHT, buff=0.30).move_to([2.4, -3.35, 0])
    scene.show(verdict, seconds=0.7)
    hund = scene.pin(outlined_text("HUND'S FIRST RULE", cfg.FONT["label"], cfg.GOLD).move_to([0, 3.65, 0]))
    scene.playq(FadeIn(hund), seconds=0.7)
    written = scene.formula(r"2p^2", position=[-4.15, -3.05, 0], size=56)
    scene.hold(2.4)
    scene.drop(hund, seconds=0.6)

    energetics = scene.pin(outlined_text("lower total energy",
                                         cfg.FONT["tiny"], cfg.MUTED).move_to([0, 3.55, 0]))
    scene.playq(FadeIn(energetics), seconds=0.6)
    scene.at(39)
    scene.drop(card, written, verdict, energetics, seconds=0.6)

    # -- Beat 3b: oxygen, where the rule runs out of empty orbitals -----------
    # The density portrait yields its space to the large occupancy equation.
    portrait.clear_updaters()
    scene.playq(FadeOut(portrait), seconds=0.6)
    scene.local.remove(portrait)
    card = scene.pin(_element_card("O", 8))
    scene.playq(FadeIn(card), seconds=0.7)
    fill_electrons(scene, 7)
    focus.focus([scene.anchor.slots[("2p", index)] for index in range(3)], cfg.CYAN)
    scene.bring_to_front(focus)
    spread = scene.pin(outlined_text("three p orbitals, one electron each",
                                     cfg.FONT["small"], cfg.CYAN).move_to([0, 3.62, 0]))
    scene.playq(FadeIn(spread), seconds=0.7)
    scene.playq(LaggedStart(*(Indicate(scene.anchor.slots[("2p", index)], color=cfg.CYAN)
                              for index in range(3)), lag_ratio=0.35), seconds=2.4)
    scene.bring_to_front(focus)
    scene.hold(1.2)

    forced = scene.pin(outlined_text("the next one has nowhere empty to go",
                                     cfg.FONT["small"], cfg.GOLD).move_to([0, 3.62, 0]))
    scene.playq(FadeTransform(spread, forced), seconds=0.8)
    scene.local.remove(spread)
    scene.remove_fixed_in_frame_mobjects(spread)
    fill_electrons(scene, 8)
    focus.focus([scene.anchor.slots[("2p", 0)]], cfg.PURPLE)
    scene.bring_to_front(focus)
    written = scene.formula(r"2p^4", position=[-4.15, -0.35, 0], size=60)
    scene.playq(Indicate(scene.anchor.slots[("2p", 0)], color=cfg.PURPLE), seconds=1.4)
    scene.bring_to_front(focus)
    pairing = scene.pin(outlined_text("so it pairs · opposite spins, as always",
                                      cfg.FONT["small"], cfg.PURPLE).move_to([0, -3.62, 0]))
    scene.playq(FadeIn(pairing), seconds=0.7)
    scene.hold(1.6)
    equal = scene.pin(outlined_text("all three have the same energy — any of them would do",
                                    cfg.FONT["tiny"], cfg.MUTED, limit=11.0).move_to([0, -3.62, 0]))
    scene.playq(FadeTransform(pairing, equal), seconds=0.8)
    # All three p orbitals are equivalent choices for the paired electron.
    focus.focus([scene.anchor.slots[("2p", index)] for index in range(3)], cfg.PURPLE)
    scene.bring_to_front(focus)
    scene.local.remove(pairing)
    scene.remove_fixed_in_frame_mobjects(pairing)
    scene.hold(1.8)
    scene.at(74)
    scene.drop(forced, equal, card, written, seconds=0.7)

    # -- Beat 4: complete the p set in one transition ------------------------
    # Nitrogen and fluorine stay off screen: the point is the completed set.
    scene.hold(0.7)
    fill_electrons(scene, 10, seconds=2.0)
    focus.focus([scene.anchor.slots[("2p", index)] for index in range(3)], cfg.GREEN)
    scene.bring_to_front(focus)
    card = scene.pin(_element_card("Ne", 10))
    scene.playq(FadeIn(card), seconds=0.6)
    written = scene.formula(r"2p^6", position=[-4.15, -0.35, 0], size=64)
    scene.at(85)

    # -- Beat 5: the capacity follows from the states already counted --------
    capacity = scene.formula(r"3\ \text{orbitals} \times 2\ \text{spins} = 6",
                             position=[0, -3.60, 0], size=44, color=cfg.GOLD)
    # Animate owned slots directly: a LaggedStart would add a second group
    # root containing them and leave an extra diagram at the chapter boundary.
    for index in range(3):
        scene.playq(Indicate(scene.anchor.slots[("2p", index)], color=cfg.GREEN), seconds=1.0)
        scene.bring_to_front(focus)
    scene.at(97)
    scene.drop(capacity, seconds=0.6)
    scene.cue("occupancy, not electron identities", color=cfg.MUTED, hold=2.2)
    scene.at(106)
    scene.drop(card, written, seconds=0.6)
    focus.clear_updaters()
    scene.playq(FadeOut(focus), seconds=0.4)
    scene.finish()
