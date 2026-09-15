"""Chapter 17: the nineteenth electron goes where the shelves say, not where the shell does.

Chapter 13 split the energies and left a puzzle on screen: 4s sits below 3d.
This chapter pays that off with the bookkeeping rule that predicts it, and with
the atom where the prediction is impossible to miss. Potassium starts a new
shell before the previous one is finished.

The rule is stated as what it is. Increasing (n + l), ties broken by the
smaller n, reproduces the ground configurations of most neutral atoms; it is a
very good guide, not a law, and the exceptions are the sequel's subject.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    diagonal_chart,
    energy_shelves,
    equation,
    glow_dot,
    madelung_rows,
    outlined_text,
)

from manim_scenes.filling_motion import ReadingTrace
from manim_scenes.screening_visuals import ShelfLight

BRIGHT_CYAN = "#A1F6FF"
BRIGHT_GOLD = "#FFE36A"
BRIGHT_VIOLET = "#D2AEFF"


class DiagonalFlow(VGroup):
    """Travel down each guide arrow without changing its filling order."""

    def __init__(self, arrows: VGroup) -> None:
        super().__init__()
        self.elapsed = 0.0
        self.routes = []
        for arrow in arrows:
            path = Line(arrow.get_start(), arrow.get_end())
            halo = VMobject().set_stroke(BRIGHT_GOLD, width=9, opacity=0.15)
            light = VMobject().set_stroke(cfg.WHITE, width=3, opacity=0.95)
            self.routes.append((path, halo, light))
            self.add(halo, light)
        self.set_z_index(2)
        self.add_updater(self._advance)

    def _advance(self, _mob, dt: float) -> None:
        self.elapsed += dt * cfg.SPEED
        head = (self.elapsed / 3.2) % 1.0
        for path, halo, light in self.routes:
            for stroke in (halo, light):
                stroke.pointwise_become_partial(path, max(0, head - 0.22), head)


def occupancy_markers(shelf: Mobject, count: int) -> VGroup:
    """Count electrons on an energy level; these are bookkeeping markers."""
    markers = VGroup()
    centre = shelf.get_center() + UP * 0.14
    for index in range(count):
        position = centre + RIGHT * (index - (count - 1) / 2) * 0.34
        marker = glow_dot(position, radius=0.060, color=BRIGHT_CYAN)
        marker.add(Dot(position, radius=0.024, color=cfg.WHITE))
        markers.add(marker)
    return markers


FILLED = ("1s", "2s", "2p", "3s", "3p")
COUNTS = {"1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 6}


class Scene17Potassium(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("17")

    # -- Beat 1: keep filling past sodium, and stop at eighteen ---------------
    shelves = energy_shelves(split=True)
    # Bright labels and fixed colors carry the 4s / 3d comparison throughout.
    for index, name in enumerate(shelves.shelves):
        colour = (BRIGHT_GOLD if name == "4s" else
                  BRIGHT_VIOLET if name == "3d" else BRIGHT_CYAN)
        shelves.shelves[name].set_color(colour)
        shelves[2 * index + 1].scale(1.14).set_color(colour)
    scene.morph(shelves, seconds=2.0)
    scene.playq(scene.anchor.animate.scale(0.78).move_to([-3.05, 0.15, 0]), seconds=1.2)

    lights = VGroup(
        ShelfLight({name: scene.anchor.shelves[name] for name in FILLED}, BRIGHT_CYAN),
        ShelfLight({"4s": scene.anchor.shelves["4s"]}, BRIGHT_GOLD),
        ShelfLight({"3d": scene.anchor.shelves["3d"]}, BRIGHT_VIOLET),
    )
    scene.add(lights)

    running = 0
    tally = scene.pin(equation(r"18\ \text{electrons placed}", 40, BRIGHT_CYAN).move_to([3.5, 2.6, 0]))
    counter = scene.pin(equation("0", 52, BRIGHT_GOLD).move_to([3.5, 1.55, 0]))
    scene.playq(FadeIn(tally), FadeIn(counter), seconds=0.5)
    for name in FILLED:
        running += COUNTS[name]
        replacement = equation(str(running), 52, BRIGHT_GOLD).move_to([3.5, 1.55, 0])
        scene.add_fixed_in_frame_mobjects(replacement)
        scene.remove(replacement)
        markers = occupancy_markers(scene.anchor.shelves[name], COUNTS[name])
        scene.playq(
            LaggedStart(*(FadeIn(marker, shift=DOWN * 0.25) for marker in markers), lag_ratio=0.12),
            Indicate(scene.anchor.shelves[name], color=cfg.GREEN, scale_factor=1.02),
            FadeTransform(counter, replacement),
            seconds=1.05,
        )
        scene.adopt(markers)
        scene.bring_to_front(lights)
        scene.remove_fixed_in_frame_mobjects(counter)
        if counter in scene.local:
            scene.local.remove(counter)
        counter = replacement
        scene.local.append(counter)
    argon = scene.pin(outlined_text("argon", cfg.FONT["small"], cfg.GREEN).move_to([3.5, 0.65, 0]))
    scene.playq(FadeIn(argon), seconds=0.5)
    scene.at(14)
    scene.drop(tally, counter, argon, seconds=0.6)

    # -- Beat 2: one electron left, and two shelves that both look reasonable -
    question = scene.pin(outlined_text("potassium · one electron left", cfg.FONT["small"], cfg.GOLD)
                         .move_to([0, 3.50, 0]))
    scene.playq(FadeIn(question), seconds=0.5)
    guesses = VGroup()
    for name, colour, note in (("3d", BRIGHT_VIOLET, "finish shell three?"),
                               ("4s", BRIGHT_GOLD, "or open shell four?")):
        shelf = scene.anchor.shelves[name]
        ring = SurroundingRectangle(shelf, color=colour, buff=0.16, stroke_width=3, corner_radius=0.10)
        tag = outlined_text(note, cfg.FONT["tiny"] - 4, colour).next_to(ring, RIGHT, buff=0.30)
        guesses.add(VGroup(ring, tag))
    for pair in guesses:
        scene.playq(Create(pair[0]), FadeIn(pair[1]), seconds=1.1)
    scene.local.append(guesses)
    candidate_focus = ReadingTrace()
    candidate_focus.focus([pair[1] for pair in guesses], BRIGHT_GOLD)
    scene.add(candidate_focus)
    scene.hold(1.6)
    scene.at(26)
    candidate_focus.clear_updaters()
    scene.remove(candidate_focus)
    scene.drop(guesses, question, seconds=0.6)

    # -- Beat 3: the arithmetic that decides it -------------------------------
    heading = scene.pin(outlined_text("FILLING GUIDE  ·  increasing n + ℓ",
                                      cfg.FONT["small"], cfg.GOLD).move_to([0, 3.50, 0]))
    scene.playq(FadeIn(heading, shift=DOWN * 0.10), seconds=0.7)
    table = madelung_rows(7, scale=0.86).move_to([3.55, -0.30, 0])
    for name, cells in table.rows.items():
        cells[0].set_color(BRIGHT_GOLD if name == "4s" else
                           BRIGHT_VIOLET if name == "3d" else BRIGHT_CYAN)
        cells[1].set_color(BRIGHT_CYAN)
        cells[2].set_color(BRIGHT_VIOLET)
        cells[3].set_color(BRIGHT_GOLD)
    scene.show(table, seconds=1.0)
    tie = scene.pin(outlined_text("same n + ℓ → smaller n first", 27, BRIGHT_CYAN, limit=6.4)
                    .move_to([3.55, 2.65, 0]))
    scene.add(tie)
    row_focus = ReadingTrace()
    row_focus.focus([table.rows["2p"], table.rows["3s"]], BRIGHT_CYAN)
    scene.add(row_focus)
    scene.playq(LaggedStart(*(Indicate(table.rows[name], color=cfg.WHITE, scale_factor=1.05)
                              for name in ("1s", "2s", "2p", "3s", "3p")), lag_ratio=0.42), seconds=3.0)
    row_focus.focus([table.rows["4s"], table.rows["3d"]], BRIGHT_GOLD)
    scene.playq(
        Indicate(table.rows["4s"], color=BRIGHT_GOLD, scale_factor=1.12),
        Indicate(scene.anchor.shelves["4s"], color=BRIGHT_GOLD, scale_factor=1.03),
        seconds=1.6,
    )
    scene.playq(
        Indicate(table.rows["3d"], color=BRIGHT_VIOLET, scale_factor=1.12),
        Indicate(scene.anchor.shelves["3d"], color=BRIGHT_VIOLET, scale_factor=1.03),
        seconds=1.6,
    )
    verdict = scene.pin(equation(r"4s:\ n+l=4 \;<\; 3d:\ n+l=5", 42, cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(verdict), seconds=0.8)
    scene.bring_to_front(row_focus, lights)
    scene.at(48)
    row_focus.clear_updaters()
    scene.remove(row_focus)
    scene.drop(table, verdict, tie, seconds=0.7)

    # -- Beat 4: the same rule, read off the diagonals -------------------------
    chart = diagonal_chart(rows=4).scale(1.10).move_to([3.55, -0.25, 0])
    chart.tiles["4s"][1].set_color(BRIGHT_GOLD)
    chart.tiles["3d"][1].set_color(BRIGHT_VIOLET)
    chart[2].set_z_index(4)
    # Draw the arrows only once, then keep a light flowing in their direction.
    chart.arrows.set_z_index(1)
    chart.remove(chart.arrows)
    scene.show(chart, seconds=0.9)
    scene.playq(LaggedStart(*(GrowArrow(arrow) for arrow in chart.arrows), lag_ratio=0.30), seconds=3.2)
    scene.remove(*chart.arrows)
    chart.submobjects.insert(1, chart.arrows)
    diagonal_flow = DiagonalFlow(chart.arrows)
    scene.add(diagonal_flow)
    scene.playq(
        Indicate(chart.tiles["4s"], color=BRIGHT_GOLD, scale_factor=1.18),
        Indicate(chart.tiles["3d"], color=BRIGHT_VIOLET, scale_factor=1.18),
        seconds=1.6,
    )
    scene.at(62)
    diagonal_flow.clear_updaters()
    scene.remove(diagonal_flow)
    scene.drop(chart, heading, seconds=0.7)

    # -- Beat 5: put the electron where the rule says -------------------------
    target = scene.anchor.shelves["4s"].get_center()
    arriving = glow_dot(target + RIGHT * 3.0 + UP * 0.8, 0.15, BRIGHT_GOLD)
    arriving.add(Dot(arriving.get_center(), radius=0.05, color=cfg.WHITE))
    scene.show(arriving, seconds=0.4)
    scene.playq(arriving.animate.move_to(target + UP * 0.16), seconds=1.5,
                rate_func=rate_functions.ease_in_out_sine)
    scene.playq(Flash(target + UP * 0.16, color=cfg.GOLD, flash_radius=0.34), seconds=0.7)
    written = scene.pin(equation(r"\mathrm{K}:\ 1s^2\,2s^2\,2p^6\,3s^2\,3p^6\,4s^1", 46, cfg.WHITE)
                        .move_to([3.3, 1.30, 0]))
    scene.playq(FadeIn(written), seconds=0.8)
    started = scene.pin(outlined_text("shell four opens before shell three fills",
                                      cfg.FONT["tiny"], cfg.GOLD, limit=6.4).move_to([3.3, 0.10, 0]))
    scene.playq(FadeIn(started), seconds=0.7)
    final_focus = ReadingTrace()
    final_focus.focus([written, scene.anchor.shelves["4s"]], BRIGHT_GOLD)
    scene.add(final_focus)
    scene.at(74)
    scene.cue("a very good guide, not a law", BRIGHT_CYAN, hold=2.2, position=DOWN * 3.45)
    final_focus.clear_updaters()
    scene.remove(final_focus)
    scene.drop(arriving, written, started, seconds=0.7)
    lights.clear_updaters()
    scene.remove(lights)

    scene.finish()
