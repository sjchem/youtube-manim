"""Chapter 12: four labels for one quantum state, built out of the pictures.

Nothing here is introduced as a table to memorise. Each label is added only
once the viewer has already seen the distinction it names: n after watching the
scale change, l after watching the shape change, m_l after watching the
orientation change, and m_s once a second electron needs somewhere to go.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    chip,
    equation,
    orbital_axes,
    outlined_text,
    street,
)

# The shorthand the chapter ends on: a question per label, not a definition.
SHORTHAND = (
    (r"n", "HOW LARGE?", cfg.GOLD),
    (r"\ell", "WHAT SHAPE?", cfg.CYAN),
    (r"m_\ell", "WHICH WAY?", cfg.PURPLE),
    (r"m_s", "WHICH SPIN?", cfg.GREEN),
)
LETTER_FAMILIES = ((1, 0, 0, "s"), (2, 1, 0, "p"), (3, 2, -2, "d"), (4, 3, 2, "f"))


class _FocusSweep(VGroup):
    """Crossfade a quiet reading highlight over existing shapes, in order.

    These are presentation overlays, not occupancy markers. The houses, room
    counts and text never move or change. Copies keep this independent of the
    authored Indicate animations, and every overlay leaves with the analogy.
    """

    def __init__(self) -> None:
        super().__init__()
        self.elapsed = 0.0
        self.period = 1.4
        self.add_updater(self._advance)

    def focus(self, parts, colour: str, period: float = 1.4,
              outline_only: bool = False) -> None:
        self.submobjects.clear()
        self.elapsed = 0.0
        self.period = period
        for part in parts:
            # Outline text rows instead of putting a fill over the letters.
            shape = (SurroundingRectangle(part, buff=0.14, corner_radius=0.08)
                     if outline_only else part.copy().clear_updaters())
            glow = shape.copy().set_fill(opacity=0).set_stroke(colour, width=8)
            face = shape.copy().set_fill(opacity=0)
            face.set_stroke(colour, width=2.3)
            self.add(VGroup(glow, face))
        self._advance(self, 0)

    def pause(self) -> None:
        self.submobjects.clear()

    def _advance(self, _mob: Mobject, dt: float) -> None:
        self.elapsed += dt * cfg.SPEED
        if not len(self):
            return
        # Overlapping cosine envelopes make one focus fade into the next.
        # Geometry stays fixed, so a sweep cannot push labels into a neighbour.
        phase = self.elapsed / self.period
        for index, (glow, face) in enumerate(self):
            distance = (phase - index + len(self) / 2) % len(self) - len(self) / 2
            strength = (0.5 + 0.5 * np.cos(PI * distance)
                        if abs(distance) < 1 else 0.0)
            glow.set_stroke(opacity=0.16 * strength)
            face.set_stroke(opacity=0.90 * strength)


def _start_camera_sway(scene: QuantumScene):
    """A bounded camera inspection, including the narration holds.

    The orbital itself remains a stationary quantum state. A small azimuth
    range keeps the established composition while its lighting reveals form.
    """
    tracker = scene.camera.theta_tracker
    origin = tracker.get_value()
    elapsed = 0.0

    def sway(mob: ValueTracker, dt: float) -> None:
        nonlocal elapsed
        elapsed += dt * cfg.SPEED
        mob.set_value(origin + 0.26 * np.sin(TAU * elapsed / 32.0))

    tracker.add_updater(sway)
    scene.add(tracker)

    def stop() -> None:
        tracker.remove_updater(sway)
        scene.remove(tracker)

    return stop


def _spin_arrows() -> VGroup:
    up = Arrow(DOWN * 0.45, UP * 0.45, buff=0, color=cfg.CYAN, stroke_width=5)
    down = Arrow(UP * 0.45, DOWN * 0.45, buff=0, color=cfg.PURPLE, stroke_width=5)
    return VGroup(up, down).arrange(RIGHT, buff=0.70)


def _shorthand_card() -> VGroup:
    """Four rows of symbol, arrow, question -- the thing worth remembering."""
    rows = VGroup()
    for symbol, question, colour in SHORTHAND:
        glyph = MathTex(symbol, color=colour, font_size=62)
        glyph.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
        arrow = Arrow(LEFT * 0.30, RIGHT * 0.30, buff=0, color=cfg.MUTED, stroke_width=3,
                      max_tip_length_to_length_ratio=0.5)
        # A fixed-width slot for the symbol, so the four arrows line up even
        # though n, l, m_l and m_s are very different widths.
        slot = VGroup(Rectangle(width=1.05, height=0.72, stroke_width=0, fill_opacity=0), glyph)
        glyph.move_to(slot[0])
        rows.add(VGroup(slot, arrow, outlined_text(question, cfg.FONT["label"], colour))
                 .arrange(RIGHT, buff=0.45))
    rows.arrange(DOWN, buff=0.52, aligned_edge=LEFT)
    return rows


class Scene12QuantumAddress(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("12")

    # -- Beat 1: which one of these did you mean? -----------------------------
    # Camera first: a p state seen end-on from the flat view is a disc, and the
    # whole chapter is about telling these shapes apart.
    scene.view3d(phi=68, theta=-50, seconds=1.6)
    stop_camera_sway = _start_camera_sway(scene)
    scene.dissolve(scene.orbital(2, 1, 0, size=2.7), seconds=2.0)
    axis = orbital_axes(3.6)
    scene.show(axis, seconds=0.5)
    scene.cue("WHICH STATE?", cfg.GOLD, hold=2.0)

    # -- Beat 2: n, watched as a change of scale ------------------------------
    principal = scene.formula(r"n = 1, 2, 3, \ldots", position=UP * 3.40, size=58, color=cfg.GOLD)
    scale_note = scene.pin(outlined_text("the shell, and the size", cfg.FONT["small"], cfg.GOLD).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(scale_note), seconds=0.6)
    for shell, size in ((1, 1.55), (2, 2.30), (3, 3.00)):
        scene.morph(scene.orbital(shell, 0, 0, size=size), seconds=2.2)
        scene.hold(3.4)
    scene.at(37)
    scene.drop(principal, scale_note, seconds=0.6)

    # -- Beat 3: l, watched as a change of shape ------------------------------
    angular = scene.formula(r"\ell = 0, 1, \ldots, n-1", position=UP * 3.40, size=56, color=cfg.GOLD)
    letter = None
    angular_example = None
    for shell, family, magnetic, name in LETTER_FAMILIES:
        scene.morph(scene.orbital(shell, family, magnetic, size=2.7), seconds=2.0)
        tag = chip(name, cfg.CYAN, cfg.FONT["hero"]).move_to([4.95, 0, 0])
        scene.add_fixed_in_frame_mobjects(tag)
        scene.remove(tag)
        if letter is None:
            scene.playq(FadeIn(tag), seconds=0.4)
        else:
            scene.playq(FadeTransform(letter, tag), seconds=0.4)
            scene.remove_fixed_in_frame_mobjects(letter)
            scene.local.remove(letter)
        letter = tag
        scene.local.append(letter)
        if angular_example is not None:
            scene.drop(angular_example, seconds=0.25)
        angular_example = scene.formula(
            rf"L^2={family * (family + 1)}\hbar^2",
            position=DOWN * 3.45, size=50, color=cfg.CYAN,
        )
        scene.hold(3.4)
    scene.drop(angular_example, seconds=0.3)
    angular_size = scene.formula(r"L^2=\ell(\ell+1)\hbar^2",
                                 position=DOWN * 3.45, size=50, color=cfg.CYAN)
    scene.hold(3.0)
    scene.at(78)
    scene.drop(angular, angular_size, letter, axis, seconds=0.6)

    # -- Beat 3b: the same three labels, as an address ------------------------
    # The chapter is called "an address for a quantum state" and until now it
    # has only said so. A house number, a floor and a room are exactly the
    # three spatial labels, and the analogy is captioned as an analogy: a shell
    # is not a container and a floor is not a place.
    stop_camera_sway()
    scene.flat(seconds=1.4)
    block = street((1, 2, 3), buff=1.30)
    if block.width > cfg.SAFE_WIDTH - 1.0:
        block.scale_to_fit_width(cfg.SAFE_WIDTH - 1.0)
    scene.morph(block.move_to([0, -0.35, 0]), seconds=2.2)
    heading = scene.pin(outlined_text("AN ADDRESS", cfg.FONT["label"], cfg.GOLD).move_to([0, 3.45, 0]))
    scene.playq(FadeIn(heading, shift=DOWN * 0.10), seconds=0.7)

    focus = _FocusSweep()
    scene.add(focus)

    for target, note, colour in (
        ("roof", "house number  =  n,  the shell", cfg.GOLD),
        ("floor", "floor  =  ℓ,  the subshell   ·   s, p, d", cfg.CYAN),
        ("room", "room  =  one orbital", cfg.GREEN),
    ):
        focus.pause()
        if target == "roof":
            highlights = [block.houses[n].roof for n in (1, 2, 3)]
        elif target == "floor":
            highlights = [block.houses[n].floors[l] for n in (1, 2, 3) for l in range(n)]
        else:
            highlights = [room for n in (1, 2, 3) for room in block.houses[n].rooms.values()]
        caption = scene.pin(outlined_text(note, cfg.FONT["small"], colour, limit=11.0)
                            .move_to([0, -3.40, 0]))
        scene.playq(
            FadeIn(caption),
            LaggedStart(*(Indicate(part, color=cfg.WHITE, scale_factor=1.12)
                          for part in highlights), lag_ratio=0.06),
            seconds=3.4,
        )
        focus.focus(highlights, colour, period=1.0)
        # Indicate promotes its targets to scene roots; the reading
        # overlay must follow them in the draw order.
        scene.bring_to_front(focus)
        scene.hold(1.5)
        scene.drop(caption, seconds=0.5)

    # Keep following the room hierarchy while the analogy is qualified.
    focus.focus([room for n in (1, 2, 3)
                 for room in block.houses[n].rooms.values()], cfg.GREEN, period=1.1)
    scene.bring_to_front(focus)
    scene.cue("an analogy · a shell is not a container", cfg.MUTED, hold=2.2, position=DOWN * 3.40)
    scene.at(120)

    # -- Beat 3c: count the rooms, and Bohr's numbers come back out -----------
    # This is the chapter's quiet payoff. 2n^2 was asserted in chapter 3 as a
    # rule from school. Here it is derived: the orbitals in a shell are
    # 1 + 3 + 5 + ... = n^2, and each takes two spin states.
    counting = scene.pin(outlined_text("COUNT THE ROOMS", cfg.FONT["small"], cfg.GOLD).move_to([0, 3.45, 0]))
    scene.playq(FadeTransform(heading, counting), seconds=0.6)
    scene.local.remove(heading)
    scene.remove_fixed_in_frame_mobjects(heading)

    focus.pause()
    sums = {1: r"1 = 1^2", 2: r"1+3 = 2^2", 3: r"1+3+5 = 3^2"}
    tallies = VGroup()
    for n in (1, 2, 3):
        rooms = list(block.houses[n].rooms.values())
        line = equation(sums[n], 34, cfg.CYAN)
        line.next_to(block.houses[n], DOWN, buff=0.42)
        scene.add_fixed_in_frame_mobjects(line)
        scene.remove(line)
        tallies.add(line)
        scene.playq(
            LaggedStart(*(Indicate(room, color=cfg.GREEN, scale_factor=1.18) for room in rooms),
                        lag_ratio=0.12),
            FadeIn(line),
            seconds=2.2,
        )
    scene.local.append(tallies)

    law = scene.pin(VGroup(
        equation(r"n^2\ \text{orbitals}", 42, cfg.CYAN),
        equation(r"\times\,2\ \text{spin states}", 38, cfg.MUTED),
        equation(r"=\ 2n^2\ \text{electrons}", 44, cfg.GOLD),
    ).arrange(RIGHT, buff=0.42).move_to([0, 2.55, 0]))
    scene.playq(LaggedStart(*(FadeIn(part) for part in law), lag_ratio=0.5), seconds=2.0)

    recovered = scene.pin(VGroup(
        equation(r"2,\quad 8,\quad 18", 50, cfg.GREEN),
        outlined_text("shell capacity follows from state counting", cfg.FONT["tiny"], cfg.GREEN, limit=7.0),
    ).arrange(DOWN, buff=0.24).move_to([0, -3.30, 0]))
    scene.playq(FadeIn(recovered, shift=UP * 0.12), seconds=1.0)
    # Revisit each room while the state-counting law stays readable.
    focus.focus([room for n in (1, 2, 3)
                 for room in block.houses[n].rooms.values()], cfg.GREEN, period=1.1)
    scene.bring_to_front(focus)
    scene.hold(2.4)
    scene.at(155)
    focus.clear_updaters()
    scene.remove(focus)
    scene.drop(tallies, law, recovered, counting, seconds=0.7)

    # -- Beat 4 opens the camera again ---------------------------------------
    scene.view3d(phi=68, theta=-50, seconds=1.6)
    stop_camera_sway = _start_camera_sway(scene)
    axis = orbital_axes(3.6)
    scene.show(axis, seconds=0.5)

    # -- Beat 4: m_l, watched as a change of orientation ----------------------
    magnetic_label = scene.formula(r"m_\ell = -\ell, \ldots, 0, \ldots, +\ell",
                                   position=UP * 3.40, size=52, color=cfg.GOLD)
    scene.morph(scene.orbital(2, 1, 0, size=2.7), seconds=2.0)
    count = scene.formula(r"2\ell+1 = 3", position=DOWN * 3.35, size=50, color=cfg.CYAN)
    scene.hold(6.0)
    scene.drop(count, seconds=0.4)
    projection = scene.formula(r"L_z=m_\ell\hbar \quad (p:\ -\hbar,0,+\hbar)",
                               position=DOWN * 3.35, size=46, color=cfg.CYAN)
    scene.at(178)
    scene.drop(magnetic_label, projection, seconds=0.6)

    honest = scene.pin(outlined_text("three real patterns spanning the same three states",
                                     cfg.FONT["small"], cfg.CYAN).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(honest), seconds=0.6)
    for magnetic in (1, -1, 0):
        scene.morph(scene.orbital(2, 1, magnetic, size=2.7), seconds=2.2)
        scene.hold(2.6)
    scene.at(205)
    scene.drop(honest, seconds=0.6)

    # -- Beat 5: three labels name an orbital ---------------------------------
    address = scene.formula(r"(n,\ \ell,\ m_\ell) = (2,\ 1,\ 0)", position=UP * 3.40, size=54)
    scene.hold(6.0)
    example = scene.formula(r"2p_z:\quad L^2=2\hbar^2,\quad L_z=0",
                            position=DOWN * 3.35, size=48, color=cfg.CYAN)
    scene.at(220)
    scene.drop(address, example, seconds=0.6)

    # -- Beat 6: the fourth label belongs to the electron, not to the orbital --
    spin = scene.formula(r"m_s = +\tfrac12,\; -\tfrac12", position=UP * 3.40, size=58, color=cfg.GOLD)
    arrows = scene.pin(_spin_arrows().move_to([4.85, 0, 0]))
    scene.playq(FadeIn(arrows), seconds=0.7)
    intrinsic = scene.pin(outlined_text("intrinsic · not a little ball spinning",
                                        cfg.FONT["tiny"], cfg.MUTED).move_to([0, -3.90, 0]))
    scene.playq(FadeIn(intrinsic), seconds=0.6)
    spin_value = scene.formula(r"S_z=m_s\hbar=\pm\frac{\hbar}{2}",
                               position=DOWN * 3.10, size=48, color=cfg.GREEN)
    scene.at(241)
    scene.drop(spin, spin_value, arrows, intrinsic, axis, seconds=0.7)

    # -- Beat 7: the shorthand worth remembering ------------------------------
    scene.dissolve(VGroup(), seconds=1.0)
    stop_camera_sway()
    scene.flat(seconds=1.4)
    card = _shorthand_card()
    scene.morph(card, seconds=1.8)
    review = _FocusSweep()
    review.focus(card, cfg.GOLD, period=2.2, outline_only=True)
    scene.add(review)
    scene.at(256)
    review.clear_updaters()
    scene.playq(FadeOut(review), seconds=0.4)

    scene.finish()
