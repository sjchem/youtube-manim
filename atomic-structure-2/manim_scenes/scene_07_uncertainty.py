"""Chapter 7: why a trajectory cannot survive, argued from waves rather than from clumsiness.

The chapter opens on the two numbers chapter 3 was careful to bank. Bohr gave
a classical electron a definite position and momentum vector at every instant.
Radius and speed alone do not specify those vectors. That pair is what this chapter takes
away.

It then shows the collision story -- a photon must hit the electron to locate
it, and a shorter wavelength locates better and hits harder -- because it is
the picture most viewers already carry. And then it dismantles it. If the limit
came from the collision, gentler equipment would evade it. The wave argument
that follows never measures anything: a long clean wave has a wavelength and no
location, a packet has a location and no single wavelength, and the trade is
visible in the state before any apparatus exists. The chapter puts both
distributions on screen at once and links them to a single tracker, so the
viewer watches the trade happen rather than being told about it.
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    QuantumScene,
    cross_mark,
    dashed_connector,
    glow_curve,
    equation,
    glow_dot,
    outlined_text,
    orbit,
)
from utils.physics_models import sigma_p
from utils.quantum_examples import (
    bohr_momentum,
    bohr_radius,
    bohr_speed,
    minimum_momentum_spread,
)
from manim_scenes.scientist_portraits import scientist_portrait

from manim_scenes.matter_wave_visuals import TravellingWave
from manim_scenes.uncertainty_visuals import (
    CYAN, GOLD, MINT, VIOLET, CORAL, bright_math, OrbitMotion, GaussianPanels,
)

POSITION_BASE = 1.70
MOMENTUM_BASE = -1.45
COMPONENT_OFFSETS = (-0.8, -0.4, 0.0, 0.4, 0.8)


def _width_bar(half_width: float, y: float, colour: str, label: str) -> VGroup:
    """Measure one standard deviation from the mean, not the full ±sigma span."""
    bar = DoubleArrow([0, y, 0], [half_width, y, 0], buff=0,
                      color=colour, stroke_width=5, tip_length=0.13)
    ticks = VGroup(*[
        Line([x, y - 0.11, 0], [x, y + 0.11, 0], color=colour, stroke_width=3)
        for x in (0, half_width)
    ])
    # Beside the marker, outside both the carrier and probability curves.
    tag = bright_math(label, 52, colour).next_to(bar, RIGHT, buff=0.26)
    return VGroup(bar, ticks, tag)


def _magnifier(colour: str = cfg.WHITE) -> VGroup:
    lens = Circle(radius=0.46, color=colour, stroke_width=5)
    handle = Line(lens.get_center() + np.array([0.33, -0.33, 0]),
                  lens.get_center() + np.array([0.85, -0.85, 0]), color=colour, stroke_width=7)
    return VGroup(lens, handle)


class Scene07Uncertainty(QuantumScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: QuantumScene) -> None:
    scene.prepare("07")

    # -- Beat 0: the pair Bohr claimed to hold at once ------------------------
    claim = orbit(radius=2.25, nucleus_radius=0.28, electron_radius=0.17).move_to([-3.2, -0.15, 0])
    rotation = OrbitMotion(claim)
    scene.add(rotation)
    scene.morph(claim, seconds=1.8)
    banked = scene.pin(VGroup(
        bright_math(rf"r_1={bohr_radius(1) * 1e10:.3f}\ \text{{\AA}}", 46, GOLD),
        bright_math(rf"v_1={bohr_speed(1) / 1e6:.3f}\times10^6\ \mathrm{{m/s}}", 44, MINT),
        bright_math(rf"p_1=m_e v_1={bohr_momentum(1) * 1e24:.3f}\times10^{{-24}}\ \mathrm{{kg\,m/s}}", 35, CYAN),
    ).arrange(DOWN, buff=0.46, aligned_edge=LEFT).move_to([3.95, 0.8, 0]))
    scene.playq(LaggedStart(*(FadeIn(line, shift=LEFT * 0.14) for line in banked), lag_ratio=0.6), seconds=2.6)
    both = scene.pin(outlined_text("a classical path specifies position and momentum",
                                   cfg.FONT["small"], cfg.WHITE, limit=8.6).move_to([0, 3.45, 0]))
    scene.playq(FadeIn(both), seconds=0.7)
    # A position vector reaches the marked point; momentum is tangent there.
    position = Arrow(claim[0].get_center(), claim[2].get_center(), buff=0.10,
                     color=GOLD, stroke_width=4)
    momentum = Arrow(claim[2].get_center(), claim[2].get_center() + UP * 1.35,
                     buff=0.10, color=CYAN, stroke_width=4)
    vectors = VGroup(position, momentum)
    vector_labels = VGroup(
        equation(r"\vec r", 48, GOLD).next_to(position, DOWN, buff=0.18),
        equation(r"\vec p", 48, CYAN).next_to(momentum, RIGHT, buff=0.18),
    )
    rotation.vectors = vectors
    rotation.labels = vector_labels
    rotation.advance(rotation, 0)
    scene.show(vectors, seconds=0.6)
    scene.show(vector_labels, seconds=0.4)
    scene.at(16)
    scene.drop(banked, both, vectors, vector_labels, seconds=0.7)
    rotation.vectors = rotation.labels = None

    # -- Beat 0b: the collision story, told properly and then withdrawn -------
    # This is the picture most viewers arrive with. It is worth showing, and it
    # is worth being explicit that it is not where the limit comes from.
    bead = glow_dot(ORIGIN, 0.18, CYAN)
    lens = _magnifier(cfg.WHITE).move_to([0, 2.05, 0])
    scene.morph(VGroup(bead, lens), seconds=1.6)
    rotation.clear_updaters()
    scene.remove(rotation)

    for wavenumber, kick, note, colour in ((26, 2.15, "short λ · sharp position, hard kick", CORAL),
                                           (7, 0.75, "long λ · soft kick, blurred position", cfg.WHITE)):
        incoming = TravellingWave(width=3.6, k=wavenumber, amplitude=0.30,
                        center=[-5.1, 0, 0], color=cfg.PHOTON_COLOR)
        scene.add(incoming)
        travel = ValueTracker(-5.1)
        incoming.add_updater(lambda mob: mob.wave_center.__setitem__(0, travel.get_value()))
        scene.playq(travel.animate.set_value(-1.1), seconds=1.2, rate_func=linear)
        incoming.clear_updaters()
        scene.playq(Flash(ORIGIN, color=cfg.PHOTON_COLOR, flash_radius=0.42), FadeOut(incoming), seconds=0.5)
        recoil = Arrow(ORIGIN, [kick, 0.55 * kick / 2.15, 0], buff=0.14, color=colour,
                       stroke_width=4, max_tip_length_to_length_ratio=0.22)
        tag = outlined_text(note, cfg.FONT["tiny"] - 4, colour, limit=6.4).move_to([0, -2.75, 0])
        scene.playq(GrowArrow(recoil), FadeIn(tag),
                    bead.animate.shift(RIGHT * kick * 0.45), seconds=1.0)
        scene.hold(1.4)
        scene.playq(FadeOut(recoil), FadeOut(tag), bead.animate.move_to(ORIGIN), seconds=0.5)

    withdraw = scene.pin(outlined_text("but this blames the apparatus", cfg.FONT["small"], CORAL)
                         .move_to([0, 3.45, 0]))
    scene.playq(FadeIn(withdraw), seconds=0.6)
    scene.hold(1.5)
    scene.playq(FadeOut(lens), seconds=0.8)
    scene.at(40)
    scene.drop(withdraw, seconds=0.6)

    # -- Beat 1: a perfectly definite wavelength, and no location at all ------
    clean_wave = TravellingWave(width=12, k=6, amplitude=0.6, color=CYAN)
    scene.morph(clean_wave, seconds=1.6)
    connection = scene.formula(r"p=\hbar k,\qquad k=\frac{2\pi}{\lambda}", position=UP * 3.15, size=54, color=GOLD)
    everywhere = scene.pin(outlined_text("one wavelength · no single place",
                                         cfg.FONT["small"], CYAN).move_to([0, -2.6, 0]))
    wavelength = scene.pin(_width_bar(TAU / 6, 1.35, GOLD, r"\lambda"))
    scene.playq(FadeIn(everywhere), FadeIn(wavelength), seconds=0.7)
    scene.at(55)
    scene.drop(everywhere, connection, wavelength, seconds=0.6)

    # -- Beat 2: add neighbouring wavelengths ---------------------------------
    components = VGroup(*[
        TravellingWave(width=11, k=6 + offset, amplitude=0.24,
                       color=(CYAN, MINT, GOLD, VIOLET, CORAL)[index],
                       center=UP * (1.85 - index * 0.72))
        for index, offset in enumerate(COMPONENT_OFFSETS)
    ])
    scene.morph(components, seconds=2.6)
    clean_wave.clear_updaters()
    adding = scene.pin(outlined_text("several wavelengths, added together",
                                     cfg.FONT["small"], cfg.WHITE).move_to([0, -3.3, 0]))
    scene.playq(FadeIn(adding), seconds=0.6)
    scene.at(68)
    scene.drop(adding, seconds=0.5)

    # -- Beat 3: the two linked distributions ---------------------------------
    width = ValueTracker(2.0)
    panels = GaussianPanels(width)
    scene.dissolve(panels, seconds=2.2)
    components.clear_updaters()

    titles = VGroup(
        outlined_text("POSITION", cfg.FONT["tiny"], CYAN).move_to([-5.35, 3.05, 0]),
        outlined_text("MOMENTUM", cfg.FONT["tiny"], VIOLET).move_to([-5.25, -0.35, 0]),
    )
    scene.show(titles, seconds=0.8)
    scene.playq(width.animate.set_value(0.45), seconds=9.5, rate_func=rate_functions.ease_in_out_sine)
    scene.at(92)

    # -- Beat 4: name the two widths, and let them measure themselves ---------
    delta_x = always_redraw(lambda: _width_bar(width.get_value(), 0.35, CYAN, r"\Delta x"))
    delta_p = always_redraw(
        lambda: _width_bar(float(sigma_p(width.get_value())), -2.30, VIOLET, r"\Delta p")
    )
    scene.show(VGroup(delta_x, delta_p), seconds=0.9)
    scene.playq(width.animate.set_value(1.9), seconds=8.5, rate_func=rate_functions.ease_in_out_sine)
    scene.playq(width.animate.set_value(0.38), seconds=8.5, rate_func=rate_functions.ease_in_out_sine)
    scene.at(121)

    # -- Beat 5: Heisenberg, and the spread relation inherited from waves -----
    panels.clear_updaters()
    delta_x.clear_updaters()
    delta_p.clear_updaters()
    scene.drop(titles, delta_x, delta_p, seconds=0.6)
    scene.dissolve(VGroup(), seconds=0.6)
    portrait = scene.pin(scientist_portrait("heisenberg.jpg", "Werner Heisenberg"))
    scene.playq(FadeIn(portrait), seconds=0.7)
    law = scene.headline(r"\Delta x\,\Delta p \geq \frac{\hbar}{2}", position=[2.1, 0.65, 0])
    fourier = scene.formula(r"\Delta x\,\Delta k\geq\frac12,\quad p=\hbar k",
                            position=[2.1, -1.35, 0], size=40, color=CYAN)
    scene.hold(2.0)
    scene.drop(portrait, fourier, seconds=0.6)
    scene.playq(law.animate.move_to(UP * 3.30), seconds=0.7)
    scene.at(129)

    # -- Beat 6: a Gaussian example with SI values ----------------------------
    # Width 1 on the plot represents 100 pm. The momentum scale is reciprocal;
    # the two curves have separate axes, with peak heights rescaled for clarity.
    width.set_value(1.0)
    compact = GaussianPanels(width, scale=0.55, center=[-3.6, 0, 0])
    scene.morph(compact, seconds=1.0)
    tags = scene.show(VGroup(
        outlined_text("POSITION", 30, CYAN).move_to([-3.6, 1.8, 0]),
        outlined_text("MOMENTUM", 30, VIOLET).move_to([-3.6, -1.6, 0]),
    ), seconds=0.5)
    spread_x = VGroup(
        MathTex(r"\Delta x=", font_size=48, color=CYAN),
        DecimalNumber(100, num_decimal_places=0, font_size=48, color=CYAN),
        MathTex(r"\mathrm{pm}", font_size=48, color=CYAN),
    )

    def update_position_readout(group: VGroup) -> None:
        group[1].set_value(100 * width.get_value())
        group.arrange(RIGHT, buff=0.12).move_to([3.25, 1.25, 0])

    spread_x.add_updater(update_position_readout)
    spread_x.update(0)
    scene.show(spread_x, seconds=0.8)
    # A fixed exponent makes doubling visible as 5.27 -> 10.55. Update numbers
    # from the physical width rather than morphing whole formula glyphs.
    value_row = VGroup(
        DecimalNumber(5.27, num_decimal_places=2, font_size=44, color=VIOLET),
        MathTex(r"\times10^{-25}\ \mathrm{kg\,m/s}", font_size=38, color=VIOLET),
    )
    spread_p = VGroup(
        MathTex(r"\Delta p_{\min}\approx", font_size=42, color=VIOLET).move_to([3.25, 0.35, 0]),
        value_row,
    )

    def update_momentum_readout(group: VGroup) -> None:
        group[1][0].set_value(minimum_momentum_spread(width.get_value() * 100e-12) / 1e-25)
        group[1].arrange(RIGHT, buff=0.12).move_to([3.25, -0.35, 0])

    spread_p.add_updater(update_momentum_readout)
    spread_p.update(0)
    scene.show(spread_p, seconds=0.8)
    gaussian = scene.pin(outlined_text("Gaussian · minimum spread", 30, cfg.WHITE).move_to([3.25, -1.45, 0]))
    scene.playq(FadeIn(gaussian), seconds=0.5)
    scene.at(139)
    scene.playq(width.animate.set_value(0.5), seconds=5.0, rate_func=rate_functions.ease_in_out_sine)
    scene.at(150)
    spread_x.clear_updaters()
    spread_p.clear_updaters()
    scene.drop(tags, spread_x, spread_p, gaussian, seconds=0.7)
    scene.cue("a property of the state", color=GOLD, hold=2.4, position=DOWN * 3.4)
    scene.at(160)
    scene.drop(law, seconds=0.6)

    # -- Beat 7: so the planetary picture loses what it was built on ----------
    atom = orbit()
    rotation = OrbitMotion(atom)
    scene.add(rotation)
    scene.morph(atom, seconds=2.6)
    compact.clear_updaters()
    demand = VGroup(
        outlined_text("a trajectory needs both, exactly, at every instant",
                      cfg.FONT["small"], GOLD),
    ).move_to([0, -3.35, 0])
    markers = VGroup(
        Circle(radius=0.26, color=GOLD, stroke_width=3.4).move_to([2.3, 0, 0]),
        Arrow([2.3, 0, 0], [2.3, 1.45, 0], buff=0.12, color=GOLD, stroke_width=4.5),
    )
    rotation.marker = markers
    rotation.advance(rotation, 0)
    scene.show(VGroup(markers, demand), seconds=0.9)
    scene.hold(2.6)
    scene.playq(
        markers.animate.set_color(CORAL).set_opacity(0.25),
        atom[1].animate.set_stroke(color=CORAL, opacity=0.35),
        seconds=1.8,
    )
    scene.at(174)
    scene.drop(markers, demand, seconds=0.7)
    rotation.marker = None

    # -- Beat 8: the replacement question is already on the screen ------------
    replacement_packet = GaussianPanels(ValueTracker(0.8))
    scene.morph(replacement_packet, seconds=2.6)
    rotation.clear_updaters()
    scene.remove(rotation)
    replacement = scene.pin(outlined_text("which wave states can exist?",
                                          cfg.FONT["small"], CYAN).move_to([0, -3.45, 0]))
    scene.playq(FadeIn(replacement), seconds=0.7)
    scene.at(191)
    scene.drop(replacement, seconds=0.6)
    scene.morph(TravellingWave(width=9, k=PI / 3, amplitude=1.1, color=CYAN), seconds=2.4)
    replacement_packet.clear_updaters()

    scene.finish()
    scene.anchor.clear_updaters()
