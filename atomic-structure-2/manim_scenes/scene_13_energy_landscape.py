"""Chapter 13: what changes when the atom stops having exactly one electron.

Hydrogen's levels depend only on n. Add electrons and they screen one another,
different shapes penetrate the inner region differently, and the energies split
by angular family as well. The shelves here are schematic on purpose, and the
chapter says so before it uses them.
"""

from __future__ import annotations

from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    boxes,
    energy_shelves,
    equation,
    glow_dot,
    outlined_text,
)

from manim_scenes.screening_visuals import ScreeningView, RadialComparison, ShelfLight

FILLING_ORDER = ("2s", "2p", "3s", "3p", "4s", "3d")

# Where each third-shell curve puts its innermost lobe, in Bohr radii, and
# how far out the screening core reaches. utils/audit.py pins all four.
CORE = 1.5
INNERMOST = {0: 0.74, 1: 3.00, 2: 9.00}


class Scene13EnergyLandscape(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("13")

    # -- Beat 1: with one electron, only n matters ----------------------------
    scene.morph(energy_shelves(split=False), seconds=2.0)
    degenerate = scene.pin(outlined_text("hydrogen · 2s and 2p sit together",
                                         cfg.FONT["small"], cfg.CYAN).move_to([0, 3.35, 0]))
    scene.playq(FadeIn(degenerate), seconds=0.7)
    level_light = ShelfLight(scene.anchor.shelves)
    scene.add(level_light)
    scene.at(16)
    level_light.clear_updaters()
    scene.remove(level_light)
    scene.drop(degenerate, seconds=0.6)

    # -- Beat 2: show the force balance at a fixed sample position -----------
    inner = ScreeningView()
    scene.morph(inner, seconds=2.0)
    inner.start_motion()
    screening = scene.pin(outlined_text("inner density screens the nuclear pull",
                                        cfg.FONT["small"], cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(screening), seconds=0.6)
    scene.playq(inner.strength.animate.set_value(1.0), seconds=4.0, rate_func=smooth)
    scene.at(33)
    inner.clear_updaters()
    scene.remove(inner.strength)
    scene.drop(screening, seconds=0.6)

    # -- Beat 2b: separate the curves, but keep their scales identical --------
    # Each state gets a row and a dedicated numeric column. No peak label or
    # leader line crosses another curve. These remain hydrogen examples, not
    # calibrated many-electron orbitals; the core band is illustrative.
    curves = RadialComparison(CORE, INNERMOST)
    scene.morph(curves, seconds=2.2)
    for row in curves.data:
        scene.playq(Create(row[0]), FadeIn(VGroup(*row[1:])), seconds=2.3)
        scene.adopt(row)
        scene.hold(1.0)
    curves.start_motion()
    penetrates = scene.pin(outlined_text("3s penetrates more strongly · 3d has a small inner tail",
                                         31, cfg.GOLD, limit=13.2).move_to([0, -3.75, 0]))
    scene.playq(FadeIn(penetrates), seconds=0.7)
    scene.hold(7.0)
    lowest = scene.pin(outlined_text("penetration helps lower s, then p, then d",
                                     31, cfg.CYAN).move_to([0, -3.75, 0]))
    scene.playq(FadeTransform(penetrates, lowest), seconds=0.8)
    scene.local.remove(penetrates)
    scene.remove_fixed_in_frame_mobjects(penetrates)
    scene.at(73)
    curves.clear_updaters()
    scene.drop(lowest, seconds=0.7)

    # -- Beat 3: the levels separate by angular family ------------------------
    scene.morph(energy_shelves(split=True), seconds=2.6)
    split_note = scene.pin(outlined_text("many electrons · n alone no longer fixes the energy",
                                         cfg.FONT["small"], cfg.CYAN).move_to([0, 3.55, 0]))
    scene.playq(FadeIn(split_note), seconds=0.7)
    schematic = scene.pin(outlined_text("schematic spacing · a common neutral-atom filling guide",
                                        cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.70, 0]))
    scene.playq(FadeIn(schematic), seconds=0.6)
    level_light = ShelfLight(scene.anchor.shelves)
    scene.add(level_light)
    # Compare equal-n families in place: their energy difference is now visible.
    # The moving light remains a reading cue, never an electron occupation.
    comparison = None
    for principal, names in ((2, ("2s", "2p")), (3, ("3s", "3p", "3d"))):
        rings = VGroup(*[
            SurroundingRectangle(scene.anchor.shelves[name], buff=0.11,
                                 color=cfg.GOLD, stroke_width=2.3, corner_radius=0.08)
            for name in names
        ])
        note = VGroup(
            equation(rf"n={principal}", 40, cfg.GOLD),
            outlined_text("same shell", 26, cfg.WHITE, limit=2.6),
            outlined_text("energies differ", 26, cfg.CYAN, limit=2.6),
        ).arrange(DOWN, buff=0.20).move_to([5.85, 0.25, 0])
        target = VGroup(rings, note)
        if comparison is None:
            scene.playq(FadeIn(target), seconds=1.0)
        else:
            scene.playq(FadeTransform(comparison, target), seconds=1.0)
        comparison = target
        scene.hold(6.0)
    scene.at(108)
    scene.playq(FadeOut(comparison), seconds=0.5)

    # -- Beat 4: walk the filling order --------------------------------------
    shelves = scene.anchor.shelves
    marker = glow_dot(shelves["1s"].get_center() + RIGHT * 3.2, radius=0.14, color=cfg.GOLD)
    scene.show(marker, seconds=0.5)
    for name in FILLING_ORDER:
        scene.playq(marker.animate.move_to(shelves[name].get_center() + RIGHT * 3.2), seconds=1.3)
        scene.hold(0.7)
    scene.at(129)
    scene.drop(marker, split_note, schematic, seconds=0.6)

    # -- Beat 4b: the order has a surprise in it, and it is left standing -----
    # Named here, answered in chapter 17. Stating the puzzle and then walking
    # away from it is deliberate: the rule that settles it belongs with the
    # atom that makes it matter.
    odd = VGroup()
    for name, colour in (("4s", cfg.CYAN), ("3d", cfg.RED)):
        ring = SurroundingRectangle(shelves[name], color=colour, buff=0.14,
                                    stroke_width=3, corner_radius=0.10)
        odd.add(ring)
    scene.playq(LaggedStart(*(Create(ring) for ring in odd), lag_ratio=0.4), seconds=1.8)
    scene.local.append(odd)
    inversion = scene.pin(outlined_text("neutral-atom filling guide: 4s before 3d", cfg.FONT["small"], cfg.GOLD)
                          .move_to([0, 3.45, 0]))
    scene.playq(FadeIn(inversion), seconds=0.7)
    scene.hold(1.6)
    consequence = scene.pin(outlined_text("a shell can begin before the one beneath it is full",
                                          cfg.FONT["small"], cfg.CYAN, limit=11.0)
                            .move_to([0, -3.70, 0]))
    scene.playq(FadeIn(consequence), seconds=0.7)
    scene.hold(2.2)
    scene.at(138)
    scene.drop(odd, inversion, consequence, seconds=0.7)

    # -- Beat 5: the rule underneath, and the diagram that will apply it ------
    principle = scene.pin(outlined_text("find the arrangement with the lowest total energy",
                                        cfg.FONT["small"], cfg.GOLD).move_to([0, 3.45, 0]))
    scene.playq(FadeIn(principle), seconds=0.7)
    level_light.clear_updaters()
    scene.remove(level_light)
    scene.morph(boxes(0, center=RIGHT * 2.4), seconds=2.0)
    scene.at(147)
    scene.drop(principle, seconds=0.6)

    scene.finish()
