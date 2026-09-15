"""Chapter 3: what Bohr's model actually promised, in numbers.

Bohr's hydrogen model fixes a radius, an energy and a speed. School diagrams
also attach a shell capacity rule, which comes from quantum state counting
and spin, rather than from the single-electron circular model. The film revisits
each number after replacing the trajectory with a wave state.

The one failure stated here is the one the film's ending answers: nothing in a
table of fixed orbits says why two atoms should join.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    bohr_shell_atom,
    chip,
    dashed_connector,
    equation,
    glow_line,
    orbit,
    outlined_text,
)
from utils.quantum_examples import bohr_radius, bohr_speed, hydrogen_energy

SHELL_RADII = (1.35, 2.35, 3.25)
ATOM_CENTRE = np.array([-3.25, 0.0, 0.0])
NUMBER_CYAN = "#D1F5FF"
NUMBER_GOLD = "#FFE799"


class _OrbitMotion(VMobject):
    """Keep beads on their live tracks during holds, fades and atom transforms.

    This invisible driver precedes the atoms in the scene, so Cairo includes
    their moving geometry in every frame. Keeping it outside animated groups
    prevents a scale or fade from suspending the electron's motion. Track
    geometry supplies the current centre and radius after every transform.

    Periods are illustrative playback speeds, not physical time or a radius
    scale. The numerical Bohr speed is taught separately.
    """

    def __init__(self) -> None:
        super().__init__()
        self.tracks = []
        self.add_updater(self._advance)

    def follow(self, ring: Circle, beads: VGroup, period: float = 5.5) -> None:
        """Register visible beads before their atom enters the frame."""
        for index, bead in enumerate(beads):
            self.tracks.append([ring, bead, index / len(beads), period])
            # A small white centre stays visible when the atom is scaled down.
            bead.add(Dot(bead.get_center(), radius=bead.width * 0.07,
                         color=cfg.WHITE))

    def release(self, beads: VGroup) -> None:
        """Stop touching a diagram once its exit animation has completed."""
        self.tracks = [track for track in self.tracks if track[1] not in beads]

    def _advance(self, _driver: VMobject, dt: float) -> None:
        for track in self.tracks:
            ring, bead, phase, period = track
            phase = (phase + dt * cfg.SPEED / period) % 1.0
            track[2] = phase
            start = ring.point_from_proportion(0)
            centre = (start + ring.point_from_proportion(0.5)) / 2
            x_axis = start - centre
            y_axis = ring.point_from_proportion(0.25) - centre
            bead.move_to(centre + np.cos(TAU * phase) * x_axis
                         + np.sin(TAU * phase) * y_axis)


def _number(latex: str, size: int = 46, color: str = NUMBER_CYAN) -> MathTex:
    """Large, lightly reinforced maths that remain legible in a 480p preview."""
    label = equation(latex, size, color)
    label.set_stroke(color, width=0.35, opacity=1)
    return label


def _capacity_tags() -> VGroup:
    """2n^2 written out for the first four shells, as a column of plates."""
    column = VGroup()
    for n in range(1, 5):
        column.add(VGroup(
            _number(f"n={n}", 46),
            _number(rf"2n^2={2 * n * n}", 48, NUMBER_GOLD),
        ).arrange(RIGHT, buff=0.55))
    column.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
    return column


def _rung(label: str, energy: float, y: float, width: float = 2.65) -> VGroup:
    """One hydrogen energy level with its value, for the small ladder."""
    shelf = glow_line([-width / 2, y, 0], [width / 2, y, 0], cfg.CYAN, 3.4)
    name = _number(label, 44).next_to(shelf, LEFT, buff=0.30)
    value = _number(rf"{energy:.2f}\ \mathrm{{eV}}", 44, NUMBER_GOLD).next_to(shelf, RIGHT, buff=0.30)
    return VGroup(shelf, name, value)


class Scene03BohrNumbers(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("03")

    # -- Beat 1: the light we just followed came from somewhere ---------------
    # The chapter opens in three dimensions so the shells read as nested space
    # rather than as three circles printed on a card. Hydrogen, because every
    # number this chapter banks is hydrogen's: the outer shells are drawn empty
    # because they are the capacity the next beat counts, not occupancy. The
    # populated ring diagram belongs to chapter 16.
    atom = bohr_shell_atom((1, 0, 0), radii=SHELL_RADII, nucleus_radius=0.34,
                           electron_radius=0.14)
    atom.move_to(ORIGIN)
    motion = _OrbitMotion()
    scene.add(motion)
    motion.follow(atom.rings[1], atom.electrons[1])
    scene.morph(atom, seconds=2.0)
    scene.view3d(phi=62, theta=-72, seconds=2.4)

    heading = scene.pin(outlined_text("BOHR'S HYDROGEN ATOM", cfg.FONT["label"], cfg.GOLD)
                        .move_to(UP * 3.45))
    scene.playq(FadeIn(heading, shift=DOWN * 0.10), seconds=0.7)
    shell_tags = scene.pin(VGroup(*[
        _number(f"n={index}", 48) for index in (1, 2, 3)
    ]).arrange(DOWN, buff=0.42).move_to([5.15, 0.0, 0]))
    for index in (1, 2, 3):
        scene.playq(
            Indicate(atom.rings[index], color=cfg.WHITE, scale_factor=1.03),
            FadeIn(shell_tags[index - 1], shift=LEFT * 0.14),
            *[Flash(bead.get_center(), color=cfg.CYAN, flash_radius=0.18, line_length=0.11)
              for bead in atom.electrons[index]],
            seconds=1.15,
        )
    scene.turn(seconds=3.0, angle=0.42)
    scene.drop(shell_tags, seconds=0.5)
    scene.at(20)
    scene.drop(heading, seconds=0.6)
    scene.flat(seconds=1.6)

    # -- Beat 2: the capacity rule the viewer already knows from school -------
    scene.playq(scene.anchor.animate.scale(0.80).move_to(ATOM_CENTRE), seconds=1.4)
    capacities = _capacity_tags().move_to([3.55, 0.35, 0])
    holds = scene.pin(outlined_text("shell capacity · explained later", cfg.FONT["tiny"], cfg.CYAN, limit=6.3)
                      .move_to([3.55, 2.65, 0]))
    scene.show(capacities, seconds=0.9)
    scene.playq(FadeIn(holds), seconds=0.5)
    for index, row in enumerate(capacities):
        if index < 3:
            scene.playq(
                Indicate(row, color=cfg.WHITE, scale_factor=1.06),
                Indicate(scene.anchor.rings[index + 1], color=cfg.GOLD, scale_factor=1.02),
                seconds=1.05,
            )
        else:
            scene.playq(Indicate(row, color=cfg.WHITE, scale_factor=1.06), seconds=1.0)
    scene.at(36)
    scene.drop(capacities, holds, seconds=0.7)

    # -- Beat 3: a fixed distance, measured off the picture -------------------
    radii_note = scene.pin(outlined_text("FIXED RADIUS · diagram not to scale", cfg.FONT["small"], cfg.GOLD).move_to(UP * 3.45))
    scene.playq(FadeIn(radii_note), seconds=0.6)
    brackets = VGroup()
    for index, (shell, angle) in enumerate(((1, 52 * DEGREES), (2, -46 * DEGREES))):
        radius = SHELL_RADII[shell - 1] * 0.80
        tip = ATOM_CENTRE + radius * np.array([np.cos(angle), np.sin(angle), 0.0])
        arrow = DoubleArrow(ATOM_CENTRE, tip, buff=0.06, color=cfg.GOLD,
                            stroke_width=3.4, tip_length=0.16)
        value = _number(
            rf"r_{shell}={bohr_radius(shell) * 1e10:.2f}\ \text{{\AA}}", 48, NUMBER_GOLD,
        ).move_to([2.9, 1.35 - 1.5 * index, 0])
        link = dashed_connector(tip, value.get_left() + LEFT * 0.16, cfg.GOLD, dashes=9, stroke_width=2)
        brackets.add(VGroup(arrow, link, value))
    for pair in brackets:
        scene.playq(GrowFromPoint(pair[0], ATOM_CENTRE), FadeIn(pair[1]), FadeIn(pair[2]), seconds=1.5)
    scene.local.append(brackets)
    scene.hold(2.4)
    scene.at(54)
    scene.drop(brackets, radii_note, seconds=0.7)

    # -- Beat 4: a fixed energy, and the spectrum it already explained --------
    energy_note = scene.pin(outlined_text("FIXED ENERGY", cfg.FONT["small"], cfg.GOLD).move_to(UP * 3.45))
    ladder = VGroup(
        _rung("n=2", hydrogen_energy(2), 1.15),
        _rung("n=1", hydrogen_energy(1), -1.35),
    ).move_to([3.35, 0.0, 0])
    scene.playq(FadeIn(energy_note), seconds=0.5)
    scene.show(ladder, seconds=1.0)
    jump = Arrow(ladder[1][0].get_center() + RIGHT * 0.0 + UP * 0.10,
                 ladder[0][0].get_center() + DOWN * 0.10,
                 buff=0.05, color=cfg.PHOTON_COLOR, stroke_width=4,
                 max_tip_length_to_length_ratio=0.14)
    scene.show(jump, seconds=0.7)
    scene.playq(Indicate(ladder[1][2], color=cfg.WHITE, scale_factor=1.10), seconds=1.1)
    scene.playq(Indicate(ladder[0][2], color=cfg.WHITE, scale_factor=1.10), seconds=1.1)
    formula = scene.formula(r"E_n=-\frac{13.6\ \mathrm{eV}}{n^2}", position=[3.35, -2.85, 0], size=60)
    formula.set_stroke(cfg.WHITE, width=0.35, opacity=1)
    scene.at(70)
    scene.drop(ladder, jump, formula, energy_note, seconds=0.7)

    # -- Beat 5: a fixed speed -- the number chapter 4 will spend -------------
    speed_note = scene.pin(outlined_text("FIXED SPEED", cfg.FONT["small"], cfg.GOLD).move_to(UP * 3.45))
    scene.playq(FadeIn(speed_note), seconds=0.5)
    # The same electron has been moving since the opening. A short trail
    # calls attention to its speed without replacing it or stopping the clock.
    runner = atom.electrons[1][0]
    trail = TracedPath(runner.get_center, stroke_color=NUMBER_CYAN,
                       stroke_width=3.5, dissipating_time=0.50 / cfg.SPEED)
    scene.add(trail)
    scene.local.append(trail)
    value = _number(
        rf"v_1={bohr_speed(1) / 1e6:.3f}\times10^6\ \mathrm{{m/s}}", 48, NUMBER_GOLD,
    ).move_to([3.3, 0.35, 0])
    scene.show(value, seconds=0.7)
    scene.at(84)
    trail.clear_updaters()
    scene.drop(trail, value, speed_note, seconds=0.6)

    # -- Beat 6: everything fixed -- and the one question it cannot answer ----
    fixed = VGroup(*[chip(word, cfg.GOLD) for word in ("RADIUS", "ENERGY", "SPEED")])
    fixed.arrange(RIGHT, buff=0.42).move_to([0, 3.30, 0])
    scene.playq(scene.anchor.animate.scale(0.74).move_to([-3.2, -0.45, 0]),
                seconds=1.0)
    scene.pin(fixed)
    scene.playq(LaggedStart(*(FadeIn(plate, shift=DOWN * 0.10) for plate in fixed), lag_ratio=0.22), seconds=1.5)

    partner = bohr_shell_atom((1,), radii=SHELL_RADII[:1], nucleus_radius=0.34,
                              electron_radius=0.14)
    partner.scale(0.74).move_to([2.9, -0.45, 0])
    motion.follow(partner.rings[1], partner.electrons[1])
    scene.show(partner, seconds=0.9)
    scene.playq(
        scene.anchor.animate.shift(RIGHT * 0.45),
        partner.animate.shift(LEFT * 0.45),
        seconds=1.6,
        rate_func=rate_functions.ease_in_out_sine,
    )
    mark = outlined_text("?", 72, "#FF8E93").move_to([0.40, -0.45, 0])
    scene.show(mark, seconds=0.6)
    scene.cue("nothing here says why atoms join", cfg.RED, hold=2.4, position=DOWN * 3.30)
    scene.at(94)
    scene.drop(partner, mark, fixed, seconds=0.7)
    motion.release(partner.electrons[1])

    # -- Beat 7: keep one track, and hand it to de Broglie --------------------
    single = orbit(radius=2.30, nucleus_radius=0.30, electron_radius=0.16)
    motion.follow(single[1], VGroup(single[2]))
    scene.morph(single, seconds=2.0)
    motion.release(atom.electrons[1])

    scene.finish()
    # The chapter hands off a clean anchor: no external driver survives into
    # de Broglie's orbit-to-wave transformation.
    motion.clear_updaters()
    scene.remove(motion)
